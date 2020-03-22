#!/usr/bin/python
# -*- coding: utf-8 -*-

from PIL import Image
from pylab import *

from scipy import ndimage
import homography

imname = 'sudoku_images/sudokus/sudoku8.JPG'
im = array(Image.open(imname).convert('L'))

# 4隅を入力する
figure()
imshow(im)
gray()
x = ginput(4)

# 左上、右上、右下、左下
fp = array([array([p[1],p[0],1]) for p in x]).T
tp = array([[0,0,1],[0,1000,1],[1000,1000,1],[1000,0,1]]).T

# ホモグラフィーを推定する
H = homography.H_from_points(tp,fp)

# geometric_transform用のヘルパー関数
def warpfcn(x):
  x = array([x[0],x[1],1])
  xt = dot(H,x)
  xt = xt/xt[2]
  return xt[0],xt[1]

# 射影変換を使って画像を変形する
im_g = ndimage.geometric_transform(im,warpfcn,(1000,1000))

figure()
imshow(im_g)
axis('off')
gray()
show()

