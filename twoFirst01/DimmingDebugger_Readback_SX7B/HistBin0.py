__author__ = 'hooloongge'
# -*- coding: utf-8 -*-
import sys, math, random, time
import ctypes as C
import two01 as TFC
# import xmltodict
import numpy as np
from dispmipsfunc import *
from PyQt4 import QtCore, QtGui, uic  # ,Qwt5
from Hist_Bin0_res import *
# from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
# from matplotlib.figure import Figure
# from mpl_toolkits.mplot3d import Axes3D
# import matplotlib.pyplot as plt
# import ctypes as C
# import cProfile
# cProfile.run('main()')
# import logging

class BinWindow(QtGui.QMainWindow):

    def __init__(self):
        super(BinWindow, self).__init__()
        self.ui = Ui_Form_Hist()
        self.ui.setupUi(self)

        self.connectFlag = False
        self.hist = np.zeros(512, np.uint32)
        for i in range(128):
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

        if self.ui.tableWidget_Hist.rowCount() != 0 and self.ui.tableWidget_Hist.columnCount() != 0:
            rectWid = viewWid/self.ui.tableWidget_Hist.columnCount()
            rectHeight = viewHeight/self.ui.tableWidget_Hist.rowCount()
        else:
            return

        for i in range(self.ui.tableWidget_Hist.columnCount()):
            for j in range(self.ui.tableWidget_Hist.rowCount()):
                var = self.hist[j * self.ui.tableWidget_Hist.columnCount() + i]
                if var < 0xFD20:
                    br = 0x80
                else:
                    br = 0x0
                color = QtGui.QColor(br, br, br)
                item = QtGui.QGraphicsRectItem(QtCore.QRectF(0, 0, rectWid, rectHeight))
                item.setBrush(color)
                scene.addItem(item)
                item.setPos((i * rectWid - viewWid/2), (j * rectHeight - viewHeight/2))
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
                tmp = i * self.ui.tableWidget_Hist.columnCount() + j
                var = TFC.tfcReadMemDword(tstartAddr + 4 * (tmp * 32)) & 0xFFFF
                self.hist[tmp] = var & 0xFFFF
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

        if histindex > 512:
            histindex = 512
        self.ui.spinBox_HistDataSelect.setValue(histindex)


        # histbaseaddress += histindex * 32
        self.updateHist(32, histindex, histbaseaddress)
        self.ui.pushButton_readHist.setText("ReadHistBin0")
        # print self.pushButton_readpwm.text
        print self.hist


if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    mywindow = BinWindow()
    mywindow.show()
    sys.exit(app.exec_())
