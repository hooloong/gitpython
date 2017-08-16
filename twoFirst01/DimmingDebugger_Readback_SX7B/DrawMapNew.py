
__author__ = 'hooloongge'
# -*- coding: utf-8 -*-
import sys, math, random, time
import ctypes as C
import two01 as TFC
import numpy as np
from dispmipsfunc import *
from PyQt4 import QtCore, QtGui, QtSql,uic  # ,Qwt5
from DrawMapNew_res import  *
import pandas as pd

class DrawMLutWindow(QtGui.QMainWindow):

    def __init__(self):
        super(DrawMLutWindow, self).__init__()
        self.ui =  Ui_Form_mLut()
        self.ui.setupUi(self)
        self.isLoadxlsx = False
        self.isHDR = False
        self.xlsxdata = None
        self.normalm= np.zeros(65, np.uint32)
        self.setzerom = np.zeros(65,np.uint32)
        self.setfullm = np.zeros(65,np.uint32)
        self.setbinarym = np.zeros(65, np.uint32)
        self.normalm_lut= np.zeros(1024, np.uint32)
        self.setzerom_lut = np.zeros(1024,np.uint32)
        self.setfullm_lut = np.zeros(1024,np.uint32)
        self.setbinarym_lut = np.zeros(1024, np.uint32)
        self.curmm= np.zeros(65, np.uint32)
        self.curmm_lut = np.zeros(1024, np.uint32)
        self.generateTestingdata()


        self.initMlutTable()
        self.connect(self.ui.pushButton_write, QtCore.SIGNAL('clicked()'), self.writeMlut)
        self.connect(self.ui.pushButton_write, QtCore.SIGNAL('pressed()'), self.changeText_Mlut)
        self.connect(self.ui.pushButton_read, QtCore.SIGNAL('clicked()'), self.readMlut)
        self.connect(self.ui.pushButton_read, QtCore.SIGNAL('pressed()'), self.changeText_Mlut_read)
        self.connect(self.ui.pushButton_convert, QtCore.SIGNAL('clicked()'), self.convert)
        self.connect(self.ui.pushButton_output, QtCore.SIGNAL('clicked()'), self.printout)
        self.connect(self.ui.pushButton_save, QtCore.SIGNAL('clicked()'), self.savetofile)
        self.connect(self.ui.pushButton_load, QtCore.SIGNAL('clicked()'), self.loadfromfile)
        self.connect(self.ui.pushButton_draw, QtCore.SIGNAL('clicked()'), self.drawit)
        self.connect(self.ui.comboBox_test, QtCore.SIGNAL('currentIndexChanged(int)'), self.comboxchange)
        self.connect(self.ui.radioButton_sdr, QtCore.SIGNAL('clicked(bool)'), self.changeBitsel)
        self.connect(self.ui.radioButton_hdr, QtCore.SIGNAL('clicked(bool)'), self.changeBitsel)
        self.connect(self.ui.checkBox_en, QtCore.SIGNAL('clicked()'), self.enableMlut)
        self.ui.tableWidget_mlut.itemChanged.connect(self.updatetable)
        self.paintMlut()

    def setConnectFlag(self, flag):
        self.connectFlag = flag

    # def update(self):
    #     print self.r.getState()
    #
    #     pass
    def changeBitsel(self,flag):
        # if not self.initFlag: return

        if self.ui.radioButton_hdr.isChecked():
            self.isHDR = True
        else:
            self.isHDR = False
    def enableMlut(self):
        if self.connectFlag is False: return
        if self.ui.checkBox_en.isChecked():
            TFC.tfcWriteDwordMask(TFC.BASIC_PAGE, 0x30, 0x00000008, 0x00000008)
        else:
            TFC.tfcWriteDwordMask(TFC.BASIC_PAGE, 0x30, 0x00000008, 0)
        pass
    # def generateLGdata(self):
    #     j = (0,0)
    #     self.lgdata.append(j)
    #     j = (0,self.curmm[0])
    #     for i in range(1,64):
    #         j = (i*10, 1000+self.curmm[i-1])
    #         self.lgdata.append(j)
    #         j = (i*10, 1000+self.curmm[i])
    #         self.lgdata.append(j)
    #     print self.lgdata
    #     pass
    # def paintMlut(self):
    #     viewWid = float(self.ui.graphicsView_mlut.width() - 2)
    #     viewHeight = float(self.ui.graphicsView_mlut.height() - 2)
    #     scene = QtGui.QGraphicsScene(self)
    #     scene.setSceneRect(-viewWid/2, -viewHeight/2, viewWid, viewHeight)
    #     rectWid = 0
    #     totalBin = 1024
    #     if totalBin != 0:
    #         rectWid = 1
    #     RangeColor = [0x7f007f, 0xff7f00, 0xff7f7f, 0xff7fff, 0xffff00, 0xffff7f, 0x7f7f00, 0x7f7f7f, 0x7f7fff,
    #                   0x7fff00, 0x7f00ff, 0x7fffff, 0x7f007f, 0x007f00, 0x00007f, 0xFFFF00, 0x00FF00]
    #     for i in range(totalBin):
    #         var = self.curmm_lut[i] *5
    #         j = self.curmm_lut[i]
    #         color = QtGui.QColor(RangeColor[j%16] & 0xFF, (RangeColor[j%16] >> 4) & 0xFF, (RangeColor[j%16] >> 8) & 0xFF)
    #         item = QtGui.QGraphicsLineItem(QtCore.QLineF(0, 0, 1, var))
    #         item.setPen(color)
    #         scene.addItem(item)
    #         item.setPos((i * rectWid - viewWid/2), (- var + viewHeight/2))
    #     self.ui.graphicsView_mlut.setScene(scene)
    #     self.ui.graphicsView_mlut.show()

    def paintMlut(self):
        viewWid = float(self.ui.graphicsView_mlut.width() - 2)
        viewHeight = float(self.ui.graphicsView_mlut.height() - 2)
        scene = QtGui.QGraphicsScene(self)
        scene.setSceneRect(-viewWid/2, -viewHeight/2, viewWid, viewHeight)
        rectWid = 0
        totalBin = 64
        if totalBin != 0:
            rectWid = 5
        RangeColor = [0x7f007f, 0xff7f00, 0xff7f7f, 0xff7fff, 0xffff00, 0xffff7f, 0x7f7f00, 0x7f7f7f, 0x7f7fff,
                      0x7fff00, 0x7f00ff, 0x7fffff, 0x7f007f, 0x007f00, 0x00007f, 0xFFFF00, 0x00FF00]

        color = QtGui.QColor(RangeColor[0] & 0xFF, (RangeColor[0] >> 4) & 0xFF,
                             (RangeColor[0] >> 8) & 0xFF)
        item = QtGui.QGraphicsRectItem(QtCore.QRectF(0, 0,self.curmm[0]-0, 5))
        item.setBrush(color)
        scene.addItem(item)
        item.setPos(( 0- viewWid / 2), (-5 + viewHeight / 2))
        for i in range(1,totalBin):
            var1 = self.curmm[i-1]
            var2 = self.curmm[i]
            color = QtGui.QColor(RangeColor[i%16] & 0xFF, (RangeColor[i%16] >> 4) & 0xFF, (RangeColor[i%16] >> 8) & 0xFF)
            item = QtGui.QGraphicsRectItem(QtCore.QRectF(0,0, var2-var1, 5))
            item.setBrush(color)
            scene.addItem(item)
            item.setPos((var1-viewWid/2), (-5*(i+1) + viewHeight/2))
        self.ui.graphicsView_mlut.setScene(scene)
        self.ui.graphicsView_mlut.show()
    def generateLGdata(self):
        self.lgdata = []
        for i in range(0,64):
            j = (i, self.curmm[i-1])
            self.lgdata.append(j)
        print self.lgdata
        pass
    def drawit(self):

        self.paintMlut()
        self.update()
        pass
    def initMlutTable(self):
        for i in range(self.ui.tableWidget_mlut.rowCount()):
            for j in range(self.ui.tableWidget_mlut.columnCount()):
                # pwmdutytemp = "%X" % (self.curpat[i * self.ui.tableWidget_pattern.columnCount() + j])
                newItemt = QtGui.QTableWidgetItem(QtCore.QString("%1").arg(self.curmm[i * \
                self.ui.tableWidget_mlut.columnCount() + j],4,10,QtCore.QChar(" ")).toUpper())
                newItemt.setTextAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
                self.ui.tableWidget_mlut.setItem(i, j, newItemt)
        pass
    def updatetable(self,item):
        # if not self.initFlag: return

        if item != self.ui.tableWidget_mlut.currentItem():
            return
        print item.text()
        stringitem = "%s" % item.text()
        isright = ispropernumber(stringitem)
        i = item.row()
        j = item.column()
        if isright is True:
            self.curmm[item.row()* 8 + item.column()] = int(stringitem,10)

        if isright is False:
            self.ui.tableWidget_mlut.currentItem().setText(QtCore.QString("%1").arg(self.curmm[i * \
                                 self.ui.tableWidget_mlut.columnCount() + j],
                                        4, 10, QtCore.QChar(" ")).toUpper())
        pass
    def tableToLut(self,inputs,output):
        # //check the input values
        print inputs,output
        if inputs[63] != 1023:
            print "input[63 ] != 1023, error"
            # QtGui.QMessageBox.information(self, "warning", ("input[63 ] != 1023, error"))
            return
        for i in range(63):
            if inputs[i] > inputs[i+1]:
                print "inputs[ %d] > next data, error" % i
                # QtGui.QMessageBox.information(self, "warning", ("data not right!!"))
                return
            if inputs[i] > 1023:
                print "inputs[ %d] > 1023, error" % i
                # QtGui.QMessageBox.information(self, "warning", ("data not right!!"))
                return
        output[0] = 0
        output[1023] = 63
        for i in range(1,64):
            for y in range(inputs[i-1],inputs[i]+1):
                output[y] = i
        print output
        pass
    def convert(self):
        self.tableToLut(self.curmm, self.curmm_lut)
        pass
    def generateTestingdata(self):
        """
        generate normal table
        """
        for i in range(64):
            self.normalm[i] = 1024/64 * (i+1)
        self.normalm[63] = 1023

        self.tableToLut(self.normalm,self.normalm_lut)
        print self.normalm_lut

        # generate  zero table for hist
        for i in range(64):
            self.setzerom[i] = 0
        for i in range(1024):
            self.setzerom_lut[i] = 0
        # generate full mapping lut
        for i in range(64):
            self.setfullm[i] = 1023
        for i in range(1024):
            self.setfullm_lut[i] = 63
        print self.setfullm_lut
        # generate binary mpping lut, the knee set to 0x512
        for i in range(64):
                if i <32:
                    self.setbinarym[i] = 0
                else:
                    self.setbinarym[i] = 1023
        for i in range(1024):
                if i < 512:
                    self.setbinarym_lut[i] = 0
                else:
                    self.setbinarym_lut[i] = 63
        print self.setbinarym_lut
        self.curmm_lut = self.normalm_lut.copy()
        self.curmm = self.normalm.copy()
        # self.curmm_lut = self.setfullm_lut.copy()
        # self.curmm = self.setfullm.copy()
        # self.curmm_lut = self.setbinarym_lut.copy()
        # self.curmm = self.setbinarym.copy()
        # self.curmm_lut = self.setzerom_lut.copy()
        # self.curmm = self.setzerom.copy()
        pass
    def comboxchange(self):
        # if  self.initFlag is False: return
        index = self.ui.comboBox_test.currentIndex()
        if index ==0:
            self.curmm_lut = self.normalm_lut.copy()
            self.curmm = self.normalm.copy()
        elif index == 1:
            self.curmm_lut = self.setzerom_lut.copy()
            self.curmm = self.setzerom.copy()
        elif index == 2:
            self.curmm_lut = self.setfullm_lut.copy()
            self.curmm = self.setfullm.copy()
        else:
            self.curmm_lut = self.setbinarym_lut.copy()
            self.curmm = self.setbinarym.copy()

        self.initMlutTable()
        self.update()
        pass
    def changeText_Mlut(self):
        if self.connectFlag is False:
            pass
        else:
            self.ui.pushButton_write.setText("Write...")
    def changeText_Mlut_read(self):
        if self.connectFlag is False:
            pass
        else:
            self.ui.pushButton_read.setText("Read...")
    def writeMlut(self):
        # added read from registers
        if self.connectFlag is False:
            QtGui.QMessageBox.information(self, "warning", ("Please connect to chip first!!!\n Setting->Connect"))
            return
        TFC.tfcWriteDwordMask(0x19A004B0, 0, 0x00008000, 0x00008000)
        for i in range(1024):
            if i%4 == 0:
                temp = self.curmm_lut[i] | (self.curmm_lut[i+1] <<8)  \
                                                          | self.curmm_lut[i+2] <<16 | self.curmm_lut[i+3] << 24
                TFC.tfcWriteDword(0x19A46000+i,0,temp)
                print temp
        TFC.tfcWriteDwordMask(0x19A004B0, 0, 0x00008000, 0x00000000)
        self.ui.pushButton_write.setText("WriteToChip")

    def readMlut(self):
        if self.connectFlag is False:
            QtGui.QMessageBox.information(self, "warning", ("Please connect to chip first!!!\n Setting->Connect"))
            return
        TFC.tfcWriteDwordMask(0x19A004B0, 0, 0x00008000, 0x00008000)
        for i in range(1024):
            if i%4 == 0:
                temp = TFC.tfcReadDword(0x19A46000 + i, 0)
                self.curmm_lut[i] = temp & 0x000000FF
                self.curmm_lut[i+1] = (temp >> 8) & 0x000000FF
                self.curmm_lut[i+2] = (temp >> 16) & 0x000000FF
                self.curmm_lut[i+3] = (temp >> 24) & 0x000000FF
                print temp
        TFC.tfcWriteDwordMask(0x19A004B0, 0, 0x00008000, 0x00000000)
        self.ui.pushButton_read.setText("ReadFromChip")
    def printout(self):

        if self.ui.checkBox_toc.isChecked():
            tmps = "DWORD const mappinglut_default[256] = { \n"
            for i in xrange(32):
                tmps += " "*4
                for j in xrange(32):
                    if j%4 == 0:
                        tmps += "0x%X, " % (self.curmm_lut[i*32+j] + (self.curmm_lut[i*32+j+1] << 8) \
                                             + (self.curmm_lut[i*32+j+2] << 16) + (self.curmm_lut[i*32+j+3] << 24))
                    # tmps += " %2d," % self.curmm_lut[i*32+j]
                tmps += "\n"
            tmps += "};\n"
            self.ui.plainTextEdit_output.setPlainText(tmps)
            return
        tmps = "Pixel(10bits), Hist(6bits) \n"
        for j in range(1024):
            tmps += "  %4d,  %4d\n" % (j, self.curmm_lut[j])
        self.ui.plainTextEdit_output.setPlainText(tmps)
        pass
    def savetofile(self):
        dfile = QtGui.QFileDialog.getSaveFileName(self,"Save File dialog", "./", "mlut files(*.mlut *.txt)")
        if dfile:
            print dfile
        else:
            return

        dfile = str(dfile)
        try:
            self.curmm.tofile(dfile)
        except Exception, e:
            print e



    def loadfromfile_1(self):
        file = QtGui.QFileDialog.getOpenFileName(self, "Open File dialog", "./", "mlut files(*.mlut  *.txt)")
        if file:
            print file
        else:
            return
        file = str(file)
        try:
            self.curmm =  np.fromfile(file, dtype=np.uint32)
        except Exception, e:
            print e
        self.initMlutTable()
        self.tableToLut(self.curmm, self.curmm_lut)
        self.update()
    def loadfromfile(self):
        file = QtGui.QFileDialog.getOpenFileName(self, "Open File dialog", "./", "mlut files(*.mlut  *.txt *.xlsx)")
        if file:
            print file
        else:
            return
        file = str(file)
        if file.split('.')[1] == "xlsx":
            print "From EXCEL data"
            try:
                self.xlsxdata = pd.read_excel(file, '2DD_MLUT', index_col=None, na_values=['NA'])
            except Exception, e:
                print e
                self.isLoadxlsx = False
                return
            print str(self.xlsxdata.values[64][2])
            if str(self.xlsxdata.values[64][2]) == "1023" and str(self.xlsxdata.values[64][1]) == "1023":
                self.isLoadxlsx = True
            else:
                self.isLoadxlsx = False
                QtGui.QMessageBox.information(self, "warning", ("Please load right M_LUT table file"))
                return
        else:
            self.isLoadxlsx = False
            try:
                self.curmm =  np.fromfile(file, dtype=np.uint32)
            except Exception, e:
                print e
        print self.isHDR
        print self.isLoadxlsx
        if self.isLoadxlsx:
            if self.isHDR:
                offset = 2
            else:
                offset = 1
            for i in range(64):
                self.curmm[i] = self.xlsxdata.values[i+1][offset]
        print self.curmm

        return
        self.initMlutTable()
        self.tableToLut(self.curmm, self.curmm_lut)
        self.update()
if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    mywindow = DrawMLutWindow()
    mywindow.show()
    sys.exit(app.exec_())
