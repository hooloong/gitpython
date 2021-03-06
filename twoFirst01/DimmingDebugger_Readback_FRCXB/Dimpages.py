__author__ = 'hooloongge'
# -*- coding: utf-8 -*-
import sys, math, random, time
import ctypes as C
import two01 as TFC
import numpy as np
from dispmipsfunc import *
from PyQt4 import QtCore, QtGui, QtSql,uic  # ,Qwt5

from Dimpages_res import *

bits_label_list = ["7","6","5","4","3","2","1","0","15","14","13","12","11","10","9","8",
                   "23","22","21","20","19","18","17","16","31","30","29","28","27","26","25","24"]

def isproperdigit(strinput):
    if len(strinput) == 0 or len(strinput) > 8:
        return False
    for c in strinput:
        if c not in proper_digit:
            return False
    return True
class HexSpinBox(QtGui.QSpinBox):

    def __init__(self):
        super(HexSpinBox, self).__init__()
        self.setRange(0,0xFFFFFFFF)
        self.validator = QtGui.QRegExpValidator(QtCore.QRegExp("[0-9A-Fa-f]{1,8}"),self)

    def validate(self, text, pos):
        return self.validator.validate(text,pos)

    def textFromValue(self, value):
        return QtCore.QString.number(value,16).toUpper()

    def valueFromText(self, text):
        p = False
        return text.toInt(p,16)

class regs():
    def __init__(self,index,name,descr,right,baseaddr):
        self.index = index
        self.name = name
        self.descr = descr
        self.right = right
        self.baseaddr = baseaddr


