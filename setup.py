import numpy as np
import random

from abbv import Abbv
import methods


def still(n=64):

	h0 = np.zeros((n,n),dtype=np.double)
	sim = Abbv(h0)
	sim.set_rain(False)
	
	return sim

def single_drop(n=64): 
	
	h0 = np.zeros((n,n),dtype=np.double)
	idx = int(n/2)
	h0[idx-1:idx+1,idx-1:idx+1] = 0.15

	sim = Abbv(h0)
	sim.set_rain(False)
	
	return sim

def single_drop_uncentered(n=64): 
	
	h0 = np.zeros((n,n),dtype=np.double)
	idx = int(n/4)
	h0[idx-1:idx+1,idx-1:idx+1] = 0.15

	sim = Abbv(h0)

	sim.set_rain(False)
	
	return sim

def raining(n=64):

	sim = still(n)
	sim.set_rain(True)
	
	return sim

def wake(n=64):
	sim = still(n)
	sim.set_obj(True)
	
	return sim

def coastline(n=64):

	h0 = np.zeros((n,n),dtype=np.double)
	a0 = np.ones((n,n+1),dtype=np.double)
	b0 = np.ones((n+1,n),dtype=np.double)

	idx = int(n/4)
	h0[idx-1:idx+1,idx-1:idx+1] = 0.05
	for i in range(0,n):
		a0[i,0] = random.random()
	print np.amax(a0)

	sim = Abbv(h0,methods.linear5_irregular,a0,b0)

	sim.set_rain(False)
	
	return sim
