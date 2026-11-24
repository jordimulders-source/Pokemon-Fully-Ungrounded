# overlay tintgrenzen in het lijf: lijn tussen twee buurpixels met verschillende vultint (2,3,5,10,6-vlak), 12x
import sys,numpy as np; from PIL import Image, ImageDraw
def overlay(p,x0=13,y0=39,x1=52,y1=61,z=12):
    im=Image.open(p); a=np.array(im); im.info['transparency']=0
    v=im.convert('RGBA').crop((x0,y0,x1,y1)).resize(((x1-x0)*z,(y1-y0)*z),Image.NEAREST); d=ImageDraw.Draw(v)
    T=(2,3,5,10)
    for y in range(y0,y1):
        for x in range(x0,x1):
            if a[y,x] not in T: continue
            if x+1<x1 and a[y,x+1] in T and a[y,x+1]!=a[y,x]: X=(x+1-x0)*z; d.line([(X,(y-y0)*z),(X,(y+1-y0)*z)],fill=(0,200,255),width=3)
            if y+1<y1 and a[y+1,x] in T and a[y+1,x]!=a[y,x]: Y=(y+1-y0)*z; d.line([((x-x0)*z,Y),((x+1-x0)*z,Y)],fill=(0,200,255),width=3)
    return v
