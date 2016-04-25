__author__ = 'hooloongge'
#coding=utf-8
import sys
from PyQt4 import QtGui, QtCore, uic
class MyDialog( QtGui.QDialog ):
    def __init__( self ):
        super( MyDialog, self ).__init__()
        uic.loadUi( "res.ui", self )
        self.setWindowIcon(QtGui.QIcon("222.ico"))

class MyWindow( QtGui.QWidget ):
    def __init__( self ):
        super( MyWindow, self ).__init__()
        self.setWindowTitle( "hello testing" )
        self.resize( 300, 200 )
        self.setWindowIcon(QtGui.QIcon("222.ico"))
        self.setToolTip("this is a tooltip for <b>qt4</b> testing")
        QtGui.QToolTip.setFont( QtGui.QFont('OldEnglish',10) )

        gridlayout = QtGui.QGridLayout()
        self.button = QtGui.QPushButton( "CreateDialog" )
        self.button1 = QtGui.QPushButton( "close" )
        gridlayout.addWidget( self.button )
        gridlayout.addWidget( self.button1 )
        self.setLayout( gridlayout )

        self.connect( self.button, QtCore.SIGNAL( 'clicked()' ), self.OnButtoN )
        self.connect( self.button1, QtCore.SIGNAL( 'clicked()' ),QtGui.qApp,QtCore.SLOT('quit()') )
    def OnButtoN( self ):
        dialog = MyDialog()
        r = dialog.exec_();
        if r:
            self.button.setText( dialog.lineEdit.text() )

app = QtGui.QApplication( sys.argv )
demo = MyWindow()
demo.show()
app.exec_()