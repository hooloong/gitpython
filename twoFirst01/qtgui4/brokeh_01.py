__author__ = 'hooloongge'
# -*- coding: utf-8 -*-
import sys,math,random,time
from bokeh.charts import Bar,output_file,show
data = {"y":[1,2,3,4,5]}
output_file("lines.html",title="line plot example")
p = Bar(data,title = "line chart example",xlabel='x',ylabel='values',width=400,height=400)
show(p)