__author__ = 'hooloongge'
# -*- coding: utf-8 -*-
from PyQt4 import QtGui, QtCore, QtSql
import sys

db=QtSql.QSqlDatabase.addDatabase("QSQLITE")
db.setDatabaseName("1111.db")
if db.open():
    print "db is open"
print "11111"
class FF(QtGui.QDialog):
    def __init__(self,parent=None):
        super(FF,self).__init__(parent)
        self.resize(300,300)

        self.model=QtSql.QSqlTableModel(self)
        self.model.setTable("user")
        self.model.setHeaderData(0,QtCore.Qt.Horizontal,QtCore.QVariant("xuhao"))
        self.model.setHeaderData(1,QtCore.Qt.Horizontal,QtCore.QVariant("content"))
        self.model.select()
        self.view=QtGui.QTableView(self)
        self.view.resize(300,300)
        self.view.setModel(self.model)
        self.view.resizeColumnsToContents()


        query=QtSql.QSqlQuery()
        query.exec_("select * from user")
        if query.next():
            print query.value(1).toString()


app=QtGui.QApplication(sys.argv)
f=FF()
f.show()
app.exec_()


