"""Shuppetto-icoon op basis van s1 (Jordi: "deze is iets beter, als je nog een pupil erin kan verwerken en misschien
die kruizen wel kan vormen, dan vind ik het wel prima"). Niets getekend:
- lijf: zelfde rijen/kolommen als s1 (factor 0,41, pal0), alleen bij de ogen een andere rij/kolom gekozen zodat de pupil
  uit de front meekomt (kol 20->19 linkeroog, rij 26->27 rechteroog);
- kruizen: als apart onderdeel uit de front gehaald en met een eigen, grotere factor geschrapt (fase met de beste X),
  dan op de plek van de hand gezet (achter het lijf);
- daarna alleen los weg / omlijning dicht. python3 bouw2.py naam fx fy (fases kruis)"""
import sys,numpy as np; from PIL import Image; from scipy import ndimage
R='/home/user/Pokemon-Fully-Ungrounded/'
fr=Image.open(R+'docs/concept/sprites/banette_evo/af/shuppetto.png'); A=np.array(fr); FP=np.array(fr.getpalette()[:48]).reshape(16,3)
IP=np.array([[int(v) for v in l.split()[:3]] for l in open(R+'graphics/pokemon/icon_palettes/pal0.pal').read().split('\n')[3:19]])
NEAR={0:0}|{k:int(((IP[1:]-FP[k])**2).sum(1).argmin()+1) for k in range(1,16)}
naam=sys.argv[1]; FK=float(sys.argv[2]) if len(sys.argv)>2 else 0.55
a=A.copy(); a[np.isin(a,[5,10,11,12,13,14])]=0
lab,_=ndimage.label(a>0); a[lab!=np.bincount(lab.ravel())[1:].argmax()+1]=0
yy,xx=np.indices(a.shape)
KR=(a>0)&(xx>=47)&(yy>=14)&(yy<=31)&np.isin(a,[1,2,3,4])      # rechterkruis
KL=(a>0)&(xx<=11)&(yy>=17)&(yy<=26)&np.isin(a,[1,2,3,4])      # linkerkruis
RIJ=[4,7,9,12,14,16,19,21,24,27,29,31,34,36,38,41,43,46,48,51,53,55]
KOL=[1,3,5,8,10,13,15,18,19,22,25,27,30,32,35,37,40,42,44,47,49,52,54,57,59,61]
lijf=a.copy(); lijf[KR|KL]=0
r=np.vectorize(NEAR.get)(lijf[np.ix_(RIJ,KOL)]).astype(np.uint8)
def deel(m,f,phy,phx):
    ys,xs=np.nonzero(m); y0,y1,x0,x1=ys.min(),ys.max(),xs.min(),xs.max()
    rr=[p for p in (y0+int((i+phy)/f) for i in range(int(round((y1-y0+1)*f)))) if p<=y1]
    kk=[p for p in (x0+int((i+phx)/f) for i in range(int(round((x1-x0+1)*f)))) if p<=x1]
    sub=np.where(m,a,0)[np.ix_(rr,kk)]
    return np.vectorize(NEAR.get)(sub).astype(np.uint8),(y0,x0)
def half(m,oy,ox):
    sub=np.where(m,a,0); ys,xs=np.nonzero(sub); y0,x0=ys.min()-oy,xs.min()-ox
    rows=[]
    for y in range(y0,ys.max()+1,2):
        row=[]
        for x in range(x0,xs.max()+1,2):
            b=sub[y:y+2,x:x+2].ravel(); nz=b[b>0]
            if len(nz)<2: row.append(0)
            elif (nz==1).sum()>=2: row.append(NEAR[1])
            else: v,c=np.unique(nz,return_counts=True); row.append(NEAR[int(v[c.argmax()])])
        rows.append(row)
    return np.array(rows,np.uint8),(y0,x0)
