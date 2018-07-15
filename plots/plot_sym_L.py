# Plot exp_u(x) for Szekeres definition


import sys
sys.path.append('../py')

import numpy as np
import matplotlib.pyplot as pp
import friterexp_sym as frit

width=6.0    # inches
height=6.0
printsize = (width,height)


def PlotSchroder(titletext, xname, xrange, Lrange, printsize, numpoints=2400):
	"""
		Plot symmetry-based Schröder’s function for given ranges
		Write to an EPS file for inclusion into the paper
		
	"""
	xx = np.linspace(xrange[0],xrange[1], num=numpoints)
	fig = pp.figure( figsize=printsize )
	plot1 = fig.add_subplot(111)   
	plot1.set_title(titletext)
	plot1.set_xlabel("x")
	plot1.set_ylabel("L(x)")
	plot1.grid(True, color='#99bbee', linestyle='solid', linewidth=0.5)
	plot1.set_xlim( xrange[0],xrange[1])
	plot1.set_ylim( Lrange[0],Lrange[1])
	yy = np.empty(xx.size)
	for i,x in enumerate(xx):
		yy[i] = frit.LfromX(x)
	plot1.plot(xx,yy, '-k', linewidth=0.75)
	fig.savefig('Schröder_'+xname+'.eps',  format='eps', pad_inches=0.02) 
	#fig.show()
	#plot1.close()



PlotSchroder("Schröder’s Function, Symmetry-Based", "wide", 
	[-1000, 4000],  [0.0, 1.0], printsize)

PlotSchroder("Schröder’s Function, Main Step", "main", 
	[-5, 21],  [0.0, 1.0], printsize)

	
PlotSchroder("Schröder’s Function, Detail", "1515", 
	[ 15.18, 15.23],  [0.05738, 0.05754], printsize)


