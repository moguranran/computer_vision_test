#!/usr/bin/python
# -*- coding: utf-8 -*-

from pylab import *
import lktrack
imnames = ['viff.000.ppm', 'viff.001.ppm',
           'viff.002.ppm', 'viff.003.ppm', 'viff.004.ppm']

# LKTrackerのジェネレータを使って追跡する
lkt = lktrack.LKTracker(imnames)
for im,ft in lkt.track():
  print 'tracking %d features' % len(ft)

  # 軌跡を描画する
  figure()
  imshow(im)
  for p in ft:
    plot(p[0],p[1],'bo')
  for t in lkt.tracks:
    plot([p[0] for p in t],[p[1] for p in t])
  axis('off')
  show()
