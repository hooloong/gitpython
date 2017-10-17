#!/usr/bin/python  
#-*-coding:utf-8-*-

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.Qt import *
from push_button import PushButton

class SettingDialog(QDialog):
	def __init__(self, parent = None):
		super(SettingDialog,self).__init__()
		self.resize(560, 400)
		self.setWindowFlags(Qt.FramelessWindowHint | Qt.Dialog)
		self.initTitle()
		self.initCenter()
		self.initTab1()
		self.initTab2()
		self.initTab3()
		self.initTab4()
		self.initTab5()
		self.initTab6()
		self.initBottom()
		
		main_layout =  QVBoxLayout()
		
		main_layout.addLayout(self.title_layout)
		main_layout.addWidget(self.tab_widget)
		main_layout.addLayout(self.bottom_layout)
		main_layout.addStretch()
		main_layout.setSpacing(0)
		main_layout.setContentsMargins(0, 0, 0, 0)

		self.setLayout(main_layout)
		self.mouse_press = False
		self.translateLanguage()
		
	
	def initTitle(self):

		self.title_label =  QLabel()
		self.title_icon_label =  QLabel()
		self.close_button =  PushButton()
		self.close_button.loadPixmap("./img/sysButton/close.png")

		self.title_label.setStyleSheet("color:white")
		pixmap = QPixmap ("./img/safe")
		self.title_icon_label.setPixmap(pixmap)
		self.title_icon_label.setFixedSize(16, 16)
		self.title_icon_label.setScaledContents(True)
	
		self.title_layout =  QHBoxLayout()
		self.title_layout.addWidget(self.title_icon_label, 0, Qt.AlignVCenter)
		self.title_layout.addWidget(self.title_label, 0, Qt.AlignVCenter)
		self.title_layout.addStretch()
		self.title_layout.addWidget(self.close_button, 0, Qt.AlignTop)
		self.title_layout.setSpacing(5)
		self.title_layout.setContentsMargins(10, 0, 5, 10)

		self.connect(self.close_button, SIGNAL("clicked()"), self, SLOT("close()"))


	def initTab1(self):

		self.tab1_group_box =  QGroupBox()
		self.auto_rise_button =  QRadioButton()
		self.not_auto_rise_button =  QRadioButton()
		self.rise_mummy_check_box =  QCheckBox()
		self.game_check_box =  QCheckBox()
		self.g3_check_box =  QCheckBox()
		self.p2p_check_box =  QCheckBox()
		self.mummy_check_box =  QCheckBox()

		self.tab1_group_box.setStyleSheet("QGroupBox.title{color:green}")
		group_box_font = QFont()
		#self.tab1_group_box.setFont()
		group_box_font.setBold(True)
		self.tab1_group_box.setFont(group_box_font)
		self.tab1_group_box.setFixedSize(480, 250)
	
		rise_mummy_layout =  QHBoxLayout()
		rise_mummy_layout.addWidget(self.rise_mummy_check_box)
		rise_mummy_layout.setSpacing(0)
		rise_mummy_layout.setContentsMargins(20, 0, 0, 0)

		group_layout =  QVBoxLayout()
		group_layout.addWidget(self.auto_rise_button)
		group_layout.addWidget(self.not_auto_rise_button)
		group_layout.addLayout(rise_mummy_layout)
		group_layout.addWidget(self.game_check_box)
		group_layout.addWidget(self.g3_check_box)
		group_layout.addWidget(self.p2p_check_box)
		group_layout.addWidget(self.mummy_check_box)
		group_layout.setSpacing(0)
		group_layout.setContentsMargins(30, 0, 0, 0)
		self.tab1_group_box.setLayout(group_layout)

		tab1_layout =  QHBoxLayout()
		tab1_layout.addWidget(self.tab1_group_box)
		tab1_layout.setSpacing(0)
		tab1_layout.setContentsMargins(0, 0, 0, 0)
		self.tab1.setLayout(tab1_layout)


	def initTab2(self):

		self.tab2_group_box1 =  QGroupBox()
		self.tab2_group_box2 =  QGroupBox()
		self.tab2_group_box3 =  QGroupBox()
		self.auto_start_check_box =  QCheckBox()
		self.remove_own_check_box =  QCheckBox()
		self.strong_remove_check_box =  QCheckBox()
		self.mummy_kill_check_box =  QCheckBox()
		self.display_count_check_box =  QCheckBox()
	
		self.tab2_group_box1.setStyleSheet("QGroupBox.title{color:green}")
		self.tab2_group_box2.setStyleSheet("QGroupBox.title{color:green}")
		self.tab2_group_box3.setStyleSheet("QGroupBox.title{color:green}")
		group_box_font = QFont() #  = self.tab2_group_box1.font()
		group_box_font.setBold(True)
		self.tab2_group_box1.setFont(group_box_font)
		self.tab2_group_box2.setFont(group_box_font)
		self.tab2_group_box3.setFont(group_box_font)
	
		group_box1_layout =  QHBoxLayout()
		group_box1_layout.addWidget(self.auto_start_check_box)
		group_box1_layout.setSpacing(0)
		group_box1_layout.setContentsMargins(30, 0, 0, 0)
		self.tab2_group_box1.setLayout(group_box1_layout)
	
		group_box2_layout =  QVBoxLayout()
		group_box2_layout.addWidget(self.remove_own_check_box)
		group_box2_layout.addWidget(self.strong_remove_check_box)
		group_box2_layout.addWidget(self.mummy_kill_check_box)
		group_box2_layout.setSpacing(0)
		group_box2_layout.setContentsMargins(30, 0, 0, 0)
		self.tab2_group_box2.setLayout(group_box2_layout)
	
		group_box3_layout =  QHBoxLayout()
		group_box3_layout.addWidget(self.display_count_check_box)
		group_box3_layout.setSpacing(0)
		group_box3_layout.setContentsMargins(30, 0, 0, 0)
		self.tab2_group_box3.setLayout(group_box3_layout)
	
		self.tab2_group_box1.setFixedSize(480, 60)
		self.tab2_group_box2.setFixedSize(480, 110)
		self.tab2_group_box3.setFixedSize(480, 60)
	
		group_layout =  QVBoxLayout()
		group_layout.addWidget(self.tab2_group_box1, 0, Qt.AlignCenter)
		group_layout.addWidget(self.tab2_group_box2, 0, Qt.AlignCenter)
		group_layout.addWidget(self.tab2_group_box3, 0, Qt.AlignCenter)
		group_layout.addStretch()
		group_layout.setSpacing(10)
		group_layout.setContentsMargins(0, 20, 0, 0)
		self.tab2.setLayout(group_layout)


	def initTab3(self):

		self.tab3_group_box1 =  QGroupBox()
		self.tab3_group_box2 =  QGroupBox()
		self.auto_check_button =  QRadioButton()
		self.first_check_button =  QRadioButton()
		self.hand_check_button =  QRadioButton()
		self.select_quit_button =  QRadioButton()
		self.backstage_mode_button =  QRadioButton()
		self.immediacy_close_button =  QRadioButton()
	
		self.tab3_group_box1.setStyleSheet("QGroupBox.title{color:green}")
		self.tab3_group_box2.setStyleSheet("QGroupBox.title{color:green}")
		group_box_font = QFont()#  = self.tab3_group_box1.font()
		group_box_font.setBold(True)
		self.tab3_group_box1.setFont(group_box_font)
		self.tab3_group_box2.setFont(group_box_font)
	
		group_box1_layout =  QVBoxLayout()
		group_box1_layout.addWidget(self.auto_check_button)
		group_box1_layout.addWidget(self.first_check_button)
		group_box1_layout.addWidget(self.hand_check_button)
		group_box1_layout.setSpacing(0)
		group_box1_layout.setContentsMargins(30, 0, 0, 0)
		self.tab3_group_box1.setLayout(group_box1_layout)
	
		group_box2_layout =  QVBoxLayout()
		group_box2_layout.addWidget(self.select_quit_button)
		group_box2_layout.addWidget(self.backstage_mode_button)
		group_box2_layout.addWidget(self.immediacy_close_button)
		group_box2_layout.setSpacing(0)
		group_box2_layout.setContentsMargins(30, 0, 0, 0)
		self.tab3_group_box2.setLayout(group_box2_layout)
	
		self.tab3_group_box1.setFixedSize(480, 120)
		self.tab3_group_box2.setFixedSize(480, 120)
	
		group_layout =  QVBoxLayout()
		group_layout.addWidget(self.tab3_group_box1, 0, Qt.AlignCenter)
		group_layout.addWidget(self.tab3_group_box2, 0, Qt.AlignCenter)
		group_layout.addStretch()
		group_layout.setSpacing(10)
		group_layout.setContentsMargins(0, 20, 0, 0)
		self.tab3.setLayout(group_layout)


	def initTab4(self):

		self.tab4_group_box =  QGroupBox()
		self.diaplay_experience_check_box =  QCheckBox()
		self.diaplay_experience_check_box =  QCheckBox()
		self.tray_quit_check_box =  QCheckBox()
		self._character_check_box =  QCheckBox()
		self.rise_remind_check_box =  QCheckBox()
	
		self.tab4_group_box.setStyleSheet("QGroupBox.title{color:green}")
		group_box_font = QFont()#  = self.tab4_group_box.font()
		group_box_font.setBold(True)
		self.tab4_group_box.setFont(group_box_font)
		self.tab4_group_box.setFixedSize(480, 180)
	
		group_layout =  QVBoxLayout()
		group_layout.addWidget(self.diaplay_experience_check_box)
		group_layout.addWidget(self.diaplay_experience_check_box)
		group_layout.addWidget(self.tray_quit_check_box)
		group_layout.addWidget(self._character_check_box)
		group_layout.addWidget(self.rise_remind_check_box)
		group_layout.setSpacing(0)
		group_layout.setContentsMargins(30, 0, 0, 0)
		self.tab4_group_box.setLayout(group_layout)
	
		tab4_layout =  QVBoxLayout()
		tab4_layout.addWidget(self.tab4_group_box, 0 , Qt.AlignCenter)
		tab4_layout.addStretch()
		tab4_layout.setSpacing(0)
		tab4_layout.setContentsMargins(0, 20, 0, 0)
		self.tab4.setLayout(tab4_layout)


	def initTab5(self):

		self.tab5_group_box =  QGroupBox()
		self.improve_plan_check_box =  QCheckBox()
		self.understand_detail_button =  QPushButton()
	
		self.tab5_group_box.setStyleSheet("QGroupBox.title{color:green}")
		group_box_font = QFont()  #= self.tab5_group_box.font()
		group_box_font.setBold(True)
		self.tab5_group_box.setFont(group_box_font)
	
		self.tab5_group_box.setFixedSize(480, 60)
		self.understand_detail_button.setFixedSize(180, 25)
		self.understand_detail_button.setCursor(Qt.PointingHandCursor)
		#解决无法parse
		self.understand_detail_button.setStyleSheet("color:rgb(0, 120, 230);background:transparent")
	
		group_layout =  QHBoxLayout()
		group_layout.addWidget(self.improve_plan_check_box)
		group_layout.addStretch()
		group_layout.addWidget(self.understand_detail_button)
		group_layout.setSpacing(0)
		group_layout.setContentsMargins(30, 0, 30, 0)
		self.tab5_group_box.setLayout(group_layout)
	
		tab5_layout =  QVBoxLayout()
		tab5_layout.addWidget(self.tab5_group_box, 0 , Qt.AlignCenter)
		tab5_layout.addStretch()
		tab5_layout.setSpacing(0)
		tab5_layout.setContentsMargins(0, 20, 0, 0)
		self.tab5.setLayout(tab5_layout)


	def initTab6(self):

		self.tab6_group_box1 =  QGroupBox()
		self.tab6_group_box2 =  QGroupBox()
		self.file_safe_label =  QLabel()
		self.internet_safe_label =  QLabel()
		self.file_safe_check_box =  QCheckBox()
		self.internet_safe_check_box =  QCheckBox()
		self.look_privacy_button =  QPushButton()
	
		self.tab6_group_box1.setStyleSheet("QGroupBox.title{color:green}")
		self.tab6_group_box2.setStyleSheet("QGroupBox.title{color:green}")
		group_box_font = QFont()  #= self.tab6_group_box1.font()
		group_box_font.setBold(True)
		self.tab6_group_box1.setFont(group_box_font)
		self.tab6_group_box2.setFont(group_box_font)
		self.look_privacy_button.setCursor(Qt.PointingHandCursor)
	
		#解决无法parse
		self.look_privacy_button.setStyleSheet("color:rgb(0, 120, 230);background:transparent")
		self.file_safe_label.setStyleSheet("color:gray")
		self.internet_safe_label.setStyleSheet("color:gray")
		self.file_safe_label.setFixedWidth(420)
		self.file_safe_label.resize(420, 25*3)
		self.file_safe_label.setWordWrap(True)
		self.internet_safe_label.setFixedWidth(420)
		self.internet_safe_label.resize(420, 25*3)
		self.internet_safe_label.setWordWrap(True)
	
		group_box1_h_layout =  QHBoxLayout()
		group_box1_h_layout.addWidget(self.file_safe_check_box)
		group_box1_h_layout.addStretch()
		group_box1_h_layout.addWidget(self.look_privacy_button)
		group_box1_h_layout.setSpacing(0)
		group_box1_h_layout.setContentsMargins(0, 0, 30, 0)
	
		group_box1_layout =  QVBoxLayout()
		group_box1_layout.addWidget(self.file_safe_label)
		group_box1_layout.addLayout(group_box1_h_layout)
		group_box1_layout.setSpacing(0)
		group_box1_layout.setContentsMargins(30, 0, 0, 10)
		self.tab6_group_box1.setLayout(group_box1_layout)
	
		group_box2_layout =  QVBoxLayout()
		group_box2_layout.addWidget(self.internet_safe_label)
		group_box2_layout.addWidget(self.internet_safe_check_box)
		group_box2_layout.setSpacing(0)
		group_box2_layout.setContentsMargins(30, 0, 0, 10)
		self.tab6_group_box2.setLayout(group_box2_layout)
	
		self.tab6_group_box1.setFixedSize(480, 120)
		self.tab6_group_box2.setFixedSize(480, 120)
	
		group_layout =  QVBoxLayout()
		group_layout.addWidget(self.tab6_group_box1, 0, Qt.AlignCenter)
		group_layout.addWidget(self.tab6_group_box2, 0, Qt.AlignCenter)
		group_layout.addStretch()
		group_layout.setSpacing(10)
		group_layout.setContentsMargins(0, 20, 0, 0)
		self.tab6.setLayout(group_layout)


	def initCenter(self):

		self.tab_widget =  QTabWidget()
		self.tab_widget.setFixedSize(self.width(), 320)
		self.tab1 =  QWidget()
		self.tab2 =  QWidget()
		self.tab3 =  QWidget()
		self.tab4 =  QWidget()
		self.tab5 =  QWidget()
		self.tab6 =  QWidget()
	
		#修复样式问题 原来为QTabBar.tab，应该为QTabBar::tab
		self.tab_widget.setStyleSheet("QTabWidget::pane{border: 10px}"
			"QTabWidget::tab-bar{alignment:center}"
			"QTabBar::tab{background:transparent; color:white; min-width:30ex; min-height:10ex}"
			"QTabBar::tab:hover{background:rgb(255, 255, 255, 100)}"
			"QTabBar::tab:selected{border-color:white;background:white;color:green}")


	def initBottom(self):

		self.ok_button =  QPushButton()
		self.cancel_button =  QPushButton()
	
		self.ok_button.setFixedSize(75, 25)
		self.cancel_button.setFixedSize(75, 25)
		self.ok_button.setStyleSheet("QPushButton{border:1px solid lightgray;background:rgb(230,230,230)}"
			"QPushButton:hover{border-color:green;background:transparent}")
		self.cancel_button.setStyleSheet("QPushButton{border:1px solid lightgray;background:rgb(230,230,230)}"
			"QPushButton:hover{border-color:green;background:transparent}")
	
		self.bottom_layout =  QHBoxLayout()
		self.bottom_layout.addStretch()
		self.bottom_layout.addWidget(self.ok_button)
		self.bottom_layout.addWidget(self.cancel_button)
		self.bottom_layout.setSpacing(20)
		self.bottom_layout.setContentsMargins(0, 10, 20, 0)
	
		self.connect(self.cancel_button, SIGNAL("clicked()"), self, SLOT("hide()"))


	def translateLanguage(self):

		space_str = QString("    ") #QString
		self.title_label.setText(u"360 safe setting")
		self.close_button.setToolTip(u"close")
	
		self.tab_widget.addTab(self.tab1, u"rise style")
		self.tab_widget.addTab(self.tab2, u"advanced setting")
		self.tab_widget.addTab(self.tab3, u"physical setting")
		self.tab_widget.addTab(self.tab4, u"user setting")
		self.tab_widget.addTab(self.tab5, u"improve program")
		self.tab_widget.addTab(self.tab6, u"cloud secure program")
	
		self.tab1_group_box.setTitle(u"rise style title")
		self.auto_rise_button.setText(u"auto rise")
		self.not_auto_rise_button.setText(u"not auto rise")
		self.rise_mummy_check_box.setText(u"rise mummy")
		self.game_check_box.setText(u"game")
		self.g3_check_box.setText(u"3g")
		self.p2p_check_box.setText(u"p2p")
		self.mummy_check_box.setText(u"mummy")
	
		self.tab2_group_box1.setTitle(u"mummy fireproof")
		self.tab2_group_box2.setTitle(u"context menu")
		self.tab2_group_box3.setTitle(u"software manager")
		self.auto_start_check_box.setText(u"auto start")
		self.remove_own_check_box.setText(u"remove own")
		self.strong_remove_check_box.setText(u"strong remove")
		self.mummy_kill_check_box.setText(u"mummy kill")
		self.display_count_check_box.setText(u"display count")
	
		self.tab3_group_box1.setTitle(u"frequency setting")
		self.tab3_group_box2.setTitle(u"quit style setting")
		self.auto_check_button.setText(u"auto check")
		self.first_check_button.setText(u"first check")
		self.hand_check_button.setText(u"hand check")
		self.select_quit_button.setText(u"select quit")
		self.backstage_mode_button.setText(u"backstage mode")
		self.immediacy_close_button.setText(u"immediacy close")
	
		self.tab4_group_box.setTitle(u"rate task setting")
		self.diaplay_experience_check_box.setText(u"diaplay experience")
		self.diaplay_experience_check_box.setText(u"diaplay login")
		self.tray_quit_check_box.setText(u"tray quit")
		self._character_check_box.setText(u" character")
		self.rise_remind_check_box.setText(u"rise remind")
	
		self.tab5_group_box.setTitle(u"improve plan")
		self.improve_plan_check_box.setText(u"join improve plan")
		self.understand_detail_button.setText(u"understand detail")
	
		self.tab6_group_box1.setTitle(u"file safe plan")
		self.tab6_group_box2.setTitle(u"internet safe plan")
		self.file_safe_label.setText(space_str + u"file safe info")
		self.internet_safe_label.setText(space_str + u"internet safe info")
		self.file_safe_check_box.setText(u"file safe")
		self.internet_safe_check_box.setText(u"internet safe")
		self.look_privacy_button.setText(u"look privacy")
	
		self.ok_button.setText(u"ok")
		self.cancel_button.setText(u"cancel")


	def paintEvent(self ,event):

		skin_name = QString() 
		#bool is_read = Util.readInit(QString("./user.ini"), QString("skin"), skin_name)
		#if(is_read)
		
			#if(skin_name.isEmpty())
			
				#skin_name = QString(":/skin/17_big")
			#
		
		#else
		
			#skin_name = QString(":/skin/17_big")
		
	
		painter = QPainter ()
		painter.begin(self)
		painter.drawPixmap(self.rect(), QPixmap("./img/skin/17_big.jpg"))
		painter.end()
	
		painter2 = QPainter ()
		painter2.begin(self)
		linear2 = QLinearGradient(self.rect().topLeft(), self.rect().bottomLeft())
		linear2.start()
		linear2.setColorAt(0, Qt.white)
		linear2.setColorAt(0.5, Qt.white)
		linear2.setColorAt(1, Qt.white)
		linear2.finalStop()
		painter2.setPen(Qt.white)  #设定画笔颜色，到时侯就是边框颜色
		painter2.setBrush(linear2)
		painter2.drawRect(QRect(0, 60, self.width(), self.height()-60))
		painter2.end()
	
		painter3 = QPainter()
		painter3.begin(self)
		painter3.setPen(Qt.gray)
		#static const QPointF points[4] = {}
		painter3.drawPolyline(QPointF(0, 60), QPointF(0, self.height()-1), QPointF(self.width()-1, self.height()-1), QPointF(self.width()-1, 60))
		painter3.end()


	def mousePressEvent(self,event):
		if event.button() == Qt.LeftButton:
			self.dragPosition = event.globalPos() - self.frameGeometry().topLeft()
			event.accept()

	def mouseMoveEvent(self,event):
		if event.buttons() == Qt.LeftButton:
			self.move(event.globalPos() - self.dragPosition)
			event.accept()
			
if __name__ == '__main__':
	
	import sys
	app = QApplication(sys.argv)
	setting = SettingDialog()
	setting.show()
	sys.exit(app.exec_())	
		




