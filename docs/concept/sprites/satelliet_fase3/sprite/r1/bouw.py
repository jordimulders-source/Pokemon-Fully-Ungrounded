# r1 ruimtestation: kale reductie (kaal.py) + benoemde reparaties, alles gemeten op het model.
import os
from lagen import *
OUTW=64
LIJN=int(os.environ.get('LIJN','11'))
THR_IN=float(os.environ.get("THR_IN","1.2"))

MODE=os.environ.get('MODE','mat')
GEO={ # T, R (eind in de lengte), L (eind dwars), aantal vakken in de lengte; gemeten op model_gekozen.png
 'PA':((86,24),(137,40),(71,36),4),
 'PC':((176,58),(227,72),(163,70),4),
 'PD':((20,86),(57,100),(3,96),4),
 'PF':((123,100),(123,136),(133,104),3),
 'PE':((102,117),(149,134),(88,132),4),
 'PB':((123,3),(123,50),(132,8),3),
}
ORDER=list(GEO)   # achter -> voor (PB voor PA, PE voor PF)
a,bg,lab=model(); H,W=lab.shape
ys,xs=np.where(~bg); X0,X1,Y0,Y1=xs.min(),xs.max()+1,ys.min(),ys.max()+1
s=(X1-X0)/OUTW; OH=int(np.ceil((Y1-Y0)/s))
Wx=kaal.overlap(OUTW,X0,s,W); Wy=kaal.overlap(OH,Y0,s,H)
def cov(mask): return Wy@mask.astype(float)@Wx.T/(s*s)
def uv(k,px,py):
    T,R,L,n=GEO[k]; T,R,L=map(np.array,(T,R,L))
    M=np.array([R-T,L-T]).T.astype(float); inv=np.linalg.inv(M)
    d=np.stack([px-T[0],py-T[1]]); r=np.tensordot(inv,d,1); return r[0],r[1]
DARK=np.isin(lab,[1,2,3,4,5,11])
yy,xx=np.mgrid[0:H,0:W]
pm={}
taken=np.zeros((H,W),bool)
for k in ORDER[::-1]:
    u,v=uv(k,xx+0.5,yy+0.5); g=1.5/ np.hypot(*np.array(GEO[k][1])-np.array(GEO[k][0]))
    inside=(u>-g)&(u<1+g)&(v>-0.12)&(v<1.12)&DARK&~taken
    pm[k]=inside; taken|=inside
nonbg=cov(~bg)
pc={k:cov(m) for k,m in pm.items()}
body=nonbg-sum(pc.values())
stack=np.stack([body]+[pc[k] for k in ORDER])
owner=stack.argmax(0)
alpha=nonbg>=0.5
kale,_=kaal.reduce(); kale=kale.astype(np.uint8)
spr=kale.copy(); spr[~alpha]=0
log={}
def setpx(zone,y,x,c):
    if spr[y,x]!=c:
        log.setdefault(zone,[]).append((int(y),int(x),int(spr[y,x]),int(c))); spr[y,x]=c
# ---- 1. panelen: vakken uit de modelgeometrie (GEO), lijnen 1 px op de modelposities
SY,SX=np.mgrid[0:OH,0:OUTW]
MX=X0+(SX+0.5)*s; MY=Y0+(SY+0.5)*s
for i,k in enumerate(ORDER):
    own=(owner==i+1)&alpha
    T,R,L,n=GEO[k]; Ls=np.hypot(*(np.array(R)-T))/s
    u,v=uv(k,MX,MY)
    # gradient van u in spritepixels
    du_dx=(uv(k,MX+s,MY)[0]-u); du_dy=(uv(k,MX,MY+s)[0]-u)
    gn=np.hypot(du_dx,du_dy); nx,ny=np.abs(du_dx)/gn,np.abs(du_dy)/gn
    lim=0.5*np.maximum(nx,ny)
    for y,x in zip(*np.where(own)):
        c=2
        for j in range(1,n):
            if abs(u[y,x]-j/n)/gn[y,x]<=lim[y,x]: c=LIJN
        setpx('paneel_'+k,y,x,c)
np.save('owner.npy',owner)

# ---- 2. romp: materiaal per pixel (oppervlakmeerderheid), wittint uit de modelhelderheid
WH=np.isin(lab,[11,12,13,14,15]); PU=np.isin(lab,[6,7,8]); NV=np.isin(lab,[1,2,3]); TE=np.isin(lab,[9,10]); LV=np.isin(lab,[4,5])
cW,cP,cN,cT,cL=[cov(m) for m in (WH,PU,NV,TE,LV)]
lum=a.astype(float).mean(2)
Lw=(Wy@(lum*WH)@Wx.T)/np.maximum(Wy@WH.astype(float)@Wx.T,1e-6)
lumP=(Wy@(lum*PU)@Wx.T)/np.maximum(Wy@PU.astype(float)@Wx.T,1e-6)
bodym=(owner==0)&alpha
mat=np.zeros((OH,OUTW),int)
mat[cP>=0.30]=1
mat[(cN>=0.55)&(cN>cP)]=2
mat[cT>=0.30]=3
GEM=[[int(c,16) if c!='.' else 0 for c in l.strip()] for l in open('kaal.txt')]
for y,x in zip(*np.where(bodym)):
    if MODE=='gem':
        setpx('romp',y,x,GEM[y][x] or 14); continue
    m=mat[y,x]
    if m==0:
        l=Lw[y,x]; c=15 if l>=243 else 14 if l>=222 else 13 if l>=200 else 12 if l>=175 else 11
    elif m==1: c=8 if lumP[y,x]>150 else 7 if lumP[y,x]>125 else 6
    elif m==2: c=2
    else: c=10 if cov(np.isin(lab,[10]))[y,x]>=cov(np.isin(lab,[9]))[y,x] else 9
    setpx('romp',y,x,c)

