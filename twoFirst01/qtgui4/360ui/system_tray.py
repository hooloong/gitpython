#!/usr/bin/python  
#-*-coding:utf-8-*-

#include <QtGui>
from PyQt4.QtGui import *
from PyQt4.QtCore import *

class SystemTray(QSystemTrayIcon):
	def __init__(self, parent=None):
		super(SystemTray, self).__init__()
		self.tray_menu = QMenu() #托盘菜单
		self.parent = parent 
		#self.action_open = QAction(self) #打开360安全卫士
		#self.action_help_center = QAction(self) #求助中心
		#self.action_kill_mummy = QAction(self) #查杀木马
		#self.action_clear = QAction(self) #清理垃圾
		#self.action_optimize = QAction(self) #一键优化
		#self.action_fireproof = QAction(self) #检查更新
		#self.action_show_speed = QAction(self) #显示加速球
		#self.action_soft_manage = QAction(self) #软件管家
		#self.action_safe_notice = QAction(self) #安全通知
		#self.action_rise = QAction(self) #升级
		#self.action_login = QAction(self) #360用户登录
		#self.action_separate = QAction(self) #隔离沙箱
		#self.action_logout = QAction(self) #退出

		self.createAction()
		self.translateLanguage()
		#quitAction = QtGui.QAction()
		#self.connect(quitAction,signal("triggered()"),QtGui.qApp.quit)


	def createAction(self):
		self.setIcon(QIcon("./img/safe.png"))

		self.tray_menu = QMenu()
		self.action_open = QAction(QIcon('./img/mainMenu/open.png'), '&Quit', self)
		self.action_help_center = QAction(QIcon('./img/mainMenu/help.png'), '&Quit', self)
		self.action_kill_mummy = QAction(QIcon('./img/mainMenu/quit.png'), '&Quit', self)
		self.action_clear = QAction(QIcon('./img/mainMenu/quit.png'), '&Quit', self)
		self.action_optimize = QAction(QIcon('./img/mainMenu/quit.png'), '&Quit', self)
		self.action_fireproof = QAction(QIcon('./img/mainMenu/quit.png'), '&Quit', self)
		self.action_show_speed = QAction(QIcon('./img/mainMenu/quit.png'), '&Quit', self)
		self.action_soft_manage = QAction(QIcon('./img/mainMenu/update.png'), '&Quit', self)
		self.action_safe_notice = QAction(QIcon('./img/mainMenu/quit.png'), '&Quit', self)
		self.action_rise = QAction(QIcon('./img/mainMenu/quit.png'), '&Quit', self)
		self.action_login = QAction(QIcon('./img/mainMenu/quit.png'), '&Quit', self)
		self.action_separate = QAction(QIcon('./img/mainMenu/quit.png'), '&Quit', self)
		self.action_logout = QAction(QIcon('./img/mainMenu/quit.png'), '&Quit', self)

		#添加菜单项
		self.tray_menu.addAction(self.action_open)
		self.tray_menu.addAction(self.action_help_center)
		self.tray_menu.addSeparator()
		self.tray_menu.addAction(self.action_kill_mummy)
		self.tray_menu.addAction(self.action_clear)
		self.tray_menu.addSeparator()
		self.tray_menu.addAction(self.action_optimize)
		self.tray_menu.addAction(self.action_fireproof)
		self.tray_menu.addAction(self.action_show_speed)
		self.tray_menu.addAction(self.action_soft_manage)
		self.tray_menu.addSeparator()
		self.tray_menu.addAction(self.action_safe_notice)
		self.tray_menu.addAction(self.action_rise)
		self.tray_menu.addAction(self.action_login)
		self.tray_menu.addAction(self.action_separate)
		self.tray_menu.addAction(self.action_logout)

		#设置信号连接
		'''QObject.connect(action_show, SIGNAL(triggered(bool)), self, SIGNAL(showWidget()))
		QObject.connect(action_quit, SIGNAL(triggered(bool)), self, SIGNAL(logoutWidget()))
		QObject.connect(action_setting, SIGNAL(triggered(bool)), self, SIGNAL(setUp()))
		QObject.connect(action_about, SIGNAL(triggered(bool)), self, SIGNAL(aboutUs()))
		QObject.connect(action_login_home, SIGNAL(triggered(bool)), MenuAction.getInstance(), SLOT(openLoginHome()))
		QObject.connect(action_help, SIGNAL(triggered(bool)), MenuAction.getInstance(), SLOT(openHelpMe()))
		QObject.connect(action_check_update, SIGNAL(triggered(bool)), MenuAction.getInstance(), SLOT(openCheckUpdate()))'''

		#修复意外关闭
		#如果有parent，则抛出，否则自己关闭
		if self.parent:
			self.connect(self.action_logout, SIGNAL("triggered()"), self.parent, SLOT('showClose()'))
		else:
			self.connect(self.action_logout, SIGNAL("triggered()"), self, SLOT('quit()'))
		self.setContextMenu(self.tray_menu)

	@pyqtSlot()
	def quit(self):
		self.hide()
		exit()

	def translateLanguage(self):

		#放在托盘图标上时候显示
		self.setToolTip(u"360 safe")

		self.action_open.setText(u"open")
		self.action_help_center.setText(u"help center")
		self.action_kill_mummy.setText(u"kill mummy")
		self.action_clear.setText(u"clear")
		self.action_optimize.setText(u"optimize")
		self.action_fireproof.setText(u"fireproof")
		self.action_show_speed.setText(u"show speed")
		self.action_soft_manage.setText(u"soft manage")
		self.action_safe_notice.setText(u"safe notice")
		self.action_rise.setText(u"rise")
		self.action_login.setText(u"login")
		self.action_separate.setText(u"separate")
		self.action_logout.setText(u"logout")

if __name__ == '__main__':
	import sys
	app = QApplication(sys.argv)
	tray = SystemTray()
	tray.show()
	app.exec_()

