__author__ = 'hooloongge'
import sys
import ctypes as C
import two01 as TFC
import xmltodict
import time
import numpy as np
from dispmipsfunc import *
from PyQt4 import  QtCore, QtGui,uic,Qwt5
class MyWindow( QtGui.QMainWindow ):
    def __init__( self ):
        super( MyWindow, self ).__init__()
        uic.loadUi( "dimmingdebugger.ui", self )
        self.setWindowIcon(QtGui.QIcon("222.ico"))
        self.setGeometry(300,300,810,640)
        self.statusBar().showMessage('DisConnected to chip!!!')
        self.connectFlag = 0
        self.pwm = np.zeros(32)
        self.pwm.dtype = np.uint32
        self.current = np.zeros(32)
        self.current.dtype = np.uint32
        print self.pwm
        #init tablewidget
        newItemt = QtGui.QTableWidgetItem('0')
        for i in range(self.tableWidget_PWM.rowCount()):
            for j in range(self.tableWidget_PWM.columnCount()):
                newItemt = QtGui.QTableWidgetItem('0')
                self.tableWidget_PWM.setItem(i,j,newItemt)
        for i in range(self.tableWidget_Current.rowCount()):
            for j in range(self.tableWidget_Current.columnCount()):
                newItemt = QtGui.QTableWidgetItem('0')
                self.tableWidget_Current.setItem(i,j,newItemt)
        #end table init
        self.connect(self.actionConnect,QtCore.SIGNAL('triggered()'),self.connectChip)
        self.connect(self.actionDisconnect,QtCore.SIGNAL('triggered()'),self.disconnectChip)
        self.connect(self.pushButton_readpwm,QtCore.SIGNAL('clicked()'),self.readPWM)
        self.connect(self.pushButton_readpwm,QtCore.SIGNAL('pressed()'),self.changeText_pwm)
        self.connect(self.pushButton_readcurrent,QtCore.SIGNAL('pressed()'),self.changeText_current)
        self.connect(self.pushButton_readcurrent,QtCore.SIGNAL('clicked()'),self.readCurrent)
    def connectChip(self):
        self.connectFlag = TFC.TFCConnect2Chip()
        print("tfcConnInit returns ",self.connectFlag)
        if self.connectFlag:
             print("Connect to chip!!! ")
             self.statusBar().showMessage('"Connect to chip!!!')
             self.setWindowTitle("Dimming Debugger     Connection")
        else:
            print("Could not Connect to chip!!! ")
            self.statusBar().showMessage('Could not Connect to chip!!!')
            self.setWindowTitle("Dimming Debugger     DisConnection")
    def disconnectChip(self):
        if self.connectFlag == False:
            return
        self.connectFlag = False
        TFC.tfcConnTerm()
        self.setWindowTitle("Dimming Debugger     DisConnect..")
    def changeText_pwm(self):
        if self.connectFlag == False:
            return
        self.pushButton_readpwm.setText("Reading")
    def changeText_current(self):
        if self.connectFlag == False:
            return
        self.pushButton_readcurrent.setText("Reading")
    def readPWM(self):
        #added read from registers
        if self.connectFlag == False:
            return
        for i in range(self.tableWidget_PWM.rowCount()):
            for j in range(self.tableWidget_PWM.columnCount()):
                TFC.tfc2ddWriteDword(0x68,0xA5)
                TFC.tfc2ddWriteDword(0x6C,i*self.tableWidget_PWM.rowCount() + j)
                time.sleep(0.05)
                var = TFC.tfc2ddReadDword(0x68) >> 8;
                self.pwm[i*self.tableWidget_PWM.rowCount() + j] = var & 0xFFF
                pwmdutytemp = "%X" % (var & 0xFFF)
                newItemt = QtGui.QTableWidgetItem(pwmdutytemp)
                self.tableWidget_PWM.setItem(i,j,newItemt)
        self.pushButton_readpwm.setText("ReadPWM")
        # print self.pushButton_readpwm.text
        print self.pwm
    def readCurrent(self):
        if self.connectFlag == False:
            return
        for i in range(self.tableWidget_Current.rowCount()):
            for j in range(self.tableWidget_Current.columnCount()):
                TFC.tfc2ddWriteDword(0x68,0xA5)
                TFC.tfc2ddWriteDword(0x6C,i*self.tableWidget_Current.rowCount() + j)
                time.sleep(0.05)
                var = TFC.tfc2ddReadDword(0x68) >> 8;
                self.current[i*self.tableWidget_Current.rowCount() + j] = var & 0xFFF
                pwmdutytemp = "%X" % (var & 0xFFF)
                newItemt = QtGui.QTableWidgetItem(pwmdutytemp)
                self.tableWidget_Current.setItem(i,j,newItemt)
        self.pushButton_readcurrent.setText("ReadCurrent")
        # print self.pushButton_readcurrent.text
        print self.current

    def closeEvent(self,event):
        reply = QtGui.QMessageBox.question(self, 'Message', "Are you sure to quit?", QtGui.QMessageBox.Yes, QtGui.QMessageBox.No)
        if reply== QtGui.QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()
if __name__ == "__main__":
    app = QtGui.QApplication( sys.argv )
    mywindow = MyWindow()
    mywindow.show()
    app.exec_()
