# coding:utf-8
import cv2
import numpy
import utils


def strokeEdge(src, dst, blurKsize=7, edgeKsize=5):         #边缘检测
    if blurKsize >=3:
        blurSrc = cv2.medianBlur(src, blurKsize)            #模糊函数
        graySrc = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)     #灰度处理
    else:
        graySrc = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)     #灰度处理
    cv2.Laplacian(graySrc, cv2.CV_8U, graySrc, ksize=edgeKsize)     #边缘检测函数
    normalizedInverseAlpha = (1.0/255)*(255-graySrc)        #归一化
    channels = cv2.split(src)
    for channel in channels:
        channel[:] = channel * normalizedInverseAlpha       #乘以原图像
    cv2.merge(channels, dst)


class VConvolutionFilter(object):
    def __init__(self, kernel):
        self._kernel = kernel

    def apply(self, src, dst):
        cv2.filter2D(src, -1, self._kernel, dst)


class SharpenFilter(VConvolutionFilter):
    def __init__(self):
        kernel = numpy.array([[-1, -1, -1],
                             [-1, 9, -1],
                             [-1, -1, -1]])
        VConvolutionFilter.__init__(self, kernel)


class FindEdgesFilter(VConvolutionFilter):
    def __init__(self):
        kernel = numpy.array([[-1, -1, -1],
                             [-1, 8, -1],
                             [-1, -1, -1]])
        VConvolutionFilter.__init__(self, kernel)


class BlurFilter(VConvolutionFilter):
    def __init__(self):
        kernel = numpy.array([[0.04, 0.04, 0.04, 0.04, 0.04],
                             [0.04, 0.04, 0.04, 0.04, 0.04],
                             [0.04, 0.04, 0.04, 0.04, 0.04],
                             [0.04, 0.04, 0.04, 0.04, 0.04],
                             [0.04, 0.04, 0.04, 0.04, 0.04]])
        VConvolutionFilter.__init__(self, kernel)


class EmbossFilter(VConvolutionFilter):
    def __init__(self):
        kernel = numpy.array([[-2, -1, 0],
                             [-1, 1, 1],
                             [0, 1, 2]])
        VConvolutionFilter.__init__(self, kernel)