# r8 model: (1) de zes panelen verbreed in hun korte richting (NN-schaal van de eigen paneelpixels rond de middellijn v=0,5,
#   lengte en vakken gelijk); (2) voorste oogbol x1,3 (= r7), zijbollen x1,6 of x1,8; alles t.o.v. het originele model r13b.
# Voor/achter: panelen achter de romp (romp/buizen/bollen worden er weer overheen gezet); onderling ORDE (achter->voor) zoals
# bouw4: PC, PA, PB, PD, PF, PE. Bollen zoals r7 (voor en rechts voor hun kraag, links achter zijn kraag).
import os, sys, numpy as np
from PIL import Image
from collections import deque
H=os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0,os.path.join(H,'..','r4')); import kaal
a=np.array(Image.open(os.path.join(H,'..','..','model','model_gekozen.png')).convert('RGB')); Hh,Ww,_=a.shape
w=a.min(2)>=245; bg=np.zeros((Hh,Ww),bool); q=deque()
for y in range(Hh):
    for x in (0,Ww-1):
        if w[y,x] and not bg[y,x]: bg[y,x]=1; q.append((y,x))
for x in range(Ww):
    for y in (0,Hh-1):
        if w[y,x] and not bg[y,x]: bg[y,x]=1; q.append((y,x))
while q:
    y,x=q.popleft()
    for dy,dx in ((1,0),(-1,0),(0,1),(0,-1)):
        yy,xx=y+dy,x+dx
        if 0<=yy<Hh and 0<=xx<Ww and w[yy,xx] and not bg[yy,xx]: bg[yy,xx]=1; q.append((yy,xx))
pal=np.array(kaal.PAL[1:],float)
lab=((a[:,:,None,:].astype(float)-pal[None,None])**2).sum(3).argmin(2)+1; lab[bg]=0
Y,X=np.mgrid[0:Hh,0:Ww]; PX,PY=X+0.5,Y+0.5
# ---------- panelen
GEO={'PA':((86,24),(137,40),(71,36)),'PC':((176,58),(227,72),(163,70)),'PD':((20,86),(61,101),(3,96)),
     'PF':((123,100),(123,136),(133,104)),'PE':((102,117),(149,134),(88,132)),'PB':((123,3),(123,50),(132,8))}
ORDE=['PC','PA','PB','PD','PF','PE']
# anker van de verbreding (v): 0,5 = rond de middellijn; PD/PC/PB alleen naar binnen (buitenrand v=1 / v=0 blijft staan),
# anders wordt het model breder of hoger dan 225x149 en wordt de hele sprite kleiner (64 px breedtegrens)
ANKER={'PA':0.5,'PE':0.5,'PF':0.5,'PD':1.0,'PC':0.0,'PB':0.0}
def uvm(k,px,py):
    T,R,L=map(np.array,GEO[k]); inv=np.linalg.inv(np.array([R-T,L-T]).T.astype(float))
    d=np.stack([px-T[0],py-T[1]]); r=np.tensordot(inv,d,1); return r[0],r[1]
af=a.astype(int)
def near(t,r): return ((af-np.array(t))**2).sum(2)<r*r
kern=(near((40,38,70),14)|(near((116,99,143),24)&((af[:,:,0]-af[:,:,1])<30))|near((28,24,45),10))&~bg
BOLC=[((62.16,127.95),21.12),((75.01,64.28),11.25),((188.46,91.70),12.48),((182.0,36.1),14.8),((128.0,72.0),20.5)]
inbol=np.zeros_like(bg)
for (cx,cy),r in BOLC: inbol|=np.hypot(PX-cx,PY-cy)<=r+0.5
licht=(a.min(2)>150)&~bg
def dil(m,n=1):
    o=m.copy()
    for _ in range(n):
        o=o|np.roll(o,1,0)|np.roll(o,-1,0)|np.roll(o,1,1)|np.roll(o,-1,1)
    return o
PMASK={}
paneelkleur=~bg&~inbol&(a.min(2)<150)&((af[:,:,0]-af[:,:,1])<30)   # navy vak, lavendel lijn, donkere rand; geen wit en geen paarse kraag (R-G>=30)
for k in ORDE:
    u,v=uvm(k,PX,PY); box=(u>-0.04)&(u<1.04)&(v>-0.12)&(v<1.12)
    PMASK[k]=paneelkleur&box
