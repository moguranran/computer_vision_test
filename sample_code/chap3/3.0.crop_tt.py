import shutil
from PIL import Image

fn = 'turningtorso1.jpg'
shutil.copyfile(fn, fn + '.org')
src = Image.open(fn)
dst = src.crop((900,508,1325,1384))
dst.save(fn)


