#!/usr/bin/python
# -*- coding: utf-8 -*-

import pickle
import os

with open('panoramio_matchscores.pkl','r') as f:
  nbr_images = pickle.load(f)
  imlist = pickle.load(f)
  matchscores = pickle.load(f)

path = os.path.abspath('.') + '/'

from PIL import Image
import pydot

threshold = 2 # リンクを作成するのに必要な一致数

g = pydot.Dot(graph_type='graph') # デフォルトの方向付きグラフは不要
for i in range(nbr_images):
  for j in range(i+1,nbr_images):
    if matchscores[i,j] > threshold:
      # 組のうちの第1の画像
      im = Image.open(imlist[i])
      im.thumbnail((100,100))
      filename = str(i)+'.png'
      im.save(filename) # サムネイルをファイルに保存
      g.add_node(pydot.Node(str(i),fontcolor='transparent', 
            shape='rectangle',image=path+filename))

      # 組のうちの第2の画像
      im = Image.open(imlist[j])
      im.thumbnail((100,100))
      filename = str(j)+'.png'
      im.save(filename) # サムネイルをファイルに保存
      g.add_node(pydot.Node(str(j),fontcolor='transparent', 
             shape='rectangle',image=path+filename)) 

      g.add_edge(pydot.Edge(str(i),str(j)))

g.write_png('whitehouse.png')
