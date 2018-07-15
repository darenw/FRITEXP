# -*- coding: utf-8 -*-
"""
Functions to compute fractionally iterated exponentials defined by the work of 
Australian mathematician G. Szekeres  (see references in the paper)

These functions are not guaranteed to be exact and precise and good and true, but
seem to work fine.  No thorough testing has been done (yet) and no attempt has been
made to make them bullet-proof, or capable of handling other than scalar real values
or in some places lists or arrays. Use at your own risk. Do not use for heart-lung
machines, billion dollar NASA spacecraft, or anything serious, without thorough testing.

Written by Daren Scot Wilson
Open Source, MIT Licenced
Get the latest/bestest from GitHub https://github.com/darenw/FRITEX
"""


import numpy as np
from math import *



# Coefs for Szekeres polynomials, taking arg a = u/2
# Beware: the paper shows the ordinary polynomials taking u.
# For some reason long forgotten, u/2 is used for these numerical calculations.
szekpoly0 = ( 1., )
szekpoly1 = ( 1.,   0.0 )
szekpoly2 = ( 1.,  -1./6.,  0.0)
szekpoly3 = ( 1.,  -5./12.,  1./24.,  0.0)
szekpoly4 = ( 1.,  -13./18.,  1./6.,  -1./90.,  0.0)
szekpoly5 = ( 1.,  -77./72.,  89./216.,  -91./1440.,  11./4320.,  0.0)
szekpoly6 = ( 1.,  -87./60.,  175./216., -149./720.,  91./4320., -1./3360., 0.0)

szekpolys = (szekpoly0, szekpoly1, szekpoly2, szekpoly3, szekpoly4, szekpoly5, szekpoly6) 


# g_u(x) for small u and small x
# Use this for -0.5 < u < 0.5,   -.1 < x < .1   (rough guideline)
#
def smallg(u, x):
	"""
		Computes g_u(x) when both u and x are "small"
		g(x) = exp(x)-1  and g_u(x) is fractional iteration order u of g
		Args:
			x (real scalar or np.array): main arg to feed the function
			u (real):   order of iteration of the function g(x) == exp(x)-1 
		Returns:
			real
		See the paper for details. "Small" is undefined, but easy to get a feel
		for after performing some computations.  
		Recommendation: keep u in the
		range -0.5 to 0.5, and x to -0.1 to 0.1   
		Better (maybe): keep u in -0.25 to +0.25, and iterate the calculation to 
		effectively double u.  Keep x in -0.5 to 0.5 or smaller.
	"""
	cc = []
	for sp in reversed(szekpolys):
		cc.append( np.polyval(sp, u/2) )
	cc.append( 0.0 )  # szek poly 0
	#print(cc)
	return np.polyval( cc, x)


# Takes only a simple float value (or integer) for x, not lists or arrays
def iterexp_scalar(u,x):
	"""
		Compute a Szekeres fractionally iterated exponential, scalar u and x only.
		Args:
			u (real):   order of iteration
			x (real):   main arg to feed the function, -inf to +inf.
		Returns:
			real
		Neither u nor x may be lists, numpy arrays, or anything else but simple scalars.
	"""
	intu = int(floor(u+0.5))
	fracu = u - intu
	counte = 0
	while x < 400:     # limit for which exp(exp.5(x)) won't overflow
		x = exp(x)
		counte += 1
		#print("UP ", x, counte)
	countg = 0
	while x > 0.5:
		x = log(x+1.0)
		countg += 1
		#print("DOWN-G ", x, countg)
	y = smallg(fracu, x)
	#print("x = ", x, "  y=", y, " u=", intu, fracu, "  #e,#g=", counte, countg)
	while countg != 0:
		y = exp(y)-1.0
		countg -= 1
		#print("UP_G ", y, countg)
		if y > 400:
			# danger of overflow
			# cut short the number of g() here, 
			# and reduce count of logs to do in next step
			# by matching amount
			counte -= countg
			#print("CUT  revise ce=", counte)
			break
	while (counte > intu):
		try:
			y = log(y)
		except ValueError:
			y = -inf
			break
		counte -= 1
		#print("DOWN ", y, counte)
	#print("\n")
	return y



# test it on some basic cases
def SzekeresTests():
	print(iterexp(0, 0), 0.0)
	print(iterexp(1,0),  1.0)
	print(iterexp(2,0), exp(1))
	print(iterexp(1/3, iterexp(2/3, 1.6), exp(1.6)))

# singularity of exp_-0.001(x) found at -6.12678572... (using incorrect code)
	
	
# Iterated exponential function capable of processing simple scalars, arrays, and 
def iterexp(u,xx):
	"""
		Compute Szekeres-based fractionally iterated exponential, taking numpy array, list, or 
		plain scalar for x.
		Args:
			u (real):   order of iteration
			x (array/list of real):   value to feed the function, real, -inf to +inf.
		Returns:
			array, list or scalar matching form of given x, filled with values of exp_u(x) 
	"""
	if type(xx)==np.ndarray:	
		yy = np.empty(xx.shape)
		for i in range(xx.size):
			yy[i] = iterexp(u,xx[i])
		return yy
	elif type(xx)==list or type(xx)==tuple:
		yy=[]
		for x in xx:
			yy.append( iterexp(u,x))
		if type(xx)==tuple:
			yy = tuple(yy)
		return yy
	else:
		return iterexp_scalar(u,xx)



