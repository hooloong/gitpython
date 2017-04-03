
__author__ = 'hooloongge'
# -*- coding: utf-8 -*-
import sys, math, random, time
import ctypes as C
import two01 as TFC
import numpy as np
from dispmipsfunc import *
from PyQt4 import QtCore, QtGui, QtSql,uic  # ,Qwt5
import pyqtgraph as pg
from Drawlg_res import  *


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
symbols = ['o','o','o','o','t','+']

## Define the line style for each connection (this is optional)
lines = np.array([
    (255,0,0,255,1),
    (255,0,255,255,2),
    (255,0,255,255,3),
    (255,255,0,255,2),
    (255,0,0,255,1),
    (255,255,255,255,4),
    ], dtype=[('red',np.ubyte),('green',np.ubyte),('blue',np.ubyte),('alpha',np.ubyte),('width',float)])

## Define text to show next to each symbol
texts = ["Point %d" % i for i in range(6)]

class CustomViewBox(pg.ViewBox):
    def __init__(self, *args, **kwds):
        pg.ViewBox.__init__(self, *args, **kwds)
        # self.setMouseMode(self.RectMode)

    ## reimplement right-click to zoom out
    def mouseClickEvent(self, ev):
        # if ev.button() == QtCore.Qt.RightButton:
        #     self.autoRange()
        pass

    def mouseDragEvent(self, ev):
        # if ev.button() == QtCore.Qt.RightButton:
        #     ev.ignore()
        # else:
        #   pg.ViewBox.mouseDragEvent(self, ev)
        pass

    def mouseMoved(self,evt):
        pos = evt[0]  ## using signal proxy turns original arguments into a tuple
        if p1.sceneBoundingRect().contains(pos):
            mousePoint = vb.mapSceneToView(pos)
            index = int(mousePoint.x())
            if index > 0 and index < len(data1):
                label.setText(
                    "<span style='font-size: 12pt'>x=%0.1f,   <span style='color: red'>y1=%0.1f</span>,   <span style='color: green'>y2=%0.1f</span>" % (
                    mousePoint.x(), data1[index], data2[index]))
            vLine.setPos(mousePoint.x())
            hLine.setPos(mousePoint.y())

class DrawL2GWindow(QtGui.QMainWindow):

    def __init__(self):
        super(DrawL2GWindow, self).__init__()
        self.ui =  Ui_Form_Hist()
        self.ui.setupUi(self)

        self.lgdata = []
        pg.setConfigOptions(antialias=True)
        self.w = pg.GraphicsWindow()
        self.ui.gridLayout_2.addWidget(self.w, 0,0)
        self.v = self.w.addViewBox()
        self.v.setAspectLocked()
        self.gld = Graph()
        self.v.addItem(self.gld)
        self.gld.setData(pos=pos, adj=adj, pen=lines, size=1, symbol=symbols, pxMode=False, text=texts)

        # self.vb = CustomViewBox()
        # self.vb.setAspectLocked()
        # self.pw = pg.PlotWidget(viewBox=self.vb, enableMenu=True,
        #                    title="Plot 2dd L2G Curve<br>left-drag to zoom, right-click to reset zoom")
        # self.ui.gridLayout_2.addWidget(self.pw, 0, 0)
        # # self.r = pg.CustomPolyLineROI([(0, 1),  (10,1), (20,1), (30, 1),(2570,0x800)])
        # self.generateLGdata()
        # self.r = pg.CustomPolyLineROI(self.lgdata)
        # self.vb.addItem(self.r)
        # self.vLine = pg.InfiniteLine(angle=90, movable=False)
        # self.hLine = pg.InfiniteLine(angle=0, movable=False)
        # self.vb.addItem(self.vLine, ignoreBounds=True)
        # self.vb.addItem(self.hLine, ignoreBounds=True)
        #
        # proxy = pg.SignalProxy(self.vb.scene().sigMouseMoved, rateLimit=60, slot=self.mouseMoved)
        #
        # self.timer = pg.QtCore.QTimer()
        # self.timer.timeout.connect(self.update)
        # # self.timer.start(1000)

    def setConnectFlag(self, flag):
        self.connectFlag = flag

    # def update(self):
    #     # print self.r.getState()
    #     self.vLine.setPos(self.r.getState()["points"][0])
    #     self.hLine.setPos(self.r.getState()["points"][0])
    #     pass

    def generateLGdata(self):
        for i in range(32):
            j = (i, i*10)
            self.lgdata.append(j)

        print self.lgdata
        pass



if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    mywindow = DrawL2GWindow()
    mywindow.show()
    sys.exit(app.exec_())
