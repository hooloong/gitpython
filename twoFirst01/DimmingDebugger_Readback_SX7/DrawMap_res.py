# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'DrawMap_res.ui'
#
# Created: Wed Jul 12 18:35:34 2017
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

class Ui_Form_mLut(object):
    def setupUi(self, Form_mLut):
        Form_mLut.setObjectName(_fromUtf8("Form_mLut"))
        Form_mLut.resize(1187, 708)
        self.tableWidget_mlut = QtGui.QTableWidget(Form_mLut)
        self.tableWidget_mlut.setGeometry(QtCore.QRect(10, 10, 391, 261))
        self.tableWidget_mlut.setRowCount(8)
        self.tableWidget_mlut.setColumnCount(8)
        self.tableWidget_mlut.setObjectName(_fromUtf8("tableWidget_mlut"))
        self.tableWidget_mlut.horizontalHeader().setVisible(False)
        self.tableWidget_mlut.horizontalHeader().setDefaultSectionSize(45)
        self.tableWidget_mlut.horizontalHeader().setHighlightSections(False)
        self.tableWidget_mlut.horizontalHeader().setMinimumSectionSize(21)
        self.tableWidget_mlut.verticalHeader().setVisible(False)
        self.gridLayoutWidget = QtGui.QWidget(Form_mLut)
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
        self.label_1 = QtGui.QLabel(Form_mLut)
        self.label_1.setGeometry(QtCore.QRect(30, 310, 81, 16))
        self.label_1.setObjectName(_fromUtf8("label_1"))
        self.label_2 = QtGui.QLabel(Form_mLut)
        self.label_2.setGeometry(QtCore.QRect(240, 310, 54, 12))
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.gridLayoutWidget_2 = QtGui.QWidget(Form_mLut)
        self.gridLayoutWidget_2.setGeometry(QtCore.QRect(430, 10, 741, 681))
        self.gridLayoutWidget_2.setObjectName(_fromUtf8("gridLayoutWidget_2"))
        self.gridLayout_2 = QtGui.QGridLayout(self.gridLayoutWidget_2)
        self.gridLayout_2.setMargin(0)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.comboBox_test = QtGui.QComboBox(Form_mLut)
        self.comboBox_test.setGeometry(QtCore.QRect(120, 310, 101, 22))
        self.comboBox_test.setObjectName(_fromUtf8("comboBox_test"))
        self.comboBox_test.addItem(_fromUtf8(""))
        self.comboBox_test.addItem(_fromUtf8(""))
        self.comboBox_test.addItem(_fromUtf8(""))
        self.comboBox_test.addItem(_fromUtf8(""))

        self.retranslateUi(Form_mLut)
        QtCore.QMetaObject.connectSlotsByName(Form_mLut)

    def retranslateUi(self, Form_mLut):
        Form_mLut.setWindowTitle(_translate("Form_mLut", "Form_mLut", None))
        self.pushButton_refresh.setText(_translate("Form_mLut", "Refresh", None))
        self.pushButton_generate.setText(_translate("Form_mLut", "Generate!", None))
        self.pushButton_write.setText(_translate("Form_mLut", "WriteToChip", None))
        self.pushButton_read.setText(_translate("Form_mLut", "ReadFromChip", None))
        self.label_1.setText(_translate("Form_mLut", "TestmodeSelect", None))
        self.label_2.setText(_translate("Form_mLut", "TextLabel", None))
        self.comboBox_test.setItemText(0, _translate("Form_mLut", "Normal", None))
        self.comboBox_test.setItemText(1, _translate("Form_mLut", "SetToZeroAll", None))
        self.comboBox_test.setItemText(2, _translate("Form_mLut", "SetAllTo_63", None))
        self.comboBox_test.setItemText(3, _translate("Form_mLut", "SetBinaryToAll", None))

