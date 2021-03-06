# -*- coding: utf-8 -*-
"""
This example demonstrates the creation of a plot with a customized
AxisItem and ViewBox. 
"""

import pyqtgraph as pg
from pyqtgraph.Qt import QtCore, QtGui
import numpy as np
import time


class DateAxis(pg.AxisItem):
    def tickStrings(self, values, scale, spacing):
        strns = []
        rng = max(values) - min(values)
        # if rng < 120:
        #    return pg.AxisItem.tickStrings(self, values, scale, spacing)
        if rng < 3600 * 24:
            string = '%H:%M:%S'
            label1 = '%b %d -'
            label2 = ' %b %d, %Y'
        elif rng >= 3600 * 24 and rng < 3600 * 24 * 30:
            string = '%d'
            label1 = '%b - '
            label2 = '%b, %Y'
        elif rng >= 3600 * 24 * 30 and rng < 3600 * 24 * 30 * 24:
            string = '%b'
            label1 = '%Y -'
            label2 = ' %Y'
        elif rng >= 3600 * 24 * 30 * 24:
            string = '%Y'
            label1 = ''
            label2 = ''
        for x in values:
            try:
                strns.append(time.strftime(string, time.localtime(x)))
            except ValueError:  ## Windows can't handle dates before 1970
                strns.append('')
        try:
            label = time.strftime(label1, time.localtime(min(values))) + time.strftime(label2,
                                                                                       time.localtime(max(values)))
        except ValueError:
            label = ''
        # self.setLabel(text=label)
        return strns


class CustomViewBox(pg.ViewBox):
    def __init__(self, *args, **kwds):
        pg.ViewBox.__init__(self, *args, **kwds)
        self.setMouseMode(self.RectMode)

    ## reimplement right-click to zoom out
    def mouseClickEvent(self, ev):
        if ev.button() == QtCore.Qt.RightButton:
            self.autoRange()

    def mouseDragEvent(self, ev):
        if ev.button() == QtCore.Qt.RightButton:
            ev.ignore()
        else:
            pg.ViewBox.mouseDragEvent(self, ev)


app = pg.mkQApp()

axis = DateAxis(orientation='bottom')
axis.setGrid(111)
vb = CustomViewBox()

# pw = pg.PlotWidget(viewBox=vb, axisItems={'bottom': axis}, enableMenu=True,
#                    title="PlotItem with custom axis and ViewBox<br>Menu disabled, mouse behavior changed: left-drag to zoom, right-click to reset zoom")
pw = pg.PlotWidget(viewBox=vb,  enableMenu=True,
                   title="PlotItem with custom axis and ViewBox<br>Menu disabled, mouse behavior changed: left-drag to zoom, right-click to reset zoom")
dates = np.arange(8) * (3600 * 24 * 356)
pw.plot(x=dates, y=[1, 6, 2, 4, 3, 5, 6, 8], symbol='o')
pw.show()
pw.setWindowTitle('pyqtgraph example: customPlot')

r = pg.CustomPolyLineROI([(0, 0), (10, 10),(1,1),(2,2),(3,3)],closed=False)
# r = pg.LineSegmentROI([(0, 0), (10, 10)])
pw.addItem(r)

# update all plots
dp = np.zeros(100)
def update():

    print r.getState()
    pass
timer = pg.QtCore.QTimer()
timer.timeout.connect(update)
timer.start(5000)

## Start Qt event loop unless running in interactive mode or using pyside.
if __name__ == '__main__':
    import sys

    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        QtGui.QApplication.instance().exec_()
