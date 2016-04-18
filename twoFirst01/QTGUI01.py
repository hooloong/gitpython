__author__ = 'hooloongge'
import sys
import ctypes as C
import two01 as TFC
from dispmipsfunc import *
from PyQt4 import QtCore, QtGui


class Window(QtGui.QWidget):
    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        self.setWindowTitle("PyQt")
        self.resize(800, 600)
        hBoxLayout1 = QtGui.QHBoxLayout()

        label1 = QtGui.QLabel("Label1")
        label2 = QtGui.QLabel("Label2")
        label3 = QtGui.QLabel("Label3")
        label4 = QtGui.QLabel("Label4")
        label5 = QtGui.QLabel("Label5")

        gridLayout = QtGui.QGridLayout()

        gridLayout.addWidget( label1 , 0, 0 )
        gridLayout.addWidget( label2 , 0, 1 )
        gridLayout.addWidget( label3 , 0, 2 )
        gridLayout.addWidget( label4 , 1, 0 )
        gridLayout.addWidget( label5 , 1, 1 )

        self.setLayout( gridLayout )

        # hBoxLayout1.addWidget(label1)
        # hBoxLayout1.addWidget(label2)
        # hBoxLayout1.addWidget(label3)
        # hBoxLayout1.addWidget(label4)
        # hBoxLayout1.addWidget(label5)
        #
        # self.setLayout(hBoxLayout1)


# vBoxLayout = QtGui.QVBoxLayout()
#        vBoxLayout.addWidget( label1 )
#        vBoxLayout.addWidget( label2 )
#        vBoxLayout.addWidget( label3 )
#        vBoxLayout.addWidget( label4 )
#        vBoxLayout.addWidget( label5 )
#
#        self.setLayout( vBoxLayout )
#
app = QtGui.QApplication(sys.argv)
demo = Window()
demo.show()
app.exec_()