#!/usr/bin/python  
#-*-coding:utf-8-*-

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.Qt import *

class Util():
	def __init__(self,parent = None):
		pass
		
	def writeInit(self,path, user_key,user_value):
		if(path.isEmpty() | user_key.isEmpty()):
			return False
		else:
			#创建配置文件操作对象
			self.config =  QSettings(path, QSettings.IniFormat)

			#将信息写入配置文件
			self.config.beginGroup("config")
			self.config.setValue(user_key, user_value)
			self.config.endGroup()
			return True
			
	def readInit(self,path, user_key, user_value):
		user_value = ""
		if(path.isEmpty() | user_key.isEmpty()):
			return False
		else:
		#创建配置文件操作对象
			self.config =  QSettings(path, QSettings.IniFormat)

		#读取用户配置信息
			user_value = self.config.value(QString("config/") + user_key).toString()
			return True
