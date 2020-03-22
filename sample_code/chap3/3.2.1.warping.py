#!/usr/bin/python
# -*- coding: utf-8 -*-

from PIL import Image
from pylab import *
import warp

# im1からim2へアフィン変換で変形する例
im1 = array(Image.open('cat.jpg').convert('L'))
im2 = array(Image.open('billboard_for_rent.jpg').convert('L'))

# 点を設定する
tp = array([[264,538,540,264],[40,36,605,605],[1,1,1,1]])
#tp = array([[675,826,826,677],[55,52,281,277],[1,1,1,1]])

im3 = warp.image_in_image(im1,im2,tp)

figure()
gray()
imshow(im3)
axis('equal')
axis('off')
show()
