__author__ = 'hooloongge'
import sys
from PyQt4 import  QtCore, QtGui

class CheckBox(QtGui.QWidget):
    def __init__(self,parent=None):
        QtGui.QWidget.__init__(self,parent)
        self.setWindowTitle("CheckBOx")

        self.setGeometry(300,300,350,80)
        self.cb = QtGui.QCheckBox('show title',self)
        self.cb.setFocusPolicy(QtCore.Qt.NoFocus)

        self.cb.move(20,20)
        self.cb.toggle()
        self.connect(self.cb,QtCore.SIGNAL('stateChanged(int)'),self.changeTitle)


    def changeTitle(self,value):
        if self.cb.isChecked():
            self.setWindowTitle('CheckBOX')
        else:
            self.setWindowTitle('UnChecked')

class ToggleButton(QtGui.QWidget):
    def __init__(self,parent=None):
        QtGui.QWidget.__init__(self,parent)
        self.setWindowTitle("ToggleButton")
        self.setGeometry(300,300,280,170)
        self.color = QtGui.QColor(255,0,0)
        self.red = QtGui.QPushButton('Red',self)
        self.red.setCheckable(True)
        self.red.move(10,10)
        self.connect(self.red,QtCore.SIGNAL('clicked()'),self.setRed)
        self.green = QtGui.QPushButton('Green',self)
        self.green.setCheckable(True)
        self.green.move(10,60)
        self.connect(self.green,QtCore.SIGNAL('clicked()'),self.setGreen)
        self.blue = QtGui.QPushButton('Blue',self)
        self.blue.setCheckable(True)
        self.blue.move(10,110)
        self.connect(self.blue,QtCore.SIGNAL('clicked()'),self.setBlue)

        self.square1 = QtGui.QWidget(self)
        self.square1.setGeometry(150,20,100,100)
        print "%s " % self.color.name()
        self.square1.setStyleSheet('Qwidget {background-color:%s}' % self.color.name())
        QtGui.QApplication.setStyle(QtGui.QStyleFactory.create('cleanlooks'))
    def setRed(self):
        if self.red.isChecked():
            self.color.setRed(255)
        else:
            self.color.setRed(0)
        self.square1.setStyleSheet('Qwidget {background-color:%s}' % self.color.name())
        print "%s " % self.color.name()
    def setGreen(self):
        if self.green.isChecked():
            self.color.setGreen(255)
        else:
            self.color.setGreen(0)
        self.square1.setStyleSheet('Qwidget {background-color:%s}' % self.color.name())
        print "%s " % self.color.name()
    def setBlue(self):
        if self.blue.isChecked():
            self.color.setBlue(255)
        else:
            self.color.setBlue(0)
        self.square1.setStyleSheet('Qwidget {background-color:%s}' % self.color.name())
        print "%s " % self.color.name()


app = QtGui.QApplication( sys.argv )

# qb = InputDailog()
# qb = CheckBox()
qb = ToggleButton()
qb.show()
sys.exit(app.exec_())

