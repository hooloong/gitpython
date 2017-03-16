#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt4.QtGui import *
from PyQt4.QtCore import *


class CLabel(QWidget):
    """
	signal definition
	"""
    signalLabelPress = pyqtSignal(QWidget)

    def __init__(self, parent=None):
        super(CLabel, self).__init__(parent)
        self.initVariable()
        self.initSetupUi()

    def setPixmap(self, pixmap):
        self.labelIcon.setPixmap(pixmap.scaled(QSize(14, 14), Qt.KeepAspectRatio, Qt.SmoothTransformation))

    def setText(self, text):
        self.labelText.setText(text)

    def setMouseEnterFlag(self, flag):
        self.mouseEnterFlag = flag
        self.update()

    def setMousePressFlag(self, flag):
        self.mousePressFlag = flag
        self.update()

    def enterEvent(self, event):
        if self.getMousePressFlag() == False:
            self.setMouseEnterFlag(True)

        self.setCursor(Qt.PointingHandCursor)

    def leaveEvent(self, event):
        self.setMouseEnterFlag(False)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.setMousePressFlag(True)
            self.signalLabelPress.emit(self)

    def initVariable(self):
        self.setMouseEnterFlag(False)
        self.setMousePressFlag(False)

    def initSetupUi(self):
        self.createFrame()
        self.createWidget()
        self.createLayout()

    def createFrame(self):
        self.setStyleSheet("QWidget {background:transparent;border:0px;color:white;font-weight:bold;font-size:16px;}")

    def createWidget(self):
        self.labelIcon = QLabel(self)
        self.labelText = QLabel(self)

    def createLayout(self):
        self.hlayout = QHBoxLayout()
        self.hlayout.setSpacing(10)
        self.hlayout.setContentsMargins(QMargins(5, 0, 5, 0))
        self.hlayout.addWidget(self.labelIcon)
        self.hlayout.addWidget(self.labelText)
        self.hlayout.addStretch()

        self.setLayout(self.hlayout)

    def getMouseEnterFlag(self):
        return self.mouseEnterFlag

    def getMousePressFlag(self):
        return self.mousePressFlag
