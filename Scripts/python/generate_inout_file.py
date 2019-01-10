import os, os.path
import cv2
import glob

f_input = open('input_list_video.txt', 'w')
f_output = open('output_list_video_prefix.txt','w')

interval_v = 16


# read file path name in alphabet order
file_list_v = sorted(glob.glob("*.mp4"))

# each video, generate input/output file
for index in range(len(file_list_v)):
	
	# file path of video
	loc = file_list_v[index]
	cap=cv2.VideoCapture(loc)
	
	# number of frames
	total_frames = int(cap.get(7))
	print(total_frames)
	counter = 0   
	
	# generate file
	while (counter < total_frames-interval_v):
		f_input.write('input/' + loc + ' ' + str(counter) + ' ' + str(0))
		f_input.write('\n')
		f_output.write('output/' + loc[:-4] + '/' + str(counter).zfill(6) )
		f_output.write('\n')
		counter = counter + interval_v

f_input.close()
f_output.close()
