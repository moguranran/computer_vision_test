#!/usr/bin/python
# -*- coding: utf-8 -*-

from PIL import Image
from pylab import *
import imtools
import pickle
from scipy.cluster.vq import *

# 画像のリストを得る
imlist = imtools.get_imlist('selected_fontimages/')
imnbr = len(imlist)

# モデルのファイルを読み込む
with open('font_pca_modes.pkl','rb') as f:
  immean = pickle.load(f)
  V = pickle.load(f)

# 平板化した画像を格納する行列を作る
immatrix = array([array(Image.open(im)).flatten()
                  for im in imlist],'f')

immean = immean.flatten()

# 第1,2主成分を射影する
projected = array([dot(V[[0,1]],immatrix[i]-immean) 
                   for i in range(imnbr)])
# 第2,3主成分を射影する
#projected = array([dot(V[[1,2]],immatrix[i]-immean) 
#                   for i in range(imnbr)])
# 第1,3主成分を射影する
#projected = array([dot(V[[0,2]],immatrix[i]-immean) 
#                   for i in range(imnbr)])

# k平均法
projected = whiten(projected)
centroids,distortion = kmeans(projected,4)

code,distance = vq(projected,centroids)


from PIL import Image, ImageDraw

# 高さと幅
h,w = 1200,1200

# 白の背景で新しい画像を生成する
img = Image.new('RGB',(w,h),(255,255,255))
draw = ImageDraw.Draw(img)

# 軸を描画する
draw.line((0,h/2,w,h/2),fill=(255,0,0))
draw.line((w/2,0,w/2,h),fill=(255,0,0))

# 軸のスケールを調整する
scale = abs(projected).max(0)
scaled = floor(array([ (p / scale) * (w/2-20,h/2-20) +
                       (w/2,h/2) for p in projected]))

# 各画像のサムネイルを貼り付ける
for i in range(imnbr):
  nodeim = Image.open(imlist[i])
  nodeim.thumbnail((25,25))
  ns = nodeim.size
  img.paste(nodeim,(int(scaled[i][0]-ns[0]//2),int(scaled[i][1]-ns[1]//2),
    int(scaled[i][0]+ns[0]//2)+1,int(scaled[i][1]+ns[1]//2)+1))

img.save('pca_font.jpg')

figure()
imshow(array(img))
axis('off')
show()
