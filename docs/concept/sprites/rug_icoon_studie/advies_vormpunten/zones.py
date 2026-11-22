"""Proef: 'ontwerpzones' i.p.v. pixelblokken.
Front -> per ontwerpzone (vacht, oor-binnen, bef, geel motief, verre poot) een gladde maskerkaart
(outline/schaduwpixels tellen mee voor de zone eronder), per onderdeel getransformeerd met de a2-factoren
(lijf .38, kop .50, oren .56) en met supersampling gerasterd. Kleine kenmerkzones winnen bij lagere dekking.
Toon (licht/schaduw) komt uit de lichtheid van de front zelf, niet verzonnen. Oog = glyph op berekende plek.
python3 zones.py <uitnaam> [sigma] [motief_drempel]"""
import sys, numpy as np
from PIL import Image
from scipy import ndimage as nd
R='/home/user/Pokemon-Fully-Ungrounded/'; D=R+'docs/concept/sprites/viscacha/'; O=sys.path[0]+'/'
naam=sys.argv[1]; SIG=float(sys.argv[2]) if len(sys.argv)>2 else 0.7; MD=float(sys.argv[3]) if len(sys.argv)>3 else 0.3
fr=np.array(Image.open(D+'af/viscacha.png'))[:64]
FP=np.array([[int(v) for v in l.split()[:3]] for l in open(D+'af/normal.pal').read().split('\n')[3:19]])
IP=np.array([[int(v) for v in l.split()[:3]] for l in open(R+'graphics/pokemon/icon_palettes/pal2.pal').read().split('\n')[3:19]])
lab=np.load(D+'icoon/onderdelen/delen.npy'); sys.path.insert(0,D+'icoon/onderdelen'); import delen as Dl
names=[d[0] for d in Dl.DELEN]
# --- per soort: welke frontindexen horen bij welke ontwerpzone (1 regel, door Claude uit het palet, Jordi checkt 1x)
ZONES={'vacht':[3,4,5,11],'oorbinnen':[12],'bef':[6,7],'motief':[8,9,10],'verrepoot':[14]}
ZKLEUR={'vacht':(7,6),'oorbinnen':(6,6),'bef':(3,2),'motief':(9,8),'verrepoot':(6,6)}  # (licht, schaduw) in pal2
ZPRIO={'vacht':1.0,'oorbinnen':1.3,'bef':1.2,'motief':1.8,'verrepoot':1.0}   # kenmerken winnen eerder
lijn=np.isin(fr,[1,2,15,13])
# lijnpixels krijgen de zone van de dichtstbijzijnde niet-lijnpixel (zones lopen door onder de omlijning)
zid=np.full(fr.shape,-1); ZN=list(ZONES)
for i,z in enumerate(ZN): zid[np.isin(fr,ZONES[z])]=i
_,(iy,ix)=nd.distance_transform_edt(zid<0,return_indices=True); zfull=zid[iy,ix]; zfull[fr==0]=-1
zfull[fr==15]=-1  # snorharen apart
lum=FP.mean(1)[fr]; lum=np.where(lijn|(fr==0),np.nan,lum)
# gladde maskers
def glad(m): return nd.gaussian_filter(m.astype(float),SIG) if SIG>0 else m.astype(float)
ZM={z:glad(zfull==i) for i,z in enumerate(ZN)}
lumf=np.nan_to_num(lum,nan=0); w=(~np.isnan(lum)).astype(float); LUM=nd.gaussian_filter(lumf,1.0)/np.maximum(nd.gaussian_filter(w,1.0),1e-3)
s_l,s_k,s_o=.38,.50,.56; KOP={'kop','verre oor','nabije oor','elektrisch motief'}
NEK=np.array([21.0,38.0]); OFF=np.array([12.0,8.0]); H,W=40,48
ORDE=['verre achterpoot','romp','dij en achtervoet','voorpoot','bef','opgeheven poot','verre oor','kop','elektrisch motief','nabije oor']
DUN={'verre oor','nabije oor','voorpoot','verre achterpoot','opgeheven poot','dij en achtervoet'}
def sc(n): return s_o if 'oor' in n else (s_k if n in KOP else s_l)
def naar(p,n):
    s=sc(n); return OFF+NEK*s_l+(np.array(p)-NEK)*s if n in KOP else OFF+np.array(p)*s_l
def bron(q,n):
    s=sc(n); q=q-OFF; return NEK+(q-NEK*s_l)/s if n in KOP else q/s_l
def samp(img,pts):
    return nd.map_coordinates(img,[pts[:,1]-.5,pts[:,0]-.5],order=1,mode='constant')
SS=4; sub=(np.arange(SS)+.5)/SS; gx,gy=np.meshgrid(sub,sub); sub=np.stack([gx.ravel(),gy.ravel()],1)
col=np.zeros((H,W),np.uint8); part=np.full((H,W),-1); tone=np.zeros((H,W))
for r,n in enumerate(ORDE):
    ids=[i for i,m in enumerate(names) if m==n]; pm=glad(np.isin(lab,ids)&(fr!=15)&(fr>0))
    if n in DUN: pm=np.maximum(pm,glad(nd.binary_dilation(np.isin(lab,ids)&(fr>0)&(fr!=15))))*0.5+pm*0.5
    for Y in range(H):
        for X in range(W):
            pts=np.array([bron(np.array([X,Y])+s,n) for s in sub])
            cov=samp(pm,pts).mean()
            if cov<(0.4 if n in DUN else 0.5): continue
            best,bz=0,None
            for z in ZN:
                c=samp(ZM[z],pts).mean()*ZPRIO[z]
                if z=='motief' and c/ZPRIO[z]>=MD: c+=1
                if c>best: best,bz=c,z
            if bz is None: continue
            lt=samp(LUM,pts).mean(); col[Y,X]=ZN.index(bz)+1; part[Y,X]=r; tone[Y,X]=lt
