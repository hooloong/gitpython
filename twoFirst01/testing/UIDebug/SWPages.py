# -*- coding: utf-8 -*-
import sys
import csv
import numpy as np
import os
import json
from PyQt4 import QtCore, QtGui, uic  # ,Qwt5
import two01 as TFC
from dispmipsfunc import *
from SWPages_res import *

#filename = "SX8_V_SW_REG_SPG.csv"
ADDRSTEP = int(4)
CURPAGESIZE = int(64)
bits_label_list = ["7","6","5","4","3","2","1","0","15","14","13","12","11","10","9","8",
                   "23","22","21","20","19","18","17","16","31","30","29","28","27","26","25","24"]
COLADDR = 0
COLNAME = 1
COLVAL = 2

class regs():
    def __init__(self, index, name, descr, right, baseaddr, value=0):
        self.index = index
        self.name = name
        self.descr = descr
        # if 'R/W' == item[header['R/W']]:
        #     regright = 3
        # elif 'W' == item[header['R/W']]:
        #     regright = 2
        # elif 'R' == item[header['R/W']]:
        #     regright = 1
        # else:
        #     regright = 0
        self.right = right
        self.baseaddr = baseaddr
        self.regAddr = baseaddr + 4 * index
        self.value = value

    def refreshVal(self, value):
        self.value = value


