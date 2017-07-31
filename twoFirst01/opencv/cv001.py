__author__ = 'hooloongge'
# -*- coding: utf-8 -*-
import sys, random,string,struct,json
import numpy as np
import csv
from PyQt4 import QtCore, QtGui, uic
import cv2


# img = cv2.imread('code.jpg')
img = np.zeros((3,3),dtype=np.uint8)
img = cv2.cvtColor(img,cv2.COLOR_GRAY2BGR)

print img.shape
print img




