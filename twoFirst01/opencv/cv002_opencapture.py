__author__ = 'hooloongge'
# -*- coding: utf-8 -*-
import cv2
import numpy as np


cap = cv2.VideoCapture(0)
# fourcc = cv2.cv.CV_FOURCC(*'XVID')
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('output.avi',fourcc,20.0,(640,480))#保存视频
while True:
    ret,frame = cap.read()
    gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    out.write(frame)#写入视频
    cv2.imshow('frame',frame)#一个窗口用以显示原视频
    cv2.imshow('gray',gray)#另一窗口显示处理视频


    if cv2.waitKey(1) &0xFF == ord('q'):
        break

cap.release()
out.release()
cv2.destroyAllWindows()
