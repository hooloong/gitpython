__author__ = 'hooloongge'
# -*- coding: utf-8 -*-
import sys, math, random, time
import ctypes as C
import two01 as TFC
# import xmltodict
import numpy as np
from dispmipsfunc import *
from PyQt4 import QtCore, QtGui, uic  # ,Qwt5
from TestPattern_res import *
# from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
# from matplotlib.figure import Figure
# from mpl_toolkits.mplot3d import Axes3D
# import matplotlib.pyplot as plt
# import ctypes as C
# import cProfile
# cProfile.run('main()')
# import logging

class TestPatternWindow(QtGui.QMainWindow):

    def __init__(self):
        super(TestPatternWindow, self).__init__()
        self.ui = Ui_Form_TestPattern()
        self.ui.setupUi(self)

        self.connectFlag = False


    def setConnectFlag(self, flag):
        self.connectFlag = flag

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    mywindow = TestPatternWindow()
    mywindow.show()
    sys.exit(app.exec_())
