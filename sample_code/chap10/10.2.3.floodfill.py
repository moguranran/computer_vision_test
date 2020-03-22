#!/usr/bin/python
# -*- coding: utf-8 -*-

from numpy import *
import cv2

# 画像を読み込む
filename = 'fisherman.jpg'
im = cv2.imread(filename)
h,w = im.shape[:2]

# 塗りつぶしの例
diff = (6,6,6)
mask = zeros((h+2,w+2),uint8)
cv2.floodFill(im,mask,(10,10),(255,255,0),diff,diff)

# OpenCVのウィンドウに結果を表示する
cv2.imshow('flood fill',im)
cv2.waitKey()

# 結果を保存する
cv2.imwrite('result.jpg',im)

