__author__ = 'hooloongge'
import sys
import ctypes as C
import two01 as TFC
from dispmipsfunc import *
from PyQt4 import  QtCore, QtGui,uic
class MyWindow( QtGui.QMainWindow ):
    def __init__( self ):
        super( MyWindow, self ).__init__()
        uic.loadUi( "dimmingdebugger.ui", self )
        self.setWindowIcon(QtGui.QIcon("222.ico"))
    def closeEvent(self,event):
        reply = QtGui.QMessageBox.question(self, 'Message', "Are you sure to quit?", QtGui.QMessageBox.Yes, QtGui.QMessageBox.No)
        if reply== QtGui.QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()
app = QtGui.QApplication( sys.argv )
mywindow = MyWindow()
mywindow.show()
app.exec_()
