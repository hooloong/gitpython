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
        self.setGeometry(400,400,380,370)
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
        self.square1.setStyleSheet('QWidget {background-color:%s}' % self.color.name())
        self.square1.setGeometry(100,100,100,100)
        print "%s " % self.color.name()

        QtGui.QApplication.setStyle(QtGui.QStyleFactory.create('cleanlooks'))
    def setRed(self):
        if self.red.isChecked():
            self.color.setRed(255)
        else:
            self.color.setRed(0)
        self.square1.setStyleSheet('QWidget {background-color:%s}' % self.color.name())
        print "%s " % self.color.name()
    def setGreen(self):
        if self.green.isChecked():
            self.color.setGreen(255)
        else:
            self.color.setGreen(0)
        self.square1.setStyleSheet('QWidget {background-color:%s}' % self.color.name())
        print "%s " % self.color.name()
    def setBlue(self):
        if self.blue.isChecked():
            self.color.setBlue(255)
        else:
            self.color.setBlue(0)
        self.square1.setStyleSheet('QWidget {background-color:%s}' % self.color.name())
        print "%s " % self.color.name()

class SliderLabel(QtGui.QWidget):
    def __init__(self,parent=None):
        QtGui.QWidget.__init__(self,parent)
        self.setWindowTitle("Silder and Label")

        self.setGeometry(300,300,350,80)
        self.slider = QtGui.QSlider(QtCore.Qt.Horizontal,self)
        self.slider.setFocusPolicy(QtCore.Qt.NoFocus)
        self.slider.setGeometry(30,40,100,30)
        self.connect(self.slider,QtCore.SIGNAL('valueChanged(int)'),self.changeValue)

        self.label = QtGui.QLabel(self)
        self.label.setPixmap(QtGui.QPixmap('222.ico'))
        self.label.setGeometry(160,40,80,30)


    def changeValue(self,value):
        pos = self.slider.value()
        if pos ==0:
            self.setWindowTitle('mute it"')
        elif 0<pos<30:
            self.setWindowTitle('normal 30')
        elif 30<pos<80:
            self.setWindowTitle('normal 80')
        else:
            self.setWindowTitle('normal high100')

class ProgressBar(QtGui.QWidget):
    def __init__(self,parent=None):
        QtGui.QWidget.__init__(self,parent)
        self.setWindowTitle("Progress Bar")
        self.setGeometry(300,300,350,300)
        self.setWindowIcon(QtGui.QIcon("222.ico"))
        self.pbar = QtGui.QProgressBar(self)
        self.pbar.setGeometry(30,40,200,25)

        self.button = QtGui.QPushButton('start',self)
        self.button.setFocusPolicy(QtCore.Qt.NoFocus)
        self.button.move(40,80)

        self.connect(self.button, QtCore.SIGNAL('clicked()'),self.onStart)
        self.timer = QtCore.QBasicTimer()
        self.step = 0

    def timerEvent(self,event):
        if self.step >=100:
            self.timer.stop()
            return
        self.step = self.step +1
        self.pbar.setValue(self.step)

    def onStart(self):
        if self.timer.isActive():
            self.timer.stop()
            self.button.setText('start')
        else:
            self.timer.start(100,self)
            self.button.setText('stop')
class Calendar(QtGui.QWidget):
    def __init__(self,parent=None):
        QtGui.QWidget.__init__(self,parent)
        self.setWindowTitle("Calendar ")
        self.setGeometry(300,300,350,300)
        self.setWindowIcon(QtGui.QIcon("222.ico"))
        self.cal = QtGui.QCalendarWidget(self)
        self.cal.setGridVisible(True)
        self.connect(self.cal,QtCore.SIGNAL('selectionChanged()'),self.showDate)

        self.label = QtGui.QLabel(self)
        date = self.cal.selectedDate()
        self.label.setText(str(date.toPyDate()))
        vbox = QtGui.QVBoxLayout()
        vbox.addWidget(self.cal)
        vbox.addWidget(self.label)
        self.setLayout(vbox)

    def showDate(self):
        date = self.cal.selectedDate()
        self.label.setText(str(date.toPyDate()))

app = QtGui.QApplication( sys.argv )

# qb = InputDailog()
# qb = CheckBox()
# qb = ToggleButton()
# qb = SliderLabel()
# qb = ProgressBar()
qb = Calendar()
qb.show()
sys.exit(app.exec_())

