#!/usr/bin/python
# -*- coding: utf-8 -*-

from PIL import Image
from pylab import *
import ncut
from scipy.misc import imresize

im = array(Image.open('C-uniform03.ppm'))
m,n = im.shape[:2]

# 画像サイズを(wid,wid)に縮小する
wid = 50
rim = imresize(im,(wid,wid),interp='bilinear')
rim = array(rim,'f')

# 正規化カット行列を作成する
A = ncut.ncut_graph_matrix(rim,sigma_d=1,sigma_g=1e-2)

# クラスタリング
code,V = ncut.cluster(A,k=3,ndim=3)

# 元の画像サイズに戻す
codeim = imresize(code.reshape(wid,wid),(m,n),interp='nearest')

# 結果を描画する
figure()
imshow(codeim)
gray()
axis('off')

figure()
for i in range(4):
  subplot(1,4,i+1)
  imshow(imresize(V[i].reshape(wid,wid),(m,n),interp='bilinear'))
  gray()
  axis('off')

show()
