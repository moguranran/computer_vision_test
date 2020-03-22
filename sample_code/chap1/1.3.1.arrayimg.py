#!/usr/bin/python
# -*- coding: utf-8 -*-

from numpy import *
from PIL import Image

im = array(Image.open('empire.jpg')) 
print im.shape, im.dtype

im = array(Image.open('empire.jpg').convert('L'),'f')
print im.shape, im.dtype
