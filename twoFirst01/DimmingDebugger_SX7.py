__author__ = 'hooloongge'
# -*- coding: utf-8 -*-
import sys, math, random, time
import ctypes as C
import two01 as TFC
# import xmltodict
import json
import ConfigParser
import numpy as np
from dispmipsfunc import *
from PyQt4 import QtCore, QtGui, uic  # ,Qwt5

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


class MyWindow(QtGui.QMainWindow):
    sin = QtCore.pyqtSignal()

    def __init__(self):
        super(MyWindow, self).__init__()
        uic.loadUi("dimmingdebugger_res.ui", self)
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
            self.pwm[i] = random.randrange(100, 4095)
        self.current = np.ones(64, np.uint32)
        self.output_pwm = np.zeros(64, np.uint32)
        self.output_current = np.ones(64, np.uint32)
        print self.pwm
        # init tablewidget
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
        # end table init
        self.offlineFlag = False
        self.readMem_Thread = ReadMemThread()
        self.worker = Worker()
        self.log_flag = False
        self.read_flag = False
        self.stop_flag = False
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
        self.connect(self.pushButton_plotout, QtCore.SIGNAL('clicked()'), self.CreateNewPlotDailog_1)
        self.connect(self.pushButton_plotin, QtCore.SIGNAL('clicked()'), self.CreateNewPlotDailog)
        # self.connect(self.pushButton_plot, QtCore.SIGNAL('clicked()'), self.CreateNewPlotDailog_2)
        self.actionQuit.connect(self.actionQuit, QtCore.SIGNAL('triggered()'), QtGui.qApp, QtCore.SLOT('quit()'))
        self.actionOpen_setting_file.connect(self.actionOpen_setting_file, QtCore.SIGNAL('triggered()'),
                                             self.loadSettingfromJson)
        self.actionSave_setting_file.connect(self.actionSave_setting_file, QtCore.SIGNAL('triggered()'),
                                             self.saveSettingfromJson)
        self.connect(self.pushButton_logstart, QtCore.SIGNAL('clicked()'), self.logStart)
        self.connect(self.pushButton_readmem, QtCore.SIGNAL('clicked()'), self.readMem)
        self.connect(self.pushButton_next, QtCore.SIGNAL('clicked()'), self.readMemNext)
        self.connect(self.pushButton_prev, QtCore.SIGNAL('clicked()'), self.readMemPrev)
        self.connect(self.pushButton_readmem, QtCore.SIGNAL('pressed()'), self.changeText_readMem)
        self.sin.connect(self.readMem_Thread.stop)
        self.readMem_Thread.stateSignal.connect(self.saveMemState)
        self.connect(self.checkBox_offline, QtCore.SIGNAL('clicked()'), self.setOffline)
        # self.connect(self.spinBox_MemDataSelect, QtCore.SIGNAL('valueChanged(int)'), self.selectReadMem)
        self.connect(self.pushButton_saveMemDataToFile, QtCore.SIGNAL('clicked()'), self.saveMemDataToFile)
        self.worker.connect(self.worker, QtCore.SIGNAL('output(QString)'), self.updatestatus)
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
            pass
        else:
            self.pushButton_readpwm.setText("Reading")

    def changeText_current(self):
        if self.connectFlag == False:
            pass
        else:
            self.pushButton_readcurrent.setText("Reading")

    def readPWM(self):
        # added read from registers
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
        self.current = self.current * self.s_dict["normal_current_mid"]
        for i in range(self.tableWidget_PWM.rowCount()):
            for j in range(self.tableWidget_PWM.columnCount()):
                pwmdutytemp = "%X" % (self.pwm[i * self.tableWidget_PWM.rowCount() + j])

                newItemt = QtGui.QTableWidgetItem(pwmdutytemp)
                self.tableWidget_PWM.setItem(i, j, newItemt)

                currenttablevar = "%X" % (self.current[i * self.tableWidget_PWM.rowCount() + j])

                newItemt = QtGui.QTableWidgetItem(currenttablevar)
                self.tableWidget_Current.setItem(i, j, newItemt)

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
            global_gain = self.s_dict["peak_max_global_gain"] - (peak_sum - self.s_dict["peak_min_num"]) * (
                self.s_dict["peak_max_global_gain"] - self.s_dict["peak_min_global_gain"]) / (
                                                                    self.s_dict["peak_max_num"] - self.s_dict[
                                                                        "peak_min_num"])

        for i in range(led_size):
            self.output_pwm[i] = self.pwm[i] * global_gain / 100
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
        assert isinstance(dc_max_sum, object)
        print dc_peak_num, peak_sum, global_gain, dc_max_sum
        for i in range(dc_size):
            power_max = self.s_dict["power_max"] * self.s_dict["power_max_percent"] * 2 / 100
            if dc_max_sum[i][4] > power_max:
                reduce_pwm_sum = dc_max_sum[i][4] - power_max
                if (dc_max_sum[i][1] * (100 - self.s_dict["limit_cof"]) / 100) > reduce_pwm_sum:
                    reduce_pwm_coef[i][0] = 100 - reduce_pwm_sum * 100 / dc_max_sum[i][1]
                    continue
                else:
                    reduce_pwm_sum -= (dc_max_sum[i][1] * (100 - self.s_dict["limit_cof"])) / 100
                    reduce_pwm_coef[i][0] = self.s_dict["limit_cof"]
                if (dc_max_sum[i][2] * (100 - self.s_dict["limit_cof"]) / 100) > reduce_pwm_sum:
                    reduce_pwm_coef[i][1] = 100 - reduce_pwm_sum * 100 / dc_max_sum[i][2]
                    continue
                else:
                    reduce_pwm_sum -= (dc_max_sum[i][2] * (100 - self.s_dict["limit_cof"])) / 100
                    reduce_pwm_coef[i][1] = self.s_dict["limit_cof"]
                reduce_pwm_coef[i][2] = 100 - (reduce_pwm_sum * 100 / dc_max_sum[i][3])
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
            self.output_pwm[i] = (self.output_pwm[i] * reduce_pwm) / 100
        self.outputPWM()

    def Algo_2(self):
        self.outputPWM()
        # self.outputCurrent()

    def Algo_3(self):
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
        # dc_mapping_3820_m70 = np.array(
        #     [0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 2, 2, 2, 2, 3, 3, 3, 3, 3, 3, 3, 3, 2, 2, 2, 2, 4, 4, 4, 4,
        #      5, 5, 5, 5, 5, 5, 5, 5, 4, 4, 4, 4, 6, 6, 6, 6, 7, 7, 7, 7, 7, 7, 7, 7, 6, 6, 6, 6], np.uint32)
        dc_mapping_3820_m70 = np.array(
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2,
             2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3], np.uint32)
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
            global_gain = self.s_dict["peak_max_global_gain"] - (peak_sum - self.s_dict["peak_min_num"]) * (
                self.s_dict["peak_max_global_gain"] - self.s_dict["peak_min_global_gain"]) / (
                                                                    self.s_dict["peak_max_num"] - self.s_dict[
                                                                        "peak_min_num"])
        global_current_set = (global_gain * self.s_dict["peak_current_max"]) / 100

        # self.current *= self.s_dict["normal_current_mid"]
        self.current = np.ones(64, np.uint32)
        self.current = self.current * (global_gain * self.s_dict["peak_current_max"]) / 100
        print self.current
        for i in range(led_size):
            self.output_pwm[i] = self.pwm[i] * global_current_set  # scale the output brightness = pwm*current
        # print self.output_pwm
        for i in range(led_size):
            tmp_i = dc_mapping_3820_m70[i]
            if self.output_pwm[i] > self.s_dict["peak_value_thr"]:
                dc_max_sum[tmp_i][3] += self.output_pwm[i]
            elif self.output_pwm[i] > self.s_dict["medium_value_thr"]:
                dc_max_sum[tmp_i][2] += self.output_pwm[i]
            elif self.output_pwm[i] > self.s_dict["low_value_thr"]:
                dc_max_sum[tmp_i][1] += self.output_pwm[i]
            else:
                dc_max_sum[tmp_i][0] += self.output_pwm[i]
            dc_max_sum[tmp_i][4] += self.output_pwm[i]

        print dc_peak_num, peak_sum, global_gain, dc_max_sum
        power_max = self.s_dict["power_max"] * self.s_dict["power_max_percent"] / 100
        for i in range(dc_size):
            if dc_max_sum[i][4] > power_max:
                reduce_pwm_sum = dc_max_sum[i][4] - power_max
                if (dc_max_sum[i][1] * (100 - self.s_dict["limit_cof"]) / 100) > reduce_pwm_sum:
                    reduce_pwm_coef[i][0] = 100 - reduce_pwm_sum * 100 / dc_max_sum[i][1]
                    continue
                else:
                    reduce_pwm_sum -= (dc_max_sum[i][1] * (100 - self.s_dict["limit_cof"])) / 100
                    reduce_pwm_coef[i][0] = self.s_dict["limit_cof"]
                if (dc_max_sum[i][2] * (100 - self.s_dict["limit_cof"]) / 100) > reduce_pwm_sum:
                    reduce_pwm_coef[i][1] = 100 - reduce_pwm_sum * 100 / dc_max_sum[i][2]
                    continue
                else:
                    reduce_pwm_sum -= (dc_max_sum[i][2] * (100 - self.s_dict["limit_cof"])) / 100
                    reduce_pwm_coef[i][1] = self.s_dict["limit_cof"]
                reduce_pwm_coef[i][2] = 100 - (reduce_pwm_sum * 100 / dc_max_sum[i][3])
        print reduce_pwm_coef
        print self.output_pwm
        for i in range(led_size):
            tmp_i = dc_mapping_3820_m70[i]
            if self.pwm[i] > self.s_dict["peak_value_thr"]:
                reduce_pwm = reduce_pwm_coef[tmp_i][2]
                self.output_pwm[i] = self.pwm[i]
                self.output_current[i] = self.current[i] * reduce_pwm / 100
            elif self.pwm[i] > self.s_dict["medium_value_thr"]:
                reduce_pwm = reduce_pwm_coef[tmp_i][1]
                self.output_current[i] = self.current[i] * reduce_pwm / 100
                if self.output_current[i] < self.s_dict["lowest_current_min"]:
                    self.output_pwm[i] = self.pwm[i] * (
                        2 * self.s_dict["lowest_current_min"] - self.output_current[i]) / self.s_dict[
                                             "lowest_current_min"]
                    self.output_current[i] = self.s_dict["lowest_current_min"]
                    if self.output_pwm[i] > 0xFFF:
                        self.output_pwm[i] = 0xFFF
                else:
                    self.output_pwm[i] = self.pwm[i]
            elif self.pwm[i] > self.s_dict["low_value_thr"]:
                reduce_pwm = reduce_pwm_coef[tmp_i][0]
                self.output_current[i] = self.current[i] * reduce_pwm / 100
                if self.output_current[i] < self.s_dict["lowest_current_min"]:
                    self.output_pwm[i] = self.pwm[i] * (
                        2 * self.s_dict["lowest_current_min"] - self.output_current[i]) / \
                                         self.s_dict["lowest_current_min"]
                    self.output_current[i] = self.s_dict["lowest_current_min"]
                    if self.output_pwm[i] > 0xFFF:
                        self.output_pwm[i] = 0xFFF
                else:
                    self.output_pwm[i] = self.pwm[i]
            else:
                self.output_current[i] = self.s_dict["lowest_current_min"]
                self.output_pwm[i] = 0xE * self.pwm[i]
                # self.output_pwm[i] = (self.output_pwm[i] * reduce_pwm) / 100
        print self.output_current
        self.outputPWM()
        self.outputCurrent()

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
            print REG_LOG_DEBUG, BIT_LOG_DEBUG
            TFC.tfcWriteDwordMask(REG_LOG_DEBUG, 0, BIT_LOG_DEBUG, BIT_LOG_DEBUG)
            print TFC.tfcReadDword(REG_LOG_DEBUG, 0)
            self.pushButton_logstart.setText("Logging")
            self.worker.start()
            self.worker.setbreakflag(True)
        else:
            self.log_flag = False
            TFC.tfcWriteDwordMask(REG_LOG_DEBUG, 0, BIT_LOG_DEBUG, 0)
            self.pushButton_logstart.setText("LogStart")
            self.worker.stop()
            self.worker.setbreakflag(False)

    def changeText_readMem(self):
        if self.connectFlag is True:
            self.pushButton_readmem.setText("Reading")

    def saveMemState(self, strState, count, total):
        if strState == "finished":
            print "read memory finished. %d/%d" % (count, total)
            # self.pushButton_readmem.setText("ReadMem")
            # self.read_flag = False
            self.pushButton_saveMemDataToFile.setText("SaveToFile")
            self.pushButton_logstart.setEnabled(True)
            self.stop_flag = False
        elif strState == "reading":
            temps = "reading memory: %d/%d" % (count, total)
            print temps
            self.statusBar().showMessage(temps)
        elif strState == "breaked":
            temps = "reading memory breaked: %d/%d" % (count, total)
            print temps
            self.statusBar().showMessage(temps)
            self.readMem_Thread.setBreakFlag(False)

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
        for i in range(self.tableWidget_PWM.rowCount()):
            for j in range(self.tableWidget_PWM.columnCount()):
                tmp = i * self.tableWidget_PWM.rowCount() + j
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
        for i in range(self.tableWidget_PWM.rowCount()):
            for j in range(self.tableWidget_PWM.columnCount()):
                tmp = i * self.tableWidget_PWM.rowCount() + j
                var = self.pwm[tmp]
                pwmdutytemp = "%X" % (var & 0xFFF)
                newItemt = QtGui.QTableWidgetItem(pwmdutytemp)
                self.tableWidget_PWM.setItem(i, j, newItemt)
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
                    print("Size not match!!!! firmware: %d, tool: %d" % (Size, tableSize))
                    self.pushButton_readmem.setText("ReadMem")
                    return
                elif Cnt == 0:
                    print("nothing in memory!!! cnt = %d" % (Cnt))
                    self.pushButton_readmem.setText("ReadMem")
                    return
                else:
                    num = self.spinBox_MemDataSelect.value()
                    if num >= Cnt:
                        num = Cnt - 1
                        self.spinBox_MemDataSelect.setValue(num)
                    self.updatePWM(Size, num, startAddr, 0)
                    # self.readMem_Thread.start()
                    self.spinBox_MemDataSelect.setRange(0, Cnt - 1)
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
                    print("Size not match!!!! file: %d, table: %d" % (DataSize, tableSize))
                else:
                    num = self.spinBox_MemDataSelect.value()
                    if num >= Cnt:
                        num = Cnt - 1
                    self.spinBox_MemDataSelect.setValue(num)
                    self.updatePWM(DataSize, num, 0, Data)
                    self.spinBox_MemDataSelect.setRange(0, Cnt - 1)
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
                    print("Size not match!!!! file: %d, table: %d" % (DataSize, tableSize))
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
    def updatestatus(self,mess):
        self.statusBar().showMessage(mess)


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

    def stop(self):
        print 'logging stop'
        self.working = False

    def setbreakflag(self, flag):
        self.working = flag

    def run(self):
        self.cnt = 0
        self.num1 = 0
        while self.working == True and self.cnt < 1000:
            time.sleep(0.1)
            self.cnt += 1
            self.num1 = TFC.tfcReadDword(REG_MEM_WRITEINDEX, 0x0) & 0xFFFF
            if self.num != self.num1:
                self.num = self.num1
                file_str = 'logging index: {0}'.format(self.num)
                self.emit(QtCore.SIGNAL('output(QString)'), file_str)



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
