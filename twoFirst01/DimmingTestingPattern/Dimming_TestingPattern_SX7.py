__author__ = 'hooloongge'
# -*- coding: utf-8 -*-
import sys, math, random, time
import ctypes as C
import two01 as TFC
#import xmltodict
import json
import ConfigParser
import numpy as np
from dispmipsfunc import *
from PyQt4 import QtCore, QtGui, uic #,Qwt5
# from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
# from matplotlib.figure import Figure
# from mpl_toolkits.mplot3d import Axes3D
#import matplotlib.pyplot as plt
# import ctypes as C
# import cProfile
# cProfile.run('main()')
# import logging
from Dimming_TestingPattern_Res import *
REG_LOG_DEBUG = TFC.SREG_LOG_DEBUG
BIT_LOG_DEBUG = TFC.SBIT_LOG_DEBUG
REG_MEM_ADDR = TFC.SREG_MEM_ADDR
REG_MEM_WRITEINDEX = TFC.SREG_MEM_WRITEINDEX  # [15:0] count; [31:16] size, unit byte;

class MyWindow(QtGui.QMainWindow):
    sin = QtCore.pyqtSignal()
    def __init__(self):
        super(MyWindow, self).__init__()
        uic.loadUi("Dimming_TestingPattern_SX7.ui", self)
        # self.ui = Ui_MainWindow()
        # self.ui.setupUi(self)
        self.setWindowIcon(QtGui.QIcon("222.ico"))
        # self.setGeometry(300,300,810,640)
        self.statusBar().showMessage('DisConnected to chip!!!')
        self.painter = QtGui.QPainter()

        self.s_dict = dict(defaultfilename="parameters_SX7.json")
        self.connectFlag = False
        self.pwm = np.zeros(64, np.uint32)
        # self.pwm *= 0xA00
        # self.pwm.dtype = np.uint32
        for i in range(64):
            self.pwm[i] = random.randrange(100, 0xFFFF)
        self.current = np.ones(64, np.uint32)
        self.output_pwm = np.zeros(64, np.uint32)
        self.output_current = np.ones(64, np.uint32)
        print self.pwm
        # init tablewidget
        newItemt = QtGui.QTableWidgetItem('0')
        for i in range(self.ui.tableWidget_hist.rowCount()):
            for j in range(self.ui.tableWidget_hist.columnCount()):
                newItemt = QtGui.QTableWidgetItem('0')
                self.ui.tableWidget_hist.setItem(i, j, newItemt)

        #end table init
        self.offlineFlag = False
        self.readMem_Thread = ReadMemThread()
        self.log_flag = False
        self.read_flag = False
        self.stop_flag = False
        self.connect(self.ui.actionConnect, QtCore.SIGNAL('triggered()'), self.connectChip)
        self.connect(self.ui.actionDisconnect, QtCore.SIGNAL('triggered()'), self.disconnectChip)
        self.connect(self.ui.pushButton_readhist, QtCore.SIGNAL('clicked()'), self.readPWM)
        self.connect(self.ui.pushButton_readhist, QtCore.SIGNAL('pressed()'), self.changeText_pwm)

        self.connect(self.ui.pushButton_flushimg, QtCore.SIGNAL('clicked()'), self.update)

        self.connect(self.ui.pushButton_plotin, QtCore.SIGNAL('clicked()'), self.CreateNewPlotDailog)
        # self.connect(self.pushButton_plot, QtCore.SIGNAL('clicked()'), self.CreateNewPlotDailog_2)
        self.ui.actionQuit.connect(self.ui.actionQuit, QtCore.SIGNAL('triggered()'), QtGui.qApp, QtCore.SLOT('quit()'))
        # self.actionOpen_setting_file.connect(self.actionOpen_setting_file, QtCore.SIGNAL('triggered()'),
        #                                      self.loadSettingfromJson)
        # self.actionSave_setting_file.connect(self.actionSave_setting_file, QtCore.SIGNAL('triggered()'),
        #                                      self.saveSettingfromJson)
        #self.connect(self.pushButton_logstart, QtCore.SIGNAL('clicked()'), self.logStart)
        #self.connect(self.ui.pushButton_readmem, QtCore.SIGNAL('clicked()'), self.readMem)
        self.connect(self.ui.pushButton_next, QtCore.SIGNAL('clicked()'), self.readMemNext)
        self.connect(self.ui.pushButton_prev, QtCore.SIGNAL('clicked()'), self.readMemPrev)
        #self.connect(self.ui.pushButton_readmem, QtCore.SIGNAL('pressed()'), self.changeText_readMem)
        self.sin.connect(self.readMem_Thread.stop)
        self.readMem_Thread.stateSignal.connect(self.saveMemState)
        self.connect(self.ui.checkBox_offline, QtCore.SIGNAL('clicked()'), self.setOffline)
        # self.connect(self.spinBox_MemDataSelect, QtCore.SIGNAL('valueChanged(int)'), self.selectReadMem)
        self.connect(self.ui.pushButton_saveMemDataToFile, QtCore.SIGNAL('clicked()'), self.saveMemDataToFile)

        # self.loadSettingfromJson()
        self.PWMshowinTable()


    def paintEvent(self, envent):
        self.painter.begin(self)
        startposx = self.ui.line.x()+20
        startposy = self.ui.line.y()
        # print startposx,startposy
        RangeColor = [0x7f0000, 0xff7f00, 0xff7f7f, 0xff7fff, 0xffff00, 0xffff7f, 0x7f7f00, 0x7f7f7f, 0x7f7fff, 0x7fff00, 0x7f00ff, 0x7fffff, 0x7f007f, 0x007f00, 0x00007f, 0xff007f] *4
        for i in range(64):
            var = self.pwm[i] >> 8
            color = QtGui.QColor(RangeColor[i] & 0xFF, (RangeColor[i] >> 4) & 0xFF, (RangeColor[i] >> 8) & 0xFF)
            self.painter.setBrush(color)
            self.painter.drawRect(startposx + i * 11, startposy+290-var, 11, var)
        self.painter.end()

    def connectChip(self):
        config_read = ConfigParser.RawConfigParser()
        config_read.read("ChipDebugger.INI")
        eth_ip = config_read.get("Connection", "Ethernet.IP")
        self.connectFlag = TFC.TFCConnect2Chip()
        print("tfcConnInit returns ", self.connectFlag)
        if self.connectFlag:
            print("Connect to chip!!! ")
            self.statusBar().showMessage('"Connect to chip!!!')
            self.setWindowTitle("Dimming Debugger" + "   " + "Connection" + "   " + eth_ip)
        else:
            print("Could not Connect to chip!!! ")
            self.statusBar().showMessage('Could not Connect to ' + "   " + eth_ip + "!!!!")
            self.setWindowTitle("Dimming Debugger" + "    " + "DisConnection")

    def disconnectChip(self):
        if self.connectFlag == False:
            return
        self.connectFlag = False
        TFC.tfcConnTerm()
        self.setWindowTitle("Dimming Debugger     DisConnect..")


    def loadParaTable(self):
        i = 1
        j = 0
        self.tableWidget_Paras.setRowCount(len(self.s_dict))
        for key in self.s_dict:
            # print key, self.s_dict[key]
            newItemh = QtGui.QTableWidgetItem(key)
            self.tableWidget_Paras.setVerticalHeaderItem(j, newItemh)
            str = "%d" % self.s_dict[key]
            newItemi = QtGui.QTableWidgetItem(str)
            self.tableWidget_Paras.setItem(j, 0, newItemi)
            i = i + 1
            j = j + 1

    def loadSettingfromJson(self):
        settingfile = "parameters.json"
        s_fp = open(settingfile, 'r')
        if s_fp == False:
            print "error file!!!!"
        else:
            self.s_setjson = json.load(s_fp)
            s_fp.close()
            self.s_dict = self.s_setjson["parameters"]
            # print self.s_setjson
            # print self.s_dict
            self.loadParaTable()

    def saveSettingfromJson(self):
        settingfile = "parameters1.json"
        s_fp = open(settingfile, 'w+')
        if s_fp == False:
            print "error file!!!!"
        elif len(self.s_dict) == 1:
            print "read firstly !!!!"
        else:
            s_fp.write("%s" % self.s_setjson)
            s_fp.close()

    def changeText_pwm(self):
        if self.connectFlag is False:
            pass
        else:
            self.ui.pushButton_readhist.setText("Reading")

    def changeText_current(self):
        if self.connectFlag == False:
            pass
        else:
            self.pushButton_readcurrent.setText("Reading")

    def readPWM(self):
        # added read from registers
        if self.offlineFlag is False:
            if self.connectFlag is False:
                return
            histbaseaddress = (TFC.tfc2ddReadDword(0xC0) & 0x0FFFFFFF) << 4
            histindex = self.ui.spinBox_MemDataSelect.value()
            print histbaseaddress,histindex

            if histindex >= 799:
                histindex -= 1
            self.ui.spinBox_MemDataSelect.setValue(histindex)
            self.ui.spinBox_MemDataSelect.setRange(0, 799)

            #histbaseaddress += histindex * 32
            self.updatePWM(32, histindex, histbaseaddress, 0)
        self.ui.pushButton_readhist.setText("ReadHist")
        # print self.pushButton_readpwm.text
        print self.pwm
        self.update()

    def PWMshowinTable(self):

        for i in range(self.ui.tableWidget_hist.rowCount()):
            for j in range(self.ui.tableWidget_hist.columnCount()):
                pwmdutytemp = "%X" % (self.pwm[i * self.ui.tableWidget_hist.rowCount() + j])

                newItemt = QtGui.QTableWidgetItem(pwmdutytemp)
                self.ui.tableWidget_hist.setItem(i, j, newItemt)


    def readCurrent(self):
        if self.connectFlag is False:
            return
        for i in range(self.tableWidget_Current.rowCount()):
            for j in range(self.tableWidget_Current.columnCount()):
                TFC.tfc2ddWriteDword(0x68, 0xA5)
                TFC.tfc2ddWriteDword(0x6C, i * self.tableWidget_Current.rowCount() + j)
                time.sleep(0.1)
                var = TFC.tfc2ddReadDword(0x68) >> 8;
                self.current[i * self.tableWidget_Current.rowCount() + j] = var & 0xFFF
                pwmdutytemp = "%X" % (var & 0xFFF)
                newItemt = QtGui.QTableWidgetItem(pwmdutytemp)
                self.tableWidget_Current.setItem(i, j, newItemt)
        self.pushButton_readcurrent.setText("ReadCurrent")
        # print self.pushButton_readcurrent.text
        print self.current

    def outputCurrent(self):
        for i in range(self.tableWidget_Current_2.rowCount()):
            for j in range(self.tableWidget_Current_2.columnCount()):
                var = self.output_current[i * self.tableWidget_Current.rowCount() + j]
                pwmdutytemp = "%X" % (var & 0xFF)
                newItemt = QtGui.QTableWidgetItem(pwmdutytemp)
                self.tableWidget_Current_2.setItem(i, j, newItemt)
                # print self.current

    def outputPWM(self):
        for i in range(self.tableWidget_PWM_2.rowCount()):
            for j in range(self.tableWidget_PWM_2.columnCount()):
                var = self.output_pwm[i * self.tableWidget_PWM_2.rowCount() + j]
                pwmdutytemp = "%X" % (var & 0xFFF)
                newItemt = QtGui.QTableWidgetItem(pwmdutytemp)
                self.tableWidget_PWM_2.setItem(i, j, newItemt)



    def CreateNewPlotDailog(self):
        # data = self.output_pwm
        data = self.pwm.copy()

        data.shape = (8, 8)
        column_names = ['1', '2', '3', '4', '5', '6', '7', '8']
        row_names = ['1', '2', '3', '4', '5', '6', '7', '8']
        fig = plt.figure()
        ax = Axes3D(fig)
        lx = len(data[0])  # Work out matrix dimensions
        ly = len(data[:, 0])
        xpos = np.arange(0, lx, 1)  # Set up a mesh of positions
        ypos = np.arange(0, ly, 1)
        xpos, ypos = np.meshgrid(xpos + 0.25, ypos + 0.25)
        xpos = xpos.flatten()  # Convert positions to 1D array
        ypos = ypos.flatten()
        zpos = np.zeros(lx * ly)
        dx = 0.5 * np.ones_like(zpos)
        dy = dx.copy()
        dz = data.flatten()
        ax.bar3d(xpos, ypos, zpos, dx, dy, dz, color='y')
        # sh()
        ax.w_xaxis.set_ticklabels(column_names)
        ax.w_yaxis.set_ticklabels(row_names)
        ax.set_xlabel('led_x')
        ax.set_ylabel('led_y')
        ax.set_zlabel('Brightness')
        plt.show()

    def CreateNewPlotDailog_1(self):
        data = self.output_pwm.copy()
        # data = (data * self.s_dict["current_scale_3820"]) / 100
        for i in range(self.s_dict["led_size"]):
            data[i] = (data[i] * self.output_current[i]) / self.s_dict["normal_current_mid"]
        data.shape = (8, 8)
        column_names = ['1', '2', '3', '4', '5', '6', '7', '8']
        row_names = ['1', '2', '3', '4', '5', '6', '7', '8']
        fig = plt.figure()
        ax = Axes3D(fig)
        lx = len(data[0])  # Work out matrix dimensions
        ly = len(data[:, 0])
        xpos = np.arange(0, lx, 1)  # Set up a mesh of positions
        ypos = np.arange(0, ly, 1)
        xpos, ypos = np.meshgrid(xpos + 0.25, ypos + 0.25)
        xpos = xpos.flatten()  # Convert positions to 1D array
        ypos = ypos.flatten()
        zpos = np.zeros(lx * ly)
        dx = 0.5 * np.ones_like(zpos)
        dy = dx.copy()
        dz = data.flatten()
        ax.bar3d(xpos, ypos, zpos, dx, dy, dz, color='r')
        # sh()
        ax.w_xaxis.set_ticklabels(column_names)
        ax.w_yaxis.set_ticklabels(row_names)
        ax.set_xlabel('led_x')
        ax.set_ylabel('led_y')
        ax.set_zlabel('Brightness')
        plt.show()

    def CreateNewPlotDailog_2(self):
        new_dailog = MyPlotDialog()
        r = new_dailog.exec_();

    def closeEvent(self, event):
        reply = QtGui.QMessageBox.question(self, 'Message', "Are you sure to quit?", QtGui.QMessageBox.Yes,
                                           QtGui.QMessageBox.No)
        if reply == QtGui.QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

    def logStart(self):
        if self.connectFlag is False:
            return
        if self.log_flag is False:
            self.log_flag = True
            print REG_LOG_DEBUG,BIT_LOG_DEBUG
            TFC.tfcWriteDwordMask(REG_LOG_DEBUG, 0, BIT_LOG_DEBUG, BIT_LOG_DEBUG)
            print TFC.tfcReadDword(REG_LOG_DEBUG,0)
            self.pushButton_logstart.setText("Logging")
        else:
            self.log_flag = False
            TFC.tfcWriteDwordMask(REG_LOG_DEBUG, 0, BIT_LOG_DEBUG, 0)
            self.pushButton_logstart.setText("LogStart")

    def changeText_readMem(self):
        if self.connectFlag is True:
            self.pushButton_readmem.setText("Reading")

    def saveMemState(self, strState, count, total):
        if strState == "finished":
            print "read memory finished. %d/%d" %(count, total)
            # self.pushButton_readmem.setText("ReadMem")
            # self.read_flag = False
            self.pushButton_saveMemDataToFile.setText("SaveToFile")
            self.pushButton_logstart.setEnabled(True)
            self.stop_flag = False
        elif strState == "reading":
            temps =  "reading memory: %d/%d" %(count, total)
            print temps
            self.statusBar().showMessage(temps)
        elif strState == "breaked":
            temps = "reading memory breaked: %d/%d" %(count, total)
            print temps
            self.statusBar().showMessage(temps)
            self.readMem_Thread.setBreakFlag(False);

    def updatePWM(self, size, num, tstartAddr, tData):
        for i in range(self.ui.tableWidget_hist.rowCount()):
            for j in range(self.ui.tableWidget_hist.columnCount()):
                tmp = i * self.ui.tableWidget_hist.rowCount() + j
                indexpwm = tmp
                tmp /= 2
                if self.offlineFlag is True:
                    var = tData[2 + tmp + size * num]
                elif j%2 == 0:
                    var = TFC.tfcReadMemDword(tstartAddr + 4 * (tmp + size * num)) & 0xFFFF
                else:
                    var = (TFC.tfcReadMemDword(tstartAddr + 4 * (tmp + size * num)) >> 16 )& 0xFFFF
                self.pwm[indexpwm] = var & 0xFFFF
                pwmdutytemp = "%X" % (var & 0xFFFF)
                newItemt = QtGui.QTableWidgetItem(pwmdutytemp)
                self.ui.tableWidget_hist.setItem(i, j, newItemt)
        # print self.pwm
        self.update()

    def readMem(self):
        if self.offlineFlag is False:
            if self.connectFlag is False:
                return
            if self.read_flag is False:
                startAddr = TFC.tfcReadDword(REG_MEM_ADDR, 0x0)
                var = TFC.tfcReadDword(REG_MEM_WRITEINDEX, 0x0)
                Cnt = var & 0xffff
                Size = ((var >> 16) & 0xffff) >> 2
                tableSize = self.tableWidget_PWM.rowCount() * self.tableWidget_PWM.columnCount()
                # p = C.create_string_buffer("",10000)
                # print p[0], p[1], p[2]
                # s = C.cast(p,C.c_char_p)
                # TFC.tfcReadFB(startAddr, 64,s)
                if Size != tableSize:
                    print("Size not match!!!! firmware: %d, tool: %d" %( Size, tableSize))
                    self.pushButton_readmem.setText("ReadMem")
                    return
                elif Cnt == 0:
                    print("nothing in memory!!! cnt = %d" %(Cnt))
                    self.pushButton_readmem.setText("ReadMem")
                    return
                else:
                    num = self.spinBox_MemDataSelect.value()
                    if num >= Cnt:
                        num = Cnt - 1
                        self.spinBox_MemDataSelect.setValue(num)
                    self.updatePWM(Size, num, startAddr, 0)
                    # self.readMem_Thread.start()
                    self.ui.spinBox_MemDataSelect.setRange(0, Cnt - 1)
            #     self.read_flag = True
            # else:
                # self.sin.emit()
                self.pushButton_readmem.setText("ReadMem")
                # self.read_flag = False
        else:
            try:
                Data = np.fromfile("DimmingMemLogData.bin", dtype=np.uint32)
                Cnt = Data[0]
                DataSize = Data[1]
                tableSize = self.tableWidget_PWM.rowCount() * self.tableWidget_PWM.columnCount()
                if Cnt == 0:
                    print "no data in file: DimmingMemLogData.bin"
                elif DataSize != tableSize:
                    print("Size not match!!!! file: %d, table: %d" %(DataSize, tableSize))
                else:
                    num = self.ui.spinBox_MemDataSelect.value()
                    if num >= Cnt:
                        num = Cnt - 1
                    self.ui.spinBox_MemDataSelect.setValue(num)
                    self.updatePWM(DataSize, num, 0, Data)
                    self.ui.spinBox_MemDataSelect.setRange(0, Cnt - 1)
                    self.update()
            except Exception, e:
                print Exception, ":", e
            self.update()
            return
    def readMemPrev(self):
        if self.offlineFlag is True:

            try:
                Data = np.fromfile("DimmingMemLogData.bin", dtype=np.uint32)
                Cnt = Data[0]
                DataSize = Data[1]
                tableSize = self.tableWidget_PWM.rowCount() * self.tableWidget_PWM.columnCount()
                if Cnt == 0:
                    print "no data in file: DimmingMemLogData.bin"
                elif DataSize != tableSize:
                    print("Size not match!!!! file: %d, table: %d" %(DataSize, tableSize))
                else:
                    num = self.spinBox_MemDataSelect.value()
                    if num > 0:
                        num -= 1
                    if num >= Cnt:
                        num = Cnt - 1
                    self.spinBox_MemDataSelect.setValue(num)

                    self.spinBox_MemDataSelect.setRange(0, Cnt - 1)
                    self.updatePWM(DataSize, num, 0, Data)
            except Exception, e:
                print Exception, ":", e
            self.update()
            return

    def readMemNext(self):
        if self.offlineFlag is True:

            try:
                Data = np.fromfile("DimmingMemLogData.bin", dtype=np.uint32)
                Cnt = Data[0]
                DataSize = Data[1]
                tableSize = self.tableWidget_PWM.rowCount() * self.tableWidget_PWM.columnCount()
                if Cnt == 0:
                    print "no data in file: DimmingMemLogData.bin"
                elif DataSize != tableSize:
                    print("Size not match!!!! file: %d, table: %d" % (DataSize, tableSize))
                else:
                    num = self.spinBox_MemDataSelect.value()
                    num += 1
                    if num >= Cnt:
                        num = Cnt - 1

                    self.spinBox_MemDataSelect.setValue(num)
                    self.spinBox_MemDataSelect.setRange(0, Cnt - 1)
                    self.updatePWM(DataSize, num, 0, Data)
            except Exception, e:
                print Exception, ":", e
            self.pushButton_readmem.setText("ReadMem")
            return
    def setOffline(self):
        if self.checkBox_offline.isChecked():
            self.offlineFlag = True
            self.pushButton_logstart.setEnabled(False)
            self.pushButton_saveMemDataToFile.setEnabled(False)
            self.pushButton_next.setEnabled(True)
            self.pushButton_prev.setEnabled(True)
        else:
            self.offlineFlag = False
            self.pushButton_logstart.setEnabled(True)
            self.pushButton_saveMemDataToFile.setEnabled(True)
            self.pushButton_next.setEnabled(False)
            self.pushButton_prev.setEnabled(False)

    def saveMemDataToFile(self):
        if self.stop_flag is False:
            if self.connectFlag is False:
                return
            self.pushButton_logstart.setEnabled(False)
            self.readMem_Thread.start()
            self.pushButton_saveMemDataToFile.setText("Saving")
            self.stop_flag = True
        else:
            # self.sin.emit()
            self.readMem_Thread.setBreakFlag(True)
            self.pushButton_saveMemDataToFile.setText("SaveToFile")
            self.pushButton_logstart.setEnabled(True)
            self.stop_flag = False


