__author__ = 'hooloongge'
# -*- coding: utf-8 -*-
import sys, math, random, time
import ctypes as C
import two01 as TFC
import numpy as np
from dispmipsfunc import *
from PyQt4 import QtCore, QtGui, QtSql,uic  # ,Qwt5

from Dimpages_res import *


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


class DimPagesWindow(QtGui.QMainWindow):

    def __init__(self):
        super(DimPagesWindow, self).__init__()
        self.ui =  Ui_Form_Dimpages()
        self.ui.setupUi(self)
        # insert hexspinbox in to table
        self.hexspinlist = []
        for i in range(64):
            # newhex = HexSpinBox()
            newhex = QtGui.QSpinBox()
            self.hexspinlist.append(newhex)
        for i in range(self.ui.tableWidget_curpage.columnCount()):
            for j in range(self.ui.tableWidget_curpage.rowCount()):
                self.ui.tableWidget_curpage.setCellWidget(j,i,self.hexspinlist[j*4 + i])



        self.connectFlag = False

        self.connect(self.ui.pushButton_getitem, QtCore.SIGNAL('clicked()'), self.printoutregs)

        self.createConnection()

    def createConnection(self):
        self.db = QtSql.QSqlDatabase.addDatabase("QODBC")
        connection_string = 'Driver={Microsoft Access Driver (*.mdb)};DBQ=D:\\testing7.mdb'
        self.db.setDatabaseName(connection_string)

        self.db.open()

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
        self.q.exec_("select id,shadowreg,shadowregval,shadowregmask from page where caption='2DDIM_PIXC'")
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

        self.q.exec_("select id,regname,regaddress,description from register where page = %d " % self.dimpageid)
        print self.q.record().count()
        addr1 = self.q.record().indexOf("RegName")
        addr2 = self.q.record().indexOf("RegAddress")
        addr3 = self.q.record().indexOf("Description")
        # dimpageid = 0
        while self.q.next():
            regname = str(self.q.value(addr1).toString())
            regaddr = int(self.q.value(addr2).toString())
            regdescription = str(self.q.value(addr3).toString())
            print hex(self.dimpageaddr + regaddr * 4), regname
            print regdescription
        self.q.exec_("select id,regname,regaddress,description from register where page = %d " %self.dimpageid_p)
        print self.q.record().count()
        addr1 = self.q.record().indexOf("RegName")
        addr2 = self.q.record().indexOf("RegAddress")
        addr3 = self.q.record().indexOf("Description")
        # dimpageid = 0
        while self.q.next():
            regname = str(self.q.value(addr1).toString())
            regaddr = int(self.q.value(addr2).toString())
            regdescription = str(self.q.value(addr3).toString())
            print hex(self.dimpageaddr_p + regaddr * 4), regname
            print regdescription

    def setConnectFlag(self, flag):
        self.connectFlag = flag




if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    mywindow = DimPagesWindow()
    mywindow.show()
    sys.exit(app.exec_())
