import numpy as np
import random
import methods

class Abbv(object):
	"""An instance of a shallow water simulation

		Input Units:
		H is average height in [m]
		dx is node spacing in [m]
		h0 is initial deviation in height from mean [m]
		u0,v0 are initial velocities [m/2]
	"""

	def __init__(self, h0):
		self.nx,self.ny = h0.shape
		self.it = 0

		self.dh = np.zeros((self.nx,self.ny),dtype=np.double)
		self.h = h0

		self.g = 0.8
		self.b = 0.2 

		self.dt = 0.01
		self.dx = 0.5

		self.rain = False
		self.dropstep = 50
	
	def add_drop(self,height):
		size = random.random()
		if(height==0):
#			height = random.random()*0.05
			height = size*0.05
		#width = random.randint(3,9)
		width = int(np.floor(size*10+1))
		X=np.arange(-0.5*width,0.5*width,1.)
		Y=np.arange(-0.5*width,0.5*width,1.)
		X,Y=np.meshgrid(X,Y)
		D = height* np.exp(-3*(np.square(X)+np.square(Y)))
		i = random.randint(0,self.nx)
		j = random.randint(0,self.ny)
		
		h = self.h
		rolli = False
		rollj = False
		if( i+width > self.nx-1 ):
			h = np.roll(h,-width,1)
			i = i-width
			rolli = True
		if( j+width > self.ny-1 ):
			h = np.roll(h,-width,0)
			j = j-width
			rollj = True
		h[i:i+width,j:j+width] = h[i:i+width,j:j+width] + D 
		if( rolli ):
			h = np.roll(h,width,1)
		if( rollj ):
			h = np.roll(h,width,0)
		self.h = h

	def step5(self):
		if(self.rain and self.it%self.dropstep==1):
			self.add_drop(0)
		self.dh = methods.linear5(self)
		methods.reflective_bc(self)
		self.h = self.h+self.dh 
		self.it = self.it+1
	def step9(self):
		if(self.rain and self.it%self.dropstep==1):
			self.add_drop(0)
		self.h[:,0] = 0.1

		self.dh = methods.linear9(self)
		methods.reflective_bc(self)
		self.h = self.h+self.dh 
		self.it = self.it+1
