#!/usr/bin/python
# -*- coding: utf-8 -*-

from pylab import *
import camera

# 点群を読み込む
points = loadtxt('house.p3d').T
points = vstack((points,ones(points.shape[1])))

# カメラを設定する
P = hstack((eye(3),array([[0],[0],[-10]]))) 
cam = camera.Camera(P) 
x = cam.project(points)

# 射影を描画する
figure() 
plot(x[0],x[1],'k.') 
show()

from numpy import random
# 変換行列を作る
r = 0.05*random.rand(3)
rot = camera.rotation_matrix(r)

# カメラを回転して射影する
figure() 
for t in range(20): 
  cam.P = dot(cam.P,rot)
  x = cam.project(points)
  plot(x[0],x[1],'k.')
show()
