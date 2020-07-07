import numpy as np
import cv2 as cv
import imutils
from scipy.spatial import distance as dist
import collections

cap = cv.VideoCapture(0)

pts =collections.deque()

def nothing(x):
    pass

def safe_div(x,y):
    if y==0:
        return 0
    return x/y


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
    #colorLower = np.array([hul, sal, val])
    #colorUpper = np.array([huh, sah, vah])
    colorLower = (24, 100, 100)
    colorUpper = (44, 255, 255)

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
        cv.putText(frame, "{:.1f}mm".format(dimA), (int(tltrX - 15), int(tltrY - 10)), cv.FONT_HERSHEY_SIMPLEX, 0.65,
                    (255, 255, 255), 2)
        cv.putText(frame, "{:.1f}mm".format(dimB), (int(trbrX + 10), int(trbrY)), cv.FONT_HERSHEY_SIMPLEX, 0.65,
                    (255, 255, 255), 2)

        M = cv.moments(c)
        cX = int(safe_div(M["m10"], M["m00"]))
        cY = int(safe_div(M["m01"], M["m00"]))
        pts.appendleft((cX,cY))

        for i in range(1, len(pts)):

            if pts[i - 1] is None or pts[i] is None:
                continue

            cv.line(frame, pts[i - 1], pts[i], (0, 0, 255), 3)


        cv.drawContours(frame, [box], 0, (123, 200, 255), 2)
        cv.circle(frame, (cX, cY), 5, (255, 255, 255), -1)

        cv.imshow('frame', frame)
