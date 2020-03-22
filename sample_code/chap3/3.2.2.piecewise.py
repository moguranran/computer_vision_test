#!/usr/bin/python
# -*- coding: utf-8 -*-

from PIL import Image
from pylab import *
import homography
import warp

# 変形する画像を開く
fromim = array(Image.open('sunset_tree.jpg')) 
x,y = meshgrid(range(5),range(6)) 
x = (fromim.shape[1]/4) * x.flatten() 
y = (fromim.shape[0]/5) * y.flatten() 

# 三角形分割する
tri = warp.triangulate_points(x, y)

# 対象の画像と点を開く
im = array(Image.open('turningtorso1.jpg')) 
tp = loadtxt('turningtorso1_points.txt') # 対応点

# 点を同次座標に変換する
fp = vstack((y,x,ones((1,len(x)))))
tp = vstack((tp[:,1],tp[:,0],ones((1,len(tp)))))

figure() 
imshow(im)
plot(tp[1],tp[0],'*')
axis('off') 

figure() 
imshow(fromim)
warp.plot_mesh(x,y,tri)
axis('off') 

# 三角形を変形する
im = warp.pw_affine(fromim,im,fp,tp,tri) 

# 描画する
figure() 
imshow(im) 
axis('off') 

figure() 
imshow(im) 
warp.plot_mesh(tp[1],tp[0],tri) 
axis('off') 

show()
