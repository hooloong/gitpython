__author__ = 'hooloongge'
# -*- coding: utf-8 -*-
import sys, math, random, time
import ctypes as C
import two01 as TFC

import numpy as np
from dispmipsfunc import *
from PyQt4 import QtCore, QtGui, uic  # ,Qwt5
from TestPattern_res import *


class TestPatternWindow(QtGui.QMainWindow):

    def __init__(self):
        super(TestPatternWindow, self).__init__()
        self.ui = Ui_Form_TestPattern()
        self.ui.setupUi(self)
        self.connectFlag = False
        self.initFlag = False
        self.regs_mapping_addr =[ 0x19A005DC,0xFF000000,24]
        self.regs_boostype_addr = [0x19A005B8, 0x3, 0]
        self.testing_pat_en_addr = [0x19A005C0, 0xC, 2]
        self.testing_pat_ctrl_addr = [0x19A005F8, 0xFFFFFFFF, 0]
        self.panel_info = {}
        self.debugregisters= {u"mapping_id":22,u"boosting_type":2,u"testing_pat_en":1,u"led_x":4,u"led_y":8}

        self.curpat= np.zeros(64, np.uint32)
        self.pat_size = 64
        for i in range(64):
            self.curpat[i] = random.randrange(100, 4095)
        self.connect(self.ui.pushButton_readpanel, QtCore.SIGNAL('clicked()'), self.getpanelinfofromchip)
        self.ui.tableWidget_pattern.itemChanged.connect(self.updatepatts)
        self.DataShowiInTable()

    def updatepatts(self,item):
        if not self.initFlag: return
        if item != self.ui.tableWidget_pattern.currentItem():
            return
        print item.row(),item.column()
        # self.parameters_vars[item.row()] = int(item.text())
        # self.s_dict[self.parameters_name[item.row()]] = self.parameters_vars[item.row()]
        # print self.s_dict[self.parameters_name[item.row()]]
    def setConnectFlag(self, flag):
        self.connectFlag = flag
        print flag

    def setSettingDict(self, panel):
        self.panel_info = panel
        print self.panel_info

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
    def generateMask(self,a,b):
        if(a > 31 or b> 31):
            return 0xFFFFFFFF
        if a <0 or b < 0 :
            return 0x0
        ret = 0
        for i in range(a,b+1):
            ret |= 1<<i
        print hex(ret)
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
        print self.debugregisters["mapping_id"],self.debugregisters["boosting_type"]
        temps = ""
        for ledtype in self.panel_info["led_output"]:
            print ledtype
            if ledtype[u"mapping_id"] == self.debugregisters["mapping_id"]:
                temps = temps+ ledtype["name"]
                print ledtype["name"]
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
        self.reStruTable()
        self.DataShowiInTable()
        self.initFlag = True
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
