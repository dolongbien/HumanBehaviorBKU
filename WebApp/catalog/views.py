from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.core.files.storage import FileSystemStorage
from django.views import View
from django.conf import settings
from django.core import files
from django.utils.text import slugify
import time
# A view function, or view for short, 
# is simply a Python function that takes a Web request and returns a Web response. 
# This response can be the HTML contents of a Web page, or a redirect, or a 404 error,
# or an XML document, or an image . . . or anything, really.
from django.views import generic
from .models import Video
from .forms import VideoForm
from .tasks import extract_feature, my_task

import os
import json
import glob
import urllib.request
import tempfile
from pytube import YouTube

from c3d.extract_feature import load_npy, extract_feature_video
from c3d.plot_controller import get_score
from c3d.configuration import weight_default_path, weight32_path, weight64_path
from catalog.utils.utils import load_annotation, format_filesize, url_downloadable, write_file, get_basename

def index(request):
    """View function for home page of site."""

    # Number of visits to this view, as counted in the session variable.
    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits+1

    # Render the HTML template index.html with the data in the context variable.
    print(request.path)
    
    return render(
        request,
        'index.html',
        context={
            'num_visits': num_visits,
            }
    )

class VideoListView(generic.TemplateView):
    template_name = 'catalog/video_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        action = context['video_action']

        gifs = sorted(glob.glob('media/gifs/{}/*.gif'.format(action)))
        for i, value in enumerate(gifs):
            title = os.path.basename(value)[:-4]
            video = {'url': '/catalog/video/{}/'.format(action) + title, 'basename': title, 'title': title[:-5]}
            gifs[i] = video

        # update context
        context['gifs'] = gifs
        context['action'] = action
        return context


class VideoDetailView(generic.TemplateView):
    template_name = 'catalog/video_detail.html'

    def get_context_data(self, **kwargs):
        
        context = super().get_context_data(**kwargs)
        title = context['video_title'] # title from URL
        video_type = context['video_type']

        video_path = 'media/videos/{}/{}.mp4'.format(video_type, title)
        context['video'] = {'url': '/media/videos/{}/{}.mp4'.format(video_type, title), 'title': title, 'video_path': video_path}

        # Temporal annotation
        annotation_path = 'media/videos/{}/{}.mat'.format(video_type, title)
        temporal_array = load_annotation(annotation_path)
        context['annotation'] = json.dumps(temporal_array.tolist())
        x, scores = get_score(video_path)
        scores = json.dumps(scores.tolist())
        context['scores'] = scores

        context['weight32_path'] = weight32_path
        context['weight64_path'] = weight64_path
        context['weight_default_path'] = weight_default_path

        return context

class C3dNewView(generic.TemplateView):
    template_name = 'catalog/video_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        title = context['video_title']
        video = Video.objects.get(title = title)
        context['video'] = {'url': video.file.url, 'title': title, 'id': video.id, 'video_path': video.file.url[1:]}
        annotation_path = 'media/videos/abnormal/{}.mat'.format(title)
        context['annotation'] = json.dumps(load_annotation(annotation_path).tolist())
        context['c3dnew'] = True

        filename_npy = settings.MEDIA_ROOT + video.file_score32.name
        print(filename_npy)
        
        if os.path.exists(filename_npy):
            scores = load_npy(filename_npy)
            scores = scores.tolist()
            
            context['scores'] = scores

        return context
    
    def post(self, request):
        video_path = request.POST.get('video_path')
        no_segment = request.POST.get('no_segment')

        x, scores = get_score(video_path, weights_path, int(no_segment))
        scores = scores.tolist()
        data = {'is_valid': True, 'scores': scores}
        return JsonResponse(data)


