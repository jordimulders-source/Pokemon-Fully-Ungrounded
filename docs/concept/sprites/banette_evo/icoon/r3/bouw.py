"""Shuppetto-icoon route 2 (front staat al in driekwart). Geen tekenwerk (Jordi 28 nov).
1. delen weglaten: Shuppets (kleuren 5,10,11,12,14), draden (13) en alles wat daarna niet meer aan het lijf vastzit
   (Jordi: "het gaat onmogelijk zijn om de kleine shuppets in het icoon te zetten ... Dragapult heeft ook geen kleine Dreepy's").
2. rijen/kolommen schrappen met één factor in beide richtingen; fase zo gekozen dat de gele ogen (9) blijven.
3. kleur = dichtstbijzijnde index van het gekozen icoonpalet; daarna alleen los weg / omlijning dicht.
python3 bouw.py naam factor [pal]"""
import sys,numpy as np; from PIL import Image; from scipy import ndimage
R='/home/user/Pokemon-Fully-Ungrounded/'
fr=Image.open(R+'docs/concept/sprites/banette_evo/af/shuppetto.png'); A=np.array(fr); FP=np.array(fr.getpalette()[:48]).reshape(16,3)
naam=sys.argv[1]; f=float(sys.argv[2]); PAL=int(sys.argv[3]) if len(sys.argv)>3 else 0
IP=np.array([[int(v) for v in l.split()[:3]] for l in open(R+f'graphics/pokemon/icon_palettes/pal{PAL}.pal').read().split('\n')[3:19]])
NEAR={0:0}|{k:int(((IP[1:]-FP[k])**2).sum(1).argmin()+1) for k in range(1,16)}
if PAL==0: NEAR[9]=5; NEAR[7]=6   # kleurtoon: gele ogen blijven geel (dichtstbij = roze 11); donkerrood blijft rood (dichtstbij = omlijning 15)
LOG=[]
# 1. delen weglaten
a=A.copy(); a[np.isin(a,[5,10,11,12,13,14])]=0
lab,n=ndimage.label(a>0); grootste=np.bincount(lab.ravel())[1:].argmax()+1; a[lab!=grootste]=0
# onderdelen als geheel verschuiven: kruizen naar binnen (breedte max 27)
DX_L=int(sys.argv[4]) if len(sys.argv)>4 else 0; DX_R=int(sys.argv[5]) if len(sys.argv)>5 else 0
yy,xx=np.indices(a.shape)
L=(a>0)&(xx<=12)&(yy>=16)&(yy<=38); Rm=(a>0)&(xx>=47)&(yy>=14)&(yy<=31)
b=a.copy(); b[L]=0; b[Rm]=0
for m,dx in ((L,DX_L),(Rm,-DX_R)):
    ys_,xs_=np.nonzero(m); keep=b[ys_,xs_+dx]==0   # deel komt achter het lijf: lijf blijft voor
    b[ys_[keep],xs_[keep]+dx]=a[ys_[keep],xs_[keep]]
a=b
ys,xs=np.nonzero(a); y0,y1,x0,x1=ys.min(),ys.max(),xs.min(),xs.max()
NEK=40; FL=float(sys.argv[6]) if len(sys.argv)>6 else f   # onderlijf eigen (kleinere) factor
def kies(lo,hi,ph): return [p for p in (lo+int((i+ph)/f) for i in range(int(round((hi-lo+1)*f)))) if p<=hi]
best=None
for phy in np.arange(0,1,0.1):
  for phx in np.arange(0,1,0.1):
    RIJ=kies(y0,NEK,phy); RIJ+= [p for p in (NEK+1+int((i+0.5)/FL) for i in range(int(round((y1-NEK)*FL)))) if p<=y1]; KOL=kies(x0,x1,phx); s=(a[np.ix_(RIJ,KOL)]==9).sum()
    if best is None or s>best[0]: best=(s,RIJ,KOL)
_,RIJ,KOL=best
r=np.vectorize(NEAR.get)(a[np.ix_(RIJ,KOL)]).astype(np.uint8)
def opschonen(c):
    c=c.copy(); h,w=c.shape
    for _ in range(2):
        for y in range(h):
            for x in range(w):
                if not c[y,x]: continue
                nb=[c[yy,xx] if 0<=yy<h and 0<=xx<w else 0 for yy,xx in ((y-1,x),(y+1,x),(y,x-1),(y,x+1))]
                if sum(1 for t in nb if t)<=1: c[y,x]=0; LOG.append((x,y,'los weg'))
    return c
def sluit(c):
    c=c.copy(); m=c>0; p=np.pad(m,1); edge=m&~(p[:-2,1:-1]&p[2:,1:-1]&p[1:-1,:-2]&p[1:-1,2:])
    lum=IP.mean(1)
    for y,x in zip(*np.nonzero(edge)):
        if lum[c[y,x]]>=110: c[y,x]=15; LOG.append((x,y,'omlijning dicht'))
    return c
def plaats(c):
    h,w=c.shape; out=np.zeros((32,32),np.uint8); oy=29-h+1; ox=15-w//2; out[oy:oy+h,ox:ox+w]=c; return out
def frame2(f1):
    ys,_=np.nonzero(f1); top,bot=ys.min(),ys.max()
    f2=np.zeros_like(f1); f2[top+1:bot+1]=f1[top:bot]   # zweeft: alles 1 px omlaag (onderste rij valt weg)
    return f2
f1=plaats(sluit(opschonen(r)))
out=np.zeros((64,32),np.uint8); out[:32]=f1; out[32:]=frame2(f1)
im=Image.fromarray(out,'P'); im.putpalette(IP.flatten().tolist()+[0]*(768-48)); im.save(naam+'.png',transparency=0)
print('pal',PAL,'map',NEAR,'rij',RIJ,'kol',KOL); print(len(LOG),'ingrepen')
for y in range(32):
    s=''.join('.' if v==0 else '%x'%v for v in f1[y])
    if s.strip('.'): print('%2d '%y+s)
