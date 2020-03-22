#!/usr/bin/python
# -*- coding: utf-8 -*-

from PIL import Image
from pylab import *
import imtools
import pickle
from scipy.cluster.vq import *

# 画像のリストを得る
imlist = imtools.get_imlist('selected_fontimages/')
imnbr = len(imlist)

# モデルのファイルを読み込む
with open('font_pca_modes.pkl','rb') as f:
  immean = pickle.load(f)
  V = pickle.load(f)

# 平板化した画像を格納する行列を作る
immatrix = array([array(Image.open(im)).flatten()
                  for im in imlist],'f')

# 第40主成分までを射影する
immean = immean.flatten()
projected = array([dot(V[:40],immatrix[i]-immean)
                   for i in range(imnbr)])

# k平均法
projected = whiten(projected)
centroids,distortion = kmeans(projected,4)

code,distance = vq(projected,centroids)

# クラスタを描画する
for k in range(4):
  ind = where(code==k)[0]
  figure()
  gray()
  for i in range(minimum(len(ind),40)):
    subplot(4,10,i+1)
    imshow(immatrix[ind[i]].reshape((25,25)))
    axis('off')
show()


