#!/usr/bin/python
# -*- coding: utf-8 -*-

from numpy import *
import os, sift
import bayes

def read_gesture_features_labels(path):
  # .dsiftで終わるすべてのファイル名のリストを作る
  featlist = [os.path.join(path,f) for f in os.listdir(path)
              if f.endswith('.dsift')]

  # 特徴量を読み込む
  features = []
  for featfile in featlist:
    l,d = sift.read_features_from_file(featfile)
    features.append(d.flatten())
  features = array(features)

  # ラベルを生成する
  labels = [featfile.split('/')[-1][0] for featfile in featlist]

  return features,array(labels)

def print_confusion(res,test_labels,classnames):

  n = len(classnames)

  # 混同行列
  class_ind = dict([(classnames[i],i) for i in range(n)])

  confuse = zeros((n,n))
  for i in range(len(test_labels)):
    confuse[class_ind[res[i]],class_ind[test_labels[i]]] += 1

  print 'Confusion matrix for'
  print classnames
  print confuse

features,labels = read_gesture_features_labels('train/') 

test_features,test_labels = read_gesture_features_labels('test/')

classnames = unique(labels)

import pca

V,S,m = pca.pca(features)

# 最も重要な次元を残す
V = V[:50]
features = array([dot(V,f-m) for f in features])
test_features = array([dot(V,f-m) for f in test_features])

# ベイズ分類器を試す
bc = bayes.BayesClassifier()
blist = [features[where(labels==c)[0]] for c in classnames]

bc.train(blist,classnames)
res = bc.classify(test_features)[0]

acc = sum(1.0*(res==test_labels)) / len(test_labels)
print 'Accuracy:', acc

print_confusion(res,test_labels,classnames)

