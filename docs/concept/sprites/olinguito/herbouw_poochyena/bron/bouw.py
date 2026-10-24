# Bouwt anim_front.png (64x128, 2 frames, 16 kleuren, index 0 = transparant) uit raster_f1/f2.txt.
import sys
from PIL import Image
sys.path.insert(0,'.')
from render import load, toimg
import render
render.loadpal('../normal.pal')
f1=toimg(load('raster_f1.txt')); f2=toimg(load('raster_f2.txt'))
im=Image.new('P',(64,128),0); im.putpalette([c for t in render.PAL for c in t])
im.paste(f1,(0,0)); im.paste(f2,(0,64))
im.save('../anim_front.png',transparency=0)
print('px f1:',sum(1 for y in range(64) for x in range(64) if f1.getpixel((x,y))))
