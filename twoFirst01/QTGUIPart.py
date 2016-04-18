__author__ = 'hooloongge'
import sys
import ctypes as C
import two01 as TFC
from dispmipsfunc import *
from PyQt4 import  QtCore, QtGui
class MyWindow( QtGui.QMainWindow ):
    def __init__( self ):
        QtGui.QMainWindow.__init__( self )
        self.setWindowTitle( "PyQt" )
        self.resize( 500,500 )
        label = QtGui.QLabel( "label" )
        label.setAlignment( QtCore.Qt.AlignCenter )
        self.setCentralWidget( label )
app = QtGui.QApplication( sys.argv )
mywindow = MyWindow()
mywindow.show()
app.exec_()