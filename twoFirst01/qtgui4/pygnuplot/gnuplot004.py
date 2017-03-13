#!/usr/bin/env python
import Gnuplot

gp = Gnuplot.Gnuplot()
gp('set title "x^2 and 1/x^2"')
gp('set xlabel "x-axis: from -10 to +10"')
gp('set ylabel "y-axis: from 0 to 100"')
gp('set terminal png')
gp('set terminal png size 1280,800')
gp('set output "xx.png"')
gp('set xrange [-10:10]')
gf = Gnuplot.Func('x*x, 1/(x*x) with filledcurves fs')
gp.plot(gf)
