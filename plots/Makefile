# Makefile to run Python scripts to make plots for the iterated exponentials paper


all:  szekpoly.eps


# Create .png files suitable for web pages, coffee mugs from EPS by using ImageMagick's Convert
%.png: %.eps
	convert -density 300  $<  $@


szekpoly.eps:
	
