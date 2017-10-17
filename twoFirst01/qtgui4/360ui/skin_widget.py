#!/usr/bin/python  
#-*-coding:utf-8-*-

from push_button import *
from change_skin_widget import *
from util import Util

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.Qt import *


class SkinWidget(QWidget):
	def __init__(self, parent = None):
		super(SkinWidget,self).__init__(parent)
	
		self.resize(620, 445)
	
		#初始化为未按下鼠标左键
		self.mouse_press = False
		self.skin_name = QString("")
		self.is_change = False
		self.current_page = 1
	
		#设置标题栏隐藏
		self.setWindowFlags(Qt.FramelessWindowHint | Qt.Dialog)
	
		self.initTitle()
		self.initCenter()
		self.initBottom()
	
		main_layout =  QVBoxLayout()
		main_layout.addLayout(self.title_layout)
		main_layout.addLayout(self.center_layout)
		main_layout.addLayout(self.bottom_layout)
		main_layout.addStretch()
		main_layout.setSpacing(0)
		main_layout.setContentsMargins(0, 0, 0, 0)
	
		self.setLayout(main_layout)
	
		self.translateLanguage()
	
		self.showSkin(QString.number(self.current_page, 10))
	
	
	def initTitle(self):
	
		self.title_label =  QLabel(self)
		self.title_icon_label =  QLabel(self)
		self.close_button =  PushButton(self)
	
		title_pixmap = QPixmap ("./img/safe.ico")
		self.title_icon_label.setPixmap(title_pixmap)
		self.title_icon_label.setFixedSize(16, 16)
		self.title_icon_label.setScaledContents(True)
	
		self.close_button.loadPixmap("./img/sysButton/close.png")
		self.title_label.setFixedHeight(30)
	
		self.title_layout =  QHBoxLayout()
		self.title_layout.addWidget(self.title_icon_label, 0, Qt.AlignVCenter)
		self.title_layout.addWidget(self.title_label, 0, Qt.AlignVCenter)
		self.title_layout.addStretch()
		self.title_layout.addWidget(self.close_button, 0, Qt.AlignTop)
		self.title_layout.setSpacing(5)
		self.title_layout.setContentsMargins(10, 0, 5, 0)
	
		self.title_label.setStyleSheet("color:white")
		self.connect(self.close_button, SIGNAL("clicked()"), SLOT("close()"))
	
	
	def initCenter(self):
	
		skin_list=[u"./img/skin/0",u"./img/skin/1",u"./img/skin/2",u"./img/skin/3",u"./img/skin/4",\
			u"./img/skin/5",u"./img/skin/6",u"./img/skin/7",u"./img/skin/8",u"./img/skin/9",\
			u"./img/skin/10",u"./img/skin/11",u"./img/skin/12",u"./img/skin/13",u"./img/skin/14",\
			u"./img/skin/15",u"./img/skin/16",u"./img/skin/17",u"./img/skin/18",u"./img/skin/19",\
			u"./img/skin/20",u"./img/skin/21",u"./img/skin/22",u"./img/skin/23"]
	
		self.center_layout =  QGridLayout()
		self.center_layout.setSpacing(5)
		self.center_layout.setContentsMargins(5, 35, 5, 0)
	
		self.change_skin_widget_0 =  ChangeSkinWidget()
		self.change_skin_widget_1 =  ChangeSkinWidget()
		self.change_skin_widget_2 =  ChangeSkinWidget()
		self.change_skin_widget_3 =  ChangeSkinWidget()
		self.change_skin_widget_4 =  ChangeSkinWidget()
		self.change_skin_widget_5 =  ChangeSkinWidget()
		self.change_skin_widget_6 =  ChangeSkinWidget()
		self.change_skin_widget_7 =  ChangeSkinWidget()
	
		self.connect(self.change_skin_widget_0, SIGNAL("changeSkin()"),SLOT("varyfySkin()"))
		self.connect(self.change_skin_widget_1, SIGNAL("changeSkin()"),SLOT("varyfySkin()"))
		self.connect(self.change_skin_widget_2, SIGNAL("changeSkin()"),SLOT("varyfySkin()"))
		self.connect(self.change_skin_widget_3, SIGNAL("changeSkin()"),SLOT("varyfySkin()"))
		self.connect(self.change_skin_widget_4, SIGNAL("changeSkin()"),SLOT("varyfySkin()"))
		self.connect(self.change_skin_widget_5, SIGNAL("changeSkin()"),SLOT("varyfySkin()"))
		self.connect(self.change_skin_widget_6, SIGNAL("changeSkin()"),SLOT("varyfySkin()"))
		self.connect(self.change_skin_widget_7, SIGNAL("changeSkin()"),SLOT("varyfySkin()"))
	
		self.center_layout.addWidget(self.change_skin_widget_0, 0, 0)
		self.center_layout.addWidget(self.change_skin_widget_1, 0, 1)
		self.center_layout.addWidget(self.change_skin_widget_2, 0, 2)
		self.center_layout.addWidget(self.change_skin_widget_3, 0, 3)
		self.center_layout.addWidget(self.change_skin_widget_4, 1, 0)
		self.center_layout.addWidget(self.change_skin_widget_5, 1, 1)
		self.center_layout.addWidget(self.change_skin_widget_6, 1, 2)
		self.center_layout.addWidget(self.change_skin_widget_7, 1, 3)
	
		skin_list_count = len(skin_list)
		self.page_count = skin_list_count / 8
		self.page_count_point = skin_list_count % 8
		if(self.page_count_point > 0):	
			self.page_count = self.page_count + 1
		
	
	
	def initBottom(self):
		self.signal_mapper =  QSignalMapper(self) #QSignalMapper *
		self.button_list =  []
		for i in range(self.page_count):
			self.page_button =  QPushButton(self)
			self.page_button.setFixedWidth(20)
			self.page_button.setText(QString.number(i+1, 10))
			self.page_button.setStyleSheet("color:rgb(0, 120, 230);background:transparent")
			self.page_button.setCursor(Qt.PointingHandCursor)
			self.connect(self.page_button, SIGNAL("clicked()"), self.signal_mapper, SLOT("map(QString)"))
			self.signal_mapper.setMapping(self.page_button, self.page_button.text())
			self.button_list.append(self.page_button)
		
	
		self.first_page_button =  QPushButton(self)
		self.previous_page_button =  QPushButton(self)
		self.next_page_button =  QPushButton(self)
		self.last_page_button =  QPushButton(self)
		self.first_page_button.setFixedWidth(50)
		self.previous_page_button.setFixedWidth(50)
		self.next_page_button.setFixedWidth(50)
		self.last_page_button.setFixedWidth(50)
		self.first_page_button.setCursor(Qt.PointingHandCursor)
		self.previous_page_button.setCursor(Qt.PointingHandCursor)
		self.next_page_button.setCursor(Qt.PointingHandCursor)
		self.last_page_button.setCursor(Qt.PointingHandCursor)
		
		#修复样式
		self.first_page_button.setStyleSheet("color:rgb(0, 120, 230);background:transparent")
		self.previous_page_button.setStyleSheet("color:rgb(0, 120, 230);background:transparent")
		self.next_page_button.setStyleSheet("color:rgb(0, 120, 230);background:transparent")
		self.last_page_button.setStyleSheet("color:rgb(0, 120, 230);background:transparent")
	
		self.first_page_button.setText(u"first")
		self.previous_page_button.setText(u"previous")
		self.next_page_button.setText(u"next")
		self.last_page_button.setText(u"last")
	
		self.connect(self.first_page_button, SIGNAL("clicked()"), self.signal_mapper, SLOT("map()"))
		self.connect(self.previous_page_button, SIGNAL("clicked()"), self.signal_mapper, SLOT("map()"))
		self.connect(self.next_page_button, SIGNAL("clicked()"), self.signal_mapper, SLOT("map()"))
		self.connect(self.last_page_button, SIGNAL("clicked()"), self.signal_mapper, SLOT("map()"))
		self.signal_mapper.setMapping(self.first_page_button, "first")
		self.signal_mapper.setMapping(self.previous_page_button, "previous")
		self.signal_mapper.setMapping(self.next_page_button, "next")
		self.signal_mapper.setMapping(self.last_page_button, "last")
		self.connect(self.signal_mapper, SIGNAL("mapped()"), self, SLOT("showSkin()"))
	
		self.bottom_layout =  QHBoxLayout()
		self.bottom_layout.addStretch()
		self.bottom_layout.addWidget(self.first_page_button, 0, Qt.AlignVCenter)
		self.bottom_layout.addWidget(self.previous_page_button, 0, Qt.AlignVCenter)
		for i in range(len(self.button_list)):
			self.page_button = self.button_list[i]
			self.bottom_layout.addWidget(self.page_button, 0, Qt.AlignVCenter)
		
		self.bottom_layout.addWidget(self.next_page_button, 0, Qt.AlignVCenter)
		self.bottom_layout.addWidget(self.last_page_button, 0, Qt.AlignVCenter)
		self.bottom_layout.addStretch()
		self.bottom_layout.setSpacing(2)
		self.bottom_layout.setContentsMargins(0, 10, 0, 0)
	
	@pyqtSlot()
	def showSkin(self, current_skin):	
		if(current_skin == "first"):		
			self.current_page = 1		
		elif(current_skin == "previous"):		
			if(self.current_page > 2):			
				self.current_page = self.current_page - 1
		elif(current_skin == "next"):		
			if(self.current_page < self.page_count):
				self.current_page = self.current_page + 1

		elif(current_skin == "last"):
			self.current_page = self.page_count
		
		else:  
			self.current_page,ok = current_skin.toInt(10)
		
		if(self.current_page == 1):		
			self.next_page_button.show()
			self.last_page_button.show()
			self.first_page_button.hide()
			self.previous_page_button.hide()
		
		elif(self.current_page == self.page_count):		
			self.first_page_button.show()
			self.previous_page_button.show()
			self.next_page_button.hide()
			self.last_page_button.hide()		
		else:		
			self.first_page_button.hide()
			self.previous_page_button.show()
			self.next_page_button.show()
			self.last_page_button.hide()
		
	
		#第一页为0-7 显示至previous_total_page个
		self.previous_total_page = (self.current_page - 1) * 8#
		
		self.tip_index = self.previous_total_page
		if(self.previous_total_page > 0):
			self.tip_index = self.previous_total_page - 1
		
		self.change_skin_widget_0.changeSkin("./img/skin/"+ QString.number(self.previous_total_page+1, 10), self.tip_list[self.tip_index+1], "11")
		self.change_skin_widget_1.changeSkin("./img/skin/"+ QString.number(self.previous_total_page+2, 10), self.tip_list[self.tip_index+2], "11")
		self.change_skin_widget_2.changeSkin("./img/skin/"+ QString.number(self.previous_total_page+3, 10), self.tip_list[self.tip_index+3], "11")
		self.change_skin_widget_3.changeSkin("./img/skin/"+ QString.number(self.previous_total_page+4, 10), self.tip_list[self.tip_index+4], "11")
		self.change_skin_widget_4.changeSkin("./img/skin/"+ QString.number(self.previous_total_page+5, 10), self.tip_list[self.tip_index+5], "11")
		self.change_skin_widget_5.changeSkin("./img/skin/"+ QString.number(self.previous_total_page+6, 10), self.tip_list[self.tip_index+6], "11")
		self.change_skin_widget_6.changeSkin("./img/skin/"+ QString.number(self.previous_total_page+7, 10), self.tip_list[self.tip_index+7], "11")
		self.change_skin_widget_7.changeSkin("./img/skin/"+ QString.number(self.previous_total_page+8, 10), self.tip_list[self.tip_index+8], "11")
	
	
	def translateLanguage(self):	
		self.title_label.setText(u"title")
		self.close_button.setToolTip(u"close")
	
		self.tip_list= ["profound life",u"blue sea",u"red heart",u"lovely baby",u"transparent water",\
			u"flower",u"great sunshine",u"shadow amazement",u"360 pet",u"beautiful stone",\
			u"yellow energy",u"magic world",u"intense emotion",u"dream sky",u"angry bird",\
			u"graceful jazz",u"card",u"summer cool",u"blue world",u"woodwind",\
			u"pink mood",u"across time",u"six year"]
	
	@pyqtSlot()
	def varyfySkin(self, skin_name):
	
		self.skin_name = skin_name
		self.is_change = True
		self.update()
		self.emit(SIGNAL("skin"),skin_name)
	
	
	def paintEvent(self,event):
	
		if(~self.is_change):
			pass
		
			#uti = Util()
			#is_read = uti.readInit(QString("./user.ini"), QString("skin"), self.skin_name)
			#if(is_read):
			
				#if(self.skin_name.isEmpty()):
				
					#self.skin_name = QString(":/skin/17_big")
				
			
			#else:
			
				#self.skin_name = QString(":/skin/17_big")
			
		self.skin_name = QString("./img/skin/17_big.png")
		painter = QPainter (self)
		painter.drawPixmap(self.rect(), QPixmap(self.skin_name))
	
		painter2 = QPainter (self)
		linear2 = QLinearGradient(QPointF(self.rect().topLeft()), QPointF(self.rect().bottomLeft()))
		linear2.setColorAt(0, Qt.white)
		linear2.setColorAt(0.5, Qt.white)
		linear2.setColorAt(1, Qt.white)
		painter2.setPen(Qt.white) #设定画笔颜色，到时侯就是边框颜色
		painter2.setBrush(linear2)
		painter2.drawRect(QRect(0, 30, self.width(), self.height()-30))
	
		painter3 = QPainter (self)
		painter3.setPen(Qt.gray)
		painter3.drawPolyline(QPointF(0, 30), QPointF(0, self.height()-1), QPointF(self.width()-1, self.height()-1), QPointF(self.width()-1, 30))
	
	
	def mousePressEvent(self,event ):
	
		#只能是鼠标左键移动和改变大小
		if(event.button() == Qt.LeftButton): 
			self.mouse_press = True
		
		#窗口移动距离
		self.move_point = event.globalPos() - self.pos() 
	
	
	def mouseReleaseEvent(self,event):
	
		self.mouse_press = False
	
	
	def mouseMoveEvent(self,event):
	
		#移动窗口
		if(self.mouse_press):   
			self.move_pos = event.globalPos()
			self.move(self.move_pos - self.move_point)
			
			
if __name__ == '__main__':
	import sys
	
	app = QApplication(sys.argv)
	
	skin = SkinWidget()
	skin.show()
	
	sys.exit(app.exec_())
	




#endif # SKIN_WIDGET_H
