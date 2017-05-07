import numpy as np

def single_drop(): 
	h0 = np.zeros((n,n),dtype=np.double)
	h0 = np.zeros((n,n),dtype=np.double)
	a0 = np.ones((n,n+1),dtype=np.double)
	b0 = np.ones((n+1,n),dtype=np.double)
	a0[:,0:35] = 0.
	h0[12:15,12:15] = 0.15

	sim = Abbv(h0,a0,b0)
	sim.rain = False
	a0 = np.ones((n,n+1),dtype=np.double)
	b0 = np.ones((n+1,n),dtype=np.double)
	a0[:,0:35] = 0.
	h0[12:15,12:15] = 0.15

	sim = Abbv(h0,a0,b0)
	sim.rain = False


