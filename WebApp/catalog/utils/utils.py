import os
import numpy as np
import scipy.io
import requests
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
        return np.array([[0,0],[0,0]])

def format_filesize(size, suffix='B'):
    for unit in ['','K','M','G','T','P','E','Z']:
        if abs(size) < 1024.0:
            return "%3.1f%s%s" % (size, unit, suffix)
        size /= 1024.0
    return "%.1f%s%s" % (size, 'Yi', suffix)

def url_downloadable(url):
    """
    Check the url contain a downloadable resource (type video) 
    return boolean
    """
    head = requests.head(url, allow_redirects = True)
    content_type = head.header.get('content-type')
    if 'video' in content_type.lower():
        return True
    else:
        return False 

def write_file(temp_file, response):
    """
    Write file with response urllib
    """
    block_sz = 8192
    file_size = int(response.info().get('Content-Length'))

    file_size_dl = 0
    while True:
        buffer = response.read(block_sz)
        if not buffer:
            break
        temp_file.write(buffer)
        file_size_dl += len(buffer)
        status = r"%10d  [%3.2f%%]" % (file_size_dl, file_size_dl * 100. / file_size)
        status = status + chr(8)*(len(status)+1)
        print(status)
    return temp_file

def get_basename(filename):
    return os.path.splitext(os.path.basename(filename))[0]

def main():
    anno = load_annotation('media/videos/RoadAccidents002_x264.mat')
    print(anno)

if __name__ == '__main__':
    # testing
    main()
    
