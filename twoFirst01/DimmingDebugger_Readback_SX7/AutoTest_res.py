# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'AutoTest_res.ui'
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

class Ui_Form_Autotest(object):
    def setupUi(self, Form_Autotest):
        Form_Autotest.setObjectName(_fromUtf8("Form_Autotest"))
        Form_Autotest.resize(870, 708)
        self.pushButton_start = QtGui.QPushButton(Form_Autotest)
        self.pushButton_start.setGeometry(QtCore.QRect(420, 50, 91, 31))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.pushButton_start.setFont(font)
        self.pushButton_start.setObjectName(_fromUtf8("pushButton_start"))
        self.gridLayoutWidget = QtGui.QWidget(Form_Autotest)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(20, 30, 160, 131))
        self.gridLayoutWidget.setObjectName(_fromUtf8("gridLayoutWidget"))
        self.gridLayout = QtGui.QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.comboBox_source = QtGui.QComboBox(self.gridLayoutWidget)
        self.comboBox_source.setObjectName(_fromUtf8("comboBox_source"))
        self.gridLayout.addWidget(self.comboBox_source, 0, 1, 1, 1)
        self.label_source = QtGui.QLabel(self.gridLayoutWidget)
        self.label_source.setObjectName(_fromUtf8("label_source"))
        self.gridLayout.addWidget(self.label_source, 0, 0, 1, 1)
        self.comboBox_signal = QtGui.QComboBox(self.gridLayoutWidget)
        self.comboBox_signal.setObjectName(_fromUtf8("comboBox_signal"))
        self.gridLayout.addWidget(self.comboBox_signal, 1, 1, 1, 1)
        self.label_delay = QtGui.QLabel(self.gridLayoutWidget)
        self.label_delay.setObjectName(_fromUtf8("label_delay"))
        self.gridLayout.addWidget(self.label_delay, 2, 0, 1, 1)
        self.spinBox_delay = QtGui.QSpinBox(self.gridLayoutWidget)
        self.spinBox_delay.setObjectName(_fromUtf8("spinBox_delay"))
        self.gridLayout.addWidget(self.spinBox_delay, 2, 1, 1, 1)
        self.label_2 = QtGui.QLabel(self.gridLayoutWidget)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)
        self.gridLayoutWidget_2 = QtGui.QWidget(Form_Autotest)
        self.gridLayoutWidget_2.setGeometry(QtCore.QRect(200, 30, 169, 131))
        self.gridLayoutWidget_2.setObjectName(_fromUtf8("gridLayoutWidget_2"))
        self.gridLayout_2 = QtGui.QGridLayout(self.gridLayoutWidget_2)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.comboBox_source_2 = QtGui.QComboBox(self.gridLayoutWidget_2)
        self.comboBox_source_2.setObjectName(_fromUtf8("comboBox_source_2"))
        self.gridLayout_2.addWidget(self.comboBox_source_2, 0, 1, 1, 1)
        self.label_3 = QtGui.QLabel(self.gridLayoutWidget_2)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.gridLayout_2.addWidget(self.label_3, 1, 0, 1, 1)
        self.label_delay_2 = QtGui.QLabel(self.gridLayoutWidget_2)
        self.label_delay_2.setObjectName(_fromUtf8("label_delay_2"))
        self.gridLayout_2.addWidget(self.label_delay_2, 2, 0, 1, 1)
        self.spinBox_delay_2 = QtGui.QSpinBox(self.gridLayoutWidget_2)
        self.spinBox_delay_2.setObjectName(_fromUtf8("spinBox_delay_2"))
        self.gridLayout_2.addWidget(self.spinBox_delay_2, 2, 1, 1, 1)
        self.comboBox_signal_2 = QtGui.QComboBox(self.gridLayoutWidget_2)
        self.comboBox_signal_2.setObjectName(_fromUtf8("comboBox_signal_2"))
        self.gridLayout_2.addWidget(self.comboBox_signal_2, 1, 1, 1, 1)
        self.label_source_2 = QtGui.QLabel(self.gridLayoutWidget_2)
        self.label_source_2.setObjectName(_fromUtf8("label_source_2"))
        self.gridLayout_2.addWidget(self.label_source_2, 0, 0, 1, 1)
        self.label_11 = QtGui.QLabel(Form_Autotest)
        self.label_11.setGeometry(QtCore.QRect(20, 0, 151, 16))
        self.label_11.setObjectName(_fromUtf8("label_11"))
        self.label_22 = QtGui.QLabel(Form_Autotest)
        self.label_22.setGeometry(QtCore.QRect(200, 0, 111, 16))
        self.label_22.setObjectName(_fromUtf8("label_22"))
        self.label_current = QtGui.QLabel(Form_Autotest)
        self.label_current.setGeometry(QtCore.QRect(20, 180, 141, 16))
        self.label_current.setObjectName(_fromUtf8("label_current"))
        self.lineEdit_currentsource = QtGui.QLineEdit(Form_Autotest)
        self.lineEdit_currentsource.setGeometry(QtCore.QRect(150, 180, 221, 20))
        self.lineEdit_currentsource.setObjectName(_fromUtf8("lineEdit_currentsource"))

        self.retranslateUi(Form_Autotest)
        QtCore.QMetaObject.connectSlotsByName(Form_Autotest)

    def retranslateUi(self, Form_Autotest):
        Form_Autotest.setWindowTitle(_translate("Form_Autotest", "Form_Autotest", None))
        self.pushButton_start.setText(_translate("Form_Autotest", "StartTest", None))
        self.label_source.setText(_translate("Form_Autotest", "Source:", None))
        self.label_delay.setText(_translate("Form_Autotest", "DelayTime", None))
        self.label_2.setText(_translate("Form_Autotest", "Signal:", None))
        self.label_3.setText(_translate("Form_Autotest", "Signal:", None))
        self.label_delay_2.setText(_translate("Form_Autotest", "DelayTime", None))
        self.label_source_2.setText(_translate("Form_Autotest", "Source:", None))
        self.label_11.setText(_translate("Form_Autotest", "Source_No_1", None))
        self.label_22.setText(_translate("Form_Autotest", "Source_No_2", None))
        self.label_current.setText(_translate("Form_Autotest", "Current Source Change:", None))

