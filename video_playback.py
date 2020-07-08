import cv2
frames = []

cap = cv2.VideoCapture(0)

while True:
    x , frame = cap.read()
    frames.append(frame)
    cv2.imshow('Video Capture', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()
print(len(frames))

def nothing(arg): pass
cv2.namedWindow('Video Playback')
cv2.createTrackbar('Frame Number', 'Video Playback', 0,len(frames), nothing)

while True:
    frame_number = cv2.getTrackbarPos('Frame Number', 'Video Playback')
    print(frame_number)
    while True :
        try:
            img = frames[frame_number]
        except :
            print('Frames Completed Successfully')
        cv2.imshow('Video Playback', img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

cv2.destroyAllWindows()
