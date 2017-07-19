
__author__ = 'hooloongge'
# -*- coding: utf-8 -*-
import sys, math, random, time
import ctypes as C
import two01 as TFC
import numpy as np
from dispmipsfunc import *
from PyQt4 import QtCore, QtGui, QtSql,uic  # ,Qwt5
import pyqtgraph as pg
from DrawMap_res import  *


class Graph(pg.GraphItem):
    def __init__(self):
        self.dragPoint = None
        self.dragOffset = None
        self.textItems = []
        pg.GraphItem.__init__(self)
        self.scatter.sigClicked.connect(self.clicked)

    def setData(self, **kwds):
        self.text = kwds.pop('text', [])
        self.data = kwds
        if 'pos' in self.data:
            npts = self.data['pos'].shape[0]
            self.data['data'] = np.empty(npts, dtype=[('index', int)])
            self.data['data']['index'] = np.arange(npts)
        self.setTexts(self.text)
        self.updateGraph()

    def setTexts(self, text):
        for i in self.textItems:
            i.scene().removeItem(i)
        self.textItems = []
        for t in text:
            item = pg.TextItem(t)
            self.textItems.append(item)
            item.setParentItem(self)

    def updateGraph(self):
        pg.GraphItem.setData(self, **self.data)
        for i,item in enumerate(self.textItems):
            item.setPos(*self.data['pos'][i])


    def mouseDragEvent(self, ev):
        if ev.button() != QtCore.Qt.LeftButton:
            ev.ignore()
            return

        if ev.isStart():
            # We are already one step into the drag.
            # Find the point(s) at the mouse cursor when the button was first
            # pressed:
            pos = ev.buttonDownPos()
            pts = self.scatter.pointsAt(pos)
            if len(pts) == 0:
                ev.ignore()
                return
            self.dragPoint = pts[0]
            ind = pts[0].data()[0]
            self.dragOffset = self.data['pos'][ind] - pos
        elif ev.isFinish():
            self.dragPoint = None
            return
        else:
            if self.dragPoint is None:
                ev.ignore()
                return

        ind = self.dragPoint.data()[0]
        self.data['pos'][ind] = ev.pos() + self.dragOffset
        self.updateGraph()
        ev.accept()

    def clicked(self, pts):
        print("clicked: %s" % pts)



## Define positions of nodes
pos = np.array([
    [0,0],
    [10,0],
    [0,10],
    [10,10],
    [5,5],
    [15,5]
    ], dtype=float)

## Define the set of connections in the graph
adj = np.array([
    [0,1],
    [1,3],
    [3,2],
    [2,0],
    [1,5],
    [3,5],
    ])

## Define the symbol to use for each node (this is optional)
symbols = ['o','o','o','o','o','o']

## Define the line style for each connection (this is optional)
lines = np.array([
    (255,0,0,255,1),
    (255,0,255,255,1),
    (255,0,255,255,1),
    (255,255,0,255,1),
    (255,0,0,255,1),
    (255,255,255,255,1),
    ], dtype=[('red',np.ubyte),('green',np.ubyte),('blue',np.ubyte),('alpha',np.ubyte),('width',float)])

## Define text to show next to each symbol
texts = ["%d" % i for i in range(192)]
for i in range(5):
    pos = np.row_stack((pos,pos))
    adj =  np.row_stack((adj,adj))
    symbols = symbols *2
# lines = lines.repeat(32)
lines =  np.tile(lines,32)
for i in range(192):
    pos[i][0] = i
    pos[i][1] = (192-i) * 0xC00/0x400
    adj[i][0] = i
    adj[i][1] = i+1
adj[191][1] = 191
print len(pos),len(adj),len(lines),len(symbols)

class CustomViewBox(pg.ViewBox):
    def __init__(self, *args, **kwds):
        pg.ViewBox.__init__(self, *args, **kwds)
        # self.setMouseMode(self.RectMode)

        self.setLimits(xMin=0,yMin=0x400)
    ## reimplement right-click to zoom out
    def mouseClickEvent(self, ev):
        if ev.button() == QtCore.Qt.RightButton:
            self.autoRange()
        pass

    def mouseDragEvent(self, ev):
        if ev.button() == QtCore.Qt.RightButton:
            ev.ignore()
        else:
          pg.ViewBox.mouseDragEvent(self, ev)
        pass



