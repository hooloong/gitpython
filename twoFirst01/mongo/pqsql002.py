# coding:UTF-8
import os
import sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtSql import *
from ExcelTool import ExcelHandler


def insertData(filenames):
    query = QSqlQuery()
    for filename in filenames:
        eh = ExcelHandler()
        results = eh.read_xls(filename)
        for result in results:
            for lines in result[1]:
                sql = "INSERT INTO pseas VALUES ("
                for ii in range(len(lines)):
                    sql = sql + "'" + lines[ii].replace("\n", "") + "'"
                    if ii == len(lines) - 1:
                        sql = sql + ")"
                    else:
                        sql = sql + ","
                query.exec_(sql)
                print sql
        QApplication.processEvents()

    query = QSqlQuery()
    sql = u"delete FROM pseas where jxName='XXX'"
    query.exec_(sql)
    print sql
    QApplication.processEvents()

    query.clear()
    query.finish()


def createData(filenames):
    print "Dropping tables..."
    query = QSqlQuery()
    query.exec_("DROP TABLE version")
    QApplication.processEvents()

    print "Creating tables..."
    #    query.exec_("""CREATE TABLE pseas (bsid VARCHAR(255) PRIMARY KEY NOT NULL,page VARCHAR(255),jxnum VARCHAR(255), jxname VARCHAR(255), jgnum VARCHAR(255), jgjpname VARCHAR(255), jgenname VARCHAR(255), ljid VARCHAR(255), ljnum VARCHAR(255),lj12num VARCHAR(255),ljjpname VARCHAR(255),ljenname VARCHAR(255),ljcount VARCHAR(255))""")
    query.exec_(
        """CREATE TABLE version (vsid INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL, vsnum VARCHAR(255) ,vsdate VARCHAR(255))""")
    QApplication.processEvents()

    #    print "Creating data..."
    #    query.exec_("""INSERT INTO version(vsnum,vsdate) VALUES('1','20100802')""")
    #    query.exec_("""INSERT INTO version(vsnum,vsdate) VALUES('2','20100802')""")
    #    query.exec_("""INSERT INTO version(vsnum,vsdate) VALUES('3','20100802')""")
    #    query.exec_("""INSERT INTO version(vsnum,vsdate) VALUES('1','20100803')""")
    #    query.exec_("""INSERT INTO version(vsnum,vsdate) VALUES('2','20100803')""")
    #    query.exec_("""INSERT INTO version(vsnum,vsdate) VALUES('3','20100803')""")
    #    query.exec_("""INSERT INTO version(vsnum,vsdate) VALUES('4','20100803')""")
    #    query.exec_("""INSERT INTO version(vsnum,vsdate) VALUES('1','20100804')""")
    #    query.exec_("""INSERT INTO version(vsnum,vsdate) VALUES('1','20100805')""")
    #    query.exec_("""INSERT INTO version(vsnum,vsdate) VALUES('1','20100806')""")
    #    QApplication.processEvents()

    #    query.exec_("""INSERT INTO version VALUES('1','1','20100802')""")
    #    query.exec_("""INSERT INTO version VALUES('2','2','20100802')""")
    #    query.exec_("""INSERT INTO version VALUES('3','3','20100802')""")
    #    query.exec_("""INSERT INTO version VALUES('4','1','20100803')""")
    #    query.exec_("""INSERT INTO version VALUES('5','2','20100803')""")
    #    query.exec_("""INSERT INTO version VALUES('6','3','20100803')""")
    #    query.exec_("""INSERT INTO version VALUES('7','4','20100803')""")
    #    query.exec_("""INSERT INTO version VALUES('8','1','20100804')""")
    #    query.exec_("""INSERT INTO version VALUES('9','1','20100805')""")
    #    query.exec_("""INSERT INTO version VALUES('10','1','20100806')""")
    #    QApplication.processEvents()
    print "Populating tables..."
    vsid = '0'
    vsnum = '0'
    vsdate = '20100813'
    query.exec_("select max(vsid),vsnum,vsdate from version where vsdate='" + vsdate + "'")
    while query.next():
        vsid = unicode(query.value(0).toString())
        vsnum = unicode(query.value(1).toString())
        vsdate = unicode(query.value(2).toString())
    if vsid == '':
        print "vsid = ''"
    if vsnum == '':
        print "vsnum = ''"
    if vsdate == "":
        print "vsdate = ''"


# insertData(filenames)
#    eh = ExcelHandler()
#    result = eh.read_xls(filename)
#    for lines in result:
#        sql = "INSERT INTO pseas VALUES ("
#        for ii in range(len(lines)):
#            sql = sql + "'" + lines[ii] + "'"
#            if ii == len(lines)-1:
#                sql = sql + ")"
#            else:
#                sql = sql + ","
#        query.exec_(sql)
#        print sql
#    QApplication.processEvents()

def main():
    app = QApplication(sys.argv)

    filename = os.path.join(os.path.dirname(__file__), "pseas.db")
    create = not QFile.exists(filename)

    db = QSqlDatabase.addDatabase("QSQLITE")
    db.setDatabaseName(filename)
    if not db.open():
        QMessageBox.warning(None, "Asset Manager",
                            QString("Database Error: %1").arg(db.lastError().text()))
        sys.exit(1)
    app.setOverrideCursor(QCursor(Qt.WaitCursor))
    app.processEvents()
    if create:
        files = [u'./datafiles/aaa.xls']
        createData(files)
    else:
        files = ['./datafiles/bbb.xls']
        #       createData(files)
        insertData(files)
    app.exec_()
    del db
    sys.exit(1)


main()
