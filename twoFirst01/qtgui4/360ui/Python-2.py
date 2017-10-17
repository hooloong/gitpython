from PyQt4 import QtGui, QtCore

app = QtGui.QApplication([])

w = QtGui.QWidget()

def showMsg():
    QtGui.QMessageBox.information(w, u"Info", u"ok")

btn = QtGui.QPushButton(u"click", w)
#w.connect(btn, QtCore.SIGNAL("clicked()"), showMsg)
btn.clicked.connect(showMsg)

w.show()
app.exec_()