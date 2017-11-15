from dispmipsfunc import *
from PyQt4 import QtCore, QtGui, uic  # ,Qwt5
from Info_res import *
import json

class InfoWindow(QtGui.QMainWindow):

    def __init__(self):
        super(InfoWindow, self).__init__()
        self.ui = Ui_Form_Info()
        self.ui.setupUi(self)

        self.connectFlag = False

        settingfile = "UI_Debug_parameters.json"
        s_fp = open(settingfile, 'r')
        if s_fp == False:
            print "error file!!!!"
            self.readJson = False
        else:
            self.s_setjson = json.load(s_fp)
            s_fp.close()
            self.info = self.s_setjson["Info"]
            self.readJsonFlag = True

        self.connect(self.ui.pushButton_read, QtCore.SIGNAL('clicked()'), self.read)

    def setConnectFlag(self, flag):
        self.connectFlag = flag

    def read(self):
        if self.readJsonFlag is False:
            QtGui.QMessageBox.information(self, "warning", ("need input a valid json file!!!\n"))
            return
        elif self.connectFlag is False:
            QtGui.QMessageBox.information(self, "warning", ("Please connect to chip first!!!\n Setting->Connect"))
            return
        if self.info.has_key("MainTSE"):
            reg = int(self.info["MainTSE"], 16)
            value = (TFC.tfcReadDword(reg, 0))
            text = "0x%x" % value
            self.ui.lineEdit_MainTSE.setText(text)
        if self.info.has_key("PQMainTSE"):
            reg = int(self.info["PQMainTSE"], 16)
            value = (TFC.tfcReadDword(reg, 0))
            text = "0x%x" % value
            self.ui.lineEdit_PQMainTSE.setText(text)
        if self.info.has_key("AttributeTSE"):
            reg = int(self.info["AttributeTSE"], 16)
            value = (TFC.tfcReadDword(reg, 0))
            text = "0x%x" % value
            self.ui.lineEdit_AttributeTSE.setText(text)
        if self.info.has_key("TableTSE"):
            reg = int(self.info["TableTSE"], 16)
            value = (TFC.tfcReadDword(reg, 0))
            text = "0x%x" % value
            self.ui.lineEdit_TableTSE.setText(text)
        if self.info.has_key("PQPanelTSE"):
            reg = int(self.info["PQPanelTSE"], 16)
            value = (TFC.tfcReadDword(reg, 0))
            text = "0x%x" % value
            self.ui.lineEdit_PQPanelTSE.setText(text)
        if self.info.has_key("PQCustomTSE"):
            reg = int(self.info["PQCustomTSE"], 16)
            value = (TFC.tfcReadDword(reg, 0))
            text = "0x%x" % value
            self.ui.lineEdit_PQCustomTSE.setText(text)
        if self.info.has_key("PanelID"):
            reg = int(self.info["PanelID"], 16)
            value = (TFC.tfcReadDword(reg, 0))
            text = "0x%x" % value
            self.ui.lineEdit_PanelID.setText(text)

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    mywindow = UIDebugWindow()
    mywindow.show()
    sys.exit(app.exec_())