
from keras.regularizers import l2
from math import factorial
from scipy.io import loadmat, savemat
from keras.models import model_from_json
import numpy as np
import numpy.matlib

from keras import Sequential
from keras.layers import Dense, Dropout
from keras.regularizers import l2

import os, sys
from os import listdir

import matplotlib as pl 
pl.use('Agg')
import matplotlib.pyplot as plt
import cv2

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

def load_model(json_path):
    model = classifier_model()
    return model

def load_weights(model, weight_path):
    dict2 = loadmat(weight_path)
    dict = conv_dict(dict2)
    i = 0
    for layer in model.layers:
        weights = dict[str(i)]
        layer.set_weights(weights)
        i += 1
    return model

def conv_dict(dict2): # Helper function to save the model
    i = 0
    dict = {}
    for i in range(len(dict2)):
        if str(i) in dict2:
            if dict2[str(i)].shape == (0, 0):
                dict[str(i)] = dict2[str(i)]
            else:
                weights = dict2[str(i)][0]
                weights2 = []
                for weight in weights:
                    if weight.shape in [(1, x) for x in range(0, 5000)]:
                        weights2.append(weight[0])
                    else:
                        weights2.append(weight)
                dict[str(i)] = weights2
    return dict



def savitzky_golay(y, window_size, order, deriv=0, rate=1):
    #try:
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


# Load Video

def load_dataset_One_Video_Features(Test_Video_Path):

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

def get_score(video_path):
    Model_dir = 'c3d/trained_models/'
    weights_path = Model_dir + 'weightsAnomalyL1L2_10000_roadaccidents2.mat'
    model_path = Model_dir + 'model.json'
    model = load_model(model_path)
    load_weights(model, weights_path)
    print(video_path)

    # video_path = 'catalog/static/media/RoadAccidents011_x264.mp4'

    cap = cv2.VideoCapture(video_path)
    #Total_frames = cap.get(cv2.CV_CAP_PROP_FRAME_COUNT)
    # print(cv2)
    Total_frames = cap.get(cv2.CAP_PROP_FRAME_COUNT)
    total_segments = np.linspace(1, Total_frames, num=33)
    total_segments = total_segments.round()
    FeaturePath=(video_path)
    FeaturePath = FeaturePath[0:-4]
    FeaturePath = FeaturePath+ '_C.txt'
    inputs = load_dataset_One_Video_Features(FeaturePath)
    #inputs = np.reshape(inputs, (32, 4096))
    predictions = model.predict_on_batch(inputs)

    Frames_Score = []
    count = -1
    for iv in range(0, 32):
        F_Score = np.matlib.repmat(predictions[iv],1,(int(total_segments[iv+1])-int(total_segments[iv])))
        count = count + 1
        if count == 0:
            Frames_Score = F_Score
        if count > 0:
            Frames_Score = np.hstack((Frames_Score, F_Score))



    cap = cv2.VideoCapture((video_path))
    while not cap.isOpened():
        cap = cv2.VideoCapture((video_path))
        cv2.waitKey(1000)
        print ("Wait for the header")

    pos_frame = cap.get(cv2.CAP_PROP_POS_FRAMES)
    Total_frames = cap.get(cv2.CAP_PROP_FRAME_COUNT)

    print ("Anomaly Prediction")
    x = np.linspace(1, Total_frames, Total_frames)
    scores = Frames_Score
    scores1=scores.reshape((scores.shape[1],))
    scores1 = savitzky_golay(scores1, 101, 3)
    # print(scores1)
    return x, scores1

# get_score('media/RoadAccidents011_x264.mp4')