__author__ = 'hooloongge'
# -*- coding: utf-8 -*-
import sys, math, random, time
import ctypes as C
import two01 as TFC
# import xmltodict
import json
import ConfigParser
import numpy as np
from dispmipsfunc import *
from PyQt4 import QtCore, QtGui,QtSql, uic  # ,Qwt5
from dimmingdebugger_res_FRCXB import *
from PWMs import *
from Hist import *
from TestPattern import *
from Dimpages import *
from DrawL2G import *
from AutoTest import  *


class MyWindow(QtGui.QMainWindow):

    def __init__(self):
        super(MyWindow, self).__init__()
        # uic.loadUi("dimmingdebugger_res.ui", self)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowIcon(QtGui.QIcon("images/222.ico"))
        self.setGeometry(300,300,810,640)
        self.statusBar().showMessage('DisConnected to chip!!!')
        self.painter = QtGui.QPainter()

        self.ui.tabWidget.removeTab(0)

        self.s_dict = dict(defaultfilename="dimming_readback_parameters_frcxb.json")

        self.connectFlag = False
        self.bConnectionTried = False
        self.loadSettingfromJson()

        self.formPWMs = PWMsWindow()
        self.ui.tabWidget.insertTab(0, self.formPWMs, u"PWMs")

        self.formHist = HistWindow()
        self.ui.tabWidget.insertTab(1, self.formHist, u"Hist")
        self.formTestPattern = TestPatternWindow()
        self.formDimpages = DimPagesWindow()
        # self.formDraw = DrawL2GWindow()
        # self.formAutoTest = AutoTestWindow()
        self.ui.tabWidget.insertTab(2, self.formTestPattern, u"TestPattern")
        self.ui.tabWidget.insertTab(3, self.formDimpages, u"DimPages")
        # self.ui.tabWidget.insertTab(4, self.formDraw, u"DrawL2G")
        # self.ui.tabWidget.insertTab(5, self.formAutoTest, u"AutoTest")
        self.connect(self.ui.actionConnect, QtCore.SIGNAL('triggered()'), self.connectChip)
        self.connect(self.ui.actionDisconnect, QtCore.SIGNAL('triggered()'), self.disconnectChip)
        self.ui.actionQuit.connect(self.ui.actionQuit, QtCore.SIGNAL('triggered()'), QtGui.qApp, QtCore.SLOT('quit()'))
        self.ui.actionOpen_setting_file.connect(self.ui.actionOpen_setting_file, QtCore.SIGNAL('triggered()'),
                                             self.loadSettingfromJson)
        self.ui.actionSave_setting_file.connect(self.ui.actionSave_setting_file, QtCore.SIGNAL('triggered()'),
                                             self.saveSettingfromJson)
        self.connect(self.ui.tabWidget, QtCore.SIGNAL('currentChanged(int)'), self.tabchanges)
        self.setPanelInfo()

        self.resize(860, 690)

    def tabchanges(self,index):
        if index == 4:
            self.resize(1180,760)
        elif index == 3:
            self.resize(960, 760)
        elif index == 2:
            self.resize(840, 690)
        elif index == 1:
            self.resize(860, 700)
        else:
            self.resize(860, 690)

    def setPanelInfo(self):
        self.formTestPattern.setSettingDict(self.s_dict)
        self.formDimpages.setSettingDict(self.s_setjson["dim_pages"])
        self.formPWMs.setSettingDict(self.s_dict)
        pass
    def modifyIP(self, config_read):
        eth_ip = config_read.get("Connection", "Ethernet.IP")
        arm_set = config_read.get("Connection", "arm")
        frcx_set = config_read.get("Connection", "sx6-frcx")
        ip_addr, ok = QtGui.QInputDialog.getText(self, 'IP', 'Enter IP address:', text=eth_ip)
        if ok is False:
            return False
        elif ip_addr.isEmpty():
            QtGui.QMessageBox.information(self, "warning", ("Please enter IP address !!!"))
            return False
        elif ip_addr != eth_ip or arm_set != '0' or frcx_set != '1':
            try:
                config_read.set("Connection", "Ethernet.IP", ip_addr)
                config_read.set("Connection", "arm", '0')
                config_read.set("Connection", "sx6-frcx", '1')
                config_read.write(open("ChipDebugger.INI", "r+"))
            except Exception, e:
                QtGui.QMessageBox.information(self, "Warning", str(e))
                return False
        return True
    def connectChip(self):
        config_read = ConfigParser.RawConfigParser()
        config_read.read("ChipDebugger.INI")
        if self.bConnectionTried is False:
            if self.modifyIP(config_read) is False:
                return
        eth_ip = config_read.get("Connection", "Ethernet.IP")
        self.connectFlag = TFC.TFCConnect2Chip()
        self.bConnectionTried = True
        self.formPWMs.setConnectFlag(self.connectFlag)
        self.formHist.setConnectFlag(self.connectFlag)
        self.formTestPattern.setConnectFlag(self.connectFlag)
        self.formDimpages.setConnectFlag(self.connectFlag)
        print("tfcConnInit returns ", self.connectFlag)
        if self.connectFlag:
            print("Connect to chip!!! ")
            self.statusBar().showMessage('"Connect to chip!!!')
            self.setWindowTitle("Dimming Debugger" + "   " + "Connection" + "   " + eth_ip)
        else:
            print("Could not Connect to chip!!! ")
            self.statusBar().showMessage('Could not Connect to ' + "   " + eth_ip + "!!!!")
            self.setWindowTitle("Dimming Debugger" + "    " + "DisConnection")
            QtGui.QMessageBox.information(self, "warning", ('Could not connect to ' + " " + eth_ip + " !!!!"))

    def disconnectChip(self):
        if self.connectFlag == False:
            return
        self.connectFlag = False
        self.formPWMs.setConnectFlag(self.connectFlag)
        self.formHist.setConnectFlag(self.connectFlag)
        self.formTestPattern.setConnectFlag(self.connectFlag)
        TFC.tfcConnTerm()
        self.setWindowTitle("Dimming Debugger     DisConnect..")

    def loadSettingfromJson(self):
        settingfile = "dimming_readback_parameters_frcxb.json"
        s_fp = open(settingfile, 'r')
        if s_fp == False:
            print "error file!!!!"
        else:
            self.s_setjson = json.load(s_fp)
            s_fp.close()
            self.s_dict = self.s_setjson["panel_info"]
            # print self.s_setjson
            print self.s_dict["registers"][0]["address"]

            # self.loadParaTable()

    def saveSettingfromJson(self):
        settingfile = "dimming_readback_parameters_frcxb_1.json"
        s_fp = open(settingfile, 'w+')
        if s_fp == False:
            print "error file!!!!"
        elif len(self.s_setjson) <= 1:
            print "read firstly !!!!"
        else:
            # s_fp.write("%s" % self.s_setjson)
            json.dump(self.s_setjson,s_fp,indent =4 )
            s_fp.close()

    def closeEvent(self, event):
        reply = QtGui.QMessageBox.question(self, 'Message', "Are you sure to quit?", QtGui.QMessageBox.Yes,
                                           QtGui.QMessageBox.No)
        if reply == QtGui.QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()


