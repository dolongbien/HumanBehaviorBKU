from __future__ import unicode_literals

from django.db import models

class Video(models.Model):
    title = models.CharField(max_length=255, blank=True)
    filesize = models.CharField(max_length=10, blank=True)
    file = models.FileField(upload_to='videos/upload/')
    uploaded_at = models.DateTimeField(auto_now_add=True)