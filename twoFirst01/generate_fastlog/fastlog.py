__author__ = 'hooloongge'
# -*- coding: utf-8 -*-
import sys, random,string,struct,json
import numpy as np
from PyQt4 import QtCore, QtGui, uic

class MyWindow(QtGui.QMainWindow):
    def __init__(self):
        super(MyWindow, self).__init__()
        uic.loadUi("fastcopy_res.ui", self)
        self.gen_flag = False
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


        self.actionQuit.connect(self.actionQuit, QtCore.SIGNAL('triggered()'), QtGui.qApp, QtCore.SLOT('quit()'))
        self.actionOpen_setting_file.connect(self.actionOpen_setting_file, QtCore.SIGNAL('triggered()'),
                                             self.loadSettingfromJson)
        self.actionSave_setting_file.connect(self.actionSave_setting_file, QtCore.SIGNAL('triggered()'),
                                             self.saveSettingfromJson)
        self.actionLoadInputFile.connect(self.actionLoadInputFile, QtCore.SIGNAL('triggered()'),
                                             self.showInputFileDialog)
        self.connect(self.pushButton_flushimg, QtCore.SIGNAL('clicked()'), self.update)
        self.connect(self.pushButton_gen, QtCore.SIGNAL('clicked()'), self.generateOutput)
        self.connect(self.pushButton_curve, QtCore.SIGNAL('clicked()'), self.curveAdjust)
        self.loadSettingfromJson()
        self.PWMshowinTable()
        #line scale down function for frcxb fw.
    def scaleDownV(self,InWidth=24,InHeight=16,OutWidth=8,OutHeight=8):
        scale_max_buf = 24*16
        dwTempBuf = np.zeros(scale_max_buf, np.uint32)
        dwTempBuf1 = np.zeros(scale_max_buf, np.uint32)

        wHPara0 = np.zeros(scale_max_buf, np.uint32)
        wHpara1 = np.zeros(scale_max_buf, np.uint32)
        wVPara0 = np.zeros(scale_max_buf, np.uint32)
        wVPara1 = np.zeros(scale_max_buf, np.uint32)


        # HScalar start ...
        if InWidth > OutWidth > 0:
            StartPhase = InPos =0
            EndPhase = InWidth
            print InWidth,OutWidth
            for i in range(InWidth):
                if (StartPhase + OutWidth) < EndPhase:
                    wHPara0[InPos] = OutWidth
                    wHpara1[InPos] = 0
                else:
                    wHPara0[InPos] = EndPhase - StartPhase
                    wHpara1[InPos] = OutWidth - wHPara0[InPos]
                    if wHpara1[InPos] == 0:
                        wHpara1[InPos] = 0xFFFF
                    EndPhase = EndPhase + InWidth
                StartPhase = StartPhase + OutWidth
                InPos = i+1

            # print wHPara0
            # print wHpara1
            # print "H para -0-1"
            pInBuf = self.input.copy()
            pHOutBuf  = dwTempBuf
            pIs = 0
            PHs = 0

            for Row in range(InHeight):
                OutPos = 0
                pHOutBuf[PHs+0] = 0
                for InPos in range(InWidth):
                    pHOutBuf[PHs+OutPos] = pHOutBuf[PHs+OutPos] + wHPara0[InPos] * pInBuf[pIs+InPos]
                    if wHpara1[InPos]:
                        OutPos += 1
                        if wHpara1[InPos] == 0xFFFF:
                            pHOutBuf[PHs+OutPos] = 0
                        else:
                            pHOutBuf[PHs+OutPos] = wHpara1[InPos] * pInBuf[pIs+InPos]
                pIs += InWidth
                PHs += OutWidth
        #Hscaler end ....
        # print "pHoutbuf"
        # print pHOutBuf,dwTempBuf


        # Vscaler start ...
        print InHeight,OutHeight
        if InHeight > OutHeight  > 0:
            StartPhase = InPos = 0
            EndPhase = InHeight
            for j in range(InHeight):
                if (StartPhase + OutHeight) < EndPhase:
                    wVPara0[InPos] = OutHeight
                    wVPara1[InPos] = 0
                else:
                    wVPara0[InPos] = EndPhase - StartPhase
                    wVPara1[InPos] = OutHeight - wVPara0[InPos]
                    if wVPara1[InPos] == 0 :
                        wVPara1[InPos] = 0xFFFF
                    EndPhase += InHeight
                StartPhase += OutHeight
                InPos = j+1

            # print "V para 0 -1"
            # print wVPara1,wVPara0
            # pHOutBuf = dwTempBuf
            pVOutBuf = dwTempBuf1
            dwDivd = InWidth * InHeight
            for i in range(OutWidth):
                pVOutBuf[i] = 0
            pIs = 0
            POs = 0
            for Row in range(InHeight):
                for j in range(OutWidth):
                    pVOutBuf[pIs+j] += wVPara0[Row] * pHOutBuf[POs+j]
                if wVPara1[Row] > 0 :
                    for i in range(OutWidth):
                        pVOutBuf[pIs+i] /= dwDivd
                    pIs += OutWidth
                    if wVPara1[Row] != 0xFFFF:
                        for i in range(OutWidth):
                            pVOutBuf[pIs+j] = wVPara1[Row] * pHOutBuf[ POs+j]
                    else:
                        for i in range(OutWidth):
                            pVOutBuf[pIs+j] = 0
                POs += OutWidth
            for j in range(OutWidth*OutHeight):
                self.output[j] = pVOutBuf[j]
        print "output"
        print self.output


        pass
    def generateOutput(self):
        self.scaleDownV( self.s_dict["input_x"],self.s_dict["input_y"],self.s_dict["output_x"],self.s_dict["output_y"])
        self.gen_flag = True
        self.tableWidget_output.setRowCount(0)
        self.tableWidget_output.setColumnCount(0)
        self.tableWidget_output.setRowCount(self.s_dict["output_y"])
        self.tableWidget_output.setColumnCount(self.s_dict["output_x"])
        self.PWMshowinTable()
        self.update()

        pass
    def curveAdjust(self):
        curve_start = self.s_dict["curve_start"]
        curve_end = self.s_dict["pwm_max"]
        curve_cof = self.s_dict["curve_cof"]
        led_input_size =  self.s_dict["input_x"] * self.s_dict["input_y"]
        for i in range(led_input_size):
            if self.input[i]  < curve_end:
                self.input[i] = self.input[i] * curve_cof /10 + curve_start
            if  self.input[i] > curve_end:
                self.input[i] = curve_end
        self.PWMshowinTable()
        self.update()

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
        output_x = startposx
        output_y = startposy
        for i in range( 16):
            for j in range( 24):
                var = self.input[i * 24 + j]
                br = (var & 0xFFF) >> 4
                color = QtGui.QColor(br, br, br)
                self.painter.setBrush(color)
                self.painter.drawRect(startposx + j * 17, startposy + i * 17, 17, 17)
                output_x = startposx + j * 17  +17 +10
        if self.gen_flag:
            offsetx = 408 /self.s_dict["output_x"]
            offsety = 272/ self.s_dict["output_y"]
            for i in range( self.s_dict["output_y"]):
                for j in range( self.s_dict["output_x"]):
                    var = self.output[i * self.s_dict["output_x"] + j]
                    br = (var & 0xFFF) >> 4
                    color = QtGui.QColor(br, br, br)
                    self.painter.setBrush(color)
                    self.painter.drawRect(output_x + j * offsetx, output_y + i * offsety, offsetx, offsety)
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
            self.statusBar().showMessage("load "+ filename +" !")
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




if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    mywindow = MyWindow()
    mywindow.show()
    sys.exit(app.exec_())
