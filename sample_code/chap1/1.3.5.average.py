#!/usr/bin/python
# -*- coding: utf-8 -*-

from pylab import *
import imtools

imlist = imtools.get_imlist('a_thumbs')

avgimg = imtools.compute_average(imlist)

imshow(avgimg)
gray()
axis('off')
show()
