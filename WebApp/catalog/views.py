from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.core.files.storage import FileSystemStorage
from django.views import View
from django.conf import settings
from celery import shared_task
from celery_progress.backend import ProgressRecorder
import time
import scipy.io
# A view function, or view for short, 
# is simply a Python function that takes a Web request and returns a Web response. 
# This response can be the HTML contents of a Web page, or a redirect, or a 404 error,
# or an XML document, or an image . . . or anything, really.
from django.views import generic
from .models import Video
from .forms import VideoForm

import os
import json
import glob

from c3d.extract_feature import load_npy, extract_feature_video
from .plot_controller import get_score
from .utils import load_annotation, format_filesize
from .config import * # all config variables (weight, segment, other options, ...)

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
        context={'num_books': '/num_books', 'num_instances': 'num_instances',
                 'num_instances_available': 'num_instances_available', 'num_authors': 'num_authors',
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
            video = {'url': '/catalog/video/{}/'.format(action) + title, 'title': title}
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

        weight32_paths = sorted(glob.glob('c3d/trained_models/weights_32*'))
        weight64_paths = sorted(glob.glob('c3d/trained_models/weights_64*'))
        context['weight32_paths'] = weight32_paths
        context['weight64_paths'] = weight64_paths
        context['weight_default_path'] = weight_default_path

        return context

class C3dNewView(generic.TemplateView):
    template_name = 'catalog/video_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        title = context['video_title']
        context['video'] = {'url': '/media/videos/{}.mp4'.format(title), 'title': title}
        annotation_path = 'media/videos/abnormal/{}.mat'.format(title)
        context['annotation'] = load_annotation(annotation_path)

        filename_npy = 'media/features/{}.npy'.format(title)
        filename_mp4 = 'media/videos/{}.mp4'.format(title)
        
        if os.path.exists(filename_npy):
            predictions = load_npy(filename_npy)
            scores = json.dumps(predictions.tolist())
            
            context['scores'] = scores
        else:
            if os.path.exists(filename_mp4):
                extract_feature_video(filename_mp4)
                predictions = load_npy(filename_npy)
                scores = json.dumps(predictions.tolist())
                context['scores'] = scores
            else:
                context['message'] = 'File {}.mp4 not found!'.format(title)
        return context

class VideoUploadView(View):
    def get(self, request):
        # Order by descent of uploaded time
        videos_list = Video.objects.order_by('-uploaded_at')
        for video in videos_list:
            video.file.filename = os.path.splitext(os.path.basename(video.file.name))[0]
        return render(self.request, 'catalog/video_upload.html', {'videos': videos_list})

    def post(self, request):
        time.sleep(1)  # You don't need this line. This is just to delay the process so you can see the progress bar testing locally.
        form = VideoForm(self.request.POST, self.request.FILES)
        if form.is_valid():
            print(form)
            video = form.save()
            video.filesize = format_filesize(video.file.size)
            video.save()
            data = {'is_valid': True, 'name': video.file.name, 'url': video.file.url, 'id': video.id, 'filesize': video.filesize}
            # if os.path.splitext(video.file.name)[1] == '.mp4':
            #     extract_feature_video('media/' + video.file.name)
        else:
            data = {'is_valid': False}
        return JsonResponse(data)

class GetScoreView(View):
    def post(self, request):
        video_path = request.POST.get('video_path')
        weights_path = request.POST.get('weights_path')
        x, scores = get_score(video_path, weights_path)
        scores = scores.tolist()
        data = {'is_valid': True, 'scores': scores}
        return JsonResponse(data)

class SettingsView(View):
    pass

class DeleteVideoView(View):
    def post(self, request):
        if request.POST.get('delete_all'):
            Video.objects.all().delete()
        else:
            # file_names = request.POST.getlist('files[]')
            ids = request.POST.getlist('ids[]')
            for id in ids:
                video = Video.objects.get(id = id)
                video.file.delete()
                video.delete()
            
        return JsonResponse({'success': True})


def get_progress(request, task_id):
    result = AsyncResult(task_id)
    response_data = {
        'state': result.state,
        'details': result.info,
    }
    return HttpResponse(json.dumps(response_data), content_type='application/json')

from celery import shared_task, current_task, task, Celery
from celery.result import AsyncResult
from celery_progress.backend import Progress
import time


app = Celery('catalog', broker='redis:///0')

@app.task
def my_task(seconds):
    print('SEF', seconds)
    """ Get some rest, asynchronously, and update the state all the time """
    for i in range(100):
        time.sleep(0.1)
        current_task.update_state(state='PROGRESS',
            meta={'current': i, 'total': 100})

def progress_view(request):
    result = my_task.delay(10)
    return render(request, 'catalog/progress.html', context={'task_id': result.task_id})