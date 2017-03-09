__author__ = 'hooloongge'
# -*- coding: utf-8 -*-
import sys
from PyQt4 import QtGui, QtCore
import time, datetime


class Main(QtGui.QWidget):
    def __init__(self, parent=None):
        super(Main, self).__init__(parent)
        self.layout()

    def layout(self):
        self.setWindowTitle(u'The_Third_Wave：简单Threading教程')

        self.text_area_l = QtGui.QTextBrowser()
        self.thread_start_l = QtGui.QPushButton('Start Left')
        self.thread_start_l.clicked.connect(self.start_threads_l)
        self.text_area_r = QtGui.QTextBrowser()
        self.thread_start_r = QtGui.QPushButton('Start Right')
        self.thread_start_r.clicked.connect(self.start_threads_r)

        lef_layout = QtGui.QVBoxLayout()
        lef_layout.addWidget(self.text_area_l)

        button_layout = QtGui.QVBoxLayout()
        button_layout.addWidget(self.thread_start_l)
        button_layout.addWidget(self.thread_start_r)

        right_layout = QtGui.QVBoxLayout()
        right_layout.addWidget(self.text_area_r)

        grid_layout = QtGui.QGridLayout()
        grid_layout.addLayout(lef_layout, 0, 0)
        grid_layout.addLayout(button_layout, 0, 1)
        grid_layout.addLayout(right_layout, 0, 2)

        self.setLayout(grid_layout)

    def start_threads_l(self):
        thread = MyThread_l(self)  # 创建线程
        thread.trigger.connect(self.update_text_l)  # 连接信号！
        thread.setup(range(0, 10))  # 传递参数
        thread.start()  # 启动线程

    def update_text_l(self, message):
        self.text_area_l.insertPlainText(message)

    def start_threads_r(self):
        thread = MyThread_r(self)  # 创建线程
        thread.trigger.connect(self.update_text_r)  # 连接信号！
        thread.setup(range(10, 20))  # 传递参数
        thread.start()  # 启动线程

    def update_text_r(self, message):
        self.text_area_r.insertPlainText(message)


class MyThread_l(QtCore.QThread):
    trigger = QtCore.pyqtSignal(str)  # trigger传输的内容是字符串

    def __init__(self, parent=None):
        super(MyThread_l, self).__init__(parent)

    def setup(self, args):
        self.args = args

    def run(self):  # 很多时候都必重写run方法, 线程start后自动运行
        self.my_function()

    def my_function(self):
        # 把代码中的print全部改为trigger.emit
        # print u"线程启动了！"
        self.trigger.emit(u"左边线程启动了！\n")
        for i in self.args:
            time.sleep(3)
            self.trigger.emit(u"当前为：" + str(i) + "----" + str(datetime.datetime.now()) + "\n")
        self.trigger.emit(u"左边线程结束了！\n")


class MyThread_r(QtCore.QThread):
    trigger = QtCore.pyqtSignal(str)  # trigger传输的内容是字符串

    def __init__(self, parent=None):
        super(MyThread_r, self).__init__(parent)

    def setup(self, args):
        self.args = args

    def run(self):  # 很多时候都必重写run方法, 线程start后自动运行
        self.my_function()

    def my_function(self):
        # 把代码中的print全部改为trigger.emit
        self.trigger.emit(u"右边线程启动了！\n")
        for i in self.args:
            time.sleep(3)
            self.trigger.emit(u"当前为：" + str(i) + "----" + str(datetime.datetime.now()) + "\n")
        self.trigger.emit(u"右边线程结束了！\n")


if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    mainwindow = Main()
    mainwindow.show()
    sys.exit(app.exec_())