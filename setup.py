import numpy as np
from abbv import Abbv


def still(n=64):

	h0 = np.zeros((n,n),dtype=np.double)
	a0 = np.ones((n,n+1),dtype=np.double)
	b0 = np.ones((n+1,n),dtype=np.double)

	sim = Abbv(h0,a0,b0)
	sim.set_rain(False)
	
	return sim

def single_drop(n=64): 
	
	h0 = np.zeros((n,n),dtype=np.double)
	a0 = np.ones((n,n+1),dtype=np.double)
	b0 = np.ones((n+1,n),dtype=np.double)
	idx = int(n/2)
	h0[idx-1:idx+1,idx-1:idx+1] = 0.15

	sim = Abbv(h0,a0,b0)
	sim.set_rain(False)
	
	return sim

def single_drop_uncentered(n=64): 
	
	h0 = np.zeros((n,n),dtype=np.double)
	a0 = np.ones((n,n+1),dtype=np.double)
	b0 = np.ones((n+1,n),dtype=np.double)
	idx = int(n/4)
	h0[idx-1:idx+1,idx-1:idx+1] = 0.15

	sim = Abbv(h0,a0,b0)
	sim.set_rain(False)
	
	return sim

def raining(n=64):

	h0 = np.zeros((n,n),dtype=np.double)
	a0 = np.ones((n,n+1),dtype=np.double)
	b0 = np.ones((n+1,n),dtype=np.double)

	sim = Abbv(h0,a0,b0)
	sim.set_rain(True)
	
	return sim


