# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Info_res.ui'
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

class Ui_Form_Info(object):
    def setupUi(self, Form_Info):
        Form_Info.setObjectName(_fromUtf8("Form_Info"))
        Form_Info.resize(870, 600)
        self.lineEdit_MainTSE = QtGui.QLineEdit(Form_Info)
        self.lineEdit_MainTSE.setGeometry(QtCore.QRect(110, 90, 105, 20))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.lineEdit_MainTSE.setFont(font)
        self.lineEdit_MainTSE.setReadOnly(True)
        self.lineEdit_MainTSE.setObjectName(_fromUtf8("lineEdit_MainTSE"))
        self.label = QtGui.QLabel(Form_Info)
        self.label.setGeometry(QtCore.QRect(60, 95, 54, 12))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label.setFont(font)
        self.label.setObjectName(_fromUtf8("label"))
        self.lineEdit_PQMainTSE = QtGui.QLineEdit(Form_Info)
        self.lineEdit_PQMainTSE.setGeometry(QtCore.QRect(300, 90, 105, 20))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.lineEdit_PQMainTSE.setFont(font)
        self.lineEdit_PQMainTSE.setReadOnly(True)
        self.lineEdit_PQMainTSE.setObjectName(_fromUtf8("lineEdit_PQMainTSE"))
        self.label_2 = QtGui.QLabel(Form_Info)
        self.label_2.setGeometry(QtCore.QRect(240, 90, 71, 20))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_2.setFont(font)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.lineEdit_AttributeTSE = QtGui.QLineEdit(Form_Info)
        self.lineEdit_AttributeTSE.setGeometry(QtCore.QRect(500, 90, 105, 20))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.lineEdit_AttributeTSE.setFont(font)
        self.lineEdit_AttributeTSE.setReadOnly(True)
        self.lineEdit_AttributeTSE.setObjectName(_fromUtf8("lineEdit_AttributeTSE"))
        self.label_3 = QtGui.QLabel(Form_Info)
        self.label_3.setGeometry(QtCore.QRect(430, 90, 71, 20))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_3.setFont(font)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.lineEdit_TableTSE = QtGui.QLineEdit(Form_Info)
        self.lineEdit_TableTSE.setGeometry(QtCore.QRect(110, 140, 105, 20))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.lineEdit_TableTSE.setFont(font)
        self.lineEdit_TableTSE.setReadOnly(True)
        self.lineEdit_TableTSE.setObjectName(_fromUtf8("lineEdit_TableTSE"))
        self.label_4 = QtGui.QLabel(Form_Info)
        self.label_4.setGeometry(QtCore.QRect(60, 140, 71, 20))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_4.setFont(font)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.groupBox = QtGui.QGroupBox(Form_Info)
        self.groupBox.setGeometry(QtCore.QRect(50, 60, 601, 121))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        self.groupBox.setFont(font)
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.label_6 = QtGui.QLabel(self.groupBox)
        self.label_6.setGeometry(QtCore.QRect(190, 80, 71, 20))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        self.label_6.setFont(font)
        self.label_6.setObjectName(_fromUtf8("label_6"))
        self.lineEdit_PQCustomTSE = QtGui.QLineEdit(self.groupBox)
        self.lineEdit_PQCustomTSE.setGeometry(QtCore.QRect(250, 80, 105, 20))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.lineEdit_PQCustomTSE.setFont(font)
        self.lineEdit_PQCustomTSE.setReadOnly(True)
        self.lineEdit_PQCustomTSE.setObjectName(_fromUtf8("lineEdit_PQCustomTSE"))
        self.lineEdit_PQPanelTSE = QtGui.QLineEdit(self.groupBox)
        self.lineEdit_PQPanelTSE.setGeometry(QtCore.QRect(450, 80, 105, 20))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.lineEdit_PQPanelTSE.setFont(font)
        self.lineEdit_PQPanelTSE.setReadOnly(True)
        self.lineEdit_PQPanelTSE.setObjectName(_fromUtf8("lineEdit_PQPanelTSE"))
        self.label_5 = QtGui.QLabel(self.groupBox)
        self.label_5.setGeometry(QtCore.QRect(380, 80, 71, 20))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        self.label_5.setFont(font)
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.lineEdit_PanelID = QtGui.QLineEdit(Form_Info)
        self.lineEdit_PanelID.setGeometry(QtCore.QRect(90, 230, 105, 20))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.lineEdit_PanelID.setFont(font)
        self.lineEdit_PanelID.setReadOnly(True)
        self.lineEdit_PanelID.setObjectName(_fromUtf8("lineEdit_PanelID"))
        self.groupBox_2 = QtGui.QGroupBox(Form_Info)
        self.groupBox_2.setGeometry(QtCore.QRect(50, 200, 171, 71))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.groupBox_2.setFont(font)
        self.groupBox_2.setObjectName(_fromUtf8("groupBox_2"))
        self.pushButton_read = QtGui.QPushButton(Form_Info)
        self.pushButton_read.setGeometry(QtCore.QRect(670, 500, 71, 41))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.pushButton_read.setFont(font)
        self.pushButton_read.setObjectName(_fromUtf8("pushButton_read"))
        self.groupBox.raise_()
        self.groupBox_2.raise_()
        self.lineEdit_MainTSE.raise_()
        self.label.raise_()
        self.lineEdit_PQMainTSE.raise_()
        self.label_2.raise_()
        self.lineEdit_AttributeTSE.raise_()
        self.label_3.raise_()
        self.lineEdit_TableTSE.raise_()
        self.label_4.raise_()
        self.lineEdit_PanelID.raise_()
        self.pushButton_read.raise_()

        self.retranslateUi(Form_Info)
        QtCore.QMetaObject.connectSlotsByName(Form_Info)

    def retranslateUi(self, Form_Info):
        Form_Info.setWindowTitle(_translate("Form_Info", "Form", None))
        self.label.setText(_translate("Form_Info", "Main", None))
        self.label_2.setText(_translate("Form_Info", "PQMain", None))
        self.label_3.setText(_translate("Form_Info", "Attribute", None))
        self.label_4.setText(_translate("Form_Info", "Table", None))
        self.groupBox.setTitle(_translate("Form_Info", "TSE_Version", None))
        self.label_6.setText(_translate("Form_Info", "PQCustom", None))
        self.label_5.setText(_translate("Form_Info", "PQPanel", None))
        self.groupBox_2.setTitle(_translate("Form_Info", "PanelID", None))
        self.pushButton_read.setText(_translate("Form_Info", "Read", None))

