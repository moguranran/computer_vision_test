#!/usr/bin/python
# -*- coding: utf-8 -*-

from PIL import Image
from numpy import *
from imtools import imresize

def compute_feature(im):
  """ OCRの画像パッチの特徴量ベクトルを返す"""

  # 縮小して、境界を削除する
  norm_im = imresize(im,(30,30))
  norm_im = norm_im[3:-3,3:-3]

  return norm_im.flatten()

def load_ocr_data(path):
  """ パスの中のすべての画像について、ラベルとOCR特徴量を返す """

  # .jpgで終わるすべてのファイルのリストを作る
  imlist = [os.path.join(path,f) for f in os.listdir(path) if f.endswith('.jpg')]
  # ラベルを作る
  labels = [int(imfile.split('/')[-1][0]) for imfile in imlist]

  # 画像から特徴量を生成する
  features = []
  for imname in imlist:
    im = array(Image.open(imname).convert('L'))
    features.append(compute_feature(im))
  return array(features),labels

from svmutil import *

# 教師データ
features,labels = load_ocr_data('sudoku_images/ocr_data/training/')

# テストデータ
test_features,test_labels = load_ocr_data('sudoku_images/ocr_data/testing/')

# 線形SVM分類器を学習させる
features = map(list,features)
test_features = map(list,test_features)

prob = svm_problem(labels,features)
param = svm_parameter('-t 0')

m = svm_train(prob,param)

# 学習はうまくいったかな？
res = svm_predict(labels,features,m)

# テストデータセットについてはどうかな？
res = svm_predict(test_labels,test_features,m)

from scipy.ndimage import measurements

def find_sudoku_edges(im,axis=0):
  """ 位置合わせをした数独画像からマスのエッジを見つける """

  # 2値化して行または列方向に足し合わせる
  trim = 1*(im<128)
  s = trim.sum(axis=axis)

  # 太線の中心を見つける
  s_labels,s_nbr = measurements.label(s>(0.5*max(s)))
  m = measurements.center_of_mass(s,s_labels,range(1,s_nbr+1))
  x = [int(x[0]) for x in m]

  # 太線だけしか見つからなかったら、間の線を補う
  if len(x)==4:
    dx = diff(x)
    x = [x[0],x[0]+dx[0]/3,x[0]+2*dx[0]/3,
         x[1],x[1]+dx[1]/3,x[1]+2*dx[1]/3,
         x[2],x[2]+dx[2]/3,x[2]+2*dx[2]/3,x[3]]

  if len(x)==10:
    return x
  else:
    raise RuntimeError('Edges not detected.')

imname = 'sudoku_images/sudokus/sudoku18.JPG'
vername = 'sudoku_images/sudokus/sudoku18.sud'
im = array(Image.open(imname).convert('L'))

# マスのエッジを検出する
x = find_sudoku_edges(im,axis=0)
y = find_sudoku_edges(im,axis=1)

# マスを切り出して分類する
crops = []
for col in range(9):
  for row in range(9):
    crop = im[y[col]:y[col+1],x[row]:x[row+1]]
    crops.append(compute_feature(crop))

res = svm_predict(loadtxt(vername),map(list,crops),m)[0]
res_im = array(res).reshape(9,9)

print 'Result:'
print res_im
