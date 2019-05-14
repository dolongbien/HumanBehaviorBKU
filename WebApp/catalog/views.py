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
from .utils import load_annotation

def index(request):
    """View function for home page of site."""

    # Number of visits to this view, as counted in the session variable.
    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits+1

    # Render the HTML template index.html with the data in the context variable.
    
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

        video_gifs = sorted(glob.glob('media/gifs/*.gif'))
        for i, value in enumerate(video_gifs):
            title = os.path.basename(value)[:-4]
            video = {'url': '/catalog/video/anormaly/' + title, 'title': title}
            video_gifs[i] = video
        context['video_gifs'] = video_gifs
        return context


class VideoDetailView(generic.TemplateView):
    template_name = 'catalog/video_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        title = context['video_title'] # title from URL
        print(title)
        context['video'] = {'url': '/media/videos/anormaly/{}.mp4'.format(title), 'title': title}

        filename_npy = 'media/features/{}.npy'.format(title)
        context['video'] = {'url': '/media/videos/anormaly/{}.mp4'.format(title), 'title': title}
        filename_mp4 = 'media/videos/anormaly/{}.mp4'.format(title)

        # Temporal annotation
        annotation_path = 'media/videos/anormaly/{}.mat'.format(title)
        temporal_array = load_annotation(annotation_path)
        print(annotation_path)
        context['annotation'] = json.dumps(temporal_array.tolist())
        # Abnormal SCORE
        # get scores by feature file txt
        
        x, scores = get_score(filename_mp4)
        scores = json.dumps(scores.tolist())
        context['scores'] = scores

        # get score by extracture from c3d keras
        # print(os.path.exists(filename_npy))
        # if os.path.exists(filename_npy):
        #     predictions = load_npy(filename_npy)
        #     scores = json.dumps(predictions.tolist())
            
        #     context['scores'] = scores
        # else:
        #     if os.path.exists(filename_mp4):
        #         extract_feature_video(filename_mp4)
        #         predictions = load_npy(filename_npy)
        #         scores = json.dumps(predictions.tolist())
        #         context['scores'] = scores
        #     else:
        #         context['message'] = 'File {}.mp4 not found!'.format(title)
        return context

class C3dNewView(generic.TemplateView):
    template_name = 'catalog/video_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        title = context['video_title']
        context['video'] = {'url': '/media/videos/{}.mp4'.format(title), 'title': title}

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
        videos_list = Video.objects.all()
        for video in videos_list:
            video.file.basename = video.file.name[7:-4]
        return render(self.request, 'catalog/video_upload.html', {'videos': videos_list})

    def post(self, request):
        time.sleep(1)  # You don't need this line. This is just to delay the process so you can see the progress bar testing locally.
        form = VideoForm(self.request.POST, self.request.FILES)
        if form.is_valid():
            video = form.save()
            data = {'is_valid': True, 'name': video.file.name, 'url': video.file.url}
            if os.path.splitext(video.file.name)[1] == '.mp4':
                extract_feature_video('media/' + video.file.name)
        else:
            data = {'is_valid': False}
        return JsonResponse(data)

class SettingsView(View):
    def get(self, request):
        # videos_list = Video.objects.all()
        return render(self.request, 'catalog/settings.html')

    def post(self, request):
        # time.sleep(1)  # You don't need this line. This is just to delay the process so you can see the progress bar testing locally.
        # form = VideoForm(self.request.POST, self.request.FILES)
        # if form.is_valid():
        #     video = form.save()
        #     data = {'is_valid': True, 'name': video.file.name, 'url': video.file.url}
        # else:
        #     data = {'is_valid': False}
        # return JsonResponse(data)
        pass

def clear_database(request):
    for photo in Photo.objects.all():
        photo.file.delete()
        photo.delete()
    return redirect(request.POST.get('next'))


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