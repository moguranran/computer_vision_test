#!/usr/bin/python
# -*- coding: utf-8 -*-

import lktrack

imnames = ['bt.003.pgm', 'bt.002.pgm', 'bt.001.pgm', 'bt.000.pgm']

# 追跡オブジェクトを生成する
lkt = lktrack.LKTracker(imnames)

# 最初のフレームで特徴点を検出し、残りで追跡する
lkt.detect_points()
lkt.draw()
for i in range(len(imnames)-1):
  lkt.track_points()
  lkt.draw()
