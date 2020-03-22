#!/usr/bin/python
# -*- coding: utf-8 -*-

from PIL import Image
from numpy import *
from pylab import *
import sift

#imname1 = 'crans_1_small.jpg'
#imname2 = 'crans_2_small.jpg'
imname1 = 'sf_view1.jpg'
imname2 = 'sf_view2.jpg'
#imname1 = 'climbing_1_small.jpg'
#imname2 = 'climbing_2_small.jpg'

im1 = array(Image.open(imname1).convert('L')) 
im2 = array(Image.open(imname2).convert('L')) 

sift.process_image(imname1,imname1 + '.sift')
l1,d1 = sift.read_features_from_file(imname1 + '.sift')

sift.process_image(imname2,imname2 + '.sift')
l2,d2 = sift.read_features_from_file(imname2 + '.sift')

print 'starting matching'
#matches = sift.match(d1,d2)
matches = sift.match_twosided(d1,d2)

figure()
gray()
sift.plot_matches(im1,im2,l1,l2,matches)
show()
