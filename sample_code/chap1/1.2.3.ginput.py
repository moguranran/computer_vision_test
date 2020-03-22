#!/usr/bin/python
# -*- coding: utf-8 -*-

from PIL import Image
from pylab import *

im = array(Image.open('empire.jpg'))
imshow(im)
print '3点クリックしてください'
x = ginput(3)
print 'クリックした座標:',x
show()