class ReadMemThread(QtCore.QThread):
    stateSignal = QtCore.pyqtSignal(str, int, int)
    def __init__(self, parent=None):
        super(ReadMemThread, self).__init__(parent)
        self.breakflag = False

    def run(self):
        startAddr = TFC.tfcReadDword(REG_MEM_ADDR, 0x0)
        var = TFC.tfcReadDword(REG_MEM_WRITEINDEX, 0x0)
        Cnt = var & 0xffff
        DatsSize = ((var >> 16) & 0xffff) >> 2
        Data = np.zeros(2 + Cnt * DatsSize, np.uint32)
        Data[0] = 0
        Data[1] = DatsSize

        for i in range(Cnt):
            # print "Reading: %d of %d" %(i, Cnt)
            self.stateSignal.emit("reading", i, Cnt)
            # t0 = time.clock()
            for j in range(DatsSize/2):
                if self.breakflag == True:
                    break
                tmp = i * DatsSize/2 + j

                var = TFC.tfcReadMemDword(startAddr + tmp * 4)
                Data[2*tmp + 2] = var & 0xFFF
                Data[2*tmp + 3] = ( var >> 16 ) & 0xFFF
            # print time.clock() - t0
            if self.breakflag == True:
                Data[0] = i
                break
            else:
                Data[0] = i + 1
            time.sleep(0.1)
        Data.tofile("DimmingMemLogData.bin")
        if self.breakflag is False:
            self.stateSignal.emit("finished", Data[0], Cnt)
        else:
            self.stateSignal.emit("breaked", Data[0], Cnt)

    def stop(self):
        print 'setting readMemThread flag false'
        self.breakflag = True

    def setBreakFlag(self, flag):
        self.breakflag = flag

