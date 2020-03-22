#!/usr/bin/python
# -*- coding: utf-8 -*-

from PIL import Image
from numpy import *

import rof

im = array(Image.open('ceramic-houses_t0.png').convert('L'))
#im = array(Image.open('flower32_t0.png').convert('L'))
U,T = rof.denoise(im,im,tolerance=0.001)
t = 0.4 # 閾値 for ceramic-houses_t0.png
#t = 0.7 # 閾値 for flower32_t0.png

#import scipy.misc
#scipy.misc.imsave('result.pdf',U < t*U.max())
seg = U < t*U.max()

from pylab import *
figure()
gray()
subplot(1,3,1)
axis('off')
imshow(im)
subplot(1,3,2)
axis('off')
imshow(U)
subplot(1,3,3)
axis('off')
imshow(seg)
show()
