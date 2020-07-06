import numpy as np
import cv2 as cv
import imutils
cap = cv.VideoCapture(0)

def nothing(x):
    pass


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





while True :
    x , frame = cap.read()

    if cv.waitKey(5) & 0xFF == ord('q') :
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

    mask = cv.inRange(hsv, colorLower, colorUpper)
    mask = cv.erode(mask, None, iterations=2)
    mask = cv.dilate(mask, None, iterations=2)


    cnts = cv.findContours(mask.copy(), cv.RETR_EXTERNAL,
                            cv.CHAIN_APPROX_SIMPLE)[-2]
    print(cnts)
    if len(cnts) > 0 :

        c = max(cnts, key=cv.contourArea)
        rect = cv.minAreaRect(c)
        box = cv.boxPoints(rect)
        box = np.int0(box)
        cv.drawContours(frame, [box], 0, (123, 200, 255), 2)
        cv.imshow('frame', frame)