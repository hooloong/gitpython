# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'UI_Debug_res.ui'
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

class Ui_Form_UIDebug(object):
    def setupUi(self, Form_UIDebug):
        Form_UIDebug.setObjectName(_fromUtf8("Form_UIDebug"))
        Form_UIDebug.resize(870, 679)
        self.checkBox_pic_mode = QtGui.QCheckBox(Form_UIDebug)
        self.checkBox_pic_mode.setEnabled(True)
        self.checkBox_pic_mode.setGeometry(QtCore.QRect(220, 33, 85, 16))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.checkBox_pic_mode.setFont(font)
        self.checkBox_pic_mode.setCheckable(True)
        self.checkBox_pic_mode.setChecked(False)
        self.checkBox_pic_mode.setObjectName(_fromUtf8("checkBox_pic_mode"))
        self.lineEdit_backlight = QtGui.QLineEdit(Form_UIDebug)
        self.lineEdit_backlight.setGeometry(QtCore.QRect(50, 225, 50, 16))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.lineEdit_backlight.setFont(font)
        self.lineEdit_backlight.setObjectName(_fromUtf8("lineEdit_backlight"))
        self.checkBox_backlight = QtGui.QCheckBox(Form_UIDebug)
        self.checkBox_backlight.setGeometry(QtCore.QRect(110, 227, 101, 16))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.checkBox_backlight.setFont(font)
        self.checkBox_backlight.setObjectName(_fromUtf8("checkBox_backlight"))
        self.checkBox_brightness = QtGui.QCheckBox(Form_UIDebug)
        self.checkBox_brightness.setGeometry(QtCore.QRect(110, 262, 111, 16))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.checkBox_brightness.setFont(font)
        self.checkBox_brightness.setObjectName(_fromUtf8("checkBox_brightness"))
        self.checkBox_contrast = QtGui.QCheckBox(Form_UIDebug)
        self.checkBox_contrast.setGeometry(QtCore.QRect(110, 297, 101, 16))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.checkBox_contrast.setFont(font)
        self.checkBox_contrast.setObjectName(_fromUtf8("checkBox_contrast"))
        self.checkBox_saturation = QtGui.QCheckBox(Form_UIDebug)
        self.checkBox_saturation.setGeometry(QtCore.QRect(110, 332, 111, 16))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.checkBox_saturation.setFont(font)
        self.checkBox_saturation.setObjectName(_fromUtf8("checkBox_saturation"))
        self.checkBox_hue = QtGui.QCheckBox(Form_UIDebug)
        self.checkBox_hue.setGeometry(QtCore.QRect(110, 367, 71, 16))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.checkBox_hue.setFont(font)
        self.checkBox_hue.setObjectName(_fromUtf8("checkBox_hue"))
        self.checkBox_sharpness = QtGui.QCheckBox(Form_UIDebug)
        self.checkBox_sharpness.setGeometry(QtCore.QRect(110, 402, 111, 16))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.checkBox_sharpness.setFont(font)
        self.checkBox_sharpness.setObjectName(_fromUtf8("checkBox_sharpness"))
        self.lineEdit_brightness = QtGui.QLineEdit(Form_UIDebug)
        self.lineEdit_brightness.setGeometry(QtCore.QRect(50, 260, 50, 20))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.lineEdit_brightness.setFont(font)
        self.lineEdit_brightness.setObjectName(_fromUtf8("lineEdit_brightness"))
        self.lineEdit_contrast = QtGui.QLineEdit(Form_UIDebug)
        self.lineEdit_contrast.setGeometry(QtCore.QRect(50, 295, 50, 20))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.lineEdit_contrast.setFont(font)
        self.lineEdit_contrast.setObjectName(_fromUtf8("lineEdit_contrast"))
        self.lineEdit_saturation = QtGui.QLineEdit(Form_UIDebug)
        self.lineEdit_saturation.setGeometry(QtCore.QRect(50, 330, 50, 20))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.lineEdit_saturation.setFont(font)
        self.lineEdit_saturation.setObjectName(_fromUtf8("lineEdit_saturation"))
        self.lineEdit_hue = QtGui.QLineEdit(Form_UIDebug)
        self.lineEdit_hue.setGeometry(QtCore.QRect(50, 365, 50, 20))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.lineEdit_hue.setFont(font)
        self.lineEdit_hue.setObjectName(_fromUtf8("lineEdit_hue"))
        self.lineEdit_sharpness = QtGui.QLineEdit(Form_UIDebug)
        self.lineEdit_sharpness.setGeometry(QtCore.QRect(50, 400, 50, 20))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.lineEdit_sharpness.setFont(font)
        self.lineEdit_sharpness.setObjectName(_fromUtf8("lineEdit_sharpness"))
        self.tableWidget_color_tuner = QtGui.QTableWidget(Form_UIDebug)
        self.tableWidget_color_tuner.setGeometry(QtCore.QRect(100, 480, 362, 92))
        self.tableWidget_color_tuner.setProperty("showDropIndicator", True)
        self.tableWidget_color_tuner.setDragDropOverwriteMode(True)
        self.tableWidget_color_tuner.setRowCount(3)
        self.tableWidget_color_tuner.setColumnCount(6)
        self.tableWidget_color_tuner.setObjectName(_fromUtf8("tableWidget_color_tuner"))
        item = QtGui.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        item.setCheckState(QtCore.Qt.Unchecked)
        self.tableWidget_color_tuner.setItem(0, 0, item)
        item = QtGui.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        item.setCheckState(QtCore.Qt.Unchecked)
        self.tableWidget_color_tuner.setItem(0, 1, item)
        item = QtGui.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        item.setCheckState(QtCore.Qt.Unchecked)
        self.tableWidget_color_tuner.setItem(0, 2, item)
        item = QtGui.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        item.setCheckState(QtCore.Qt.Unchecked)
        self.tableWidget_color_tuner.setItem(0, 3, item)
        item = QtGui.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        item.setCheckState(QtCore.Qt.Unchecked)
        self.tableWidget_color_tuner.setItem(0, 4, item)
        item = QtGui.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        item.setCheckState(QtCore.Qt.Unchecked)
        self.tableWidget_color_tuner.setItem(0, 5, item)
        item = QtGui.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        item.setCheckState(QtCore.Qt.Unchecked)
        self.tableWidget_color_tuner.setItem(1, 0, item)
        item = QtGui.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        item.setCheckState(QtCore.Qt.Unchecked)
        self.tableWidget_color_tuner.setItem(1, 1, item)
        item = QtGui.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        item.setCheckState(QtCore.Qt.Unchecked)
        self.tableWidget_color_tuner.setItem(1, 2, item)
        item = QtGui.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        item.setCheckState(QtCore.Qt.Unchecked)
        self.tableWidget_color_tuner.setItem(1, 3, item)
        item = QtGui.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        item.setCheckState(QtCore.Qt.Unchecked)
        self.tableWidget_color_tuner.setItem(1, 4, item)
        item = QtGui.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        item.setCheckState(QtCore.Qt.Unchecked)
        self.tableWidget_color_tuner.setItem(1, 5, item)
        item = QtGui.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        item.setCheckState(QtCore.Qt.Unchecked)
        self.tableWidget_color_tuner.setItem(2, 0, item)
        item = QtGui.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        item.setCheckState(QtCore.Qt.Unchecked)
        self.tableWidget_color_tuner.setItem(2, 1, item)
        item = QtGui.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        item.setCheckState(QtCore.Qt.Unchecked)
        self.tableWidget_color_tuner.setItem(2, 2, item)
        item = QtGui.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        item.setCheckState(QtCore.Qt.Unchecked)
        self.tableWidget_color_tuner.setItem(2, 3, item)
        item = QtGui.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        item.setCheckState(QtCore.Qt.Unchecked)
        self.tableWidget_color_tuner.setItem(2, 4, item)
        item = QtGui.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        item.setCheckState(QtCore.Qt.Unchecked)
        self.tableWidget_color_tuner.setItem(2, 5, item)
        self.tableWidget_color_tuner.horizontalHeader().setVisible(False)
        self.tableWidget_color_tuner.horizontalHeader().setDefaultSectionSize(60)
        self.tableWidget_color_tuner.verticalHeader().setVisible(False)
        self.tableWidget_color_tuner.verticalHeader().setHighlightSections(True)
        self.tableWidget_wb = QtGui.QTableWidget(Form_UIDebug)
        self.tableWidget_wb.setGeometry(QtCore.QRect(100, 571, 182, 62))
        self.tableWidget_wb.setRowCount(2)
        self.tableWidget_wb.setColumnCount(3)
        self.tableWidget_wb.setObjectName(_fromUtf8("tableWidget_wb"))
        item = QtGui.QTableWidgetItem()
        item.setCheckState(QtCore.Qt.Unchecked)
        self.tableWidget_wb.setItem(0, 0, item)
        item = QtGui.QTableWidgetItem()
        item.setCheckState(QtCore.Qt.Unchecked)
        self.tableWidget_wb.setItem(0, 1, item)
        item = QtGui.QTableWidgetItem()
        item.setCheckState(QtCore.Qt.Unchecked)
        self.tableWidget_wb.setItem(0, 2, item)
        item = QtGui.QTableWidgetItem()
        item.setCheckState(QtCore.Qt.Unchecked)
        self.tableWidget_wb.setItem(1, 0, item)
        item = QtGui.QTableWidgetItem()
        item.setCheckState(QtCore.Qt.Unchecked)
        self.tableWidget_wb.setItem(1, 1, item)
        item = QtGui.QTableWidgetItem()
        item.setCheckState(QtCore.Qt.Unchecked)
        self.tableWidget_wb.setItem(1, 2, item)
        self.tableWidget_wb.horizontalHeader().setVisible(False)
        self.tableWidget_wb.horizontalHeader().setDefaultSectionSize(60)
        self.tableWidget_wb.verticalHeader().setVisible(False)
        self.label = QtGui.QLabel(Form_UIDebug)
        self.label.setGeometry(QtCore.QRect(130, 460, 21, 16))
        self.label.setObjectName(_fromUtf8("label"))
        self.label_2 = QtGui.QLabel(Form_UIDebug)
        self.label_2.setGeometry(QtCore.QRect(190, 460, 21, 16))
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.label_3 = QtGui.QLabel(Form_UIDebug)
        self.label_3.setGeometry(QtCore.QRect(250, 460, 21, 16))
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.label_4 = QtGui.QLabel(Form_UIDebug)
        self.label_4.setGeometry(QtCore.QRect(310, 460, 21, 16))
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.label_5 = QtGui.QLabel(Form_UIDebug)
        self.label_5.setGeometry(QtCore.QRect(430, 460, 21, 16))
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.label_6 = QtGui.QLabel(Form_UIDebug)
        self.label_6.setGeometry(QtCore.QRect(370, 460, 21, 16))
        self.label_6.setObjectName(_fromUtf8("label_6"))
        self.label_7 = QtGui.QLabel(Form_UIDebug)
        self.label_7.setGeometry(QtCore.QRect(70, 490, 30, 12))
        self.label_7.setObjectName(_fromUtf8("label_7"))
        self.label_8 = QtGui.QLabel(Form_UIDebug)
        self.label_8.setGeometry(QtCore.QRect(70, 520, 30, 12))
        self.label_8.setObjectName(_fromUtf8("label_8"))
        self.label_9 = QtGui.QLabel(Form_UIDebug)
        self.label_9.setGeometry(QtCore.QRect(70, 550, 30, 12))
        self.label_9.setObjectName(_fromUtf8("label_9"))
        self.label_10 = QtGui.QLabel(Form_UIDebug)
        self.label_10.setGeometry(QtCore.QRect(65, 580, 30, 12))
        self.label_10.setObjectName(_fromUtf8("label_10"))
        self.label_11 = QtGui.QLabel(Form_UIDebug)
        self.label_11.setGeometry(QtCore.QRect(55, 610, 41, 16))
        self.label_11.setObjectName(_fromUtf8("label_11"))
        self.groupBox = QtGui.QGroupBox(Form_UIDebug)
        self.groupBox.setGeometry(QtCore.QRect(35, 440, 451, 201))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setItalic(False)
        font.setUnderline(False)
        font.setStrikeOut(False)
        self.groupBox.setFont(font)
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.pushButton_read = QtGui.QPushButton(Form_UIDebug)
        self.pushButton_read.setGeometry(QtCore.QRect(670, 500, 71, 41))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.pushButton_read.setFont(font)
        self.pushButton_read.setObjectName(_fromUtf8("pushButton_read"))
        self.comboBox_pic_mode = QtGui.QComboBox(Form_UIDebug)
        self.comboBox_pic_mode.setGeometry(QtCore.QRect(50, 30, 150, 22))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.comboBox_pic_mode.setFont(font)
        self.comboBox_pic_mode.setObjectName(_fromUtf8("comboBox_pic_mode"))
        self.pushButton_write = QtGui.QPushButton(Form_UIDebug)
        self.pushButton_write.setGeometry(QtCore.QRect(670, 570, 71, 41))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.pushButton_write.setFont(font)
        self.pushButton_write.setObjectName(_fromUtf8("pushButton_write"))
        self.comboBox_AutoBrightness = QtGui.QComboBox(Form_UIDebug)
        self.comboBox_AutoBrightness.setGeometry(QtCore.QRect(450, 27, 100, 22))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.comboBox_AutoBrightness.setFont(font)
        self.comboBox_AutoBrightness.setObjectName(_fromUtf8("comboBox_AutoBrightness"))
        self.checkBox_AutoBrightness = QtGui.QCheckBox(Form_UIDebug)
        self.checkBox_AutoBrightness.setEnabled(True)
        self.checkBox_AutoBrightness.setGeometry(QtCore.QRect(570, 30, 151, 16))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.checkBox_AutoBrightness.setFont(font)
        self.checkBox_AutoBrightness.setCheckable(True)
        self.checkBox_AutoBrightness.setChecked(False)
        self.checkBox_AutoBrightness.setObjectName(_fromUtf8("checkBox_AutoBrightness"))
        self.checkBox_BlackExtention = QtGui.QCheckBox(Form_UIDebug)
        self.checkBox_BlackExtention.setEnabled(True)
        self.checkBox_BlackExtention.setGeometry(QtCore.QRect(170, 73, 151, 16))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.checkBox_BlackExtention.setFont(font)
        self.checkBox_BlackExtention.setCheckable(True)
        self.checkBox_BlackExtention.setChecked(False)
        self.checkBox_BlackExtention.setObjectName(_fromUtf8("checkBox_BlackExtention"))
        self.comboBox_BlackExtention = QtGui.QComboBox(Form_UIDebug)
        self.comboBox_BlackExtention.setGeometry(QtCore.QRect(50, 70, 100, 22))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.comboBox_BlackExtention.setFont(font)
        self.comboBox_BlackExtention.setObjectName(_fromUtf8("comboBox_BlackExtention"))
        self.comboBox_DCI = QtGui.QComboBox(Form_UIDebug)
        self.comboBox_DCI.setGeometry(QtCore.QRect(50, 107, 100, 22))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.comboBox_DCI.setFont(font)
        self.comboBox_DCI.setObjectName(_fromUtf8("comboBox_DCI"))
        self.checkBox_DCI = QtGui.QCheckBox(Form_UIDebug)
        self.checkBox_DCI.setEnabled(True)
        self.checkBox_DCI.setGeometry(QtCore.QRect(170, 110, 61, 16))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.checkBox_DCI.setFont(font)
        self.checkBox_DCI.setCheckable(True)
        self.checkBox_DCI.setChecked(False)
        self.checkBox_DCI.setObjectName(_fromUtf8("checkBox_DCI"))
        self.comboBox_LocalDimming = QtGui.QComboBox(Form_UIDebug)
        self.comboBox_LocalDimming.setGeometry(QtCore.QRect(450, 67, 100, 22))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.comboBox_LocalDimming.setFont(font)
        self.comboBox_LocalDimming.setObjectName(_fromUtf8("comboBox_LocalDimming"))
        self.checkBox_LocalDimming = QtGui.QCheckBox(Form_UIDebug)
        self.checkBox_LocalDimming.setEnabled(True)
        self.checkBox_LocalDimming.setGeometry(QtCore.QRect(570, 70, 161, 16))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.checkBox_LocalDimming.setFont(font)
        self.checkBox_LocalDimming.setCheckable(True)
        self.checkBox_LocalDimming.setChecked(False)
        self.checkBox_LocalDimming.setObjectName(_fromUtf8("checkBox_LocalDimming"))
        self.comboBox_ClearAction = QtGui.QComboBox(Form_UIDebug)
        self.comboBox_ClearAction.setGeometry(QtCore.QRect(450, 107, 100, 22))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.comboBox_ClearAction.setFont(font)
        self.comboBox_ClearAction.setObjectName(_fromUtf8("comboBox_ClearAction"))
        self.checkBox_ClearAction = QtGui.QCheckBox(Form_UIDebug)
        self.checkBox_ClearAction.setEnabled(True)
        self.checkBox_ClearAction.setGeometry(QtCore.QRect(570, 110, 161, 16))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.checkBox_ClearAction.setFont(font)
        self.checkBox_ClearAction.setCheckable(True)
        self.checkBox_ClearAction.setChecked(False)
        self.checkBox_ClearAction.setObjectName(_fromUtf8("checkBox_ClearAction"))
        self.comboBox_MpegNR = QtGui.QComboBox(Form_UIDebug)
        self.comboBox_MpegNR.setGeometry(QtCore.QRect(50, 147, 100, 22))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.comboBox_MpegNR.setFont(font)
        self.comboBox_MpegNR.setObjectName(_fromUtf8("comboBox_MpegNR"))
        self.checkBox_MpegNR = QtGui.QCheckBox(Form_UIDebug)
        self.checkBox_MpegNR.setEnabled(True)
        self.checkBox_MpegNR.setGeometry(QtCore.QRect(170, 150, 81, 16))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.checkBox_MpegNR.setFont(font)
        self.checkBox_MpegNR.setCheckable(True)
        self.checkBox_MpegNR.setChecked(False)
        self.checkBox_MpegNR.setObjectName(_fromUtf8("checkBox_MpegNR"))
        self.comboBox_NR = QtGui.QComboBox(Form_UIDebug)
        self.comboBox_NR.setGeometry(QtCore.QRect(50, 187, 100, 22))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.comboBox_NR.setFont(font)
        self.comboBox_NR.setObjectName(_fromUtf8("comboBox_NR"))
        self.checkBox_NR = QtGui.QCheckBox(Form_UIDebug)
        self.checkBox_NR.setEnabled(True)
        self.checkBox_NR.setGeometry(QtCore.QRect(170, 190, 71, 16))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.checkBox_NR.setFont(font)
        self.checkBox_NR.setCheckable(True)
        self.checkBox_NR.setChecked(False)
        self.checkBox_NR.setObjectName(_fromUtf8("checkBox_NR"))
        self.comboBox_GameMode = QtGui.QComboBox(Form_UIDebug)
        self.comboBox_GameMode.setGeometry(QtCore.QRect(450, 154, 100, 22))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.comboBox_GameMode.setFont(font)
        self.comboBox_GameMode.setObjectName(_fromUtf8("comboBox_GameMode"))
        self.checkBox_GameMode = QtGui.QCheckBox(Form_UIDebug)
        self.checkBox_GameMode.setEnabled(True)
        self.checkBox_GameMode.setGeometry(QtCore.QRect(570, 157, 101, 16))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.checkBox_GameMode.setFont(font)
        self.checkBox_GameMode.setCheckable(True)
        self.checkBox_GameMode.setChecked(False)
        self.checkBox_GameMode.setObjectName(_fromUtf8("checkBox_GameMode"))
        self.checkBox_MovieMode = QtGui.QCheckBox(Form_UIDebug)
        self.checkBox_MovieMode.setEnabled(True)
        self.checkBox_MovieMode.setGeometry(QtCore.QRect(570, 200, 111, 16))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.checkBox_MovieMode.setFont(font)
        self.checkBox_MovieMode.setCheckable(True)
        self.checkBox_MovieMode.setChecked(False)
        self.checkBox_MovieMode.setObjectName(_fromUtf8("checkBox_MovieMode"))
        self.comboBox_MovieMode = QtGui.QComboBox(Form_UIDebug)
        self.comboBox_MovieMode.setGeometry(QtCore.QRect(450, 197, 100, 22))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.comboBox_MovieMode.setFont(font)
        self.comboBox_MovieMode.setObjectName(_fromUtf8("comboBox_MovieMode"))
        self.comboBox_Judder = QtGui.QComboBox(Form_UIDebug)
        self.comboBox_Judder.setGeometry(QtCore.QRect(450, 237, 100, 22))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.comboBox_Judder.setFont(font)
        self.comboBox_Judder.setObjectName(_fromUtf8("comboBox_Judder"))
        self.comboBox_Blur = QtGui.QComboBox(Form_UIDebug)
        self.comboBox_Blur.setGeometry(QtCore.QRect(450, 277, 100, 22))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.comboBox_Blur.setFont(font)
        self.comboBox_Blur.setObjectName(_fromUtf8("comboBox_Blur"))
        self.checkBox_Judder = QtGui.QCheckBox(Form_UIDebug)
        self.checkBox_Judder.setEnabled(True)
        self.checkBox_Judder.setGeometry(QtCore.QRect(570, 239, 151, 16))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.checkBox_Judder.setFont(font)
        self.checkBox_Judder.setCheckable(True)
        self.checkBox_Judder.setChecked(False)
        self.checkBox_Judder.setObjectName(_fromUtf8("checkBox_Judder"))
        self.checkBox_Blur = QtGui.QCheckBox(Form_UIDebug)
        self.checkBox_Blur.setEnabled(True)
        self.checkBox_Blur.setGeometry(QtCore.QRect(570, 280, 151, 16))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.checkBox_Blur.setFont(font)
        self.checkBox_Blur.setCheckable(True)
        self.checkBox_Blur.setChecked(False)
        self.checkBox_Blur.setObjectName(_fromUtf8("checkBox_Blur"))
        self.checkBox_ColorTemp = QtGui.QCheckBox(Form_UIDebug)
        self.checkBox_ColorTemp.setEnabled(True)
        self.checkBox_ColorTemp.setGeometry(QtCore.QRect(570, 320, 151, 16))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.checkBox_ColorTemp.setFont(font)
        self.checkBox_ColorTemp.setCheckable(True)
        self.checkBox_ColorTemp.setChecked(False)
        self.checkBox_ColorTemp.setObjectName(_fromUtf8("checkBox_ColorTemp"))
        self.comboBox_ColorTemp = QtGui.QComboBox(Form_UIDebug)
        self.comboBox_ColorTemp.setGeometry(QtCore.QRect(450, 317, 100, 22))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.comboBox_ColorTemp.setFont(font)
        self.comboBox_ColorTemp.setObjectName(_fromUtf8("comboBox_ColorTemp"))
        self.comboBox_gammaFactor = QtGui.QComboBox(Form_UIDebug)
        self.comboBox_gammaFactor.setGeometry(QtCore.QRect(450, 357, 100, 22))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.comboBox_gammaFactor.setFont(font)
        self.comboBox_gammaFactor.setObjectName(_fromUtf8("comboBox_gammaFactor"))
        self.checkBox_gammaFactor = QtGui.QCheckBox(Form_UIDebug)
        self.checkBox_gammaFactor.setEnabled(True)
        self.checkBox_gammaFactor.setGeometry(QtCore.QRect(570, 360, 151, 16))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.checkBox_gammaFactor.setFont(font)
        self.checkBox_gammaFactor.setCheckable(True)
        self.checkBox_gammaFactor.setChecked(False)
        self.checkBox_gammaFactor.setObjectName(_fromUtf8("checkBox_gammaFactor"))
        self.groupBox.raise_()
        self.tableWidget_color_tuner.raise_()
        self.checkBox_pic_mode.raise_()
        self.lineEdit_backlight.raise_()
        self.checkBox_backlight.raise_()
        self.checkBox_brightness.raise_()
        self.checkBox_contrast.raise_()
        self.checkBox_saturation.raise_()
        self.checkBox_hue.raise_()
        self.checkBox_sharpness.raise_()
        self.lineEdit_brightness.raise_()
        self.lineEdit_contrast.raise_()
        self.lineEdit_saturation.raise_()
        self.lineEdit_hue.raise_()
        self.lineEdit_sharpness.raise_()
        self.tableWidget_wb.raise_()
        self.label.raise_()
        self.label_2.raise_()
        self.label_3.raise_()
        self.label_4.raise_()
        self.label_5.raise_()
        self.label_6.raise_()
        self.label_7.raise_()
        self.label_8.raise_()
        self.label_9.raise_()
        self.label_10.raise_()
        self.label_11.raise_()
        self.pushButton_read.raise_()
        self.comboBox_pic_mode.raise_()
        self.pushButton_write.raise_()
        self.comboBox_AutoBrightness.raise_()
        self.checkBox_AutoBrightness.raise_()
        self.checkBox_BlackExtention.raise_()
        self.comboBox_BlackExtention.raise_()
        self.comboBox_DCI.raise_()
        self.checkBox_DCI.raise_()
        self.comboBox_LocalDimming.raise_()
        self.checkBox_LocalDimming.raise_()
        self.comboBox_ClearAction.raise_()
        self.checkBox_ClearAction.raise_()
        self.comboBox_MpegNR.raise_()
        self.checkBox_MpegNR.raise_()
        self.comboBox_NR.raise_()
        self.checkBox_NR.raise_()
        self.comboBox_GameMode.raise_()
        self.checkBox_GameMode.raise_()
        self.checkBox_MovieMode.raise_()
        self.comboBox_MovieMode.raise_()
        self.comboBox_Judder.raise_()
        self.comboBox_Blur.raise_()
        self.checkBox_Judder.raise_()
        self.checkBox_Blur.raise_()
        self.checkBox_ColorTemp.raise_()
        self.comboBox_ColorTemp.raise_()
        self.comboBox_gammaFactor.raise_()
        self.checkBox_gammaFactor.raise_()

        self.retranslateUi(Form_UIDebug)
        QtCore.QMetaObject.connectSlotsByName(Form_UIDebug)

    def retranslateUi(self, Form_UIDebug):
        Form_UIDebug.setWindowTitle(_translate("Form_UIDebug", "Form", None))
        self.checkBox_pic_mode.setText(_translate("Form_UIDebug", "PicMode", None))
        self.checkBox_backlight.setText(_translate("Form_UIDebug", "backlight", None))
        self.checkBox_brightness.setText(_translate("Form_UIDebug", "brightness", None))
        self.checkBox_contrast.setText(_translate("Form_UIDebug", "contrast", None))
        self.checkBox_saturation.setText(_translate("Form_UIDebug", "saturation", None))
        self.checkBox_hue.setText(_translate("Form_UIDebug", "tint", None))
        self.checkBox_sharpness.setText(_translate("Form_UIDebug", "sharpness", None))
        __sortingEnabled = self.tableWidget_color_tuner.isSortingEnabled()
        self.tableWidget_color_tuner.setSortingEnabled(False)
        self.tableWidget_color_tuner.setSortingEnabled(__sortingEnabled)
        __sortingEnabled = self.tableWidget_wb.isSortingEnabled()
        self.tableWidget_wb.setSortingEnabled(False)
        self.tableWidget_wb.setSortingEnabled(__sortingEnabled)
        self.label.setText(_translate("Form_UIDebug", "R", None))
        self.label_2.setText(_translate("Form_UIDebug", "G", None))
        self.label_3.setText(_translate("Form_UIDebug", "B", None))
        self.label_4.setText(_translate("Form_UIDebug", "C", None))
        self.label_5.setText(_translate("Form_UIDebug", "Y", None))
        self.label_6.setText(_translate("Form_UIDebug", "M", None))
        self.label_7.setText(_translate("Form_UIDebug", "hue", None))
        self.label_8.setText(_translate("Form_UIDebug", "sat", None))
        self.label_9.setText(_translate("Form_UIDebug", "bri", None))
        self.label_10.setText(_translate("Form_UIDebug", "gain", None))
        self.label_11.setText(_translate("Form_UIDebug", "offset", None))
        self.groupBox.setTitle(_translate("Form_UIDebug", "ColorTuner", None))
        self.pushButton_read.setText(_translate("Form_UIDebug", "Read", None))
        self.pushButton_write.setText(_translate("Form_UIDebug", "Write", None))
        self.checkBox_AutoBrightness.setText(_translate("Form_UIDebug", "AutoBrightness", None))
        self.checkBox_BlackExtention.setText(_translate("Form_UIDebug", "BlackExtention", None))
        self.checkBox_DCI.setText(_translate("Form_UIDebug", "DCI", None))
        self.checkBox_LocalDimming.setText(_translate("Form_UIDebug", "Active LED Zone", None))
        self.checkBox_ClearAction.setText(_translate("Form_UIDebug", "Clear Action", None))
        self.checkBox_MpegNR.setText(_translate("Form_UIDebug", "MpegNR", None))
        self.checkBox_NR.setText(_translate("Form_UIDebug", "TNR", None))
        self.checkBox_GameMode.setText(_translate("Form_UIDebug", "GameMode", None))
        self.checkBox_MovieMode.setText(_translate("Form_UIDebug", "MovieMode", None))
        self.checkBox_Judder.setText(_translate("Form_UIDebug", "Judder Reduce", None))
        self.checkBox_Blur.setText(_translate("Form_UIDebug", "Blur Reduce", None))
        self.checkBox_ColorTemp.setText(_translate("Form_UIDebug", "ColorTemp", None))
        self.checkBox_gammaFactor.setText(_translate("Form_UIDebug", "gammaFactor", None))

