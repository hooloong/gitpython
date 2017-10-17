#!/usr/bin/python  
#-*-coding:utf-8-*-

from title_widget import *
from content_widget import *
from system_tray import *
from about_us import *
from main_menu import *
from character_widget import *
from setting_dialog import *
from  skin_widget import *
import util

from PyQt4.QtGui import *
from PyQt4.QtCore import *
from PyQt4.Qt import *

#来自于http://download.csdn.net/detail/zhuyeqing_432/6045601
#代码很多功能不能用，需要重新调整，包括：
#1 最大化和还原【已修复】
#2 退出时出现异常【已修复，不会出现异常】
#3 无法拖动【已修复，通过在title_widget中的press方法】
#4 有多处stylesheet无法parse，在content_widget.py、change_skin_widget.py，需要增加分号
#5 按钮样式和tab样式还是未如意【已修复，是stylesheet中写错了】
#6 优化拖动效果，对于MainWidget和Aboutus窗口，其他窗口自行实现了mousePressEvent和mouseMoveEvent则是不停重绘的方法
#参考 以下文档QT 无边框拖动
#http://support.microsoft.com/kb/320687
#http://blog.csdn.net/kfbyj/article/details/9284923
#http://www.cppblog.com/biao/archive/2013/07/11/201704.aspx
#http://www.cnblogs.com/qpl007/articles/442577.html
#http://blog.csdn.net/vagrxie/article/details/5252302
#	http://blog.csdn.net/harvic880925/article/details/9785439
class MainWidget(QWidget):
	closeWidget = pyqtSignal()
	
	def __init__(self, parent=None):
		super(MainWidget, self).__init__()
		self.location = QRect()
		self.title_widget = TitleWidget(self) #
		self.title_widget.setFixedHeight(100)
		self.content_widget = ContentWidget(self) #
		
		self.system_tray = SystemTray(self) #
		self.setting_dialog = SettingDialog(self) #
		self.character_widget = CharacterWidget(self) #
		self.about_us_dialog = AboutUsDialog(self) #
		self.skin_name = QString("./img/skin/17_big.png") #
		self.main_menu = MainMenu() #
		self.skin_widget = SkinWidget() #
		self.setMinimumSize(900, 600) #
		
		self.setWindowIcon(QIcon("./img/safe.ico"))#
#		self.setWindowFlags(Qt.FramelessWindowHint)#
		self.setWindowFlags(Qt.MSWindowsFixedSizeDialogHint | Qt.FramelessWindowHint)#
		self.location = self.geometry() #
		self.closeWidget.connect(self.close)
		
		self.is_max = False
		#self.is_read = Util.readInit(QString("./user.ini"), QString("skin"), skin_name)

		#if(self.is_read):
		#if(skin_name.isEmpty()):
		#skin_name = QString(":/skin/17_big")
		#else:
		#skin_name = QString(":/skin/17_big")

		self.center_layout = QVBoxLayout()
		self.center_layout.addWidget(self.content_widget)
		self.center_layout.setSpacing(0)
		self.center_layout.setContentsMargins(1, 0, 1, 1)

		main_layout = QVBoxLayout()
		main_layout.addWidget(self.title_widget)
		main_layout.addLayout(self.center_layout)
		main_layout.setSpacing(0)
		main_layout.setContentsMargins(0, 0, 0, 0)

		self.setLayout(main_layout)

		self.connect(self.title_widget, SIGNAL("showSkin()"), self, SLOT("showSkinWidget()"))
		self.connect(self.title_widget, SIGNAL("showMainMenu()"), self, SLOT("showMainMenu()"))
		self.connect(self.title_widget, SIGNAL("showMax()"), self, SLOT("showMax()"))
		self.connect(self.title_widget, SIGNAL("showMin()"), self, SLOT("showMinimized()"))
		self.connect(self.title_widget, SIGNAL("showClose()"), self, SLOT("showClose()")) #hide()

		self.connect(self.main_menu, SIGNAL("showSettingDialog()"), self, SLOT("showSettingDialog()"))
		self.connect(self.main_menu, SIGNAL("showCharacter()"), self, SLOT("showCharacter()"))
		self.connect(self.main_menu, SIGNAL("showAboutUs()"), self, SLOT("showAboutUs()"))

		self.connect(self.skin_widget, SIGNAL("changeSkin()"), self, SLOT("changeSkin()"))
		self.connect(self.system_tray, SIGNAL("activated()"), self, SLOT("iconIsActived()"))
		self.connect(self.system_tray, SIGNAL("showClose()"), self, SLOT("showClose()"))

		self.system_tray.show()
		
		self.pixmap = QPixmap() 
		self.pixmap.load(self.skin_name)
		
