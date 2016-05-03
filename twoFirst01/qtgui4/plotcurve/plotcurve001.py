# -*- coding: utf-8 -*-
"""
Created on Sat Mar 05 06:47:39 2016

@author: hooloongge
"""

import numpy as np

import matplotlib.pyplot as plt

plt.figure(1) 
#ax1 = plt.subplot(211)
x = np.linspace(0,4095,1000)
#for i in xrange(5):
plt.figure(1)  
plt.plot(x, x,label='No.1:y=1.0*x')
plt.plot(x, 1.6*x,label='No.2:y=1.6*x')
   # plt.sca(ax1) 
plt.plot(x, 0.0005*x*x,label='No.3:y=x*x/(0x3E*0x20)')
  #  plt.sca(ax2)

#plt.sca(ax1)
plt.xlabel("PWM duties")
plt.ylabel("Boosting Brigntness")
plt.legend()
plt.show()