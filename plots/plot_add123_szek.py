# Plot exp_u(x) for Szekeres definition

import sys
sys.path.append('../py')

import numpy as np
import matplotlib.pyplot as pp

import friterexp_sym as fritsym
import friterexp_szek as fritszek


width=6.0    # inches
height=6.0
printsize = (width,height)


def PlotOneSubplot(subplot, frit, xrange, nxpoints, yrange, uvalue, ulabel, addvalues):
	"""
	"""
	xx = np.linspace(xrange[0], xrange[1], num=nxpoints)
	subplot.set_title("x op[%s] n" % (ulabel,) )
	subplot.set_xlim(xx[0],xx[-1])
	subplot.set_ylim(yrange[0],yrange[1])
	subplot.grid(True, color="#a4c8e6", linestyle='solid', linewidth=0.3)
	for n,ycolor in reversed(addvalues):
		logn = n #frit.iterexp(-uvalue, n)
		yy = np.empty(xx.shape)
		for i in range(len(xx)):
		  yy[i] = frit.iterexp(uvalue, frit.iterexp(-uvalue, xx[i]) + logn )
		subplot.plot(xx, yy, "-", color=ycolor, label=str(n))


def PlotCollectionAddOneTwoThree(title, frit, ulist, addvalues):
	"""
	   Make figure of six plots showing generalized arithmetic operator for 
	   different values of order of iteration
	"""
	fig = pp.figure( figsize=printsize )
	nxpoints = 907
	fig.suptitle = "TEST SUP TITLE"  #title
	plotspots = [231,232,233,234,235,236]
	for i,(uvalue,ulabel,xrange,yrange) in enumerate(ulist):
	    print('making sub-plot for u=%g'  % (uvalue,)	
		PlotOneSubplot( fig.add_subplot(plotspots[i]), frit, xrange, nxpoints, yrange, uvalue,ulabel, addvalues)
	#pp.show() 
	fig.savefig(title+".eps", format='eps', pad_inches=0.02)


addvalues = [
    # value to "add", color
	[ -2, "#6688ee" ],
	[ -1, "#66aacc" ],
	[  0, "#000000" ],
	[  1, "#ee6688" ],
	[  2, "#dd9966" ],
	[  3, "#bbaa66" ],	
]

ulist1 = [
   # uvalue, text in [],   x range,  y range
	[ -2.0, '-2', (-4, 3),  (-4, 2)],
	[ -1.0, '-1', (-4, 5),  (-3, 6) ],
	[  0.0, '0', (-2, 6), (-2, 8) ],
	[  1.0, '1', (-1, 5), (-1, 10) ],
	[  2.0, '2', (0, 5), (0, 140) ],
	[  3.0, '3', (2, 6), (0, 300) ],
]


ulist2 = [
   # uvalue, text in [],   x range,  y range
	[ -0.125, '-1/8', (-5, 5), (-4, 8) ],
	[  0.125, '1/8', (-3, 6), (-3,  9) ],
	[  0.25, '1/4', (-2, 6),  (-2, 10) ],
	[  0.50, '1/2', (-2, 7),  (-1, 14) ],
	[  0.75, '3/4', (-2, 7),  (-1, 15) ],
	[  1.25, '5/4', (-2, 7),  (-1, 30) ],
]



PlotCollectionAddOneTwoThree("Integer-Order Generalized Arith Operators", fritszek, ulist1, addvalues )
PlotCollectionAddOneTwoThree("Szekeres Fractional Order Operators", fritszek, ulist2, addvalues )
PlotCollectionAddOneTwoThree("Symmetry-Based Operators", fritsym, ulist2, addvalues )

#pp.close()

