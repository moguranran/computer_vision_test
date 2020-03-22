#!/usr/bin/python
# -*- coding: utf-8 -*-

from PIL import Image
from numpy import *
from scipy.ndimage import measurements,morphology

# 画像を読み込み、閾値処理で2値化する
im = array(Image.open('houses.png').convert('L')) 
im = 1*(im<128) 

labels, nbr_objects = measurements.label(im) 
print "Number of objects:", nbr_objects

from pylab import *

for i in (im, labels):
  figure()
  gray()
  axis('off')
  imshow(i)
show()
