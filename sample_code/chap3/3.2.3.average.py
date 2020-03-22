#!/usr/bin/python
# -*- coding: utf-8 -*-

from pylab import *
import imtools

for dir in ('jkfaces2008_small', 'jkfaces2008_small/aligned'):
  imlist = imtools.get_imlist(dir)
  avgimg = imtools.compute_average(sorted(imlist)[:150])
  figure()
  imshow(avgimg)
  gray()
  axis('off')
  title(dir)

show()
