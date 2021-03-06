__author__ = 'hooloongge'
# -*- coding: utf-8 -*-
import sys, math, random, time
import ctypes as C
import two01 as TFC
import xmltodict
import json
import ConfigParser
import numpy as np
from dispmipsfunc import *
from PyQt4 import QtCore, QtGui, uic
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
# import cProfile
# cProfile.run('main()')
# import logging

class MyWindow(QtGui.QMainWindow):
    def __init__(self):
        super(MyWindow, self).__init__()
        uic.loadUi("dimmiming_boosting_2017_res.ui", self)
        self.setWindowIcon(QtGui.QIcon("222.ico"))
        self.statusBar().showMessage('DisConnected to chip!!!')
        self.painter = QtGui.QPainter()

        #self.s_dict = dict(defaultfilename="parameters.json")
        # self.setGeometry(300,300,810,640)
        self.s_dict = dict(defaultfilename="parameters_m50.json")
        self.connectFlag = False
        self.pwm = np.zeros(64, np.uint32)
        self.loadSettingfromJson()
        # self.pwm *= 0xA00
        # self.pwm.dtype = np.uint32
        self.totalsize = self.s_dict["led_size"]
        self.default_pwm = np.array(
            [0, 0, 0, 0, 0x85C, 0x85E, 0xED6, 0xFFF, 0x9A3, 0xA18, 0xA61, 0xFFF, 0xAE3, 0x84C, 0xB44, 0xD5E, 0xC7B, 0xCE3, 0xFFF, 0xF31,
             0xD4B, 0xD4C, 0xFFF, 0xD4C, 0xED0, 0xED0, 0xFFF, 0xF39, 0, 0, 0, 0], np.uint32)
        for i in range(self.totalsize):
            self.pwm[i] = self.default_pwm[i]
            # self.pwm[i] = random.randrange(100, 4095)
        self.current = np.ones(64, np.uint32)
        self.output_pwm = np.zeros(64, np.uint32)
        self.output_current = np.ones(64, np.uint32)
        print self.pwm
        # init tablewidget
        newItemt = QtGui.QTableWidgetItem('0')
        self.tableWidget_PWM.setColumnCount(self.s_dict["led_x"])
        self.tableWidget_PWM_2.setColumnCount(self.s_dict["led_x"])
        self.tableWidget_Current.setColumnCount(self.s_dict["led_x"])
        self.tableWidget_Current_2.setColumnCount(self.s_dict["led_x"])
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
        self.connect(self.pushButton_plotout, QtCore.SIGNAL('clicked()'), self.CreateNewPlotDailog_1)
        self.connect(self.pushButton_plotin, QtCore.SIGNAL('clicked()'), self.CreateNewPlotDailog)
        # self.connect(self.pushButton_plot, QtCore.SIGNAL('clicked()'), self.CreateNewPlotDailog_2)
        self.actionQuit.connect(self.actionQuit, QtCore.SIGNAL('triggered()'), QtGui.qApp, QtCore.SLOT('quit()'))
        self.actionOpen_setting_file.connect(self.actionOpen_setting_file, QtCore.SIGNAL('triggered()'),
                                             self.loadSettingfromJson)
        self.actionSave_setting_file.connect(self.actionSave_setting_file, QtCore.SIGNAL('triggered()'),
                                             self.saveSettingfromJson)

        #self.loadSettingfromJson()
        self.PWMshowinTable()


    def paintEvent(self, envent):
        self.painter.begin(self)
        startposx = self.tableWidget_Paras.x()
        startposy = self.tableWidget_Paras.y() + self.tableWidget_Paras.height() + 60
        for i in range(4):
            for j in range(8):
                var = self.pwm[j * self.tableWidget_Current.columnCount() + i]
                br = (var & 0xFFF) >> 4
                color = QtGui.QColor(br, br, br)
                self.painter.setBrush(color)
                self.painter.drawRect(startposx + i * 80, startposy + j * 30, 80, 30)
        config_read = ConfigParser.RawConfigParser()
        config_read.read("ChipDebugger.INI")
        eth_ip = config_read.get("Connection", "Ethernet.IP")
        self.painter.end()

    def connectChip(self):
        config_read = ConfigParser.RawConfigParser()
        config_read.read("ChipDebugger.INI")
        eth_ip = config_read.get("Connection", "Ethernet.IP")
        self.connectFlag = TFC.TFCConnect2Chip()
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
        settingfile = "parameters_m50.json"
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
                TFC.tfc2ddWriteDword(0x6C, i * self.tableWidget_PWM.columnCount() + j)
                time.sleep(0.1)
                var = TFC.tfc2ddReadDword(0x68) >> 8;
                self.pwm[i * self.tableWidget_PWM.columnCount() + j] = var & 0xFFF
                pwmdutytemp = "%X" % (var & 0xFFF)
                newItemt = QtGui.QTableWidgetItem(pwmdutytemp)
                self.tableWidget_PWM.setItem(i, j, newItemt)
        self.pushButton_readpwm.setText("ReadPWM")
        # print self.pushButton_readpwm.text
        print self.pwm
        self.update()

    def PWMshowinTable(self):
        self.current =  self.current * self.s_dict["normal_current_mid"]
        for i in range(self.tableWidget_PWM.rowCount()):
            for j in range(self.tableWidget_PWM.columnCount()):
                pwmdutytemp = "%X" % (self.pwm[i * self.tableWidget_PWM.columnCount() + j])

                newItemt = QtGui.QTableWidgetItem(pwmdutytemp)
                self.tableWidget_PWM.setItem(i, j, newItemt)

                currenttablevar = "%X" % (self.current[i * self.tableWidget_PWM.columnCount() + j])

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
                var = self.output_current[i * self.tableWidget_Current.columnCount() + j]
                pwmdutytemp = "%X" % (var & 0xFF)
                newItemt = QtGui.QTableWidgetItem(pwmdutytemp)
                self.tableWidget_Current_2.setItem(i, j, newItemt)
                # print self.current

    def outputPWM(self):
        for i in range(self.tableWidget_PWM_2.rowCount()):
            for j in range(self.tableWidget_PWM_2.columnCount()):
                var = self.output_pwm[i * self.tableWidget_PWM_2.columnCount() + j]
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
        dc_mapping_3824_m65 = np.array(
            [0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1], np.uint32)
        # dc_mapping_3820_m70.shape = (8, 8)
        dc_mapping_3820_m50 = np.array(
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], np.uint32)
        for i in range(led_size):
            tmp_i = dc_mapping_3820_m50[i]
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
        peak_sum = 0
        # global_gain = 1024
        reduce_pwm = 100
        led_x = self.s_dict["led_x"]
        led_y = self.s_dict["led_y"]
        led_size = led_x * led_y
        print led_size, led_x, led_y
        dc_size = self.s_dict["dc_dc_size"]
        dc_max_sum = np.zeros((8, 5), np.uint32)
        reduce_pwm_coef = np.ones((8, 2), np.uint32)
        reduce_pwm_coef *= 100
        dc_peak_num = np.zeros(8, np.uint32)
        dc_init_current_list_m50_1 =  np.array(
            [72, 82, 92, 102, 112, 122, 132, 142, 152, 162, 172, 182, 192, 202, 212, 217], np.uint32)
        dc_init_current_list_m50_2 =  np.array(
            [72, 82, 92, 102, 112, 122, 132, 142, 152, 162, 172, 182, 192, 202, 212, 217], np.uint32)
        dc_pwm_hist = np.zeros((2, 16), np.uint32)

        dc_mapping_3820_m50 = np.array(
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], np.uint32)
        dc_mapping = dc_mapping_3820_m50
        for i in range(led_size):
            tmp_i = dc_mapping[i]
            if self.pwm[i] > self.s_dict["peak_value_thr"]:
                dc_peak_num[tmp_i] += 1
                peak_sum += 1
            dc_pwm_hist[tmp_i][self.pwm[i]/0x100] += self.pwm[i]
        print dc_pwm_hist
        dc_pwm_hist_temp_up = np.zeros((2, 16), np.uint32)
        dc_pwm_hist_temp_down = np.zeros((2, 16), np.uint32)
        for i in range(led_size/dc_size):
            for j in range(0,i,1):
                dc_pwm_hist_temp_up[0][i] += dc_pwm_hist[0][j]
                dc_pwm_hist_temp_up[1][i] += dc_pwm_hist[1][j]
            for j in range(i,led_size/dc_size,1):
                dc_pwm_hist_temp_down[0][i] += dc_pwm_hist[0][j]
                dc_pwm_hist_temp_down[1][i] += dc_pwm_hist[1][j]
        print dc_pwm_hist_temp_up
        print dc_pwm_hist_temp_down
        print "11111"
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
        print global_current_set,peak_sum,dc_peak_num
        dc_current_list_num = 15
        for i in range(15,-1,-1):
            if dc_init_current_list_m50_1[i] > global_current_set:
                dc_init_current_list_m50_1[i] = global_current_set
            if dc_init_current_list_m50_2[i] > global_current_set:
                dc_init_current_list_m50_2[i] = global_current_set
            else:
                dc_current_list_num = i
                break
            dc_current_list_num = 0
        print dc_current_list_num,dc_init_current_list_m50_1,dc_init_current_list_m50_2
        if dc_current_list_num == 0:
            self.current = np.ones(32, np.uint32)
            self.current = dc_init_current_list_m50_1[0]
        # self.current *= self.s_dict["normal_current_mid"]
        else:
            self.current = np.ones(32, np.uint32)
            self.current = self.current * (global_gain * self.s_dict["peak_current_max"]) / 100
        print self.current
        for i in range(led_size/dc_size):
            dc_sum_power_max_1 = dc_pwm_hist[0][i] * dc_init_current_list_m50_1[i]
            dc_sum_power_max_2 = dc_pwm_hist[1][i] * dc_init_current_list_m50_2[i]

        print dc_sum_power_max_1,dc_sum_power_max_2
        power_max = self.s_dict["power_max"] * self.s_dict["power_max_percent"] / 100
        print power_max
        dc_current_list_num_1 = dc_current_list_num-1
        dc_current_list_num_2 = dc_current_list_num-1
        steps = 10
        # while(power_max < dc_sum_power_max_1):
        #
        #     reduce_num_1 =
        for i in range(led_size):
            self.output_pwm[i] = self.pwm[i] * global_current_set  # scale the output brightness = pwm*current
        # print self.output_pwm
        for i in range(led_size):
            tmp_i = dc_mapping[i]
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
            tmp_i = dc_mapping[i]
            if self.pwm[i] > self.s_dict["peak_value_thr"]:
                reduce_pwm = reduce_pwm_coef[tmp_i][2]
                self.output_pwm[i] = self.pwm[i]
                self.output_current[i] = self.current[i] * reduce_pwm / 100
            elif self.pwm[i] > self.s_dict["medium_value_thr"]:
                reduce_pwm = reduce_pwm_coef[tmp_i][1]
                self.output_current[i] = self.current[i] * reduce_pwm / 100
                if self.output_current[i] < self.s_dict["lowest_current_min"]:
                    self.output_pwm[i] = self.pwm[i] * (2 * self.s_dict["lowest_current_min"] - self.output_current[i]) / self.s_dict["lowest_current_min"]
                    self.output_current[i] = self.s_dict["lowest_current_min"]
                    if self.output_pwm[i] > 0xFFF:
                        self.output_pwm[i] = 0xFFF
                else:
                    self.output_pwm[i] = self.pwm[i]
            elif self.pwm[i] > self.s_dict["low_value_thr"]:
                reduce_pwm = reduce_pwm_coef[tmp_i][0]
                if self.output_current[i] < self.s_dict["lowest_current_min"]:
                    self.output_pwm[i] = self.pwm[i] * (2 * self.s_dict["lowest_current_min"] - self.output_current[i]) / \
                                         self.s_dict["lowest_current_min"]
                    self.output_current[i] = self.s_dict["lowest_current_min"]
                    if self.output_pwm[i] > 0xFFF:
                        self.output_pwm[i] = 0xFFF
                else:
                    self.output_pwm[i] = self.pwm[i]
            else:
                self.output_current[i] = self.s_dict["lowest_current_min"]
                self.output_pwm[i] = 0xE * self.pwm[i]
                self.output_current[i] = self.current[i] * reduce_pwm / 100
                # self.output_pwm[i] = (self.output_pwm[i] * reduce_pwm) / 100
        print self.output_current
        self.outputPWM()
        self.outputCurrent()

    def Algo_3(self):
        peak_sum = 0
        # global_gain = 1024
        reduce_pwm = 100
        led_x = self.s_dict["led_x"]
        led_y = self.s_dict["led_y"]
        led_size = led_x * led_y
        print led_size,led_x,led_y
        dc_size = self.s_dict["dc_dc_size"]
        dc_max_sum = np.zeros((8, 5), np.uint32)
        reduce_pwm_coef = np.ones((8, 3), np.uint32)
        reduce_pwm_coef *= 100
        dc_peak_num = np.zeros(8, np.uint32)
        reduce_pwm_sum = 0
        dc_mapping_3820_m50 = np.array(
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], np.uint32)
        dc_mapping = dc_mapping_3820_m50
        for i in range(led_size):
            tmp_i = dc_mapping[i]
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
        global_current_set = (global_gain * self.s_dict["peak_current_max"] ) / 100

        #self.current *= self.s_dict["normal_current_mid"]
        self.current = np.ones(32, np.uint32)
        # self.current =  self.current * (global_gain * self.s_dict["peak_current_max"] ) / 100
        self.current = self.current*self.s_dict["peak_current_max"]
        print self.current
        for i in range(led_size):
            self.output_pwm[i] = self.pwm[i]
        # print self.output_pwm
        for i in range(led_size):
            tmp_i = dc_mapping[i]
            if self.output_pwm[i] > self.s_dict["peak_value_thr"] :
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
            power_max_dc = dc_max_sum[i][4] * self.s_dict["peak_current_max"]
            if power_max_dc > power_max:

                reduce_pwm_sum = power_max_dc - power_max
                print  power_max_dc,reduce_pwm_sum,power_max
                reduce_pwm_coef[i][1] = self.s_dict["limit_cof"]
                reduce_pwm_coef[i][2] = 100-(reduce_pwm_sum * 100 / power_max_dc)
        if reduce_pwm_coef[0][2] > reduce_pwm_coef[1][2]:
            reduce_pwm_coef[0][2] = reduce_pwm_coef[1][2]
        else:
            reduce_pwm_coef[0][2] = reduce_pwm_coef[1][2]
        print reduce_pwm_coef
        print self.output_pwm

        power_max_total_set = 0xFFF*self.s_dict["normal_current_mid"]*32
        power_max_total = 0
        for i in range(led_size):
            tmp_i = dc_mapping[i]
            if self.pwm[i] > self.s_dict["low_value_thr"]:
                reduce_pwm = reduce_pwm_coef[tmp_i][2]
                self.output_current[i] = self.current[i] * reduce_pwm / 100
                self.output_pwm[i] = self.pwm[i]
            else:
                self.output_current[i] = self.s_dict["lowest_current_min"]
                self.output_pwm[i] = self.pwm[i]
                # self.output_current[i] = self.current[i] * reduce_pwm / 100
            power_max_total += self.output_pwm[i] *  self.output_current[i]
        if power_max_total > power_max_total_set:
            print power_max_total,power_max_total_set
            reduce_pwm_total = power_max_total - power_max_total_set
            reduce_pwm_coef_total = 100-  reduce_pwm_total*100/power_max_total
            print reduce_pwm_coef_total
            for i in range(led_size):
                self.output_pwm[i] = reduce_pwm_coef_total * self.output_pwm[i] / 100
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
        ax.set_zlabel('Brightness')
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


