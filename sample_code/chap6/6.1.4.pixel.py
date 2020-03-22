#!/usr/bin/python
# -*- coding: utf-8 -*-

from PIL import Image
from pylab import *

from scipy.cluster.vq import *
from scipy.misc import imresize

steps = 100 # 画像は steps*steps の領域に分割される
im = array(Image.open('empire.jpg'))
#im = array(Image.open('boy_on_hill.jpg'))

dx = im.shape[0] / steps
dy = im.shape[1] / steps

# 各領域の色特徴量を計算する
features = []
for x in range(steps):
  for y in range(steps):
    R = mean(im[x*dx:(x+1)*dx,y*dy:(y+1)*dy,0])
    G = mean(im[x*dx:(x+1)*dx,y*dy:(y+1)*dy,1])
    B = mean(im[x*dx:(x+1)*dx,y*dy:(y+1)*dy,2])
    features.append([R,G,B])
features = array(features,'f') # 配列に入れる

# クラスタリング
centroids,variance = kmeans(features,3)
code,distance = vq(features,centroids)

# クラスタのラベルを使って画像を生成する
codeim = code.reshape(steps,steps)
codeim = imresize(codeim,im.shape[:2],interp='nearest')

figure()
gray()
axis('off')
imshow(codeim)
show()
