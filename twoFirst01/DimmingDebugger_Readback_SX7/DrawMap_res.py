# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'DrawMap_res.ui'
#
# Created: Wed Jul 19 14:11:37 2017
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
        self.tableWidget_mlut.setGeometry(QtCore.QRect(10, 10, 371, 251))
        self.tableWidget_mlut.setRowCount(8)
        self.tableWidget_mlut.setColumnCount(8)
        self.tableWidget_mlut.setObjectName(_fromUtf8("tableWidget_mlut"))
        self.tableWidget_mlut.horizontalHeader().setVisible(False)
        self.tableWidget_mlut.horizontalHeader().setDefaultSectionSize(45)
        self.tableWidget_mlut.horizontalHeader().setHighlightSections(False)
        self.tableWidget_mlut.horizontalHeader().setMinimumSectionSize(21)
        self.tableWidget_mlut.verticalHeader().setVisible(False)
        self.gridLayoutWidget = QtGui.QWidget(Form_mLut)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(10, 330, 323, 83))
        self.gridLayoutWidget.setObjectName(_fromUtf8("gridLayoutWidget"))
        self.gridLayout = QtGui.QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setMargin(0)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.pushButton_write = QtGui.QPushButton(self.gridLayoutWidget)
        self.pushButton_write.setObjectName(_fromUtf8("pushButton_write"))
        self.gridLayout.addWidget(self.pushButton_write, 0, 1, 1, 1)
        self.pushButton_output = QtGui.QPushButton(self.gridLayoutWidget)
        self.pushButton_output.setObjectName(_fromUtf8("pushButton_output"))
        self.gridLayout.addWidget(self.pushButton_output, 3, 4, 1, 1)
        self.pushButton_read = QtGui.QPushButton(self.gridLayoutWidget)
        self.pushButton_read.setObjectName(_fromUtf8("pushButton_read"))
        self.gridLayout.addWidget(self.pushButton_read, 3, 1, 1, 1)
        self.pushButton_draw = QtGui.QPushButton(self.gridLayoutWidget)
        self.pushButton_draw.setObjectName(_fromUtf8("pushButton_draw"))
        self.gridLayout.addWidget(self.pushButton_draw, 0, 4, 1, 1)
        self.pushButton_convert = QtGui.QPushButton(self.gridLayoutWidget)
        self.pushButton_convert.setObjectName(_fromUtf8("pushButton_convert"))
        self.gridLayout.addWidget(self.pushButton_convert, 0, 2, 1, 1)
        self.pushButton_refresh = QtGui.QPushButton(self.gridLayoutWidget)
        self.pushButton_refresh.setObjectName(_fromUtf8("pushButton_refresh"))
        self.gridLayout.addWidget(self.pushButton_refresh, 3, 2, 1, 1)
        self.pushButton_load = QtGui.QPushButton(self.gridLayoutWidget)
        self.pushButton_load.setObjectName(_fromUtf8("pushButton_load"))
        self.gridLayout.addWidget(self.pushButton_load, 0, 3, 1, 1)
        self.pushButton_save = QtGui.QPushButton(self.gridLayoutWidget)
        self.pushButton_save.setObjectName(_fromUtf8("pushButton_save"))
        self.gridLayout.addWidget(self.pushButton_save, 3, 3, 1, 1)
        self.gridLayoutWidget_2 = QtGui.QWidget(Form_mLut)
        self.gridLayoutWidget_2.setGeometry(QtCore.QRect(400, 10, 741, 681))
        self.gridLayoutWidget_2.setObjectName(_fromUtf8("gridLayoutWidget_2"))
        self.gridLayout_2 = QtGui.QGridLayout(self.gridLayoutWidget_2)
        self.gridLayout_2.setMargin(0)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.plainTextEdit_output = QtGui.QPlainTextEdit(Form_mLut)
        self.plainTextEdit_output.setGeometry(QtCore.QRect(10, 420, 371, 271))
        self.plainTextEdit_output.setObjectName(_fromUtf8("plainTextEdit_output"))
        self.horizontalLayoutWidget = QtGui.QWidget(Form_mLut)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(10, 280, 259, 41))
        self.horizontalLayoutWidget.setObjectName(_fromUtf8("horizontalLayoutWidget"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setMargin(0)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.label_1 = QtGui.QLabel(self.horizontalLayoutWidget)
        self.label_1.setObjectName(_fromUtf8("label_1"))
        self.horizontalLayout.addWidget(self.label_1)
        self.comboBox_test = QtGui.QComboBox(self.horizontalLayoutWidget)
        self.comboBox_test.setObjectName(_fromUtf8("comboBox_test"))
        self.comboBox_test.addItem(_fromUtf8(""))
        self.comboBox_test.addItem(_fromUtf8(""))
        self.comboBox_test.addItem(_fromUtf8(""))
        self.comboBox_test.addItem(_fromUtf8(""))
        self.horizontalLayout.addWidget(self.comboBox_test)
        self.checkBox_en = QtGui.QCheckBox(self.horizontalLayoutWidget)
        self.checkBox_en.setObjectName(_fromUtf8("checkBox_en"))
        self.horizontalLayout.addWidget(self.checkBox_en)

        self.retranslateUi(Form_mLut)
        QtCore.QMetaObject.connectSlotsByName(Form_mLut)

    def retranslateUi(self, Form_mLut):
        Form_mLut.setWindowTitle(_translate("Form_mLut", "Form_mLut", None))
        self.pushButton_write.setText(_translate("Form_mLut", "WriteToChip", None))
        self.pushButton_output.setText(_translate("Form_mLut", "OutputMlut", None))
        self.pushButton_read.setText(_translate("Form_mLut", "ReadFromChip", None))
        self.pushButton_draw.setText(_translate("Form_mLut", "DrawIt!", None))
        self.pushButton_convert.setText(_translate("Form_mLut", "EditorConv", None))
        self.pushButton_refresh.setText(_translate("Form_mLut", "Refresh", None))
        self.pushButton_load.setText(_translate("Form_mLut", "loadFromFile", None))
        self.pushButton_save.setText(_translate("Form_mLut", "SaveToFile", None))
        self.label_1.setText(_translate("Form_mLut", "TestingData:", None))
        self.comboBox_test.setItemText(0, _translate("Form_mLut", "Normal", None))
        self.comboBox_test.setItemText(1, _translate("Form_mLut", "SetToZeroAll", None))
        self.comboBox_test.setItemText(2, _translate("Form_mLut", "SetAllTo_63", None))
        self.comboBox_test.setItemText(3, _translate("Form_mLut", "SetBinaryToAll", None))
        self.checkBox_en.setText(_translate("Form_mLut", "Enable M_LUT", None))

