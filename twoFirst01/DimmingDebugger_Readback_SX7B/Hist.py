__author__ = 'hooloongge'
# -*- coding: utf-8 -*-
import sys, math, random, time
import ctypes as C
import two01 as TFC
# import xmltodict
import numpy as np
from dispmipsfunc import *
from PyQt4 import QtCore, QtGui, uic  # ,Qwt5
from Hist_res import *
# from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
# from matplotlib.figure import Figure
# from mpl_toolkits.mplot3d import Axes3D
# import matplotlib.pyplot as plt
# import ctypes as C
# import cProfile
# cProfile.run('main()')
# import logging

class HistWindow(QtGui.QMainWindow):

    def __init__(self):
        super(HistWindow, self).__init__()
        self.ui = Ui_Form_Hist()
        self.ui.setupUi(self)

        self.connectFlag = False
        self.hist = np.zeros(64, np.uint32)
        for i in range(64):
            self.hist[i] = random.randrange(100, 0xFFFF)
        # init tablewidget
        newItemt = QtGui.QTableWidgetItem('0')
        for i in range(self.ui.tableWidget_Hist.rowCount()):
            for j in range(self.ui.tableWidget_Hist.columnCount()):
                newItemt = QtGui.QTableWidgetItem('0')
                self.ui.tableWidget_Hist.setItem(i, j, newItemt)
        # end table init

        self.connect(self.ui.pushButton_readHist, QtCore.SIGNAL('clicked()'), self.readHist)
        self.connect(self.ui.pushButton_readHist, QtCore.SIGNAL('pressed()'), self.changeText_Hist)

        self.DataShowiInTable()
        self.paintHist()

    def setConnectFlag(self, flag):
        self.connectFlag = flag

    def paintHist(self):
        viewWid = float(self.ui.graphicsView_Hist.width() - 2)
        viewHeight = float(self.ui.graphicsView_Hist.height() - 2)
        scene = QtGui.QGraphicsScene(self)
        scene.setSceneRect(-viewWid/2, -viewHeight/2, viewWid, viewHeight)
        rectWid = 0
        totalBin = self.ui.tableWidget_Hist.rowCount() * self.ui.tableWidget_Hist.columnCount()
        if totalBin != 0:
            rectWid = viewWid/totalBin
        RangeColor = [0x7f0000, 0xff7f00, 0xff7f7f, 0xff7fff, 0xffff00, 0xffff7f, 0x7f7f00, 0x7f7f7f, 0x7f7fff,
                      0x7fff00, 0x7f00ff, 0x7fffff, 0x7f007f, 0x007f00, 0x00007f, 0xff007f]
        for i in range(totalBin):
            var = self.hist[i] * viewHeight / 0xffff
            color = QtGui.QColor(RangeColor[i%16] & 0xFF, (RangeColor[i%16] >> 4) & 0xFF, (RangeColor[i%16] >> 8) & 0xFF)
            item = QtGui.QGraphicsRectItem(QtCore.QRectF(0, 0, rectWid, var))
            item.setBrush(color)
            scene.addItem(item)
            item.setPos((i * rectWid - viewWid/2), (- var + viewHeight/2))
        self.ui.graphicsView_Hist.setScene(scene)
        self.ui.graphicsView_Hist.show()

    def DataShowiInTable(self):
        # Hist
        for i in range(self.ui.tableWidget_Hist.rowCount()):
            for j in range(self.ui.tableWidget_Hist.columnCount()):
                pwmdutytemp = "%X" % (self.hist[i * self.ui.tableWidget_Hist.rowCount() + j])

                newItemt = QtGui.QTableWidgetItem(pwmdutytemp)
                self.ui.tableWidget_Hist.setItem(i, j, newItemt)

    def updateHist(self, size, num, tstartAddr):
        for i in range(self.ui.tableWidget_Hist.rowCount()):
            for j in range(self.ui.tableWidget_Hist.columnCount()):
                tmp = i * self.ui.tableWidget_Hist.rowCount() + j
                indexpwm = tmp
                tmp /= 2
                if j%2 == 0:
                    var = TFC.tfcReadMemDword(tstartAddr + 4 * (tmp + size * num)) & 0xFFFF
                else:
                    var = (TFC.tfcReadMemDword(tstartAddr + 4 * (tmp + size * num)) >> 16 )& 0xFFFF
                self.hist[indexpwm] = var & 0xFFFF
                pwmdutytemp = "%X" % (var & 0xFFFF)
                newItemt = QtGui.QTableWidgetItem(pwmdutytemp)
                self.ui.tableWidget_Hist.setItem(i, j, newItemt)
        self.paintHist()
        self.update()

    def changeText_Hist(self):
        if self.connectFlag is False:
            pass
        else:
            self.ui.pushButton_readHist.setText("Reading")

    def readHist(self):
        # added read from registers
        if self.connectFlag is False:
            QtGui.QMessageBox.information(self, "warning", ("Please connect to chip first!!!\n Setting->Connect"))
            return
        histbaseaddress = (TFC.tfc2ddReadDword(0xC0) & 0x0FFFFFFF) << 4
        histindex = self.ui.spinBox_HistDataSelect.value()
        print histbaseaddress, histindex

        if histindex >= 799:
            histindex -= 1
        self.ui.spinBox_HistDataSelect.setValue(histindex)
        self.ui.spinBox_HistDataSelect.setRange(0, 799)

        # histbaseaddress += histindex * 32
        self.updateHist(32, histindex, histbaseaddress)
        self.ui.pushButton_readHist.setText("ReadHist")
        # print self.pushButton_readpwm.text
        print self.hist


if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    mywindow = HistWindow()
    mywindow.show()
    sys.exit(app.exec_())
