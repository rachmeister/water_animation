import numpy as np

def linear5(sim):
	k = sim.b
	c2 = sim.g
	dt = sim.dt
	dx = sim.dx
	nb = sim.nb

#	reflective_bc(sim)
	dh = (1.-k*dt)*(sim.dh)+(c2*(dt/dx)**2)*(-4*sim.h[  nb:  -nb,  nb:  -nb] + \
															  sim.h[    :-2*nb,  nb:  -nb] + \
															  sim.h[2*nb:     ,  nb:  -nb] + \
															  sim.h[  nb:  -nb,    :-2*nb] + \
															  sim.h[  nb:  -nb,2*nb:     ])

	return dh

def linear5_irregular(sim):
	k = sim.b
	c2 = sim.g
	dt = sim.dt
	dx = sim.dx
	nb = sim.nb

	A = 2./(np.square(sim.alpha[:,:-1])+np.multiply(sim.alpha[:,:-1],sim.alpha[:,1:]) )
	B = 2./(np.square(sim.beta[1:,:])+np.multiply(sim.beta[1:,:],sim.beta[:-1,:]) )
	C = 2./np.multiply(sim.alpha[:,:-1],sim.alpha[:,1:])+2./np.multiply(sim.beta[:-1,:],sim.beta[1:,:])
	D = 2./(np.square(sim.beta[:-1,:])+np.multiply(sim.beta[:-1,:],sim.beta[1:,:]) )
	E = 2./(np.square(sim.alpha[:,1:])+np.multiply(sim.alpha[:,:1],sim.alpha[:,:-1]) )

	dh = (1.-k*dt)*(sim.dh)+(c2*(dt/dx)**2)*(-np.multiply(C,sim.h[  nb:  -nb,  nb:  -nb]) + \
															np.multiply(A,sim.h[    :-2*nb,  nb:  -nb]) + \
															np.multiply(E,sim.h[2*nb:     ,  nb:  -nb]) + \
															np.multiply(B,sim.h[  nb:  -nb,    :-2*nb]) + \
															np.multiply(D,sim.h[  nb:  -nb,2*nb:     ]))

	return dh

def linear9(sim):
	k = sim.b
	c2 = sim.g
	dt = sim.dt
	dx = sim.dx
	nb = sim.nb

#	reflective_bc(sim)

## Standard stencil
	dh = (1.-k*dt)*(sim.dh)+(c2*(dt/dx)**2)*(-8*sim.h[nb:-nb,nb:-nb] + \
															  sim.h[    :-2*nb,  nb:  -nb] + \
															  sim.h[2*nb:     ,  nb:  -nb] + \
															  sim.h[  nb:  -nb,    :-2*nb] + \
															  sim.h[  nb:  -nb,2*nb:     ] + \
															  sim.h[    :-2*nb,    :-2*nb] + \
															  sim.h[2*nb:     ,2*nb:     ] + \
															  sim.h[2*nb:     ,    :-2*nb] + \
															  sim.h[    :-2*nb,2*nb:     ])
## Skewed stencil
#	dh = (1.-k*dt)*(sim.dh)+(c2*(dt/dx)**2)*(-20*sim.h[nb:-nb,nb:-nb] + \
#															 4*sim.h[    :-2*nb,  nb:  -nb] + \
#															 4*sim.h[2*nb:     ,  nb:  -nb] + \
#															 4*sim.h[  nb:  -nb,    :-2*nb] + \
#															 4*sim.h[  nb:  -nb,2*nb:     ] + \
#															   sim.h[    :-2*nb,    :-2*nb] + \
#															   sim.h[2*nb:     ,2*nb:     ] + \
#															   sim.h[2*nb:     ,    :-2*nb] + \
#															   sim.h[    :-2*nb,2*nb:     ])

	return dh

def reflective_bc(sim):
	sim.h[ :, 0] = sim.h[ :, 1]
	sim.h[ :,-1] = sim.h[ :,-2]
	sim.h[ 0, :] = sim.h[ 1, :]
	sim.h[-1, :] = sim.h[-2, :]

def passive_bc(sim):
#	sim.h[ :, 0] = sim.h[:, 2] - 2.*sim.h[ :, 1]
#	sim.h[ :,-1] = sim.h[:,-3] - 2.*sim.h[ :,-2]
#	sim.h[ 0, :] = sim.h[2, :] - 2.*sim.h[ 1, :]
#	sim.h[-1, :] = sim.h[-3,:] - 2.*sim.h[-2, :]
	sim.h[ :, 0] = 0
	sim.h[ :,-1] = 0
	sim.h[ 0, :] = 0
	sim.h[-1, :] = 0

def periodic_bc(sim):
	sim.h[ :, 0] = sim.h[ :,-2]
	sim.h[ :,-1] = sim.h[ :, 1]
	sim.h[ 0, :] = sim.h[-2, :]
	sim.h[-1, :] = sim.h[1,  :]
