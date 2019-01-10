import os, os.path
import cv2

f_input = open('input_list_video.txt', 'w')
f_output = open('output_list_video_prefix.txt','w')

interval_v = 16


loc = 'Shoplifting033_x264.mp4'
cap=cv2.VideoCapture(loc)
number_files=int(cap.get(7))
print(number_files)
counter = 0   
 
while (counter < number_files-interval_v):
	f_input.write('input/Shoplifting033_x264.mp4' + ' ' + str(counter) + ' ' + str(0))
	f_input.write('\n')
	f_output.write('output/Shoplifting033_x264.mp4' + '/' + str(counter).zfill(6) )
	f_output.write('\n')
	counter = counter + interval_v

f_input.close()
f_output.close()
