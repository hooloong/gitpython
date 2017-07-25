# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Hist_Bin0_res.ui'
#
# Created: Tue Jul 25 18:08:35 2017
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
        self.graphicsView_Hist.setGeometry(QtCore.QRect(30, 410, 831, 251))
        self.graphicsView_Hist.setObjectName(_fromUtf8("graphicsView_Hist"))
        self.horizontalLayoutWidget = QtGui.QWidget(Form_Hist)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(30, 310, 301, 51))
        self.horizontalLayoutWidget.setObjectName(_fromUtf8("horizontalLayoutWidget"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setMargin(0)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.label = QtGui.QLabel(self.horizontalLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setObjectName(_fromUtf8("label"))
        self.horizontalLayout.addWidget(self.label)
        self.spinBox_HistDataSelect = QtGui.QSpinBox(self.horizontalLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.spinBox_HistDataSelect.setFont(font)
        self.spinBox_HistDataSelect.setMinimum(128)
        self.spinBox_HistDataSelect.setMaximum(512)
        self.spinBox_HistDataSelect.setSingleStep(16)
        self.spinBox_HistDataSelect.setObjectName(_fromUtf8("spinBox_HistDataSelect"))
        self.horizontalLayout.addWidget(self.spinBox_HistDataSelect)
        self.pushButton_readHist = QtGui.QPushButton(self.horizontalLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.pushButton_readHist.setFont(font)
        self.pushButton_readHist.setObjectName(_fromUtf8("pushButton_readHist"))
        self.horizontalLayout.addWidget(self.pushButton_readHist)

        self.retranslateUi(Form_Hist)
        QtCore.QMetaObject.connectSlotsByName(Form_Hist)

    def retranslateUi(self, Form_Hist):
        Form_Hist.setWindowTitle(_translate("Form_Hist", "Form_Hist", None))
        self.label.setText(_translate("Form_Hist", "Total Hist:", None))
        self.pushButton_readHist.setText(_translate("Form_Hist", "ReadBin0", None))

