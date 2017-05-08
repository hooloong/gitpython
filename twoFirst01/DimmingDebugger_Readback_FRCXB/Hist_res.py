# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Hist_res.ui'
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
        Form_Hist.resize(870, 708)
        self.tableWidget_Hist = QtGui.QTableWidget(Form_Hist)
        self.tableWidget_Hist.setGeometry(QtCore.QRect(10, 20, 362, 242))
        self.tableWidget_Hist.setRowCount(8)
        self.tableWidget_Hist.setColumnCount(8)
        self.tableWidget_Hist.setObjectName(_fromUtf8("tableWidget_Hist"))
        self.tableWidget_Hist.horizontalHeader().setVisible(False)
        self.tableWidget_Hist.horizontalHeader().setDefaultSectionSize(45)
        self.tableWidget_Hist.horizontalHeader().setHighlightSections(False)
        self.tableWidget_Hist.horizontalHeader().setMinimumSectionSize(21)
        self.tableWidget_Hist.verticalHeader().setVisible(False)
        self.graphicsView_Hist = QtGui.QGraphicsView(Form_Hist)
        self.graphicsView_Hist.setGeometry(QtCore.QRect(10, 310, 831, 321))
        self.graphicsView_Hist.setObjectName(_fromUtf8("graphicsView_Hist"))
        self.pushButton_readHist = QtGui.QPushButton(Form_Hist)
        self.pushButton_readHist.setGeometry(QtCore.QRect(460, 50, 91, 31))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.pushButton_readHist.setFont(font)
        self.pushButton_readHist.setObjectName(_fromUtf8("pushButton_readHist"))
        self.spinBox_HistDataSelect = QtGui.QSpinBox(Form_Hist)
        self.spinBox_HistDataSelect.setGeometry(QtCore.QRect(580, 50, 61, 29))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.spinBox_HistDataSelect.setFont(font)
        self.spinBox_HistDataSelect.setObjectName(_fromUtf8("spinBox_HistDataSelect"))
        self.label = QtGui.QLabel(Form_Hist)
        self.label.setGeometry(QtCore.QRect(650, 50, 91, 31))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setObjectName(_fromUtf8("label"))

        self.retranslateUi(Form_Hist)
        QtCore.QMetaObject.connectSlotsByName(Form_Hist)

    def retranslateUi(self, Form_Hist):
        Form_Hist.setWindowTitle(_translate("Form_Hist", "Form_Hist", None))
        self.pushButton_readHist.setText(_translate("Form_Hist", "ReadHist", None))
        self.label.setText(_translate("Form_Hist", "Hist Index:", None))

