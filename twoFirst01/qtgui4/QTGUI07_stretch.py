__author__ = 'hooloongge'
import sys
from PyQt4 import  QtCore, QtGui
class Absolute( QtGui.QWidget ):
    def __init__( self,parent=None ):
        QtGui.QWidget.__init__( self )
        self.setWindowTitle( "Communication" )

        label = QtGui.QLabel( "Could\'t",self )
        label.move(15,10)
        label = QtGui.QLabel( "care" ,self)
        label.move(35,40)
        label = QtGui.QLabel( "less" ,self)
        label.move(55,65)
        label = QtGui.QLabel( "And" ,self)
        label.move(115,65)
        label = QtGui.QLabel( "then" ,self)
        label.move(135,45)
        label = QtGui.QLabel( "you" ,self)
        label.move(115,25)
        label = QtGui.QLabel( "kissed" ,self)
        label.move(145,10)
        label = QtGui.QLabel( "me" ,self)
        label.move(215,10)
        self.resize( 250,150 )
class BoxLayout(QtGui.QWidget):
    def __init__(self,parent=None):
        QtGui.QWidget.__init__(self)
        self.setWindowTitle("Box_layout")

        ok = QtGui.QPushButton("OK!")
        cancela = QtGui.QPushButton("Cancel!")

        hbox = QtGui.QHBoxLayout()
        hbox.addStretch(1)
        hbox.addWidget(ok)
        hbox.addWidget(cancela)

        vbox = QtGui.QVBoxLayout()
        vbox.addStretch(1)
        vbox.addLayout(hbox)

        self.setLayout(vbox)
        self.resize(300,150)

class GridLayout1(QtGui.QWidget):
    def __init__(self,parent=None):
        QtGui.QWidget.__init__(self)
        self.setWindowTitle("Grid_layout")

        bnames = ['Cls','Bck','','Close','7','8','9','/','4','5','6','*','1','2','3','-','0','.','=','+']
        grid = QtGui.QGridLayout()
        j = 0
        pos = [(0,0),(0,1),(0,2),(0,3),(1,0),(1,1),(1,2),(1,3),(2,0),(2,1),(2,2),(2,3),(3,0),(3,1),(3,2),(3,3),(4,0),(4,1),(4,2),(4,3),(4,4)]

        for i in bnames:
            button = QtGui.QPushButton(i)
            if j == 2:
                grid.addWidget(QtGui.QLabel(""),0,2)
            else:
                grid.addWidget(button,pos[j][0],pos[j][1])
            j=j+1

        self.setLayout(grid)
class GridLayout(QtGui.QWidget):
    def __init__(self,parent=None):
        QtGui.QWidget.__init__(self)
        self.setWindowTitle("Grid_layout")

        bnames = ['Cls','Bck','','Close','7','8','9','/','4','5','6','*','1','2','3','-','0','.','=','+']
        grid = QtGui.QGridLayout()

        title = QtGui.QLabel("Title")
        author = QtGui.QLabel("Author")
        review = QtGui.QLabel("Review")

        titleEdit = QtGui.QLineEdit()
        authorEdit = QtGui.QLineEdit()
        reviewEdit = QtGui.QLineEdit()

        grid.setSpacing(10)

        grid.addWidget(title,1,0)
        grid.addWidget(titleEdit,1,1)

        grid.addWidget(author,2,0)
        grid.addWidget(authorEdit,2,1)

        grid.addWidget(review,3,0)
        grid.addWidget(reviewEdit,3,1,5,1)
        self.setLayout(grid)

        self.resize(350,300)
app = QtGui.QApplication( sys.argv )

# qb = Absolute()
# qb = BoxLayout()
qb = GridLayout()
qb.show()
sys.exit(app.exec_())
