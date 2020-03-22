#!/usr/bin/python
# -*- coding: utf-8 -*-

from PIL import Image
from pylab import *

# 配列に画像を読み込む
im = array(Image.open('empire.jpg'))

# 画像を表示する
imshow(im)

# 点の座標
x = [100,100,400,400] 
y = [200,500,200,500] 

# 赤い星マークで点を描画する
plot(x,y,'r*') 

# 最初の2点間に線を描画する
plot(x[:2],y[:2]) 

# タイトルを追加し、描画結果を表示する
title('Plotting: "empire.jpg"') 
axis('off')
show()




