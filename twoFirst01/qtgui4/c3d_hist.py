__author__ = 'hoo'
import random

import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

from mpl_toolkits.mplot3d import Axes3D

mpl.rcParams['font.size'] = 10

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

for z in range(8):
     xs = xrange(0,8)
     ys = 4095 * np.random.rand(8)

     color =plt.cm.Set2(random.choice(xrange(plt.cm.Set2.N)))
     ax.bar3d(xs, ys,2,2,2, zs=z, zdir='y', color=color, alpha=0.8)

ax.xaxis.set_major_locator(mpl.ticker.FixedLocator(xs))
ax.yaxis.set_major_locator(mpl.ticker.FixedLocator(ys))

ax.set_xlabel('ledx')
ax.set_ylabel('ledy')
ax.set_zlabel('light')

plt.show()