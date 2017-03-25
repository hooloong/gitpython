__author__ = 'hooloongge'
# -*- coding: utf-8 -*-
import sys, math, random, time
import ctypes as C
import two01 as TFC

import numpy as np
from dispmipsfunc import *
from PyQt4 import QtCore, QtGui, uic  # ,Qwt5
from TestPattern_res import *

proper_digit="0123456789ABCDEFabcdef"
low_digit="abcdef"
TOTAL_PATS_LIMIT = 100
MANUAL_TESTING_PATS_ADDR = 0x91834B40
class TestPatternWindow(QtGui.QMainWindow):

    def __init__(self):
        super(TestPatternWindow, self).__init__()
        self.ui = Ui_Form_TestPattern()
        self.ui.setupUi(self)
        self.connectFlag = False
        self.initFlag = False
        self.edit_status = {"TEMP":0}
        self.current_edit_frame = self.edit_status["TEMP"]
        self.regs_mapping_addr =[ 0x19A005DC,0xFF000000,24]
        self.regs_boostype_addr = [0x19A005B8, 0x3, 0]
        self.testing_pat_en_addr = [0x19A005C0, 0xC, 2]
        self.testing_pat_ctrl_addr = [0x19A005F8, 0xFFFFFFFF, 0]
        self.manual_testpat_addr = [0x19A004D0,0xFFFFFFF,0]
        self.manual_buff_addr = MANUAL_TESTING_PATS_ADDR
        self.panel_info = {}
        self.debugregisters= {u"mapping_id":22,u"boosting_type":2,u"testing_pat_en":1,u"led_x":4,u"led_y":8}

        self.curpat= np.zeros(64, np.uint32)
        self.curtmpppat = np.zeros(64,np.uint32)
        self.storepats = np.zeros(64,np.uint32)
        self.pat_size = 64
        for i in range(64):
            self.curpat[i] = random.randrange(100, 4095)

        self.connect(self.ui.pushButton_readpanel, QtCore.SIGNAL('clicked()'), self.getpanelinfofromchip)
        self.ui.tableWidget_pattern.itemChanged.connect(self.updatepatts)
        # self.ui.tableWidget_pattern.cellChanged.connect(self.updatepatts_1)
        self.connect(self.ui.pushButton_sendpattochip, QtCore.SIGNAL('pressed()'), self.changeText_sending)
        self.connect(self.ui.pushButton_sendpattochip, QtCore.SIGNAL('clicked()'), self.sendpats)


        self.wi_row = 255
        self.wi_col = 255
        self.DataShowiInTable()

    def paintEvent(self, envent):
        if self.current_edit_frame == 0:
            self.ui.lineEdit_index.setText("TEMP")
        else:
            self.ui.lineEdit_index.setText("%d" % self.current_edit_frame)

    def changeText_sending(self):
        if self.connectFlag is True:
            self.ui.pushButton_sendpattochip.setText("Sending")

    def sendpats(self):
        for i in range(self.pat_size+6):
            tmps = "%X" % self.curtmpppat[i]
            print tmps
        pass

    def isproperdigit(self,strinput):
        if len(strinput) == 0 or len(strinput) >3:
            return  False
        for c in strinput:
            if c not in proper_digit:
                return False
        return True
    def islowerdigit(self,strinput):
        for c in strinput:
            if c in low_digit:
                return True
        return False
    def headpartupdate(self):
        """
        generate the 6 uint16 head part
        0:
        1: magic number: 0x31323334
        2: total pats
        3: current index
        4:
        5: delay time uint32
        :return:
        """
        if self.current_edit_frame == 0:
            self.curtmpppat[0] = 0x3132
            self.curtmpppat[1] = 0x3334
            self.curtmpppat[2] = 1
            self.curtmpppat[3] = 1
            self.curtmpppat[4] = 0xFFFF
            self.curtmpppat[5] = 0xFFFF
            return
        else:
            self.curtmpppat[(6 + self.pat_size) * self.current_edit_frame + 0] = 0x3132
            self.curtmpppat[(6 + self.pat_size) * self.current_edit_frame + 1] = 0x3334
            self.curtmpppat[(6 + self.pat_size) * self.current_edit_frame + 2] = self.current_edit_frame
            self.curtmpppat[(6 + self.pat_size) * self.current_edit_frame + 3] = self.current_edit_frame
            self.patdelaytime = self.ui.spinBox_patdelays.value() * 60
            self.curtmpppat[(6 + self.pat_size) * self.current_edit_frame + 4] = self.patdelaytime & 0xFFFF
            self.curtmpppat[(6 + self.pat_size) * self.current_edit_frame + 5] = (self.patdelaytime >> 16) & 0xFFFF
            return


    def updatepatts(self,item):
        if not self.initFlag: return
        # if self.wi_col != item.column() or self.wi_row !=  item.row():
        #     return
        if item != self.ui.tableWidget_pattern.currentItem():
            return
        print item.text()
        # print item.row(),item.column()
        stringitem = "%s" % item.text()
        isright = self.isproperdigit(stringitem)
        i = item.row()
        j = item.column()
        if isright is True:
            self.curpat[item.row()* self.debugregisters[u"led_x"] + item.column()] = int(stringitem,16)

        if self.islowerdigit(stringitem) is True or isright is False:
            # newItemt = QtGui.QTableWidgetItem(QtCore.QString("%1").arg(self.curpat[i * \
            #                      self.ui.tableWidget_pattern.columnCount() + j],
            #                             3, 16, QtCore.QChar(" ")).toUpper())
            # newItemt.setTextAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
            # self.ui.tableWidget_pattern.setItem(i, j, newItemt)
            self.ui.tableWidget_pattern.currentItem().setText(QtCore.QString("%1").arg(self.curpat[i * \
                                 self.ui.tableWidget_pattern.columnCount() + j],
                                        3, 16, QtCore.QChar(" ")).toUpper())
        for i in range(self.pat_size):
            # self.headpartupdate()
            self.curtmpppat[(self.pat_size)*self.current_edit_frame +6+i] = self.curpat[i]
        # print stringitem
        # self.DataShowiInTable()
        # self.update()
    def updatepatts_1(self,i,j):
        if not self.initFlag: return
        # if self.wi_col == j and self.wi_row == i: return
        self.wi_col = j
        self.wi_row = i
        item = self.ui.tableWidget_pattern.currentItem()
        print item.text(),i,j
        stringitem = "%s" % item.text()
        isright = self.isproperdigit(stringitem)
        if isright is True:
            self.curpat[item.row()* self.debugregisters[u"led_x"] + item.column()] = int(stringitem,16)
        else:
            newItemt = QtGui.QTableWidgetItem(QtCore.QString("%1").arg(self.curpat[i * \
                                 self.ui.tableWidget_pattern.columnCount() + j],
                                        3, 16, QtCore.QChar(" ")).toUpper())
            newItemt.setTextAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
            self.ui.tableWidget_pattern.setItem(i, j, newItemt)

        for i in range(self.pat_size):
            # self.headpartupdate()
            self.curtmpppat[(6+self.pat_size)*self.current_edit_frame +6+i] = self.curpat[i]

    def setConnectFlag(self, flag):
        self.connectFlag = flag
        # print flag
        # for tesing ,force to TRUE
        self.connectFlag = True

    def setSettingDict(self, panel):
        self.panel_info = panel
        # print self.panel_info

        for regs in  self.panel_info["registers"]:
            if regs["name"] == "mapping_id":
                self.regs_mapping_addr[0] = int(regs["address"],16)
                self.regs_mapping_addr[1] = self.generateMask(regs["bit_start"],regs["bit_end"])
                self.regs_mapping_addr[2] = regs["bit_start"]
            if regs["name"] == "boosting_type":
                self.regs_boostype_addr[0] = int(regs["address"],16)
                self.regs_boostype_addr[1] = self.generateMask(regs["bit_start"],regs["bit_end"])
                self.regs_boostype_addr[2] = regs["bit_start"]
            if regs["name"] == "testing_pat_en":
                self.testing_pat_en_addr[0] = int(regs["address"],16)
                self.testing_pat_en_addr[1] = self.generateMask(regs["bit_start"],regs["bit_end"])
                self.testing_pat_en_addr[2] = regs["bit_start"]
            if regs["name"] == "testing_pat_ctrl":
                self.testing_pat_ctrl_addr[0] = int(regs["address"],16)
                self.testing_pat_ctrl_addr[1] = self.generateMask(regs["bit_start"],regs["bit_end"])
                self.testing_pat_ctrl_addr[2] = regs["bit_start"]
            if regs["name"] == "manual_pats_addr":
                self.manual_testpat_addr[0] = int(regs["address"],16)
                self.manual_testpat_addr[1] = self.generateMask(regs["bit_start"],regs["bit_end"])
                self.manual_testpat_addr[2] = regs["bit_start"]

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

    def getpanelinfofromchip(self):
        if self.connectFlag is False:
            QtGui.QMessageBox.information(self, "warning", ("Please connect to chip first!!!\n Setting->Connect"))
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
        self.reStruTable()
        self.DataShowiInTable()
        self.initFlag = True
        self.headpartupdate()
        pass
    def reStruTable(self):
        self.ui.tableWidget_pattern.clear()
        self.ui.tableWidget_pattern.setRowCount(self.debugregisters[u"led_y"])
        self.ui.tableWidget_pattern.setColumnCount(self.debugregisters[u"led_x"])

        pass
    def DataShowiInTable(self):
        # testing patt
        for i in range(self.ui.tableWidget_pattern.rowCount()):
            for j in range(self.ui.tableWidget_pattern.columnCount()):
                # pwmdutytemp = "%X" % (self.curpat[i * self.ui.tableWidget_pattern.columnCount() + j])
                newItemt = QtGui.QTableWidgetItem(QtCore.QString("%1").arg(self.curpat[i * \
                self.ui.tableWidget_pattern.columnCount() + j],3,16,QtCore.QChar(" ")).toUpper())
                newItemt.setTextAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
                self.ui.tableWidget_pattern.setItem(i, j, newItemt)

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    mywindow = TestPatternWindow()
    mywindow.show()
    sys.exit(app.exec_())
