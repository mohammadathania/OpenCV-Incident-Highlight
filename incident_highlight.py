import numpy as np
import cv2 as cv
import imutils
from scipy.spatial import distance as dist
import collections
from tkinter import *
from tkinter import filedialog
from PIL import ImageTk,Image
import os

root = Tk()

root.title('Incident Segment Highlight App')
root.geometry('1200x720')

frame1 = Frame(root, bg='blue', width=500, height=720)
frame1.pack(side=RIGHT)

frame2 = Frame(root, bg='red', width=700, height=720)
frame2.pack(side=LEFT)

def open_video():
    cap = cv.VideoCapture(0)
    global data_to_print
    data_to_print = ""

    pts = collections.deque()

    def nothing(x):
        pass

    def safe_div(x, y):
        if y == 0:
            return 0
        return x / y

    barsWindow = 'Bars'
    hl = 'Hue Low'
    hh = 'Hue High'
    sl = 'Saturation Low'
    sh = 'Saturation High'
    vl = 'Value Low'
    vh = 'Value High'

    cv.namedWindow(barsWindow, flags=cv.WINDOW_AUTOSIZE)
    cv.createTrackbar(hl, barsWindow, 0, 179, nothing)
    cv.createTrackbar(hh, barsWindow, 0, 179, nothing)
    cv.createTrackbar(sl, barsWindow, 0, 255, nothing)
    cv.createTrackbar(sh, barsWindow, 0, 255, nothing)
    cv.createTrackbar(vl, barsWindow, 0, 255, nothing)
    cv.createTrackbar(vh, barsWindow, 0, 255, nothing)
    cv.setTrackbarPos(hl, barsWindow, 0)
    cv.setTrackbarPos(hh, barsWindow, 179)
    cv.setTrackbarPos(sl, barsWindow, 0)
    cv.setTrackbarPos(sh, barsWindow, 255)
    cv.setTrackbarPos(vl, barsWindow, 0)
    cv.setTrackbarPos(vh, barsWindow, 255)

    while True:
        x, frame = cap.read()

        if cv.waitKey(5) & 0xFF == ord('q'):
            break

        frame = imutils.resize(frame, width=600)
        hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
        hul = cv.getTrackbarPos(hl, barsWindow)
        huh = cv.getTrackbarPos(hh, barsWindow)
        sal = cv.getTrackbarPos(sl, barsWindow)
        sah = cv.getTrackbarPos(sh, barsWindow)
        val = cv.getTrackbarPos(vl, barsWindow)
        vah = cv.getTrackbarPos(vh, barsWindow)
        colorLower = np.array([hul, sal, val])
        colorUpper = np.array([huh, sah, vah])
        #colorLower = (24, 100, 100)
        #colorUpper = (44, 255, 255)

        mask = cv.inRange(hsv, colorLower, colorUpper)
        mask = cv.erode(mask, None, iterations=2)
        mask = cv.dilate(mask, None, iterations=2)

        cnts = cv.findContours(mask.copy(), cv.RETR_EXTERNAL,
                               cv.CHAIN_APPROX_SIMPLE)[-2]
        print(cnts)
        if len(cnts) > 0:

            c = max(cnts, key=cv.contourArea)
            rect = cv.minAreaRect(c)
            box = cv.boxPoints(rect)
            box = np.int0(box)
            (tl, tr, br, bl) = box

            def midpoint(ptA, ptB):
                return ((ptA[0] + ptB[0]) * 0.5, (ptA[1] + ptB[1]) * 0.5)

            (tltrX, tltrY) = midpoint(tl, tr)
            (blbrX, blbrY) = midpoint(bl, br)
            (tlblX, tlblY) = midpoint(tl, bl)
            (trbrX, trbrY) = midpoint(tr, br)

            dA = dist.euclidean((tltrX, tltrY), (blbrX, blbrY))
            dB = dist.euclidean((tlblX, tlblY), (trbrX, trbrY))

            pixelsPerMetric = 1

            dimA = dA / pixelsPerMetric
            dimB = dB / pixelsPerMetric
            cv.putText(frame, "{:.1f}mm".format(dimA), (int(tltrX - 15), int(tltrY - 10)), cv.FONT_HERSHEY_SIMPLEX,
                       0.65,
                       (255, 255, 255), 2)
            cv.putText(frame, "{:.1f}mm".format(dimB), (int(trbrX + 10), int(trbrY)), cv.FONT_HERSHEY_SIMPLEX, 0.65,
                       (255, 255, 255), 2)
            global length
            global breadth
            length = "{:.1f}mm".format(dimA)
            breadth = "{:.1f}mm".format(dimB)

            M = cv.moments(c)
            print(M)
            cX = int(safe_div(M["m10"], M["m00"]))
            cY = int(safe_div(M["m01"], M["m00"]))

            global area
            area = "{:.1f}mm".format(M["m00"])

            pts.appendleft((cX, cY))

            for i in range(1, len(pts)):

                if pts[i - 1] is None or pts[i] is None:
                    continue

                cv.line(frame, pts[i - 1], pts[i], (0, 0, 255), 3)

            cv.drawContours(frame, [box], 0, (123, 200, 255), 2)
            cv.circle(frame, (cX, cY), 5, (255, 255, 255), -1)

            cv.imshow('frame', frame)

