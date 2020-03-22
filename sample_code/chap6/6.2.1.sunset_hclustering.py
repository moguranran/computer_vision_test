#!/usr/bin/python
# -*- coding: utf-8 -*-

from PIL import Image 
from pylab import *
import os
import hcluster

# 画像のリストを作成する
path = 'flickr-sunsets/'
imlist = [os.path.join(path,f) for f in os.listdir(path)
          if f.endswith('.jpg')]

# 特徴量ベクトルを抽出する（色チャンネルに8つのビン）
features = zeros([len(imlist), 512])
for i,f in enumerate(imlist):
  im = array(Image.open(f))

  # 多次元ヒストグラム
  h,edges = histogramdd(im.reshape(-1,3),8,normed=True,
                        range=[(0,255),(0,255),(0,255)])
  features[i] = h.flatten()

tree = hcluster.hcluster(features)

hcluster.draw_dendrogram(tree,imlist,filename='sunset.pdf')

# 任意の閾値についてクラスタを可視化する
clusters = tree.extract_clusters(0.23*tree.distance)

# 3要素以上のクラスタの画像を描画する
for c in clusters:
  elements = c.get_cluster_elements()
  nbr_elements = len(elements)
  if nbr_elements>3:
    figure()
    for p in range(minimum(nbr_elements,20)):
      subplot(4,5,p+1)
      im = array(Image.open(imlist[elements[p]]))
      imshow(im)
      axis('off')
show()

