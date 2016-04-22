__author__ = 'hooloongge'
import sys
import ctypes as C
import two01 as TFC
import xmltodict
import time
from dispmipsfunc import *
from PyQt4 import  QtCore, QtGui,uic
class MyWindow( QtGui.QMainWindow ):
    def __init__( self ):
        super( MyWindow, self ).__init__()
        uic.loadUi( "dimmingdebugger.ui", self )
        self.setWindowIcon(QtGui.QIcon("222.ico"))
        self.setGeometry(300,300,810,640)
        self.statusBar().showMessage('DisConnect to chip!!!')
        self.connectFlag = 0
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
        self.connect(self.pushButton_readcurrent,QtCore.SIGNAL('clicked()'),self.readCurrent)
    def connectChip(self):
        self.connectFlag = TFC.TFCConnect2Chip()
        print("tfcConnInit returns ",self.connectFlag)
        if self.connectFlag:
             print("Connect to chip!!! ")
             self.statusBar().showMessage('"Connect to chip!!!')
             self.setWindowTitle("Dimming Debugger     Connect...")
        else:
            print("Could not Connect to chip!!! ")
            self.statusBar().showMessage('Could not Connect to chip!!!')
            self.setWindowTitle("Dimming Debugger     DisConnect..")
    def disconnectChip(self):
        self.connectFlag = False
        TFC.tfcConnTerm()
        self.setWindowTitle("Dimming Debugger     DisConnect..")
    def readPWM(self):
        #added read from registers
        for i in range(self.tableWidget_PWM.rowCount()):
            for j in range(self.tableWidget_PWM.columnCount()):
                TFC.tfc2ddWriteDword(0x68,0xA5)
                TFC.tfc2ddWriteDword(0x6C,i*self.tableWidget_PWM.rowCount() + j)
                time.sleep(0.05)
                var = TFC.tfc2ddReadDword(0x68) >> 8;
                pwmdutytemp = "%X" % (var & 0xFFF)
                newItemt = QtGui.QTableWidgetItem(pwmdutytemp)
                self.tableWidget_PWM.setItem(i,j,newItemt)

    def readCurrent(self):
        return
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
