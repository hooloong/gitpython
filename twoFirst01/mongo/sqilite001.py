# -*- coding: utf-8 -*-
from PyQt4 import QtGui, QtCore, QtSql

import sys

from PyQt4.QtSql import QSqlTableModel


def createConnection():
    db = QtSql.QSqlDatabase.addDatabase("QSQLITE")

    db.setDatabaseName("test0.db")

    db.open()


def createTable():
    q = QtSql.QSqlQuery()
    q.exec_("create table if not exists t1 (f1 integer primary key,f2 varchar(20))")
    q.exec_("delete from t1")

    q.exec_(u"insert into t1 values(1,'我')")
    q.exec_(u"insert into t1 values(2,'我')")
    q.exec_("commit")


class Model(QSqlTableModel):
    def __init__(self, parent):
        # type: (object) -> object
        QSqlTableModel.__init__(self, parent)

        self.setTable("t1")

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
    createTable()
    w = TestWidget()
    w.show()
    sys.exit(a.exec_())
