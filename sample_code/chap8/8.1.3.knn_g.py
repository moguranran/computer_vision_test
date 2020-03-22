#!/usr/bin/python
# -*- coding: utf-8 -*-

from numpy import *
import os, sift
import knn

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

# k近傍法を試す
k = 1
knn_classifier = knn.KnnClassifier(labels,features)
res = array([knn_classifier.classify(test_features[i],k) for i in
             range(len(test_labels))])

# 精度
acc = sum(1.0*(res==test_labels)) / len(test_labels)
print 'Accuracy:', acc


print_confusion(res,test_labels,classnames)
