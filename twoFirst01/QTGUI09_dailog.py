__author__ = 'hooloongge'
import sys
from PyQt4 import  QtCore, QtGui

class InputDailog(QtGui.QWidget):
    def __init__(self,parent=None):
        QtGui.QWidget.__init__(self,parent)
        self.setWindowTitle("Input dailog")

        self.setGeometry(300,300,350,80)
        self.button = QtGui.QPushButton('Dialog',self)
        self.button.setFocusPolicy(QtCore.Qt.NoFocus)

        self.button.move(20,20)
        self.connect(self.button,QtCore.SIGNAL('clicked()'),self.showDialog)
        self.setFocus()

        self.label = QtGui.QLineEdit(self)
        self.label.move(130,22)
        # self.resize(350,300)

    def showDialog(self):
        text,ok = QtGui.QInputDialog.getText(self,'Input Dailog','Enter your name')
        if ok:
            self.label.setText(unicode(text))

class ColorDialog(QtGui.QWidget):
    def __init__(self,parent=None):
        QtGui.QWidget.__init__(self,parent)
        self.setWindowTitle("Color dailog")
        color = QtGui.QColor(0,0,0)
        self.setGeometry(300,300,250,180)

        self.button = QtGui.QPushButton('Dialog',self)
        self.button.setFocusPolicy(QtCore.Qt.NoFocus)
        self.button.move(20,20)

        self.connect(self.button,QtCore.SIGNAL('clicked()'),self.showDialog)
        self.setFocus()
        print "%s " % color.name()
        self.widget = QtGui.QWidget(self)
        self.widget.setStyleSheet('QWidget {background-color:%s}' % color.name())
        self.widget.setGeometry(130,22,100,100)

        # self.resize(350,300)

    def showDialog(self):
        col = QtGui.QColorDialog.getColor()
        print "%s" % col.name()
        if col.isValid():
             self.widget.setStyleSheet('QWidget {background-color:%s}' % col.name())



app = QtGui.QApplication( sys.argv )

# qb = InputDailog()
qb = ColorDialog()
qb.show()
sys.exit(app.exec_())

