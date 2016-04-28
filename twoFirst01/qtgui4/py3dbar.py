from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import numpy as np
#from IPython.Shell import IPShellEmbed
#sh = IPShellEmbed()
data = np.array([
[0,1,0,2,0],
[0,3,0,2,0],
[6,1,1,7,0],
[0,5,0,2,9],
[0,1,0,4,0],
[9,1,3,4,2],
[0,0,2,1,3],
])
column_names = ['a','b','c','d','e']
row_names = ['Mon','Tue','Wed','Thu','Fri','Sat','Sun']
fig = plt.figure()
ax = Axes3D(fig)
lx= len(data[0])   # Work out matrix dimensions
ly= len(data[:,0])
xpos = np.arange(0,lx,1) # Set up a mesh of positions
ypos = np.arange(0,ly,1)
xpos, ypos = np.meshgrid(xpos+0.25, ypos+0.25)
xpos = xpos.flatten() # Convert positions to 1D array
ypos = ypos.flatten()
zpos = np.zeros(lx*ly)
dx = 0.5 * np.ones_like(zpos)
dy = dx.copy()
dz = data.flatten()
ax.bar3d(xpos,ypos,zpos, dx, dy, dz, color='b')
#sh()
ax.w_xaxis.set_ticklabels(column_names)
ax.w_yaxis.set_ticklabels(row_names)
ax.set_xlabel('Letter')
ax.set_ylabel('Day')
ax.set_zlabel('Occurrence')
plt.show()