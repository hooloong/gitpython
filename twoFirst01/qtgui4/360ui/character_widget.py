#!/usr/bin/python  
#-*-coding:utf-8-*-

from push_button import *
from clabel import *
from common import *

from PyQt4.QtGui import *
from PyQt4.QtCore import *
from PyQt4.Qt import *


class CharacterWidget(QWidget):
	def __init__(self, parent=None):
		super(CharacterWidget, self).__init__()
		self.mouse_press = False
		self.mouse_move = False
		self.current_index = 0 #当前图片下标
		self.current_pos_x = 0
		#self.name_list = QStringList()
		self.m_mouseSrcPos = QPoint()
		self.m_mouseDstPos = QPoint()
		self.label_move = False
		self.label_array = [CLabel(), CLabel(), CLabel(), CLabel()] #存储图片的数组 

		self.resize(QSize(WINDOW_WIDTH, WINDOW_HEIGHT))
		self.setWindowFlags(Qt.FramelessWindowHint)

		self.background_label = QLabel(self) #背景图片
		self.background_label.setPixmap(QPixmap("./img/Character/bg_bottom.png"))
		self.background_label.setGeometry(QRect(0, 0, self.width(), self.height()))

		#将4张图片合成一张
		self.pixmap = QPixmap(QSize(self.width() * WINDOW_PAGE_COUNT, WINDOW_HEIGHT)) #
		painter = QPainter(self.pixmap)
		for i  in range(WINDOW_PAGE_COUNT):
			painter.drawImage(QRect(WINDOW_WIDTH * i, 0, WINDOW_WIDTH, WINDOW_HEIGHT), \
				QImage(QString("./img/Character/desktop_%1.png").arg(i)))
		self.total_label = QLabel(self) #图片（结合体）
		self.total_label.resize(self.pixmap.size())
		self.total_label.setPixmap(self.pixmap)
		self.total_label.move(WINDOW_START_X, WINDOW_START_Y)

		self.close_button = PushButton(self)  #关闭按钮
		self.translateLanguage()
		for i in range(WINDOW_BUTTON_COUNT):
			label = CLabel(self)
			label.resize(QSize(155, 45))
			label.setPixmap(QPixmap(QString("./img/Character/btn_%1").arg(i)))
			label.setText(self.name_list[i])
			label.move(8 + i * 170, 319)

			#修复无法响应clicked事件的问题
#			self.connect(self.label, SIGNAL("clicked()"), self, SLOT("changeCurrentPage(CLabel())"))
			label.signalLabelPress.connect(self.changeCurrentPage)
			self.label_array[i] = label
		self.label_array[0].setMousePressFlag(False)

		self.close_button.loadPixmap("./img/sysButton/close.png")
		self.close_button.move(self.width() - 52, 0)
		self.connect(self.close_button, SIGNAL("clicked()"), self, SLOT("close()"))


	def translateLanguage(self):
		self.name_list = [u"function", u"clear cookie", u"triggerman", u"booster"]
		self.close_button.setToolTip(u"close")

	def mousePressEvent(self, event):
		if(event.button() == Qt.LeftButton):
			self.m_mouseSrcPos = event.pos()
			if(self.m_mouseSrcPos.y() <= 40):
				self.mouse_move = True
			else:
				self.current_pos_x = self.total_label.x()
				self.mouse_press = True
		elif(event.button() == Qt.RightButton):
			if(self.label_move):
				if(self.current_index > 0):
					self.current_index = self.current_index - 1
					self.moveCurrentPage(False) #右移

