# Basis r1: kale reductie -> tinten uit de modelhelderheid (A) + technische omlijning (B). Geen ogen/spiraal (die komen in varianten.py).
import numpy as np
from palet import PAL
z=np.load('reductie.npz'); cls=z['cls'].copy(); lum=z['lum']; col=z['col']
H,W=cls.shape
def blur(v,m,s):
    r=max(1,int(3*s)); k=np.exp(-np.arange(-r,r+1)**2/(2*s*s))
    num=np.where(m,v,0.0); den=m.astype(float)
    for ax in (0,1):
        num=np.apply_along_axis(lambda x:np.convolve(x,k,'same'),ax,num)
        den=np.apply_along_axis(lambda x:np.convolve(x,k,'same'),ax,den)
    return num/np.maximum(den,1e-6)
def comps(m):
    lab=np.zeros(m.shape,int); n=0
    for y in range(H):
        for x in range(W):
            if m[y,x] and not lab[y,x]:
                n+=1; st=[(y,x)]
                while st:
                    j,i=st.pop()
                    if j<0 or i<0 or j>=H or i>=W or lab[j,i] or not m[j,i]: continue
                    lab[j,i]=n; st+=[(j+1,i),(j-1,i),(j,i+1),(j,i-1)]
    return lab,n
# gat in het linkerkristal: wit facet dat via een kier met de achtergrond verbonden was (lucht-floodfill) -> ijs
for y in (8,9,10): cls[y,10]=3; lum[y,10]=238
ICE=(cls==2)|(cls==3)
lab,n=comps(ICE)
sz={k:(lab==k).sum() for k in range(1,n+1)}
jj,ii=np.mgrid[0:H,0:W]
glove=np.isin(lab,[k for k in sz if sz[k]>=60 and (jj[lab==k].min()>=19)])
crys=ICE&~glove&~((jj<=12)&(ii>=13)&(ii<=33)&(jj>=2))&~((jj>=17)&(ii>=17)&(ii<=28)&(jj<=29))  # zonder ogen/mond/spiraal
out=np.zeros((H,W),'uint8')
Y=cls==1; K=cls==4
# A: lijf zwart: helderheid licht gladgestreken (sigma 1.0 cel)
sb=blur(lum,K,1.0)
out[K]=np.select([sb[K]>=68,sb[K]>=38],[4,3],2)
sy=blur(lum,Y,1.0)
out[Y]=np.select([sy[Y]>=203,sy[Y]>=172],[5,6],7)
for m in (glove,crys):
    ice=m&(cls==3); si=blur(lum,ice,0.45)
    out[ice]=np.select([si[ice]>=222,si[ice]>=200,si[ice]>=170],[8,9,10],11)
red=(cls==2); out[red]=np.select([lum[red]>=125,lum[red]>=95],[12,13],14)
# ijs dat geen handschoen of kristal is (ogen, spiraalcellen) voorlopig: per cel
rest=(cls==3)&~glove&~crys; out[rest]=np.select([lum[rest]>=222,lum[rest]>=200,lum[rest]>=170],[8,9,10],11)
# B: omlijning (rand = naast lucht); normaal uit de 3x3-luchtburen, licht van linksboven
def lucht(y,x): return y<0 or x<0 or y>=H or x>=W or out[y,x]==0
o=out.copy()
for y in range(H):
    for x in range(W):
        v=out[y,x]
        if v==0: continue
        if not (lucht(y-1,x) or lucht(y+1,x) or lucht(y,x-1) or lucht(y,x+1)): continue
        sx=sum(dx for dy in (-1,0,1) for dx in (-1,0,1) if lucht(y+dy,x+dx)); sy_=sum(dy for dy in (-1,0,1) for dx in (-1,0,1) if lucht(y+dy,x+dx))
        schaduw=(sx+sy_)>0
        if v in (2,3,4): o[y,x]=1
        elif v in (5,6,7): o[y,x]=1 if schaduw else 7
        elif glove[y,x]: o[y,x]=1 if schaduw else 11
        elif crys[y,x] or v in (8,9,10,11): o[y,x]=15 if schaduw else 11
        elif v in (12,13,14): o[y,x]=1 if schaduw else 14
out=o
# C: reparaties per pixel naar het model (zie NOTITIES.md)
FIX={(19,8):7,(22,8):7,(17,11):13,(25,11):13,   # mond: 2 cellen met 40% rood verbinden de modellijn
                # neusgaten (model: 2 donkere stipjes, in de reductie minderheid)
     (12,42):7,(13,42):7,(36,43):7,(37,44):7,(40,44):7}   # teenlijnen (donkergeel 'y' 30-40% van de cel)
for (x,y),v in FIX.items(): out[y,x]=v
# ruis: losse tintpixels (cluster van 1) in lijf (2/3/4) en geel (5/6) -> meest voorkomende buurtint uit dezelfde groep
GRP={2:(2,3,4),3:(2,3,4),4:(2,3,4),5:(5,6,7),6:(5,6,7)}
SPZ=(slice(17,31),slice(15,32))
ruis=[]
for y in range(H):
    for x in range(W):
        v=out[y,x]
        if v not in GRP or (x,y) in FIX or (17<=y<=30 and 15<=x<=31) or y<=8: continue
        nb=[out[y+a,x+b] for a,b in ((1,0),(-1,0),(0,1),(0,-1)) if 0<=y+a<H and 0<=x+b<W]
        if v in nb: continue
        same=[n for n in nb if n in GRP[v]]
        if len(same)>=2: out[y,x]=max(set(same),key=same.count); ruis.append((x,y))
# oogzones van het model: het hele modeloog (wit, pupil en zwarte oogring) wordt eerst opgevuld met de kop eromheen;
# de ogen komen daarna 1-op-1 uit een bestaande sprite (varianten.py). Silhouetrand (pixel naast lucht) blijft staan.
OOGC=[(16,4.5),(29,4.5)]; OOGRAD=2.7
oogzone=np.zeros((H,W),bool)
for cx,cy in OOGC: oogzone|=((ii-cx)**2+(jj-cy)**2<=OOGRAD**2)
rand=np.zeros((H,W),bool)
for y in range(H):
    for x in range(W):
        if out[y,x] and any(not(0<=y+a<H and 0<=x+b<W) or out[y+a,x+b]==0 for a,b in ((1,0),(-1,0),(0,1),(0,-1))): rand[y,x]=True
open_=oogzone&~rand&(out>0)
while open_.any():
    nxt=open_.copy()
    for y,x in zip(*np.where(open_)):
        nb=[out[y+a,x+b] for a,b in ((1,0),(-1,0),(0,1),(0,-1)) if 0<=y+a<H and 0<=x+b<W and not open_[y+a,x+b] and out[y+a,x+b] not in (0,8,9,10,11)]
        nb=[n for n in nb if n!=1] or nb
        if nb: out[y,x]=max(set(nb),key=nb.count); nxt[y,x]=False
    open_=nxt
out[oogzone&rand&np.isin(out,[8,9,10,11])]=1   # wit van het modeloog op de silhouetrand -> omlijning
