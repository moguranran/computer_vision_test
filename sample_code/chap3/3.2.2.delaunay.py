#!/usr/bin/python
# -*- coding: utf-8 -*-

from pylab import *
from numpy import random
import matplotlib.delaunay as md

x,y = array(random.standard_normal((2,100)))
centers,edges,tri,neighbors = md.delaunay(x,y)

figure()
for t in tri:
  t_ext = [t[0], t[1], t[2], t[0]] # 第1の点を最後に追加する
  plot(x[t_ext],y[t_ext],'r')

plot(x,y,'*')
axis('off')
show()
