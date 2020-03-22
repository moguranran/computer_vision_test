#!/usr/bin/python
# -*- coding: utf-8 -*-

from PIL import Image
from pylab import *
from scipy.misc import imresize
import graphcut

def create_msr_labels(m,lasso=False):
  """ ユーザーの注釈情報から教師ラベル行列を作成する """

  labels = zeros(im.shape[:2])

  # 背景
  labels[m==0] = -1
  labels[m==64] = -1

  # 前景
  if lasso:
    labels[m==255] = 1
  else:
    labels[m==128] = 1

  return labels

# 画像と、注釈情報マップを読み込む
im = array(Image.open('376043.jpg'))
m = array(Image.open('376043.bmp'))

# 縮小する
scale = 0.1
im = imresize(im,scale,interp='bilinear')
m = imresize(m,scale,interp='nearest')

# 教師ラベルを作成する
labels = create_msr_labels(m,False)

# 注釈情報からグラフを構築する
g = graphcut.build_bayes_graph(im,labels,kappa=2)

# グラフをカットする
res = graphcut.cut_graph(g,im.shape[:2])

# 背景の部分を削除する
res[m==0] = 1
res[m==64] = 1

# 結果を描画する
figure()
imshow(res)
gray()
xticks([])
yticks([])
savefig('labelplot.pdf')
