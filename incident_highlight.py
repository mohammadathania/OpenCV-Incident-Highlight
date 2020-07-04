import numpy as np
import cv2 as cv
import imutils

'''img = cv.imread('marker.jpg')
gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

ret,thresh = cv.threshold(gray,127,255,0)
contours,hierarchy = cv.findContours(thresh, 1, 2)
print(contours)'''
#c = contours[0]
'''M = cv.moments(contours[0])
print( M )

area = cv.contourArea(contours[0])
print(area)'''

'''c = max(contours, key=cv.contourArea)
print(c)
perimeter = cv.arcLength(c,True)
print(perimeter)
rect = cv.minAreaRect(c)
box = cv.boxPoints(rect)
box = np.int0(box)
cv.drawContours(img,[box],0,(123,200,255),2)
cv.imshow('frame',img)
cv.waitKey(0)
'''
cap = cv.VideoCapture(0)

while True :
    x , frame = cap.read()
    if cv.waitKey(1) & 0xFF == ord('q') :
        break
    colorLower = (24, 100, 100)
    colorUpper = (44, 255, 255)
    frame = imutils.resize(frame, width=600)
    hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)

    # construct a mask for the color "green", then perform
    # a series of dilations and erosions to remove any small
    # blobs left in the mask
    mask = cv.inRange(hsv, colorLower, colorUpper)
    mask = cv.erode(mask, None, iterations=2)
    mask = cv.dilate(mask, None, iterations=2)

    # find contours in the mask and initialize the current
    # (x, y) center of the ball
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
