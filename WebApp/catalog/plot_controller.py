
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

from .utils import savitzky_golay
from .utils import conv_dict
from .utils import load_one_video_features
from .utils import load_weights
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

# Load Video

def get_score(video_path):

    K.clear_session()
    Model_dir = 'c3d/trained_models/'
    weights_path = Model_dir + 'weightsAnomalyL1L2_10000_roadaccidents2.mat'
    model_path = Model_dir + 'model.json'
    model = load_model(model_path)
    load_weights(model, weights_path)

    cap = cv2.VideoCapture(video_path)

    Total_frames = cap.get(cv2.CAP_PROP_FRAME_COUNT)
    total_segments = np.linspace(1, Total_frames, num=33)
    total_segments = total_segments.round()
    print("Video path == " + video_path)

    FeaturePath=(video_path)
    FeaturePath = FeaturePath[0:-4]
    FeaturePath = FeaturePath.replace('videos/anormaly', 'features')
    FeaturePath = FeaturePath+ '_C.txt'

    inputs = load_one_video_features(FeaturePath)
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

    print ("Anomaly Prediction")
    x = np.linspace(1, Total_frames, Total_frames)
    scores = Frames_Score
    scores1=scores.reshape((scores.shape[1],))
    scores1 = savitzky_golay(scores1, 101, 3)
    return x, scores1

#x, score = get_score('media/videos/anormaly/RoadAccidents002_x264.mp4')
#print(score)