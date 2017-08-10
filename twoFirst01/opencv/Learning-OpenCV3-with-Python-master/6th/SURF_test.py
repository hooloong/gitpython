# coding:utf-8
import cv2, sys
import numpy as np

imgpath = sys.argv[1]
img = cv2.imread(imgpath)
alg = sys.argv[2]


def fd(algorithm):
    if algorithm == 'SIFT':
        return cv2.xfeatures2d.SIFT_create()
    if algorithm == 'SURF':
        return cv2.xfeatures2d.SURF_create(float(sys.argv[3]) if
                                           len(sys.argv) == 4 else 4000)


gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
fd_alg = fd(alg)
keypoints, descriptor = fd_alg.detectAndCompute(gray, None)

img = cv2.drawKeypoints(image=img, outImage=img, keypoints=keypoints, flags=4, color=(51, 163, 236))
cv2.imshow('SURF', img)
while (True):
    if cv2.waitKey(1) & 0xff == ord('q'):
        break
cv2.destroyAllWindows()
