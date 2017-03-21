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
from PyQt4 import QtCore, QtGui, uic  # ,Qwt5
# import dimmingdebugger_res_sx7
from dimmingdebugger_res_sx7 import *
from PWMs import *
from Hist import *
from TestPattern import *
# from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
# from matplotlib.figure import Figure
# from mpl_toolkits.mplot3d import Axes3D
# import matplotlib.pyplot as plt
# import ctypes as C
# import cProfile
# cProfile.run('main()')
# import logging


class MyWindow(QtGui.QMainWindow):

    def __init__(self):
        super(MyWindow, self).__init__()
        # uic.loadUi("dimmingdebugger_res.ui", self)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowIcon(QtGui.QIcon("222.ico"))
        # self.setGeometry(300,300,810,640)
        self.statusBar().showMessage('DisConnected to chip!!!')
        self.painter = QtGui.QPainter()

        self.ui.tabWidget.removeTab(0)

        self.formPWMs = PWMsWindow()
        self.ui.tabWidget.insertTab(0, self.formPWMs, u"PWMs")

        self.formHist = HistWindow()
        self.ui.tabWidget.insertTab(1, self.formHist, u"Hist")

        self.formTestPattern = TestPatternWindow()
        self.ui.tabWidget.insertTab(2, self.formTestPattern, u"TestPattern")

        self.s_dict = dict(defaultfilename="dimming_readback_parameters_sx7.json")

        self.connectFlag = False

        self.connect(self.ui.actionConnect, QtCore.SIGNAL('triggered()'), self.connectChip)
        self.connect(self.ui.actionDisconnect, QtCore.SIGNAL('triggered()'), self.disconnectChip)
        self.ui.actionQuit.connect(self.ui.actionQuit, QtCore.SIGNAL('triggered()'), QtGui.qApp, QtCore.SLOT('quit()'))
        self.ui.actionOpen_setting_file.connect(self.ui.actionOpen_setting_file, QtCore.SIGNAL('triggered()'),
                                             self.loadSettingfromJson)
        self.ui.actionSave_setting_file.connect(self.ui.actionSave_setting_file, QtCore.SIGNAL('triggered()'),
                                             self.saveSettingfromJson)

        self.loadSettingfromJson()


    def connectChip(self):
        config_read = ConfigParser.RawConfigParser()
        config_read.read("ChipDebugger.INI")
        eth_ip = config_read.get("Connection", "Ethernet.IP")
        self.connectFlag = TFC.TFCConnect2Chip()
        self.formPWMs.setConnectFlag(self.connectFlag)
        self.formHist.setConnectFlag(self.connectFlag)
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
        TFC.tfcConnTerm()
        self.setWindowTitle("Dimming Debugger     DisConnect..")

    def loadSettingfromJson(self):
        settingfile = "dimming_readback_parameters_sx7.json"
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
        settingfile = "dimming_readback_parameters_sx7_1.json"
        s_fp = open(settingfile, 'w+')
        if s_fp == False:
            print "error file!!!!"
        elif len(self.s_dict) == 1:
            print "read firstly !!!!"
        else:
            s_fp.write("%s" % self.s_setjson)
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
    mywindow = MyWindow()
    mywindow.show()
    sys.exit(app.exec_())