class Worker(QtCore.QThread):
    def __init__(self, parent=None):
        super(Worker, self).__init__(parent)
        self.working = True
        self.num = 0

    def __del__(self):
        self.working = False
        self.wait()

    def run(self):
        while self.working == True:
            file_str = 'File index {0}'.format(self.num)
            self.num += 1
            self.emit(SIGNAL('output(QString)'), file_str)
            self.sleep(3)


# class MyMplCanvas(FigureCanvas):
#     """Ultimately, this is a QWidget (as well as a FigureCanvasAgg, etc.)."""
#
#     def __init__(self, parent=None, width=5, height=4, dpi=100):
#         self.fig = Figure(figsize=(width, height), dpi=dpi)
#         self.axes = self.fig.add_subplot(111)
#         # We want the axes cleared every time plot() is called
#         self.axes.hold(False)
#
#         self.compute_initial_figure()
#
#         FigureCanvas.__init__(self, self.fig)
#         self.setParent(parent)
#
#         FigureCanvas.setSizePolicy(self,
#                                    QtGui.QSizePolicy.Expanding,
#                                    QtGui.QSizePolicy.Expanding)
#         FigureCanvas.updateGeometry(self)
#
#     def sizeHint(self):
#         w, h = self.get_width_height()
#         return QtCore.QSize(w, h)
#
#     def minimumSizeHint(self):
#         return QtCore.QSize(10, 10)