class MyMplCanvas(FigureCanvas):
    """Ultimately, this is a QWidget (as well as a FigureCanvasAgg, etc.)."""

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = self.fig.add_subplot(111)
        # We want the axes cleared every time plot() is called
        self.axes.hold(False)

        self.compute_initial_figure()

        FigureCanvas.__init__(self, self.fig)
        self.setParent(parent)

        FigureCanvas.setSizePolicy(self,
                                   QtGui.QSizePolicy.Expanding,
                                   QtGui.QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)

    def sizeHint(self):
        w, h = self.get_width_height()
        return QtCore.QSize(w, h)

    def minimumSizeHint(self):
        return QtCore.QSize(10, 10)


class MyStaticMplCanvas(MyMplCanvas):
    """Simple canvas with a sine plot."""

    def compute_initial_figure(self):
        t = np.arange(0.0, 3.0, 0.01)
        s = np.sin(2 * np.pi * t)
        self.axes.plot(t, s)


class MyPlotDialog(QtGui.QDialog):
    def __init__(self):
        super(MyPlotDialog, self).__init__()
        uic.loadUi("plot_it.ui", self)
        self.setWindowIcon(QtGui.QIcon("222.ico"))
        self.main_widget = QtGui.QWidget(self)

        l = QtGui.QVBoxLayout(self.main_widget)
        sc = MyStaticMplCanvas(self.main_widget, width=5, height=4, dpi=100)
        l.addWidget(sc)
        self.main_widget.setFocus()
        # self.setCentralWidget(self.main_widget)

    def closeEvent(self, event):
        reply = QtGui.QMessageBox.question(self, 'Message', "Are you sure to quit?", QtGui.QMessageBox.Yes,
                                           QtGui.QMessageBox.No)
        if reply == QtGui.QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()


if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    mywindow = MyWindow()
    mywindow.show()
    sys.exit(app.exec_())
