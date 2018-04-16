from dispmipsfunc import *
from PyQt4 import QtCore, QtGui, uic  # ,Qwt5
from Info_res import *
import json
import csv

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
            if self.s_setjson.has_key("SWPages"):
                if self.s_setjson["SWPages"].has_key("csvFile"):
                    self.filename = self.s_setjson["SWPages"]["csvFile"]
                else:
                    QtGui.QMessageBox.information(self, "warning",
                                                  ("no 'csvFile' info in 'SWPages' of file: %s" % (settingfile)))
                    return
            else:
                QtGui.QMessageBox.information(self, "warning",
                                              ('''No SWPages info in file '%s', please add below info in the file.
                                               \n"SWPages":{\n         "csvFile":"filename.csv"\n}''' % (settingfile)))
                return
            self.debugRegs = {}
            self.readJsonFlag = self.loadDebugRegsAddr()

        self.connect(self.ui.pushButton_read, QtCore.SIGNAL('clicked()'), self.read)

    def setConnectFlag(self, flag):
        self.connectFlag = flag

    def getRegAddr(self, regName):
        return self.debugRegs[regName]

    def loadDebugRegsAddr(self):
        for key in self.info:
            regName = self.info[key]
            self.debugRegs[regName] = 0

        if self.loadSWRegFromFile(self.filename, self.debugRegs) is False:
            return False

        for key in self.debugRegs:
            # print key, '0x%x' %(self.debugRegs[key])
            if self.debugRegs[key] is 0:
                QtGui.QMessageBox.information(self, "warning",
                                              ("Haven't found reg %s in csv file!!!!" % (key)))
                return False
        return True

    def loadSWRegFromFile(self, file, debugRegs):
        try:
            if file.endswith('.csv') is False:
                QtGui.QMessageBox.information(self, "warning", ("%s is not csv file!!!\nPlease input csv file!!!" %(file)))
                return False
            with open(file, "r") as csvFile:
                reader = csv.reader(csvFile)
                for item in reader:
                    if reader.line_num == 1:
                        header = {'Address':'', 'Register Name':''}
                        if False == set(header.keys()).issubset(item):
                            return False
                        for i in range(len(item)):
                            for key in header:
                                if key == item[i]: header[key] = i
                    else:
                        regname = str(item[header['Register Name']].replace(' ', ''))
                        regaddr = int(item[header['Address']].replace('_', ''), 16)
                        if regname in debugRegs:
                            debugRegs[regname] = regaddr
                            continue
                # self.initFlag = True
        except IOError as e:
            QtGui.QMessageBox.information(self, "warning", ('%s' % (e)))
        except csv.Error as e:
            QtGui.QMessageBox.information(self, "warning", ('file %s: %s' % (file, e)))
        return True

    def read(self):
        if self.readJsonFlag is False:
            QtGui.QMessageBox.information(self, "warning", ("need input valid json file and csv file!!!\n"))
            return
        elif self.connectFlag is False:
            QtGui.QMessageBox.information(self, "warning", ("Please connect to chip first!!!\n Setting->Connect"))
            return
        if self.info.has_key("MainTSE"):
            reg = self.getRegAddr(self.info["MainTSE"])
            value = (TFC.tfcReadDword(reg, 0))
            text = "0x%x" % value
            self.ui.lineEdit_MainTSE.setText(text)
        if self.info.has_key("PQMainTSE"):
            reg = self.getRegAddr(self.info["PQMainTSE"])
            value = (TFC.tfcReadDword(reg, 0))
            text = "0x%x" % value
            self.ui.lineEdit_PQMainTSE.setText(text)
        if self.info.has_key("AttributeTSE"):
            reg = self.getRegAddr(self.info["AttributeTSE"])
            value = (TFC.tfcReadDword(reg, 0))
            text = "0x%x" % value
            self.ui.lineEdit_AttributeTSE.setText(text)
        if self.info.has_key("TableTSE"):
            reg = self.getRegAddr(self.info["TableTSE"])
            value = (TFC.tfcReadDword(reg, 0))
            text = "0x%x" % value
            self.ui.lineEdit_TableTSE.setText(text)
        if self.info.has_key("PQPanelTSE"):
            reg = self.getRegAddr(self.info["PQPanelTSE"])
            value = (TFC.tfcReadDword(reg, 0))
            text = "0x%x" % value
            self.ui.lineEdit_PQPanelTSE.setText(text)
        if self.info.has_key("PQCustomTSE"):
            reg = self.getRegAddr(self.info["PQCustomTSE"])
            value = (TFC.tfcReadDword(reg, 0))
            text = "0x%x" % value
            self.ui.lineEdit_PQCustomTSE.setText(text)
        if self.info.has_key("PanelID"):
            reg = self.getRegAddr(self.info["PanelID"])
            value = (TFC.tfcReadDword(reg, 0))
            text = "0x%x" % value
            self.ui.lineEdit_PanelID.setText(text)

if __name__ == "__main__":
    # app = QtGui.QApplication(sys.argv)
    mywindow = InfoWindow()
    mywindow.show()
    # sys.exit(app.exec_())