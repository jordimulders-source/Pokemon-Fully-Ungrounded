# Technische opschoning van de kale reductie BUITEN het gezicht (zelfde stappen als sprite/r1 stap2-5). Niets getekend; elke wijziging geteld.
import sys; sys.path.insert(0,'.'); from gemeen import *; from PIL import Image; from clusters import vlakjes
a=np.asarray(Image.open('../natief_g1.png').convert('RGB')).astype(float); Lm=lum(a); NH,NW=Lm.shape
MY,MX=np.load('basis_map.npy')
gezn=np.load('../natief_g1_gez.npy')
def blok(y,x):
    y0,x0=MY+3*y,MX+3*x
    return (slice(max(y0,0),max(y0+3,0)),slice(max(x0,0),max(x0+3,0)))
o=np.load('basis.npy'); raw=o.copy(); log={}
def tel(k): log[k]=log.get(k,0)+1
N4=((1,0),(-1,0),(0,1),(0,-1)); N8=[(p,q) for p in (-1,0,1) for q in (-1,0,1) if p or q]
def nb(y,x,n=N4): return [(y+dy,x+dx) for dy,dx in n if 0<=y+dy<64 and 0<=x+dx<64]
# gezichtszone: cellen met >=3 gezichtspixels (gezicht + binnenlijn), apart in gezicht.py
gez=np.zeros((64,64),bool)
for y in range(64):
  for x in range(64):
    b=blok(y,x)
    if gezn[b].sum()>=3: gez[y,x]=True
p=np.pad(gez,1); gezr=gez|p[:-2,1:-1]|p[2:,1:-1]|p[1:-1,:-2]|p[1:-1,2:]   # + binnenlijn eromheen
np.save('gezzone.npy',gezr)
near=nearest(a); gr=a[...,1]-a[...,0]; t=(gr<8)&np.isin(near,TURK); near[t]=nearest(a[t],[i for i in range(2,14)])
g=(gr>=8)&np.isin(near,(3,4,13)); near[g]=nearest(a[g],(6,14,15))
DONK={2:2,3:2,4:3,5:13,13:4,6:6,14:6,15:14,7:7,8:7,9:7,10:9,11:2,12:11}
m=o>0
# 1. buitenrand dicht
for y in range(64):
  for x in range(64):
    if not m[y,x] or o[y,x]==1: continue
    if not [q for q in nb(y,x) if not m[q]]: continue
    b=blok(y,x); bb=(slice(max(b[0].start-2,0),b[0].stop+2),slice(max(b[1].start-2,0),b[1].stop+2))
    if Lm[bb].min()>=90: o[y,x]=DONK[raw[y,x]]; tel('rand: geen zwarte modellijn -> donkerste eigen tint')
    else: o[y,x]=1; tel('rand zwart')
rand=np.zeros((64,64),bool); pd=np.pad(m,1); rand=m&~(pd[:-2,1:-1]&pd[2:,1:-1]&pd[1:-1,:-2]&pd[1:-1,2:])
# 2. lijnkaart: modellijnen (>=3 donkere modelpixels in het blok) -> donkerste tint van het vlak; zwart zonder modellijn -> vlak
dk=Lm<70; zw=Lm<40
n=np.zeros((64,64),int); kl=np.zeros((64,64),int)
for y in range(64):
  for x in range(64):
    if not m[y,x]: continue
    b=blok(y,x); n[y,x]=dk[b].sum(); v=near[b][~dk[b]]
    kl[y,x]=np.bincount(v,minlength=16).argmax() if len(v) else 0
lijn=(n>=3)&~rand&m&~gezr
for y in range(64):
  for x in range(64):
    if gezr[y,x] or rand[y,x] or not m[y,x]: continue
    if lijn[y,x]:
      gs=[kl[y,x]]+[o[q] for q in nb(y,x) if o[q]>1]
      tt=min((DONK.get(v,2) for v in gs if v), key=lambda i: lum(P[i]))
      if zw[blok(y,x)].sum()>=3: tt=1; tel('waarvan zwart (dikke modellijn)')
      if o[y,x]!=tt: o[y,x]=tt; tel('binnenlijn uit model -> donkerste eigen tint')
    elif o[y,x]==1:
      c=[o[q] for q in nb(y,x) if o[q]>1]
      o[y,x]=kl[y,x] if kl[y,x] else np.bincount(c).argmax(); tel('zwart binnenin zonder modellijn -> vlak')
# 3. tintvlakjes < 3 px (geen lijn, rand of gezicht) -> 2e modelkeuze uit het blok, mits buurkleur
for it in range(3):
  for v,comp in vlakjes(o):
    if v==5: continue
    for (y,x) in comp:
      if lijn[y,x] or rand[y,x] or gezr[y,x]: continue
      if any(lijn[q] and o[q]==v for q in nb(y,x,N8)): continue
      bc=np.bincount(near[blok(y,x)].ravel(),minlength=16)
      buur={o[q] for q in nb(y,x)}-{0,1,v}
      kand=sorted(buur,key=lambda k:-bc[k])
      if kand and bc[kand[0]]>0: o[y,x]=kand[0]; tel('vlakje -> 2e modelkeuze')
      elif kand:
        cnt={k:sum(o[q]==k for q in nb(y,x,N8)) for k in kand}; o[y,x]=max(cnt,key=cnt.get); tel('vlakje -> buurkleur')
# 4. losse lijnpixel (donkere tint zonder lijnbuur) die geen lijn is -> blijft; losse zwarte binnenin -> donkere eigen tint
for y in range(1,63):
  for x in range(1,63):
    if o[y,x]!=1 or gezr[y,x]: continue
    if any(o[q] in (0,1) for q in nb(y,x,N8)): continue
    c=[o[q] for q in nb(y,x) if o[q]>1]; tt=min({DONK[v] for v in c},key=lambda i:lum(P[i])); o[y,x]=tt; tel('losse zwarte -> donkere eigen tint')
np.save('romp.npy',o); np.save('lijn.npy',lijn); print(log,'gewijzigd',int((o!=raw).sum()))
im=Image.fromarray(o.astype('uint8'),'P'); im.putpalette([v for c in PAL for v in c]+[0]*(768-48)); im.save('romp.png',transparency=0)
