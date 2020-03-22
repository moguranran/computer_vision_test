#!/usr/bin/python
# -*- coding: utf-8 -*-

from pylab import *
import pickle
import sift
import imagesearch
import homography

# 画像リストとボキャブラリを読み込む
with open('ukbench_imlist.pkl','rb') as f:
  imlist = pickle.load(f)
  featlist = pickle.load(f)

nbr_images = len(imlist)

with open('vocabulary.pkl', 'rb') as f:
  voc = pickle.load(f)

src = imagesearch.Searcher('test.db',voc)

# クエリ画像の番号と、検索結果の個数
q_ind = 38
nbr_results = 20

# 通常の検索
res_reg = [w[1] for w in src.query(imlist[q_ind])[:nbr_results]]
print 'top matches (regular):', res_reg

# クエリ画像の特徴量を読み込む
q_locs,q_descr = sift.read_features_from_file(featlist[q_ind])
q_locs[:,[0,1]] = q_locs[:,[1,0]]
fp = homography.make_homog(q_locs[:,:2].T)

# ホモグラフィーの対応付け用のRANSACモデル
model = homography.RansacModel()
rank = {}

# 検索結果の画像特徴量を読み込む
for ndx in res_reg[1:]:
  locs,descr = sift.read_features_from_file(featlist[ndx-1])
  locs[:,[0,1]] = locs[:,[1,0]]

  # 一致度を調べる
  matches = sift.match(q_descr,descr)
  ind = matches.nonzero()[0]
  ind2 = matches[ind]
  tp = homography.make_homog(locs[:,:2].T)

  # ホモグラフィーを計算し、インライアを数える。
  # 一致度が足りなければ空リストを返す。
  try:
    H,inliers = homography.H_from_ransac(fp[:,ind],tp[:,ind2],
                                         model,match_theshold=4)
  except:
    inliers = []

  # インライアの数を格納する
  rank[ndx] = len(inliers)

# 最もモデルに当てはまるものが先頭になるよう辞書をソートする
sorted_rank = sorted(rank.items(), key=lambda t: t[1], reverse=True)
res_geom = [res_reg[0]]+[s[0] for s in sorted_rank]
print 'top matches (homography):', res_geom

# 検索結果を描画する
imagesearch.plot_results(src,res_reg[:8])
imagesearch.plot_results(src,res_geom[:8])
