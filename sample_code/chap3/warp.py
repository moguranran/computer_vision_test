#!/usr/bin/python
# -*- coding: utf-8 -*-

import homography
from numpy import *
from scipy import ndimage
from pylab import *

def image_in_image(im1,im2,tp):
  """ 四隅をできるだけtpに近づけるアフィン変換を使ってim1をim2に埋め込む。
     tpは同次座標で、左上から逆時計回りにとる """

  # 元の座標
  m,n = im1.shape[:2]
  fp = array([[0,m,m,0],[0,0,n,n],[1,1,1,1]])

  # アフィン変換を計算し適用する
  H = homography.Haffine_from_points(tp,fp)
  im1_t = ndimage.affine_transform(im1,H[:2,:2],
          (H[0,2],H[1,2]),im2.shape[:2])
  alpha = (im1_t > 0)

  return (1-alpha)*im2 + alpha*im1_t

def alpha_for_triangle(points,m,n):
  """ pointsで定義された頂点（正規化された同次座標系）
      を持つ三角形について、サイズ(m,n)の透明度マップを作成する。"""

  alpha = zeros((m,n))
  for i in range(min(points[0]),max(points[0])):
    for j in range(min(points[1]),max(points[1])):
      x = linalg.solve(points,[i,j,1])
      if min(x) > 0: # すべての係数が正の数
        alpha[i,j] = 1
  return alpha

import matplotlib.delaunay as md

def triangulate_points(x,y): 
  """ 2Dの点のドロネー三角形分割 """
  centers,edges,tri,neighbors = md.delaunay(x,y)
  return tri

def pw_affine(fromim,toim,fp,tp,tri):
  """ 画像の三角形パッチを変形する。
      fromim = 変形する画像
      toim = 画像の合成先
      fp = 基準点（同次座標系）
      tp = 対応点（同次座標系）
      tri = 三角形分割 """

  im = toim.copy()

  # 画像がグレースケールかカラーか調べる
  is_color = len(fromim.shape) == 3

  # 変形する先の画像を作成する
  im_t = zeros(im.shape, 'uint8')

  for t in tri:
    # アフィン変換を計算する
    H = homography.Haffine_from_points(tp[:,t],fp[:,t])
    if is_color:
      for col in range(fromim.shape[2]):
        im_t[:,:,col] = ndimage.affine_transform(
          fromim[:,:,col],H[:2,:2],(H[0,2],H[1,2]),im.shape[:2])
    else:
      im_t = ndimage.affine_transform(
        fromim,H[:2,:2],(H[0,2],H[1,2]),im.shape[:2])

    # 三角形の透明度マップ
    alpha = alpha_for_triangle(tp[:,t].astype('int'),im.shape[0],im.shape[1])

    # 三角形を画像に追加する
    im[alpha>0] = im_t[alpha>0]

  return im

def plot_mesh(x,y,tri):
  """ 三角形を描画する """

  for t in tri:
    t_ext = [t[0], t[1], t[2], t[0]] # 最初の点を最後に追加する
    plot(x[t_ext],y[t_ext],'r')


def panorama(H,fromim,toim,padding=2400,delta=2400):
  """ ホモグラフィー行列H（RANSACで推定するのが望ましい）を用いて、
      2つの画像を合成して水平方向のパノラマを作成する。
      出力画像はtoimと同じ高さ。'padding'は横に追加する画素数。
      'delta'は水平移動量 """

  # 画像がグレースケールかカラーかを調べる
  is_color = len(fromim.shape) == 3

  # geometric_transform()に必要な同次変換
  def transf(p):
    p2 = dot(H,[p[0],p[1],1])
    return (p2[0]/p2[2],p2[1]/p2[2])

  if H[1,2]<0: # fromim が右側なら
    print 'warp - right'
    # fromimを変形
    if is_color:
      # 出力画像の右側に0の領域を追加する
      toim_t = hstack((toim,zeros((toim.shape[0],padding,3))))
      fromim_t = zeros((toim.shape[0],toim.shape[1]+padding,toim.shape[2]))
      for col in range(3):
        fromim_t[:,:,col] = ndimage.geometric_transform(fromim[:,:,col],
             transf,(toim.shape[0],toim.shape[1]+padding))
    else:
     # 出力画像の右側に0の領域を追加する
      toim_t = hstack((toim,zeros((toim.shape[0],padding))))
      fromim_t = ndimage.geometric_transform(fromim,transf,
                    (toim.shape[0],toim.shape[1]+padding))
  else:
    print 'warp - left'
    # 左側に領域を追加するために水平移動する
    H_delta = array([[1,0,0],[0,1,-delta],[0,0,1]])
    H = dot(H,H_delta)
    # fromimを変形
    if is_color:
      # 出力画像の左側に0の領域を追加する
      toim_t = hstack((zeros((toim.shape[0],padding,3)),toim))
      fromim_t = zeros((toim.shape[0],toim.shape[1]+padding,toim.shape[2]))
      for col in range(3):
        fromim_t[:,:,col] = ndimage.geometric_transform(fromim[:,:,col],
               transf,(toim.shape[0],toim.shape[1]+padding))
    else:
      # 出力画像の左側に0の領域を追加する
      toim_t = hstack((zeros((toim.shape[0],padding)),toim))
      fromim_t = ndimage.geometric_transform(fromim,transf,
                     (toim.shape[0],toim.shape[1]+padding))

  # 画像を合成して返す（toimにfromimを重ねる）
  if is_color:
    # 非0の全ピクセル
    alpha = ((fromim_t[:,:,0] + fromim_t[:,:,1] + fromim_t[:,:,2] ) > 0)
    for col in range(3):
      toim_t[:,:,col] = fromim_t[:,:,col]*alpha + toim_t[:,:,col]*(1-alpha)
  else:
    alpha = (fromim_t > 0)
    toim_t = fromim_t*alpha + toim_t*(1-alpha)

  return toim_t
