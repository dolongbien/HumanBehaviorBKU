from c3d.utils.array_util import *
import c3d.parameters as params
import cv2


def get_video_clips(video_path):
    frames = get_video_frames(video_path)
    clips = sliding_window(frames, params.frame_count, params.frame_count)
    return clips, len(frames)


def get_video_frames(video_path):
    cap = cv2.VideoCapture(video_path)
    frames = []
    while (cap.isOpened()):
        ret, frame = cap.read()
        if ret == True:
            frames.append(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        else:
            break
    return frames