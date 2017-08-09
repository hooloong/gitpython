__author__ = 'hooloongge'
# -*- coding: utf-8 -*-
import cv2
import numpy as np


cap = cv2.VideoCapture(0)
fps = cap.get(cv2.CAP_PROP_FPS)
print fps
fps = 30
size = (int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)),int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))
print size

fourcc = cv2.VideoWriter_fourcc('I','4','2','0')
out = cv2.VideoWriter('output.avi',fourcc,fps,size)
ret,frame = cap.read()
num = 10 * fps -1
while ret and num>0:
    out.write(frame)
    ret,frame = cap.read()
    num -= 1

cap.release()
out.release()

