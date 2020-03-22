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

import hcluster
tree = hcluster.hcluster(projected) 
hcluster.draw_dendrogram(tree,imlist,filename='fonts.jpg')