def zet(c,d,anker):
    # anker in frontcoördinaten -> rastercoördinaten van s1 (dichtstbijzijnde bewaarde rij/kolom)
    oy=int(np.searchsorted(RIJ,anker[0])); ox=int(np.searchsorted(KOL,anker[1]))
    h,w=d.shape; H,W=c.shape
    for y in range(h):
        for x in range(w):
            Y,X=oy+y,ox+x
            if d[y,x] and 0<=Y<H and 0<=X<W and c[Y,X]==0: c[Y,X]=d[y,x]   # achter het lijf
    return c
LOG=[]
def opschonen(c):
    c=c.copy(); h,w=c.shape
    for _ in range(2):
        for y in range(h):
            for x in range(w):
                if not c[y,x]: continue
                nb=[c[yy,xx] if 0<=yy<h and 0<=xx<w else 0 for yy,xx in ((y-1,x),(y+1,x),(y,x-1),(y,x+1))]
                if sum(1 for t in nb if t)<=1: c[y,x]=0; LOG.append((x,y,'los weg'))
                elif all(t for t in nb) and c[y,x] not in nb and c[y,x] not in (5,15):
                    v,k=np.unique(nb,return_counts=True)
                    if k.max()>=3: c[y,x]=v[k.argmax()]; LOG.append((x,y,'los weg (spikkel)'))
    return c
def sluit(c):
    c=c.copy(); m=c>0; p=np.pad(m,1); edge=m&~(p[:-2,1:-1]&p[2:,1:-1]&p[1:-1,:-2]&p[1:-1,2:]); lum=IP.mean(1)
    for y,x in zip(*np.nonzero(edge)):
        if lum[c[y,x]]>=110: c[y,x]=15; LOG.append((x,y,'omlijning dicht'))
    return c
def plaats(c):
    ys,xs=np.nonzero(c); c=c[ys.min():ys.max()+1,xs.min():xs.max()+1]
    h,w=c.shape; out=np.zeros((32,32),np.uint8); oy=29-h+1; ox=15-w//2; out[oy:oy+h,ox:ox+w]=c; return out
def frame2(f1):
    ys,_=np.nonzero(f1); top,bot=ys.min(),ys.max(); f2=np.zeros_like(f1); f2[top+1:bot+1]=f1[top:bot]; return f2
ph=[float(v) for v in sys.argv[3].split(',')] if len(sys.argv)>3 else [0.5,0.5,0.5,0.5]
dr,ar=half(KR,1,0); dl,al=half(KL,0,0)
c=zet(zet(r.copy(),dr,ar),dl,al)
# ogen: uitzondering op de algemene regels (Jordi: "het oog moet altijd een uitzondering zijn op je algemene regels,
# want een pupil blijft altijd zichtbaar, zelfs in het icoon"). Het midden van elk front-oog (geel-pupil-geel) 1-op-1 als
# onderdeel op de berekende plek; geel blijft geel (index 5), pupil = 15.
OOGKLEUR={9:5,1:15,15:6}
c=opschonen(c)
for (fy,fx,h) in ((29,18,1),(27,31,2)):            # linkeroog rij 29 x18-20; rechteroog rijen 27-28 x31-33
    Y=int(np.searchsorted(RIJ,fy)); X=int(np.searchsorted(KOL,fx))
    for dy in range(h):
        for dx in range(3): c[Y+dy,X+dx]=OOGKLEUR[int(a[fy+dy,fx+dx])]
f1=plaats(sluit(c))
out=np.zeros((64,32),np.uint8); out[:32]=f1; out[32:]=frame2(f1)
im=Image.fromarray(out,'P'); im.putpalette(IP.flatten().tolist()+[0]*(768-48)); im.save(naam+'.png',transparency=0)
print(len(LOG),'ingrepen'); print('kruis R'); [print(''.join('.' if v==0 else '%x'%v for v in row)) for row in dr]
print('kruis L'); [print(''.join('.' if v==0 else '%x'%v for v in row)) for row in dl]
for y in range(32):
    s=''.join('.' if v==0 else '%x'%v for v in f1[y])
    if s.strip('.'): print('%2d '%y+s)
