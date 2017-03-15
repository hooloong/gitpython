from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtSql import *
import sys

db=QSqlDatabase.addDatabase("QSQLITE")
db.setDatabaseName('a.db')
if db.open():
    print "db is open"

class FF(QDialog):
    def __init__(self,parent=None):
        super(FF,self).__init__(parent)
        resize = self.resize(300, 300)

        self.model=QSqlTableModel(self)
        self.model.setTable("user")
        self.model.setHeaderData(0,Qt.Horizontal,QVariant("xuhao"))
        self.model.setHeaderData(1,Qt.Horizontal,QVariant("content"))
        self.model.select()
        self.view=QTableView(self)
        self.view.resize(300,300)
        self.view.setModel(self.model)
        self.view.resizeColumnsToContents()

        query=QSqlQuery()
        query.exec_("select * from user")
        if query.next():
            print query.value(1).toString()


pp=QApplication(sys.argv)
f=FF()
f.show()
app.exec_()


