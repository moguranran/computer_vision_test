#!/usr/bin/python
# -*- coding: utf-8 -*-

from PIL import Image
from pylab import *

# 画像を配列に読み込む
im = array(Image.open('empire.jpg').convert('L'))

# 新しい図を作成する
figure()
# 色を使わない
gray()
# 左上隅を原点とする等高線を表示する
contour(im, origin='image')
axis('equal')
axis('off')

figure()
hist(im.flatten(),128)
show()
