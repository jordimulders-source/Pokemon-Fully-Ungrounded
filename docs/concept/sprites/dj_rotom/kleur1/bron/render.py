"""Tekstraster -> dj_rotom.png + zoom met rooster (8x) in scratch."""
import sys, numpy as np
sys.path.insert(0,'/home/user/Pokemon-Fully-Ungrounded/tools/concept/sprites')
from ascii_sprite import parse
from PIL import Image, ImageDraw
from palet import COLS
a=parse('dj_rotom.txt')[0]
im=Image.fromarray(a.astype('uint8'),'P'); p=[]
for c in COLS: p+=list(c)
im.putpalette(p+[0]*(768-len(p))); im.save('../dj_rotom.png',transparency=0)
if len(sys.argv)>1:
    Z=12; y0,y1=16,64
    rgb=Image.new('RGB',(64,64),(255,255,255)); m=Image.fromarray(((a>0)*255).astype('uint8'))
    rgb.paste(im.convert('RGB'),(0,0),m)
    b=rgb.crop((0,y0,64,y1)).resize((64*Z,(y1-y0)*Z),Image.NEAREST); d=ImageDraw.Draw(b)
    for x in range(0,65,5): d.line([(x*Z,0),(x*Z,b.size[1])],fill=(200,0,200))
    for y in range(y0,y1+1):
        if y%5==0: d.line([(0,(y-y0)*Z),(b.size[0],(y-y0)*Z)],fill=(200,0,200))
    big=Image.new('RGB',(b.size[0]+64*3+10,b.size[1]),(255,255,255)); big.paste(b,(0,0))
    big.paste(rgb.crop((0,y0,64,y1)),(b.size[0]+5,0))
    big.paste(rgb.crop((0,y0,64,y1)).resize((128,(y1-y0)*2),Image.NEAREST),(b.size[0]+5,60))
    big.save(sys.argv[1])
