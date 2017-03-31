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
    def __init__(self,index,name,descr,right):
        self.index = index
        self.name = name
        self.descr = descr
        self.right = right


class DimPagesWindow(QtGui.QMainWindow):

    def __init__(self):
        super(DimPagesWindow, self).__init__()
        self.ui =  Ui_Form_Dimpages()
        self.ui.setupUi(self)
        # insert hexspinbox in to table
        self.hexspinlist = []
        self.histpageregs=[]
        for i in range(64):
            # newhex = HexSpinBox()
            newhex = QtGui.QSpinBox()
            newhex.setRange(0,99999999)
            newhex.setButtonSymbols(2)
            newhex.setVisible(False)
            # newhex.setButtonSymbols(0)
            self.hexspinlist.append(newhex)
        self.curvars = np.zeros(64,np.uint32)

        self.connectFlag = False
        self.initFlag = False
        self.start_pos = 0

        self.connect(self.ui.pushButton_getitem, QtCore.SIGNAL('clicked()'), self.printoutregs)
        # self.connect(self.ui.tableWidget_curpage, QtCore.SIGNAL('itemClicked(int,int)'),self.changeRegDescri_1)
        # self.connect(self.ui.tableWidget_curpage, QtCore.SIGNAL('cellEntered(int,int)'), self.changeRegDescri)
        # self.connect(self.ui.tableWidget_curpage, QtCore.SIGNAL('cellActivated(int,int)'), self.changeRegDescri)
        self.connect(self.ui.tableWidget_curpage, QtCore.SIGNAL('cellPressed(int,int)'), self.changeRegDescri)
        self.ui.tableWidget_curpage.itemChanged.connect(self.updatepatts)
        self.connect(self.ui.radioButton_7, QtCore.SIGNAL('clicked(bool)'), self.changeBitsel)
        self.connect(self.ui.radioButton_15, QtCore.SIGNAL('clicked(bool)'), self.changeBitsel)
        self.connect(self.ui.radioButton_23, QtCore.SIGNAL('clicked(bool)'), self.changeBitsel)
        self.connect(self.ui.radioButton_31, QtCore.SIGNAL('clicked(bool)'), self.changeBitsel)

        self.createConnection()
        self.printoutregs()
        self.DataShowiInTable()

        self.ui.radioButton_31.setChecked(True)
        self.initFlag = True
        self.curselreg = 0

    def createConnection(self):
        self.db = QtSql.QSqlDatabase.addDatabase("QODBC")
        connection_string = 'Driver={Microsoft Access Driver (*.mdb)};DBQ=D:\\testing7.mdb'
        self.db.setDatabaseName(connection_string)
        self.db.open()
    def DataShowiInTable(self):
        # testing patt
        for i in range(self.ui.tableWidget_curpage.rowCount()):
            for j in range(self.ui.tableWidget_curpage.columnCount()):
                # pwmdutytemp = "%X" % (self.curpat[i * self.ui.tableWidget_pattern.columnCount() + j])
                newItemt = QtGui.QTableWidgetItem(QtCore.QString("%1").arg(self.curvars[i * \
                self.ui.tableWidget_curpage.columnCount() + j],8,16,QtCore.QChar("0")).toUpper())
                newItemt.setTextAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
                if self.histpageregs[i*4 + j].right == 1:
                    newItemt.setBackground(QtGui.QColor(255,0,255))
                self.ui.tableWidget_curpage.setItem(i, j, newItemt)

    def changeRegDescri(self,row,col):
        print row,col
        self.ui.textEdit_curregdes.setText(self.histpageregs[row*4 + col].descr)
        self.ui.label_addr.setText("%X" % (self.dimpageaddr + self.histpageregs[row*4 + col].index * 4))
        self.ui.label_regsname.setText(self.histpageregs[row*4 + col].name)
        print self.histpageregs[row*4 + col].right
        self.curselreg = row*4 + col

    def changeRegDescri_1(self,row,col):
        print row,col

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

        if islowerdigit(stringitem) is True or isright is False:
            self.ui.tableWidget_curpage.currentItem().setText(QtCore.QString("%1").arg(self.curvars[i * \
                                 self.ui.tableWidget_curpage.columnCount() + j],
                                        8, 16, QtCore.QChar("0")).toUpper())


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
            self.histpageregs.append(regs(regaddr,regname,regdescription,regright))
        print len(self.histpageregs)

        # self.q.exec_("select id,shadowreg,shadowregval,shadowregmask from page where caption='2DDIM_PIXC'")
        # print self.q.record().count()
        # addr1 = self.q.record().indexOf("ShadowReg")
        # addr2 = self.q.record().indexOf("ShadowRegVal")
        # addr3 = self.q.record().indexOf("ShadowRegMask")
        # # print addr1,addr2,addr3
        # self.dimpageid_p = 0
        # while self.q.next():
        #     self.dimpageaddr_p = (int(self.q.value(addr1).toString()) << 24) + (int(self.q.value(addr2).toString()) << 16) + (
        #         int(self.q.value(addr3).toString()) << 8)
        #     self. dimpageid_p = int(self.q.value(0).toString())
        # print hex(self.dimpageaddr_p), self.dimpageid_p
        # self.q.exec_("select id,regname,regaddress,description from register where page = %d " %self.dimpageid_p)
        # print self.q.record().count()
        # addr1 = self.q.record().indexOf("RegName")
        # addr2 = self.q.record().indexOf("RegAddress")
        # addr3 = self.q.record().indexOf("Description")
        # # dimpageid = 0
        # while self.q.next():
        #     regname = str(self.q.value(addr1).toString())
        #     regaddr = int(self.q.value(addr2).toString())
        #     regdescription = str(self.q.value(addr3).toString())
        #     print hex(self.dimpageaddr_p + regaddr * 4), regname
        #     print regdescription

    def setConnectFlag(self, flag):
        self.connectFlag = flag




if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    mywindow = DimPagesWindow()
    mywindow.show()
    sys.exit(app.exec_())
