#!/usr/bin/python
# -*- coding: utf-8 -*-

from PIL import Image
from numpy import *
from pylab import *
import sift
import imtools

imlist = imtools.get_imlist('panoramio')
featlist = []
for imname in imlist:
  sname = imname+'.sift'
  sift.process_image(imname,sname)
  featlist.append(sname)

nbr_images = len(imlist)

matchscores = zeros((nbr_images,nbr_images))

for i in range(nbr_images):
  for j in range(i,nbr_images): # 上三角成分だけを計算する
    print 'comparing ', imlist[i], imlist[j]

    l1,d1 = sift.read_features_from_file(featlist[i])
    l2,d2 = sift.read_features_from_file(featlist[j])

    matches = sift.match_twosided(d1,d2)

    nbr_matches = sum(matches > 0)
    print 'number of matches = ', nbr_matches
    matchscores[i,j] = nbr_matches 

# 値をコピーする
for i in range(nbr_images): 
  for j in range(i+1,nbr_images): # 対角成分はコピー不要
    matchscores[j,i] = matchscores[i,j]

print matchscores
import pickle
with open('panoramio_matchscores.pkl','w') as f:
  pickle.dump(nbr_images,f)
  pickle.dump(imlist,f)
  pickle.dump(matchscores,f)




