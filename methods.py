import numpy as np

def roll(u, shift):

    v = u.copy()
    for k in range(len(shift)):
        v = np.roll(v, shift[k], axis=k)
    return v
def d_dx(M):
   #create array of x derivatives
   return (np.roll(M,-1,1) - np.roll(M, 1, 1))/2.
def d_dy(M):
   return (np.roll(M,-1,0) - np.roll(M, 1, 0))/2.
def calc_dt(sim):
	return sim.dt
def eulers(sim):
	g = sim.g
	b = sim.b
	dx = sim.dx
	dt = sim.dt
	du_dt = -sim.y*d_dx(sim.u)/dx-sim.v*d_dy(sim.u)/dx-g*d_dx(sim.eta)/dx - b*sim.u
	dv_dt = -sim.u*d_dx(sim.v)/dx-sim.v*d_dy(sim.v)/dx-g*d_dy(sim.eta)/dx - b*sim.v 

	deta_dt = -d_dx(sim.u*(sim.eta+sim.h)) - d_dy(sim.v*(sim.eta+sim.h))

	return deta_dt*dt, du_dt*dt, dv_dt*dt

def laxwendroff(sim):
	n = sim.n
	g = sim.g
	b = sim.b
	dx = sim.dx
	dt = sim.dt

	H = sim.eta+sim.h
	U = sim.u
	V = sim.v
	## Reflective Boundary Conditons
#	H[:,0]   = H[:,1];		U[:,0]   = U[:,1];		V[:,0]   = -V[:,1];
#	H[:,n+1] = H[:,n];		U[:,n+1] = U[:,n];		V[:,n+1] = -V[:,n];
#	H[0,:]   = H[1,:];		U[0,:]   = -U[1,:];	 	V[0,:]   = V[1,:];
#	H[n+1,:] = H[n,:];		U[n+1,:] = -U[n,:];		V[n+1,:] = V[n,:];

	## Half Step
	hx = (roll(H,(1,1))+np.roll(H,1,0))/2. - dt/(2.*dx)*(roll(U,(1,1))-np.roll(U,1,0))  	
	ux = (roll(U,(1,1))+roll(U,(1,0)))/2. - dt/(2.*dx)*( 	\
		( np.divide(np.square(roll(U,(1,1))), roll(H,(1,1))) + g/2.*np.square(roll(H,(1,1))) ) -	\
		( np.divide(np.square(roll(U,(1,0))), roll(H,(1,0))) + g/2.*np.square(roll(H,(1,0))) ))
	vx = (roll(V,(1,1))+roll(V,(1,0)))/2. - dt/(2.*dx)*( 	\
		np.divide(np.multiply(roll(U,(1,1)),roll(V,(1,1))), roll(H,(1,1))) -
		np.divide(np.multiply(roll(U,(1,0)),roll(V,(1,0))), roll(H,(1,0))) )

	hy = (roll(H,(1,1))+np.roll(H,1,1))/2. - dt/(2.*dx)*(roll(U,(1,1))-np.roll(U,1,1))  	
	uy = (roll(U,(1,1))+roll(V,(1,0)))/2. - dt/(2.*dx)*( 	\
		np.divide(np.multiply(roll(V,(1,1)),roll(U,(1,1))), roll(H,(1,1))) -
		np.divide(np.multiply(roll(V,(0,1)),roll(U,(0,1))), roll(H,(0,1))) )
	vy = (roll(V,(1,1))+roll(V,(0,1)))/2. - dt/(2.*dx)*( 	\
		( np.divide(np.square(roll(V,(1,1))), roll(H,(1,1))) + g/2.*np.square(roll(H,(1,1))) ) -	\
		( np.divide(np.square(roll(V,(0,1))), roll(H,(0,1))) + g/2.*np.square(roll(H,(0,1))) ))

	## Full Step
	deta = -(dt/dx)*(roll(ux,(-1,0)) - roll(ux,(-1,-1))) - \
				  (dt/dx)*(roll(vy,(0,-1)) - roll(vy,(-1,-1)))
	du = -(dt/dx)*(( np.divide(np.square(roll(ux,(-1,0))), roll(hx,(-1,0))) + g/2.*np.square(roll(hx,(-1,0)))) - \
			( np.divide(np.square(roll(ux,(-1,-1))), roll(hx,(-1,-1))) + g/2.*np.square(roll(hx,(-1,-1))) )) \
		  -(dt/dx)*((np.divide(np.multiply(roll(vy,(0,-1)),roll(uy,(0,-1))), roll(hy,(0,-1)) )) - \
			( np.divide(np.multiply(roll(vy,(-1,-1)),roll(uy,(-1,-1))), roll(hy,(-1,-1))) ))
	dv = -(dt/dx)*((np.divide(np.multiply(roll(ux,(-1,0)),roll(vx,(-1,0))), roll(hx,(-1,0)) )) - \
			( np.divide(np.multiply(roll(ux,(-1,-1)),roll(vx,(-1,-1))), roll(hx,(-1,-1))) )) \
	     -(dt/dx)*(( np.divide(np.square(roll(vy,(0,-1))), roll(hy,(0,-1))) + g/2.*np.square(roll(hy,(0,-1)))) - \
			( np.divide(np.square(roll(vy,(-1,-1))), roll(hy,(-1,-1))) + g/2.*np.square(roll(hy,(-1,-1))) )) 

	#dampening
	du = du - dt*U*b
	dv = dv - dt*V*b
	
	return deta, du, dv

