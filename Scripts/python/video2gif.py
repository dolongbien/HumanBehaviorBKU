# -*- coding: utf-8 -*-
"""
Created on Sun Jan 27 19:35:54 2019

@author: anilosmantur
"""

import cv2
import imageio
import glob
import sys

video_path = sys.argv[1] # video file input folder
gif_folder = sys.argv[2] # gif output folder
all_videos = glob.glob(video_path + '/*.mp4')


def __draw_label(img, text, pos, bg_color):
    font_face = cv2.FONT_HERSHEY_SIMPLEX
    scale = 0.5
    color = (0, 0, 0)
    thickness = cv2.FILLED
    margin = 2

    txt_size = cv2.getTextSize(text, font_face, scale, thickness)

    end_x = pos[0] + txt_size[0][0] + margin
    end_y = pos[1] - txt_size[0][1] - margin -3
    
    cv2.rectangle(img, pos, (end_x, end_y), bg_color, thickness)
    cv2.putText(img, text, (pos[0],pos[1]-2), font_face, scale, color, 1, cv2.LINE_AA)

for video_file in all_videos:
    #video_file = 'Shoplifting028_x264.mp4'
    gif_file = video_file[:-3] + 'gif'

    cap = cv2.VideoCapture(video_file)
    nFrames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    print(video_file, ' - file will be converted.')
    with imageio.get_writer(gif_file, duration=0.001, mode='I') as writer:
        print('video to gif started...')
        for i in range(nFrames):
            ret, frame = cap.read()
            print(i)
            if ret and i % 8 == 0:
                print('\r{:6.2f}%({}/{})'.format(100*(i+1)/nFrames, i+1, nFrames), end='')
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                frame = cv2.resize(frame, (320, 240))
                __draw_label(frame, 'Frame number: ' + str(int(i)), (20,20), (255,255,255))
                writer.append_data(frame)
            else:
                pass
        print()
    print('gif converting finished.')