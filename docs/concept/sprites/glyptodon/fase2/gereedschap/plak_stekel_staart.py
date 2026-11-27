import sys
from PIL import Image
import numpy as np
base=np.array(Image.open('r3_1_zonder_keuze.png').convert('RGB')).astype(int)
src=np.array(Image.open('r3_3_Y_A.png').convert('RGB')).astype(int)
W=np.array([255,255,255]); BL=(20,16,14)
nw=lambda a: a.sum(2)<720
out=base.copy()
reg=out[530:720,835:1024]; reg[nw(reg)]=W
t=src[400:780,805:1000]; m=nw(t)
for y,x in zip(*np.where(m)):
    X=805+x+25
    if X<1024: out[400+y-40,X]=t[y,x]
# stekel in blokken van G px
G=10; cx,top,bot=int(sys.argv[1]),int(sys.argv[2]),int(sys.argv[3])
a,f=float(sys.argv[4]),float(sys.argv[5])
pal=[(138,119,109),(101,82,72),(76,63,56),(53,45,39)]
rows=range(top//G,bot//G+1)
cells={}
for gy in rows:
    tt=(gy*G-top)/(bot-top); hw=a*tt+f*tt**5
    l,r=int((cx-hw)//G),int((cx+hw)//G)
    for gx in range(l,r+1):
        u=(gx-l)/max(1,r-l)
        cells[(gx,gy)]=pal[0] if u<.3 else pal[1] if u<.6 else pal[2] if u<.85 else pal[3]
def paint(gx,gy,c): out[gy*G:(gy+1)*G,gx*G:(gx+1)*G]=c
for (gx,gy),c in cells.items(): paint(gx,gy,c)
# omlijning: buurcellen die wit zijn
for (gx,gy) in list(cells):
    for ex,ey in [(1,0),(-1,0),(0,-1)]:
        n=(gx+ex,gy+ey)
        if n in cells: continue
        blk=out[n[1]*G:(n[1]+1)*G,n[0]*G:(n[0]+1)*G]
        if blk.mean()>200: paint(n[0],n[1],BL)
Image.fromarray(out.astype('uint8')).save(sys.argv[6])
