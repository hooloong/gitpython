# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Drawlg_res.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_Form_Hist(object):
    def setupUi(self, Form_Hist):
        Form_Hist.setObjectName(_fromUtf8("Form_Hist"))
        Form_Hist.resize(1187, 708)
        self.tableWidget_lg = QtGui.QTableWidget(Form_Hist)
        self.tableWidget_lg.setGeometry(QtCore.QRect(790, 10, 391, 261))
        self.tableWidget_lg.setRowCount(8)
        self.tableWidget_lg.setColumnCount(8)
        self.tableWidget_lg.setObjectName(_fromUtf8("tableWidget_lg"))
        self.tableWidget_lg.horizontalHeader().setVisible(False)
        self.tableWidget_lg.horizontalHeader().setDefaultSectionSize(45)
        self.tableWidget_lg.horizontalHeader().setHighlightSections(False)
        self.tableWidget_lg.horizontalHeader().setMinimumSectionSize(21)
        self.tableWidget_lg.verticalHeader().setVisible(False)
        self.gridLayoutWidget = QtGui.QWidget(Form_Hist)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(880, 400, 160, 80))
        self.gridLayoutWidget.setObjectName(_fromUtf8("gridLayoutWidget"))
        self.gridLayout = QtGui.QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.pushButton_refresh = QtGui.QPushButton(self.gridLayoutWidget)
        self.pushButton_refresh.setObjectName(_fromUtf8("pushButton_refresh"))
        self.gridLayout.addWidget(self.pushButton_refresh, 0, 0, 1, 1)
        self.pushButton_1 = QtGui.QPushButton(self.gridLayoutWidget)
        self.pushButton_1.setObjectName(_fromUtf8("pushButton_1"))
        self.gridLayout.addWidget(self.pushButton_1, 1, 0, 1, 1)
        self.pushButton_2 = QtGui.QPushButton(self.gridLayoutWidget)
        self.pushButton_2.setObjectName(_fromUtf8("pushButton_2"))
        self.gridLayout.addWidget(self.pushButton_2, 0, 1, 1, 1)
        self.pushButton_3 = QtGui.QPushButton(self.gridLayoutWidget)
        self.pushButton_3.setObjectName(_fromUtf8("pushButton_3"))
        self.gridLayout.addWidget(self.pushButton_3, 1, 1, 1, 1)
        self.label_1 = QtGui.QLabel(Form_Hist)
        self.label_1.setGeometry(QtCore.QRect(800, 290, 54, 12))
        self.label_1.setObjectName(_fromUtf8("label_1"))
        self.label_2 = QtGui.QLabel(Form_Hist)
        self.label_2.setGeometry(QtCore.QRect(880, 290, 54, 12))
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.tabWidget = QtGui.QTabWidget(Form_Hist)
        self.tabWidget.setGeometry(QtCore.QRect(0, 0, 741, 701))
        self.tabWidget.setTabPosition(QtGui.QTabWidget.South)
        self.tabWidget.setObjectName(_fromUtf8("tabWidget"))
        self.tab = QtGui.QWidget()
        self.tab.setObjectName(_fromUtf8("tab"))
        self.tabWidget.addTab(self.tab, _fromUtf8(""))
        self.tab_2 = QtGui.QWidget()
        self.tab_2.setObjectName(_fromUtf8("tab_2"))
        self.tabWidget.addTab(self.tab_2, _fromUtf8(""))

        self.retranslateUi(Form_Hist)
        self.tabWidget.setCurrentIndex(1)
        QtCore.QMetaObject.connectSlotsByName(Form_Hist)

    def retranslateUi(self, Form_Hist):
        Form_Hist.setWindowTitle(_translate("Form_Hist", "Form_Hist", None))
        self.pushButton_refresh.setText(_translate("Form_Hist", "Refresh", None))
        self.pushButton_1.setText(_translate("Form_Hist", "PushButton", None))
        self.pushButton_2.setText(_translate("Form_Hist", "PushButton", None))
        self.pushButton_3.setText(_translate("Form_Hist", "PushButton", None))
        self.label_1.setText(_translate("Form_Hist", "TextLabel", None))
        self.label_2.setText(_translate("Form_Hist", "TextLabel", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("Form_Hist", "Tab 1", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("Form_Hist", "Tab 2", None))
