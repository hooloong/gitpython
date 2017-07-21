# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'DrawMapNew_res.ui'
#
# Created: Fri Jul 21 15:47:01 2017
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
        Form_mLut.resize(1072, 708)
        self.tableWidget_mlut = QtGui.QTableWidget(Form_mLut)
        self.tableWidget_mlut.setGeometry(QtCore.QRect(10, 10, 371, 261))
        self.tableWidget_mlut.setRowCount(8)
        self.tableWidget_mlut.setColumnCount(8)
        self.tableWidget_mlut.setObjectName(_fromUtf8("tableWidget_mlut"))
        self.tableWidget_mlut.horizontalHeader().setVisible(False)
        self.tableWidget_mlut.horizontalHeader().setDefaultSectionSize(45)
        self.tableWidget_mlut.horizontalHeader().setHighlightSections(False)
        self.tableWidget_mlut.horizontalHeader().setMinimumSectionSize(21)
        self.tableWidget_mlut.verticalHeader().setVisible(False)
        self.plainTextEdit_output = QtGui.QPlainTextEdit(Form_mLut)
        self.plainTextEdit_output.setGeometry(QtCore.QRect(660, 10, 391, 261))
        self.plainTextEdit_output.setObjectName(_fromUtf8("plainTextEdit_output"))
        self.graphicsView_mlut = QtGui.QGraphicsView(Form_mLut)
        self.graphicsView_mlut.setGeometry(QtCore.QRect(10, 300, 1040, 400))
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        self.graphicsView_mlut.setBackgroundBrush(brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0, 0))
        brush.setStyle(QtCore.Qt.NoBrush)
        self.graphicsView_mlut.setForegroundBrush(brush)
        self.graphicsView_mlut.setInteractive(True)
        self.graphicsView_mlut.setObjectName(_fromUtf8("graphicsView_mlut"))
        self.gridLayoutWidget_2 = QtGui.QWidget(Form_mLut)
        self.gridLayoutWidget_2.setGeometry(QtCore.QRect(400, 10, 242, 261))
        self.gridLayoutWidget_2.setObjectName(_fromUtf8("gridLayoutWidget_2"))
        self.gridLayout_2 = QtGui.QGridLayout(self.gridLayoutWidget_2)
        self.gridLayout_2.setMargin(0)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.checkBox_en = QtGui.QCheckBox(self.gridLayoutWidget_2)
        self.checkBox_en.setObjectName(_fromUtf8("checkBox_en"))
        self.gridLayout_2.addWidget(self.checkBox_en, 1, 0, 1, 1)
        self.pushButton_output = QtGui.QPushButton(self.gridLayoutWidget_2)
        self.pushButton_output.setObjectName(_fromUtf8("pushButton_output"))
        self.gridLayout_2.addWidget(self.pushButton_output, 6, 1, 1, 1)
        self.pushButton_read = QtGui.QPushButton(self.gridLayoutWidget_2)
        self.pushButton_read.setObjectName(_fromUtf8("pushButton_read"))
        self.gridLayout_2.addWidget(self.pushButton_read, 3, 0, 1, 1)
        self.checkBox_toc = QtGui.QCheckBox(self.gridLayoutWidget_2)
        self.checkBox_toc.setObjectName(_fromUtf8("checkBox_toc"))
        self.gridLayout_2.addWidget(self.checkBox_toc, 1, 1, 1, 1)
        self.comboBox_test = QtGui.QComboBox(self.gridLayoutWidget_2)
        self.comboBox_test.setObjectName(_fromUtf8("comboBox_test"))
        self.comboBox_test.addItem(_fromUtf8(""))
        self.comboBox_test.addItem(_fromUtf8(""))
        self.comboBox_test.addItem(_fromUtf8(""))
        self.comboBox_test.addItem(_fromUtf8(""))
        self.gridLayout_2.addWidget(self.comboBox_test, 0, 1, 1, 1)
        self.pushButton_convert = QtGui.QPushButton(self.gridLayoutWidget_2)
        self.pushButton_convert.setObjectName(_fromUtf8("pushButton_convert"))
        self.gridLayout_2.addWidget(self.pushButton_convert, 2, 1, 1, 1)
        self.pushButton_load = QtGui.QPushButton(self.gridLayoutWidget_2)
        self.pushButton_load.setObjectName(_fromUtf8("pushButton_load"))
        self.gridLayout_2.addWidget(self.pushButton_load, 4, 0, 1, 1)
        self.pushButton_draw = QtGui.QPushButton(self.gridLayoutWidget_2)
        self.pushButton_draw.setObjectName(_fromUtf8("pushButton_draw"))
        self.gridLayout_2.addWidget(self.pushButton_draw, 6, 0, 1, 1)
        self.pushButton_write = QtGui.QPushButton(self.gridLayoutWidget_2)
        self.pushButton_write.setObjectName(_fromUtf8("pushButton_write"))
        self.gridLayout_2.addWidget(self.pushButton_write, 2, 0, 1, 1)
        self.pushButton_refresh = QtGui.QPushButton(self.gridLayoutWidget_2)
        self.pushButton_refresh.setObjectName(_fromUtf8("pushButton_refresh"))
        self.gridLayout_2.addWidget(self.pushButton_refresh, 3, 1, 1, 1)
        self.pushButton_save = QtGui.QPushButton(self.gridLayoutWidget_2)
        self.pushButton_save.setObjectName(_fromUtf8("pushButton_save"))
        self.gridLayout_2.addWidget(self.pushButton_save, 4, 1, 1, 1)
        self.label_1 = QtGui.QLabel(self.gridLayoutWidget_2)
        self.label_1.setObjectName(_fromUtf8("label_1"))
        self.gridLayout_2.addWidget(self.label_1, 0, 0, 1, 1)

        self.retranslateUi(Form_mLut)
        QtCore.QMetaObject.connectSlotsByName(Form_mLut)

    def retranslateUi(self, Form_mLut):
        Form_mLut.setWindowTitle(_translate("Form_mLut", "Form_mLut", None))
        self.checkBox_en.setText(_translate("Form_mLut", "Enable M_LUT", None))
        self.pushButton_output.setText(_translate("Form_mLut", "OutputMlut", None))
        self.pushButton_read.setText(_translate("Form_mLut", "ReadFromChip", None))
        self.checkBox_toc.setText(_translate("Form_mLut", "C-Format", None))
        self.comboBox_test.setItemText(0, _translate("Form_mLut", "Normal", None))
        self.comboBox_test.setItemText(1, _translate("Form_mLut", "SetToZeroAll", None))
        self.comboBox_test.setItemText(2, _translate("Form_mLut", "SetAllTo_63", None))
        self.comboBox_test.setItemText(3, _translate("Form_mLut", "SetBinaryToAll", None))
        self.pushButton_convert.setText(_translate("Form_mLut", "EditorConv", None))
        self.pushButton_load.setText(_translate("Form_mLut", "loadFromFile", None))
        self.pushButton_draw.setText(_translate("Form_mLut", "DrawIt!", None))
        self.pushButton_write.setText(_translate("Form_mLut", "WriteToChip", None))
        self.pushButton_refresh.setText(_translate("Form_mLut", "Refresh", None))
        self.pushButton_save.setText(_translate("Form_mLut", "SaveToFile", None))
        self.label_1.setText(_translate("Form_mLut", "TestingInitData:", None))

