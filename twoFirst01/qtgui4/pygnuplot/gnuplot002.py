#!/usr/bin/env python
from numpy import *
import Gnuplot, Gnuplot.funcutils

gp = Gnuplot.Gnuplot()
gp('set surface')
gp('set contour surface')
gp('set view 60,30,1,1')
gp('set clabel "%8.2f"')
gp('set key right')
gp('set xlabel "vss"')
gp('set ylabel "closs"')
gp('set zlabel "closs"')
gp('set term png')
gp('set terminal png size 1280,1000')
gp('set style data lines')
gp('set output "demo.png"')
gp.title('3D plot demo')
gp.splot('"data.txt" using')