class VideoUploadView(View):
    def get(self, request):
        # Order by descent of uploaded time
        videos_list = Video.objects.order_by('-uploaded_at')
        return render(self.request, 'catalog/video_upload.html', {'videos': videos_list})

    def post(self, request):
        """
        Post from form blue-upload or url.
        """
        #time.sleep(1)  # You don't need this line. This is just to delay the process so you can see the progress bar testing locally.
        url = request.POST.get('url')
        filename = request.POST.get('filename')

        response = {'is_valid': False}

        form = VideoForm(self.request.POST, self.request.FILES)
        if form.is_valid():
            video = form.save()
            video.filesize = format_filesize(video.file.size)
            video.title = get_basename(video.file.name)
            video.save()
            response = {'is_valid': True, 'name': video.file.name, 'url': video.file.url, 'id': video.id, 'filesize': video.filesize, 'title': video.title}
        elif url:
            url_response = urllib.request.urlopen(url)
            url_info = url_response.info()
            if 'youtube.com' in url:
                yt = YouTube(url)
                if filename == '':
                    filename = slugify(yt.title)
                video = Video()
                video.title = filename
                video.file.name = 'videos/upload/'+ filename + '.mp4'
                yt.streams.filter(progressive=True, file_extension='mp4', fps= 30).order_by('resolution').desc().first().download('media/videos/upload/', filename)
                video.filesize = format_filesize(video.file.size)
                video.save()
                response = {'is_valid': True, 'name': video.file.name, 'url': video.file.url, 'id': video.id, 'filesize': video.filesize, 'title': video.title}
            if 'video' in url_info.get_content_type():
                temp_video = tempfile.NamedTemporaryFile()
                write_file(temp_video, url_response)

                video = Video()
                video.file.save(filename, files.File(temp_video))
                video.filesize = format_filesize(video.file.size)
                video.title = get_basename(video.file.name)
                video.save()
                response = {'is_valid': True, 'name': video.file.name, 'url': video.file.url, 'id': video.id, 'filesize': video.filesize, 'title': video.title}


        # Extract Feature in Celery
        if response['is_valid'] == True:
            print(video.id)
            task = extract_feature.delay(video.id)
            video.task_id = task.task_id
            video.save()
            response['task_id'] = task.task_id

        return JsonResponse(response)

class GetScoreView(View):
    def post(self, request):
        isC3Dnew = request.POST.get('isC3Dnew')
        video_path = request.POST.get('video_path')
        weights_path = request.POST.get('weights_path')
        no_segment = request.POST.get('no_segment')
 
        # isC3Dnew js 'true' 
        if isC3Dnew == 'true':
            id = request.POST.get('id')
            video = Video.objects.get(id = id)
            # scores = extract_feature_video(video_path, int(no_segment))
            if int(no_segment) == 32:
                filename_npy = video.file_score32.url[1:]
            elif int(no_segment) == 64:
                filename_npy = video.file_score64.url[1:]

            scores = load_npy(filename_npy)
        else:
            x, scores = get_score(video_path, weights_path, int(no_segment))
        scores = scores.tolist()
        data = {'is_valid': True, 'scores': scores}
        return JsonResponse(data)

class DeleteVideoView(View):
    def post(self, request):
        response = {'success': False}
        print(request.POST)
        if request.POST.get('delete_all'):
            videos = Video.objects.all()
            for video in videos:
                video.file.delete()
                video.file_score32.delete()
                video.file_score64.delete()
                video.delete()
            videos.delete()
            response = {'success': True}
        else:
            # file_names = request.POST.getlist('files[]')
            ids = request.POST.getlist('ids[]')
            for id in ids:
                video = Video.objects.get(id = id)
                video.file.delete()
                video.file_score32.delete()
                video.file_score64.delete()
                video.delete()
            response = {'success': True}
            
        return JsonResponse(response)


class AboutView(View):
    def get(self, request):
        return render(self.request, 'catalog/about.html')

class ContactView(View):
    def get(self, request):
        return render(self.request, 'catalog/contact.html')

class DatasetView(View):
    def get(self, request):
        return render(self.request, 'catalog/dataset.html')

class ResultView(View):
    def get(self, request):
        return render(self.request, 'catalog/result.html')


from celery.result import AsyncResult
from .tasks import add 
def progress_view(request):
    result = my_task.delay(100)
    return render(request, 'catalog/progress.html', context={'task_id': result.task_id})