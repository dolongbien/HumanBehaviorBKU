# Create your tasks here
from __future__ import absolute_import, unicode_literals
from celery import shared_task
from django.conf import settings

import numpy as np
from .models import Video
from c3d.extract_feature import load_npy, extract_feature_video
from celery_progress.backend import ProgressRecorder
from catalog.utils.utils import get_basename
import time

@shared_task
def add(x, y):
    return x + y


@shared_task
def mul(x, y):
    return x * y


@shared_task
def xsum(numbers):
    return sum(numbers)

@shared_task(bind=True)
def extract_feature(self, video_id):
    progress_recorder = ProgressRecorder(self)
    video = Video.objects.get(id = video_id)
    video_path =  settings.MEDIA_ROOT + video.file.name
    score32 = extract_feature_video(video_path, progress_recorder, 32)
    score64 = extract_feature_video(video_path, progress_recorder, 64)
    file_score32 = 'media/features/' + get_basename(video.file.name) + '_32.npy'
    file_score64 = 'media/features/' + get_basename(video.file.name) + '_64.npy'
    np.save(file_score32, score32)
    np.save(file_score64, score64)
    video.file_score32.name = file_score32[6:]
    video.file_score64.name = file_score64[6:]
    video.save()
    return 'done'

@shared_task(bind=True)
def my_task(self, seconds):
    progress_recorder = ProgressRecorder(self)
    for i in range(seconds):
        time.sleep(1)
        progress_recorder.set_progress(i + 1, seconds)
    return 'done'