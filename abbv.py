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

	def __init__(self, h0, a0, b0):
		self.nx,self.ny = h0.shape		# number of points in x,y of the domain
		self.nb = 1 						# number of boundary cells per side
		self.it = 0							# iteration number

		array = np.zeros((self.nx+2*self.nb,self.ny+2*self.nb),dtype=np.double)
		array[self.nb:-self.nb,self.nb:-self.nb] = h0
		self.h = array
		self.dh = np.zeros((self.nx,self.ny),dtype=np.double)

		self.bc = methods.passive_bc 	# Boundary Condition type -- callable BC function 

		self.g = 0.8
		self.b = 0.05 

		self.dt = 0.01
		self.dx = 0.5
		self.alpha = a0
		self.beta = b0

		self.rain = False
		self.dropstep = 50

		self.obj = True
		self.objx = 10.
		self.objy = 10.
		self.sgn = 1.
		self.objstep = 25

####Access Functions
	def get_shape(self):
		return (self.nx,self.ny)
	def get_h(self):
		return self.h[self.nb:-self.nb,self.nb:-self.nb]
	def set_rain(self,rain, drop=50):
		self.rain = rain
		self.dropstep = drop
	def set_bc(self,type):
		if type == 'passive':
			self.bc = methods.passive_bc
		elif type == 'reflective':
			self.bc = methods.reflective_bc
		elif type == 'periodic':
			self.bc = methods.periodic_bc
		
####Interactions
	def move_object(self):

		move = 1
		direction = random.random()
		dx = self.sgn*direction*move
		dy = self.sgn*(1.-direction)*move
		if( self.objx + dx > self.nx or self.objx + dx < 0 ):
			dx = -dx
			self.sgn = -self.sgn
		if( self.objy + dy > self.ny or self.objy + dy < 0 ):
			dy = -dy
			self.sgn = -self.sgn
		self.objx = self.objx + dx
		self.objy = self.objy + dy		

		idx = int(self.objx)
		idy = int(self.objy)
		self.h[idx,idy] = self.h[idx,idy] - 0.005*(1.-self.objx+idx)
		self.h[idx,idy] = self.h[idx,idy] - 0.005*(1.-self.objy+idy)


	def add_drop(self,height):
		size = random.random()
		if(height==0):
			height = size*0.05
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

####Steps in time
	def step5(self):
		if(self.rain and self.it%self.dropstep==0):
			self.add_drop(0)
		if(self.obj and self.it%self.objstep==0):
			self.move_object()
		self.bc(self)
		self.dh = methods.linear5(self)
#		self.dh = methods.linear5_irregular(self)
		self.h[self.nb:-self.nb,self.nb:-self.nb] = self.h[self.nb:-self.nb,self.nb:-self.nb] + self.dh
		self.it = self.it+1

	def step9(self):
		if(self.rain and self.it%self.dropstep==0):
			self.add_drop(0)
		if(self.obj and self.it%self.objstep==0):
			self.move_object()
		self.bc(self)
		self.dh = methods.linear9(self)
		self.h[self.nb:-self.nb,self.nb:-self.nb] = self.h[self.nb:-self.nb,self.nb:-self.nb] + self.dh
		self.it = self.it+1
