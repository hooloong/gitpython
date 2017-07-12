# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'DrawMap_res.ui'
#
# Created: Wed Jul 12 15:08:16 2017
#      by: PyQt4 UI code generator 4.9.6
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

class Ui_Form_MLut(object):
    def setupUi(self, Form_MLut):
        Form_MLut.setObjectName(_fromUtf8("Form_MLut"))
        Form_MLut.resize(1187, 708)
        self.tableWidget_lg = QtGui.QTableWidget(Form_MLut)
        self.tableWidget_lg.setGeometry(QtCore.QRect(10, 10, 391, 261))
        self.tableWidget_lg.setRowCount(8)
        self.tableWidget_lg.setColumnCount(8)
        self.tableWidget_lg.setObjectName(_fromUtf8("tableWidget_lg"))
        self.tableWidget_lg.horizontalHeader().setVisible(False)
        self.tableWidget_lg.horizontalHeader().setDefaultSectionSize(45)
        self.tableWidget_lg.horizontalHeader().setHighlightSections(False)
        self.tableWidget_lg.horizontalHeader().setMinimumSectionSize(21)
        self.tableWidget_lg.verticalHeader().setVisible(False)
        self.gridLayoutWidget = QtGui.QWidget(Form_MLut)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(30, 360, 161, 80))
        self.gridLayoutWidget.setObjectName(_fromUtf8("gridLayoutWidget"))
        self.gridLayout = QtGui.QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setMargin(0)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.pushButton_refresh = QtGui.QPushButton(self.gridLayoutWidget)
        self.pushButton_refresh.setObjectName(_fromUtf8("pushButton_refresh"))
        self.gridLayout.addWidget(self.pushButton_refresh, 0, 0, 1, 1)
        self.pushButton_generate = QtGui.QPushButton(self.gridLayoutWidget)
        self.pushButton_generate.setObjectName(_fromUtf8("pushButton_generate"))
        self.gridLayout.addWidget(self.pushButton_generate, 1, 0, 1, 1)
        self.pushButton_write = QtGui.QPushButton(self.gridLayoutWidget)
        self.pushButton_write.setObjectName(_fromUtf8("pushButton_write"))
        self.gridLayout.addWidget(self.pushButton_write, 0, 1, 1, 1)
        self.pushButton_read = QtGui.QPushButton(self.gridLayoutWidget)
        self.pushButton_read.setObjectName(_fromUtf8("pushButton_read"))
        self.gridLayout.addWidget(self.pushButton_read, 1, 1, 1, 1)
        self.label_1 = QtGui.QLabel(Form_MLut)
        self.label_1.setGeometry(QtCore.QRect(30, 310, 81, 16))
        self.label_1.setObjectName(_fromUtf8("label_1"))
        self.label_2 = QtGui.QLabel(Form_MLut)
        self.label_2.setGeometry(QtCore.QRect(230, 310, 54, 12))
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.gridLayoutWidget_2 = QtGui.QWidget(Form_MLut)
        self.gridLayoutWidget_2.setGeometry(QtCore.QRect(430, 10, 741, 681))
        self.gridLayoutWidget_2.setObjectName(_fromUtf8("gridLayoutWidget_2"))
        self.gridLayout_2 = QtGui.QGridLayout(self.gridLayoutWidget_2)
        self.gridLayout_2.setMargin(0)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.comboBox = QtGui.QComboBox(Form_MLut)
        self.comboBox.setGeometry(QtCore.QRect(120, 310, 69, 22))
        self.comboBox.setObjectName(_fromUtf8("comboBox"))
        self.comboBox.addItem(_fromUtf8(""))
        self.comboBox.addItem(_fromUtf8(""))
        self.comboBox.addItem(_fromUtf8(""))
        self.comboBox.addItem(_fromUtf8(""))

        self.retranslateUi(Form_MLut)
        QtCore.QMetaObject.connectSlotsByName(Form_MLut)

    def retranslateUi(self, Form_MLut):
        Form_MLut.setWindowTitle(_translate("Form_MLut", "Form_Hist", None))
        self.pushButton_refresh.setText(_translate("Form_MLut", "Refresh", None))
        self.pushButton_generate.setText(_translate("Form_MLut", "Generate!", None))
        self.pushButton_write.setText(_translate("Form_MLut", "WriteToChip", None))
        self.pushButton_read.setText(_translate("Form_MLut", "ReadFromChip", None))
        self.label_1.setText(_translate("Form_MLut", "TestmodeSelect", None))
        self.label_2.setText(_translate("Form_MLut", "TextLabel", None))
        self.comboBox.setItemText(0, _translate("Form_MLut", "Normal", None))
        self.comboBox.setItemText(1, _translate("Form_MLut", "SetToZeroAll", None))
        self.comboBox.setItemText(2, _translate("Form_MLut", "SetAllTo_63", None))
        self.comboBox.setItemText(3, _translate("Form_MLut", "SetBinaryToAll", None))

