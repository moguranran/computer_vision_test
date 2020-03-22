#!/usr/bin/python
# -*- coding: utf-8 -*-

from PIL import Image
from pylab import *
import warp
import homography
from scipy import ndimage

# im1からim2へアフィン変換で変形する例
im1 = array(Image.open('cat.jpg').convert('L'))
im2 = array(Image.open('blank_billboard.jpg').convert('L'))

# 点を設定する
tp = array([[143,353,302,50],[100,30,980,922],[1,1,1,1]])

im3 = warp.image_in_image(im1,im2,tp)

figure()
gray()
imshow(im3)
axis('equal')
axis('off')

# im1の四隅の座標を設定する
m,n = im1.shape[:2] 
fp = array([[0,m,m,0],[0,0,n,n],[1,1,1,1]]) 

# 第1の三角形
tp2 = tp[:,:3] 
fp2 = fp[:,:3] 

# H を計算する
H = homography.Haffine_from_points(tp2,fp2) 
im1_t = ndimage.affine_transform(im1,H[:2,:2], 
          (H[0,2],H[1,2]),im2.shape[:2]) 

# 三角形の透明度マップ
alpha = warp.alpha_for_triangle(tp2,im2.shape[0],im2.shape[1]) 
im3 = (1-alpha)*im2 + alpha*im1_t 

# 第2の三角形
tp2 = tp[:,[0,2,3]]
fp2 = fp[:,[0,2,3]]

# H を計算する
H = homography.Haffine_from_points(tp2,fp2) 
im1_t = ndimage.affine_transform(im1,H[:2,:2],
          (H[0,2],H[1,2]),im2.shape[:2])

# 三角形の透明度マップ
alpha = warp.alpha_for_triangle(tp2,im2.shape[0],im2.shape[1]) 
im4 = (1-alpha)*im3 + alpha*im1_t

figure()
gray()
imshow(im4)
axis('equal')
axis('off')
show()


