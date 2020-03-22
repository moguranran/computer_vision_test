#!/usr/bin/python
# -*- coding: utf-8 -*-

from numpy import *

class KnnClassifier(object):

  def __init__(self,labels,samples):
    """ 教師データを使って分類器を初期化する """

    self.labels = labels
    self.samples = samples

  def classify(self,point,k=3):
    """ pointを教師データ中のk個の最近傍を使って分類し、
        ラベルを返す """

    # 全教師データへの距離を計算する
    dist = array([L2dist(point,s) for s in self.samples])

    # ソートする
    ndx = dist.argsort()

    # k個の最近傍を保持するのに辞書を用いる
    votes = {}
    for i in range(k):
      label = self.labels[ndx[i]]
      votes.setdefault(label,0)
      votes[label] += 1

    return max(votes, key=lambda x: votes.get(x))

def L2dist(p1,p2):
  return sqrt( sum( (p1-p2)**2) )