class CustomPolyLineROI2(pg.PolyLineROI):

    def __init__(self, positions, closed=False, pos=None, **args):
        pg.PolyLineROI.__init__(self, positions, closed=False, pos=None,movable=False, **args)

    def segmentClicked(self, segment, ev=None, pos=None): ## pos should be in this item's coordinate system
        if ev != None:
            pos = segment.mapToParent(ev.pos())
        elif pos != None:
            pos = pos
        else:
            raise Exception("Either an event or a position must be given.")

    # def paint(self, p, *args):
    #     p.setRenderHint(QtGui.QPainter.Antialiasing)
    #     p.setPen(self.currentPen)
    #     h1 = self.handles[0]['item'].pos()
    #     h2 = self.handles[1]['item'].pos()
    #     p.drawCubicBezier(h1, h2)
    # def shape(self):
    #     p = QtGui.QPainterPath()
    #     if len(self.handles) == 0:
    #         return p
    #     p.moveTo(self.handles[0]['item'].pos())
    #     for i in range(len(self.handles)):
    #         p.lineTo(self.handles[i]['item'].pos())
    #     p.lineTo(self.handles[0]['item'].pos())
    #     print p
    #     return p

class DrawMLutWindow(QtGui.QMainWindow):

    def __init__(self):
        super(DrawMLutWindow, self).__init__()
        self.ui =  Ui_Form_mLut()
        self.ui.setupUi(self)

        self.lgdata = []
        pg.setConfigOptions(antialias=True)
        # #self.w = pg.GraphicsWindow()
        # self.w = pg.GraphicsLayoutWidget()
        # self.ui.gridLayout_2.addWidget(self.w, 0,0)
        # self.v = self.w.addViewBox()
        # self.v.setAspectLocked()
        # self.gld = Graph()
        # self.v.addItem(self.gld)
        # self.gld.setData(pos=pos, adj=adj, pen=lines, size=1, symbol=symbols, pxMode=False, text=texts)
        # self.vLine = pg.InfiniteLine(angle=90, movable=False)
        # self.hLine = pg.InfiniteLine(angle=0, movable=False)
        # self.v.addItem(self.vLine, ignoreBounds=True)
        # self.v.addItem(self.hLine, ignoreBounds=True)
        # self.linepen = pg.mkPen({'color': "111"})
        # for i in range(1,192):
        #     vlines = pg.InfiniteLine(angle=90, movable=False,pen=self.linepen)
        #     self.v.addItem(vlines)
        #     vlines.setPos([i,0])

        self.vb = CustomViewBox()
        self.vb.setAspectLocked(False)
        self.pw = pg.PlotWidget(viewBox=self.vb, enableMenu=True,
                           title="Plot 2dd L2G Curve<br>left-drag to zoom, right-click to reset zoom")
        self.pw.showGrid(True,True,0.5)
        self.ui.gridLayout_2.addWidget(self.pw, 0, 0)
        # self.r = pg.CustomPolyLineROI([(0, 1),  (10,1), (20,1), (30, 1),(2570,0x800)])
        self.generateLGdata()
        self.r = CustomPolyLineROI2(self.lgdata)
        self.vb.addItem(self.r)
        # self.vLine = pg.InfiniteLine(angle=90, movable=False)
        # self.hLine = pg.InfiniteLine(angle=0, movable=False)
        # self.vb.addItem(self.vLine, ignoreBounds=True)
        # self.vb.addItem(self.hLine, ignoreBounds=True)

        # proxy = pg.SignalProxy(self.vb.scene().sigMouseMoved, rateLimit=60, slot=self.mouseMoved)

        self.timer = pg.QtCore.QTimer()
        self.timer.timeout.connect(self.update)
        # self.timer.start(2000)
        self.normalm= np.zeros(65, np.uint32)
        self.setzerom = np.zeros(65,np.uint32)
        self.setfullm = np.zeros(65,np.uint32)
        self.setbinarym = np.zeros(65, np.uint32)
        self.normalm_lut= np.zeros(1024, np.uint32)
        self.setzerom_lut = np.zeros(1024,np.uint32)
        self.setfullm_lut = np.zeros(1024,np.uint32)
        self.setbinarym_lut = np.zeros(1024, np.uint32)
        self.curmm= np.zeros(65, np.uint32)
        self.curmm_lut = np.zeros(1024, np.uint32)
        self.generateTestingdata()
        self.initMlutTable()
        self.connect(self.ui.pushButton_write, QtCore.SIGNAL('clicked()'), self.writeMlut)
        self.connect(self.ui.pushButton_write, QtCore.SIGNAL('pressed()'), self.changeText_Mlut)
        self.connect(self.ui.pushButton_read, QtCore.SIGNAL('clicked()'), self.readMlut)
        self.connect(self.ui.pushButton_read, QtCore.SIGNAL('pressed()'), self.changeText_Mlut_read)
        self.connect(self.ui.comboBox_test, QtCore.SIGNAL('currentIndexChanged(int)'), self.comboxchange)
        self.connect(self.ui.checkBox_en, QtCore.SIGNAL('clicked()'), self.enableMlut)
        self.ui.tableWidget_mlut.itemChanged.connect(self.updatetable)

    def setConnectFlag(self, flag):
        self.connectFlag = flag

    def update(self):
        print self.r.getState()
        # self.vLine.setPos(self.r.getState()["points"][0])
        # self.hLine.setPos(self.r.getState()["points"][0])
        pass

    def enableMlut(self):
        if self.connectFlag is False: return
        if self.ui.checkBox_en.isChecked():
            TFC.tfcWriteDwordMask(TFC.BASIC_PAGE, 0x30, 0x00000008, 0x00000008)
        else:
            TFC.tfcWriteDwordMask(TFC.BASIC_PAGE, 0x30, 0x00000008, 0)
        pass
    def generateLGdata(self):
        for i in range(11,-1,-1):
            j = (i*20, 0x400+(0xC00-0x400)*(11-i)/11)
            self.lgdata.append(j)

        print self.lgdata
        pass

    def initMlutTable(self):
        for i in range(self.ui.tableWidget_mlut.rowCount()):
            for j in range(self.ui.tableWidget_mlut.columnCount()):
                # pwmdutytemp = "%X" % (self.curpat[i * self.ui.tableWidget_pattern.columnCount() + j])
                newItemt = QtGui.QTableWidgetItem(QtCore.QString("%1").arg(self.curmm[i * \
                self.ui.tableWidget_mlut.columnCount() + j],4,10,QtCore.QChar(" ")).toUpper())
                newItemt.setTextAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
                self.ui.tableWidget_mlut.setItem(i, j, newItemt)
        pass
    def updatetable(self,item):
        # if not self.initFlag: return

        if item != self.ui.tableWidget_mlut.currentItem():
            return
        print item.text()
        stringitem = "%s" % item.text()
        isright = ispropernumber(stringitem)
        i = item.row()
        j = item.column()
        if isright is True:
            self.curmm[item.row()* 8 + item.column()] = int(stringitem,10)

        if isright is False:
            self.ui.tableWidget_mlut.currentItem().setText(QtCore.QString("%1").arg(self.curmm[i * \
                                 self.ui.tableWidget_mlut.columnCount() + j],
                                        4, 10, QtCore.QChar(" ")).toUpper())
        pass
    def tableToLut(self,inputs,output):
        # //check the input values
        print inputs,output
        if inputs[63] != 1023:
            print "input[63 ] != 1023, error"
            # QtGui.QMessageBox.information(self, "warning", ("input[63 ] != 1023, error"))
            return
        for i in range(63):
            if inputs[i] > inputs[i+1]:
                print "inputs[ %d] > next data, error" % i
                # QtGui.QMessageBox.information(self, "warning", ("data not right!!"))
                return
            if inputs[i] > 1023:
                print "inputs[ %d] > 1023, error" % i
                # QtGui.QMessageBox.information(self, "warning", ("data not right!!"))
                return
        output[0] = 0
        output[1023] = 63
        for i in range(1,64):
            for y in range(inputs[i-1],inputs[i]):
                output[y] = i
        print output
        pass

    def generateTestingdata(self):
        """
        generate normal table
        """
        for i in range(64):
            self.normalm[i] = 1024/64 * (i+1)
        self.normalm[63] = 1023

        self.tableToLut(self.normalm,self.normalm_lut)
        print self.normalm_lut

        # generate  zero table for hist
        for i in range(64):
            self.setzerom[i] = 0
        for i in range(1024):
            self.setzerom_lut[i] = 0
        # generate full mapping lut
        for i in range(64):
            self.setfullm[i] = 1023
        for i in range(1024):
            self.setfullm_lut[i] = 63
        print self.setfullm_lut
        # generate binary mpping lut, the knee set to 0x512
        for i in range(64):
                if i <32:
                    self.setbinarym[i] = 0
                else:
                    self.setbinarym[i] = 1023
        for i in range(1024):
                if i < 512:
                    self.setbinarym_lut[i] = 0
                else:
                    self.setbinarym_lut[i] = 63
        print self.setbinarym_lut
        self.curmm_lut = self.normalm_lut.copy()
        self.curmm = self.normalm.copy()
        # self.curmm_lut = self.setfullm_lut.copy()
        # self.curmm = self.setfullm.copy()
        # self.curmm_lut = self.setbinarym_lut.copy()
        # self.curmm = self.setbinarym.copy()
        # self.curmm_lut = self.setzerom_lut.copy()
        # self.curmm = self.setzerom.copy()
        pass
    def comboxchange(self):
        # if  self.initFlag is False: return
        index = self.ui.comboBox_test.currentIndex()
        if index ==0:
            self.curmm_lut = self.normalm_lut.copy()
            self.curmm = self.normalm.copy()
        elif index == 1:
            self.curmm_lut = self.setzerom_lut.copy()
            self.curmm = self.setzerom.copy()
        elif index == 2:
            self.curmm_lut = self.setfullm_lut.copy()
            self.curmm = self.setfullm.copy()
        else:
            self.curmm_lut = self.setbinarym_lut.copy()
            self.curmm = self.setbinarym.copy()

        self.initMlutTable()
        self.update()
        pass
    def changeText_Mlut(self):
        if self.connectFlag is False:
            pass
        else:
            self.ui.pushButton_write.setText("Write...")
    def changeText_Mlut_read(self):
        if self.connectFlag is False:
            pass
        else:
            self.ui.pushButton_read.setText("Read...")
    def writeMlut(self):
        # added read from registers
        if self.connectFlag is False:
            QtGui.QMessageBox.information(self, "warning", ("Please connect to chip first!!!\n Setting->Connect"))
            return
        TFC.tfcWriteDwordMask(0x19A004B0, 0, 0x00008000, 0x00008000)
        for i in range(1024):
            if i%4 == 0:
                temp = self.curmm_lut[i] | (self.curmm_lut[i+1] <<8)  \
                                                          | self.curmm_lut[i+2] <<16 | self.curmm_lut[i+3] << 24
                TFC.tfcWriteDword(0x19A46000+i,0,temp)
                print temp
        TFC.tfcWriteDwordMask(0x19A004B0, 0, 0x00008000, 0x00000000)
        self.ui.pushButton_write.setText("WriteToChip")

    def readMlut(self):
        if self.connectFlag is False:
            QtGui.QMessageBox.information(self, "warning", ("Please connect to chip first!!!\n Setting->Connect"))
            return
        TFC.tfcWriteDwordMask(0x19A004B0, 0, 0x00008000, 0x00008000)
        for i in range(1024):
            if i%4 == 0:
                temp = TFC.tfcReadDword(0x19A46000 + i, 0)
                self.curmm_lut[i] = temp & 0x000000FF
                self.curmm_lut[i+1] = (temp >> 8) & 0x000000FF
                self.curmm_lut[i+2] = (temp >> 16) & 0x000000FF
                self.curmm_lut[i+3] = (temp >> 24) & 0x000000FF
                print temp
        TFC.tfcWriteDwordMask(0x19A004B0, 0, 0x00008000, 0x00000000)
        self.ui.pushButton_read.setText("ReadFromChip")

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    mywindow = DrawMLutWindow()
    mywindow.show()
    sys.exit(app.exec_())
