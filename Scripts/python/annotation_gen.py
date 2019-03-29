import cv2


f_out = open('annotation.txt', 'w')
video_name = 'Shoplifting028_x264.mp4'
action = 'Shoplifting'
tab = '  '
frame_list = []
#Shoplifting028_x264.mp4  Shoplifting  570  840  -1  -1  
cap = cv2.VideoCapture(video_name)

while not cap.isOpened():
    cap = cv2.VideoCapture(video_path)
    cv2.waitKey(100)
    print ("Wait for the header")

while True:

    ret, frame = cap.read()
    key = cv2.waitKey(25) & 0xff
    pos_frame = cap.get(cv2.CAP_PROP_POS_FRAMES)
    #print(pos_frame)
    if not ret:
        break

    if key == ord('p'):

        while True:
            key2 = cv2.waitKey(25) or 0xff
            cv2.imshow('frame', frame)
            if key2 == ord('p'):
                print('Abnormal----' + str(pos_frame))
                frame_list.append(pos_frame)
                break

    cv2.imshow('frame', frame)

    if key == 27: #ESC
        break

if len(frame_list) == 2:
    f_out.write(video_name + tab + action + tab + str(int(frame_list[0])) + tab + str(int(frame_list[1])) + tab + '-1' + tab + '-1')

elif len(frame_list)== 4:
    f_out.write(video_name + tab + action + tab + str(int(frame_list[0])) + tab + str(int(frame_list[1])) + tab + str(int(frame_list[2])) + tab + str(int(frame_list[3])))

cap.release()
cv2.destroyAllWindows()