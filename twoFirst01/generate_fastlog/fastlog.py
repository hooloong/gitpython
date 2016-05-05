__author__ = 'hooloongge'
# -*- coding: utf-8 -*-
import sys, random,string,struct,json
import numpy as np
from PyQt4 import QtCore, QtGui, uic

class MyWindow(QtGui.QMainWindow):
    def __init__(self):
        super(MyWindow, self).__init__()
        uic.loadUi("fastcopy_res.ui", self)
        self.setWindowIcon(QtGui.QIcon("222.ico"))
        # self.setGeometry(300,300,810,640)
        self.statusBar().showMessage('Generated a fast logo array!!!')
        self.painter = QtGui.QPainter()

        self.s_dict = dict(defaultfilename="fc_parameters.json")

        self.input = np.zeros(512, np.uint32)
        self.output = np.zeros(512, np.uint32)
        self.rl_list = []
        for i in range(512):
            self.input[i] = random.randrange(100, 4095)


        print self.input
        # init tablewidget
        newItemt = QtGui.QTableWidgetItem('0')
        for i in range(self.tableWidget_input.rowCount()):
            for j in range(self.tableWidget_input.columnCount()):
                newItemt = QtGui.QTableWidgetItem('0')
                self.tableWidget_input.setItem(i, j, newItemt)


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
        self.PWMshowinTable()
    def PWMshowinTable(self):
        for i in range(self.tableWidget_input.rowCount()):
            for j in range(self.tableWidget_input.columnCount()):
                pwmdutytemp = "%X" % (self.input[i * self.tableWidget_input.columnCount() + j])

                newItemt = QtGui.QTableWidgetItem(pwmdutytemp)
                self.tableWidget_input.setItem(i, j, newItemt)
        for i in range(self.tableWidget_output.rowCount()):
            for j in range(self.tableWidget_output.columnCount()):
                currenttablevar = "%X" % (self.output[i * self.tableWidget_output.columnCount() + j])

                newItemt = QtGui.QTableWidgetItem(currenttablevar)
                self.tableWidget_output.setItem(i, j, newItemt)

    def paintEvent(self, envent):
        self.painter.begin(self)
        startposx = self.tableWidget_Paras.x()
        startposy = self.tableWidget_Paras.y() + self.tableWidget_Paras.height() + 60
        for i in range( 16):
            for j in range( 24):
                var = self.input[i * 24 + j]
                br = (var & 0xFFF) >> 4
                color = QtGui.QColor(br, br, br)
                self.painter.setBrush(color)
                self.painter.drawRect(startposx + j * 17, startposy + i * 17, 17, 17)
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
        settingfile = "fc_parameters.json"
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
        with open(filename,'r') as f:
            for line in f:
                line = line.strip()
                row_len = len(line)
                break;
            f.close()
        if row_len != 95:
            self.statusBar().showMessage("file "+ filename +"is not a right file!!")
            return
        else:
            self.statusBar().showMessage("load "+ filename +"!")
            col_num = (row_len +2)/4
            print col_num
        row_num = 0

        with open(filename,'r') as f:
            for line in f:
                line = line.strip()
                row_num += 1
                line_num = line.split(' ')
                self.rl_list = self.rl_list + line_num

        print len(self.rl_list),row_num
        num = 0
        for it in self.rl_list:
            self.input[num] = string.atoi(self.rl_list[num],base=16)
            num = num +1
        # print self.input
        self.PWMshowinTable()
        self.update()
        # data = np.loadtxt(filename,dtype="string",delimiter=" ")



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