class SWPagesWindow(QtGui.QMainWindow):
    def __init__(self):
        super(SWPagesWindow, self).__init__()
        self.ui = Ui_Form_Pages()
        self.ui.setupUi(self)
        self.pages = {}
        self.initFlag = False
        self.connectFlag = False
        self.curchipreadflag = False

        self.initData()

        self.connect(self.ui.pushButton_Convert, QtCore.SIGNAL('clicked()'), self.ConvertCsv2VirtualRegListFiles)

        self.ui.treeWidget_pages.itemPressed.connect(self.pageSel)

        self.connect(self.ui.tableWidget_curpage, QtCore.SIGNAL('cellPressed(int,int)'), self.changeRegDescri)
        self.ui.tableWidget_curpage.itemChanged.connect(self.tableItemChanged)

        # self.connect(self.ui.pushButton_getitem, QtCore.SIGNAL('clicked()'), self.printoutregs)
        self.connect(self.ui.pushButton_readpage, QtCore.SIGNAL('clicked()'), self.readCurPageRegs)
        self.connect(self.ui.pushButton_writepage, QtCore.SIGNAL('clicked()'), self.writeCurpPageRegs)
        self.connect(self.ui.pushButton_refresh, QtCore.SIGNAL('clicked()'), self.readCurPageRegs)

        self.connect(self.ui.radioButton_7, QtCore.SIGNAL('clicked(bool)'), self.changeBitsel)
        self.connect(self.ui.radioButton_15, QtCore.SIGNAL('clicked(bool)'), self.changeBitsel)
        self.connect(self.ui.radioButton_23, QtCore.SIGNAL('clicked(bool)'), self.changeBitsel)
        self.connect(self.ui.radioButton_31, QtCore.SIGNAL('clicked(bool)'), self.changeBitsel)
        self.connect(self.ui.checkBox_0, QtCore.SIGNAL('clicked()'), self.setBitCheckbox)
        self.connect(self.ui.checkBox_1, QtCore.SIGNAL('clicked()'), self.setBitCheckbox)
        self.connect(self.ui.checkBox_2, QtCore.SIGNAL('clicked()'), self.setBitCheckbox)
        self.connect(self.ui.checkBox_3, QtCore.SIGNAL('clicked()'), self.setBitCheckbox)
        self.connect(self.ui.checkBox_4, QtCore.SIGNAL('clicked()'), self.setBitCheckbox)
        self.connect(self.ui.checkBox_5, QtCore.SIGNAL('clicked()'), self.setBitCheckbox)
        self.connect(self.ui.checkBox_6, QtCore.SIGNAL('clicked()'), self.setBitCheckbox)
        self.connect(self.ui.checkBox_7, QtCore.SIGNAL('clicked()'), self.setBitCheckbox)

    def initData(self):
        settingfile = "UI_Debug_parameters.json"
        s_fp = open(settingfile, 'r')
        if s_fp == False:
            QtGui.QMessageBox.information(self, "warning", ('failed to open file %s' % (settingfile)))
            return
        self.s_setjson = json.load(s_fp)
        s_fp.close()
        if self.s_setjson.has_key("SWPages"):
            self.info = self.s_setjson["SWPages"]
            if self.info.has_key("csvFile"):
                self.filename = self.info["csvFile"]
            else:
                QtGui.QMessageBox.information(self, "warning",
                                              ("no 'csvFile' info in 'SWPages' of file: %s" % (settingfile)))
                return
        else:
            QtGui.QMessageBox.information(self, "warning",
                                          ('''No SWPages info in file '%s', please add below info in the file.
                                           \n"SWPages":{\n         "csvFile":"filename.csv"\n}''' %(settingfile)))
            return

        self.loadDataFromFile(self.filename)
        if self.initFlag is False:
            return

        self.curvars = np.zeros(64, np.uint32)
        self.chipstorecurvars = np.zeros(64, np.uint32)
        self.chippageright = np.zeros(64, np.uint32)

        self.treepagesname = {}
        for pagename in self.pages:
            self.treepagesname[pagename] = 0

        pagenames = sorted(self.treepagesname.keys())
        if len(pagenames) is 0: return
        for i in range(len(pagenames)):
            itm = QtGui.QTreeWidgetItem(self.ui.treeWidget_pages)
            itm.setText(0, pagenames[i])
            self.ui.treeWidget_pages.addTopLevelItem(itm)
            if i == 0:
                self.ui.treeWidget_pages.setItemSelected(itm, True)
        self.ui.treeWidget_pages.header().setResizeMode(3)
        self.ui.treeWidget_pages.header().setStretchLastSection(False)

        self.ui.tableWidget_curpage.horizontalHeader().resizeSection(1, 290)

        curkey = pagenames[0]
        self.curpageregs = self.pages[curkey]

        self.RegsInfoShowInTable(self.ui.tableWidget_curpage, self.curpageregs)

        self.curbaseaddr = self.curpageregs[0].baseaddr
        self.treepagesname[curkey] = 1
        self.curselreg = 0

        self.ui.radioButton_31.setChecked(True)
        self.start_pos = 24
        # self.ui.label_addr.setText("%X" % (self.curbaseaddr))

        self.itemChangeFlag = True
        pass

    def checkConnectStatus(self):
        if self.connectFlag is False:
            # QtGui.QMessageBox.information(self, "warning", ("Please connect to chip first!!!\n Setting->Connect"))
            return False
        else:
            return True

    def setConnectFlag(self, flag):
        self.connectFlag = flag
        pass

    def keyReleaseEvent(self, ev):
        if ev.key() == QtCore.Qt.Key_Space:
            self.readCurPageRegs()
            ev.ignore()
            return
        ev.accept()

    def ConvertCsv2VirtualRegListFiles(self):

        # return
        file_name = QtGui.QFileDialog.getOpenFileName(self, "open file dialog", "",
                                                "Csv files(*.csv)")#None, QtGui.QFileDialog.DontUseNativeDialog)
        orgFile = str(file_name)
        filepath = os.path.dirname(orgFile)
        try:
            if orgFile.endswith('.csv') is False:
                QtGui.QMessageBox.information(self, "warning", ("%s is not csv file!!!\nPlease input csv file!!!" %(orgFile)))
                return
            with open(orgFile, "r") as csvFile:
                reader = csv.reader(csvFile)
                Regs = []
                for item in reader:
                    if reader.line_num == 1:
                        # header = {'IP_Name':'', 'Block':'', 'Address':'', 'Bits':'', 'Register Name':'', 'R/W':'', 'Description':''}
                        header = {'Address': '', 'Bits': '', 'Register Name': '', 'Description': ''}
                        if False == set(header.keys()).issubset(item):
                            return
                        for i in range(len(item)):
                            for key in header:
                                if key == item[i]: header[key] = i
                    else:
                        # print item[header['Address']]
                        bNewReg = True
                        itemaddr = int(item[header['Address']].replace('_', ''), 16)
                        itemname = str(item[header['Register Name']])
                        itemname = itemname.strip()
                        for i in range(len(Regs)):
                            # if self.pages[pagename][i]['Address'] == item[header['Address']]:
                            regaddr = Regs[i]['Addr']
                            regname = Regs[i]['Name']
                            if itemaddr == regaddr and itemname != regname:
                                msg =( "Confilct between reg(%s, %x) and reg(%s, %x)" %(regname, regaddr, itemname, itemaddr))
                                QtGui.QMessageBox.information(self, "warning", msg)
                                return
                            elif itemaddr == regaddr:
                                bNewReg = False
                                break
                        if bNewReg:
                            itemdescr = str('    //' + item[header['Bits']] + ':' + item[header['Description']] + '\n')
                            reg = {'Addr':itemaddr, 'Name':itemname, 'Descri':itemdescr}
                            Regs.append(reg)
                        else:
                            Regs[i]['Descri'] += '    //' + item[header['Bits']] + ':' + item[header['Description']] + '\n'
                cfile_str = ''
                hfile_str = ''
                for  i in range(len(Regs)):
                    itemstr = ('    0x%X,  // %d\n' %(Regs[i]['Addr'], i))
                    cfile_str += itemstr
                    itemstr = ('    %s = %d,  // 0x%X\n%s' %(Regs[i]['Name'], i, Regs[i]['Addr'], Regs[i]['Descri']))
                    hfile_str += itemstr
                cfile_start = '''/**
*
*
FILE: VirtualRegList.c
*  Trident FRCV SDK
*
*  Copyright (C) Trident Multimedia Technologies (Shanghai) Co., Ltd
*  All rights reserved.
*
*  DESCRIPTION:
*
HISTORY:
*
*/

/**
*about how to maintain and use virtual reg list, please see Fusion Virtual Register List.doc
* it has been update for SX6. So the file name will remove the Fusion char.
*/

unsigned long const VIRTUALREG_ADD_LIST[] = {\n'''
                cfile_end = '};\n'
                hfile_start = '''/**
*
*
FILE: VirtualRegList.h
*  Trident FRCV SDK
*
*  Copyright (C) Trident Multimedia Technologies (Shanghai) Co., Ltd
*  All rights reserved.
*
*  DESCRIPTION:
*
HISTORY:
*
*/

#ifndef _Virtual_Reg_List_H
#define _Virtual_Reg_List_H
#include "VirtualRegDebugBit.h"
/**
* about how to maintain and use virtual reg list, please see Fusion Virtual Register List.doc
* it has been update for SX6. So the file name will remove the Fusion char.
*/
#ifdef __cplusplus
extern "C" {
#endif

extern unsigned long VIRTUALREG_ADD_LIST[];

enum VIRTUALREG_USE_LIST {\n'''
                hfile_end = '''};
#define WriteVirtualReg(dwIndex, dwVal) tfcWriteHidRegU32((VIRTUALREG_ADD_LIST[dwIndex]), (dwVal))
#define WriteVirtualRegMask(dwIndex, dwMask, dwVal) tfcWriteHidRegMaskU32((VIRTUALREG_ADD_LIST[dwIndex]), dwMask, dwVal)
#define ReadVirtualReg(dwIndex) (tfcReadHidRegU32(VIRTUALREG_ADD_LIST[dwIndex]))

#define WRITE_VREG(dwIndex, dwVal) tfcWriteHidRegU32((VIRTUALREG_ADD_LIST[(dwIndex)]), (dwVal))
#define WRITE_VREG_MASK(dwIndex, dwMask, dwVal) tfcWriteHidRegMaskU32((VIRTUALREG_ADD_LIST[(dwIndex)]), (dwMask), (dwVal))
#define READ_VREG(dwIndex) (tfcReadHidRegU32(VIRTUALREG_ADD_LIST[(dwIndex)]))
#define SET_TO_1(dwIndex, dwMask) tfcWriteHidRegMaskU32((dwIndex), (dwMask), (dwMask))
#define SET_TO_0(dwIndex, dwMask) tfcWriteHidRegMaskU32((dwIndex), (dwMask), (0))
#define SET_TO(dwFlag, dwIndex, dwMask) tfcWriteHidRegMaskU32((dwIndex), (dwMask), (dwFlag) ? (dwMask) : (0))

#ifdef __cplusplus
}
#endif

#endif
'''
                cfile_str = cfile_start + cfile_str + cfile_end
                hfile_str = hfile_start + hfile_str + hfile_end
                cFile = filepath + '/VirtualRegList.c'
                with open(cFile, "w+") as cfh:
                    cfh.write(cfile_str)
                hFile = filepath + '/VirtualRegList.h'
                with open(hFile, "w+") as hfh:
                    hfh.write(hfile_str)
                QtGui.QMessageBox.information(self, "info",
                                              ("Convert .csv to .c/.h\n%s\n%s\n%s\n" %(orgFile, cFile, hFile)))
                # print Regs
                # print hfile_str

        except IOError as e:
            QtGui.QMessageBox.information(self, "warning", ('%s' % (e)))
        except csv.Error as e:
            QtGui.QMessageBox.information(self, "warning", ('file %s: %s' % (orgFile, e)))

    def loadDataFromFile(self, file):
        try:
            if file.endswith('.csv') is False:
                QtGui.QMessageBox.information(self, "warning", ("%s is not csv file!!!\nPlease input csv file!!!" %(file)))
                return
            with open(file, "r") as csvFile:
                reader = csv.reader(csvFile)
                for item in reader:
                    if reader.line_num == 1:
                        header = {'IP_Name':'', 'Block':'', 'Address':'', 'Bits':'', 'Register Name':'', 'R/W':'', 'Description':''}
                        if False == set(header.keys()).issubset(item):
                            return
                        for i in range(len(item)):
                            for key in header:
                                if key == item[i]: header[key] = i
                    else:
                        pagename = item[header['Block']]
                        bNewReg = True
                        if pagename in self.pages:
                            for i in range(len(self.pages[pagename])):
                                # if self.pages[pagename][i]['Address'] == item[header['Address']]:
                                addr = self.pages[pagename][i].baseaddr + self.pages[pagename][i].index * ADDRSTEP
                                itemaddr = int(item[header['Address']].replace('_', ''), 16)
                                if addr == itemaddr:
                                    bNewReg = False
                                    break
                        else:
                            self.pages[pagename] = []
                        if bNewReg:
                            descr = str(item[header['Register Name']] + '\n' + \
                                    item[header['Bits']] + item[header['Description']] + '\n')
                            # reginfoDict = {'RegName': item[header['Register Name']],
                            #                'Address': item[header['Address']], 'R/W': item[header['R/W']],
                            #                'Description': descr}
                            regaddr = int(item[header['Address']].replace('_', ''), 16)
                            pageaddr = int(regaddr & 0xffffff00)
                            regindex = int((regaddr & 0xff)/ADDRSTEP)
                            regname = str(item[header['Register Name']])
                            if 'R/W'== item[header['R/W']]: regright = 3
                            elif 'W'== item[header['R/W']]: regright = 2
                            elif 'R'== item[header['R/W']]: regright = 1
                            else:                           regright = 0
                            self.pages[pagename].append(regs(regindex, regname, descr, regright, pageaddr))
                        else:
                            self.pages[pagename][i].descr += item[header['Bits']] + item[header['Description']]+'\n'
                # print self.pages
                self.initFlag = True
        except IOError as e:
            # sys.exit('%s' % (e))
            QtGui.QMessageBox.information(self, "warning", ('%s' % (e)))
        except csv.Error as e:
            # sys.exit('file %s: %s' % (filename, e))
            QtGui.QMessageBox.information(self, "warning", ('file %s: %s' % (file, e)))

    def newTableWidgetItem(self, val, filedWid, base, type):
        if type is "int":
            item = QtGui.QTableWidgetItem(QtCore.QString("%1").arg(val, filedWid, base, QtCore.QChar("0")).toUpper())
        else:
            item = QtGui.QTableWidgetItem(QtCore.QString("%1").arg(val))
        item.setTextAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
        return item

    def addRowInTable(self, tableWdg, reg):
        rowCnt = tableWdg.rowCount()
        tableWdg.insertRow(rowCnt)
        rowCntItem = self.newTableWidgetItem(rowCnt, 0, 10, "int")
        tableWdg.setVerticalHeaderItem(rowCnt, rowCntItem)
        addrItem = self.newTableWidgetItem(reg.regAddr, 8, 16, "int")
        addrItem.setFlags(QtCore.Qt.ItemIsEnabled)
        tableWdg.setItem(rowCnt, COLADDR, addrItem)
        nameItem = self.newTableWidgetItem(reg.name, 8, 16, "s")
        nameItem.setFlags(QtCore.Qt.ItemIsEnabled)
        tableWdg.setItem(rowCnt, COLNAME, nameItem)
        valItem = self.newTableWidgetItem(reg.value, 8, 16, "int")
        tableWdg.setItem(rowCnt, COLVAL, valItem)

    def RegsInfoShowInTable(self, tableWdg, curRegs):
        tableWdg.setRowCount(0)
        for k in range(len(curRegs)):
            self.addRowInTable(tableWdg, curRegs[k])

    def RegsValueShowInTable(self, tableWdg, curRegs):
        for i in range(tableWdg.rowCount()):
            valItem = self.newTableWidgetItem(curRegs[i].value, 8, 16, "int")
            tableWdg.setItem(i, COLVAL, valItem)

    def writeCurpPageRegs(self):
        if self.checkConnectStatus() is False: return
        if self.initFlag is False: return
        if self.curchipreadflag is False: return
        curRegs = self.curpageregs
        for i in range(len(curRegs)):
            if curRegs[i].right != 0 and curRegs[i].right != 1:
                TFC.tfcWriteDword(curRegs[i].baseaddr, curRegs[i].index * 4, curRegs[i].value)

    def readCurPageRegs(self):
        if self.checkConnectStatus() is False: return
        if self.initFlag is False: return
        curRegs = self.curpageregs
        for i in range(len(curRegs)):
            if curRegs[i].right != 0 and curRegs[i].right != 2:
                curRegs[i].value = TFC.tfcReadDword(curRegs[i].baseaddr, curRegs[i].index * 4)
        self.RegsValueShowInTable(self.ui.tableWidget_curpage, curRegs)
        self.curchipreadflag = True

    def pageSel(self, item, pos):
        if self.initFlag is False: return
        if item != self.ui.treeWidget_pages.currentItem():
            return
        curKey = ""
        for key in self.treepagesname:
            if key == item.text(pos) and self.treepagesname[key] == 1:
                return
            if key == item.text(pos) and self.treepagesname[key] == 0:
                self.curchipreadflag= False
                curKey = key
        self.treepagesname[curKey] = 1
        for key in self.treepagesname:
            if key != curKey:
                self.treepagesname[key] = 0
        self.curpageregs = self.pages[curKey]
        self.curbaseaddr = self.curpageregs[0].baseaddr

        self.RegsInfoShowInTable(self.ui.tableWidget_curpage, self.curpageregs)
        self.readCurPageRegs()

    def refreshOneRegValInTable(self, value):
        self.ui.tableWidget_curpage.currentItem().setText(QtCore.QString("%1").arg(value,
                                        8, 16, QtCore.QChar("0")).toUpper())

    def changeRegDescri(self, row, col):
        curReg = self.curpageregs[row]
        self.curselreg = row
        if col != COLVAL:
            self.updateBitsFromValue(0)
        else:
            flagValueChange = self.getCurRegVarFromchip(curReg)
            if flagValueChange is True:
                self.refreshOneRegValInTable(curReg.value)
            self.updateBitsFromValue(curReg.value)
        self.ui.textEdit_curregdes.setText(curReg.descr)

    def updateBitsFromValue(self, value):
        self.updateCheckboxBits(value >> self.start_pos)

    def updateCheckboxBits(self, byte):
        if byte & 0x80:
            self.ui.checkBox_7.setChecked(True)
        else:
            self.ui.checkBox_7.setChecked(False)
        if byte & 0x40:
            self.ui.checkBox_6.setChecked(True)
        else:
            self.ui.checkBox_6.setChecked(False)
        if byte & 0x20:
            self.ui.checkBox_5.setChecked(True)
        else:
            self.ui.checkBox_5.setChecked(False)
        if byte & 0x10:
            self.ui.checkBox_4.setChecked(True)
        else:
            self.ui.checkBox_4.setChecked(False)
        if byte & 0x8:
            self.ui.checkBox_3.setChecked(True)
        else:
            self.ui.checkBox_3.setChecked(False)
        if byte & 0x4:
            self.ui.checkBox_2.setChecked(True)
        else:
            self.ui.checkBox_2.setChecked(False)
        if byte & 0x2:
            self.ui.checkBox_1.setChecked(True)
        else:
            self.ui.checkBox_1.setChecked(False)
        if byte & 0x1:
            self.ui.checkBox_0.setChecked(True)
        else:
            self.ui.checkBox_0.setChecked(False)
        pass

    def tableItemChanged(self, item):
        if not self.initFlag: return
        if item != self.ui.tableWidget_curpage.currentItem(): return
        if item.column() is not COLVAL: return
        i = item.row()
        stringitem = "%s" % item.text()
        isright = isproperdigit(stringitem)
        if isright is True:
            value = int(stringitem, 16)
            if i in range(len(self.curpageregs)) and self.itemChangeFlag is True:
                self.curpageregs[i].value = value
                self.setCurRegVarTochip(self.curpageregs[i])
                self.getCurRegVarFromchip(self.curpageregs[i])
        self.itemChangeFlag = False
        item.setText(QtCore.QString("%1").arg(self.curpageregs[i].value, 8, 16, QtCore.QChar("0")).toUpper())
        self.itemChangeFlag = True

    def getbitfromcheckbox(self):
        bytevar = 0
        if self.ui.checkBox_0.isChecked():
            bytevar |= 1
        if self.ui.checkBox_1.isChecked():
            bytevar |= 2

        if self.ui.checkBox_2.isChecked():
            bytevar |= 4

        if self.ui.checkBox_3.isChecked():
            bytevar |= 8

        if self.ui.checkBox_4.isChecked():
            bytevar |= 0x10

        if self.ui.checkBox_5.isChecked():
            bytevar |= 0x20

        if self.ui.checkBox_6.isChecked():
            bytevar |= 0x40

        if self.ui.checkBox_7.isChecked():
            bytevar |= 0x80

        return bytevar

    def setBitCheckbox(self):
        temp = 0xFFFFFFFF & (~(0xFF << self.start_pos))
        item = self.ui.tableWidget_curpage.currentItem()
        if item is None: return
        if item.column() != COLVAL: return
        i = item.row()
        if i in range(len(self.curpageregs)):
            self.curpageregs[i].value &= temp
            self.curpageregs[i].value |= (self.getbitfromcheckbox() << self.start_pos)
            self.refreshOneRegValInTable(self.curpageregs[i].value)
            self.setCurRegVarTochip(self.curpageregs[i])

    def changeBitsel(self,flag):
        if not self.initFlag: return

        if self.ui.radioButton_7.isChecked():
            self.start_pos = 0
        elif self.ui.radioButton_15.isChecked():
            self.start_pos = 8
        elif self.ui.radioButton_23.isChecked():
            self.start_pos = 16
        else:
            self.start_pos = 24
        self.ui.label_24.setText(bits_label_list[self.start_pos+7])
        self.ui.label_25.setText(bits_label_list[self.start_pos+6])
        self.ui.label_26.setText(bits_label_list[self.start_pos+5])
        self.ui.label_27.setText(bits_label_list[self.start_pos+4])
        self.ui.label_28.setText(bits_label_list[self.start_pos+3])
        self.ui.label_29.setText(bits_label_list[self.start_pos+2])
        self.ui.label_30.setText(bits_label_list[self.start_pos+1])
        self.ui.label_31.setText(bits_label_list[self.start_pos])

        item = self.ui.tableWidget_curpage.currentItem()
        if item is None: return
        i = item.row()
        if i in range(len(self.curpageregs)):
            self.updateBitsFromValue(self.curpageregs[i].value)
        pass

    def getCurRegVarFromchip(self, reg):
        if self.connectFlag is False: return False
        if self.initFlag is False: return False
        if self.curchipreadflag is False: return False
        reg.value = TFC.tfcReadDword(reg.baseaddr, reg.index*4)
        return True

    def setCurRegVarTochip(self, reg):
        if self.connectFlag is False: return
        if self.initFlag is False: return
        if self.curchipreadflag is False: return
        if reg.right != 1:
            TFC.tfcWriteDword(reg.baseaddr, reg.index*4, reg.value)


if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    mywindow = SWPagesWindow()
    mywindow.show()
    sys.exit(app.exec_())