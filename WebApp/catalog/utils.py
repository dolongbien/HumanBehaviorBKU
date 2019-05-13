import numpy as np
import scipy.io
import os

# ultility functions

def load_annotation(file_path):
    """
    Load temporal annotation file (.mat)
    Input: file_path: *.mat file path
    Return: a array, temporal interval value pairs (can have more than 1 pair)
    ex: array([[x,y]])
    """
    if os.path.exists(file_path):
        mat = scipy.io.loadmat(file_name=file_path)
        anno = mat['Annotation_file']
        anno = anno[0][0][1] # annotation value
        return anno
    else:
        return np.array([[0,0]])

def main():
    anno = load_annotation('media/videos/RoadAccidents002_x264.mat')
    print(anno)

if __name__ == '__main__':
    # testing
    main()
    
