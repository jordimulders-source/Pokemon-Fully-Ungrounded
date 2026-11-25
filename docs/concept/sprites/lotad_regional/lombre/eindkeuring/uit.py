# Opslaan + snelle preview (12x) voor e1.py
import numpy as np; from PIL import Image
def opslaan(s,pal,pad):
    im=Image.fromarray(s.astype('uint8'),'P'); im.putpalette([int(v) for v in pal.ravel()]+[0]*(768-48))
    im.save(pad,transparency=0); return im
def rgb(s,pal,bg=(200,200,200)):
    a=pal[s].astype('uint8'); a[s==0]=bg; return a
def preview(s,pal,s0,pal0,pad,Z=12,box=(8,20,56,64)):
    x0,y0,x1,y1=box
    A=Image.fromarray(rgb(s0,pal0)[y0:y1,x0:x1]).resize(((x1-x0)*Z,(y1-y0)*Z),Image.NEAREST)
    B=Image.fromarray(rgb(s,pal)[y0:y1,x0:x1]).resize(((x1-x0)*Z,(y1-y0)*Z),Image.NEAREST)
    W=Image.new('RGB',(A.width*2+10,A.height),(255,255,255)); W.paste(A,(0,0)); W.paste(B,(A.width+10,0)); W.save(pad)
