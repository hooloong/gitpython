# -*- coding: utf-8 -*-
import sys
import csv
import numpy as np
import os
from PyQt4 import QtCore, QtGui, uic  # ,Qwt5
import two01 as TFC
from dispmipsfunc import *
from SWPages_res import *

filename = "SX8_V_SW_REG_SPG.csv"
ADDRSTEP = int(4)
CURPAGESIZE = int(64)
bits_label_list = ["7","6","5","4","3","2","1","0","15","14","13","12","11","10","9","8",
                   "23","22","21","20","19","18","17","16","31","30","29","28","27","26","25","24"]

class regs():
    def __init__(self,index,name,descr,right,baseaddr):
        self.index = index
        self.name = name
        self.descr = descr
        self.right = right
        self.baseaddr = baseaddr

class SWPagesWindow(QtGui.QMainWindow):
    def __init__(self):
        super(SWPagesWindow, self).__init__()
        self.ui = Ui_Form_Pages()
        self.ui.setupUi(self)
        self.pages = {}
        self.initFlag = False
        self.connectFlag = False
        self.curchipreadflag = False

        self.connect(self.ui.pushButton_Convert, QtCore.SIGNAL('clicked()'), self.ConvertCsv2VirtualRegListFiles)

        self.loadDataFromFile(filename)
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
        self.ui.treeWidget_pages.header().setResizeMode(3)
        self.ui.treeWidget_pages.header().setStretchLastSection(False)

        curkey = pagenames[0]
        self.curpageregs = self.pages[curkey]
        self.curbaseaddr = self.curpageregs[0].baseaddr
        self.treepagesname[curkey] = 1
        self.getrightforcurpage()
        self.DataShowiInTable()
        self.curselreg = 0
        self.ui.radioButton_31.setChecked(True)
        self.start_pos = 24
        self.ui.label_addr.setText("%X" % (self.curbaseaddr))

        self.ui.treeWidget_pages.itemPressed.connect(self.pagesel)

        self.connect(self.ui.tableWidget_curpage, QtCore.SIGNAL('cellPressed(int,int)'), self.changeRegDescri)
        self.ui.tableWidget_curpage.itemChanged.connect(self.updatepatts)

        # self.connect(self.ui.pushButton_getitem, QtCore.SIGNAL('clicked()'), self.printoutregs)
        self.connect(self.ui.pushButton_readpage, QtCore.SIGNAL('clicked()'), self.readcurpage)
        self.connect(self.ui.pushButton_writepage, QtCore.SIGNAL('clicked()'), self.writecurpage)
        self.connect(self.ui.pushButton_refresh, QtCore.SIGNAL('clicked()'), self.readcurpage)

        self.connect(self.ui.radioButton_7, QtCore.SIGNAL('clicked(bool)'), self.changeBitsel)
        self.connect(self.ui.radioButton_15, QtCore.SIGNAL('clicked(bool)'), self.changeBitsel)
        self.connect(self.ui.radioButton_23, QtCore.SIGNAL('clicked(bool)'), self.changeBitsel)
        self.connect(self.ui.radioButton_31, QtCore.SIGNAL('clicked(bool)'), self.changeBitsel)
        self.connect(self.ui.checkBox_0, QtCore.SIGNAL('clicked()'), self.setbitcheck)
        self.connect(self.ui.checkBox_1, QtCore.SIGNAL('clicked()'), self.setbitcheck)
        self.connect(self.ui.checkBox_2, QtCore.SIGNAL('clicked()'), self.setbitcheck)
        self.connect(self.ui.checkBox_3, QtCore.SIGNAL('clicked()'), self.setbitcheck)
        self.connect(self.ui.checkBox_4, QtCore.SIGNAL('clicked()'), self.setbitcheck)
        self.connect(self.ui.checkBox_5, QtCore.SIGNAL('clicked()'), self.setbitcheck)
        self.connect(self.ui.checkBox_6, QtCore.SIGNAL('clicked()'), self.setbitcheck)
        self.connect(self.ui.checkBox_7, QtCore.SIGNAL('clicked()'), self.setbitcheck)



    def setConnectFlag(self, flag):
        self.connectFlag = flag
        pass

    def keyReleaseEvent(self, ev):
        if ev.key() == QtCore.Qt.Key_Space:
            self.readcurpage()
            ev.ignore()
            return
        ev.accept()

    def ConvertCsv2VirtualRegListFiles(self):
        file_name = QtGui.QFileDialog.getOpenFileName(self, "open file dialog", "",
                                                "Csv files(*.csv)")#None, QtGui.QFileDialog.DontUseNativeDialog)
        orgFile = str(file_name)
        filepath = os.path.dirname(orgFile)
        try:
            if orgFile.endswith('.csv') is False:
                QtGui.QMessageBox.information(self, "warning", ("%s is not csv file!!!\nPlease input csv file!!!" %(file)))
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
                            itemdescr = str('    //' + item[header['Bits']] + item[header['Description']] + '\n')
                            reg = {'Addr':itemaddr, 'Name':itemname, 'Descri':itemdescr}
                            Regs.append(reg)
                        else:
                            Regs[i]['Descri'] += '    //' + item[header['Bits']] + item[header['Description']] + '\n'
                cfile_str = ''
                hfile_str = ''
                for  i in range(len(Regs)):
                    itemstr = ('    0x%x,  // %d\n' %(Regs[i]['Addr'], i))
                    cfile_str += itemstr
                    itemstr = ('    %s = %d,  // 0x%x\n%s' %(Regs[i]['Name'], i, Regs[i]['Addr'], Regs[i]['Descri']))
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
            QtGui.QMessageBox.information(self, "warning", ('file %s: %s' % (filename, e)))

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
            QtGui.QMessageBox.information(self, "warning", ('file %s: %s' % (filename, e)))

    def getrightforcurpage(self):
        self.chippageright = np.zeros(CURPAGESIZE, np.uint32)
        for inx in range(CURPAGESIZE):
            for k in range(len(self.curpageregs)):
                if self.curpageregs[k].index == inx:
                    getright = self.curpageregs[k].right
                    self.chippageright[inx] = getright

    def DataShowiInTable(self):
        self.chippageright = np.zeros(CURPAGESIZE, np.uint32)
        for i in range(self.ui.tableWidget_curpage.rowCount()):
            for j in range(self.ui.tableWidget_curpage.columnCount()):
                getFlag = False
                getright = 0
                # pwmdutytemp = "%X" % (self.curpat[i * self.ui.tableWidget_pattern.columnCount() + j])
                newItemt = QtGui.QTableWidgetItem(QtCore.QString("%1").arg(self.curvars[i * \
                self.ui.tableWidget_curpage.columnCount() + j],8,16,QtCore.QChar("0")).toUpper())
                newItemt.setTextAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
                ind = (i*4 + j)
                for k in range(len(self.curpageregs)):
                    # print reg.index,i,j
                    if self.curpageregs[k].index == ind:
                        getright =  self.curpageregs[k].right
                        getFlag = True
                        if getright == 1:
                            newItemt.setBackground(QtGui.QColor(255, 0, 255))
                if getFlag is False:
                    newItemt.setBackground(QtGui.QColor(125, 125, 125))
                    newItemt.setFlags(QtCore.Qt.NoItemFlags)
                self.ui.tableWidget_curpage.setItem(i, j, newItemt)

    def updatepatts(self,item):
        if not self.initFlag: return
        if item != self.ui.tableWidget_curpage.currentItem():
            return
        # print item.text()
        stringitem = "%s" % item.text()
        isright = isproperdigit(stringitem)
        i = item.row()
        j = item.column()
        if isright is True:
            self.curvars[item.row()* 4 + item.column()] = int(stringitem,16)
            self.ui.tableWidget_curpage.currentItem().setText(QtCore.QString("%1").arg(self.curvars[i * \
                                 self.ui.tableWidget_curpage.columnCount() + j],
                                        8, 16, QtCore.QChar("0")).toUpper())
            if self.connectFlag is True:
                for k in range(len(self.curpageregs)):
                    if self.curpageregs[k].index == self.curselreg:
                        self.setCurRegVarTochip(self.curpageregs[k], self.curselreg)
                        break

        if islowerdigit(stringitem) is True or isright is False:
            self.ui.tableWidget_curpage.currentItem().setText(QtCore.QString("%1").arg(self.curvars[i * \
                                 self.ui.tableWidget_curpage.columnCount() + j],
                                        8, 16, QtCore.QChar("0")).toUpper())

    def updatethebitsfromvars(self):
        # print self.curselreg,self.curvars[self.curselreg],self.start_pos
        self.updatethecheckboxbits(self.curvars[self.curselreg] >> self.start_pos)
        pass

    def updatethecheckboxbits(self,byte):
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

    def changeTableOneReg(self,row,col):
        self.ui.tableWidget_curpage.currentItem().setText(QtCore.QString("%1").arg(self.curvars[row * \
                                 self.ui.tableWidget_curpage.columnCount() + col],
                                        8, 16, QtCore.QChar("0")).toUpper())
        pass

    def changeRegDescri(self,row,col):
        itemregchangflag = False
        for k in range(len(self.curpageregs)):
            if self.curpageregs[k].index == (row * 4 + col):
                itemregchangflag = self.getCurRegVarFromchip(self.curpageregs[k],row * 4 + col)
                self.ui.textEdit_curregdes.setText(self.curpageregs[k].descr)
                self.ui.label_addr.setText(
                    "%X" % (self.curpageregs[k].baseaddr + self.curpageregs[k].index * 4))
                self.ui.label_regsname.setText(self.curpageregs[k].name)
                # print self.curpageregs[k].right
                self.curselreg = row * 4 + col
                self.updatethebitsfromvars()
                if itemregchangflag is True:
                    self.changeTableOneReg(row,col)
                break

    def pagesel(self,item,pos):
        if self.initFlag is False: return
        if item != self.ui.treeWidget_pages.currentItem():
            return
        currentkey = ""
        for key in self.treepagesname:
            if key == item.text(pos) and self.treepagesname[key] == 1:
                return
            if key == item.text(pos) and self.treepagesname[key] == 0:
                self.curchipreadflag= False
                currentkey = key
        self.treepagesname[currentkey] = 1
        for key in self.treepagesname:
            if key != currentkey:
                self.treepagesname[key] = 0
        self.curpageregs = self.pages[currentkey]
        self.curbaseaddr = self.curpageregs[0].baseaddr
        self.getrightforcurpage()
        self.readcurpage()
        self.DataShowiInTable()

    def setbitcheck(self):

        temp = 0xFFFFFFFF & (~(0xFF << self.start_pos))
        self.curvars[self.curselreg] &= temp
        self.curvars[self.curselreg] |= (self.getbitfromcheckbox() << self.start_pos)

        for k in range(len(self.curpageregs)):
            if self.curpageregs[k].index == self.curselreg:
                self.changeTableOneReg(self.curselreg/4 , self.curselreg%4)
                self.setCurRegVarTochip(self.curpageregs[k],self.curselreg)
        pass

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

        self.updatethebitsfromvars()
        pass

    def readcurpage(self):
        if self.connectFlag is False: return
        if self.initFlag is False: return
        # self.chipstorecurvars = np.zeros(64, np.uint32)
        self.curbaseaddr = self.curpageregs[0].baseaddr
        self.getrightforcurpage()
        for i in range(64):
            if self.chippageright[i] != 0 and self.chippageright[i] != 2:
                self.chipstorecurvars[i] = TFC.tfcReadDword(self.curbaseaddr, i*4)
            else:
                self.chipstorecurvars[i] = 0
            self.curvars[i] = self.chipstorecurvars[i]

        self.DataShowiInTable()
        # print self.chipstorecurvars
        self.curchipreadflag = True
        pass

    def writecurpage(self):
        if self.connectFlag is False: return
        if self.initFlag is False: return
        if self.curchipreadflag is False: return
        self.curbaseaddr = self.curpageregs[0].baseaddr
        self.getrightforcurpage()
        self.chipstorecurvars = np.zeros(64, np.uint32)
        for i in range(64):
            self.chipstorecurvars[i] = self.curvars[i]
            if self.chippageright[i] != 0 and self.chippageright[i] != 1:
                TFC.tfcWriteDword(self.curbaseaddr,i*4,self.chipstorecurvars[i])

        print self.curbaseaddr
        pass

    def getCurRegVarFromchip(self,reg,num):
        if self.connectFlag is False: return
        if self.initFlag is False: return
        if self.curchipreadflag is False: return
        ret = False
        self.chipstorecurvars[num] = TFC.tfcReadDword(reg.baseaddr, num*4)
        if self.curvars[num] != self.chipstorecurvars[num]:
            ret = True
        else:
            ret = False
        self.curvars[num] = self.chipstorecurvars[num]
        return True

    def setCurRegVarTochip(self,reg,num):
        if self.connectFlag is False: return
        if self.initFlag is False: return
        if self.curchipreadflag is False: return
        ret = False
        if self.curvars[num] != self.chipstorecurvars[num]:
            ret = True
        else:
            ret = False
        self.chipstorecurvars[num] = self.curvars[num]
        if ret is True and self.connectFlag is True and self.curchipreadflag is True:
            if reg.right !=1 :
                TFC.tfcWriteDword(reg.baseaddr, num*4,self.chipstorecurvars[num])
                print hex(reg.baseaddr), hex(num*4), hex(self.chipstorecurvars[num])
        pass

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    mywindow = SWPagesWindow()
    mywindow.show()
    sys.exit(app.exec_())