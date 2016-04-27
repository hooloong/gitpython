# -*- coding: utf-8 -*- 
from PyQt4.QtCore import * 
from PyQt4.QtGui import * 
import sys 
import os 
import time

class Test(QDialog): 
    def __init__(self,parent=None): 
        super(Test,self).__init__(parent) 
        self.thread=Worker() 
        self.listFile=QListWidget() 
        self.btnStart=QPushButton('Start') 
        layout=QGridLayout(self) 
        layout.addWidget(self.listFile,0,0,1,2) 
        layout.addWidget(self.btnStart,1,1) 
        self.connect(self.btnStart,SIGNAL('clicked()'),self.slotStart) 
        self.connect(self.thread,SIGNAL('output(QString)'),self.slotAdd) 
    def slotAdd(self,file_inf): 
        self.listFile.addItem(file_inf) 
    def slotStart(self): 
        self.btnStart.setEnabled(False) 
        self.thread.start() 
class Worker(QThread): 
    def __init__(self,parent=None): 
        super(Worker,self).__init__(parent) 
        self.working=True 
        self.num=0 
    def __del__(self): 
        self.working=False 
        self.wait() 
    def run(self): 
        while self.working==True: 
            file_str='File index {0}'.format(self.num) 
            self.num+=1 
            self.emit(SIGNAL('output(QString)'),file_str) 
            self.sleep(3) 
app=QApplication(sys.argv) 
dlg=Test() 
dlg.show() 
sys.exit(app.exec_())