__author__ = 'hooloongge'
import sys
from PyQt4 import  QtCore, QtGui

class SigSlot(QtGui.QWidget):
    def __init__(self,parent=None):
        QtGui.QWidget.__init__(self,parent)
        self.setWindowTitle("signal & slot")

        self.vbox1 = QtGui.QVBoxLayout()
        self.lcd1 =QtGui.QLCDNumber(self)
        self.slider1 = QtGui.QSlider(QtCore.Qt.Horizontal,self)

        self.vbox1.addWidget(self.lcd1)
        self.vbox1.addWidget(self.slider1)
        self.setLayout(self.vbox1)
        self.connect(self.slider1,QtCore.SIGNAL('valueChanged(int)'), self.lcd1,QtCore.SLOT('display(int)'))
        self.resize(350,300)


class Escape(QtGui.QWidget):
    def __init__(self,parent=None):
        QtGui.QWidget.__init__(self,parent)
        self.setWindowTitle("ESCAPE")
        self.resize(260,260)
        self.connect(self,QtCore.SIGNAL('closeEmitApp()'),QtCore.SLOT('close()'))

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Escape:
            self.close()
class Emit(QtGui.QWidget):
    def __init__(self,parent=None):
        QtGui.QWidget.__init__(self,parent)
        self.setWindowTitle("EMIT")
        self.resize(260,260)
        self.connect(self,QtCore.SIGNAL('closeEmitApp()'),QtCore.SLOT('close()'))

    def mousePressEvent(self, event):
        self.emit(QtCore.SIGNAL('closeEmitApp()'))
app = QtGui.QApplication( sys.argv )
# qb = SigSlot()
# qb=Escape()
qb = Emit()
qb.show()
sys.exit(app.exec_())