#这里的代码会导致会混乱
#	def mouseReleaseEvent(self, event):
#		self.xpos = 0
#		if (self.mouse_press):
#			if (self.label_move):
#				self.m_mouseDstPos = event.pos()
#				self.xpos = self.m_mouseDstPos.x() - self.m_mouseSrcPos.x()
#				if(self.xpos > 0):#右移
#					if(self.xpos >= WINDOW_ONEBUTTON_WIDTH):
#						if(self.current_index > 0):
#							self.current_index = self.current_index - 1
#							self.moveCurrentPage(False) #右移
#						else:
#							self.moveCurrentPage(True) #左移
#					else:
#						self.moveCurrentPage(True) #左移
#				else: #左移
#					if(self.xpos <= -WINDOW_ONEBUTTON_WIDTH):
#						if(self.current_index < WINDOW_PAGE_COUNT - 1):
#							self.current_index = self.current_index + 1
#							self.moveCurrentPage(True) #左移
#						else:
#							self.moveCurrentPage(False) #右移
#					else:
#						self.moveCurrentPage(False) #右移
#				self.mouse_press = False
#		elif(self.mouse_move):
#			self.mouse_move = False

	
	def changeCurrentPage(self,label):
		
		for i in range(WINDOW_BUTTON_COUNT):
			if(label != self.label_array[i]):
				self.label_array[i].setMousePressFlag(False)
		#获取点击的图标下标
		index = 0
		for i  in range(WINDOW_PAGE_COUNT):
			if(label == self.label_array[i]):
				index = i
				break	#这里从return改为break
			
		#若下标小于当前下标右移，否则左移
		if(index < self.current_index):
			while(index != self.current_index):
				self.current_index = self.current_index - 1
				self.moveCurrentPage(False)
		elif(index > self.current_index):
			while(index != self.current_index):
				self.current_index = self.current_index + 1
				self.moveCurrentPage(True)

#	def mouseMoveEvent(self, event):
#		x = 10
#		if(self.mouse_press):
#			if(self.label_move):
#				self.m_mouseDstPos = event.pos()
#				x = self.m_mouseDstPos.x() - self.m_mouseSrcPos.x()
#				self.setLabelMove(False)
#				self.total_label.move(self.current_pos_x + x, WINDOW_START_Y)
#				self.setLabelMove(True)
#		elif(self.mouse_move):
#			self.m_mouseDstPos = event.pos()
#			self.move(event.pos() + self.m_mouseDstPos - self.m_mouseSrcPos) #注意debug


	def keyPressEvent(self, e):
		if(self.label_move):			
			if e.key() == Qt.Key_Left | e.key() == Qt.Key_Up:
				if(self.current_index > 0):
					self.current_index = self.current_index - 1
					self.moveCurrentPage(False) #右移
					
				elif e.key() == Qt.Key_Down | e.key() == Qt.Key_Right:
					if(self.current_index < WINDOW_PAGE_COUNT - 1):
						self.current_index = self.current_index + 1
						self.moveCurrentPage(True) #左移


	def moveCurrentPage(self, direction):
		#改变当前页面对应的按钮
		self.changeCurrentButton()

		#图片的几个分割点
		#0-680, 680-1360, 1360-2040, 2040-2720
		#真:向左移  假:向右移

		#左移的几种可能性,对于x坐标
		#index=0, 将label移动到-680*0
		#index=1, 将label移动到-680*1
		#index=2, 将label移动到-680*2
		#index=3, 将label移动到-680*3
		self.setLabelMove(False)
		self.current_pos_x = self.total_label.x() #当前label坐标
		self.dest_pos_x = -WINDOW_WIDTH * self.current_index #目标X坐标
		if(direction):
			if(self.current_pos_x > self.dest_pos_x):
				self.total_label.move(self.current_pos_x - WINDOW_PAGE_MOVE, WINDOW_START_Y)
				self.current_pos_x = self.total_label.x()
				qApp.processEvents(QEventLoop.AllEvents)
		else:
			if(self.current_pos_x < self.dest_pos_x):

				self.total_label.move(self.current_pos_x + WINDOW_PAGE_MOVE, WINDOW_START_Y)
				self.current_pos_x = self.total_label.x()
				qApp.processEvents(QEventLoop.AllEvents)
		self.total_label.move(self.dest_pos_x, WINDOW_START_Y)
		self.setLabelMove(True)

	def changeCurrentButton(self):
		for i in range(WINDOW_BUTTON_COUNT):
			if(i != self.current_index):
				self.label_array[i].setMousePressFlag(False)
			else:
				self.label_array[i].setMousePressFlag(True)

	def setLabelMove(self, enable):
		self.label_move = enable
		
if __name__ == '__main__':
	import sys
	app = QApplication(sys.argv)
	Character = CharacterWidget()
	Character.show()
	sys.exit(app.exec_())
	





