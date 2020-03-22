#!/usr/bin/python
# -*- coding: utf-8 -*-

import cv2

# 画像を読み込む
im = cv2.imread('fisherman.jpg')
gray = cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)

# 積分画像を計算する
intim = cv2.integral(gray)

# 正規化して保存する
intim = (255.0*intim) / intim.max()
cv2.imwrite('result.jpg',intim)
