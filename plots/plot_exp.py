# Plot exp_u(x) for Szekeres definition


import sys
sys.path.append('../py')

import numpy as np
import matplotlib.pyplot as pp

# pick what to plot:
want = 'szek'

if want=='szek':
	import friterexp_szek as frit
	fritex = frit.iterexp
	numpoints = 331
	titletext = "Szekeres' Fractionally Iterated Exponentials"
	filename = "plot_exp_szek.eps"
elif want=='sym':
	import friterexp_sym as frit
	fritex = frit.iterexp
	numpoints = 931
	titletext = "Symmetry-based Fractionally Iterated Exponentials"
	filename = "plot_exp_sym.eps"
else:
	print('???')
	


width=6.0    # inches
height=6.0

xrange = [-4.0, 4.0]
yrange = [ -5, 12]

xx = np.linspace(xrange[0],xrange[1], num=numpoints)


ulist = [
	(-1.25,  "-5/4",         "#bbaaff"),
	(-1.0,   "-1 y=log(x)",  "#000000"),
	(-0.75,  "-3/4",         "#99bbff"),
	(-0.5,   "-1/2",         "#6688e4"),
	(-0.25,  "-1/4",         "#aaccbb"),
	( 0.0,   " 0 y=x",       "#000000"),
	( 0.25,  " 1/4",         "#ccccaa"),
	( 0.5,   " 1/2",         "#ccaa99"),
	( 0.75,  " 3/4",         "#ffccbb"),
	( 1.0,   " 1 y=exp(x)",  "#000000"),
	( 1.25,  " 1/4",         "#eebbaa"),
	( 1.5,   " 1/2",         "#f488aa"),
]


fig = pp.figure( figsize=(width,height) )
plot1 = fig.add_subplot(111)   
plot1.set_title(titletext)
plot1.set_xlabel("x")
plot1.set_ylabel("exp_u(x)")
plot1.grid(True, color='#aaccee', linestyle='solid', linewidth=0.3)
plot1.set_xlim( xrange[0],xrange[1])
plot1.set_ylim( yrange[0],yrange[1])

for uvalue, ulabel, ucolor in reversed(ulist):
	yy = fritex(uvalue, xx)
	# avoid graphics trouble at logarithm's singularity
	# (should do so for other u<0 cases, but -inf happens to fall between xx[] samples)
	if uvalue== -1.0:
		yy[0:numpoints//2+1] = float('-inf')
	plot1.plot(xx,yy, '-', label=ulabel, color=ucolor, linewidth=0.75)

plot1.legend(loc="upper left")

fig.savefig(filename, format='eps', pad_inches=0.02) 
#pp.show()
#plot1.close()

