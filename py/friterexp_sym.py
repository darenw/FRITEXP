# -*- coding: utf-8 -*-
# fritex_sym.py
"""
Functions to compute fractionally iterated exponentials and related things
These follow the "symmetry based" definition, where the Schröder function
is made to obey L(-x) + L(x) = 1 and L(exp(x)) = (1/2)L(x)

Although not stated in the individual function docstrings, beware that exceptions
may be thrown.  We're performing iterated exponentials which can easily overflow,
and iterated logarithms that could bad.  The "if" and "while" statements take care
of all the normal cases I encountered, but maybe I missed some crazy corner cases.

These functions are not guaranteed to be exact and precise and good and true, but
seem to work fine.  No thorough testing has been done (yet) and no attempt has been
made to make them bullet-proof, or capable of handling other than scalar real values
or in some places lists or arrays. Use at your own risk. Do not use for heart-lung
machines, billion dollar NASA spacecraft, or anything serious, without thorough testing.

Written by Daren Scot Wilson
Open Source, MIT Licenced
Get the latest/bestest from GitHub https://github.com/darenw/FRITEX 
"""

from math import *
import numpy as np



def LfromX(x):
	"""
		Compute Schroder function value from given x.
		
		Args:
			x  (real):   main arg, -inf to +inf
	"""
	
	return LfromS( SfromX( x ))



def SfromX(x, nmax=25, tau= 1E-12):
	"""
		Compute sequence of generalized inverses for a given x.
		The result is to be fed into LfromS() to obtain L, 
		or XfromS() to reproduce x. 
		Use LfromX() if all you want is L.
		
		Args:
			x     (real):  -inf to +inf
			nmax  (int):   Maximum length for sequence.  default 25. 
			tau   (real):  How close to zero for terminating S.
			
		Returns:
			List of integers, mostly ranging from 1 to 5 or so.
			Length will never exceed nmax.
		
		Each element in S is worth about two or three bits. 25 elements is then
		worth about 50 to 75 bits, maybe more. That should cover IEEE double floats,
		though such rough estimation isn't really valid for the weird 
		exponential-fractal nature of symmetry-based fritex function.
	"""
	seq = []
	if x<0:
		seq = [0]
		x=-x
	while nmax>0:
		count = 0
		while x>0:
			x = log(x)
			count +=1
		seq.append(count)
		if abs(x) < tau:
			break
		x = -x
		nmax -= 1
	return seq



def XfromS(S):
	"""
		Compute value of x for a given sequence. Inverse of SfromX().
		
		Args:
			S (list/tuple of int):    list of integers - see paper for details 
		Returns:
			real
			
		Note that "large" integers in S, for example six, will effectively cut
		off the list there - you might as well not bother with that element and 
		anything after, when using normal IEEE 64-bit (or 80-bit) floats.
		If you use some super high precision form of binaryized real numbers,
		then have fun! You may be able to use S elements as high as 7 maybe 8. 
		
		Remember, the value of each element in S corresponds to tapping the 'exp'
		key on a calculator that number of times. This overflows quick!
	"""
	x = 0
	for c in reversed(S):
		try:
			for i in range(c):
				x = exp(x)
		except OverflowError:
			x = inf
		x = -x
	return -x    




def LfromS(seq):
	"""
		Compute Schroder function value L from a given sequence.
		This performs the calculation by plodding through the algorithm given in
		the paper.  Humans can easily recognize the relation between elements of S
		and length of runs of 0s or 1s in the binary representation of L. Knowing
		that, there probably is a slicker way to code LfromS().
		
		Args:
			S (list of int):   Sequence - see paper for details
			
		Returns:
			value of L, real in range  0.0 .. 1.0
			
		Note that overflows are no problem - S may contain "large" values like ten.
		Note also there's no check on the length of S, or if it's empty.
	"""
	Lambda = 1.0
	L = Lambda/2
	for c in reversed(seq):
		L = L/(2**c)
		L = Lambda - L
	L = Lambda-L
	return L



def SfromL( L, nmax=25, epsilon= 2**(-50) ):
	"""	
		Compute sequence of generalized inverses from given Schroder value L.
		
		Args:
			L       (real):    main arg, range 0.0 to 1.0
			nmax    (integer): default 22.  Max length to allow for S.
			epsilon (real):    smallest change in L you don't care about.
		Returns:
			Sequence as list of integers
		
		Normally epsilon should be 2 ** -(number of significant bits in L), and for
		IEEE 64-bit that's 52 bits (the rest being sign and exponent).
		Fearing trouble with round-offs, I set the default to 50 bits.
		
		If you're using some alternative form of real numbers, say a fixed point
		format built for a fixed range like -1 to 1, or 0 to 1, then set epsilon
		to something suitable for that type.
	"""
	# Prevent accidental use of negative L, or L too close to zero
	# which can lead to infinite loop
	if L<1e-22:   # 1e-22 is a guess; no real thinking was done
		return [73]
	S = []
	while  len(S) <= nmax:
		count = 0
		while L < 0.5:
			L = 2.0*L
			count +=1
		S.append( count)
		if count > 52:
			break;
		if abs(L-0.5) < epsilon:
			break
		L = 1-L
		if L<1e-22:
			break
	return S



def iterexp_scalar(u, x):
	"""
		Compute a symmetry-based fractionally iterated exponential, scalar u and x only.
		Args:
			u (real):   order of iteration
			x (real):   main arg to feed the function, -inf to +inf.
		Returns:
			real
		Neither u nor x may be lists, numpy arrays, or anything else but simple scalars.
	"""
	L = LfromS( SfromX( x ))
	L *= 2**(-u)
	S = SfromL( L )
	return XfromS(S)



def iterexp(u,xx):
	"""
		Compute symmetry-based fractionally iterated exponential, taking numpy array, list, or 
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



def iterexp_show_and_tell(u, x_in):
	"""
		Experimental version of iterexp to print out intermediate data
		See iterexp_scalar for details
	"""
	s_in = SfromX( x_in )
	L_in = LfromS(s_in)
	L_out = L_in * 2**(-u)
	S_out = SfromL( L_out )
	x_out=XfromS(S_out)
	print("       %21s  %21s  %s "  % ("x", "L", "Stack") )
	print("Input  %21g  %21g  %s "  % (x_in, L_in, s_in) )
	print("Output %21g  %21g  %s "  % (x_out, L_out, S_out) )
	return x_out

