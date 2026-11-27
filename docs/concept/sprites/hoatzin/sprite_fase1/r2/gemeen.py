import numpy as np
from PIL import Image
H=44
PAL=[(152,208,160),   # 0 transparant
 (16,16,20),          # 1 omlijning
 (36,38,42),(54,57,62),(76,80,86),(100,104,110),   # 2-5 zwartig dons (kop iets lichter in het model)
 (82,78,46),(122,114,66),                          # 6-7 gelige tinten (alleen in het dons)
 (126,128,134),(150,152,158),(176,178,184),        # 8-10 grijs: snavel, kale vleugels, poten (5 = schaduw)
 (228,228,228)]                                    # 11 oogglans
P=np.array(PAL,float)
def nearest(c):
    c=np.asarray(c,float); chroma=(c[0]-c[2])
    best=None
    for i in range(1,len(PAL)):
        p=P[i]; d=((p-c)**2).sum()+ 6*((p[0]-p[2])-chroma)**2
        if best is None or d<best[0]: best=(d,i)
    return best[1]
def save(idx,fn,canvas=64):
    h,w=idx.shape; can=np.zeros((canvas,canvas),np.uint8)
    ox=(canvas-w)//2; can[canvas-h:canvas,ox:ox+w]=idx
    im=Image.fromarray(can,'P'); pal=sum(PAL,())+(0,)*(768-3*len(PAL)); im.putpalette(pal); im.save(fn,transparency=0); return can
def rgba(can):
    a=np.zeros(can.shape+(4,),np.uint8); a[...,:3]=P[can]; a[...,3]=np.where(can>0,255,0); return a
