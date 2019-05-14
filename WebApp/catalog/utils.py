import numpy as np
import scipy.io
import os
from math import factorial
from scipy.io import loadmat, savemat
# ultility functions

def load_annotation(file_path):
    """
    Load temporal annotation file (.mat)
    Input: file_path: *.mat file path
    Return: a numpy array, temporal interval value pairs (can have more than 1 pair)
    ex: array([[x,y]])
    """
    if os.path.exists(file_path):
        mat = scipy.io.loadmat(file_name=file_path)
        anno = mat['Annotation_file']
        anno = anno[0][0][1] # annotation value
        return anno
    else:
        return np.array([[0,0]])


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

def load_weights(model, weight_path):
    dict2 = loadmat(weight_path)
    dict = conv_dict(dict2)
    i = 0
    for layer in model.layers:
        weights = dict[str(i)]
        layer.set_weights(weights)
        i += 1
    return model

def main():
    anno = load_annotation('media/videos/RoadAccidents002_x264.mat')
    print(anno)

if __name__ == '__main__':
    # testing
    main()
    
