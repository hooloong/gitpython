__author__ = 'hooloongge'
# -*- coding: utf-8 -*-
import sys#, math, random, time
# import ctypes as C
import two01 as TFC
# import xmltodict
import json
import ConfigParser
# import numpy as np
from dispmipsfunc import *
from PyQt4 import QtCore, QtGui,QtSql, uic  # ,Qwt5
# import dimmingdebugger_res_sx7
from mainwindow_res import *
from UI_Debug import *
from Info import *
from SWPages import *
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
        #self.setWindowIcon(QtGui.QIcon("222.ico"))
        # self.setGeometry(300,300,810,640)
        self.statusBar().showMessage('DisConnected to chip!!!')
        self.painter = QtGui.QPainter()

        self.ui.tabWidget.removeTab(0)

        self.formUIDebug = UIDebugWindow()
        self.ui.tabWidget.insertTab(0, self.formUIDebug, u"UI_Debug")

        self.formInfo = InfoWindow()
        self.ui.tabWidget.insertTab(1, self.formInfo, u"Info")

        self.formSWPages = SWPagesWindow()
        self.ui.tabWidget.insertTab(2, self.formSWPages, u'SWPages')
        # print 'page size:', self.formSWPages.frameSize().height(), self.formSWPages.frameSize().width()

        # self.s_dict = dict(defaultfilename="dimming_readback_parameters_sx7.json")

        self.connectFlag = False
        self.bConnectionTried = False
        self.loadSettingfromJson()
        self.connect(self.ui.actionConnect, QtCore.SIGNAL('triggered()'), self.connectChip)
        self.connect(self.ui.actionDisconnect, QtCore.SIGNAL('triggered()'), self.disconnectChip)
        self.ui.actionQuit.connect(self.ui.actionQuit, QtCore.SIGNAL('triggered()'), QtGui.qApp, QtCore.SLOT('quit()'))
        self.ui.actionOpen_setting_file.connect(self.ui.actionOpen_setting_file, QtCore.SIGNAL('triggered()'),
                                             self.loadSettingfromJson)
        self.ui.actionSave_setting_file.connect(self.ui.actionSave_setting_file, QtCore.SIGNAL('triggered()'),
                                             self.saveSettingfromJson)
        self.connect(self.ui.tabWidget, QtCore.SIGNAL('currentChanged(int)'), self.tabchanges)
        self.setPanelInfo()

        self.resize(900, 730)

        qss_file = open('style.qss').read()
        self.setStyleSheet(qss_file)

    def tabchanges(self,index):
        if index == 4:
            self.resize(1180,760)
        elif index == 3:
            self.resize(960, 760)
        elif index == 2:
            self.resize(960, 760)
        elif index == 1:
            self.resize(900, 720)
        else:
            self.resize(900, 720)

    def setPanelInfo(self):
        return
        self.formTestPattern.setSettingDict(self.s_dict)
        self.formDimpages.setSettingDict(self.s_setjson["dim_pages"])
        pass
    def modifyIP(self, config_read):
        eth_ip = config_read.get("Connection", "Ethernet.IP")
        ip_addr, ok = QtGui.QInputDialog.getText(self, 'IP', 'Enter IP address:', text=eth_ip)
        if ok is False:
            return False
        elif ip_addr.isEmpty():
            QtGui.QMessageBox.information(self, "warning", ("Please enter IP address !!!"))
            return False
        elif ip_addr != eth_ip:
            try:
                config_read.set("Connection", "Ethernet.IP", ip_addr)
                config_read.write(open("ChipDebugger.INI", "r+"))
            except Exception, e:
                QtGui.QMessageBox.information(self, "Warning", str(e))
                return False
        return True
    def connectChip(self):
        config_read = ConfigParser.RawConfigParser()
        config_read.read("ChipDebugger.INI")
        connectType = config_read.get("Connection", "Type")
        if connectType == "Ethernet":
            if self.bConnectionTried is False:
                if self.modifyIP(config_read) is False:
                    return
        eth_ip = config_read.get("Connection", "Ethernet.IP")
        self.connectFlag = TFC.TFCConnect2Chip()
        self.bConnectionTried = True
        self.formUIDebug.setConnectFlag(self.connectFlag)
        self.formInfo.setConnectFlag(self.connectFlag)
        self.formSWPages.setConnectFlag(self.connectFlag)
        print("tfcConnInit returns ", self.connectFlag)
        if self.connectFlag:
            print("Connect to chip!!! ")
            self.statusBar().showMessage('"Connect to chip!!!')
            if connectType == "Ethernet":
                self.setWindowTitle("Debugger Tool" + "   " + "Connection" + "   " + eth_ip)
            else:
                self.setWindowTitle("Debugger Tool" + "   " + "Connection" + "   " + connectType)
        else:
            print("Could not Connect to chip!!! ")

            self.setWindowTitle("Debugger Tool" + "    " + "DisConnection")
            if connectType == "Ethernet":
                self.statusBar().showMessage('Could not Connect to ' + "   " + eth_ip + "!!!!")
                QtGui.QMessageBox.information(self, "warning", ('Could not connect to ' + " " + eth_ip + " !!!!"))
            else:
                QtGui.QMessageBox.information(self, "warning", ('Could not connect by ' + " " + connectType + " !!!!"))

    def disconnectChip(self):
        if self.connectFlag == False:
            return
        self.connectFlag = False
        self.formUIDebug.setConnectFlag(self.connectFlag)
        TFC.tfcConnTerm()
        self.setWindowTitle("Dimming Debugger     DisConnect..")

    def loadSettingfromJson(self):
        return
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
        return
        settingfile = "dimming_readback_parameters_sx7_1.json"
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
    mywindow = MyWindow()
    mywindow.show()
    sys.exit(app.exec_())
