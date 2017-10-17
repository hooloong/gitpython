#!/usr/bin/python  
#-*-coding:utf-8-*-
			
from tool_button import ToolButton
from push_button import PushButton

from PyQt4.QtGui import *
from PyQt4.QtCore import *
from PyQt4.Qt import *

class TitleWidget(QWidget):
	def __init__(self, parent=None):
		super(TitleWidget, self).__init__(parent)
		
		self.skin_button = PushButton(self)
		self.main_menu_button = PushButton(self)
		self.min_button = PushButton(self)
		self.max_button = PushButton(self)
		self.close_button = PushButton(self)
		self.medal_button = QPushButton(self)
		self.button_list = []
		
		#版本标题颜色设置
		self.version_title = QLabel()
		self.version_title.setStyleSheet("color:white")
	
		#设置按钮的图片
		self.skin_button.loadPixmap("./img/sysButton/skin_button.png")
		self.main_menu_button.loadPixmap("./img/sysButton/main_menu.png")
		self.min_button.loadPixmap("./img/sysButton/min_button.png")
		self.max_button.loadPixmap("./img/sysButton/max_button.png")
		self.close_button.loadPixmap("./img/sysButton/close_button.png")
		
		#设置功勋图标
		medal_icon = QIcon ("./img/contentWidget/medal.png")
		self.medal_button.setIcon(medal_icon)
		self.medal_button.setFixedSize(25, 25)
		self.medal_button.setIconSize(QSize(25, 25))
		self.medal_button.setStyleSheet("background:transparent") #透明显示
	
		self.connect(self.skin_button, SIGNAL("clicked()"), self, SIGNAL("showSkin()"))
		self.connect(self.main_menu_button, SIGNAL("clicked()"), self, SIGNAL("showMainMenu()"))
		self.connect(self.min_button, SIGNAL("clicked()"), self, SIGNAL("showMin()"))
		self.connect(self.max_button, SIGNAL("clicked()"), self, SIGNAL("showMax()"))
		self.connect(self.close_button, SIGNAL("clicked()"), self, SIGNAL("showClose()")) #closeWidget self, 
	
		title_layout = QHBoxLayout()
		title_layout.addWidget(self.version_title, 0, Qt.AlignVCenter)
		title_layout.addStretch()
		title_layout.addWidget(self.medal_button, 0, Qt.AlignTop)
		title_layout.addWidget(self.skin_button, 0, Qt.AlignTop)
		title_layout.addWidget(self.main_menu_button, 0, Qt.AlignTop)
		title_layout.addWidget(self.min_button, 0, Qt.AlignTop)
		title_layout.addWidget(self.max_button, 0, Qt.AlignTop)
		title_layout.addWidget(self.close_button, 0, Qt.AlignTop)
		title_layout.setSpacing(0)
		title_layout.setContentsMargins(0, 0, 5, 0)
		self.version_title.setContentsMargins(15, 0, 0, 0)
		self.skin_button.setContentsMargins(0, 0, 10, 0)
	
		#string_list = QStringList 
		string_list = ["./img/toolWidget/tiJian.png", "./img/toolWidget/muMa.png", "./img/toolWidget/louDong.png", \
			       "./img/toolWidget/xiTong.png", "./img/toolWidget/qingLi.png", "./img/toolWidget/jiaSu.png", \
			       "./img/toolWidget/menZhen.png", "./img/toolWidget/ruanJian.png"]
	
		button_layout = QHBoxLayout()
		#还不知道怎么用
		signal_mapper = QSignalMapper(self)
		for i in range(len(string_list)):
		
			self.tool_button = ToolButton(string_list[i])
			#self.tool_button.setParent()
			self.button_list.append(self.tool_button)
			self.connect(self.tool_button, SIGNAL("clicked()"), signal_mapper, SLOT("map()"))
			signal_mapper.setMapping(self.tool_button, QString.number(i, 10))
	
			button_layout.addWidget(self.tool_button, 0, Qt.AlignBottom)
		
		self.connect(signal_mapper, SIGNAL("mapped()"), self, SLOT("turnPage()"))
		
		logo_label = QLabel()
		pixmap = QPixmap ("./img/logo.png")
		logo_label.setPixmap(pixmap)
		logo_label.setFixedSize(pixmap.size())
		logo_label.setCursor(Qt.PointingHandCursor)
	
		button_layout.addStretch()
		button_layout.addWidget(logo_label)
		button_layout.setSpacing(8)
		button_layout.setContentsMargins(15, 0, 0, 0)
	
		main_layout = QVBoxLayout()
		main_layout.addLayout(title_layout)
		main_layout.addLayout(button_layout)
		main_layout.setSpacing(0)
		main_layout.setContentsMargins(0, 0, 0, 0)
	
		self.translateLanguage()

		self.setLayout(main_layout)
		self.setFixedHeight(100)
		self.is_move = False
		


	def translateLanguage(self):
	
		self.version_title.setText(u"360 safe gurd 9.2")
		self.skin_button.setToolTip(u"change skin")
		self.main_menu_button.setToolTip(u"main menu")
		self.min_button.setToolTip(u"minimize")
		self.max_button.setToolTip(u"maximize")
		self.close_button.setToolTip(u"close")
	
		self.button_list[0].setText(u"power")
		self.button_list[1].setText(u"mummy")
		self.button_list[2].setText(u"hole")
		self.button_list[3].setText(u"repair")
		self.button_list[4].setText(u"clear")
		self.button_list[5].setText(u"optimize")
		self.button_list[6].setText(u"expert")
		self.button_list[7].setText(u"software")

#如果不用QApplication.winEvent方法，就要启动以下代码
#	def mousePressEvent(self, e):
#		self.press_point = e.pos()
#		self.is_move = True
#
#	#已修复无法移动的问题
#	def mouseMoveEvent(self, e):
#		if e.buttons() == Qt.LeftButton and self.is_move:
#			parent_widget = self.parentWidget()
#			if parent_widget:
#				parent_point = QPoint()
#				parent_point = parent_widget.pos() #
#				parent_point.setX(parent_point.x() + e.x() - self.press_point.x())
#				parent_point.setY(parent_point.y() + e.y() - self.press_point.y())
#				parent_widget.move(parent_point)
#	
#	def mouseReleaseEvent(self, event):
#		if self.is_move:
#			self.is_move = False
	

#使用winEvent方法，不建议用doubleclick来放大缩小
#	def mouseDoubleClickEvent(self, e):	
#		self.emit(SIGNAL("showMax()"))

	@pyqtSlot()
	def turnPage(self, current_page):	
		current_index = current_page
		for i in range(len(self.button_list)):
			self.tool_button = self.button_list[i]
			if(current_index == i):
				self.tool_button.setMousePress(True)			
			else:
				self.tool_button.setMousePress(False)
		
	

		
if __name__ == '__main__':
	import sys
	
	app = QApplication(sys.argv)
	
	title = TitleWidget()
	title.show()
	
	app.exec_()
		

