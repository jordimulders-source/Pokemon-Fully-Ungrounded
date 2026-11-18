"""Onderlaag voor een icoon (NOOIT het eindresultaat): front verkleind naar de doelhoogte uit
STUDIE.md §2, kop (optioneel) extra vergroot, gemapt op het best passende icoonpalet.
python3 icon_onderlaag.py front.png normal.pal uitmap [--kop x0,y0,x1,y1] [--kopschaal 1.3] [--h N]
Schrijft onderlaag_palK.png (32x32, geïndexeerd op icoonpalet K), onderlaag_8x.png en de foutscore per palet."""
import os,sys,numpy as np
from PIL import Image
def pal(p):
    L=open(p).read().split('\n'); return np.array([[int(v) for v in L[3+k].split()[:3]] for k in range(int(L[2]))])
a=sys.argv[1:]; opt=lambda k,d=None:(a[a.index(k)+1] if k in a else d)
ix=np.array(Image.open(a[0]))[:64]; P=pal(a[1]); out=a[2]; os.makedirs(out,exist_ok=True)
rgb=np.zeros((64,64,4)); rgb[...,:3]=P[ix]; rgb[...,3]=(ix>0)*255
ys,xs=np.nonzero(ix); fh=ys.max()-ys.min()+1
# doelhoogte: interpolatie van de mediaantabel (fronthoogte -> icoonhoogte)
T=[(25,15),(35,18),(45,21),(54,22),(61,24),(64,25)]
h=int(opt('--h',0)) or round(np.interp(fh,[t[0] for t in T],[t[1] for t in T]))
im=Image.fromarray(rgb.astype(np.uint8),'RGBA').crop((xs.min(),ys.min(),xs.max()+1,ys.max()+1))
s=h/fh
def small(img,sc):
    w,hh=img.size; q=img.resize((max(1,round(w*sc)),max(1,round(hh*sc))),Image.BOX); q=np.array(q).astype(float)
    q[...,3]=np.where(q[...,3]>110,255,0); return q
body=small(im,s)
canvas=np.zeros((32,32,4))
bh,bw=body.shape[:2]; oy=30-bh; ox=16-bw//2
def paste(c,q,ox,oy):
    for y in range(q.shape[0]):
        for x in range(q.shape[1]):
            if q[y,x,3] and 0<=y+oy<32 and 0<=x+ox<32: c[y+oy,x+ox]=q[y,x]
paste(canvas,body,ox,oy)
if opt('--kop'):
    x0,y0,x1,y1=[int(v) for v in opt('--kop').split(',')]; ks=float(opt('--kopschaal',1.3))
    kop=small(im.crop((x0-xs.min(),y0-ys.min(),x1-xs.min()+1,y1-ys.min()+1)),s*ks)
    cx=ox+((x0+x1)/2-xs.min())*s; cy=oy+(y1-ys.min())*s   # kop groeit vanaf de hals (onderkant kopvak) omhoog
    paste(canvas,kop,round(cx-kop.shape[1]/2),round(cy-kop.shape[0]))
res=[]
for k in range(6):
    IP=pal('graphics/pokemon/icon_palettes/pal%d.pal'%k)[1:]
    m=canvas[...,3]>0; px=canvas[m][:,:3]
    d=((px[:,None,:]-IP[None,:,:])**2).sum(-1); idx=d.argmin(1)+1; err=np.sqrt(d.min(1)).mean()
    o=np.zeros((32,32),np.uint8); o[m]=idx
    # buitenrand in index 15 (donkergrijs) als ondergrond-omlijning
    im2=Image.fromarray(o,'P'); full=pal('graphics/pokemon/icon_palettes/pal%d.pal'%k)
    im2.putpalette(full.flatten().tolist()); im2.save(f'{out}/onderlaag_pal{k}.png'); res.append((err,k))
res.sort(); print('foutscore per icoonpalet (lager = beter):',[(k,round(e,1)) for e,k in res])
best=Image.open(f'{out}/onderlaag_pal{res[0][1]}.png').convert('RGB'); best.resize((256,256),Image.NEAREST).save(f'{out}/onderlaag_8x.png')
print('fronthoogte',fh,'-> icoonhoogte',h,'beste palet',res[0][1])
