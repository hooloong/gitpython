# coding:utf-8
import cv2
import numpy as np

img = cv2.imread("2.jpg")                        #imread()读图片
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
gray = np.float32(gray)
dst = cv2.cornerHarris(gray, 2, 23, 0.04)       #调用cornerHarris函数，
img[dst > 0.01 * dst.max()] = [0, 0, 255]
while (True):
    cv2.imshow('corner', img)
    if cv2.waitKey(100 / 12) & 0xff == ord('q'):
        break
cv2.destroyAllWindows()
