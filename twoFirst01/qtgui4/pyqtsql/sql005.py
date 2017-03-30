# -*- coding: utf-8 -*-
import sys

from PyQt4 import QtGui, QtSql,QtCore
from PyQt4.QtSql import QSqlTableModel
# import Rtf2TXT as RTF


def createConnection():
    db = QtSql.QSqlDatabase.addDatabase("QODBC")
    connection_string = 'Driver={Microsoft Access Driver (*.mdb)};DBQ=D:\\testing7.mdb'
    db.setDatabaseName(connection_string)

    db.open()


def createTable():
    q = QtSql.QSqlQuery()
    q.exec_("create table if not exists t1 (f1 integer primary key,f2 varchar(20))")
    #q.exec_("delete from t1")

    q.exec_(u"insert into t1 values(1,'我')")
    q.exec_(u"insert into t1 values(2,'你你你')")
    q.exec_("commit")

def printoutpage():
    q = QtSql.QSqlQuery()
    q.exec_("select id,shadowreg,shadowregval,shadowregmask from page where caption='2DDIM_HIST'")
    print q.record().count()
    addr1 = q.record().indexOf("ShadowReg")
    addr2 = q.record().indexOf("ShadowRegVal")
    addr3 = q.record().indexOf("ShadowRegMask")
    # print addr1,addr2,addr3
    dimpageid = 0
    while q.next():
        dimpageaddr = (int(q.value(addr1).toString()) << 24) + (int(q.value(addr2).toString()) << 16) + (
        int(q.value(addr3).toString()) << 8)
        dimpageid = int(q.value(0).toString())
    print hex(dimpageaddr),dimpageid
    q.exec_("select id,shadowreg,shadowregval,shadowregmask from page where caption='2DDIM_PIXC'")
    print q.record().count()
    addr1 = q.record().indexOf("ShadowReg")
    addr2 = q.record().indexOf("ShadowRegVal")
    addr3 = q.record().indexOf("ShadowRegMask")
    # print addr1,addr2,addr3
    dimpageid_p = 0
    while q.next():
        dimpageaddr_p = (int(q.value(addr1).toString()) << 24) + (int(q.value(addr2).toString()) << 16) + (
        int(q.value(addr3).toString()) << 8)
        dimpageid_p = int(q.value(0).toString())
    print hex(dimpageaddr_p),dimpageid_p

    q.exec_("select id,regname,regaddress,description from register where page = %d " % dimpageid )
    print q.record().count()
    addr1 = q.record().indexOf("RegName")
    addr2 = q.record().indexOf("RegAddress")
    addr3 = q.record().indexOf("Description")
    # dimpageid = 0
    while q.next():
        regname = str(q.value(addr1).toString())
        regaddr =  int(q.value(addr2).toString())
        regdescription = str(q.value(addr3).toString())
        print hex(dimpageaddr+regaddr*4),regname
        print regdescription
    q.exec_("select id,regname,regaddress,description from register where page = %d " % dimpageid_p )
    print q.record().count()
    addr1 = q.record().indexOf("RegName")
    addr2 = q.record().indexOf("RegAddress")
    addr3 = q.record().indexOf("Description")
    # dimpageid = 0
    while q.next():
        regname = str(q.value(addr1).toString())
        regaddr =  int(q.value(addr2).toString())
        regdescription = str(q.value(addr3).toString())
        print hex(dimpageaddr_p+regaddr*4),regname
        print regdescription

def createTable():
    q = QtSql.QSqlQuery()
    q.exec_("create table if not exists t1 (f1 integer primary key,f2 varchar(20))")
    #q.exec_("delete from t1")

    q.exec_(u"insert into t1 values(1,'我')")
    q.exec_(u"insert into t1 values(2,'你你你')")
    q.exec_("commit")




if __name__ == "__main__":
    a = QtGui.QApplication(sys.argv)
    createConnection()
    printoutpage()

