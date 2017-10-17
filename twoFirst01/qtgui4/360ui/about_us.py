#!/usr/bin/python  
#-*-coding:utf-8-*-

from push_button import PushButton
import util
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from PyQt4.Qt import *


class AboutUsDialog(QDialog):
	
	def __init__(self, parent=None):
		super(AboutUsDialog, self).__init__(parent)
				
		self.title_label = QLabel(self)
		self.title_label.setFixedHeight(30)
		self.title_label.setStyleSheet("color:white")
		
		self.title_icon_label = QLabel(self)
		self.title_icon_label.setPixmap(QPixmap("./img/safe.ico"))
		self.title_icon_label.setFixedSize(16, 16)
		self.title_icon_label.setScaledContents(True)
		
		self.close_button = PushButton()
		self.close_button.loadPixmap("./img/sysButton/close.png")
		
		self.title_info_label = QLabel(self)
		self.title_info_label.setStyleSheet("color:rgb(30,170,60)")
		self.title_info_label.setFont(QFont("微软雅黑", 14, QFont.Bold, False))
		
		self.info_label = QLabel(self)
		self.info_label.setContentsMargins(0, 0, 0, 40)
		self.info_label.setStyleSheet("color:rgb(30,170,60)")
		self.info_label.setFont(QFont("微软雅黑", 10, QFont.Bold, False))
		self.info_label.setContentsMargins(0, 0, 0, 40)
		
		self.version_label = QLabel(self)		
		
		self.mummy_label = QLabel(self)
		
		self.copyright_label = QLabel(self)
		self.copyright_label.setStyleSheet("color:gray")
		
		self.icon_label = QLabel(self)
		self.pixmap = QPixmap ("./img/360safe.png")
		self.icon_label.setPixmap(self.pixmap)
		self.icon_label.setFixedSize(self.pixmap.size())
		
		self.ok_button = QPushButton(self)
		self.ok_button.setFixedSize(75, 25)
		self.ok_button.setStyleSheet("QPushButton{border:1px solid lightgray;background:rgb(230,230,230)}"
			"QPushButton:hover{border-color:green;background:transparent}")
					
		self.setWindowFlags(Qt.FramelessWindowHint | Qt.Dialog)
		#布局标题		
		self.title_layout = QHBoxLayout()
		self.title_layout.addWidget(self.title_icon_label, 0, Qt.AlignVCenter)
		self.title_layout.addWidget(self.title_icon_label, 0, Qt.AlignVCenter)
		self.title_layout.addWidget(self.title_label, 0, Qt.AlignVCenter)
		self.title_layout.addStretch() #平均
		self.title_layout.addWidget(self.close_button, 0, Qt.AlignTop)
		
		#布局信息列表
		self.v1_layout = QVBoxLayout()
		self.v1_layout.addWidget(self.title_info_label)
		self.v1_layout.addWidget(self.info_label)
		self.v1_layout.setSpacing(10)

		self.v2_layout = QVBoxLayout()
		self.v2_layout.addWidget(self.version_label)
		self.v2_layout.addWidget(self.mummy_label)
		self.v2_layout.addWidget(self.copyright_label)
		self.v2_layout.setSpacing(10)
		
		self.v_layout = QVBoxLayout()
		self.v_layout.addLayout(self.v1_layout)
		self.v_layout.addLayout(self.v2_layout)
		self.v_layout.addStretch() #平均分配
		self.v_layout.setSpacing(50)
		self.v_layout.setContentsMargins(0, 15, 0, 0) #设置距离边界的值

		#布局地下配置
		self.bottom_layout = QHBoxLayout()
		self.bottom_layout.addStretch()
		self.bottom_layout.addWidget(self.ok_button)
		self.bottom_layout.setSpacing(0)
		self.bottom_layout.setContentsMargins(0, 0, 30, 20)
	
		self.h_layout = QHBoxLayout()
		self.h_layout.addLayout(self.v_layout)
		self.h_layout.addWidget(self.icon_label)
		self.h_layout.setSpacing(0)
		self.h_layout.setContentsMargins(40, 0, 20, 10)
	
		self.main_layout = QVBoxLayout()
		self.main_layout.addLayout(self.title_layout)
		self.main_layout.addStretch()
		self.main_layout.addLayout(self.h_layout)
		self.main_layout.addLayout(self.bottom_layout)
		self.main_layout.setSpacing(0)
		self.main_layout.setContentsMargins(0, 0, 0, 0)
	
		self.setLayout(self.main_layout)
		
		
		self.title_layout.setSpacing(0)
		self.title_layout.setContentsMargins(10, 0, 5, 0)
				
		self.translateLanguage()
		self.resize(520, 290)
		
		self.connect(self.ok_button, SIGNAL("clicked()"), self, SLOT("hide()"))
		self.connect(self.close_button, SIGNAL("clicked()"), self, SLOT("close()"))
	
	
	def paintEvent(self, event):
		
		self.painter = QPainter()
		self.painter.begin(self)
		self.painter.drawPixmap(self.rect(), QPixmap("./img/skin/17_big.png"))
		self.painter.end()
		linear2 = QLinearGradient(QPoint(self.rect().topLeft()), QPoint(self.rect().bottomLeft()))
		linear2.start()
		linear2.setColorAt(0, Qt.white)
		linear2.setColorAt(0.5, Qt.white)
		linear2.setColorAt(1, Qt.white)
		linear2.finalStop()
		self.painter2 = QPainter()
		self.painter2.begin(self)
		self.painter2.setPen(Qt.white) #设定画笔颜色，到时侯就是边框颜色
		self.painter2.setBrush(linear2);
		self.painter2.drawRect(QRect(0, 30, self.width(), self.height() - 30));
		self.painter2.end()
		
		self.painter3 = QPainter()
		self.painter3.begin(self)
		self.painter3.setPen(Qt.gray)
		self.painter3.drawPolyline(QPointF(0, 30), QPointF(0, self.height() - 1), QPointF(self.width() - 1, self.height() - 1), QPointF(self.width() - 1, 30))
		self.painter3.end()
	
	def translateLanguage(self):
		self.title_label.setText(u"360安全卫士")
		self.title_info_label.setText(u"360安全卫士")
		self.info_label.setText(u"杀木马 防盗号 电脑加速")
		self.version_label.setText(u"主程序版本:9.1.0.2002")
		self.mummy_label.setText(u"备用木马库:2013-8-19")
		self.copyright_label.setText(u"Copyright(c) 360.cn Inc.All Rights Reserved.")
		#self.close_button.setToolTip(self.tr("close"))
		self.ok_button.setText(u"确定")

	def mousePressEvent(self, event):
		if event.button() == Qt.LeftButton:
			self.dragPosition = event.globalPos() - self.frameGeometry().topLeft()
			QApplication.postEvent(self, QEvent(174))
			event.accept()

	def mouseMoveEvent(self, event):
		if event.buttons() == Qt.LeftButton:
			self.move(event.globalPos() - self.dragPosition)
			event.accept()

	def isInTitle(self, xPos, yPos):
		return yPos < 30 and xPos < 456
									
if __name__ == '__main__':
	
	import sys
	app = QApplication(sys.argv)
	aboutus = AboutUsDialog()
	aboutus.show()
	sys.exit(app.exec_())	
