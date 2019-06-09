
from keras.regularizers import l2
import numpy as np
import numpy.matlib
from keras.models import Sequential
from keras.layers import Dense, Dropout
from keras.regularizers import l2
import os, sys
from os import listdir
from keras import backend as K # to clear session each time reloading

import cv2

from c3d.classifier import conv_dict, load_weights
from c3d.configuration import weight_default_path, feature32_alias, no_segment, feature64_alias, feature32_alias # all config variables (weight, segment, other options, ...)

import scipy.io
from math import factorial
from scipy.io import loadmat, savemat

seed = 7
np.random.seed(seed)


def classifier_model():
    model = Sequential()
    model.add(Dense(512, input_dim=4096, kernel_initializer='glorot_normal', kernel_regularizer=l2(0.001), activation='relu'))
    model.add(Dropout(0.6))
    model.add(Dense(32, kernel_initializer='glorot_normal', kernel_regularizer=l2(0.001)))
    model.add(Dropout(0.6))
    model.add(Dense(1, kernel_initializer='glorot_normal', kernel_regularizer=l2(0.001), activation='sigmoid'))
    return model

def load_model():
    model = classifier_model()
    return model

# Load Video

def get_score(video_path, weights_path = weight_default_path, no_segment = no_segment):

    if K.backend() == 'tensorflow':
        K.clear_session()

    # K.clear_session()
    # model_path = model_dir + model_name
    model = load_model()
    load_weights(model, weights_path)

    cap = cv2.VideoCapture(video_path)

    Total_frames = cap.get(cv2.CAP_PROP_FRAME_COUNT)
    total_segments = np.linspace(1, Total_frames, num=(no_segment+1))
    total_segments = total_segments.round()

    if no_segment == 64:
        feature_alias = feature64_alias
    else:
        feature_alias = feature32_alias

    FeaturePath=(video_path)
    FeaturePath = FeaturePath[0:-4]
    FeaturePath = FeaturePath.replace('videos/normal', 'features')
    FeaturePath = FeaturePath.replace('videos/abnormal', 'features')
    FeaturePath = FeaturePath+ feature_alias

    inputs = load_one_video_features(FeaturePath)
    predictions = model.predict_on_batch(inputs)

    Frames_Score = []
    count = -1
    for iv in range(0, no_segment):
        F_Score = np.matlib.repmat(predictions[iv],1,(int(total_segments[iv+1])-int(total_segments[iv])))
        count = count + 1
        if count == 0:
            Frames_Score = F_Score
        if count > 0:
            Frames_Score = np.hstack((Frames_Score, F_Score))

    print ("Anomaly Prediction")
    x = np.linspace(1, Total_frames, Total_frames)
    scores = Frames_Score
    scores1=scores.reshape((scores.shape[1],))
    scores1 = savitzky_golay(scores1, 101, 3)
    return x, scores1


def load_one_video_features(Test_Video_Path):
    
    VideoPath =Test_Video_Path
    f = open(VideoPath, "r")
    words = f.read().split()
    num_feat = len(words) / 4096
    # Number of features per video to be loaded. In our case num_feat=32, as we divide the video into 32 segments. Npte that
    # we have already computed C3D features for the whole video and divide the video features into 32 segments.

    count = -1
    VideoFeatues = []
    for feat in range(0, int(num_feat)):
        feat_row1 = np.float32(words[feat * 4096:feat * 4096 + 4096])
        count = count + 1
        if count == 0:
            VideoFeatues = feat_row1
        if count > 0:
            VideoFeatues = np.vstack((VideoFeatues, feat_row1))
    AllFeatures = VideoFeatues

    return  AllFeatures



def savitzky_golay(y, window_size, order, deriv=0, rate=1):
    """
    Savitzky Golay filter for smoothing the score
    """
    window_size = np.abs(np.int(window_size))
    order = np.abs(np.int(order))
    #except ValueError, msg:
    #    raise ValueError("window_size and order have to be of type int")

    if window_size % 2 != 1 or window_size < 1:
        raise TypeError("window_size size must be a positive odd number")

    if window_size < order + 2:
        raise TypeError("window_size is too small for the polynomials order")

    order_range = range(order + 1)

    half_window = (window_size - 1) // 2
    b = np.mat([[k ** i for i in order_range] for k in range(-half_window, half_window + 1)])
    m = np.linalg.pinv(b).A[deriv] * rate ** deriv * factorial(deriv)
    firstvals = y[0] - np.abs(y[1:half_window + 1][::-1] - y[0])
    lastvals = y[-1] + np.abs(y[-half_window - 1:-1][::-1] - y[-1])
    y = np.concatenate((firstvals, y, lastvals))
    return np.convolve(m[::-1], y, mode='valid')


#x, score = get_score('media/videos/anormaly/RoadAccidents002_x264.mp4')
#print(score)