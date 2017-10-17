#!/usr/bin/python  
#-*-coding:utf-8-*-

from PyQt4.QtGui import *
from PyQt4.QtCore import *
from PyQt4.Qt import *

class ChangeSkinWidget(QWidget):
	def __init__(self,parent = None):
		super(ChangeSkinWidget,self).__init__(parent)
		self.setFixedSize(140, 160)
		self.mouse_press = False
		self.mouse_enter = False
		#self.pixmap = QPixmap()
		self.pixmap_name = ""

		self.skin_label =  QLabel() #显示皮肤
		self.skin_name_label =  QLabel() #显示皮肤名称
		self.download_count_label =  QLabel() #显示下载次数
		self.use_skin_button =  QPushButton() #使用此皮肤按钮
		self.setCursor(Qt.PointingHandCursor)

		#修复这里存在无法解释的情况
		#Could not parse stylesheet of widget 0x1df35a8
		self.use_skin_button.setStyleSheet("border-radius:3px;border:1px solid rgb(180, 190, 200);color:rgb(70, 70, 70);background:transparent")
		self.skin_label.setScaledContents(True)
		self.skin_label.setFixedSize(100, 65)
		self.use_skin_button.setFixedSize(85, 25)

		self.background_layout =  QVBoxLayout()
		self.background_layout.addWidget(self.skin_label, 0, Qt.AlignCenter)
		self.background_layout.addWidget(self.skin_name_label, 0, Qt.AlignCenter)
		self.background_layout.addWidget(self.download_count_label, 0, Qt.AlignCenter)
		self.background_layout.addWidget(self.use_skin_button, 0, Qt.AlignCenter)
		self.background_layout.setSpacing(5)
		self.background_layout.setContentsMargins(0, 10, 0, 10)

		self.setLayout(self.background_layout)
		self.skin.connect(self.changeSkin)

		self.translateLanguage()
	
	skin = pyqtSignal()
	
	def changeSkin(self, pixmap_name,  skin_name,  download_count):
		self.background_name = pixmap_name + "_big.png"
		self.pixmap_name = self.background_name

	#更改皮肤背景
		#self.pixmap()
		self.skin_label.setPixmap(QPixmap(self.background_name))

	#更改皮肤名称
		self.skin_name_label.setText(skin_name)

	#更改下载次数
		self.download_count_label.setText(u"download count:" + download_count)

	def translateLanguage(self):
		self.use_skin_button.setText(u"use skin")

	def paintEvent(self,event):
		if(self.mouse_enter):
			#绘制边框
			painter = QPainter(self)
			pen = QPen(QColor(210, 225, 230))
			painter.setPen(pen)
			painter.drawRoundRect(0,0,self.width()-1, self.height()-1, 5, 5)

	def mousePressEvent(self,event):
		#只能是鼠标左键移动和改变大小
		if(event.button() == Qt.LeftButton):
			self.mouse_press = True
			self.emit(SIGNAL("skin"),self.pixmap_name)

	def mouseReleaseEvent(self,event):
		self.mouse_press = False

	def enterEvent(self,event):
		self.mouse_enter = True
		self.update()

	def leaveEvent(self,event):
		self.mouse_enter = False
		self.update()
if __name__ == '__main__':
	import sys
	app = QApplication(sys.argv)
	
	skin = ChangeSkinWidget()
	skin.show()
	
	sys.exit(app.exec_())
