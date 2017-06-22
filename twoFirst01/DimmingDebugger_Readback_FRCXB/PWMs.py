__author__ = 'hooloongge'
# -*- coding: utf-8 -*-
import sys, math, random, time
import ctypes as C
import two01 as TFC
# import xmltodict
# import json
# import ConfigParser
import numpy as np
from dispmipsfunc import *
from PyQt4 import QtCore, QtGui, uic  # ,Qwt5
# import dimmingdebugger_res_sx7
from PWMs_res import *
# from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
# from matplotlib.figure import Figure
# from mpl_toolkits.mplot3d import Axes3D
# import matplotlib.pyplot as plt
# import ctypes as C
# import cProfile
# cProfile.run('main()')
# import logging

REG_LOG_DEBUG = TFC.SREG_LOG_DEBUG
BIT_LOG_DEBUG = TFC.SBIT_LOG_DEBUG
REG_MEM_ADDR = TFC.SREG_MEM_ADDR
REG_MEM_WRITEINDEX = TFC.SREG_MEM_WRITEINDEX  # [15:0] count; [31:16] size, unit byte;

class PWMsWindow(QtGui.QMainWindow):
    sin = QtCore.pyqtSignal()

    def __init__(self):
        super(PWMsWindow, self).__init__()
        # uic.loadUi("dimmingdebugger_res.ui", self)
        self.ui = Ui_Form_PWMs()
        self.ui.setupUi(self)

        self.painter = QtGui.QPainter()

        self.connectFlag = False
        self.regs_mapping_addr = [0x198A01F8, 0x0000FFFF, 0]
        self.regs_boostype_addr = [0x198800DC, 0x3, 0]
        self.pwm = np.zeros(64, np.uint32)
        for i in range(64):
            self.pwm[i] = random.randrange(100, 4095)
        self.output_pwm = np.zeros(64, np.uint32)
        print self.pwm
        # init tablewidget
        newItemt = QtGui.QTableWidgetItem('0')
        for i in range(self.ui.tableWidget_PWM.rowCount()):
            for j in range(self.ui.tableWidget_PWM.columnCount()):
                newItemt = QtGui.QTableWidgetItem('0')
                newItemt1 = QtGui.QTableWidgetItem('0')
                self.ui.tableWidget_PWM.setItem(i, j, newItemt)
        # end table init
        self.offlineFlag = False
        self.worker = Worker()
        self.log_flag = False
        self.read_flag = False
        self.stop_flag = False
        self.ui.lineEdit_PWMfile.setText("DimmingMemLogData_FRCXB.bin")
        self.readMem_Thread = ReadMemThread()
        self.readMem_Thread.setFilePath(self.ui.lineEdit_PWMfile.text())
        self.connect(self.ui.pushButton_logstart, QtCore.SIGNAL('clicked()'), self.logStart)
        self.connect(self.ui.pushButton_readmem, QtCore.SIGNAL('clicked()'), self.readMem)
        self.connect(self.ui.pushButton_nextPWM, QtCore.SIGNAL('clicked()'), self.readMemNext)
        self.connect(self.ui.pushButton_prevPWM, QtCore.SIGNAL('clicked()'), self.readMemPrev)
        self.connect(self.ui.pushButton_readmem, QtCore.SIGNAL('pressed()'), self.changeText_readMem)
        self.sin.connect(self.readMem_Thread.stop)
        self.readMem_Thread.stateSignal.connect(self.saveMemState)
        self.connect(self.ui.checkBox_offline, QtCore.SIGNAL('clicked()'), self.setOffline)
        # self.connect(self.spinBox_MemDataSelect, QtCore.SIGNAL('valueChanged(int)'), self.selectReadMem)
        self.connect(self.ui.pushButton_saveMemDataToFile, QtCore.SIGNAL('clicked()'), self.saveMemDataToFile)
        self.worker.connect(self.worker, QtCore.SIGNAL('output(QString, int)'), self.updatestatus)
        self.connect(self.ui.pushButton_chooseFile, QtCore.SIGNAL('pressed()'), self.chooseFile)

        self.DataShowiInTable()
        self.paintPWM()

    def setConnectFlag(self, flag):
        self.connectFlag = flag

    def setSettingDict(self, panel):
        self.panel_info = panel
        # print self.panel_info
        for regs in self.panel_info["registers"]:
            if regs["name"] == "mapping_id":
                self.regs_mapping_addr[0] = int(regs["address"], 16)
                self.regs_mapping_addr[1] = self.generateMask(regs["bit_start"], regs["bit_end"])
                self.regs_mapping_addr[2] = regs["bit_start"]
            if regs["name"] == "boosting_type":
                self.regs_boostype_addr[0] = int(regs["address"], 16)
                self.regs_boostype_addr[1] = self.generateMask(regs["bit_start"], regs["bit_end"])
                self.regs_boostype_addr[2] = regs["bit_start"]
        pass
    def generateMask(self,a,b):
        if(a > 31 or b> 31):
            return 0xFFFFFFFF
        if a <0 or b < 0 :
            return 0x0
        ret = 0
        for i in range(a,b+1):
            ret |= 1<<i
        # print hex(ret)
        return ret
    def paintPWM(self):
        viewWid = float(self.ui.graphicsView_PWM.width() - 2)
        viewHeight = float(self.ui.graphicsView_PWM.height() - 2)
        scene = QtGui.QGraphicsScene(self)
        scene.setSceneRect(-viewWid/2, -viewHeight/2, viewWid, viewHeight)
        if self.ui.tableWidget_PWM.rowCount() != 0 and self.ui.tableWidget_PWM.columnCount() != 0:
            rectWid = viewWid/self.ui.tableWidget_PWM.rowCount()
            rectHeight = viewHeight/self.ui.tableWidget_PWM.columnCount()
        else:
            return
        for i in range(self.ui.tableWidget_PWM.rowCount()):
            for j in range(self.ui.tableWidget_PWM.columnCount()):
                var = self.pwm[j * self.ui.tableWidget_PWM.rowCount() + i]
                br = (var & 0xFFF) >> 4
                color = QtGui.QColor(br, br, br)
                item = QtGui.QGraphicsRectItem(QtCore.QRectF(0, 0, rectWid, rectHeight))
                item.setBrush(color)
                scene.addItem(item)
                item.setPos((i * rectWid - viewWid/2), (j * rectHeight - viewHeight/2))
        self.ui.graphicsView_PWM.setScene(scene)
        self.ui.graphicsView_PWM.show()

    def DataShowiInTable(self):
        # PWM
        for i in range(self.ui.tableWidget_PWM.rowCount()):
            for j in range(self.ui.tableWidget_PWM.columnCount()):
                pwmdutytemp = "%X" % (self.pwm[i * self.ui.tableWidget_PWM.rowCount() + j])

                newItemt = QtGui.QTableWidgetItem(pwmdutytemp)
                self.ui.tableWidget_PWM.setItem(i, j, newItemt)

                # currenttablevar = "%X" % (self.current[i * self.tableWidget_PWM.rowCount() + j])
                #
                # newItemt = QtGui.QTableWidgetItem(currenttablevar)
                # self.tableWidget_Current.setItem(i, j, newItemt)
    def getpanelinfofromchip(self):
        if self.connectFlag is False:
            QtGui.QMessageBox.information(self, "warning", ("Please connect to chip first!!!\n Setting->Connect"))
            return
        if self.initFlag is True:
            return
        """
        update panel info label
        """
        self.debugregisters["mapping_id"] = (TFC.tfcReadDword(self.regs_mapping_addr[0], 0x0) \
                                             & self.regs_mapping_addr[1]) >> self.regs_mapping_addr[2]
        self.debugregisters["boosting_type"] = (TFC.tfcReadDword(self.regs_boostype_addr[0], 0x0) \
                                             & self.regs_boostype_addr[1]) >> self.regs_boostype_addr[2]
        # print self.debugregisters["mapping_id"],self.debugregisters["boosting_type"]
        self.manual_buff_addr = (TFC.tfcReadDword(self.manual_testpat_addr[0], 0x0) \
                                             & self.manual_testpat_addr[1]) << 4
        print  hex(self.manual_buff_addr)
        temps = ""
        for ledtype in self.panel_info["led_output"]:
            # print ledtype
            if ledtype[u"mapping_id"] == self.debugregisters["mapping_id"]:
                temps = temps+ ledtype["name"]
                # print ledtype["name"]
                self.debugregisters[u"led_x"] = ledtype["led_x"]
                self.debugregisters[u"led_y"] = ledtype["led_y"]
        self.ui.label_paneinfo_1.setText("Panel is %s!   LEDX=%d, LEDY=%d." % ( \
            self.panel_info["boosting_type"][self.debugregisters["boosting_type"]],\
            self.debugregisters[u"led_x"] , self.debugregisters[u"led_y"] ))
        """
        update the current pattern table widget
        """

        self.pat_size = self.debugregisters[u"led_x"] * self.debugregisters[u"led_y"]
        self.curpat = np.zeros(self.pat_size, np.uint32)
        self.curtmpppat = np.zeros((self.pat_size + 6)*TOTAL_PATS_LIMIT, np.uint16)
        self.total_manual_pat = 0
        self.reStruTable()
        self.DataShowiInTable()
        self.initFlag = True
        self.headpartupdate()
        pass
    def logStart(self):
        if self.connectFlag is False:
            QtGui.QMessageBox.information(self, "warning", ("Please connect to chip first!!!\n Setting->Connect"))
            return
        if self.log_flag is False:
            self.ui.pushButton_saveMemDataToFile.setEnabled(False)
            self.log_flag = True
            print REG_LOG_DEBUG, BIT_LOG_DEBUG
            TFC.tfcWriteDwordMask(REG_LOG_DEBUG, 0, BIT_LOG_DEBUG, BIT_LOG_DEBUG)
            print TFC.tfcReadDword(REG_LOG_DEBUG, 0)
            self.ui.pushButton_logstart.setText("Logging")
            self.worker.start()
            self.worker.setbreakflag(True)
        else:
            self.ui.pushButton_saveMemDataToFile.setEnabled(True)
            self.worker.stop()
            self.worker.setbreakflag(False)
            self.log_flag = False
            TFC.tfcWriteDwordMask(REG_LOG_DEBUG, 0, BIT_LOG_DEBUG, 0)
            self.ui.pushButton_logstart.setText("LogStart")

    def changeText_readMem(self):
        if self.connectFlag is True:
            self.ui.pushButton_readmem.setText("Reading")

    def saveMemState(self, strState, count, total):
        if strState == "finished":
            temps = "read memory finished: %d/%d" % (count, total)
            self.ui.label_Status.setText(temps)
            self.ui.pushButton_saveMemDataToFile.setText("SaveToFile")
            self.ui.pushButton_logstart.setEnabled(True)
            self.stop_flag = False
        elif strState == "reading":
            temps = "reading memory: %d/%d" % (count, total)
            self.ui.label_Status.setText(temps)
        elif strState == "breaked":
            temps = "reading memory breaked: %d/%d" % (count, total)
            self.ui.label_Status.setText(temps)
            self.readMem_Thread.setBreakFlag(False)
        elif strState == "error":
            datafile = str(self.ui.lineEdit_PWMfile.text())
            if datafile == "":
                 QtGui.QMessageBox.information(self, "warning", ("Please choose a file !!!"))
            else:
                 QtGui.QMessageBox.information(self, "warning", ("Failed to save data to file: %s !!!" %(datafile)))

    def boostingtransferpwm(self):
        for i in range(8):
            for j in range(8):
                if j < 4 and i < 4:
                    self.output_pwm[i*8+j] = self.pwm[i*4+j]
                elif j >= 4 and i < 4:
                    self.output_pwm[i * 8 + j] = self.pwm[32 + i*4 + j-4]
                elif j <4 and i >=4 :
                    self.output_pwm[i * 8 + j] = self.pwm[16+(i -4)*4 +j]
                else:
                    self.output_pwm[i * 8 + j] = self.pwm[48+(i-4)*4 + j-4]
        for i in range(64):
            self.pwm[i] = self.output_pwm[i]

        pass

    def updatePWM(self, size, num, tstartAddr, tData):
        for i in range(self.ui.tableWidget_PWM.rowCount()):
            for j in range(self.ui.tableWidget_PWM.columnCount()):
                tmp = i * self.ui.tableWidget_PWM.rowCount() + j
                tmpreg = tmp/2
                if self.offlineFlag is True:
                    var = tData[2 + tmp + size * num]
                else:
                    if tmp % 2 == 0:
                        var = TFC.tfcReadMemDword(tstartAddr + 4 * (tmpreg + size * num/2)) & 0xFFF
                    else:
                        var = (TFC.tfcReadMemDword(tstartAddr + 4 * (tmpreg + size * num / 2)) >> 16) & 0xFFF
                self.pwm[tmp] = var & 0xFFF
        # print self.pwm

        self.boostingtransferpwm()
        # print self.pwm
        for i in range(self.ui.tableWidget_PWM.rowCount()):
            for j in range(self.ui.tableWidget_PWM.columnCount()):
                tmp = i * self.ui.tableWidget_PWM.rowCount() + j
                var = self.pwm[tmp]
                pwmdutytemp = "%X" % (var & 0xFFF)
                newItemt = QtGui.QTableWidgetItem(pwmdutytemp)
                self.ui.tableWidget_PWM.setItem(i, j, newItemt)
        # print self.pwm
        self.paintPWM()
        self.update()

    def readOfflineData(self, readCommand):
        if self.offlineFlag is True:
            try:
                datafile = str(self.ui.lineEdit_PWMfile.text())
                Data = np.fromfile(datafile, dtype=np.uint32)
                Cnt = Data[0]
                DataSize = Data[1]
                tableSize = self.ui.tableWidget_PWM.rowCount() * self.ui.tableWidget_PWM.columnCount()
                if Cnt == 0:
                    # print "no data in file: %s" %(datafile)
                    QtGui.QMessageBox.information(self, "warning", ("no data in file: %s" % (datafile)))
                elif DataSize != tableSize:
                    # print("Size not match!!!! file: %d, table: %d" % (DataSize, tableSize))
                    QtGui.QMessageBox.information(self, "warning", (
                        "Data size not match!!!! file: %d, table: %d" % (DataSize, tableSize)))
                else:
                    num = self.ui.spinBox_MemDataSelect.value()
                    if readCommand == "Prev":
                        if num > 0:
                            num -= 1
                    elif readCommand == "Next":
                        num += 1

                    if num >= Cnt:
                        num = Cnt - 1
                    self.ui.spinBox_MemDataSelect.setValue(num)
                    self.updatePWM(DataSize, num, 0, Data)
                    self.ui.spinBox_MemDataSelect.setRange(0, Cnt - 1)
            except Exception, e:
                # print Exception, ":", e
                QtGui.QMessageBox.about(self, "Warning", str(e))
            self.update()
            return

    def readMem(self):
        if self.offlineFlag is False:
            if self.connectFlag is False:
                QtGui.QMessageBox.information(self, "warning", ("Please connect to chip first!!!\n Setting->Connect"))
                return
            if self.read_flag is False:
                startAddr = TFC.tfcReadDword(REG_MEM_ADDR, 0x0)
                var = TFC.tfcReadDword(REG_MEM_WRITEINDEX, 0x0)
                Cnt = var & 0xffff
                Size = ((var >> 16) & 0xffff) >> 2
                tableSize = self.ui.tableWidget_PWM.rowCount() * self.ui.tableWidget_PWM.columnCount()
                # p = C.create_string_buffer("",10000)
                # print p[0], p[1], p[2]
                # s = C.cast(p,C.c_char_p)
                # TFC.tfcReadFB(startAddr, 64,s)
                if Size != tableSize:
                    # print("Size not match!!!! firmware: %d, tool: %d" % (Size, tableSize))
                    QtGui.QMessageBox.information(self, "warning", (
                    "Data size not match!!!! file: %d, table: %d" % (Size, tableSize)))
                    self.ui.pushButton_readmem.setText("ReadMem")
                    return
                elif Cnt == 0:
                    # print("nothing in memory!!! cnt = %d" % (Cnt))
                    QtGui.QMessageBox.information(self, "warning", ("nothing in memory!!! cnt = %d" % (Cnt)))
                    self.ui.pushButton_readmem.setText("ReadMem")
                    return
                else:
                    num = self.ui.spinBox_MemDataSelect.value()
                    if num >= Cnt:
                        num = Cnt - 1
                        self.ui.spinBox_MemDataSelect.setValue(num)
                    self.updatePWM(Size, num, startAddr, 0)
                    # self.readMem_Thread.start()
                    self.ui.spinBox_MemDataSelect.setRange(0, Cnt - 1)
                    #     self.read_flag = True
                    # else:
                # self.sin.emit()
                self.ui.pushButton_readmem.setText("ReadMem")
                # self.read_flag = False
        else:
            self.readOfflineData("Current")

    def readMemPrev(self):
        self.readOfflineData("Prev")

    def readMemNext(self):
        self.readOfflineData("Next")

    def setOffline(self):
        if self.ui.checkBox_offline.isChecked():
            self.offlineFlag = True
            self.ui.pushButton_logstart.setEnabled(False)
            self.ui.pushButton_saveMemDataToFile.setEnabled(False)
            self.ui.pushButton_nextPWM.setEnabled(True)
            self.ui.pushButton_prevPWM.setEnabled(True)
        else:
            self.offlineFlag = False
            self.ui.pushButton_logstart.setEnabled(True)
            self.ui.pushButton_saveMemDataToFile.setEnabled(True)
            self.ui.pushButton_nextPWM.setEnabled(False)
            self.ui.pushButton_prevPWM.setEnabled(False)

    def saveMemDataToFile(self):
        datafile = str(self.ui.lineEdit_PWMfile.text())
        if datafile == "":
            QtGui.QMessageBox.information(self, "warning", ("Please choose a file !!!"))
            return
        if self.stop_flag is False:
            if self.connectFlag is False:
                QtGui.QMessageBox.information(self, "warning", ("Please connect to chip first!!!\n Setting->Connect"))
                return
            self.ui.pushButton_logstart.setEnabled(False)
            self.readMem_Thread.setFilePath(self.ui.lineEdit_PWMfile.text())
            self.readMem_Thread.start()
            self.ui.pushButton_saveMemDataToFile.setText("Saving")
            self.stop_flag = True
        else:
            # self.sin.emit()
            self.readMem_Thread.setBreakFlag(True)
            self.ui.pushButton_saveMemDataToFile.setText("SaveToFile")
            self.ui.pushButton_logstart.setEnabled(True)
            self.stop_flag = False

    def updatestatus(self,mess, num):
        if num >= 495:
            self.logStart()
            num = TFC.tfcReadDword(REG_MEM_WRITEINDEX, 0x0) & 0xFFFF
            temps = "logging index: %d" % (num)
            self.ui.label_Status.setText(temps)
        else:
            self.ui.label_Status.setText(mess)

    def chooseFile(self):
        file = QtGui.QFileDialog.getOpenFileName(self, "Open File dialog", "/", "bin files(*.bin *.txt)")
        if file:
            self.ui.lineEdit_PWMfile.setText(file)


