import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from mpl_toolkits.mplot3d import axes3d

import setup
from abbv import Abbv

#sim = setup.raining(64)
#sim = setup.single_drop_uncentered(64)
sim = setup.still(64)
sim.set_bc('reflective')
#sim.set_bc('passive')
#sim.set_bc('periodic')
#sim.add_object()

# Setup for display
nx,ny=sim.get_shape()
X=np.arange(-(nx-1)/2.,(nx)/2.,1.)
Y=np.arange(-(ny-1)/2.,(ny)/2.,1.)
X,Y=np.meshgrid(X,Y)

zlim = 0.15 

fig = plt.figure(figsize=(12, 12)) 
ax = fig.gca(projection='3d')
#fig.canvas.mpl_connect('button_press_event', onClick)
#ax = fig.add_subplot('211',projection='3d')

for it in range(0,10000):
	sim.step5()
	if(it%15 == 0):
		ax.clear()
		ax.plot_wireframe(X,Y,sim.get_h())
		ax.set_zlim3d(-zlim,zlim)
		ax.axis('off')
		fig.tight_layout()
		plt.pause(0.0001)
	if(it==0):
		raw_input('Press Enter to continue...')