#		self.pixmap.load('f:/17_big.jpg')

	#修复关闭时候的异常
	@pyqtSlot()
	def showClose(self):
		self.close()

	def paintEvent(self, event):# QPaintEvent *
		
		painter = QPainter(self)
		painter.drawPixmap(self.rect(), self.pixmap)
		painter.end()
		
		painter2 = QPainter (self)
		painter2.setPen(Qt.gray)
		painter2.drawPolyline(QPointF(0, 100), QPointF(0, self.height() - 1), QPointF(self.width() - 1, self.height() - 1), QPointF(self.width() - 1, 100))
		painter2.end()
	
	@pyqtSlot()	
	def showMax(self):
		#修复有问题的最大化
		if not self.isMaximized():
			self.showMaximized()
		else:
			self.showNormal()
	
	@pyqtSlot()	
	def showSkinWidget(self):
		self.skin_widget.show()
	
	@pyqtSlot()	
	def showMainMenu(self):
		p = self.rect().topRight() #QPoint
		p.setX(p.x() - 150)
		p.setY(p.y() + 22)
		self.main_menu.exec_(self.mapToGlobal(p))
	
	@pyqtSlot()	
	def iconIsActived(self, reason): #QSystemTrayIcon.ActivationReason 

		if reason == QSystemTrayIcon.Trigger:
			self.showWidget()
		elif reason == QSystemTrayIcon.DoubleClick:
			self.showWidget()
	
	@pyqtSlot()
	def showWidget(self):
		self.showNormal()
		self.raise_()
		self.activateWindow()
#		self.title_widget.turnPage(0)
	
	@pyqtSlot()	
	def showAboutUs(self):
		self.about_us_dialog.exec_()
	
	@pyqtSlot()	
	def showCharacter(self):
		self.character_widget.show()
	
	@pyqtSlot()	
	def showSettingDialog(self):
		self.setting_dialog.exec_()
	
	@pyqtSlot()	
	def changeSkin(self, skin_name): #QString 
		#Util.writeInit(QString("./user.ini"), QString("skin"), skin_name)
		self.skin_name = skin_name
		self.update()

	def isInTitle(self, xPos, yPos):
		return yPos < 30 and xPos < 695

class MyApplication(QApplication):
	
	def __init__(self, args):
		super(MyApplication, self).__init__(args)
	
	def GET_X_LPARAM(self, param):
		#define LOWORD(l)           ((WORD)((DWORD_PTR)(l) & 0xffff))
		#define HIWORD(l)           ((WORD)((DWORD_PTR)(l) >> 16))
		#define GET_X_LPARAM(lp)                        ((int)(short)LOWORD(lp))
		#define GET_Y_LPARAM(lp)                        ((int)(short)HIWORD(lp))
		return param & 0xffff

	def GET_Y_LPARAM(self, param):
		return param >> 16
	
	def winEventFilter(self, msg):
		if msg.message == 0x84: #WM_NCHITTEST 
			form = self.activeWindow()
			if form:
				xPos = self.GET_X_LPARAM(msg.lParam) - form.frameGeometry().x()
				yPos = self.GET_Y_LPARAM(msg.lParam) - form.frameGeometry().y()
#				鼠标在窗体自定义标题范围内，窗体自定义一个isInTitle的方法判断 
#				if yPos < 30 and xPos < 456:
				if not form.isMaximized() and hasattr(form, 'isInTitle') and form.isInTitle(xPos, yPos):
					return True, 0x2 #HTCAPTION
			
		return False, 0

if __name__ == "__main__":

	import sys
	app = MyApplication(sys.argv)

	translator = QTranslator(app)
	translator.load(QString("qt_zh_CN.qm"))
	app.installTranslator(translator)
	
	translator_zh = QTranslator(app)
	translator_zh.load(QString("360safe_zh.qm"))
	app.installTranslator(translator_zh)
	app.setFont(QFont("Arial", 9))

	main_widget = MainWidget ()
	main_widget.showWidget()
	sys.exit(app.exec_())



