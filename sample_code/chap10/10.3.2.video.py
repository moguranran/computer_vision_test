#!/usr/bin/python
# -*- coding: utf-8 -*-

from numpy import *
import cv2

# 動画キャプチャを準備する
cap = cv2.VideoCapture(0)

frames = []
# フレームを取得して配列に格納する
while True:
  ret,im = cap.read()
  cv2.imshow('video',im)
  frames.append(im)
  if cv2.waitKey(10) == 27:
    break
frames = array(frames)

# サイズを調べる
print im.shape
print frames.shape
