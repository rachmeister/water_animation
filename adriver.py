import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from mpl_toolkits.mplot3d import axes3d

from abbv import Abbv

n = 64
h0 = np.zeros((n,n),dtype=np.double)
#for i in range(0,n):
#	h0[i,:] = i*0.001
#h0[12:14,12:14]=-0.05

sim = Abbv(h0)

dx = 0.5
nx=n
ny=n
X=np.arange(-(nx-1)*dx/2.,(nx)*dx/2.,dx)
Y=np.arange(-(ny-1)*dx/2.,(ny)*dx/2.,dx)
X,Y=np.meshgrid(X,Y)

zlim = 0.1
fig = plt.figure(figsize=(7, 7)) 
ax = fig.gca(projection='3d')
#ax = fig.add_subplot('211',projection='3d')

for it in range(0,10000):
	sim.step9()
	if(it%15 == 0):
		ax.clear()
		ax.plot_wireframe(X,Y,sim.h)
		ax.set_zlim3d(-zlim,zlim)
		ax.axis('off')
		fig.tight_layout()
		plt.pause(0.0001)
	if(it==0):
		raw_input('Press Enter to continue...')

