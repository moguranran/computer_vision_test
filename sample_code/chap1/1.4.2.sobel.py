#!/usr/bin/python
# -*- coding: utf-8 -*-

from PIL import Image
from numpy import *
from scipy.ndimage import filters

im = array(Image.open('empire.jpg').convert('L'))

# Sobel微分係数フィルタ
imx = zeros(im.shape)
filters.sobel(im,1,imx)

imy = zeros(im.shape)
filters.sobel(im,0,imy)

magnitude = sqrt(imx**2+imy**2)

from pylab import *

for i in (im, imx, imy, magnitude):
  figure()
  axis('off')
  gray()
  imshow(i)

show()

pim = Image.fromarray(uint8(magnitude))
pim.save("magnitude.png")

