# Abnormal Traffic Detection

## Overview

This web application demo Abnormal Traffic Detection. User can upload video to detect abnormal traffic like road accident,...

The main features that have currently been implemented are:

* There are models for video.
* Users can view list and detail information video's demo.
* Users can upload a video, the system will score for this video and plot the result.
* Users can change between segment 32 with segment 64.
### Video Demo Use-Case
![USER CASE](https://raw.githubusercontent.com/mdn/django-locallibrary-tutorial/master/catalog/static/images/DemoVideo.pdf)
### Upload Use-Case
![USER CASE](https://raw.githubusercontent.com/mdn/django-locallibrary-tutorial/master/catalog/static/images/LinkYoutube.pdf)

## Quick Start

To get this project up and running locally on your computer:
1. Install [rabbitmq][https://www.rabbitmq.com/download.html] and run as background service.

1. Set up the [Python development environment](https://developer.mozilla.org/en-US/docs/Learn/Server-side/Django/development_environment).
   We recommend using a Python virtual environment.
   ```
   conda create -n DjangoEnv
   source activate DjangoEnv
   ```
1. Install necessary file
    -  Download file https://github.com/adamcasson/c3d/releases/download/v0.1/sports1M_weights_tf.h5, rename and save in 'c3d/trained_models/c3d_sports1m.h5'
1. Install neccesary package:
```
   pip3 install -r requirements.txt
```
1. Open new terminal and run in virtualen had created and run celery worker server. The celery will worker like the queue, extract feature video.
```
    celery -A locallibrary worker -l info
```
1. Open orther terminal with DjangoEnv enviroment. Assuming you have Python setup, run the following commands (if you're on Windows you may use `py` or `py -3` instead of `python` to start Python):
   ```
   python3 manage.py makemigrations
   python3 manage.py migrate
   python3 manage.py collectstatic
   python3 manage.py test # Run the standard tests. These should all pass.
   python3 manage.py createsuperuser # Create a superuser
   python3 manage.py runserver
   ```
1. Open tab to `http://127.0.0.1:8000` to see the main site, with your new objects.