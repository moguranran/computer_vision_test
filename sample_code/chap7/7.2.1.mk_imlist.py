import pickle
import imtools
import os

imlist = sorted(imtools.get_imlist('first1000'))
nbr_images = len(imlist)
featlist = [imlist[i][:-3]+'sift' for i in range(nbr_images)]

with open('ukbench_imlist.pkl','wb') as f:
  pickle.dump(imlist,f)
  pickle.dump(featlist,f)

with open('webimlist.txt','w') as f:
  for i in imlist:
    f.write(i)
    f.write('\n')
