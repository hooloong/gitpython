
# -*- coding: utf-8 -*-
import numpy as np
from PyQt4.QtGui import *
from PyQt4.QtCore import Qt
from guiqwt.plot import PlotManager, CurvePlot
from guiqwt.builder import make

class PlotDemo(QWidget):
    def __init__(self):
        super(PlotDemo, self).__init__()
        self.setWindowTitle(u"Plot Demo")
        self.manager = PlotManager(self)
        self.plot = CurvePlot()
        self.manager.add_plot(self.plot)
        self.manager.register_standard_tools()
        self.manager.get_default_tool().activate()
        t = np.arange(0, 20, 0.05)
        x = np.sin(t) + np.random.randn(len(t))
        curve = make.curve(t, x, color="red", title=u"")
        self.plot.add_item(curve)
        vbox = QVBoxLayout()
        vbox.addWidget(self.plot)
        self.setLayout(vbox)