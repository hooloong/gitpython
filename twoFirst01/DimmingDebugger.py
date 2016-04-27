__author__ = 'hooloongge'
# -*- coding: utf-8 -*-
import sys,math,random,time
import ctypes as C
import two01 as TFC
import xmltodict
import json
import ConfigParser
import numpy as np
from dispmipsfunc import *
from PyQt4 import QtCore, QtGui, uic, Qwt5


class MyWindow(QtGui.QMainWindow):
    def __init__(self):
        super(MyWindow, self).__init__()
        uic.loadUi("dimmingdebugger.ui", self)
        self.setWindowIcon(QtGui.QIcon("222.ico"))
        # self.setGeometry(300,300,810,640)
        self.statusBar().showMessage('DisConnected to chip!!!')
        self.painter = QtGui.QPainter()

        self.s_dict = dict(defaultfilename="parameters.json")
        self.connectFlag = 0
        self.pwm = np.zeros(64,np.uint32)
        # self.pwm *= 0xA00
        # self.pwm.dtype = np.uint32
        for i in range(64):
            self.pwm[i] = random.randrange(100,4095)
        self.current = np.zeros(64,np.uint32)
        self.output_pwm = np.zeros(64,np.uint32)
        print self.pwm
        #init tablewidget
        newItemt = QtGui.QTableWidgetItem('0')
        for i in range(self.tableWidget_PWM.rowCount()):
            for j in range(self.tableWidget_PWM.columnCount()):
                newItemt = QtGui.QTableWidgetItem('0')
                newItemt1 = QtGui.QTableWidgetItem('0')
                self.tableWidget_PWM.setItem(i, j, newItemt)
                self.tableWidget_PWM_2.setItem(i, j, newItemt1)
        for i in range(self.tableWidget_Current.rowCount()):
            for j in range(self.tableWidget_Current.columnCount()):
                newItemt = QtGui.QTableWidgetItem('0')
                newItemt1 = QtGui.QTableWidgetItem('0')
                self.tableWidget_Current.setItem(i, j, newItemt)
                self.tableWidget_Current_2.setItem(i, j, newItemt1)
        #end table init
        self.connect(self.actionConnect, QtCore.SIGNAL('triggered()'), self.connectChip)
        self.connect(self.actionDisconnect, QtCore.SIGNAL('triggered()'), self.disconnectChip)
        self.connect(self.pushButton_readpwm, QtCore.SIGNAL('clicked()'), self.readPWM)
        self.connect(self.pushButton_readpwm, QtCore.SIGNAL('pressed()'), self.changeText_pwm)
        self.connect(self.pushButton_readcurrent, QtCore.SIGNAL('pressed()'), self.changeText_current)
        self.connect(self.pushButton_readcurrent, QtCore.SIGNAL('clicked()'), self.readCurrent)
        self.connect(self.pushButton_flushimg, QtCore.SIGNAL('clicked()'), self.update)
        self.connect(self.pushButton_A1, QtCore.SIGNAL('clicked()'), self.Algo_1)
        self.connect(self.pushButton_A2, QtCore.SIGNAL('clicked()'), self.Algo_2)
        self.connect(self.pushButton_A3, QtCore.SIGNAL('clicked()'), self.Algo_3)
        self.actionQuit.connect(self.actionQuit, QtCore.SIGNAL('triggered()'), QtGui.qApp, QtCore.SLOT('quit()'))
        self.actionOpen_setting_file.connect(self.actionOpen_setting_file, QtCore.SIGNAL('triggered()'),
                                             self.loadSettingfromJson)
        self.actionSave_setting_file.connect(self.actionSave_setting_file, QtCore.SIGNAL('triggered()'),
                                             self.saveSettingfromJson)

        self.loadSettingfromJson()
        self.PWMshowinTable()
    def paintEvent(self, envent):
        self.painter.begin(self)
        startposx = self.tableWidget_Paras.x()
        startposy = self.tableWidget_Paras.y() + self.tableWidget_Paras.height() + 60
        for i in range(8):
            for j in range(8):
                var = self.pwm[j * self.tableWidget_Current.rowCount() + i]
                br = (var & 0xFFF) >> 4
                color = QtGui.QColor(br, br, br)
                self.painter.setBrush(color)
                self.painter.drawRect(startposx + i * 40, startposy + j * 30, 40, 30)
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
            return
        self.pushButton_readpwm.setText("Reading")

    def changeText_current(self):
        if self.connectFlag == False:
            return
        self.pushButton_readcurrent.setText("Reading")

    def readPWM(self):
        #added read from registers
        if self.connectFlag is False:
            return
        for i in range(self.tableWidget_PWM.rowCount()):
            for j in range(self.tableWidget_PWM.columnCount()):
                TFC.tfc2ddWriteDword(0x68, 0xA5)
                TFC.tfc2ddWriteDword(0x6C, i * self.tableWidget_PWM.rowCount() + j)
                time.sleep(0.05)
                var = TFC.tfc2ddReadDword(0x68) >> 8;
                self.pwm[i * self.tableWidget_PWM.rowCount() + j] = var & 0xFFF
                pwmdutytemp = "%X" % (var & 0xFFF)
                newItemt = QtGui.QTableWidgetItem(pwmdutytemp)
                self.tableWidget_PWM.setItem(i, j, newItemt)
        self.pushButton_readpwm.setText("ReadPWM")
        # print self.pushButton_readpwm.text
        print self.pwm
        self.update()
    def PWMshowinTable(self):
        for i in range(self.tableWidget_PWM.rowCount()):
            for j in range(self.tableWidget_PWM.columnCount()):
                pwmdutytemp = "%X" % (self.pwm[i * self.tableWidget_PWM.rowCount() + j])
                newItemt = QtGui.QTableWidgetItem(pwmdutytemp)
                self.tableWidget_PWM.setItem(i, j, newItemt)

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
                var = self.current[i * self.tableWidget_Current.rowCount() + j]
                pwmdutytemp = "%X" % (var & 0xFFF)
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

    def Algo_1(self):
        peak_sum = 0
        # global_gain = 1024
        reduce_pwm = 100
        led_x = self.s_dict["led_x"]
        led_y = self.s_dict["led_y"]
        led_size = led_x * led_y
        dc_size = self.s_dict["dc_dc_size"]
        dc_max_sum = np.zeros((8, 5), np.uint32)
        reduce_pwm_coef = np.ones((8, 3), np.uint32)
        reduce_pwm_coef *= 100
        dc_peak_num = np.zeros(8, np.uint32)
        reduce_pwm_sum = 0
        dc_mapping_3820_m70 = np.array(
            [0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 2, 2, 2, 2, 3, 3, 3, 3, 3, 3, 3, 3, 2, 2, 2, 2, 4, 4, 4, 4,
             5, 5, 5, 5, 5, 5, 5, 5, 4, 4, 4, 4, 6, 6, 6, 6, 7, 7, 7, 7, 7, 7, 7, 7, 6, 6, 6, 6], np.uint32)
        # dc_mapping_3820_m70.shape = (8, 8)

        for i in range(led_size):
            tmp_i = dc_mapping_3820_m70[i]
            if self.pwm[i] > self.s_dict["peak_value_thr"]:
                dc_peak_num[tmp_i] += 1
                peak_sum += 1
        if peak_sum >= self.s_dict["peak_max_num"]:
            global_gain = self.s_dict["peak_min_global_gain"]
        elif peak_sum <= self.s_dict["peak_min_num"]:
            global_gain = self.s_dict["peak_max_global_gain"]
        else:
            global_gain = self.s_dict["peak_max_global_gain"] - (peak_sum - self.s_dict["peak_min_num"]) * (self.s_dict["peak_max_global_gain"] - self.s_dict["peak_min_global_gain"]) / (self.s_dict["peak_max_num"] - self.s_dict["peak_min_num"])

        for i in range(led_size):
            self.output_pwm[i] = self.pwm[i] * global_gain /100
        # print self.output_pwm
        for i in range(led_size):
            tmp_i = dc_mapping_3820_m70[i]
            if self.output_pwm[i] > self.s_dict["peak_value_thr"]:
                dc_max_sum[tmp_i][3] += self.output_pwm[i] * 256
            elif self.output_pwm[i] > self.s_dict["medium_value_thr"]:
                dc_max_sum[tmp_i][2] += self.output_pwm[i] * 256
            elif self.output_pwm[i] > self.s_dict["low_value_thr"]:
                dc_max_sum[tmp_i][1] += self.output_pwm[i] * 256
            else:
                dc_max_sum[tmp_i][0] += self.output_pwm[i] * 256
            dc_max_sum[tmp_i][4] += self.output_pwm[i]
        print dc_peak_num, peak_sum, global_gain, dc_max_sum
        for i in range(dc_size):
            power_max = self.s_dict["power_max"] * self.s_dict["power_max_percent"] * 2 /100
            if dc_max_sum[i][4] > power_max:
                reduce_pwm_sum = dc_max_sum[i][4] - power_max
                if (dc_max_sum[i][1] * (100 - self.s_dict["limit_cof"])/100) > reduce_pwm_sum:
                    reduce_pwm_coef[i][0] = 100 - reduce_pwm_sum*100/dc_max_sum[i][1]
                    continue
                else:
                    reduce_pwm_sum -= (dc_max_sum[i][1] * (100 - self.s_dict["limit_cof"]))/100
                    reduce_pwm_coef[i][0] = self.s_dict["limit_cof"]
                if (dc_max_sum[i][2] * (100 - self.s_dict["limit_cof"])/100) > reduce_pwm_sum:
                    reduce_pwm_coef[i][1] = 100 - reduce_pwm_sum*100/dc_max_sum[i][2]
                    continue
                else:
                    reduce_pwm_sum -= (dc_max_sum[i][2] * (100 - self.s_dict["limit_cof"]))/100
                    reduce_pwm_coef[i][1] = self.s_dict["limit_cof"]
                reduce_pwm_coef[i][2] = 100 - (reduce_pwm_sum * 100 /dc_max_sum[i][3])
        for i in range(led_size):
            tmp_i = dc_mapping_3820_m70[i]
            if self.output_pwm[i] > self.s_dict["peak_value_thr"]:
                reduce_pwm = reduce_pwm_coef[tmp_i][2]
            elif self.output_pwm[i] > self.s_dict["medium_value_thr"]:
                reduce_pwm = reduce_pwm_coef[tmp_i][1]
            elif self.output_pwm[i] > self.s_dict["low_value_thr"]:
                reduce_pwm = reduce_pwm_coef[tmp_i][0]
            else:
                reduce_pwm = 100
            self.output_pwm[i] *= reduce_pwm/100
        self.outputPWM()
    def Algo_2(self):
        self.outputPWM()
        # self.outputCurrent()

    def Algo_3(self):
        pass

    def closeEvent(self, event):
        reply = QtGui.QMessageBox.question(self, 'Message', "Are you sure to quit?", QtGui.QMessageBox.Yes,
                                           QtGui.QMessageBox.No)
        if reply == QtGui.QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()


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


if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    mywindow = MyWindow()
    mywindow.show()
    app.exec_()
