#!/usr/bin/python  
#-*-coding:utf-8-*-


from PyQt4.QtGui import *
from PyQt4.QtCore import *
from PyQt4.Qt import *

class ContentWidget(QWidget):
	def __init__(self, parent=None):
		super(ContentWidget, self).__init__(parent)
		self.palette = QPalette()
		self.right_splitter = QSplitter()
		self.right_top_widget = QWidget()
		self.right_center_widget = QWidget()
		self.right_bottom_widget = QWidget()
		self.right_center_function_widget = QWidget()
		self.left_widget = QWidget()
		
		self.palette.setBrush(QPalette.Window, QBrush(Qt.white))
		self.setPalette(self.palette)
		self.setAutoFillBackground(True)
		self.main_splitter = QSplitter()
		self.main_splitter.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
		self.main_splitter.setOrientation(Qt.Horizontal)
		self.main_splitter.setHandleWidth(1)
		self.main_splitter.setStyleSheet("QSplitter.handle{background:lightgray}")
		self.initLeft()
		self.initRight()
		self.initRightTop()
		self.initRightCenter()
		self.initRightCenterFunction()
		self.initRightBottom()
		self.right_splitter.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
		self.right_splitter.setOrientation(Qt.Vertical)
		self.right_splitter.setHandleWidth(1)
		self.right_splitter.setStyleSheet("QSplitter.handle{background:lightgray}")
		self.right_top_widget.setFixedSize(250, 130)
		self.right_center_widget.setFixedSize(250, 90)
		self.right_bottom_widget.setFixedSize(250, 30)
		self.right_splitter.addWidget(self.right_top_widget)
		self.right_splitter.addWidget(self.right_center_widget)
		self.right_splitter.addWidget(self.right_center_function_widget)
		self.right_splitter.addWidget(self.right_bottom_widget)
		self.main_splitter.addWidget(self.left_widget)
		self.main_splitter.addWidget(self.right_splitter)

		#禁止拖动
		for i in range(self.right_splitter.count()):
			handle = QSplitterHandle(Qt.Horizontal, self.right_splitter)
			self.right_splitter.handle(i)
			handle.setEnabled(False)
		
	
		for i in range(self.main_splitter.count()):		    
			handle = QSplitterHandle(Qt.Horizontal, self.right_splitter)
			self.main_splitter.handle(i)
			handle.setEnabled(False)
		self.main_layout = QHBoxLayout()
		self.main_layout.addWidget(self.main_splitter)
		self.main_layout.setSpacing(0)
		self.main_layout.setContentsMargins(0, 0, 0, 0)
		self.setLayout(self.main_layout)
		self.translateLanguage()


	def initLeft(self):

		#self.left_widget =  QWidget()
		self.label = QLabel()
		self.suggest_label = QLabel()
		self.system_safe_label = QLabel()
		self.power_button = QPushButton()
	
		self.left_widget.resize(650, 500)
	
		label_pixmap = QPixmap ("./img/contentWidget/computer.png")
		self.label.setPixmap(label_pixmap)
		self.label.setFixedSize(label_pixmap.size())
	
		suggest_font = QFont()  #= self.suggest_label.font()
		suggest_font.setPointSize(12)
		suggest_font.setBold(True)
		self.suggest_label.setFont(suggest_font)
		self.suggest_label.setStyleSheet("color:gray")
	
		system_safe_font = QFont()#  = self.system_safe_label.font()
		system_safe_font.setBold(True)
		self.system_safe_label.setFont(system_safe_font)
		self.system_safe_label.setStyleSheet("color:gray")
	
		pixmap = QPixmap("./img/contentWidget/power.png") #
		self.power_button.setIcon(QIcon(pixmap))
		self.power_button.setIconSize(pixmap.size())
		self.power_button.setFixedSize(180, 70)
		self.power_button.setStyleSheet("QPushButton{border-radius:5px;background:rgb(110, 190, 10);color:white}"
			"QPushButton:hover{background:rgb(140, 220, 35)}")
		power_font = QFont()  #= self.power_button.font()
		power_font.setPointSize(16)
		self.power_button.setFont(power_font)
	
		v_layout = QVBoxLayout()
		v_layout.addWidget(self.suggest_label)
		v_layout.addWidget(self.system_safe_label)
		v_layout.addStretch()
		v_layout.setSpacing(15)
		v_layout.setContentsMargins(0, 20, 0, 0)
	
		h_layout = QHBoxLayout()
		h_layout.addWidget(self.label, 0, Qt.AlignTop)
		h_layout.addLayout(v_layout)
		h_layout.addStretch()
		h_layout.setSpacing(20)
		h_layout.setContentsMargins(30, 20, 0, 0)
	
		main_layout = QVBoxLayout()
		main_layout.addLayout(h_layout)
		main_layout.addWidget(self.power_button, 0, Qt.AlignCenter)
		main_layout.addStretch()
		main_layout.setSpacing(0)
		main_layout.setContentsMargins(0, 0, 0, 0)
	
		self.left_widget.setLayout(main_layout)


	def initRight(self):

		self.right_splitter = QSplitter()
		#self.right_splitter.resize(250, 500)


	def initRightTop(self):

		self.right_top_widget = QWidget()
		self.login_button = QPushButton()
		priv_label = QLabel()
		self.info_label = QLabel()
		self.privilege_label = QLabel()
		self.register_button = QPushButton()
		safe_button = QPushButton()
		tab_button = QPushButton()
		pet_button = QPushButton()
		lottery_button = QPushButton()
		cloud_five_button = QPushButton()
		caipiao_button = QPushButton()
	
		self.login_button.setFixedSize(240, 60)
		self.login_button.setStyleSheet("QPushButton{color:green;border-image:url(./img/contentWidget/login.png)}"
			"QPushButton:hover{color:rgb(110, 190, 10)}")
		login_font = QFont()#  = self.login_button.font()
		login_font.setBold(True)
		login_font.setPointSize(12)
		self.login_button.setFont(login_font)
	
		priv_label.setPixmap(QPixmap("./img/contentWidget/priv.png"))
		safe_pixmap = QPixmap ("./img/contentWidget/360")
		safe_button.setIcon(QIcon(safe_pixmap))
		safe_button.setFixedSize(safe_pixmap.size())
		tab_pixmap = QPixmap ("./img/contentWidget/tab.png")
		tab_button.setIcon(QIcon(tab_pixmap))
		tab_button.setFixedSize(tab_pixmap.size())
		pet_pixmap = QPixmap ("./img/contentWidget/pet.png")
		pet_button.setIcon(QIcon(pet_pixmap))
		pet_button.setFixedSize(tab_pixmap.size())
		lottery_pixmap = QPixmap ("./img/contentWidget/lottery.png")
		lottery_button.setIcon(QIcon(lottery_pixmap))
		lottery_button.setFixedSize(lottery_pixmap.size())
		cloud_five_pixmap = QPixmap ("./img/contentWidget/cloud_five.png")
		cloud_five_button.setIcon(QIcon(cloud_five_pixmap))
		cloud_five_button.setFixedSize(cloud_five_pixmap.size())
		caipiao_pixmap = QPixmap ("./img/contentWidget/caipiao.png")
		caipiao_button.setIcon(QIcon(caipiao_pixmap))
		caipiao_button.setFixedSize(caipiao_pixmap.size())
	
		self.register_button.setCursor(Qt.PointingHandCursor)
		safe_button.setCursor(Qt.PointingHandCursor)
		tab_button.setCursor(Qt.PointingHandCursor)
		pet_button.setCursor(Qt.PointingHandCursor)
		lottery_button.setCursor(Qt.PointingHandCursor)
		cloud_five_button.setCursor(Qt.PointingHandCursor)
		caipiao_button.setCursor(Qt.PointingHandCursor)
		
		#修复无法parses的问题：elf.register_button.setStyleSheet("color:rgb(0, 120, 230) background:transparent")
		self.register_button.setStyleSheet("color:rgb(0, 120, 230);background:transparent")
		safe_button.setStyleSheet("background:transparent")
		tab_button.setStyleSheet("background:transparent")
		pet_button.setStyleSheet("background:transparent")
		lottery_button.setStyleSheet("background:transparent")
		cloud_five_button.setStyleSheet("background:transparent")
		caipiao_button.setStyleSheet("background:transparent")
	
		login_layout = QHBoxLayout()
		login_layout.addWidget(self.login_button)
		login_layout.addStretch()
		login_layout.setContentsMargins(15, 0, 0, 0)
	
		register_layout = QHBoxLayout()
		register_layout.addStretch()
		register_layout.addWidget(priv_label)
		register_layout.addWidget(self.info_label)
		register_layout.addWidget(self.register_button)
		register_layout.addStretch()
		register_layout.setSpacing(5)
		register_layout.setContentsMargins(0, 0, 0, 0)
	
		privilege_layout = QHBoxLayout()
		privilege_layout.addStretch()
		privilege_layout.addWidget(self.privilege_label)
		privilege_layout.addWidget(safe_button)
		privilege_layout.addWidget(tab_button)
		privilege_layout.addWidget(pet_button)
		privilege_layout.addWidget(lottery_button)
		privilege_layout.addWidget(cloud_five_button)
		privilege_layout.addWidget(caipiao_button)
		privilege_layout.addStretch()
		privilege_layout.setSpacing(8)
		privilege_layout.setContentsMargins(0, 0, 0, 0)
	
		main_layout = QVBoxLayout()
		main_layout.addStretch()
		main_layout.addLayout(login_layout)
		main_layout.addLayout(register_layout)
		main_layout.addLayout(privilege_layout)
		main_layout.addStretch()
		main_layout.setSpacing(5)
		main_layout.setContentsMargins(10, 10, 10, 10)
	
		self.right_top_widget.setLayout(main_layout)


	def initRightCenter(self):

		self.right_center_widget = QWidget()
		self.fireproof_button = QToolButton()
		self.triggerman_button = QToolButton()
		self.net_shop_button = QToolButton()
		self.line_label_1 = QLabel()
		self.line_label_2 = QLabel()
		self.line_label_1.setFixedWidth(10)
		self.line_label_2.setFixedWidth(10)
		self.line_label_1.installEventFilter(self)
		self.line_label_2.installEventFilter(self)
	
		self.fireproof_button.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
		self.triggerman_button.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
		self.net_shop_button.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
	
		#设置图标
		fireproof_pixmap = QPixmap ("./img/contentWidget/fireproof.png")
		self.fireproof_button.setIcon(QIcon(fireproof_pixmap))
		self.fireproof_button.setIconSize(fireproof_pixmap.size())
		self.fireproof_button.setFixedSize(fireproof_pixmap.width() + 25, fireproof_pixmap.height() + 25)
	
		triggerman_pixmap = QPixmap ("./img/contentWidget/triggerman.png")
		self.triggerman_button.setIcon(QIcon(triggerman_pixmap))
		self.triggerman_button.setIconSize(triggerman_pixmap.size())
		self.triggerman_button.setFixedSize(triggerman_pixmap.width() + 25, triggerman_pixmap.height() + 25)
	
		net_shop_pixmap = QPixmap ("./img/contentWidget/net_shop.png")
		self.net_shop_button.setIcon(QIcon(net_shop_pixmap))
		self.net_shop_button.setIconSize(net_shop_pixmap.size())
		self.net_shop_button.setFixedSize(net_shop_pixmap.width() + 25, net_shop_pixmap.height() + 25)
	
		self.fireproof_button.setStyleSheet("background:transparent")
		self.triggerman_button.setStyleSheet("background:transparent")
		self.net_shop_button.setStyleSheet("background:transparent")
	
		h_layout = QHBoxLayout()
		h_layout.addWidget(self.fireproof_button)
		h_layout.addWidget(self.line_label_1)
		h_layout.addWidget(self.triggerman_button)
		h_layout.addWidget(self.line_label_2)
		h_layout.addWidget(self.net_shop_button)
		h_layout.setSpacing(0)
		h_layout.setContentsMargins(0, 0, 0, 0)
	
		self.right_center_widget.setLayout(h_layout)


	def initRightCenterFunction(self):

		self.right_center_function_widget = QWidget()
		self.function_label = QLabel()
		self.more_button = QPushButton()
	
		function_font = QFont()#  = self.function_label.font()
		function_font.setBold(True)
		self.function_label.setFont(function_font)
		self.function_label.setStyleSheet("color:green")
		self.more_button.setFixedSize(50, 25)
		self.more_button.setStyleSheet("QPushButton{color:rgb(0, 120, 230);background:transparent}")
		self.more_button.setCursor(Qt.PointingHandCursor)
	
		h_layout = QHBoxLayout()
		h_layout.addWidget(self.function_label)
		h_layout.addStretch()
		h_layout.addWidget(self.more_button)
		h_layout.setSpacing(0)
		h_layout.setContentsMargins(10, 5, 0, 0)
	
		self.recovery_button = QToolButton()
		self.recovery_button.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
		recovery_pixmap = QPixmap ("./img/contentWidget/recovery.png")
		self.recovery_button.setIcon(QIcon(recovery_pixmap))
		self.recovery_button.setIconSize(recovery_pixmap.size())
		self.recovery_button.setFixedSize(recovery_pixmap.width() + 50, recovery_pixmap.height() + 35)
		#修复hover样式
		self.recovery_button.setStyleSheet("QToolButton{background:transparent}"
			"QToolButton:hover{border-radius:5px;border:1px solid rgb(210, 225, 230)}")
	
		self.mobile_button = QToolButton()
		self.mobile_button.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
		mobile_pixmap = QPixmap ("./img/contentWidget/mobile.png")
		self.mobile_button.setIcon(QIcon(mobile_pixmap))
		self.mobile_button.setIconSize(mobile_pixmap.size())
		self.mobile_button.setFixedSize(mobile_pixmap.width() + 50, mobile_pixmap.height() + 35)
		self.mobile_button.setStyleSheet("QToolButton{background:transparent}"
			"QToolButton:hover{border-radius:5px;border:1px solid rgb(210, 225, 230)}")
	
		self.game_box_button = QToolButton()
		self.game_box_button.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
		game_box_pixmap = QPixmap ("./img/contentWidget/game_box.png")
		self.game_box_button.setIcon(QIcon(game_box_pixmap))
		self.game_box_button.setIconSize(game_box_pixmap.size())
		self.game_box_button.setFixedSize(game_box_pixmap.width() + 50, game_box_pixmap.height() + 35)
		self.game_box_button.setStyleSheet("QToolButton{background:transparent}"
			"QToolButton:hover{border-radius:5px;border:1px solid rgb(210, 225, 230)}")
	
		self.desktop_button = QToolButton()
		self.desktop_button.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
		desktop_pixmap = QPixmap ("./img/contentWidget/desktop.png")
		self.desktop_button.setIcon(QIcon(desktop_pixmap))
		self.desktop_button.setIconSize(desktop_pixmap.size())
		self.desktop_button.setFixedSize(desktop_pixmap.width() + 50, desktop_pixmap.height() + 35)
		self.desktop_button.setStyleSheet("QToolButton{background:transparent}"
			"QToolButton:hover{border-radius:5px;border:1px solid rgb(210, 225, 230)}")
	
		self.net_repair_button = QToolButton()
		self.net_repair_button.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
		net_repair_pixmap = QPixmap ("./img/contentWidget/net_repair.png")
		self.net_repair_button.setIcon(QIcon(net_repair_pixmap))
		self.net_repair_button.setIconSize(net_repair_pixmap.size())
		self.net_repair_button.setFixedSize(net_repair_pixmap.width() + 50, net_repair_pixmap.height() + 35)
		self.net_repair_button.setStyleSheet("QToolButton{background:transparent}"
			"QToolButton:hover{border-radius:5px;border:1px solid rgb(210, 225, 230)}")
	
		self.auto_run_button = QToolButton()
		self.auto_run_button.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
		auto_run_pixmap = QPixmap ("./img/contentWidget/auto_run.png")
		self.auto_run_button.setIcon(QIcon(auto_run_pixmap))
		self.auto_run_button.setIconSize(auto_run_pixmap.size())
		self.auto_run_button.setFixedSize(auto_run_pixmap.width() + 50, auto_run_pixmap.height() + 35)
		self.auto_run_button.setStyleSheet("QToolButton{background:transparent}"
			"QToolButton:hover{border-radius:5px;border:1px solid rgb(210, 225, 230)}")
	
		self.net_speed_button = QToolButton()
		self.net_speed_button.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
		net_speed_pixmap = QPixmap ("./img/contentWidget/net_speed.png")
		self.net_speed_button.setIcon(QIcon(net_speed_pixmap))
		self.net_speed_button.setIconSize(net_speed_pixmap.size())
		self.net_speed_button.setFixedSize(net_speed_pixmap.width() + 50, net_speed_pixmap.height() + 35)
		self.net_speed_button.setStyleSheet("QToolButton{background:transparent}"
			"QToolButton:hover{border-radius:5px;border:1px solid rgb(210, 225, 230)}")
	
		self.net_pretext_button = QToolButton()
		self.net_pretext_button.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
		net_pretext_pixmap = QPixmap ("./img/contentWidget/net_pretext.png")
		self.net_pretext_button.setIcon(QIcon(net_pretext_pixmap))
		self.net_pretext_button.setIconSize(net_pretext_pixmap.size())
		self.net_pretext_button.setFixedSize(net_pretext_pixmap.width() + 50, net_pretext_pixmap.height() + 35)
		self.net_pretext_button.setStyleSheet("QToolButton{background:transparent}"
			"QToolButton:hover{border-radius:5px;border:1px solid rgb(210, 225, 230)}")
	
		self.first_add_button = QToolButton()
		self.first_add_button.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
		first_add_pixmap = QPixmap ("./img/contentWidget/first_add.png")
		self.first_add_button.setIcon(QIcon(first_add_pixmap))
		self.first_add_button.setIconSize(first_add_pixmap.size())
		self.first_add_button.setFixedSize(first_add_pixmap.width() + 50, first_add_pixmap.height() + 35)
		self.first_add_button.setStyleSheet("QToolButton{background:transparent}"
			"QToolButton:hover{border-radius:5px;border:1px solid rgb(210, 225, 230)}")
	
		grid_layout = QGridLayout()
		grid_layout.addWidget(self.recovery_button, 0, 0)
		grid_layout.addWidget(self.mobile_button, 0, 1)
		grid_layout.addWidget(self.game_box_button, 0, 2)
		grid_layout.addWidget(self.desktop_button, 1, 0)
		grid_layout.addWidget(self.net_repair_button, 1, 1)
		grid_layout.addWidget(self.auto_run_button, 1, 2)
		grid_layout.addWidget(self.net_speed_button, 3, 0)
		grid_layout.addWidget(self.net_pretext_button, 3, 1)
		grid_layout.addWidget(self.first_add_button, 3, 2)
		grid_layout.setSpacing(0)
		grid_layout.setContentsMargins(5, 0, 5, 5)
	
		v_layout = QVBoxLayout()
		v_layout.addLayout(h_layout)
		v_layout.addLayout(grid_layout)
		v_layout.addStretch()
		v_layout.setSpacing(10)
		v_layout.setContentsMargins(0, 0, 0, 0)
	
		self.right_center_function_widget.setLayout(v_layout)


	def initRightBottom(self):

		self.right_bottom_widget = QWidget()
		icon_label = QLabel()
		self.connect_label = QLabel()
		self.version_label = QLabel()
		version_button = QPushButton()
	
		label_pixmap = QPixmap ("./img/contentWidget/cloud.png")
		icon_label.setPixmap(label_pixmap)
		icon_label.setFixedSize(label_pixmap.size())
	
		pixmap = QPixmap ("./img/contentWidget/version.png")
		version_button.setIcon(QIcon(pixmap))
		version_button.setIconSize(pixmap.size())
		version_button.setFixedSize(20, 20)
		version_button.setStyleSheet("background:transparent")
	
		bottom_layout = QHBoxLayout()
		bottom_layout.addWidget(icon_label)
		bottom_layout.addWidget(self.connect_label)
		bottom_layout.addStretch()
		bottom_layout.addWidget(self.version_label)
		bottom_layout.addWidget(version_button)
		bottom_layout.setSpacing(5)
		bottom_layout.setContentsMargins(10, 0, 10, 0)
		self.right_bottom_widget.setLayout(bottom_layout)


	def translateLanguage(self):

		self.suggest_label.setText(u"suggest")
		self.system_safe_label.setText(u"system safe")
		self.power_button.setText(u"power")
	
		self.login_button.setText(u"login home")
		self.info_label.setText(u"show beautifull icon")
		self.register_button.setText(u"register")
		self.privilege_label.setText(u"privilege power")
	
		self.fireproof_button.setText(u"fireproof")
		self.triggerman_button.setText(u"triggerman")
		self.net_shop_button.setText(u"net shop")
	
		self.function_label.setText(u"function")
		self.more_button.setText(u"more")
		self.recovery_button.setText(u"recovery")
		self.mobile_button.setText(u"mobile")
		self.game_box_button.setText(u"game box")
		self.desktop_button.setText(u"desktop")
		self.net_repair_button.setText(u"net repair")
		self.auto_run_button.setText(u"auto run")
		self.net_speed_button.setText(u"net speed")
		self.net_pretext_button.setText(u"net pretext")
		self.first_add_button.setText(u"first add")
	
		self.connect_label.setText(u"connect success")
		self.version_label.setText(u"version")


	def eventFilter(self, obj, event):
		if(obj is QLabel):
		
			if(event.type() == QEvent.Paint):
				label_height_1 = self.line_label_1.height()
				label_width_1 = self.line_label_1.width()
				painter = QPainter (self.line_label_1)
				painter.setPen(QPen(QColor(220, 220, 220), 1, Qt.DashLine))
				painter.drawLine(label_width_1 / 2, 0, label_width_1 / 2, label_height_1)
	
				label_height_2 = self.line_label_2.height()
				label_width_2 = self.line_label_2.width()
				painter2 = QPainter (self.line_label_2)
				painter2.setPen(QPen(QColor(220, 220, 220), 1, Qt.DashLine))
				painter2.drawLine(label_width_2 / 2, 0, label_width_2 / 2, label_height_2)
				return True
			
		return False#self.eventFilter(obj, event)
	
if __name__ == '__main__':
	import sys
	app = QApplication(sys.argv)
	content = ContentWidget()
	content.show()
	sys.exit(app.exec_())


