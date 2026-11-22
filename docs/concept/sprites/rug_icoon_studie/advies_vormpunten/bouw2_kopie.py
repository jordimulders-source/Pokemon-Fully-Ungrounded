"""Onderlaag v2: per onderdeel verkleind (vaste factoren), maar als icoon opgebouwd:
- vlakken = gemiddelde kleur van de NIET-donkere frontpixels van dat onderdeel (geen lijnblur);
- dunne delen (poten, oren) eerst 1 px verdikt in de front, zodat ze als stompjes overblijven;
- lijnen getekend op de grenzen: buitenrand (boven 15, onder 14) en tussen onderdelen (onderdeel achter -> lijn);
- oog = donker blokje + 1 witte pixel + bruin ooglid op de omgerekende plek van het front-oog;
- snorharen = 1-px lijntjes; staart pixel voor pixel uit v8.
python3 bouw2.py naam s_lijf s_kop s_oren"""
import sys,numpy as np
from PIL import Image
sys.path.insert(0,'docs/concept/sprites/viscacha/icoon/onderdelen'); import delen as Dl
D='docs/concept/sprites/viscacha/'
naam,s_l,s_k,s_o=sys.argv[1],float(sys.argv[2]),float(sys.argv[3]),float(sys.argv[4])
fr=np.array(Image.open(D+'af/viscacha.png'))[:64]; L=open(D+'af/normal.pal').read().split('\n'); FP=np.array([[int(v) for v in L[3+k].split()[:3]] for k in range(16)])
rgb=FP[fr].astype(float); lab=np.load(D+'icoon/onderdelen/delen.npy'); names=[d[0] for d in Dl.DELEN]
donker=FP.mean(1)[fr]<75
snor=(fr==15)   # snorhaarkleur: niet als vlak meenemen
geel=np.isin(fr,[8,9,10,11])
IP=np.array([[int(v) for v in l.split()[:3]] for l in open('graphics/pokemon/icon_palettes/pal2.pal').read().split('\n')[3:19]])
KOP={'kop','verre oor','nabije oor','elektrisch motief'}; DUN={'verre oor','nabije oor','voorpoot','verre achterpoot','opgeheven poot','dij en achtervoet'}
NEK=np.array([21.0,38.0]); OFF=np.array([12.0,8.0]); H,W=40,48
def dil(m):
    p=np.pad(m,1); return m|p[:-2,1:-1]|p[2:,1:-1]|p[1:-1,:-2]|p[1:-1,2:]
def naar(x,y,n):
    s=s_o if 'oor' in n else s_k
    if n in KOP: return OFF+NEK*s_l+(np.array([x,y])-NEK)*s
    return OFF+np.array([x,y])*s_l
def bron(X,Y,n):
    s=s_o if 'oor' in n else (s_k if n in KOP else s_l); q=np.array([X+.5,Y+.5])-OFF
    c=NEK+(q-NEK*s_l)/s if n in KOP else q/s_l
    return c,1/s
ORDE=['verre achterpoot','romp','dij en achtervoet','voorpoot','bef','opgeheven poot','verre oor','kop','elektrisch motief','nabije oor']
col=np.zeros((H,W),np.uint8); part=np.full((H,W),-1)
for r,n in enumerate(ORDE):
    ids=[i for i,m in enumerate(names) if m==n]; pm=np.isin(lab,ids)
    pm=pm&~snor
    pmd=dil(pm)&(fr>0)&~snor if n in DUN else pm
    for Y in range(H):
        for X in range(W):
            (cx,cy),k=bron(X,Y,n)
            x0,y0=int(np.floor(cx-k/2)),int(np.floor(cy-k/2)); x1,y1=int(np.ceil(cx+k/2)),int(np.ceil(cy+k/2))
            x0,y0,x1,y1=max(0,x0),max(0,y0),min(64,x1),min(64,y1)
            if x1<=x0 or y1<=y0: continue
            sel=pmd[y0:y1,x0:x1]
            if sel.mean()<0.4: continue
            licht=pm[y0:y1,x0:x1]&~donker[y0:y1,x0:x1]
            if not licht.any(): licht=pmd[y0:y1,x0:x1]&~donker[y0:y1,x0:x1]
            if not licht.any(): continue
            cc=rgb[y0:y1,x0:x1][licht]
            # meest voorkomende tint i.p.v. gemiddelde: geen mengkleuren
            idx=((IP[None,1:14]-cc[:,None])**2).sum(-1).argmin(1)+1
            g=geel[y0:y1,x0:x1][licht]
            if n=='elektrisch motief' and g.mean()>=0.3: idx=idx[g]
            col[Y,X]=np.bincount(idx).argmax(); part[Y,X]=r