out=np.zeros((H,W),np.uint8)
for Y in range(H):
    for X in range(W):
        if part[Y,X]<0: continue
        z=ZN[col[Y,X]-1]; li,sh=ZKLEUR[z]
        # schaduw waar de front zelf donker is (drempel per zone uit de front: onderste 30%)
        out[Y,X]=li
fz=np.zeros_like(tone)
for i,z in enumerate(ZN):
    m=col==i+1
    if m.sum()<4: continue
    t=np.percentile(tone[m],32)
    li,sh=ZKLEUR[z]; out[m&(tone<t)]=sh
# verre delen donker (diepte)
for n in ['verre oor','verre achterpoot']:
    out[(part==ORDE.index(n))&(out==7)]=6
# lijn tussen onderdelen (verre kant krijgt de lijn)
m=part>=0; res=out.copy()
for Y in range(H):
    for X in range(W):
        if not m[Y,X]: continue
        for dy,dx in ((0,1),(1,0),(0,-1),(-1,0)):
            yy,xx=Y+dy,X+dx
            if 0<=yy<H and 0<=xx<W and part[yy,xx]>part[Y,X] and ORDE[part[Y,X]] not in('bef','elektrisch motief') and ORDE[part[yy,xx]] not in('bef','elektrisch motief') and not(ORDE[part[Y,X]]=='kop' and 'oor' in ORDE[part[yy,xx]]):
                res[Y,X]=14; break
# oog-glyph: front-oog = zwart 2-3 px met witte glans -> icoon 'f3'-achtig: zwart blok 2x1 met glans in bovenrij
eye_f=np.argwhere(fr==13); ey,ex=eye_f.mean(0)  # glanspixel in de front
# zwart oog in de front: de 1-pixels rond de glans
blk=np.argwhere((fr==1)&(np.abs(np.arange(64)[:,None]-ey)<=2)&(np.abs(np.arange(64)[None,:]-ex)<=3))
cy,cx=blk.mean(0); e=naar((cx+.5,cy+.5),'kop'); g=naar((ex+.5,ey+.5),'kop')
EX,EY=int(np.floor(e[0])),int(np.floor(e[1])); GX,GY=int(np.floor(g[0])),int(np.floor(g[1]))
for (x,y,v) in [(EX-1,EY,15),(EX,EY,3),(EX-1,EY+1,15),(EX,EY+1,15)]: res[y,x]=v
print('oog front',(cx,cy),'glans',(ex,ey),'-> icoon',(EX,EY),'glans',(GX,EY))
# snorharen: front-snorpixels als dunne lijnen meeschalen met de kop (1 px), alleen buiten het lijf
lb,nw=nd.label(fr==15,structure=np.ones((3,3)))
def bres(a,b):
    (x0,y0),(x1,y1)=a,b; n=max(abs(x1-x0),abs(y1-y0))
    return [(int(round(x0+(x1-x0)*t/max(n,1))),int(round(y0+(y1-y0)*t/max(n,1)))) for t in range(n+1)]
for k in range(1,nw+1):
    P=np.argwhere(lb==k)[:,::-1]
    if len(P)<3: continue
    d=((P[:,None]-P[None])**2).sum(-1); i,j=np.unravel_index(d.argmax(),d.shape)
    a,b=[naar(P[q]+.5,'kop') for q in (i,j)]
    for X,Y in bres((int(a[0]),int(a[1])),(int(b[0]),int(b[1]))):
        if 0<=X<W and 0<=Y<H and part[Y,X]<0: res[Y,X]=1
# staart uit v8 (Jordi: perfect), zoals bouw2
v8=np.array(Image.open(D+'icoon/maker/icon_v8.png'))[:32]
T=[(x,y,v8[y,x]) for y in range(0,23) for x in range(22,32) if v8[y,x]]
yt=int(round(OFF[1]+44*s_l)); row=np.nonzero(m[yt])[0]; xr=row.max()
for x,y,v in T:
    X,Y=x+xr-23,y+yt-22
    if 0<=Y<H and 0<=X<W and not m[Y,X]: res[Y,X]=v
# naar 32x32 en buitenrand
ys,xs=np.nonzero(res); c=res[ys.min():ys.max()+1,xs.min():xs.max()+1]; h,w=c.shape
o=np.zeros((32,32),np.uint8); oy,ox=30-h,16-w//2; o[oy:oy+h,ox:ox+w]=c
mm=(o>0)&(o!=1); pad=np.pad(mm,1); edge=mm&~(pad[:-2,1:-1]&pad[2:,1:-1]&pad[1:-1,:-2]&pad[1:-1,2:])
yy,_=np.nonzero(mm); mid=(yy.min()+yy.max())/2
for y,x in zip(*np.nonzero(edge)):
    if o[y,x] not in (8,9,15,3): o[y,x]=15 if y<mid else 14
im=Image.fromarray(o,'P'); im.putpalette(IP.flatten().tolist()); im.save(O+naam+'.png'); print(naam,w,'x',h)