PAN=np.zeros_like(bg)
for m in PMASK.values(): PAN|=m
def panelen(f):
    out=np.full_like(a,255); al=np.zeros_like(bg)
    for k in ORDE:                       # achter -> voor
        u,v=uvm(k,PX,PY); an=ANKER[k]; vs=an+(v-an)/f
        if an in (0.0,1.0): vs=np.where((v-an)*(0.5-an)<0,v,vs)   # buitenrand (ankerkant) blijft 1-op-1 staan
        T,R,L=map(np.array,GEO[k]); src=T[None,None,:]+u[...,None]*(R-T)+vs[...,None]*(L-T)
        sx=np.floor(src[...,0]).astype(int); sy=np.floor(src[...,1]).astype(int)
        ok=(sx>=0)&(sx<Ww)&(sy>=0)&(sy<Hh)
        ok[ok]&=PMASK[k][sy[ok],sx[ok]]
        out[ok]=a[sy[ok],sx[ok]]; al|=ok
    body=~bg&~PAN                         # romp, buizen, bollen, staafjes: voor de panelen
    out[body]=a[body]; al|=body
    return out,al
# ---------- bollen (zoals r7/model_bol.py)
BOL={'voor':(62.16,127.95,20.62),'links':(75.01,64.28,10.75),'rechts':(188.46,91.70,11.98)}
KRAAGSET=(1,2,3,4,6,7,8)
KSTART={y:next(x for x in range(79,110) if lab[y,x] in KRAAGSET) for y in range(54,75)}
def masker(nm):
    cx,cy,r=BOL[nm]; d=np.hypot(PX-cx,PY-cy); m=(d<=r+0.5)&~bg
    ang=np.degrees(np.arctan2(PY-cy,PX-cx))%360
    if nm=='voor': m&=~((ang>270)&(ang<360)&(d>0.85*r)&np.isin(lab,(4,6,7,8)))
    if nm=='rechts': m&=~((ang>135)&(ang<225)&(d>0.85*r)&np.isin(lab,(4,6,7,8)))
    if nm=='links':
        for y,x0 in KSTART.items(): m[y,x0:]=False
    return m&~PAN
MASK={nm:masker(nm) for nm in BOL}
KR=np.zeros_like(bg)
for y,x0 in KSTART.items(): KR[y,x0:x0+8]=~bg[y,x0:x0+8]
def bollen(base,al,kf,ks):
    out=base.copy(); al=al.copy()
    for nm,k in (('rechts',ks),('links',ks),('voor',kf)):
        cx,cy,r=BOL[nm]; Rr=(r+0.5)*k+1
        if nm=='links':   # r8: schalen vanuit de kraagkant (x=79, kraagrand) i.p.v. het middelpunt: de snede achter de kraag blijft
            ox=79.0; Rr=(r+0.5+(ox-cx))*k+1; cx=ox   # bij de kraag; anders steekt de bol boven/onder de kraag als blok naar rechts uit
        sx=np.floor(cx+(PX-cx)/k).astype(int); sy=np.floor(cy+(PY-cy)/k).astype(int)
        ok=(np.hypot(PX-cx,PY-cy)<=Rr)&(sx>=0)&(sx<Ww)&(sy>=0)&(sy<Hh)
        ok[ok]&=MASK[nm][sy[ok],sx[ok]]
        if nm=='links': ok&=~KR
        out[ok]=a[sy[ok],sx[ok]]; al|=ok
    out[~al]=255
    return out,al
if __name__=='__main__':
    VARS={'s16p13':(1.3,1.6,1.3),'s16p15':(1.3,1.6,1.5),'s18p13':(1.3,1.8,1.3),'s18p15':(1.3,1.8,1.5)}
    for tag,(kf,ks,kp) in VARS.items():
        p,al=panelen(kp); out,al=bollen(p,al,kf,ks)
        Image.fromarray(out).save(os.path.join(H,'model_%s.png'%tag))
        Image.fromarray(out).resize((Ww*8,Hh*8),Image.NEAREST).save(os.path.join(H,'model_%s_8x.png'%tag))
        np.save(os.path.join(H,'model_%s_bg.npy'%tag),~al)
        ys,xs=np.where(al); print(tag,'bbox',xs.min(),xs.max(),ys.min(),ys.max())
    print({k:int(m.sum()) for k,m in PMASK.items()})
