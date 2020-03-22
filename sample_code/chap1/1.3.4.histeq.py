#!/usr/bin/python
# -*- coding: utf-8 -*-

from PIL import Image
from numpy import *
import imtools

#im = array(Image.open('AquaTermi_lowcontrast.jpg').convert('L'))
im = array(Image.open('empire.jpg').convert('L'))
im2,cdf = imtools.histeq(im)

from pylab import *

for i in (im, im2):
  figure()
  gray()
  axis('off')
  imshow(i)

  figure()
  hist(i.flatten(),128)

figure()
plot(cdf)
show()