def linear5(sim):
	k = sim.b
	c2 = sim.g
	dt = sim.dt
	dx = sim.dx
	dh = (1.-k*dt)*(sim.dh)+(c2*(dt/dx)**2)*(-4*sim.h+roll(sim.h,(0,1))+roll(sim.h,(0,-1))+roll(sim.h,(1,0))+roll(sim.h,(-1,0)))

	return dh

def linear9(sim):
	k = sim.b
	c2 = sim.g
	dt = sim.dt
	dx = sim.dx
## Standard stencil
#	dh = (1.-k*dt)*(sim.dh)+(c2*(dt/dx)**2)*(-8*sim.h+roll(sim.h,(0,1))+roll(sim.h,(0,-1))+roll(sim.h,(1,0))+roll(sim.h,(-1,0)) \
#																	+roll(sim.h,(1,1)) + roll(sim.h,(-1,-1)) + roll(sim.h,(1,-1)) + roll(sim.h,(-1,1)))
## Skewed stencil
	dh = (1.-k*dt)*(sim.dh)+(c2*(dt/dx)**2)*(-20*sim.h+4*roll(sim.h,(0,1))+4*roll(sim.h,(0,-1))+4*roll(sim.h,(1,0))+4*roll(sim.h,(-1,0)) \
																	+roll(sim.h,(1,1)) + roll(sim.h,(-1,-1)) + roll(sim.h,(1,-1)) + roll(sim.h,(-1,1)))
	return dh

def reflective_bc(sim):
	k = sim.b
	c2 = sim.g
	dt = sim.dt
	dx = sim.dx
	nx = sim.nx-1
	ny = sim.ny-1
	sim.dh[:,0] = (1.-k*dt)*(sim.dh[:,0])-(c2*(dt/dx)**2)*(3*sim.h[:,0]-sim.h[:,1]-np.roll(sim.h[:,0],1)-np.roll(sim.h[:,0],-1))
	sim.dh[:,nx] = (1.-k*dt)*(sim.dh[:,nx])-(c2*(dt/dx)**2)*(3*sim.h[:,nx]-sim.h[:,nx-1]-np.roll(sim.h[:,nx],1)-np.roll(sim.h[:,nx],-1))
	sim.dh[0,:] = (1.-k*dt)*(sim.dh[0,:])-(c2*(dt/dx)**2)*(3*sim.h[0,:]-np.roll(sim.h[0,:],1)-np.roll(sim.h[0,:],-1)-sim.h[1,:])
	sim.dh[ny,:] = (1.-k*dt)*(sim.dh[ny,:])-(c2*(dt/dx)**2)*(3*sim.h[ny,:]-sim.h[ny-1,:]-np.roll(sim.h[ny,:],1,0)-np.roll(sim.h[ny,:],-1,0))