# lijnen: buitenrand en grens met een onderdeel dat ervoor ligt
out=col.copy(); m=part>=0
for Y in range(H):
    for X in range(W):
        if not m[Y,X]: continue
        for dy,dx in ((0,1),(1,0),(0,-1),(-1,0)):
            yy,xx=Y+dy,X+dx
            if not(0<=yy<H and 0<=xx<W) or part[yy,xx]<0: continue
            if part[yy,xx]>part[Y,X] and ORDE[part[Y,X]]!='bef' and ORDE[part[yy,xx]] not in ('bef','elektrisch motief'):
                out[Y,X]=15; break
# oog: front-oog rond (15,30) -> blokje 2 donker + witte pixel, ooglid erboven
e=naar(15.5,30.5,'kop'); ex,ey=int(e[0]),int(e[1])
for (x,y,v) in [(ex-1,ey-1,6),(ex,ey-1,6),(ex+1,ey-1,6),(ex-1,ey,15),(ex,ey,15),(ex+1,ey,3),(ex-1,ey+1,15),(ex,ey+1,15),(ex+1,ey+1,15)]:
    if 0<=y<H and 0<=x<W and m[y,x]: out[y,x]=v
# staart uit v8
v8=np.array(Image.open(D+'icoon/maker/icon_v8.png'))[:32]
T=[(x,y,v8[y,x]) for y in range(0,23) for x in range(22,32) if v8[y,x]]
yt=int(round(OFF[1]+44*s_l)); row=np.nonzero(m[yt])[0]; xr=row.max() if len(row) else 30
for x,y,v in T:
    X,Y=x+xr-23,y+yt-22
    if 0<=Y<H and 0<=X<W and not m[Y,X]: out[Y,X]=v
# snorharen: 1-px lijntjes van de snuitpunt schuin naar links
ys,xs=np.nonzero(m); sn_y=int(naar(6,36,'kop')[1]); sn_x=xs[ys==sn_y].min() if (ys==sn_y).any() else xs.min()
for (dx,dy) in [(-1,0),(-2,0),(-3,1),(-1,1),(-2,2)]:
    X,Y=sn_x+dx,sn_y+dy
    if 0<=X<W and 0<=Y<H and out[Y,X]==0: out[Y,X]=1
# naar 32x32
ys,xs=np.nonzero(out); c=out[ys.min():ys.max()+1,xs.min():xs.max()+1]; h,w=c.shape
res=np.zeros((32,32),np.uint8); oy,ox=30-h,16-w//2
res[max(0,oy):oy+h,max(0,ox):ox+w]=c[max(0,-oy):,max(0,-ox):]
mm=(res>0)&(res!=1); pad=np.pad(mm,1); edge=mm&~(pad[:-2,1:-1]&pad[2:,1:-1]&pad[1:-1,:-2]&pad[1:-1,2:])
yy,_=np.nonzero(mm); mid=(yy.min()+yy.max())/2
for y,x in zip(*np.nonzero(edge)):
    if res[y,x] not in (8,9): res[y,x]=15 if y<mid else 14
im=Image.fromarray(res,'P'); im.putpalette(IP.flatten().tolist()); im.save('/tmp/claude-0/-home-user-Pokemon-Fully-Ungrounded/9987886b-1e4e-57fe-95d6-00d02ead3dd5/scratchpad/advies_icoon/'+naam+'.png'); np.save('/tmp/claude-0/-home-user-Pokemon-Fully-Ungrounded/9987886b-1e4e-57fe-95d6-00d02ead3dd5/scratchpad/advies_icoon/'+naam+'_off.npy',np.array([ys.min(),xs.min(),oy,ox])); print(naam,w,'x',h)
