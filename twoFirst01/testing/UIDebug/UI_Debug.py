
# -*- coding: utf-8 -*-
# import math, random, time
# import ctypes as C
import sys
import two01 as TFC
# import xmltodict
# import numpy as np
from dispmipsfunc import *
from PyQt4 import QtCore, QtGui, uic  # ,Qwt5
from UI_Debug_res import *
import json
import csv

nameList = ["pic_mode", "AutoBrightness", "MpegNR", "NR", "GameMode", "MovieMode", "BlackExtention",
                        "DCI", "LocalDimming", "ClearAction", "ColorTemp", "gammaFactor"]

class UIDebugWindow(QtGui.QMainWindow):

    def __init__(self):
        super(UIDebugWindow, self).__init__()
        self.ui = Ui_Form_UIDebug()
        self.ui.setupUi(self)

        self.connectFlag = False
        self.debugRegs = {}

        settingfile = "UI_Debug_parameters.json"
        s_fp = open(settingfile, 'r')
        if s_fp == False:
            # print "error file!!!!"
            self.readJson = False
        else:
            self.s_setjson = json.load(s_fp)
            s_fp.close()
            self.ui_debug_info = self.s_setjson["UI_Debug_info"]
            self.initWidgets()
            if self.s_setjson.has_key("SWPages"):
                if self.s_setjson["SWPages"].has_key("csvFile"):
                    self.filename = self.s_setjson["SWPages"]["csvFile"]
                else:
                    QtGui.QMessageBox.information(self, "warning",
                                                  ("no 'csvFile' info in 'SWPages' of file: %s" % (settingfile)))
                    return
            else:
                QtGui.QMessageBox.information(self, "warning",
                                              ('''No SWPages info in file '%s', please add below info in the file.
                                               \n"SWPages":{\n         "csvFile":"filename.csv"\n}''' % (settingfile)))
                return

            self.readJsonFlag = self.loadDebugRegsAddr()


        self.connect(self.ui.pushButton_read, QtCore.SIGNAL('clicked()'), self.read)
        self.connect(self.ui.pushButton_read, QtCore.SIGNAL('pressed()'), self.changeText_Read)
        self.connect(self.ui.pushButton_write, QtCore.SIGNAL('clicked()'), self.write)
        self.connect(self.ui.pushButton_write, QtCore.SIGNAL('pressed()'), self.changeText_Write)


    def setConnectFlag(self, flag):
        self.connectFlag = flag

    def loadDebugRegsAddr(self):
        regName = self.ui_debug_info["version_info"]["regName"]
        self.debugRegs[regName] = 0

        regName = self.ui_debug_info["debug_control"]["regName"]
        self.debugRegs[regName] = 0
        regName = self.ui_debug_info["debug_control"]["LowLevelCtlReg"][0]
        self.debugRegs[regName] = 0
        regName = self.ui_debug_info["debug_control"]["LowLevelCtlReg"][1]
        self.debugRegs[regName] = 0

        regs = self.ui_debug_info["debug_regs"]
        for i in range(len(regs)):
            regName = regs[i]["regName"]
            self.debugRegs[regName] = 0

        if self.loadSWRegFromFile(self.filename, self.debugRegs) is False:
            return False

        for key in self.debugRegs:
            if self.debugRegs[key] is 0:
                QtGui.QMessageBox.information(self, "warning",
                                              ("Haven't found reg %s in csv file!!!!" % (key)))
                return False
        return True

    def loadSWRegFromFile(self, file, debugRegs):
        try:
            if file.endswith('.csv') is False:
                QtGui.QMessageBox.information(self, "warning", ("%s is not csv file!!!\nPlease input csv file!!!" %(file)))
                return False
            with open(file, "r") as csvFile:
                reader = csv.reader(csvFile)
                for item in reader:
                    if reader.line_num == 1:
                        header = {'Address':'', 'Register Name':''}
                        if False == set(header.keys()).issubset(item):
                            return False
                        for i in range(len(item)):
                            for key in header:
                                if key == item[i]: header[key] = i
                    else:
                        regname = str(item[header['Register Name']].replace(' ', ''))
                        regaddr = int(item[header['Address']].replace('_', ''), 16)
                        if regname in debugRegs:
                            debugRegs[regname] = regaddr
                            continue
                # self.initFlag = True
        except IOError as e:
            QtGui.QMessageBox.information(self, "warning", ('%s' % (e)))
        except csv.Error as e:
            QtGui.QMessageBox.information(self, "warning", ('file %s: %s' % (file, e)))
        return True

    def initWidgets(self):
        DebugInfo = self.ui_debug_info["Debug_info"]
        for i in range(len(DebugInfo)):
            if "ct_r_hue" == DebugInfo[i]["name"]:
                self.ct_start = i
            elif "ct_y_bri" == DebugInfo[i]["name"]:
                self.ct_end = i
            elif "wb_r_gain" == DebugInfo[i]["name"]:
                self.wb_start = i
            elif "wb_b_offset" == DebugInfo[i]["name"]:
                self.wb_end = i
        for i in range(len(DebugInfo)):
            if (self.ct_start <= i and self.ct_end >= i) or (self.wb_start <= i and self.wb_end >= i):
                continue
            Name = DebugInfo[i]["name"]
            if Name in nameList:
                CBName = "comboBox_" + Name
                FindCB = self.findChild((QtGui.QComboBox,), CBName)
                if DebugInfo[i].has_key("content") and FindCB != None:
                    content = DebugInfo[i]["content"]
                    FindCB.addItems(content)
            elif Name == "customMEMC":
                print "customMEMC"
                if DebugInfo[i].has_key("content"):
                    content = DebugInfo[i]["content"]
                    print content
                    self.ui.comboBox_Judder.addItems(content)
                    self.ui.comboBox_Blur.addItems(content)
                # CBName = "checkBox_" + Name
                # FindCB = self.findChild((QtGui.QCheckBox,), CBName)
                # if FindCB != None:
                #     # FindCB.setChecked(False)
                #     print CBName, FindCB.isChecked()
                #     print CBName, FindCB.checkStateSet()
        # FindLE = self.findChild((QtGui.QLineEdit,), LEName)
        # FindLE.setText(LEName)
        # FindLE = self.findChild((QtGui.QCheckBox,), LEName)
        # FindLE.setChecked(True)
        # i = 6
        # if i < len(self.ui_debug_info["Debug_info"][0]["content"]):
        #     FindCB.setCurrentIndex(i)
        # else:
        #     text = "%d:unknow" %i
        #     FindCB.insertItem(6, text)
        #     FindCB.setCurrentIndex(6)
        # print FindCB.currentText()
        # print FindCB.lineEdit()

        # self.MappingVersionLocal = self.ui_debug_info["version_info"]["VersionNo"]

    def getRegAddr(self, regName):
        return self.debugRegs[regName]

    def changeText_Read(self):
        if self.connectFlag is False:
            pass
        else:
            self.ui.pushButton_read.setText("Reading")

    def updateComboBox(self, CB, contentLen, invalue):
        comboBoxCount = CB.count()
        if invalue < contentLen:
            CB.setCurrentIndex(invalue)
        elif comboBoxCount > contentLen:
            text = "%d:unknow" % invalue
            CB.setItemText(comboBoxCount - 1, text)
            CB.setCurrentIndex(comboBoxCount - 1)
        else:
            text = "%d:unknow" % invalue
            CB.insertItem(contentLen, text)
            CB.setCurrentIndex(contentLen)

    def read(self):
        if self.readJsonFlag is False:
            QtGui.QMessageBox.information(self, "warning", ("need input valid json file and csv file!!!\n"))
            return
        elif self.connectFlag is False:
            QtGui.QMessageBox.information(self, "warning", ("Please connect to chip first!!!\n Setting->Connect"))
            return
        DebugInfo = self.ui_debug_info["Debug_info"]
        for i in range(len(DebugInfo)):
            regNo = int(DebugInfo[i]["debug_reg"])
            # regAddr = int(self.ui_debug_info["debug_regs"][regNo]["address"], 16)
            regName = self.ui_debug_info["debug_regs"][regNo]["regName"]
            regAddr = self.getRegAddr(regName)
            regMask = int(DebugInfo[i]["mask"], 16)
            valueShift = int(DebugInfo[i]["shift"])
            value = ((TFC.tfcReadDword(regAddr, 0)) & regMask) >> valueShift
            if (self.ct_start <= i and self.ct_end >= i):
                col = int((i - self.ct_start) / 3)
                row = (i - self.ct_start) % 3
                if value & 0x8000 == 0x8000:
                    text = "%d" % (value - 0x10000)
                else:
                    text = "%d" % value
                ctitem = self.ui.tableWidget_color_tuner.item(row, col)
                ctitem.setText(text)
                continue
            elif (self.wb_start <= i and self.wb_end >= i):
                col = (i - self.wb_start) % 3
                row = 1 - int((i - self.wb_start) / 3)
                if value & 0x8000 == 0x8000:
                    text = "%d" % (value - 0x10000)
                else:
                    text = "%d" % value
                ctitem = self.ui.tableWidget_wb.item(row, col)
                ctitem.setText(text)
                continue
            Name = DebugInfo[i]["name"]
            if Name in nameList:
                CBName = "comboBox_" + Name
                FindCB = self.findChild((QtGui.QComboBox,), CBName)
                if DebugInfo[i].has_key("content") and FindCB != None:
                    contentLen = len(DebugInfo[i]["content"])
                    self.updateComboBox(FindCB, contentLen, value)
            elif Name == "customMEMC":
                judderLevel = (value >> 8) & 0xff
                blurLevel = (value >> 16) & 0xff
                contentLen = len(DebugInfo[i]["content"])
                self.updateComboBox(self.ui.comboBox_Judder, contentLen, judderLevel)
                self.updateComboBox(self.ui.comboBox_Blur, contentLen, blurLevel)
            else:
                LEName = "lineEdit_" + Name
                FindLE = self.findChild((QtGui.QLineEdit,), LEName)
                if FindLE != None:
                    if Name == "hue" and value & 0x8000 == 0x8000:
                        text = "%d" %(value - 0x10000)
                    else:
                        text = "%d" %value
                    FindLE.setText(text)
        self.ui.pushButton_read.setText("Read")

    def changeText_Write(self):
        if self.connectFlag is False:
            pass
        else:
            self.ui.pushButton_write.setText("Writing")

    def write(self):
        if self.readJsonFlag is False:
            QtGui.QMessageBox.information(self, "warning", ("need input valid json file and csv file!!!\n"))
            return
        elif self.connectFlag is False:
            QtGui.QMessageBox.information(self, "warning", ("Please connect to chip first!!!\n Setting->Connect"))
            return
        DebugInfo = self.ui_debug_info["Debug_info"]
        DebugCtl = self.ui_debug_info["debug_control"]
        LowLevelRegVal0 = 0
        LowLevelRegVal1 = 0
        count = 0
        for i in range(len(DebugInfo)):
            Name = DebugInfo[i]["name"]
            if (self.ct_start <= i and self.ct_end >= i):
                col = int((i - self.ct_start) / 3)
                row = (i - self.ct_start) % 3
                item = self.ui.tableWidget_color_tuner.item(row, col)
                if item.checkState() == 0:
                    continue
                text = item.text()
                if text == "":
                    QtGui.QMessageBox.information(self, "warning", ('Please input value for ' + Name + " !!!!"))
                    break
                value = int(text)
                if DebugInfo[i].has_key("range"):
                    range0 = DebugInfo[self.ct_start]["range"]
                    if value < range0[0] or value > range0[1]:
                        msg = "%s range: %d~%d. need input valid value! " % (Name, range0[0], range0[1])
                        QtGui.QMessageBox.information(self, "warning", msg)
                        self.ui.pushButton_write.setText("Write")
                        return
            elif (self.wb_start <= i and self.wb_end >= i):
                col = (i - self.wb_start) % 3
                row = 1 - int((i - self.wb_start) / 3)
                item = self.ui.tableWidget_wb.item(row, col)
                if item.checkState() == 0:
                    continue
                text = item.text()
                if text == "":
                    QtGui.QMessageBox.information(self, "warning", ('Please input value for ' + Name + " !!!!"))
                    break
                value = int(text)
                if DebugInfo[i].has_key("range"):
                    range0 = DebugInfo[self.wb_start]["range"]
                    if value < range0[0] or value > range0[1]:
                        msg = "%s range: %d~%d. need input valid value! " % (Name, range0[0], range0[1])
                        QtGui.QMessageBox.information(self, "warning", msg)
                        self.ui.pushButton_write.setText("Write")
                        return
            elif Name == "customMEMC":
                if self.ui.checkBox_Blur.isChecked() is False and self.ui.checkBox_Judder.isChecked() is False:
                    continue
                regNo = int(DebugInfo[i]["debug_reg"])
                # regAddr = int(self.ui_debug_info["debug_regs"][regNo]["address"], 16)
                regName = self.ui_debug_info["debug_regs"][regNo]["regName"]
                regAddr = self.getRegAddr(regName)
                regMask = int(DebugInfo[i]["mask"], 16)
                valueShift = int(DebugInfo[i]["shift"])
                valueReg = ((TFC.tfcReadDword(regAddr, 0)) & regMask) >> valueShift
                if self.ui.checkBox_Judder.isChecked() is True:
                    judderLevel = self.ui.comboBox_Judder.currentIndex()
                    value = (valueReg & 0xffff0000) | ((judderLevel & 0xff) << 8) | 0x4
                if self.ui.checkBox_Blur.isChecked() is True:
                    blurLevel = self.ui.comboBox_Blur.currentIndex()
                    value = (valueReg & 0xff00ff00) | ((blurLevel & 0xff) << 16) | 0x4
            else:
                CheckBoxName = "checkBox_" + Name
                FindCheckBox = self.findChild((QtGui.QCheckBox,), CheckBoxName)
                if FindCheckBox == None or FindCheckBox.isChecked() is False:
                    continue
                if Name in nameList:
                    CBName = "comboBox_" + Name
                    FindCB = self.findChild((QtGui.QComboBox,), CBName)
                    if FindCB == None:
                        continue
                    value = FindCB.currentIndex()
                else:
                    LEName = "lineEdit_" + Name
                    FindLE = self.findChild((QtGui.QLineEdit,), LEName)
                    if FindLE == None:
                        continue
                    elif FindLE.text() == "":
                        QtGui.QMessageBox.information(self, "warning", ('Please input value for ' + Name + " !!!!"))
                        break
                    value = int(FindLE.text())
                    if DebugInfo[i].has_key("range"):
                        range0 = DebugInfo[i]["range"]
                        if value < range0[0] or value > range0[1]:
                            msg = "%s range: %d~%d. need input valid value! " % (Name, range0[0], range0[1])
                            QtGui.QMessageBox.information(self, "warning", msg)
                            self.ui.pushButton_write.setText("Write")
                            return
            # print Name, value
            regNo = int(DebugInfo[i]["debug_reg"])
            # regAddr = int(self.ui_debug_info["debug_regs"][regNo]["address"], 16)
            regName = self.ui_debug_info["debug_regs"][regNo]["regName"]
            regAddr = self.getRegAddr(regName)
            regMask = int(DebugInfo[i]["mask"], 16)
            valueShift = int(DebugInfo[i]["shift"])
            valueReg = (value << valueShift) & regMask
            # print "0x%x" %valueReg
            TFC.tfcWriteDwordMask(regAddr, 0, regMask, valueReg)
            if i < 32:
                LowLevelRegVal0 = LowLevelRegVal0 | (1<<i)
            elif i < 64:
                LowLevelRegVal1 = LowLevelRegVal1 | (1<<(i-32))
            count = count + 1
        if count > 0:
            # LowLevelReg0 = int(DebugCtl["LowLevelCtlReg"][0], 16)
            # LowLevelReg1 = int(DebugCtl["LowLevelCtlReg"][1], 16)
            regName = DebugCtl["LowLevelCtlReg"][0]
            LowLevelReg0 = self.getRegAddr(regName)
            regName = DebugCtl["LowLevelCtlReg"][1]
            LowLevelReg1 = self.getRegAddr(regName)
            TFC.tfcWriteDword(LowLevelReg0, 0, LowLevelRegVal0)
            TFC.tfcWriteDword(LowLevelReg1, 0, LowLevelRegVal1)
            # regAddr = int(DebugCtl["address"], 16)
            regName = DebugCtl["regName"]
            regAddr = self.getRegAddr(regName)
            regMask = int(DebugCtl["mask"], 16)
            regVal = int(DebugCtl["value"], 16)
            TFC.tfcWriteDwordMask(regAddr, 0, regMask, regVal)
            # print "========="
            # print LowLevelReg0, LowLevelRegVal0
            # print LowLevelReg1, LowLevelRegVal1
            # print regAddr, regMask, regVal
        self.ui.pushButton_write.setText("Write")





if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    mywindow = UIDebugWindow()
    mywindow.show()
    sys.exit(app.exec_())