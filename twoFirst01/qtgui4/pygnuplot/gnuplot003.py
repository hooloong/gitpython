#!/usr/bin/env python
import Gnuplot

gp = Gnuplot.Gnuplot()
gp('set title "sin(x) and cos(x)"')
gp('set terminal png size 2560,1600')
gp('set xlabel "x-axis: from -2*pi to +2*pi"')
gp('set ylabel "y-axis: from -1 to +1"')
gp('set terminal png')
gp('set output "sincos.png"')
gp('set xrange [-2*pi:2*pi]')
gp('set xtics ("0" 0,"-270" -(3/2)*pi, "-180" -pi, "-90" -pi/2, "90" pi/2, "180" pi, "270" (3/2)*pi)')
gp('set ytics ("0" 0, "0.5" 0.5, "1" 1, "-0.5" -0.5, "-1" -1)')
gp('set grid')
gf = Gnuplot.Func('sin(x), cos(x)')
gp.plot(gf)
