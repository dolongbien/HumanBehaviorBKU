import keras
import scipy.io as sio
from keras import Sequential
from keras.layers import Dense, Dropout
from keras.regularizers import l2

import c3d.configuration as cfg
from catalog.utils import conv_dict
from catalog.utils import load_weights

def classifier_model():
    model = Sequential()
    model.add(Dense(512, input_dim=4096, kernel_initializer='glorot_normal', kernel_regularizer=l2(0.001), activation='relu'))
    model.add(Dropout(0.6))
    model.add(Dense(32, kernel_initializer='glorot_normal', kernel_regularizer=l2(0.001)))
    model.add(Dropout(0.6))
    model.add(Dense(1, kernel_initializer='glorot_normal', kernel_regularizer=l2(0.001), activation='sigmoid'))
    return model


def build_classifier_model():
    model = classifier_model()
    model = load_weights(model, cfg.classifier_model_weigts)
    return model

if __name__ == '__main__':
    model = build_classifier_model()
    model.summary()