# class MyStaticMplCanvas(MyMplCanvas):
#     """Simple canvas with a sine plot."""
#
#     def compute_initial_figure(self):
#         t = np.arange(0.0, 3.0, 0.01)
#         s = np.sin(2 * np.pi * t)
#         self.axes.plot(t, s)


# class MyPlotDialog(QtGui.QDialog):
#     def __init__(self):
#         super(MyPlotDialog, self).__init__()
#         uic.loadUi("plot_it.ui", self)
#         self.setWindowIcon(QtGui.QIcon("222.ico"))
#         self.main_widget = QtGui.QWidget(self)
#
#         l = QtGui.QVBoxLayout(self.main_widget)
#         sc = MyStaticMplCanvas(self.main_widget, width=5, height=4, dpi=100)
#         l.addWidget(sc)
#         self.main_widget.setFocus()
#         # self.setCentralWidget(self.main_widget)
#
#     def closeEvent(self, event):
#         reply = QtGui.QMessageBox.question(self, 'Message', "Are you sure to quit?", QtGui.QMessageBox.Yes,
#                                            QtGui.QMessageBox.No)
#         if reply == QtGui.QMessageBox.Yes:
#             event.accept()
#         else:
#             event.ignore()


if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    mywindow = MyWindow()
    mywindow.show()
    sys.exit(app.exec_())
