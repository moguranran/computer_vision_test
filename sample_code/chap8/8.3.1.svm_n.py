#!/usr/bin/python
# -*- coding: utf-8 -*-

from numpy import *
from pylab import *
import pickle
from svmutil import *
import imtools

# Pickleを用いて2Dの点を読み込む
with open('points_normal.pkl', 'r') as f:
  class_1 = pickle.load(f)
  class_2 = pickle.load(f)
  labels = pickle.load(f)

# libsvm用にリストに変換する
class_1 = map(list,class_1)
class_2 = map(list,class_2)
labels = list(labels)
samples = class_1+class_2 # 2つのリストを連結する

# SVMを生成する
prob = svm_problem(labels,samples)
param = svm_parameter('-t 2')

# データを使ってSVMを学習させる
m = svm_train(prob,param)

# 学習はうまくいったかな？
res = svm_predict(labels,samples,m)

# Pickleを用いてテストデータを読み込む
with open('points_normal_test.pkl', 'r') as f:
  class_1 = pickle.load(f)
  class_2 = pickle.load(f)
  labels = pickle.load(f)

# libsvm用にリストに変換する
class_1 = map(list,class_1)
class_2 = map(list,class_2)

# 描画用の関数を定義する
def predict(x,y,model=m):
  return array(svm_predict([0]*len(x),zip(x,y),model)[0])

# 分類境界を描画する
imtools.plot_2D_boundary([-6,6,-6,6],[array(class_1),array(class_2)],
                         predict,[1,-1])
show()
