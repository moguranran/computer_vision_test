#!/usr/bin/python
# -*- coding: utf-8 -*-

from PIL import Image
from numpy import *
from pylab import *
import sift
import warp

featname = ['Univ'+str(i+1)+'.sift' for i in range(5)]
imname = ['Univ'+str(i+1)+'.jpg' for i in range(5)]
l = {}
d = {}
for i in range(5):
  sift.process_image(imname[i],featname[i])
  l[i],d[i] = sift.read_features_from_file(featname[i])
  l[i][:,[0,1]] = l[i][:,[1,0]] # x,y --> row,col

matches = {}
for i in range(4):
  matches[i] = sift.match(d[i+1],d[i])

import homography

# 対応点を同次座標の点に変換する関数
def convert_points(j): 
  ndx = matches[j].nonzero()[0]
  fp = homography.make_homog(l[j+1][ndx,:2].T)
  ndx2 = [int(matches[j][i]) for i in ndx]
  tp = homography.make_homog(l[j][ndx2,:2].T)
  return fp,tp

# ホモグラフィーを推定
model = homography.RansacModel()

fp,tp = convert_points(1)
H_12 = homography.H_from_ransac(fp,tp,model)[0] #画像1から2へ

fp,tp = convert_points(0)
H_01 = homography.H_from_ransac(fp,tp,model)[0] #画像0から1へ

tp,fp = convert_points(2) #注意: 順番が逆転
H_32 = homography.H_from_ransac(fp,tp,model)[0] #画像3から2へ

tp,fp = convert_points(3) #注意: 順番が逆転
#H_43 = homography.H_from_ransac(fp,tp,model,match_threshold=3000)[0] #画像4から3へ
H_43 = homography.H_from_ransac(fp,tp,model)[0] #画像4から3へ

# 画像を変形する
im1 = array(Image.open(imname[1]))
delta = im1.shape[1] # 領域追加と水平移動量

im2 = array(Image.open(imname[2]))
im_12 = warp.panorama(H_12,im1,im2,delta,delta)

im1 = array(Image.open(imname[0]))
im_02 = warp.panorama(dot(H_12,H_01),im1,im_12,delta,delta)

im1 = array(Image.open(imname[3]))
im_32 = warp.panorama(H_32,im1,im_02,delta,delta)

im1 = array(Image.open(imname[4]))
im_42 = warp.panorama(dot(H_32,H_43),im1,im_32,delta,2*delta)

imshow(uint8(im_42))
axis('off')
show()
