# -*- coding: utf-8 -*-
"""
Created on Sun Jan 27 19:35:54 2019

@author: anilosmantur
"""

import cv2
import imageio
import glob
import sys
import os.path

video_path = 'input' # video file input folder
gif_folder = 'output' # gif output folder
all_videos = glob.glob(video_path + '/*.mp4')
print(video_path,gif_folder, sep="\n")

def __draw_label(img, text, pos, bg_color):
    font_face = cv2.FONT_HERSHEY_DUPLEX
    scale = 0.6
    color = (0, 0, 0)
    thickness = cv2.FILLED
    margin = 2

    txt_size = cv2.getTextSize(text, font_face, scale, thickness)
    
    end_x = pos[0] + txt_size[0][0] + margin
    end_y = pos[1] - txt_size[0][1] - margin - 5
    
    cv2.rectangle(img, (pos[0],pos[1]+3), (end_x, end_y), bg_color, thickness)
    cv2.putText(img, text, (pos[0],pos[1]-3), font_face, scale, color, 1, cv2.LINE_AA)

for video_file in all_videos:

    video_name = os.path.basename(video_file)
    gif_name = video_name[:-3] + 'gif'
    print("VIDEO NAME and GIF NAME")
    print(video_name, gif_name, sep="\n")
    gif_file = gif_folder + '/' + gif_name
    
    cap = cv2.VideoCapture(video_file)
    nFrames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    print(video_file, ' - file will be converted.')
    with imageio.get_writer(gif_file, duration=0.001, mode='I') as writer:
        print('video to gif started...')
        for i in range(nFrames):
            ret, frame = cap.read()
            if ret and i % 8 == 0:
                print('\r{:6.2f}%({}/{})'.format(100*(i+1)/nFrames, i+1, nFrames), end='')
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                frame = cv2.resize(frame, (320, 240))
                __draw_label(frame, 'Frame No = ' + str(int(i)), (10,35), (255,255,255))
                writer.append_data(frame)
            else:
                pass
        print()
    print('gif converting finished.')