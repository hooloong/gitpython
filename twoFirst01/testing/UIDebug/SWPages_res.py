# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'SWPages_res.ui'
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

class Ui_Form_Pages(object):
    def setupUi(self, Form_Pages):
        Form_Pages.setObjectName(_fromUtf8("Form_Pages"))
        Form_Pages.resize(960, 700)
        self.tableWidget_curpage = QtGui.QTableWidget(Form_Pages)
        self.tableWidget_curpage.setGeometry(QtCore.QRect(180, 0, 601, 507))
        self.tableWidget_curpage.setEditTriggers(QtGui.QAbstractItemView.DoubleClicked|QtGui.QAbstractItemView.EditKeyPressed)
        self.tableWidget_curpage.setSelectionMode(QtGui.QAbstractItemView.SingleSelection)
        self.tableWidget_curpage.setColumnCount(3)
        self.tableWidget_curpage.setObjectName(_fromUtf8("tableWidget_curpage"))
        self.tableWidget_curpage.setRowCount(0)
        item = QtGui.QTableWidgetItem()
        self.tableWidget_curpage.setHorizontalHeaderItem(0, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidget_curpage.setHorizontalHeaderItem(1, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidget_curpage.setHorizontalHeaderItem(2, item)
        self.tableWidget_curpage.horizontalHeader().setCascadingSectionResizes(True)
        self.tableWidget_curpage.horizontalHeader().setDefaultSectionSize(130)
        self.tableWidget_curpage.horizontalHeader().setHighlightSections(False)
        self.tableWidget_curpage.verticalHeader().setHighlightSections(False)
        self.treeWidget_pages = QtGui.QTreeWidget(Form_Pages)
        self.treeWidget_pages.setEnabled(True)
        self.treeWidget_pages.setGeometry(QtCore.QRect(10, 0, 169, 691))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Arial"))
        font.setPointSize(11)
        self.treeWidget_pages.setFont(font)
        self.treeWidget_pages.setAutoFillBackground(False)
        self.treeWidget_pages.setStyleSheet(_fromUtf8("border-color: rgb(85, 170, 0);"))
        self.treeWidget_pages.setFrameShadow(QtGui.QFrame.Plain)
        self.treeWidget_pages.setAlternatingRowColors(False)
        self.treeWidget_pages.setIndentation(28)
        self.treeWidget_pages.setItemsExpandable(True)
        self.treeWidget_pages.setAnimated(False)
        self.treeWidget_pages.setAllColumnsShowFocus(True)
        self.treeWidget_pages.setWordWrap(True)
        self.treeWidget_pages.setHeaderHidden(False)
        self.treeWidget_pages.setColumnCount(1)
        self.treeWidget_pages.setObjectName(_fromUtf8("treeWidget_pages"))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.treeWidget_pages.headerItem().setFont(0, font)
        self.textEdit_curregdes = QtGui.QTextEdit(Form_Pages)
        self.textEdit_curregdes.setGeometry(QtCore.QRect(180, 507, 601, 181))
        self.textEdit_curregdes.setReadOnly(True)
        self.textEdit_curregdes.setObjectName(_fromUtf8("textEdit_curregdes"))
        self.label_2 = QtGui.QLabel(Form_Pages)
        self.label_2.setGeometry(QtCore.QRect(790, 329, 31, 16))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_2.setFont(font)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.label_4 = QtGui.QLabel(Form_Pages)
        self.label_4.setGeometry(QtCore.QRect(790, 349, 141, 16))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_4.setFont(font)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.gridLayoutWidget = QtGui.QWidget(Form_Pages)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(790, 400, 160, 101))
        self.gridLayoutWidget.setObjectName(_fromUtf8("gridLayoutWidget"))
        self.gridLayout = QtGui.QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.pushButton_writepage = QtGui.QPushButton(self.gridLayoutWidget)
        self.pushButton_writepage.setObjectName(_fromUtf8("pushButton_writepage"))
        self.gridLayout.addWidget(self.pushButton_writepage, 0, 1, 1, 1)
        self.pushButton_getitem = QtGui.QPushButton(self.gridLayoutWidget)
        self.pushButton_getitem.setObjectName(_fromUtf8("pushButton_getitem"))
        self.gridLayout.addWidget(self.pushButton_getitem, 1, 1, 1, 1)
        self.pushButton_readpage = QtGui.QPushButton(self.gridLayoutWidget)
        self.pushButton_readpage.setObjectName(_fromUtf8("pushButton_readpage"))
        self.gridLayout.addWidget(self.pushButton_readpage, 0, 0, 1, 1)
        self.pushButton_refresh = QtGui.QPushButton(self.gridLayoutWidget)
        self.pushButton_refresh.setObjectName(_fromUtf8("pushButton_refresh"))
        self.gridLayout.addWidget(self.pushButton_refresh, 1, 0, 1, 1)
        self.label_addr = QtGui.QLabel(Form_Pages)
        self.label_addr.setGeometry(QtCore.QRect(820, 330, 81, 16))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_addr.setFont(font)
        self.label_addr.setStyleSheet(_fromUtf8("color: rgb(0, 0, 255);"))
        self.label_addr.setText(_fromUtf8(""))
        self.label_addr.setObjectName(_fromUtf8("label_addr"))
        self.groupBox = QtGui.QGroupBox(Form_Pages)
        self.groupBox.setGeometry(QtCore.QRect(782, 40, 171, 71))
        self.groupBox.setTitle(_fromUtf8(""))
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.gridLayoutWidget_3 = QtGui.QWidget(self.groupBox)
        self.gridLayoutWidget_3.setGeometry(QtCore.QRect(10, 11, 160, 51))
        self.gridLayoutWidget_3.setObjectName(_fromUtf8("gridLayoutWidget_3"))
        self.gridLayout_2 = QtGui.QGridLayout(self.gridLayoutWidget_3)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.radioButton_7 = QtGui.QRadioButton(self.gridLayoutWidget_3)
        self.radioButton_7.setObjectName(_fromUtf8("radioButton_7"))
        self.gridLayout_2.addWidget(self.radioButton_7, 0, 0, 1, 1)
        self.radioButton_15 = QtGui.QRadioButton(self.gridLayoutWidget_3)
        self.radioButton_15.setObjectName(_fromUtf8("radioButton_15"))
        self.gridLayout_2.addWidget(self.radioButton_15, 1, 0, 1, 1)
        self.radioButton_23 = QtGui.QRadioButton(self.gridLayoutWidget_3)
        self.radioButton_23.setObjectName(_fromUtf8("radioButton_23"))
        self.gridLayout_2.addWidget(self.radioButton_23, 0, 1, 1, 1)
        self.radioButton_31 = QtGui.QRadioButton(self.gridLayoutWidget_3)
        self.radioButton_31.setObjectName(_fromUtf8("radioButton_31"))
        self.gridLayout_2.addWidget(self.radioButton_31, 1, 1, 1, 1)
        self.verticalLayoutWidget_3 = QtGui.QWidget(Form_Pages)
        self.verticalLayoutWidget_3.setGeometry(QtCore.QRect(790, 110, 161, 51))
        self.verticalLayoutWidget_3.setObjectName(_fromUtf8("verticalLayoutWidget_3"))
        self.verticalLayout_4 = QtGui.QVBoxLayout(self.verticalLayoutWidget_3)
        self.verticalLayout_4.setObjectName(_fromUtf8("verticalLayout_4"))
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.label_31 = QtGui.QLabel(self.verticalLayoutWidget_3)
        self.label_31.setObjectName(_fromUtf8("label_31"))
        self.horizontalLayout_2.addWidget(self.label_31)
        self.label_30 = QtGui.QLabel(self.verticalLayoutWidget_3)
        self.label_30.setObjectName(_fromUtf8("label_30"))
        self.horizontalLayout_2.addWidget(self.label_30)
        self.label_29 = QtGui.QLabel(self.verticalLayoutWidget_3)
        self.label_29.setObjectName(_fromUtf8("label_29"))
        self.horizontalLayout_2.addWidget(self.label_29)
        self.label_28 = QtGui.QLabel(self.verticalLayoutWidget_3)
        self.label_28.setObjectName(_fromUtf8("label_28"))
        self.horizontalLayout_2.addWidget(self.label_28)
        self.label_27 = QtGui.QLabel(self.verticalLayoutWidget_3)
        self.label_27.setObjectName(_fromUtf8("label_27"))
        self.horizontalLayout_2.addWidget(self.label_27)
        self.label_26 = QtGui.QLabel(self.verticalLayoutWidget_3)
        self.label_26.setObjectName(_fromUtf8("label_26"))
        self.horizontalLayout_2.addWidget(self.label_26)
        self.label_25 = QtGui.QLabel(self.verticalLayoutWidget_3)
        self.label_25.setObjectName(_fromUtf8("label_25"))
        self.horizontalLayout_2.addWidget(self.label_25)
        self.label_24 = QtGui.QLabel(self.verticalLayoutWidget_3)
        self.label_24.setObjectName(_fromUtf8("label_24"))
        self.horizontalLayout_2.addWidget(self.label_24)
        self.verticalLayout_4.addLayout(self.horizontalLayout_2)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.checkBox_7 = QtGui.QCheckBox(self.verticalLayoutWidget_3)
        self.checkBox_7.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.checkBox_7.setText(_fromUtf8(""))
        self.checkBox_7.setTristate(False)
        self.checkBox_7.setObjectName(_fromUtf8("checkBox_7"))
        self.horizontalLayout.addWidget(self.checkBox_7)
        self.checkBox_6 = QtGui.QCheckBox(self.verticalLayoutWidget_3)
        self.checkBox_6.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.checkBox_6.setText(_fromUtf8(""))
        self.checkBox_6.setTristate(False)
        self.checkBox_6.setObjectName(_fromUtf8("checkBox_6"))
        self.horizontalLayout.addWidget(self.checkBox_6)
        self.checkBox_5 = QtGui.QCheckBox(self.verticalLayoutWidget_3)
        self.checkBox_5.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.checkBox_5.setText(_fromUtf8(""))
        self.checkBox_5.setTristate(False)
        self.checkBox_5.setObjectName(_fromUtf8("checkBox_5"))
        self.horizontalLayout.addWidget(self.checkBox_5)
        self.checkBox_4 = QtGui.QCheckBox(self.verticalLayoutWidget_3)
        self.checkBox_4.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.checkBox_4.setText(_fromUtf8(""))
        self.checkBox_4.setTristate(False)
        self.checkBox_4.setObjectName(_fromUtf8("checkBox_4"))
        self.horizontalLayout.addWidget(self.checkBox_4)
        self.checkBox_3 = QtGui.QCheckBox(self.verticalLayoutWidget_3)
        self.checkBox_3.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.checkBox_3.setText(_fromUtf8(""))
        self.checkBox_3.setTristate(False)
        self.checkBox_3.setObjectName(_fromUtf8("checkBox_3"))
        self.horizontalLayout.addWidget(self.checkBox_3)
        self.checkBox_2 = QtGui.QCheckBox(self.verticalLayoutWidget_3)
        self.checkBox_2.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.checkBox_2.setText(_fromUtf8(""))
        self.checkBox_2.setTristate(False)
        self.checkBox_2.setObjectName(_fromUtf8("checkBox_2"))
        self.horizontalLayout.addWidget(self.checkBox_2)
        self.checkBox_1 = QtGui.QCheckBox(self.verticalLayoutWidget_3)
        self.checkBox_1.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.checkBox_1.setText(_fromUtf8(""))
        self.checkBox_1.setTristate(False)
        self.checkBox_1.setObjectName(_fromUtf8("checkBox_1"))
        self.horizontalLayout.addWidget(self.checkBox_1)
        self.checkBox_0 = QtGui.QCheckBox(self.verticalLayoutWidget_3)
        self.checkBox_0.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.checkBox_0.setText(_fromUtf8(""))
        self.checkBox_0.setTristate(False)
        self.checkBox_0.setObjectName(_fromUtf8("checkBox_0"))
        self.horizontalLayout.addWidget(self.checkBox_0)
        self.verticalLayout_4.addLayout(self.horizontalLayout)
        self.label_regsname = QtGui.QLabel(Form_Pages)
        self.label_regsname.setGeometry(QtCore.QRect(810, 20, 111, 16))
        self.label_regsname.setStyleSheet(_fromUtf8("color: rgb(0, 85, 255);"))
        self.label_regsname.setObjectName(_fromUtf8("label_regsname"))
        self.pushButton_Convert = QtGui.QPushButton(Form_Pages)
        self.pushButton_Convert.setGeometry(QtCore.QRect(800, 560, 151, 23))
        self.pushButton_Convert.setObjectName(_fromUtf8("pushButton_Convert"))

        self.retranslateUi(Form_Pages)
        QtCore.QMetaObject.connectSlotsByName(Form_Pages)

    def retranslateUi(self, Form_Pages):
        Form_Pages.setWindowTitle(_translate("Form_Pages", "Form_Pages", None))
        item = self.tableWidget_curpage.horizontalHeaderItem(0)
        item.setText(_translate("Form_Pages", "Address", None))
        item = self.tableWidget_curpage.horizontalHeaderItem(1)
        item.setText(_translate("Form_Pages", "Name", None))
        item = self.tableWidget_curpage.horizontalHeaderItem(2)
        item.setText(_translate("Form_Pages", "Value", None))
        self.treeWidget_pages.setSortingEnabled(False)
        self.treeWidget_pages.headerItem().setText(0, _translate("Form_Pages", "V_SW", None))
        self.label_2.setText(_translate("Form_Pages", "<html><head/><body><p><span style=\" color:#ff0000;\">ADD</span>:</p></body></html>", None))
        self.label_4.setText(_translate("Form_Pages", "DWORD Mode", None))
        self.pushButton_writepage.setText(_translate("Form_Pages", "Write", None))
        self.pushButton_getitem.setText(_translate("Form_Pages", "GetItem", None))
        self.pushButton_readpage.setText(_translate("Form_Pages", "Read", None))
        self.pushButton_refresh.setText(_translate("Form_Pages", "Refresh", None))
        self.radioButton_7.setText(_translate("Form_Pages", "7-0", None))
        self.radioButton_15.setText(_translate("Form_Pages", "15-8", None))
        self.radioButton_23.setText(_translate("Form_Pages", "23-16", None))
        self.radioButton_31.setText(_translate("Form_Pages", "31-24", None))
        self.label_31.setText(_translate("Form_Pages", "31", None))
        self.label_30.setText(_translate("Form_Pages", "30", None))
        self.label_29.setText(_translate("Form_Pages", "29", None))
        self.label_28.setText(_translate("Form_Pages", "28", None))
        self.label_27.setText(_translate("Form_Pages", "27", None))
        self.label_26.setText(_translate("Form_Pages", "26", None))
        self.label_25.setText(_translate("Form_Pages", "25", None))
        self.label_24.setText(_translate("Form_Pages", "24", None))
        self.label_regsname.setText(_translate("Form_Pages", "spare:spare", None))
        self.pushButton_Convert.setText(_translate("Form_Pages", "Convert .csv to .c/.h", None))

