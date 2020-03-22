#!/usr/bin/python
# -*- coding: utf-8 -*-

from PIL import Image
from numpy import *

im = array(Image.open('empire.jpg').convert('L'))

im2 = 255 - im # 画像を反転する

im3 = (100.0/255) * im + 100 # 100〜200の値に縮める

im4 = 255.0 * (im/255.0)**2  # 2乗する

from pylab import *

for i in (im,im2,im3,im4):
  figure()
  gray()
  axis('off')
  imshow(i)
  print int(i.min()), int(i.max())

show()
