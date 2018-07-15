# Plot the Szekeres Polynomials for the paper


import sys
sys.path.append('../py')

import numpy as np
import matplotlib.pyplot as pp
import friterexp_szek as frit


tightview = False

width=6.0    # inches
height=5.5
if tightview:
	urange=(-0.5, 0.5)
	yrange=(-0.12, 0.12)
	filename = 'szekpoly_tight.eps'
else:
	urange=(-1.0, 1.0)
	yrange=(-0.5, 1.05)
	filename = 'szekpoly.eps'

uvisual_step_inches = 0.025
nstep = width/uvisual_step_inches  # ignores space used for y scale, margins
ustep = (urange[1]-urange[0])/nstep
uu = np.arange(urange[0], urange[1], ustep)

pp.title("Szekeres Polynomials")
pp.xlabel('u')
pp.ylabel('S_n(u)')
pp.xlim(urange[0],urange[1])
pp.ylim(yrange[0],yrange[1])
pp.grid(True)
pp.legend([]) # does this clear out existing crud from previous execution? No.
pp.legend(None) # does this clear out existing crud from previous execution? No.
pp.legend(loc='best', shadow=True )
for i,sp in enumerate(frit.szekpolys):
		pp.plot(uu, np.polyval(sp, uu/2), '-', label=i, linewidth=0.2)

#pp.show()
pp.savefig(filename, format='eps', dpi=600)

