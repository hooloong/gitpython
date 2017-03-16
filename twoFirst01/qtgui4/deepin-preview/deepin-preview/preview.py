#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt4.QtGui import *
from PyQt4.QtCore import *
from clabel import CLabel
import sys

WINDOW_WIDTH = 563
WINDOW_HEIGHT = 352
WINDOW_START_X = 0
WINDOW_START_Y = 0
WINDOW_PAGE_COUNT = 3
WINDOW_BUTTON_COUNT = 3
WINDOW_PAGE_MOVE = 20
WINDOW_ONEBUTTON_WIDTH = 170


class EButtonMouseState(object):
    EButtonMouseDefault, EButtonMouseEnter, EButtonMousePress, EButtonMouseNone = range(0, 4)


class PreviewWidget(QWidget):
    def __init__(self, lang, parent=None):
        super(PreviewWidget, self).__init__(parent)
        self.mouse_press = False
        self.mouse_move = False
        self.label_move = False
        self.current_index = 0
        self.current_pos_x = 0
        self.name_list = []
        self.label_array = []

        self.resize(QSize(WINDOW_WIDTH, WINDOW_HEIGHT))
        self.setWindowFlags(Qt.FramelessWindowHint)

        pixmap = QPixmap(QSize(self.width() * WINDOW_PAGE_COUNT, WINDOW_HEIGHT))
        painter = QPainter()
        painter.begin(pixmap)
        for i in range(0, WINDOW_PAGE_COUNT):
            painter.drawImage(QRect(WINDOW_WIDTH * i, 0, WINDOW_WIDTH, WINDOW_HEIGHT),
                              QImage(QString("./wizard/%1/%2.png").arg(lang).arg(i)))
        painter.end()
        self.total_label = QLabel(self)
        self.total_label.resize(pixmap.size())
        self.total_label.setPixmap(pixmap)
        self.total_label.move(WINDOW_START_X, WINDOW_START_Y)

        self.close_button = QToolButton(self)
        self.translateLanguage()

        for i in range(0, WINDOW_BUTTON_COUNT):
            label = CLabel(self)
            label.setStyleSheet("background:transparent;border:0px;")
            label.setPixmap(QPixmap(QString("./wizard/dot_normal.png")))
            label.move(250 + i * 20, 319)
            label.signalLabelPress.connect(self.changeCurrentPage)
            self.label_array.append(label)

        self.label_array[0].setMousePressFlag(True)
        self.label_array[0].setPixmap(QPixmap("./wizard/dot_active.png"))

        self.close_button.setStyleSheet("background:transparent;border:0px;")
        self.close_button.setFocusPolicy(Qt.NoFocus)
        pixmap = QPixmap("./wizard/btn_close.png")
        self.close_button.setIcon(QIcon(pixmap.copy(QRect(0, 0, pixmap.width() / 4, pixmap.height()))))
        self.close_button.setIconSize(QSize(pixmap.width() / 4, pixmap.height()))
        self.close_button.move(self.width() - 52, 1)
        self.close_button.clicked.connect(qApp.quit)
        self.close_button.raise_()

    def translateLanguage(self):
        self.close_button.setToolTip(self.tr("close"))

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.mouseSrcPos = event.pos()
            if self.mouseSrcPos.y() <= 40:
                self.mouse_move = True
            else:
                self.current_pos_x = self.total_label.x()
                self.mouse_press = True
        elif event.button() == Qt.RightButton:
            if self.label_move:
                if self.current_index > 0:
                    self.current_index -= 1
                    self.moveCurrentPage(False)

    def mouseReleaseEvent(self, event):
        xpos = 0

        if self.mouse_press:
            if self.label_move:
                self.mouseDstPos = event.pos()
                xpos = self.mouseDstPos.x() - self.mouseSrcPos.x()

                if xpos > 0:
                    if xpos >= WINDOW_ONEBUTTON_WIDTH:
                        if self.current_index > 0:
                            self.current_index -= 1
                            self.moveCurrentPage(False)
                        else:
                            self.moveCurrentPage(True)
                    else:
                        self.moveCurrentPage(True)
                else:
                    if xpos <= -WINDOW_ONEBUTTON_WIDTH:
                        if self.current_index < WINDOW_PAGE_COUNT - 1:
                            self.current_index += 1
                            self.moveCurrentPage(True)
                        else:
                            self.moveCurrentPage(False)
                    else:
                        self.moveCurrentPage(False)

                self.mouse_press = False
        elif self.mouse_move:
            self.mouse_move = False

    def mouseMoveEvent(self, event):
        x = 0
        if self.mouse_press:
            if self.label_move:
                self.mouseDstPos = event.pos()
                x = self.mouseDstPos.x() - self.mouseSrcPos.x()

                self.setLabelMove(False)
                self.total_label.move(self.current_pos_x + x, WINDOW_START_Y)
                self.setLabelMove(True)
        elif self.mouse_move:
            self.mouseDstPos = event.pos()
            self.move(self.pos() + self.mouseDstPos - self.mouseSrcPos)

    def keyPressEvent(self, event):
        if self.label_move:
            key = event.key()
            if key == Qt.Key_Left or key == Qt.Key_Up:
                if self.current_index > 0:
                    self.current_index -= 1
                    self.moveCurrentPage(False)
            elif key == Qt.Key_Right or key == Qt.Key_Down:
                if self.current_index < WINDOW_PAGE_COUNT - 1:
                    self.current_index += 1
                    self.moveCurrentPage(True)

    def changeCurrentPage(self, label):
        for i in range(0, WINDOW_BUTTON_COUNT):
            if label != self.label_array[i]:
                self.label_array[i].setMousePressFlag(False)

        index = 0
        for i in range(0, WINDOW_PAGE_COUNT):
            if label == self.label_array[i]:
                index = i
                break

        if index < self.current_index:
            while index != self.current_index:
                self.current_index -= 1
                self.moveCurrentPage(False)
        elif index > self.current_index:
            while index != self.current_index:
                self.current_index += 1
                self.moveCurrentPage(True)

    def changeCurrentButton(self):
        for i in range(0, WINDOW_BUTTON_COUNT):
            if i != self.current_index:
                self.label_array[i].setMousePressFlag(False)
                self.label_array[i].setPixmap(QPixmap("./wizard/dot_normal.png"))
            else:
                self.label_array[i].setMousePressFlag(True)
                self.label_array[i].setPixmap(QPixmap("./wizard/dot_active.png"))

    def setLabelMove(self, enable):
        self.label_move = enable

    def moveCurrentPage(self, direction):
        self.changeCurrentButton()
        self.setLabelMove(False)

        current_pos_x = self.total_label.x()
        dest_pos_x = -WINDOW_WIDTH * self.current_index
        if direction:
            while current_pos_x > dest_pos_x:
                self.total_label.move(current_pos_x - WINDOW_PAGE_MOVE, WINDOW_START_Y)
                current_pos_x = self.total_label.x()
                qApp.processEvents(QEventLoop.AllEvents)
        else:
            while current_pos_x < dest_pos_x:
                self.total_label.move(current_pos_x + WINDOW_PAGE_MOVE, WINDOW_START_Y)
                current_pos_x = self.total_label.x()
                qApp.processEvents(QEventLoop.AllEvents)

        self.total_label.move(dest_pos_x, WINDOW_START_Y)
        self.setLabelMove(True)


if __name__ == "__main__":
    # if len(sys.argv) != 2:
    # 	print "Usage: python %s locale[en | zh_CN | zh_HK]" % (sys.argv[0])
    # 	sys.exit(1)
    #
    # lang = sys.argv[1]
    # if sys.argv[1] != "en" and sys.argv[1] != "zh_CN" and sys.argv[1] != "zh_HK":
    # 	lang = "en" # set default locale
    lang = "en"
    app = QApplication(sys.argv)
    win = PreviewWidget(lang)
    win.show()
    sys.exit(app.exec_())
