__author__ = 'hooloongge'
#coding=utf-8
import sys
from PyQt4 import QtGui, QtCore, uic
class MyDialog( QtGui.QDialog ):
    def __init__( self ):
        super( MyDialog, self ).__init__()
        uic.loadUi( "res.ui", self )
        self.setWindowIcon(QtGui.QIcon("222.ico"))
    def closeEvent(self,event):
        reply = QtGui.QMessageBox.question(self, 'Message', "Are you sure to quit?", QtGui.QMessageBox.Yes, QtGui.QMessageBox.No)
        if reply== QtGui.QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

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

    def center(self):
        screen = QtGui.QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move((screen.width()-size.width())/2,(screen.height()-size.height())/2)
    def closeEvent(self, event):
        reply = QtGui.QMessageBox.question( self, 'Message',"Are you sure to quit?",QtGui.QMessageBox.Yes,QtGui.QMessageBox.No)
        if reply== QtGui.QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()
class MainWindow(QtGui.QMainWindow):
    def __init__(self,parent=None):
        QtGui.QMainWindow.__init__(self)
        self.window = MyWindow()
        self.setWindowTitle( "MainWindow" )
        self.resize( 300, 200 )
        self.setWindowIcon(QtGui.QIcon("222.ico"))
        self.statusBar().showMessage('Ready Go!!!')
        self.window.show()
        self.exit = QtGui.QAction(QtGui.QIcon('222.ico'),'Exit',self)
        self.exit.setShortcut('Ctrl+Q')
        self.exit.setStatusTip('Exit application')
        self.connect(self.exit,QtCore.SIGNAL('triggered()'),QtGui.qApp,QtCore.SLOT('quit()'))

        self.toolbar = self.addToolBar('Exit')

        self.toolbar.addAction(self.exit)
app = QtGui.QApplication( sys.argv )
demo = MainWindow()
demo.show()
app.exec_()