def close_all():
    root.quit()

def view_text():
    txt_area.insert('2.0',"Length :"+length+"\t"+"Breadth :"+breadth+"\t"+"Area :"+area+"\n" )
def video_playback():

    frames = []

    cap = cv.VideoCapture(0)
    fourcc = cv.VideoWriter_fourcc(*'XVID')
    global out
    out = cv.VideoWriter('output.mp4', fourcc, 20.0, (640, 480))
    while True:
        x, frame = cap.read()
        frames.append(frame)
        cv.imshow('Video Capture', frame)
        global hsv
        hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
        if cv.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release()
    cv.destroyAllWindows()
    print(len(frames))

    def nothing(arg):
        pass

    cv.namedWindow('Video Playback')
    cv.createTrackbar('Frame Number', 'Video Playback', 0, len(frames), nothing)

    while True:
        frame_number = cv.getTrackbarPos('Frame Number', 'Video Playback')
        print(frame_number)
        try:
            img = frames[frame_number]
        except:
            print('Frames Completed')
        cv.imshow('Video Playback', img)
        if cv.waitKey(1) & 0xFF == ord('q'):
            break

    cv.destroyAllWindows()

def save_txt_file():
    filepath = os.path.dirname(__file__)
    file = open(os.path.join(filepath, 'Dimension.txt'), 'w')
    file.write("Length :"+length+"\t"+"Breadth :"+breadth+"\t"+"Area :"+area+"\n")
    file.close()

def save_video():
    out.write(hsv)
select_file_btn = Button(frame1, text='Object Tracking', font=("Courier 15 bold"), command=open_video)
select_file_btn.config(width=20, height=3)
select_file_btn.place(x=165, y=50)

save_file_btn = Button(frame1, text='Video Playback', font=("Courier 15 bold"), command=video_playback)
save_file_btn.config(width=20, height=3)
save_file_btn.place(x=165, y=150)

dimension_btn = Button(frame1, text='Object Dimensions', font=("Courier 15 bold"), command=view_text)
dimension_btn.config(width=20, height=3)
dimension_btn.place(x=165, y=250)

save_btn = Button(frame1, text='Save Text', font=("Courier 15 bold"), command=save_txt_file, padx=5)
save_btn.config(width=20, height=3)
save_btn.place(x=165, y=350)

save_video = Button(frame1, text='Save Video', font=("Courier 15 bold"), command=save_video)
save_video.config(width=20, height=3)
save_video.place(x=165, y=450)

close_btn = Button(frame1, text='Close', font=("Courier 15 bold"), command=close_all)
close_btn.config(width=20, height=3)
close_btn.place(x=165, y=550)

heading = Label(frame2, text='Welcome to Incident Segment Highlight App !',bg = 'red', font=("Courier 20 bold"))
heading.place(x=65, y=20)

txt_area = Text(frame2, width=90, height=47)
txt_area.place(x=30, y=60)

madeBy = Button(frame1, text='Made By JPM', font=("Courier 15 bold") )
madeBy.config(width=20, height=3)
madeBy.place(x=305, y=650)


cv.destroyAllWindows()
root.resizable(False, False)

root.mainloop()