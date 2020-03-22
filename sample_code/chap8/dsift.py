#!/usr/bin/python
# -*- coding: utf-8 -*-

from PIL import Image
from numpy import *
import os
import sift

def process_image_dsift(imagename,resultname,size=20,steps=10,
                        force_orientation=False,resize=None):
  """ 画像から密なSIFT記述子を抽出し、結果をファイルに保存する。
      オプション：特徴量のサイズ、グリッドの間隔、方向記述子の計算の指定
      （Falseならすべて上向き）、画像のリサイズ用のタプル """

  im = Image.open(imagename).convert('L')
  if resize!=None:
    im = im.resize(resize)
  m,n = im.size

  if imagename[-3:] != 'pgm':
    # pgmファイルを作成
    im.save('tmp.pgm')
    imagename = 'tmp.pgm'

  # フレームを作成して一時ファイルに保存する
  scale = size/3.0
  x,y = meshgrid(range(steps,m,steps),range(steps,n,steps))
  xx,yy = x.flatten(),y.flatten()
  frame = array([xx,yy,scale*ones(xx.shape[0]),zeros(xx.shape[0])])
  savetxt('tmp.frame',frame.T,fmt='%03.3f')

  if force_orientation:
    cmmd = str("sift "+imagename+" --output="+resultname+
              " --read-frames=tmp.frame --orientations")
  else:
    cmmd = str("sift "+imagename+" --output="+resultname+
              " --read-frames=tmp.frame")
  os.system(cmmd)
  print 'processed', imagename, 'to', resultname
