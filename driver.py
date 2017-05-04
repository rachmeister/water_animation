import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from mpl_toolkits.mplot3d import axes3d

from simulation import Simulation 

n = 64
eta0 = np.zeros((n,n),dtype=np.double)
z0 = np.zeros((n,n),dtype=np.double)
h0 = np.ones((n,n),dtype=np.double)
eta0[10:15,13]=0.2
#eta0[12:14,14] =0.17
#eta0[12:14,12] = 0.17
#eta0[12,13] = 0.17
#eta0[14,13] = 0.17
#eta0[3:5,3:5] = 0.1
#h0[:,0:30] = 1.5
#h0[:,31:32] = 1.4
#h0[:,32:33] = 1.3
#h0[:,33:34] = 1.2
#h0[:,34:35] = 1.1
#h0[:,35:36] = 1.

sim = Simulation(eta0,h0,z0,z0)
#sim.rain = False

dx = 0.5
nx=n
ny=n
X=np.arange(-(nx-1)*dx/2.,(nx)*dx/2.,dx)
Y=np.arange(-(ny-1)*dx/2.,(ny)*dx/2.,dx)
X,Y=np.meshgrid(X,Y)

zlim = 0.2
fig = plt.figure(figsize=(7, 7)) 
ax = fig.gca(projection='3d')
#ax = fig.add_subplot('211',projection='3d')

for it in range(0,10000):
	#sim.euler_step()
	
	sim.lax_wendroff()
	if(it%15 == 0):
		ax.clear()
		ax.plot_wireframe(X,Y,sim.h+sim.eta)
		ax.set_zlim3d(0,1.6)
		ax.axis('off')
		fig.tight_layout()
		plt.pause(0.00001)
	if(it==0):
		raw_input('Press Enter to continue...')


plt.show()

