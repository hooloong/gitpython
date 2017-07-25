# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Hist_Bin0_res.ui'
#
# Created: Tue Jul 25 19:16:09 2017
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

class Ui_Form_Hist(object):
    def setupUi(self, Form_Hist):
        Form_Hist.setObjectName(_fromUtf8("Form_Hist"))
        Form_Hist.resize(870, 708)
        self.tableWidget_Hist = QtGui.QTableWidget(Form_Hist)
        self.tableWidget_Hist.setGeometry(QtCore.QRect(30, 20, 831, 271))
        self.tableWidget_Hist.setRowCount(8)
        self.tableWidget_Hist.setColumnCount(16)
        self.tableWidget_Hist.setObjectName(_fromUtf8("tableWidget_Hist"))
        self.tableWidget_Hist.horizontalHeader().setVisible(True)
        self.tableWidget_Hist.horizontalHeader().setDefaultSectionSize(45)
        self.tableWidget_Hist.horizontalHeader().setHighlightSections(False)
        self.tableWidget_Hist.horizontalHeader().setMinimumSectionSize(21)
        self.tableWidget_Hist.verticalHeader().setVisible(True)
        self.tableWidget_Hist.verticalHeader().setCascadingSectionResizes(False)
        self.tableWidget_Hist.verticalHeader().setDefaultSectionSize(30)
        self.tableWidget_Hist.verticalHeader().setMinimumSectionSize(21)
        self.tableWidget_Hist.verticalHeader().setSortIndicatorShown(False)
        self.graphicsView_Hist = QtGui.QGraphicsView(Form_Hist)
        self.graphicsView_Hist.setGeometry(QtCore.QRect(30, 400, 831, 251))
        self.graphicsView_Hist.setObjectName(_fromUtf8("graphicsView_Hist"))
        self.gridLayoutWidget = QtGui.QWidget(Form_Hist)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(30, 300, 235, 91))
        self.gridLayoutWidget.setObjectName(_fromUtf8("gridLayoutWidget"))
        self.gridLayout = QtGui.QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setMargin(0)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.label = QtGui.QLabel(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.label_2 = QtGui.QLabel(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.label_2.setFont(font)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)
        self.spinBox_HistDataSelect = QtGui.QSpinBox(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.spinBox_HistDataSelect.setFont(font)
        self.spinBox_HistDataSelect.setMinimum(128)
        self.spinBox_HistDataSelect.setMaximum(512)
        self.spinBox_HistDataSelect.setSingleStep(16)
        self.spinBox_HistDataSelect.setObjectName(_fromUtf8("spinBox_HistDataSelect"))
        self.gridLayout.addWidget(self.spinBox_HistDataSelect, 0, 1, 1, 1)
        self.lineEdit = QtGui.QLineEdit(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.lineEdit.setFont(font)
        self.lineEdit.setMaxLength(5)
        self.lineEdit.setEchoMode(QtGui.QLineEdit.Normal)
        self.lineEdit.setObjectName(_fromUtf8("lineEdit"))
        self.gridLayout.addWidget(self.lineEdit, 1, 1, 1, 1)
        self.pushButton_readHist = QtGui.QPushButton(Form_Hist)
        self.pushButton_readHist.setGeometry(QtCore.QRect(290, 310, 111, 31))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.pushButton_readHist.setFont(font)
        self.pushButton_readHist.setObjectName(_fromUtf8("pushButton_readHist"))

        self.retranslateUi(Form_Hist)
        QtCore.QMetaObject.connectSlotsByName(Form_Hist)

    def retranslateUi(self, Form_Hist):
        Form_Hist.setWindowTitle(_translate("Form_Hist", "Form_Hist", None))
        self.label.setText(_translate("Form_Hist", "Total Hist:", None))
        self.label_2.setText(_translate("Form_Hist", "THR:", None))
        self.lineEdit.setText(_translate("Form_Hist", "FD20", None))
        self.pushButton_readHist.setText(_translate("Form_Hist", "ReadBin0", None))

