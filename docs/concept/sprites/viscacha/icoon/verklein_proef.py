"""Proef: Gemini-chibi-illustratie -> icoon-onderlaag (verkleinen, icoonpalet, omlijning). Geen eindresultaat."""
import sys,numpy as np
from PIL import Image
D='docs/concept/sprites/viscacha/icoon/'
def pal(k):
    L=open(f'graphics/pokemon/icon_palettes/pal{k}.pal').read().split('\n'); return np.array([[int(v) for v in L[3+i].split()[:3]] for i in range(16)])
a=np.array(Image.open(D+'gemini_chibi_r1.png').convert('RGB')).astype(float)
m=(a.sum(2)<720)
ys,xs=np.nonzero(m); a=a[ys.min():ys.max()+1,xs.min():xs.max()+1]; m=m[ys.min():ys.max()+1,xs.min():xs.max()+1]
fr=np.array(Image.open('docs/concept/sprites/viscacha/af/viscacha.png'))[:64]; fy,_=np.nonzero(fr>0); fh=fy.max()-fy.min()+1
T=[(25,15),(35,18),(45,21),(54,22),(61,24),(64,25)]; h=int(sys.argv[1]) if len(sys.argv)>1 else round(np.interp(fh,[t[0] for t in T],[t[1] for t in T]))
w=round(a.shape[1]*h/a.shape[0])
# donkere lijnen niet laten meetellen in de kleur: kleur = gemiddelde van niet-zwarte pixels per vak
rgb=Image.fromarray(a.astype(np.uint8)); dark=(a.sum(2)<150)
col=np.zeros((h,w,3)); msk=np.zeros((h,w),bool); dk=np.zeros((h,w))
for y in range(h):
    for x in range(w):
        y0,y1=int(y*a.shape[0]/h),int((y+1)*a.shape[0]/h); x0,x1=int(x*a.shape[1]/w),int((x+1)*a.shape[1]/w)
        mm=m[y0:y1,x0:x1]; dd=dark[y0:y1,x0:x1]
        msk[y,x]=mm.mean()>0.45; dk[y,x]=dd.mean()
        sel=mm&~dd
        col[y,x]=a[y0:y1,x0:x1][sel].mean(0) if sel.any() else a[y0:y1,x0:x1][mm].mean(0) if mm.any() else 255
best=None
for k in ([int(sys.argv[2])] if len(sys.argv)>2 else range(6)):
    P=pal(k)[1:14]
    d=((col[...,None,:]-P[None,None])**2).sum(-1); e=np.sqrt(d.min(-1))[msk].mean()
    if best is None or e<best[0]: best=(e,k,d.argmin(-1)+1)
e,k,idx=best; out=np.zeros((32,32),np.uint8)
oy=30-h; ox=16-w//2
sub=np.where(msk,idx,0)
# binnenlijnen: vakken die vooral zwart waren
sub=np.where(msk&(dk>0.5),15,sub)
out[oy:oy+h,ox:ox+w]=sub
# omlijning: buitenrand boven 15, onder 14
mm=out>0; pad=np.pad(mm,1); edge=mm&~(pad[:-2,1:-1]&pad[2:,1:-1]&pad[1:-1,:-2]&pad[1:-1,2:])
ys2,_=np.nonzero(mm); mid=(ys2.min()+ys2.max())/2
for y,x in zip(*np.nonzero(edge)): out[y,x]=15 if y<mid else 14
im=Image.fromarray(out,'P'); im.putpalette(pal(k).flatten().tolist()); im.save(D+'proef_onderlaag.png')
print('palet',k,'fout',round(e,1),'maat',w,'x',h)
