
from PIL import Image
from pylab import *

im = array(Image.open('turningtorso1.jpg').convert('L'))

figure()
imshow(im)
gray()
x = ginput(30,timeout=0)
savetxt('turningtorso1_points.txt',x,'%i')


