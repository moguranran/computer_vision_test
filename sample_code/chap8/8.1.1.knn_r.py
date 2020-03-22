#!/usr/bin/python
# -*- coding: utf-8 -*-
from PIL import Image
from numpy import *
from pylab import *
import pickle
import knn
import imtools

# Pickleを使って2D点を読み込む
with open('points_ring.pkl', 'r') as f:
  class_1 = pickle.load(f)
  class_2 = pickle.load(f)
  labels = pickle.load(f)

  model = knn.KnnClassifier(labels,vstack((class_1,class_2)))

# Pickleを使ってデータを読み込む
with open('points_ring_test.pkl', 'r') as f:
  class_1 = pickle.load(f)
  class_2 = pickle.load(f)
  labels = pickle.load(f)

# 最初の点についてテストする
print model.classify(class_1[0])

# 描画用関数の定義
def classify(x,y,model=model):
  return array([model.classify([xx,yy]) for (xx,yy) in zip(x,y)])

# 分類の境界を描画する
imtools.plot_2D_boundary([-6,6,-6,6],[class_1,class_2],classify,[1,-1])
show()
