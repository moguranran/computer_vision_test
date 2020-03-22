#!/usr/bin/python
# -*- coding: utf-8 -*-

from pylab import *

import pickle
import bayes
import imtools

# Pickleを使って2Dの点を読み込む
with open('points_ring.pkl', 'r') as f:
  class_1 = pickle.load(f)
  class_2 = pickle.load(f)
  labels = pickle.load(f)

# ベイズ分類器を学習させる
bc = bayes.BayesClassifier()
bc.train([class_1,class_2],[1,-1])

# Pickleを使ってテストデータを読み込む
with open('points_ring_test.pkl', 'r') as f:
  class_1 = pickle.load(f)
  class_2 = pickle.load(f)
  labels = pickle.load(f)

# いくつかの点についてテストする
print bc.classify(class_1[:10])[0]

# 点と判別境界を表示する
def classify0(x,y,bc=bc):
  points = vstack((x,y))
  return bc.classify(points.T)[0]

imtools.plot_2D_boundary([-6,6,-6,6],[class_1,class_2],classify0,[1,-1])
show()
