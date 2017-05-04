import numpy as np
import random
import methods

class Simulation(object):
	"""An instance of a shallow water simulation

		Input Units:
		H is average height in [m]
		dx is node spacing in [m]
		h0 is initial deviation in height from mean [m]
		u0,v0 are initial velocities [m/2]
	"""

	def __init__(self, eta0, h0, u0, v0, H=1.0, dx=0.5):
		self.nx,self.ny = h0.shape
		self.n,_ = h0.shape
		self.n = self.n - 4
		self.it = 0

		self.eta = eta0
		self.h = h0
		self.u = u0
		self.v = v0

		self.g = 1.
		self.b = 0.05

		self.dt = 0.05
		self.dx = dx

		self.rain = True
		self.dropstep = 50

	def add_drop(self):
		height = random.random()*0.08
		width = random.randint(6,10)
		X=np.arange(-0.5*width,0.5*width,1.)
		Y=np.arange(-0.5*width,0.5*width,1.)
		X,Y=np.meshgrid(X,Y)
		D = height* np.exp(-5*(np.square(X)+np.square(Y)))
		i = random.randint(0,self.nx)
		j = random.randint(0,self.ny)
		
		h = self.eta
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
		self.eta = h

	def eulers_step(self):
		
		detah, du, dv = methods.eulers(self)

		self.eta = self.eta + deta
		self.u = self.u + du
		self.v = self.v + dv
		self.it = self.it+1

	def lax_wendroff(self):
		if(self.rain and self.it%self.dropstep==1):
			self.add_drop()

		deta, du, dv = methods.laxwendroff(self)

		self.eta = self.eta + deta
		self.u = self.u + du
		self.v = self.v + dv
		self.it = self.it+1
