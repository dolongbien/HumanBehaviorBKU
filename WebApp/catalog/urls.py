from django.urls import path, include
from django.conf.urls import url

from . import views

app_name = 'catalog'
urlpatterns = [
    path('', views.index, name='index'),
    path('videos/', views.VideoListView.as_view(), name='videos'),
    # parameter at video detail <str:video_title>, it WORKS EVEN for invalid video string title
    # video_title parameter can be invoked in corresponding VIEW later then 
    path('video/anormaly/<str:video_title>', views.VideoDetailView.as_view(), name='video-detail'),
    path('video/normal/<str:video_title>', views.VideoDetailView.as_view(), name='video-detail'),
    path('c3d-new/<str:video_title>', views.C3dNewView.as_view(), name='c3d-new'),
    path('video-upload', views.VideoUploadView.as_view(), name='video-upload'),
    path('settings', views.SettingsView.as_view(), name='settings'),
    path('progress', views.progress_view, name='progress'),
    url(r'^clear/$', views.clear_database, name='clear_database'),
]