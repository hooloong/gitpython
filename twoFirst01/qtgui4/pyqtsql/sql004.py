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
    q.exec_("select * from page")
    # q.exec_("commit")
    print q.result()
    print q.record().count()
    pagenameindex = q.record().indexOf("Caption")
    addr1 = q.record().indexOf("ShadowReg")
    addr2 = q.record().indexOf("ShadowRegVal")
    addr3 = q.record().indexOf("ShadowRegMask")
    print pagenameindex,addr1,addr2,addr3
    dimpageid = 0
    while q.next():
        if q.value(pagenameindex) == QtCore.QVariant("2DDIM_HIST"):
            print q.value(0).toString()
            dimpageid = int(q.value(0).toString())
            print "get the number ....."
            break
    q.exec_("select * from page where id = %d" % dimpageid)

    while q.next():
        dimpageaddr = (int(q.value(addr1).toString()) << 24) + (int(q.value(addr2).toString()) << 16) + (
        int(q.value(addr3).toString()) << 8)
    print hex(dimpageaddr)


def createTable():
    q = QtSql.QSqlQuery()
    q.exec_("create table if not exists t1 (f1 integer primary key,f2 varchar(20))")
    #q.exec_("delete from t1")

    q.exec_(u"insert into t1 values(1,'我')")
    q.exec_(u"insert into t1 values(2,'你你你')")
    q.exec_("commit")

class Model(QSqlTableModel):
    def __init__(self, parent):
        # type: (object) -> object
        QSqlTableModel.__init__(self, parent)

        # self.setTable("register")
        self.setTable("register")
        self.select()

        self.setEditStrategy(QSqlTableModel.OnManualSubmit)

class TestWidget(QtGui.QWidget):
    def __init__(self):
        QtGui.QWidget.__init__(self)
        vbox = QtGui.QVBoxLayout(self)
        self.view = QtGui.QTableView()
        self.model = Model(self.view)
        self.view.setModel(self.model)
        vbox.addWidget(self.view)


if __name__ == "__main__":
    a = QtGui.QApplication(sys.argv)
    createConnection()
    printoutpage()
    # w = TestWidget()
    # w.show()
    # sys.exit(a.exec_())
