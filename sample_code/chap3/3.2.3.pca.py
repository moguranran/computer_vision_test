#!/usr/bin/python
# -*- coding: utf-8 -*-

from PIL import Image, ImageDraw
from numpy import *
from pylab import *
import pca
import imtools

imlist = imtools.get_imlist('jkfaces2008_small')
#imlist = imtools.get_imlist('jkfaces2008_small/aligned')

imlist = sorted(imlist)

im = array(Image.open(imlist[0]).convert('L')) # サイズを得るため画像を1つ開く
m,n = im.shape[0:2] # 画像のサイズを得る
imnbr = len(imlist) # 画像数の得る

maskim = Image.new('L',(n,m))
draw = ImageDraw.Draw(maskim)
draw.ellipse((90,100,230,286),fill=1)
#draw.ellipse((40,82,180,268),fill=1) # 位置合わせ済み画像用
mask = array(maskim).flatten()

# すべての平板化画像を格納する行列を作る
immatrix = array([mask*array(Image.open(imlist[i]).convert('L')).flatten() 
                  for i in range(150)],'f') 

# 主成分分析を実行する
V,S,immean = pca.pca(immatrix) 

# 画像を表示する（平均と、最初の7つの主成分）
figure() 
gray() 
subplot(2,4,1) 
imshow(immean.reshape(m,n)) 
axis('off')
for i in range(7):
  subplot(2,4,i+2)
  imshow(V[i].reshape(m,n))
  axis('off')

show()

