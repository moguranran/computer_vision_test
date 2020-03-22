#!/usr/bin/python
# -*- coding: utf-8 -*-

from PIL import Image
from numpy import *
from scipy.ndimage import measurements,morphology

# 画像を読み込み、閾値処理で2値化する
im = array(Image.open('houses.png').convert('L')) 
im = 1*(im<128) 

# モルフォロジー  物体を分離する
im_open = morphology.binary_opening(im,ones((9,5)),iterations=2) 

labels_open, nbr_objects_open = measurements.label(im_open) 
print "Number of objects:", nbr_objects_open

from pylab import *

for i in (im_open, labels_open):
  figure()
  gray()
  axis('off')
  imshow(i)
show()
