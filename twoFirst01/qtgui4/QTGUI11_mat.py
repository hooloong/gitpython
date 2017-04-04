# -*-coding:UTF-8 -*-
__author__ = 'Hooloong'


from PyQt4 import QtGui
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QT as NavigationToolbar
import matplotlib.pyplot as plt
import pylab as pl
from scipy.optimize import leastsq
from scipy.integrate import *
import warnings
import matplotlib.backends.backend_qt5agg
import math

pl.mpl.rcParams['font.sans-serif'] = ['SimHei']#指定默认字体
pl.mpl.rcParams['axes.unicode_minus'] = False#解决保存图像是负号'-'显示为方块的问题

class Window(QtGui.QWidget):
    param=[0,0,0]
    def __init__(self):
        super(Window, self).__init__()

        # a figure instance to plot on
        self.figure = plt.figure()

        # this is the Canvas Widget that displays the `figure`
        # it takes the `figure` instance as a parameter to __init__
        self.canvas = FigureCanvas(self.figure)

        # this is the Navigation widget
        # it takes the Canvas widget and a parent
        self.toolbar = NavigationToolbar(self.canvas, self)

        # Just some button connected to `plot` method
        self.button = QtGui.QPushButton('Plot')
        self.button.clicked.connect(self.plot)

        self.inLbl=QtGui.QLabel(u"输入",self)
        self.inEdit=QtGui.QLineEdit(self)

        self.modelLbl=QtGui.QLabel(u"函数模型：a*b^c^x",self)
        self.blankLbll=QtGui.QLabel("",self)

        self.oriALbl=QtGui.QLabel(u"初始参数a：",self)
        self.oriAEdit=QtGui.QLineEdit(self)
        self.oriBLbl=QtGui.QLabel(u"初始参数b：",self)
        self.oriBEdit=QtGui.QLineEdit(self)
        self.oriCLbl=QtGui.QLabel(u"初始参数c：",self)
        self.oriCEdit=QtGui.QLineEdit(self)

        self.resALbl=QtGui.QLabel(u"预测参数a：",self)
        self.resAEdit=QtGui.QLineEdit(self)
        self.resBLbl=QtGui.QLabel(u"预测参数b：",self)
        self.resBEdit=QtGui.QLineEdit(self)
        self.resCLbl=QtGui.QLabel(u"预测参数c：",self)
        self.resCEdit=QtGui.QLineEdit(self)

        self.perLbl=QtGui.QLabel(u"问题数百分比：",self)
        self.perEdit=QtGui.QLineEdit(self)
        self.perEdit.setValidator(QtGui.QDoubleValidator(0,100,2,self))
        self.perUnitLbl=QtGui.QLabel(u"%",self)
        self.dayLbl=QtGui.QLabel(u"天数：",self)
        self.dayEdit=QtGui.QLineEdit(self)
        self.dayUnitLbl=QtGui.QLabel(u"天",self)
        self.getDayBtn=QtGui.QPushButton(u"计算天数")
        self.getDayBtn.clicked.connect(self.getDay)

        self.dayLbl2=QtGui.QLabel(u"天数：",self)
        self.dayEdit2=QtGui.QLineEdit(self)
        self.dayUnitLbl2=QtGui.QLabel(u"天",self)
        self.numLbl=QtGui.QLabel(u"问题数：",self)
        self.numEdit=QtGui.QLineEdit(self)
        self.numUnitLbl=QtGui.QLabel(u"个",self)
        self.getNumBtn=QtGui.QPushButton(u"计算问题数")
        self.getNumBtn.clicked.connect(self.getNum)

        # set the layout
        gridLayout=QtGui.QGridLayout()
        # gridLayout.setSpacing(10)
        gridLayout.addWidget(self.inLbl,0,0,1,2)
        gridLayout.addWidget(self.inEdit,0,1,1,8)

        gridLayout.addWidget(self.modelLbl,1,0,2,2)
        gridLayout.addWidget(self.blankLbll,1,2,2,1)

        gridLayout.addWidget(self.oriALbl,1,3,1,1)
        gridLayout.addWidget(self.oriAEdit,1,4,1,1)
        gridLayout.addWidget(self.oriBLbl,1,5,1,1)
        gridLayout.addWidget(self.oriBEdit,1,6,1,1)
        gridLayout.addWidget(self.oriCLbl,1,7,1,1)
        gridLayout.addWidget(self.oriCEdit,1,8,1,1)

        gridLayout.addWidget(self.resALbl,2,3,1,1)
        gridLayout.addWidget(self.resAEdit,2,4,1,1)
        gridLayout.addWidget(self.resBLbl,2,5,1,1)
        gridLayout.addWidget(self.resBEdit,2,6,1,1)
        gridLayout.addWidget(self.resCLbl,2,7,1,1)
        gridLayout.addWidget(self.resCEdit,2,8,1,1)

        gridLayout.addWidget(self.perLbl,3,0,1,1)
        gridLayout.addWidget(self.perEdit,3,1,1,1)
        gridLayout.addWidget(self.perUnitLbl,3,2,1,1)
        gridLayout.addWidget(self.dayLbl,3,3,1,1)
        gridLayout.addWidget(self.dayEdit,3,4,1,1)
        gridLayout.addWidget(self.dayUnitLbl,3,5,1,1)
        gridLayout.addWidget(self.getDayBtn,3,6,1,1)

        gridLayout.addWidget(self.dayLbl2,4,0,1,1)
        gridLayout.addWidget(self.dayEdit2,4,1,1,1)
        gridLayout.addWidget(self.dayUnitLbl2,4,2,1,1)
        gridLayout.addWidget(self.numLbl,4,3,1,1)
        gridLayout.addWidget(self.numEdit,4,4,1,1)
        gridLayout.addWidget(self.numUnitLbl,4,5,1,1)
        gridLayout.addWidget(self.getNumBtn,4,6,1,1)

        gridLayout.addWidget(self.toolbar,5, 1, 1, 8)
        gridLayout.addWidget(self.canvas,6, 1, 1, 8)
        gridLayout.addWidget(self.button,7,0,1,1)
        self.setLayout(gridLayout)

        self.setWindowTitle(u"缺陷预测")
        self.resize(900, 700)

        self.oriAEdit.setText('5.0')
        self.oriBEdit.setText('0.1')
        self.oriCEdit.setText('1.0')
        self.perEdit.setText("95")

    def plot(self):
        ''' plot some random stuff '''
        # random data

        #data = [random.random() for i in range(10)]
        # create an axis
        x_new,y_new=self.predict()
        ax = self.figure.add_subplot(111)
        ax.clear()
        self.clearDate()
        # discards the old graph
        ax.hold(True)
        # plot data
        y_src=self.getData()
        x_src=np.arange(1,len(y_src)+1,1)

        ax.plot(x_src,y_src,"*",label=u"真实数据")
        ax.plot(x_new,y_new, label=u"拟合数据")
        plt.legend()

        # refresh canvas
        self.canvas.draw()
        self.resAEdit.setText(str(self.param[0]))
        self.resBEdit.setText(str(self.param[1]))
        self.resCEdit.setText(str(self.param[2]))
        self.dayEdit2.setText("")

        ax.hold(False)


    #从输入文本框中获取文本并返回数字列表
    def getData(self):
          textData_str=self.inEdit.text()
          data=str(textData_str).split(',')
          data_f=[]
          for i in range(len(data)):
               data_f.append(float(data[i]))
          #print data_f
          return data_f

    def clearDate(self):
        self.numEdit.setText("")
        self.dayEdit.setText("")

    def func(self,x, p):
        """
        数据拟合所用的函数: a*b^c^x
        """
        a,b,c = p
        return a*b**c**x   #两个**表示指数运算

    def getNum(self):
        # 根据给定的x，求y
        x_str = str(self.dayEdit2.text()).replace("\n","").split(",")
        try:
            if(len(x_str)==0):
                self.numEdit.setText(str(0))
            else:
                x=float(x_str[0])
                y = self.func(float(x),self.param)
                self.numEdit.setText(str(round(y)))
        except ValueError,e:
            print "error",e,x_str
            self.numEdit.setText(str(0))

    def getDay(self):
        # 根据给定的y，求x
        y_str=str(self.perEdit.text()).replace("\n","").split(",")
        try:
            y=float(y_str[0])*0.01*self.param[0]
            #求x
            a=self.param[0]
            b=self.param[1]
            c=self.param[2]
            tmp=(math.log(y)-math.log(a))/math.log(b)
            x=math.log(tmp)/math.log(c)
            self.dayEdit.setText(str(round(x)))
        except ValueError,e:
            print "error:",e,y_str

    def residuals(self,p, y, x):
        """
        实验数据x, y和拟合函数之间的差，p为拟合需要找到的系数
        """
        return y - self.func(x, p)

    def predict(self,):
        #x=np.arange(1,22,1)  #1~21周
        #y=np.array([24,27,22,20,20,15,9,18,19,16,37,32,29,15,11,10,12,11,7,9,11])  #第1周的缺陷数
        y=self.getData()
        x=np.arange(1,len(y)+1,1)
        #y_accu=np.add.accumulate(y)    #累积分布
        y_accu=y;
        num=len(y)

        #p=[0.5,0.1,1.2]   #指定a、b、c的初始值
        #p=self.getParam()
        p=[float(self.oriAEdit.text()),float(self.oriBEdit.text()),float(self.oriCEdit.text())]

        # 调用leastsq进行数据拟合
        # residuals为计算误差的函数
        # p0为拟合参数的初始值
        # args为需要拟合的实验数据
        plsq = leastsq(self.residuals, p, args=(y_accu, x))
        x_new=np.arange(1,num+200,1)

        #print u"拟合参数", plsq[0] # 实验数据拟合后的参数

        predict_res=self.func(x_new,plsq[0])
        self.param=plsq[0]   #保存拟合后的参数

        return x_new,predict_res


import sys
if __name__ == '__main__':
    # warnings.filterwarnings("ignore",category=matplotlib.backends.backend_qt5agg.mplDeprecation)
    app = QtGui.QApplication(sys.argv)
    m = Window()
    m.show()
    app.exec_()
    #del m
    sys.exit()