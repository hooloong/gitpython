#!/usr/bin/python  
#-*-coding:utf-8-*-



from PyQt4.QtGui import *
from PyQt4.Qt import *
from PyQt4.QtCore import *

class skinWidget(QWidget):
	
	def __init__(self, pixname, parent=None):
		super(skinWidget, self).__init__(parent)
		self.signalMapper = QSignalMapper(self)
		 #QSignalMapper *
		self.bkPicName = QStringList()
		self.bkPicName = ["./img/skin/angryBird.jpg", u"./img/skin/blackPoint.jpg", u"./img/skin/blueSky.jpg", \
				   u"./img/skin/classic.jpg", u"./img/skin/greenWorld.jpg", u"./img/skin/oldWood.jpg", \
				   u"./img/skin/pinkLove.jpg", u"./img/skin/redThunder.jpg", u"./img/skin/sixYears.jpg"]
		#self.tip = QStringList()
		self.tip = [ u"愤怒的小鸟", u"优雅爵士", u"蓝色天空", u"经典皮肤", \
				 u"青青世界", u"古典木纹", u"粉色之恋", u"红色惊雷", u"卫士六周年"]

		self.gridLayout = QGridLayout()
		self.gridLayout.setSpacing(0)
		r = 0;c = 0
		for i in range(9):
			self.btn = QPushButton(self)
			# btn.setFlat(true)
			self.icon = QIcon(self.bkPicName[i]) #.left(self.bkPicName[i].indexOf("."))+"Small.jpg"
			self.btn.setIcon(self.icon)
			self.btn.setIconSize(QSize(97, 62))
			self.btn.setToolTip(self.tip[i])
			self.connect(self.btn, SIGNAL("clicked()"), self.signalMapper, SLOT("map()"))
			self.signalMapper.setMapping(self.btn, self.bkPicName[i])
			if(i % 3 == 0):
				r = r + 1
				c = 0
			self.gridLayout.addWidget(self.btn, r, c + 1)
		self.connect(self.signalMapper, SIGNAL("mapped()"), SLOT("changeSkin()"))
		self.connect(self.signalMapper, SIGNAL("mapped()"), SLOT("setSkin()"))
	
		self.mainLayout = QVBoxLayout()
		self.mainLayout.addWidget(QLabel(u"更换皮肤"), 0, Qt.AlignHCenter)
		self.mainLayout.addLayout(self.gridLayout)
		self.setLayout(self.mainLayout)
	
		self.setWindowFlags(Qt.Popup)

	def paintEvent(self, event):
		self.painter = QPainter()
		self.painter.begin(self)
		self.painter.setBrush(QBrush(QPixmap(self.bkPicName)))
		self.painter.setRenderHints(QPainter.Antialiasing, True)
		self.painter.setPen(Qt.black)
		self.painter.drawRect(self.rect())
		self.painter.end()
		
	@pyqtSlot()
	def setSkin(self, picName):
		self.bkPicName = picName
		self.update()
		
if __name__ == '__main__':
	import sys
	app = QApplication(sys.argv)
	
	kin = skinWidget("./img/skin/angryBird.jpg")
	kin.show()
	
	sys.exit(app.exec_())



