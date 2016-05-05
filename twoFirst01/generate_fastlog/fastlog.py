__author__ = 'hooloongge'
# -*- coding: utf-8 -*-
import sys, math, random, time
import ctypes as C
import xmltodict
import json
import ConfigParser
import numpy as np
from PyQt4 import QtCore, QtGui, uic, Qwt5



class MyWindow(QtGui.QMainWindow):
    def __init__(self):
        super(MyWindow, self).__init__()
        uic.loadUi("fastcopy_res.ui", self)
        self.setWindowIcon(QtGui.QIcon("222.ico"))
        # self.setGeometry(300,300,810,640)
        self.statusBar().showMessage('DisConnected to chip!!!')
        self.painter = QtGui.QPainter()

        self.s_dict = dict(defaultfilename="fc_parameters.json")

        self.pwm = np.zeros(64, np.uint32)

        for i in range(64):
            self.pwm[i] = random.randrange(100, 4095)


        print self.pwm
        # init tablewidget
        newItemt = QtGui.QTableWidgetItem('0')
        for i in range(self.tableWidget_PWM.rowCount()):
            for j in range(self.tableWidget_PWM.columnCount()):
                newItemt = QtGui.QTableWidgetItem('0')
                newItemt1 = QtGui.QTableWidgetItem('0')
                self.tableWidget_PWM.setItem(i, j, newItemt)



        #end table init
        self.actionQuit.connect(self.actionQuit, QtCore.SIGNAL('triggered()'), QtGui.qApp, QtCore.SLOT('quit()'))
        self.actionOpen_setting_file.connect(self.actionOpen_setting_file, QtCore.SIGNAL('triggered()'),
                                             self.loadSettingfromJson)
        self.actionSave_setting_file.connect(self.actionSave_setting_file, QtCore.SIGNAL('triggered()'),
                                             self.saveSettingfromJson)
        self.actionLoadInputFile.connect(self.actionLoadInputFile, QtCore.SIGNAL('triggered()'),
                                             self.showInputFileDialog)
        self.connect(self.pushButton_flushimg, QtCore.SIGNAL('clicked()'), self.update)
        self.loadSettingfromJson()



    def paintEvent(self, envent):
        self.painter.begin(self)
        startposx = self.tableWidget_Paras.x()
        startposy = self.tableWidget_Paras.y() + self.tableWidget_Paras.height() + 60
        for i in range(8):
            for j in range(8):
                var = self.pwm[j * self.tableWidget_Current.rowCount() + i]
                br = (var & 0xFFF) >> 4
                color = QtGui.QColor(br, br, br)
                self.painter.setBrush(color)
                self.painter.drawRect(startposx + i * 40, startposy + j * 30, 40, 30)
        self.painter.end()


    def loadParaTable(self):
        i = 1
        j = 0
        self.tableWidget_Paras.setRowCount(len(self.s_dict))
        for key in self.s_dict:
            # print key, self.s_dict[key]
            newItemh = QtGui.QTableWidgetItem(key)
            self.tableWidget_Paras.setVerticalHeaderItem(j, newItemh)
            str = "%d" % self.s_dict[key]
            newItemi = QtGui.QTableWidgetItem(str)
            self.tableWidget_Paras.setItem(j, 0, newItemi)
            i = i + 1
            j = j + 1

    def loadSettingfromJson(self):
        settingfile = "fc_parameters.json"
        s_fp = open(settingfile, 'r')
        if s_fp == False:
            print "error file!!!!"
        else:
            self.s_setjson = json.load(s_fp)
            s_fp.close()
            self.s_dict = self.s_setjson["parameters"]
            # print self.s_setjson
            # print self.s_dict
            self.loadParaTable()

    def saveSettingfromJson(self):
        settingfile = "parameters1.json"
        s_fp = open(settingfile, 'w+')
        if s_fp == False:
            print "error file!!!!"
        elif len(self.s_dict) == 1:
            print "read firstly !!!!"
        else:
            s_fp.write("%s" % self.s_setjson)
            s_fp.close()

    def showInputFileDialog(self):
        filename = QtGui.QFileDialog.getOpenFileName(self,'Open file','./')
        # file = open(filename)
        # data = file.read()
        # self.textedit.setText(data)




    def closeEvent(self, event):
        reply = QtGui.QMessageBox.question(self, 'Message', "Are you sure to quit?", QtGui.QMessageBox.Yes,
                                           QtGui.QMessageBox.No)
        if reply == QtGui.QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()


class Worker(QtCore.QThread):
    def __init__(self, parent=None):
        super(Worker, self).__init__(parent)
        self.working = True
        self.num = 0

    def __del__(self):
        self.working = False
        self.wait()

    def run(self):
        while self.working == True:
            file_str = 'File index {0}'.format(self.num)
            self.num += 1
            self.emit(SIGNAL('output(QString)'), file_str)
            self.sleep(3)




if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    mywindow = MyWindow()
    mywindow.show()
    sys.exit(app.exec_())
