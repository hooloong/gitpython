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

class FileDailog(QtGui.QMainWindow):
    def __init__(self,parent=None):
        QtGui.QWidget.__init__(self,parent)
        self.setWindowTitle("File dailog")

        self.setGeometry(300,300,250,180)

        self.textedit = QtGui.QTextEdit()
        self.setCentralWidget(self.textedit)
        self.statusBar()
        self.setFocus()

        exit = QtGui.QAction(QtGui.QIcon("222.ico"),'Open',self)
        exit.setShortcut('Ctrl+O')
        exit.setStatusTip('Open new file')

        self.connect(exit,QtCore.SIGNAL('triggered()'),self.showDialog)

        menubar = self.menuBar()
        file = menubar.addMenu('&File')
        file.addAction(exit)

    def showDialog(self):
        filename = QtGui.QFileDialog.getOpenFileName(self,'Open file','./')
        file = open(filename)
        data = file.read()
        self.textedit.setText(data)

class FontDailog(QtGui.QWidget):
    def __init__(self,parent=None):
        QtGui.QWidget.__init__(self,parent)
        self.setWindowTitle("font dailog")
        self.setGeometry(300,300,250,180)
        hbox = QtGui.QHBoxLayout()
        self.button = QtGui.QPushButton('font',self)
        self.button.setFocusPolicy(QtCore.Qt.NoFocus)
        self.button.move(20,20)
        hbox.addWidget(self.button)
        self.connect(self.button,QtCore.SIGNAL('clicked()'),self.showDialog)
        self.setFocus()

        self.label = QtGui.QLabel("Knowlege only matterss",self)
        self.label.move(130,20)

        hbox.addWidget(self.label,1)
        self.setLayout(hbox)

        # self.resize(350,300)

    def showDialog(self):
        font,ok = QtGui.QFontDialog.getFont()
        print "font:%s" % font
        if ok:
             self.label.setFont(font)


app = QtGui.QApplication( sys.argv )

# qb = InputDailog()
# qb = ColorDialog()
# qb = FileDailog()
qb = FontDailog()
qb.show()
sys.exit(app.exec_())