class DimPagesWindow(QtGui.QMainWindow):

    def __init__(self):
        super(DimPagesWindow, self).__init__()
        self.ui =  Ui_Form_Dimpages()
        self.ui.setupUi(self)
        # insert hexspinbox in to table
        self.hexspinlist = []
        self.histpageregs=[]
        self.pixcpageregs=[]
        self.treepagesname={"2DDIM_HIST":1,"2DDIM_PIXC":0}
        for i in range(64):
            # newhex = HexSpinBox()
            newhex = QtGui.QSpinBox()
            newhex.setRange(0,99999999)
            newhex.setButtonSymbols(2)
            newhex.setVisible(False)
            # newhex.setButtonSymbols(0)
            self.hexspinlist.append(newhex)
        self.curvars = np.zeros(64,np.uint32)
        self.chipstorecurvars = np.zeros(64, np.uint32)
        self.chippageright = np.zeros(64, np.uint32)
        self.curbaseaddr = 0x19A00400
        self.curpageregs = []
        self.connectFlag = False
        self.initFlag = False
        self.curchipreadflag = False
        self.start_pos = 0
        self.pages= {}

        self.connect(self.ui.pushButton_getitem, QtCore.SIGNAL('clicked()'), self.printoutregs)
        self.connect(self.ui.pushButton_readpage, QtCore.SIGNAL('clicked()'), self.readcurpage)
        self.connect(self.ui.pushButton_writepage, QtCore.SIGNAL('clicked()'), self.writecurpage)
        self.connect(self.ui.pushButton_refresh, QtCore.SIGNAL('clicked()'), self.readcurpage)

        self.connect(self.ui.tableWidget_curpage, QtCore.SIGNAL('cellPressed(int,int)'), self.changeRegDescri)
        self.ui.tableWidget_curpage.itemChanged.connect(self.updatepatts)

        self.ui.treeWidget_pages.itemPressed.connect(self.pagesel)

        self.connect(self.ui.radioButton_7, QtCore.SIGNAL('clicked(bool)'), self.changeBitsel)
        self.connect(self.ui.radioButton_15, QtCore.SIGNAL('clicked(bool)'), self.changeBitsel)
        self.connect(self.ui.radioButton_23, QtCore.SIGNAL('clicked(bool)'), self.changeBitsel)
        self.connect(self.ui.radioButton_31, QtCore.SIGNAL('clicked(bool)'), self.changeBitsel)
        self.connect(self.ui.checkBox_0, QtCore.SIGNAL('clicked()'), self.setbitcheck)
        self.connect(self.ui.checkBox_1, QtCore.SIGNAL('clicked()'), self.setbitcheck)
        self.connect(self.ui.checkBox_2, QtCore.SIGNAL('clicked()'), self.setbitcheck)
        self.connect(self.ui.checkBox_3, QtCore.SIGNAL('clicked()'), self.setbitcheck)
        self.connect(self.ui.checkBox_4, QtCore.SIGNAL('clicked()'), self.setbitcheck)
        self.connect(self.ui.checkBox_5, QtCore.SIGNAL('clicked()'), self.setbitcheck)
        self.connect(self.ui.checkBox_6, QtCore.SIGNAL('clicked()'), self.setbitcheck)
        self.connect(self.ui.checkBox_7, QtCore.SIGNAL('clicked()'), self.setbitcheck)

        self.createConnection()
        self.printoutregs()
        self.curpageregs = self.histpageregs
        self.getrightforcurpage()
        self.DataShowiInTable()
        self.ui.radioButton_31.setChecked(True)
        self.start_pos = 24
        self.initFlag = True
        self.curselreg = 0

    # def keyPressEvent(self, ev):
    #     print ev.key()
    #     print  QtCore.Qt.Key_Space
    #     if ev.key() == QtCore.Qt.Key_Space:
    #         ev.ignore()
    #         return
    #     ev.accept()

    def keyReleaseEvent(self, ev):
        if ev.key() == QtCore.Qt.Key_Space:
            self.readcurpage()
            ev.ignore()
            return
        ev.accept()

    def createConnection(self):
        self.db = QtSql.QSqlDatabase.addDatabase("QODBC")
        connection_string = 'Driver={Microsoft Access Driver (*.mdb)};DBQ=D:\\testing_fb.mdb'
        self.db.setDatabaseName(connection_string)
        self.db.open()

    def getrightforcurpage(self):
        self.chippageright = np.zeros(64,np.uint32)
        for inx in range(64):
            for k in range(len(self.curpageregs)):
                if self.curpageregs[k].index == inx:
                    getright = self.curpageregs[k].right
                    self.chippageright[inx] = getright

    def DataShowiInTable(self):
        self.chippageright = np.zeros(64, np.uint32)
        for i in range(self.ui.tableWidget_curpage.rowCount()):
            for j in range(self.ui.tableWidget_curpage.columnCount()):
                getFlag = False
                getright = 0
                # pwmdutytemp = "%X" % (self.curpat[i * self.ui.tableWidget_pattern.columnCount() + j])
                newItemt = QtGui.QTableWidgetItem(QtCore.QString("%1").arg(self.curvars[i * \
                self.ui.tableWidget_curpage.columnCount() + j],8,16,QtCore.QChar("0")).toUpper())
                newItemt.setTextAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
                ind = (i*4 + j)
                for k in range(len(self.curpageregs)):
                    # print reg.index,i,j
                    if self.curpageregs[k].index == ind:
                        getright =  self.curpageregs[k].right
                        getFlag = True
                        if getright == 1:
                            newItemt.setBackground(QtGui.QColor(255, 0, 255))
                if getFlag is False:
                    newItemt.setBackground(QtGui.QColor(125, 125, 125))
                    newItemt.setFlags(QtCore.Qt.NoItemFlags)
                self.ui.tableWidget_curpage.setItem(i, j, newItemt)

    def updatethecheckboxbits(self,byte):
        if byte & 0x80:
            self.ui.checkBox_7.setChecked(True)
        else:
            self.ui.checkBox_7.setChecked(False)
        if byte & 0x40:
            self.ui.checkBox_6.setChecked(True)
        else:
            self.ui.checkBox_6.setChecked(False)
        if byte & 0x20:
            self.ui.checkBox_5.setChecked(True)
        else:
            self.ui.checkBox_5.setChecked(False)
        if byte & 0x10:
            self.ui.checkBox_4.setChecked(True)
        else:
            self.ui.checkBox_4.setChecked(False)
        if byte & 0x8:
            self.ui.checkBox_3.setChecked(True)
        else:
            self.ui.checkBox_3.setChecked(False)
        if byte & 0x4:
            self.ui.checkBox_2.setChecked(True)
        else:
            self.ui.checkBox_2.setChecked(False)
        if byte & 0x2:
            self.ui.checkBox_1.setChecked(True)
        else:
            self.ui.checkBox_1.setChecked(False)
        if byte & 0x1:
            self.ui.checkBox_0.setChecked(True)
        else:
            self.ui.checkBox_0.setChecked(False)
        pass

    def setCurRegVarTochip(self,reg,num):
        if self.connectFlag is False: return
        if self.initFlag is False: return
        if self.curchipreadflag is False: return
        ret = False
        if self.curvars[num] != self.chipstorecurvars[num]:
            ret = True
        else:
            ret = False
        self.chipstorecurvars[num] = self.curvars[num]
        if ret is True and self.connectFlag is True and self.curchipreadflag is True:
            if reg.right !=1 :
                TFC.tfcWriteDword(reg.baseaddr, num*4,self.chipstorecurvars[num])
        pass
    def setbitcheck(self):

        temp = 0xFFFFFFFF & (~(0xFF << self.start_pos))
        self.curvars[self.curselreg] &= temp
        self.curvars[self.curselreg] |= (self.getbitfromcheckbox() << self.start_pos)

        for k in range(len(self.curpageregs)):
            if self.curpageregs[k].index == self.curselreg:
                self.changeTableOneReg(self.curselreg/4 , self.curselreg%4)
                self.setCurRegVarTochip(self.curpageregs[k],self.curselreg)
        pass
    def getbitfromcheckbox(self):
        bytevar = 0
        if self.ui.checkBox_0.isChecked():
            bytevar |= 1
        if self.ui.checkBox_1.isChecked():
            bytevar |= 2

        if self.ui.checkBox_2.isChecked():
            bytevar |= 4

        if self.ui.checkBox_3.isChecked():
            bytevar |= 8

        if self.ui.checkBox_4.isChecked():
            bytevar |= 0x10

        if self.ui.checkBox_5.isChecked():
            bytevar |= 0x20

        if self.ui.checkBox_6.isChecked():
            bytevar |= 0x40

        if self.ui.checkBox_7.isChecked():
            bytevar |= 0x80

        return bytevar


    def updatethebitsfromvars(self):
        print self.curselreg,self.curvars[self.curselreg],self.start_pos
        self.updatethecheckboxbits(self.curvars[self.curselreg] >> self.start_pos)
        pass

    def changeTableOneReg(self,row,col):
        self.ui.tableWidget_curpage.currentItem().setText(QtCore.QString("%1").arg(self.curvars[row * \
                                 self.ui.tableWidget_curpage.columnCount() + col],
                                        8, 16, QtCore.QChar("0")).toUpper())
        pass

    def getCurRegVarFromchip(self,reg,num):
        if self.connectFlag is False: return
        if self.initFlag is False: return
        if self.curchipreadflag is False: return
        ret = False
        self.chipstorecurvars[num] = TFC.tfcReadDword(reg.baseaddr, num*4)
        if self.curvars[num] != self.chipstorecurvars[num]:
            ret = True
        else:
            ret = False
        self.curvars[num] = self.chipstorecurvars[num]
        return True

    def changeRegDescri(self,row,col):
        itemregchangflag = False
        for k in range(len(self.curpageregs)):
            if self.curpageregs[k].index == (row * 4 + col):
                itemregchangflag = self.getCurRegVarFromchip(self.curpageregs[k],row * 4 + col)
                self.ui.textEdit_curregdes.setText(self.curpageregs[k].descr)
                self.ui.label_addr.setText(
                    "%X" % (self.curpageregs[k].baseaddr + self.curpageregs[k].index * 4))
                self.ui.label_regsname.setText(self.curpageregs[k].name)
                print self.curpageregs[k].right
                self.curselreg = row * 4 + col
                self.updatethebitsfromvars()
                if itemregchangflag is True:
                    self.changeTableOneReg(row,col)
                break

    def changeRegDescri_1(self,row,col):
        print row,col

    def pagesel(self,item,pos):
        if self.initFlag is False: return
        if item != self.ui.treeWidget_pages.currentItem():
            return
        currentkey = ""
        for key in self.treepagesname:
            if key == item.text(pos) and self.treepagesname[key] == 1:
                return
            if key == item.text(pos) and self.treepagesname[key] == 0:
                self.curchipreadflag= False
                currentkey = key
        self.treepagesname[currentkey] = 1
        for key in self.treepagesname:
            if key != currentkey:
                self.treepagesname[key] = 0
        print self.treepagesname
        if currentkey == "2DDIM_PIXC":
            self.curpageregs= self.pixcpageregs
        else:
            self.curpageregs = self.histpageregs
        self.curbaseaddr = self.curpageregs[0].baseaddr
        self.getrightforcurpage()
        self.readcurpage()
        self.DataShowiInTable()

    def changeBitsel(self,flag):
        if not self.initFlag: return

        if self.ui.radioButton_7.isChecked():
            self.start_pos = 0
        elif self.ui.radioButton_15.isChecked():
            self.start_pos = 8
        elif self.ui.radioButton_23.isChecked():
            self.start_pos = 16
        else:
            self.start_pos = 24
        self.ui.label_24.setText(bits_label_list[self.start_pos+7])
        self.ui.label_25.setText(bits_label_list[self.start_pos+6])
        self.ui.label_26.setText(bits_label_list[self.start_pos+5])
        self.ui.label_27.setText(bits_label_list[self.start_pos+4])
        self.ui.label_28.setText(bits_label_list[self.start_pos+3])
        self.ui.label_29.setText(bits_label_list[self.start_pos+2])
        self.ui.label_30.setText(bits_label_list[self.start_pos+1])
        self.ui.label_31.setText(bits_label_list[self.start_pos])

        self.updatethebitsfromvars()
        pass

    def updatepatts(self,item):
        if not self.initFlag: return
        if item != self.ui.tableWidget_curpage.currentItem():
            return
        print item.text()
        stringitem = "%s" % item.text()
        isright = isproperdigit(stringitem)
        i = item.row()
        j = item.column()
        if isright is True:
            self.curvars[item.row()* 4 + item.column()] = int(stringitem,16)
            self.ui.tableWidget_curpage.currentItem().setText(QtCore.QString("%1").arg(self.curvars[i * \
                                 self.ui.tableWidget_curpage.columnCount() + j],
                                        8, 16, QtCore.QChar("0")).toUpper())

        if islowerdigit(stringitem) is True or isright is False:
            self.ui.tableWidget_curpage.currentItem().setText(QtCore.QString("%1").arg(self.curvars[i * \
                                 self.ui.tableWidget_curpage.columnCount() + j],
                                        8, 16, QtCore.QChar("0")).toUpper())

    def readcurpage(self):
        if self.connectFlag is False: return
        if self.initFlag is False: return
        # self.chipstorecurvars = np.zeros(64, np.uint32)
        self.curbaseaddr = self.curpageregs[0].baseaddr
        self.getrightforcurpage()
        for i in range(64):
            if self.chippageright[i] != 0 and self.chippageright[i] != 2:
                self.chipstorecurvars[i] = TFC.tfcReadDword(self.curbaseaddr, i*4)
            else:
                self.chipstorecurvars[i] = 0
            self.curvars[i] =  self.chipstorecurvars[i]

        self.DataShowiInTable()
        # print self.chipstorecurvars
        self.curchipreadflag = True

        pass

    def writecurpage(self):
        if self.connectFlag is False: return
        if self.initFlag is False: return
        if self.curchipreadflag is False: return
        self.curbaseaddr = self.curpageregs[0].baseaddr
        self.getrightforcurpage()
        self.chipstorecurvars = np.zeros(64, np.uint32)
        for i in range(64):
            self.chipstorecurvars[i] = self.curvars[i]
            if self.chippageright[i] != 0 and self.chippageright[i] != 1:
                TFC.tfcWriteDword(self.curbaseaddr,i*4,self.chipstorecurvars[i])

        print self.curbaseaddr
        pass

    def printoutregs(self):
        self.q = QtSql.QSqlQuery()
        self.q.exec_("select id,shadowreg,shadowregval,shadowregmask from page where caption='2DDIM_HIST'")
        print self.q.record().count()
        addr1 = self.q.record().indexOf("ShadowReg")
        addr2 = self.q.record().indexOf("ShadowRegVal")
        addr3 = self.q.record().indexOf("ShadowRegMask")
        # print addr1,addr2,addr3
        self.dimpageid = 0
        while self.q.next():
            self.dimpageaddr = (int(self.q.value(addr1).toString()) << 24) + (int(self.q.value(addr2).toString()) << 16) + (
                int(self.q.value(addr3).toString()) << 8)
            self.dimpageid = int(self.q.value(0).toString())
        print hex(self.dimpageaddr), self.dimpageid

        self.q.exec_("select id,regname,regaddress,description,bit0right from register where page = %d and regaddress < 64 order by regaddress" % self.dimpageid)
        print self.q.record().count()
        addr1 = self.q.record().indexOf("RegName")
        addr2 = self.q.record().indexOf("RegAddress")
        addr3 = self.q.record().indexOf("Description")
        addr4 = self.q.record().indexOf("bit0right")
        # dimpageid = 0
        while self.q.next():
            regname = str(self.q.value(addr1).toString())
            regaddr = int(self.q.value(addr2).toString())
            regdescription = str(self.q.value(addr3).toString())
            regright = int(self.q.value(addr4).toString())
            # print hex(self.dimpageaddr + regaddr * 4), regname,regright
            # print regdescription
            self.histpageregs.append(regs(regaddr,regname,regdescription,regright,self.dimpageaddr))
        print len(self.histpageregs)

        self.q.exec_("select id,shadowreg,shadowregval,shadowregmask from page where caption='2DDIM_PIXC0'")
        print self.q.record().count()
        addr1 = self.q.record().indexOf("ShadowReg")
        addr2 = self.q.record().indexOf("ShadowRegVal")
        addr3 = self.q.record().indexOf("ShadowRegMask")
        # print addr1,addr2,addr3
        self.dimpageid_p = 0
        while self.q.next():
            self.dimpageaddr_p = (int(self.q.value(addr1).toString()) << 24) + (int(self.q.value(addr2).toString()) << 16) + (
                int(self.q.value(addr3).toString()) << 8)
            self. dimpageid_p = int(self.q.value(0).toString())
        print hex(self.dimpageaddr_p), self.dimpageid_p
        self.q.exec_("select id,regname,regaddress,description,bit0right from register where page = %d and regaddress < 64 order by regaddress " %self.dimpageid_p)
        print self.q.record().count()
        addr1 = self.q.record().indexOf("RegName")
        addr2 = self.q.record().indexOf("RegAddress")
        addr3 = self.q.record().indexOf("Description")
        addr4 = self.q.record().indexOf("bit0right")
        # dimpageid = 0
        while self.q.next():
            regname = str(self.q.value(addr1).toString())
            regaddr = int(self.q.value(addr2).toString())
            regdescription = str(self.q.value(addr3).toString())
            regright = int(self.q.value(addr4).toString())
            self.pixcpageregs.append(regs(regaddr,regname,regdescription,regright,self.dimpageaddr_p))
        print len(self.pixcpageregs)

    def setConnectFlag(self, flag):
        self.connectFlag = flag
        pass

    def setSettingDict(self, pages):
        self.pages = pages
        # print self.pages



if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    mywindow = DimPagesWindow()
    mywindow.show()
    sys.exit(app.exec_())
