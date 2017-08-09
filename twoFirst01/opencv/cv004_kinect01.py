__author__ = 'hooloongge'
# -*- coding: utf-8 -*-
import cv2
import numpy as np


cameraCapture0 = cv2.VideoCapture(0)
cameraCapture1 = cv2.VideoCapture(1)


size = (int(cameraCapture0.get(cv2.CAP_PROP_FRAME_WIDTH)),int(cameraCapture0.get(cv2.CAP_PROP_FRAME_HEIGHT)))
print size
while True:
    suc0 = cameraCapture0.grab()
    suc1 = cameraCapture1.grab()
    if suc1 and suc0:
        ret,frame0 = cameraCapture0.retrieve()
        ret,frame1 = cameraCapture1.retrieve()
        cv2.imshow('frame0',frame0)
        cv2.imshow('frame1',frame1)
        print ret


    if cv2.waitKey(10) &0xFF == ord('q'):
        break

cameraCapture0.release()
cameraCapture1.release()
cv2.destroyAllWindows()
