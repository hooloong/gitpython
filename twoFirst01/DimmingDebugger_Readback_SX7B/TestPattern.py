__author__ = 'hooloongge'
# -*- coding: utf-8 -*-
import sys, math, random, time
import ctypes as C
import two01 as TFC

import numpy as np
from dispmipsfunc import *
from PyQt4 import QtCore, QtGui, uic  # ,Qwt5
from TestPattern_res import *

# proper_digit="0123456789ABCDEFabcdef"
# low_digit="abcdef"
TOTAL_PATS_LIMIT = 200
MANUAL_TESTING_PATS_ADDR = 0x91834B40

class TestPatternWindow(QtGui.QMainWindow):

    def __init__(self):
        super(TestPatternWindow, self).__init__()
        self.ui = Ui_Form_TestPattern()
        self.ui.setupUi(self)
        self.connectFlag = False
        self.initFlag = False
        self.test_pat_en = False
        self.edit_status = {"TEMP":0}
        self.current_edit_frame = self.edit_status["TEMP"]
        self.total_manual_pat = 0
        self.regs_mapping_addr =[ 0x19A005DC,0xFF000000,24]
        self.regs_boostype_addr = [0x19A005B8, 0x3, 0]
        self.testing_pat_en_addr = [0x19A005C0, 0x30, 4]
        self.testing_pat_ctrl_addr = [0x19A005F8, 0xFFFFFFFF, 0]
        self.manual_testpat_addr = [0x19A004D0,0xFFFFFFF,0]
        self.manual_panel_bls = [0x19080004, 0xFFFFFFF, 0]
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
        self.connect(self.ui.pushButton_disable, QtCore.SIGNAL('clicked()'), self.disablemanualpats)
        self.connect(self.ui.pushButton_enable, QtCore.SIGNAL('clicked()'), self.enablemanualpats)
        self.connect(self.ui.pushButton_addpattern, QtCore.SIGNAL('clicked()'), self.addonepat)
        self.connect(self.ui.pushButton_delpat, QtCore.SIGNAL('clicked()'), self.dellastonepat)
        self.connect(self.ui.spinBox_patdelays, QtCore.SIGNAL('valueChanged(int)'), self.patdelaytimechange)
        self.connect(self.ui.pushButton_printallpats, QtCore.SIGNAL('clicked()'), self.printoutallpats)
        self.connect(self.ui.pushButton_savepatToFile, QtCore.SIGNAL('clicked()'), self.savetofile)
        self.connect(self.ui.pushButton_loadpatfromFile, QtCore.SIGNAL('clicked()'), self.loadfromfile)
        self.connect(self.ui.checkBox_bls, QtCore.SIGNAL('clicked()'), self.setbluescreen)
        self.connect(self.ui.pushButton_prev, QtCore.SIGNAL('clicked()'), self.prevpat)
        self.connect(self.ui.pushButton_next, QtCore.SIGNAL('clicked()'), self.nextpat)
        self.connect(self.ui.comboBox_listpats, QtCore.SIGNAL('currentIndexChanged(int)'), self.comboxchange)
        self.ui.comboBox_listpats.clear()
        self.ui.comboBox_listpats.addItem("TEMP")

        self.wi_row = 255
        self.wi_col = 255
        self.DataShowiInTable()

    def paintEvent(self, envent):
        if self.current_edit_frame == 0:
            self.ui.lineEdit_index.setText("TEMP")
            # self.ui.lineEdit_totalpat.setText("Total is 0")
        else:
            self.ui.lineEdit_index.setText("Current:%d" % (self.current_edit_frame))
        self.ui.lineEdit_totalpat.setText("Total:%d" % (self.total_manual_pat))

    def changeText_sending(self):
        if self.connectFlag is True:
            self.ui.pushButton_sendpattochip.setText("Sending")

    def enablemanualpats(self):
        if self.connectFlag is False: return
        if self.test_pat_en is False:
            TFC.tfcWriteDwordMask(self.testing_pat_en_addr[0], 0, self.testing_pat_en_addr[1],\
                                  self.testing_pat_en_addr[1])
            self.test_pat_en = True
        pass

    def disablemanualpats(self):
        if self.connectFlag is False: return
        if self.test_pat_en is True:
            TFC.tfcWriteDwordMask(self.testing_pat_en_addr[0], 0, self.testing_pat_en_addr[1], 0)
            self.test_pat_en = False
        pass


    def enableTestingPats(self,flag):
        if self.connectFlag is False: return
        if flag is True:
            TFC.tfcWriteDwordMask(self.testing_pat_ctrl_addr[0], 0, self.testing_pat_ctrl_addr[1],
                                  0xC80F000C)
            TFC.tfcWriteDwordMask(self.testing_pat_en_addr[0], 0, self.testing_pat_en_addr[1],  self.testing_pat_en_addr[1])
            if self.ui.checkBox_bls.isChecked():
                TFC.tfcWriteDwordMask(self.manual_panel_bls[0], 0, self.manual_panel_bls[1], self.manual_panel_bls[1])
        else:
            TFC.tfcWriteDwordMask(self.testing_pat_en_addr[0], 0, self.testing_pat_en_addr[1], 0)
            TFC.tfcWriteDwordMask(self.manual_panel_bls[0], 0, self.manual_panel_bls[1], 0)
        self.test_pat_en = flag

    def patdelaytimechange(self):
        self.patdelaytime = self.ui.spinBox_patdelays.value() * 60
        self.curtmpppat[(6 + self.pat_size) * self.current_edit_frame + 5] = self.patdelaytime & 0xFFFF
        self.curtmpppat[(6 + self.pat_size) * self.current_edit_frame + 4] = (self.patdelaytime >> 16) & 0xFFFF
        print self.patdelaytime
        pass

    def addonepat(self):
        if self.initFlag is False: return
        if self.current_edit_frame >= 99:
            print "pattern is over flow!!"
            return
        # self.current_edit_frame += 1
        self.total_manual_pat += 1
        self.current_edit_frame = self.total_manual_pat
        self.ui.comboBox_listpats.addItem(" ==%d== " % self.total_manual_pat )
        for i in range(self.pat_size):
            self.curtmpppat[(6 + self.pat_size) * self.current_edit_frame + 6+i] = self.curpat[i]
        self.headpartupdate()
        pass

    def dellastonepat(self):
        if self.initFlag is False: return
        if self.total_manual_pat < 1:
            print "pattern is clear!!"
            return
        # self.current_edit_frame += 1
        self.total_manual_pat -= 1
        self.current_edit_frame = self.total_manual_pat
        self.ui.comboBox_listpats.removeItem(self.total_manual_pat +1)
        for i in range(self.pat_size):
            self.curpat[i] = self.curtmpppat[(6 + self.pat_size) * self.current_edit_frame + 6+i]
        self.headpartupdate()
        lowpos = (self.pat_size + 6)*self.current_edit_frame+4
        self.refreshspinbox(lowpos)
        self.DataShowiInTable()
        pass

    def sendpats(self):
        # sss = ""
        # for i in range((self.pat_size+6) * self.total_manual_pat):
        #     tmps = "%X" % self.curtmpppat[i]
        #     sss += " " + tmps
        # print sss
        if self.connectFlag is False: return
        if self.initFlag is False:return
        if self.current_edit_frame == 0:
            print("send one temp frame data!")
            for i in range(self.pat_size + 6):
                if 0== i%2:
                    addr_up = MANUAL_TESTING_PATS_ADDR + (i/2)*4
                    val = self.curtmpppat[i]+ (self.curtmpppat[i+1] <<16)
                    TFC.tfcWriteMemDword(addr_up,val)
                    # print hex(addr_up),hex(val)
        else:
            print("send %d frames data!" % self.total_manual_pat)
            for i in range(self.pat_size + 6,(self.pat_size + 6)*(self.total_manual_pat+1)):
                if 0== i%2:
                    addr_up = MANUAL_TESTING_PATS_ADDR + ((i-(self.pat_size + 6))/2)*4
                    val = self.curtmpppat[i]+ (self.curtmpppat[i+1] <<16)
                    TFC.tfcWriteMemDword(addr_up,val)
        self.ui.pushButton_sendpattochip.setText("SendToChip")
        self.enableTestingPats(True)
        pass

    def updatethenumnerofhead(self):
        for i in range(1,self.total_manual_pat+1):
            self.curtmpppat[(6 + self.pat_size) * i + 2] = self.total_manual_pat
        pass

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
            self.curtmpppat[0] = 0x3334
            self.curtmpppat[1] = 0x3132
            self.curtmpppat[2] = 1
            self.curtmpppat[3] = 1
            self.curtmpppat[4] = 0xFFFF
            self.curtmpppat[5] = 0xFFFF
            return
        else:
            self.curtmpppat[(6 + self.pat_size) * self.current_edit_frame + 0] = 0x3334
            self.curtmpppat[(6 + self.pat_size) * self.current_edit_frame + 1] = 0x3132
            self.curtmpppat[(6 + self.pat_size) * self.current_edit_frame + 2] = self.current_edit_frame
            self.curtmpppat[(6 + self.pat_size) * self.current_edit_frame + 3] = self.current_edit_frame
            self.patdelaytime = self.ui.spinBox_patdelays.value() * 60
            self.curtmpppat[(6 + self.pat_size) * self.current_edit_frame + 5] = self.patdelaytime & 0xFFFF
            self.curtmpppat[(6 + self.pat_size) * self.current_edit_frame + 4] = (self.patdelaytime >> 16) & 0xFFFF
            if self.total_manual_pat > 0:
                self.updatethenumnerofhead()
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
        isright = isproperdigit(stringitem)
        i = item.row()
        j = item.column()
        if isright is True:
            self.curpat[item.row()* self.debugregisters[u"led_x"] + item.column()] = int(stringitem,16)

        if islowerdigit(stringitem) is True or isright is False:
            self.ui.tableWidget_pattern.currentItem().setText(QtCore.QString("%1").arg(self.curpat[i * \
                                 self.ui.tableWidget_pattern.columnCount() + j],
                                        3, 16, QtCore.QChar(" ")).toUpper())
        for i in range(self.pat_size):
            self.curtmpppat[(self.pat_size+6)*self.current_edit_frame +6+i] = self.curpat[i]

    def updatepatts_1(self,i,j):
        if not self.initFlag: return
        # if self.wi_col == j and self.wi_row == i: return
        self.wi_col = j
        self.wi_row = i
        item = self.ui.tableWidget_pattern.currentItem()
        print item.text(),i,j
        stringitem = "%s" % item.text()
        isright = isproperdigit(stringitem)
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
        print flag
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
            if regs["name"] == "manual_panel_bls":
                self.manual_panel_bls[0] = int(regs["address"],16)
                self.manual_panel_bls[1] = self.generateMask(regs["bit_start"],regs["bit_end"])
                self.manual_panel_bls[2] = regs["bit_start"]
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
    def refreshcombox(self):
        self.ui.comboBox_listpats.clear()
        self.ui.comboBox_listpats.addItem("TEMP")
        for i in range(1,self.total_manual_pat+1):
            self.ui.comboBox_listpats.addItem(" ==%d== " % i)
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
    def printoutallpats(self):
        if self.total_manual_pat == 0:
            QtGui.QMessageBox.information(self, "warning", ("Please Add a new pattern!"))
            return
        tmps = "Total pattern: %d  \n" % self.total_manual_pat

        for j in range(1,self.total_manual_pat+1):
            tmps += "Current No. %d  / %d \n" % (self.curtmpppat[j*(self.pat_size + 6) +3], self.curtmpppat[j*(self.pat_size + 6) +2])
            tmps += "Delay Time: %d Seconds  \n" % (int((self.curtmpppat[j * (self.pat_size + 6) + 4] <<16) +
                                                self.curtmpppat[j * (self.pat_size + 6) + 5]  )/60)
            for i in range(6,(self.pat_size + 6)):
                if (i-6) % self.debugregisters[u"led_x"] == 0:
                    tmps += "\n"
                tmps += " %4X " % self.curtmpppat[j*(self.pat_size + 6) +i]
            tmps += "\n"
            tmps += "-------------------------------------------\n"
        self.ui.plainTextEdi_pats.setPlainText(tmps)
        pass

    def findthepatsize(self):
        ret = 32
        for i in range(1,512):
            if self.curtmpppat[i] == 0x3334:
                ret = i-6
                break
        return ret
        pass

    def savetofile(self):
        # file = QtGui.QFileDialog.getOpenFileName(self, "Open File dialog", "/", "bin files(*.bin *.txt)")
        dfile = QtGui.QFileDialog.getSaveFileName(self,"Save File dialog", "./", "bin files(*.bin *.txt)")
        if dfile:
            print dfile
        else:
            return

        dfile = str(dfile)
        try:
            self.curtmpppat.tofile(dfile)
        except Exception, e:
            print e



    def loadfromfile(self):
        file = QtGui.QFileDialog.getOpenFileName(self, "Open File dialog", "./", "bin files(*.bin *.txt)")
        if file:
            print file
        else:
            return
        file = str(file)
        try:
            self.curtmpppat =  np.fromfile(file, dtype=np.uint16)
        except Exception, e:
            print e
        if self.curtmpppat[0] != 0x3334:
            QtGui.QMessageBox.information(self, "warning", ("Please load correct file!\n current buffer has been clear."))
            self.total_manual_pat =0
            self.current_edit_frame = 0
            return
        self.pat_size = self.findthepatsize()
        if self.pat_size % 2 == 1:
            QtGui.QMessageBox.information(self, "warning", ("Please load correct file!\n current buffer has been clear."))
            self.total_manual_pat =0
            self.current_edit_frame = 0
            return
        if self.pat_size == 32 or self.pat_size == 48 or self.pat_size == 28:
            self.debugregisters[u"led_x"] = 4
        elif self.pat_size == 64:
            self.debugregisters[u"led_x"] = 8
        elif self.pat_size <= 18:
            self.debugregisters[u"led_x"] = 2
        else:
            self.debugregisters[u"led_x"] = 8
        self.debugregisters[u"led_y"] =  self.pat_size /self.debugregisters[u"led_x"]

        self.total_manual_pat = self.curtmpppat[(6 + self.pat_size)  + 2]
        self.current_edit_frame = 0
        self.initFlag = True
        for i in range(0,self.pat_size):
            self.curpat[i] = self.curtmpppat[i+6]
        self.reStruTable()
        self.DataShowiInTable()
        self.refreshcombox()


    def setbluescreen(self):
        if self.connectFlag is False: return
        if self.ui.checkBox_bls.isChecked():
            TFC.tfcWriteDwordMask(self.manual_panel_bls[0], 0, self.manual_panel_bls[1], self.manual_panel_bls[1])
        else:
            TFC.tfcWriteDwordMask(self.manual_panel_bls[0], 0, self.manual_panel_bls[1], 0)
    def refreshspinbox(self,pos):
        self.ui.spinBox_patdelays.setValue(((self.curtmpppat[pos] << 16) + self.curtmpppat[pos + 1])/60)
        # print ((self.curtmpppat[pos] << 16) + self.curtmpppat[pos + 1])/60
        # self.ui.spinBox_patdelays.setValue(99)
    def nextpat(self):
        if self.current_edit_frame < self.total_manual_pat:
            self.current_edit_frame += 1
        else:
            return
        for i in range(0,self.pat_size):
            self.curpat[i] = self.curtmpppat[(self.pat_size + 6)*self.current_edit_frame+i+6]
        lowpos = (self.pat_size + 6)*self.current_edit_frame+4
        self.refreshspinbox(lowpos)
        self.DataShowiInTable()
        pass

    def prevpat(self):
        if self.current_edit_frame > 0:
            self.current_edit_frame -= 1
        else:
            return
        for i in range(0,self.pat_size):
            self.curpat[i] = self.curtmpppat[(self.pat_size + 6)*self.current_edit_frame+i+6]
        lowpos = (self.pat_size + 6)*self.current_edit_frame+4
        self.refreshspinbox(lowpos)
        self.DataShowiInTable()
        pass

    def comboxchange(self):
        if  self.initFlag is False: return
        index = self.ui.comboBox_listpats.currentIndex()
        print index
        self.current_edit_frame = index
        for i in range(0,self.pat_size):
            self.curpat[i] = self.curtmpppat[(self.pat_size + 6)*self.current_edit_frame+i+6]
        lowpos = (self.pat_size + 6)*self.current_edit_frame+4
        self.refreshspinbox(lowpos)
        self.DataShowiInTable()
        pass

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    mywindow = TestPatternWindow()
    mywindow.show()
    sys.exit(app.exec_())
