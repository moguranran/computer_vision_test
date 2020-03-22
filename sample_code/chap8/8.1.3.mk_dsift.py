#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
d = 'test'
imlist = [os.path.join(d,f) for f in os.listdir(d) if f.endswith('.ppm')]
d = 'train'
imlist += [os.path.join(d,f) for f in os.listdir(d) if f.endswith('.ppm')]

print imlist

import dsift

# 画像を固定サイズ（50×50）で処理する
for filename in imlist:
  featfile = filename[:-3]+'dsift'
  dsift.process_image_dsift(filename,featfile,10,5,resize=(50,50))
