import sys; from PIL import Image; import numpy as np
from pal import PAL
def png(g,out):
    im=Image.fromarray(np.array(g,'uint8'),'P'); im.putpalette([c for p in PAL for c in p]); im.save(out,transparency=0); return im
def rgba(g):
    P=np.array(PAL,'uint8'); g=np.array(g); a=np.dstack([P[g],np.where(g==0,0,255).astype('uint8')]); return Image.fromarray(a,'RGBA')
def zij(g,out,z=8,box=None):
    m=Image.open('../../model/model.png').convert('RGB'); S=968/62
    sp=rgba(g); bg=Image.new('RGBA',sp.size,(255,255,255,255)); sp=Image.alpha_composite(bg,sp).convert('RGB')
    if box is None: box=(0,0,64,64)
    x0,y0,x1,y1=box
    A=sp.crop(box).resize(((x1-x0)*z,(y1-y0)*z),Image.NEAREST)
    mb=(24+(x0-1)*S,1+(y0-4)*S,24+(x1-1)*S,1+(y1-4)*S)
    mw=Image.new('RGB',(1400,1400),'white'); mw.paste(m,(200,200)); B=mw.crop(tuple(int(v)+200 for v in mb)).resize(A.size,Image.LANCZOS)
    c=Image.new('RGB',(A.width*2+8,A.height),(255,255,255)); c.paste(A,(0,0)); c.paste(B,(A.width+8,0)); c.save(out)
