#!/usr/bin/python
# -*- coding: utf-8 -*-

from numpy import * 
from numpy import random 
from scipy.ndimage import filters 
import rof 

# ノイズを含む画像を合成する
im = zeros((500,500)) 
im[100:400,100:400] = 128 
im[200:300,200:300] = 255 
im = im + 30*random.standard_normal((500,500)) 

U,T = rof.denoise(im,im) 
G = filters.gaussian_filter(im,10) 

# 結果を保存する
from scipy.misc import imsave 
imsave('synth_rof.pdf',U) 
imsave('synth_gaussian.pdf',G)
imsave('synth_original.pdf',im)

from pylab import *
titles = ('original','gaussian','ROF')
for i,j in enumerate((im,G,U)):
  subplot(1,3,i+1)
  title(titles[i])
  gray()
  axis('off')
  imshow(j)
show()
