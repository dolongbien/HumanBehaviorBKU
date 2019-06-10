from __future__ import unicode_literals

from django.db import models

class Video(models.Model):
    title = models.CharField(max_length=255, blank=True)
    filesize = models.CharField(max_length=10, blank=True)
    file = models.FileField(upload_to='videos/upload/')
    file_score32 = models.FileField(upload_to='features/', default="")
    file_score64 = models.FileField(upload_to='features/', default="")
    uploaded_at = models.DateTimeField(auto_now_add=True)
    task_id = models.CharField(max_length=50, default='')