class ReadMemThread(QtCore.QThread):
    stateSignal = QtCore.pyqtSignal(str, int, int)

    def __init__(self, parent=None):
        super(ReadMemThread, self).__init__(parent)
        self.breakflag = False
        self.filepath = "DimmingMemLogData_FRCXB.bin"

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
            for j in range(DatsSize / 2):
                if self.breakflag == True:
                    break
                tmp = i * DatsSize / 2 + j

                var = TFC.tfcReadMemDword(startAddr + tmp * 4)
                Data[2 * tmp + 2] = var & 0xFFF
                Data[2 * tmp + 3] = (var >> 16) & 0xFFF
            # print time.clock() - t0
            if self.breakflag == True:
                Data[0] = i
                break
            else:
                Data[0] = i + 1
            time.sleep(0.01)
        try:
            Data.tofile(self.filepath)
        except Exception, e:
            print e
            self.stateSignal.emit("error", Data[0], Cnt)
        if self.breakflag is False:
            self.stateSignal.emit("finished", Data[0], Cnt)
        else:
            self.stateSignal.emit("breaked", Data[0], Cnt)

    def stop(self):
        print 'setting readMemThread flag false'
        self.breakflag = True

    def setBreakFlag(self, flag):
        self.breakflag = flag
        print "read mem break"

    def setFilePath(self, filePath):
        self.filepath = str(filePath)


class Worker(QtCore.QThread):
    def __init__(self, parent=None):
        super(Worker, self).__init__(parent)
        self.working = True
        self.num = 0

    def __del__(self):
        self.working = False
        self.wait()

    def stop(self):
        print 'logging stop'
        self.working = False

    def setbreakflag(self, flag):
        self.working = flag

    def run(self):
        self.cnt = 0
        self.num1 = 0
        while self.working == True and self.cnt < 1000:
            time.sleep(0.04)
            self.cnt += 1
            self.num1 = TFC.tfcReadDword(REG_MEM_WRITEINDEX, 0x0) & 0xFFFF
            if self.num != self.num1:
                self.num = self.num1
                file_str = 'logging index: {0}'.format(self.num)
                self.emit(QtCore.SIGNAL('output(QString, int)'), file_str, self.num)

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    test = PWMsWindow()
    test.show()
    sys.exit(app.exec_())