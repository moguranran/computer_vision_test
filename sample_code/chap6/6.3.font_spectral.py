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

n = len(projected)

# 距離行列を計算する
S = array([[ sqrt(sum((projected[i]-projected[j])**2))
          for i in range(n) ] for j in range(n)], 'f')

# ラプラシアン行列を作成する
rowsum = sum(S,axis=0)
D = diag(1 / sqrt(rowsum))
I = identity(n)
L = I - dot(D,dot(S,D))

# Lの固有ベクトルを計算する
U,sigma,V = linalg.svd(L)

k = 5
# 最初のk個の固有ベクトルを列として並べて
# 特徴量ベクトルを作成する
features = array(V[:k]).T

# k-means
features = whiten(features)
centroids,distortion = kmeans(features,k)
code,distance = vq(features,centroids)

# クラスタを描画する
for c in range(k):
  ind = where(code==c)[0]
  figure()
  for i in range(minimum(len(ind),39)):
    im = Image.open(imlist[ind[i]])
    subplot(4,10,i+1)
    gray()
    imshow(array(im))
    axis('equal')
    axis('off')
show()
