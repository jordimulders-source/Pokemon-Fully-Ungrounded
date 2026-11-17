# Sprite als tekstraster <-> png (zelfde tekens als ../sprite_r2/print.py)
import numpy as np; from PIL import Image
CH='.#drpPgGhHwWoyYs'
def lees(p): return np.asarray(Image.open(p)).astype(int)
def tekst(o,x0,y0,x1,y1): return ['%2d '%y+''.join(CH[o[y,x]] for x in range(x0,x1)) for y in range(y0,y1)]
def zet_rijen(o,x0,rijen):
    """rijen: {y: 'tekens vanaf x0'} ; spatie = ongewijzigd"""
    for y,s in rijen.items():
        for i,c in enumerate(s):
            if c!=' ': o[y,x0+i]=CH.index(c)
def schrijf(o,pal,p):
    im=Image.fromarray(o.astype('uint8'),'P'); im.putpalette(pal); im.save(p,transparency=0)
