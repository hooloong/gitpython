#!/usr/bin/python  
#-*-coding:utf-8-*-

from PyQt4.QtGui import *
from PyQt4.QtCore import *
from PyQt4.Qt import *

class CLabel(QWidget):
	
	signalLabelPress = pyqtSignal(QWidget)
	
	def __init__(self,parent = None):
		super(CLabel,self).__init__(parent)
		self.initVariable()
		self.initSetupUi()
		#self.m_mouseEnterFlag = False
		#self.m_mousePressFlag = True
		#pointer members
		
		#self.m_pLabelIcon = QLabel(self)
		#self.m_pLabelText = QLabel(self)
	
	def setPixmap(self,pixmap):
		self.m_pLabelIcon.setPixmap(pixmap.scaled(QSize(30, 30), Qt.KeepAspectRatio, Qt.SmoothTransformation))
	

	def setText(self,text):
		self.m_pLabelText.setText(text)
	

	def setMouseEnterFlag(self, flag):
		self.m_mouseEnterFlag = flag
		self.update()
	

	def setMousePressFlag(self, flag):
		self.m_mousePressFlag = flag
		self.update()
	

	def enterEvent(self,event):
		if(~self.getMousePressFlag()):
			self.setMouseEnterFlag(True)
		self.setCursor(Qt.PointingHandCursor)
	

	def leaveEvent(self,event):
		self.setMouseEnterFlag(False)
	

	def mousePressEvent(self,e):
		if(e.button() == Qt.LeftButton):		
			self.setMousePressFlag(True)
			self.signalLabelPress.emit(self)
		
	

	def paintEvent(self,e):	
		painter = QPainter(self)
		if(self.getMouseEnterFlag()):		
			self.paintWidget(50, painter)		
		elif(self.getMousePressFlag()):		
			self.paintWidget(80, painter)		
		QWidget.paintEvent(self,e)
	

	def initVariable(self):	
		self.setMouseEnterFlag(False)
		self.setMousePressFlag(False)
	

	def initSetupUi(self):	
		self.createFrame()
		self.createWidget()
		self.createLayout()
	

	def createFrame(self):	
		self.setStyleSheet("QWidget{background:transparent; border:0px; color:white; font-weight:bold; font-size:16px}")
	

	def createWidget(self):	
		self.m_pLabelIcon =  QLabel(self)
		self.m_pLabelText =  QLabel(self)
	

	def createLayout(self):
		self.m_pHLayout = QHBoxLayout()
		self.m_pHLayout.setSpacing(10)
		self.m_pHLayout.setContentsMargins(QMargins(5, 0, 5, 0))
		self.m_pHLayout.addWidget(self.m_pLabelIcon)
		self.m_pHLayout.addWidget(self.m_pLabelText)
		self.m_pHLayout.addStretch()

		self.setLayout(self.m_pHLayout)
	

	def paintWidget(self,transparency,device):	 #QPainter *
		#self.pen = QPen(Qt.NoBrush)
		#self.pen.setWidth(1)
		device.setPen(Qt.NoPen)
		self.linear = QLinearGradient(QPointF(self.rect().topLeft()), QPointF(self.rect().bottomLeft()))
		self.linear.setColorAt(0, QColor(255, 255, 255, transparency))
		self.brush = QBrush(self.linear)
		device.setBrush(self.brush)
		device.drawRoundedRect(self.rect(), 2, 2)
	

	def getMouseEnterFlag(self):	
		return self.m_mouseEnterFlag
	

	def getMousePressFlag(self):	
		return self.m_mousePressFlag
	



if __name__ == '__main__':
	import sys
	app = QApplication(sys.argv)
	
	Label = CLabel()
	Label.show()
	sys.exit(app.exec_())
	


