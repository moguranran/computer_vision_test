#!/usr/bin/python
# -*- coding: utf-8 -*-

from numpy import *
import cv2

# 画像読み込み
im = cv2.imread('empire.jpg')

# ダウンサンプリング
im_lowres = cv2.pyrDown(im)

# グレースケールに変換
gray = cv2.cvtColor(im_lowres,cv2.COLOR_BGR2GRAY)

# 特徴点を検出
s = cv2.SURF()
mask = uint8(ones(gray.shape))
keypoints = s.detect(gray,mask)

# 画像と点を表示
vis = cv2.cvtColor(gray,cv2.COLOR_GRAY2BGR)

for k in keypoints[::10]:
  cv2.circle(vis,(int(k.pt[0]),int(k.pt[1])),2,(0,255,0),-1)
  cv2.circle(vis,(int(k.pt[0]),int(k.pt[1])),int(k.size),(0,255,0),2)

cv2.imshow('local descriptors',vis)
cv2.waitKey()
