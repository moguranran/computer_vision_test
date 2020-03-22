#!/usr/bin/python
# -*- coding: utf-8 -*-

import cv2

# 画像を読み込む
im = cv2.imread('empire.jpg')
h,w = im.shape[:2]
print h,w

# 画像を保存する
cv2.imwrite('result.png',im)

# グレースケール版を作成する
gray = cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)

# 画像を保存する
cv2.imwrite('resultgray.png',gray)


