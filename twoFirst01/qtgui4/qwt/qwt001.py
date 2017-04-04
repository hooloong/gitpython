
__author__ = 'hooloongge'
#coding=utf-8
import numpy as np
from guiqwt.pyplot import *

t = np.linspace(0, 20, 1000)
u = np.sin(t) + np.random.randn(1000)
i = np.cos(t) + np.random.randn(1000)
subplot(2,1,1)
plot(t, u, "r-", label=u"v")
xlabel(u"time")
ylabel(u"VV")
legend()
subplot(2,1,2)
plot(t, i, "g-", label=u"current")
xlabel(u"time")
ylabel(u"current")
legend()
title(u"V-C")
show()