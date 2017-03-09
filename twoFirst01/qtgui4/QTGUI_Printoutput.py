from __future__ import print_function
from PyQt4 import QtGui, QtCore
import threading, time
# from __future__ import print_function

class sy(QtGui.QWidget):
    txt_signal = QtCore.pyqtSignal(str)

    def __init__(self, parent=None):
        self.app = QtGui.QApplication([])
        super(sy, self).__init__(parent)
        self.txt = QtGui.QTextEdit()
        lay = QtGui.QVBoxLayout()
        self.txt_signal.connect(self.writetoTextbox)
        lay.addWidget(self.txt)
        self.setLayout(lay)

    def main(self):
        self.show()
        self.app.exec_()

    def write(self, s):
        self.txt_signal.emit(s)

    @QtCore.pyqtSlot(str)
    def writetoTextbox(self, text):
        self.txt.append(text)


def PrintSomething(stream):
    time.sleep(3)
    print('hello world', file = stream, end = "Yes,it's a test!")

if __name__ == '__main__':
    s = sy()
    t = threading.Thread(target=PrintSomething, args=(s,))
    t.start()
    s.main()