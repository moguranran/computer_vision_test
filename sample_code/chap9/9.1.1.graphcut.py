#!/usr/bin/python
# -*- coding: utf-8 -*-

from PIL import Image
from pylab import *
from scipy.misc import imresize
import graphcut

im = array(Image.open('empire.jpg'))
im = imresize(im,0.07,interp='bilinear')
size = im.shape[:2]

# 2つの長方形の教師データ領域を追加する
labels = zeros(size)
labels[3:18,3:18] = -1
labels[-18:-3,-18:-3] = 1

# グラフを作成する
g = graphcut.build_bayes_graph(im,labels,kappa=1)

# グラフをカットする
res = graphcut.cut_graph(g,size)

figure()
graphcut.show_labeling(im,labels)

figure()
imshow(res)
gray()
axis('off')

show()
