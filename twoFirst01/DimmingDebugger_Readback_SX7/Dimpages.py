__author__ = 'hooloongge'
# -*- coding: utf-8 -*-
import sys, math, random, time
import ctypes as C
import two01 as TFC
import numpy as np
from dispmipsfunc import *
from PyQt4 import QtCore, QtGui, uic  # ,Qwt5
from Dimpages_res import *


class HexSpinBox(QtGui.QSpinBox):

    def __init__(self):
        super(HexSpinBox, self).__init__()
        self.setRange(0,0xFFFFFFFF)
        self.validator = QtGui.QRegExpValidator(QtCore.QRegExp("[0-9A-Fa-f]{1,8}"))

    def validate(self, text, pos):
        return self.validator.validate(text,pos)

    def textFromValue(self, value):
        return QtCore.QString.number(value,16).toUpper()

    def valueFromText(self, text):
        return text.toInt(16)

class DimPagesWindow(QtGui.QMainWindow):

    def __init__(self):
        super(DimPagesWindow, self).__init__()
        self.ui =  Ui_Form_Dimpages()
        self.ui.setupUi(self)
        # insert hexspinbox in to table
        hexspinlist = []
        for i in range(64):
            # newhex = HexSpinBox()
            newhex = QtGui.QSpinBox()
            hexspinlist.append(newhex)
        for i in range(self.ui.tableWidget_curpage.columnCount()):
            for j in range(self.ui.tableWidget_curpage.rowCount()):
                self.ui.tableWidget_curpage.setCellWidget(j,i,hexspinlist[j*4 + i])



        self.connectFlag = False


    def setConnectFlag(self, flag):
        self.connectFlag = flag




if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    mywindow = DimPagesWindow()
    mywindow.show()
    sys.exit(app.exec_())
