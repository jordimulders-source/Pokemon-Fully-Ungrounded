# Lijnkaart: binnenlijnen uit het model (donkere modelpixels per 3x3-blok) terugzetten, in de donkerste tint van het vlak.
import sys; sys.path.insert(0,'.'); from gemeen import *; from PIL import Image
a=np.asarray(Image.open('../natief.png').convert('RGB')).astype(float); Lm=lum(a); dk=Lm<70; zw=Lm<40
o=np.load('stap2.npy'); raw=np.load('basis.npy'); log={}
def tel(k): log[k]=log.get(k,0)+1
def blok(sy,sx): y0=3*sy-9; x0=3*sx+3; return (slice(max(y0,0),y0+3),slice(x0,x0+3))
n=np.zeros((64,64),int); kl=np.zeros((64,64),int)
near=nearest(a); gr=a[...,1]-a[...,0]; g=gr<8; near[g&(near>=13)]=nearest(a[g&(near>=13)],range(2,13))
for sy in range(64):
  for sx in range(64):
    if o[sy,sx]==0 or 3*sy-9<0: continue
    b=blok(sy,sx); n[sy,sx]=dk[b].sum()
    v=near[b][~dk[b]]; kl[sy,sx]=np.bincount(v,minlength=16).argmax() if len(v) else 0
rand=np.zeros((64,64),bool); m=o>0; pd=np.pad(m,1)
rand=m&~(pd[:-2,1:-1]&pd[2:,1:-1]&pd[1:-1,:-2]&pd[1:-1,2:])
GEZ=(13,26,24,40)
ingez=lambda y,x: GEZ[0]<=y<GEZ[1] and GEZ[2]<=x<GEZ[3]
lijn=(n>=3)&~rand&m
for it in range(3):
  for y in range(1,63):
    for x in range(1,63):
      if lijn[y,x] or rand[y,x] or not m[y,x] or n[y,x]<2: continue
      nbp=[(y+dy,x+dx) for dy in (-1,0,1) for dx in (-1,0,1) if (dy or dx) and (lijn[y+dy,x+dx] or (rand[y+dy,x+dx] and o[y+dy,x+dx]==1))]
      # brug: twee lijnburen die elkaar niet raken
      if any(abs(p[0]-q[0])>1 or abs(p[1]-q[1])>1 for p in nbp for q in nbp): lijn[y,x]=True
DONK={2:2,3:2,4:3,5:4,6:4,7:7,8:7,9:7,10:7,11:2,12:11,13:13,14:13,15:13}
for y in range(64):
  for x in range(64):
    if ingez(y,x): continue
    if lijn[y,x]:
      # donkerste tint van de vlakken eromheen (blok + 4-buren)
      gs=[kl[y,x]]+[o[p] for p in ((y-1,x),(y+1,x),(y,x-1),(y,x+1)) if o[p]>1]
      t=min((DONK.get(v,2) for v in gs if v), key=lambda i: lum(P[i]))
      if zw[blok(y,x)].sum()>=3: t=1; tel('waarvan zwart (dikke modellijn)')
      if o[y,x]!=t: o[y,x]=t; tel('binnenlijn uit model')
    elif o[y,x]==1 and not rand[y,x]:
      c=[o[p] for p in ((y-1,x),(y+1,x),(y,x-1),(y,x+1)) if o[p]>1]
      o[y,x]=kl[y,x] if kl[y,x] else np.bincount(c).argmax(); tel('zwart binnenin zonder modellijn -> vlak')
np.save('stap3.npy',o); np.save('lijn.npy',lijn); print(log)
p=Image.fromarray(o.astype('uint8'),'P'); p.putpalette([v for c in PAL for v in c]+[0]*(768-48)); p.save('stap3.png',transparency=0)
