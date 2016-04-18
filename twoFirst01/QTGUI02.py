__author__ = 'hooloongge'
#coding=utf-8
import sys
from PyQt4 import QtGui, QtCore, uic
class MyDialog( QtGui.QDialog ):
    def __init__( self ):
        super( MyDialog, self ).__init__()
        uic.loadUi( "res.ui", self )

class MyWindow( QtGui.QWidget ):
    def __init__( self ):
        super( MyWindow, self ).__init__()
        self.setWindowTitle( "hello" )
        self.resize( 300, 200 )

        gridlayout = QtGui.QGridLayout()
        self.button = QtGui.QPushButton( "CreateDialog" )
        gridlayout.addWidget( self.button )
        self.setLayout( gridlayout )

        self.connect( self.button, QtCore.SIGNAL( 'clicked()' ), self.OnButtoN )

    def OnButtoN( self ):
        dialog = MyDialog()
        r = dialog.exec_();
        if r:
            self.button.setText( dialog.lineEdit.text() )

app = QtGui.QApplication( sys.argv )
demo = MyWindow()
demo.show()
app.exec_()