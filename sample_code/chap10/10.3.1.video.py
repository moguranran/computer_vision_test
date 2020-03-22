#!/usr/bin/python
# -*- coding: utf-8 -*-

import cv2

# 動画キャプチャを準備する
#cap = cv2.VideoCapture(0)
cap = cv2.VideoCapture('test.avi')

while True:
  ret,im = cap.read()
  cv2.imshow('video test',im)
  key = cv2.waitKey(10)
  if key == 27:
    break
  if key == ord(' '):
    cv2.imwrite('vid_result.jpg',im)