# ---- 2b. binnenlijnen van de romp: dunne donkere modellijnen (klasse 1/2 met weinig donkere buren) geprojecteerd
DK=np.isin(lab,[1,2,3])
nb=np.zeros_like(DK,int)
for dy in (-2,-1,0,1,2):
    for dx in (-2,-1,0,1,2):
        nb+=np.roll(np.roll(DK,dy,0),dx,1)
THIN=DK&(nb<=13)
SXm=np.floor((xx+0.5-X0)/s).astype(int); SYm=np.floor((yy+0.5-Y0)/s).astype(int)
okm=THIN&(SXm>=0)&(SXm<OUTW)&(SYm>=0)&(SYm<OH)
Pthin=np.zeros((OH,OUTW)); np.add.at(Pthin,(SYm[okm],SXm[okm]),1); Pthin/=s
for y,x in zip(*np.where(bodym&(Pthin>=THR_IN)&~np.isin(spr,[6,7,8]))):
    setpx('binnenlijn',y,x,2)

# ---- 2c. kragen/banden: paars uit de puntbemonstering (punt.txt) waar de romp wit kreeg
PUNT=[l.strip() for l in open('punt.txt')]
for y,x in zip(*np.where(bodym)):
    ch=PUNT[y][x]
    if ch in '678' and spr[y,x] in (11,12,13,14,15):
        setpx('kraag_paars',y,x,int(ch,16))
# ---- 3. buitenlijn: rand van het silhouet; schaduwkant (rechts/onder) zwart 1, lichtkant navy 2
for y,x in zip(*np.where(alpha)):
    nb=[(y-1,x),(y+1,x),(y,x-1),(y,x+1)]
    out=[(yy_,xx_) for yy_,xx_ in nb if not(0<=yy_<OH and 0<=xx_<OUTW) or not alpha[yy_,xx_]]
    if out:
        shadow=any(yy_>y or xx_>x for yy_,xx_ in out)
        setpx('buitenlijn',y,x,1 if (shadow or owner[y,x]!=0) else 2)

# ---- 4. ogen: maten gemeten op het model (ring/iris/pupil-bbox, zie RAPPORT), ring paars licht->donker naar rechtsonder,
#      binnen de ring alleen iris (9/a) en pupil (2), geen wit (Jordi)
def put(zone,pix):
    for (x,y),c in pix.items(): setpx(zone,y,x,c)
oog={}
# voorste oog: ronde ring 7x7 (x12-18, y33-39; model ring + donkere rand 11.95-17.92 x 33.3-39.5), iris binnen, pupil 2x2 links van het midden
EYE=["..887..",
     ".8999a6",
     "89aaaa6",
     "7a22aa6",
     "7a22aa6",
     ".6aaa6.",
     "..666.."]
for j,r in enumerate(EYE):
    for i,ch in enumerate(r):
        if ch!='.': oog[(12+i,33+j)]=int(ch,16)
put('oog_voor',oog)
def klein(x0,y0,zone):
    p={(x0+1,y0):8,(x0+2,y0):7,(x0,y0+1):8,(x0+3,y0+1):6,(x0,y0+2):7,(x0+3,y0+2):6,(x0+1,y0+3):6,(x0+2,y0+3):6,
       (x0+1,y0+1):9,(x0+2,y0+1):10,(x0+1,y0+2):2,(x0+2,y0+2):10}
    put(zone,p)
klein(17,16,'oog_links')
klein(50,24,'oog_rechts')

# ---- 5. ruis: losse pixel binnen de romp (geen enkele 8-buur in dezelfde klasse) -> meest voorkomende buurkleur
KL={0:'t',1:'d',2:'d',3:'d',4:'l',5:'l',6:'p',7:'p',8:'p',9:'o',10:'o',11:'w',12:'w',13:'w',14:'w',15:'w'}
from collections import Counter
for it in range(2):
    for y in range(1,OH-1):
        for x in range(1,OUTW-1):
            c=spr[y,x]
            if c==0 or owner[y,x]!=0 or KL[c] in 'o': continue
            if any(abs(x-ex)<=2 and abs(y-ey)<=2 for ex,ey in ((14,36),(18,17),(51,25))): continue
            nb=[spr[y+dy,x+dx] for dy in (-1,0,1) for dx in (-1,0,1) if (dy or dx)]
            if not any(KL[n]==KL[c] for n in nb):
                cand=Counter(n for n in nb if n!=0 and KL[n]!='d').most_common(1)
                if cand: setpx('ruis',y,x,cand[0][0])

# ---- 6. losse handreparaties
pass #   # hoekpixel linksonder weg: bol en oogring ronder (was losse paarse hoek)
setpx('kraag_onder',27,36,6)  # onderste kraag (mastvoet onder de hub) 2 px paars zoals puntbemonstering, was losse pixel

import sys
def dump(path):
    with open(path,'w') as f:
        for y in range(OH): f.write(''.join('.' if spr[y,x]==0 else '0123456789abcdef'[spr[y,x]] for x in range(OUTW))+'\n')
if __name__=='__main__':
    dump('basis.txt'); kaal.save(spr,'basis.png')
    print({k:len(v) for k,v in log.items()})