# class MyMplCanvas(FigureCanvas):
#     """Ultimately, this is a QWidget (as well as a FigureCanvasAgg, etc.)."""
#
#     def __init__(self, parent=None, width=5, height=4, dpi=100):
#         self.fig = Figure(figsize=(width, height), dpi=dpi)
#         self.axes = self.fig.add_subplot(111)
#         # We want the axes cleared every time plot() is called
#         self.axes.hold(False)
#
#         self.compute_initial_figure()
#
#         FigureCanvas.__init__(self, self.fig)
#         self.setParent(parent)
#
#         FigureCanvas.setSizePolicy(self,
#                                    QtGui.QSizePolicy.Expanding,
#                                    QtGui.QSizePolicy.Expanding)
#         FigureCanvas.updateGeometry(self)
#
#     def sizeHint(self):
#         w, h = self.get_width_height()
#         return QtCore.QSize(w, h)
#
#     def minimumSizeHint(self):
#         return QtCore.QSize(10, 10)


# class MyStaticMplCanvas(MyMplCanvas):
#     """Simple canvas with a sine plot."""
#
#     def compute_initial_figure(self):
#         t = np.arange(0.0, 3.0, 0.01)
#         s = np.sin(2 * np.pi * t)
#         self.axes.plot(t, s)


# class MyPlotDialog(QtGui.QDialog):
#     def __init__(self):
#         super(MyPlotDialog, self).__init__()
#         uic.loadUi("plot_it.ui", self)
#         self.setWindowIcon(QtGui.QIcon("222.ico"))
#         self.main_widget = QtGui.QWidget(self)
#
#         l = QtGui.QVBoxLayout(self.main_widget)
#         sc = MyStaticMplCanvas(self.main_widget, width=5, height=4, dpi=100)
#         l.addWidget(sc)
#         self.main_widget.setFocus()
#         # self.setCentralWidget(self.main_widget)
#
#     def closeEvent(self, event):
#         reply = QtGui.QMessageBox.question(self, 'Message', "Are you sure to quit?", QtGui.QMessageBox.Yes,
#                                            QtGui.QMessageBox.No)
#         if reply == QtGui.QMessageBox.Yes:
#             event.accept()
#         else:
#             event.ignore()


if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    with open("./darkero.qss") as f:
        s = f.read()
    app.setStyleSheet(s)
    splash = QtGui.QSplashScreen(pixmap=QtGui.QPixmap("images/sigma-logo.png"))
    splash.show()
    time.sleep(1)
    mywindow = MyWindow()
    mywindow.show()
    splash.finish(mywindow)
    sys.exit(app.exec_())
