#!/usr/bin/python
# -*- coding: utf-8 -*-

from PIL import Image
from numpy import *
from scipy.ndimage import filters

im = array(Image.open('empire.jpg').convert('L'))

sigma = 5 # 標準偏差

imx = zeros(im.shape)
filters.gaussian_filter(im, (sigma,sigma), (0,1), imx)

imy = zeros(im.shape)
filters.gaussian_filter(im, (sigma,sigma), (1,0), imy)

magnitude = sqrt(imx**2+imy**2)

from pylab import *

figure()
for j, i in enumerate((im, imx, imy, magnitude)):
  subplot(1,4,j+1)
  axis('off')
  gray()
  imshow(i)

show()

