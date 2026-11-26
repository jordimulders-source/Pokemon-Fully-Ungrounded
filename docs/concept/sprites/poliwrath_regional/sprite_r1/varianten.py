# Varianten r1: basis + mond (recht) + ogen (O1 model / O2 Gen 3-Poliwrath naar verhouding) + spiraal (S1 model / S2 regionale Poliwhirl af).
import numpy as np; from PIL import Image
exec(open('basis.py').read())
ROOT='../../../../../'
pwr=np.array(Image.open(ROOT+'graphics/pokemon/poliwrath/anim_front_gba.png'))[:64]
phr=np.array(Image.open('../../poliwhirl_regional/af/poliwhirl_regional.png'))
def buurgeel(o,m):
    # vul cellen in m met de meest voorkomende geeltint van hun niet-m-buren (herhaald tot alles gevuld is)
    m=m.copy()
    while m.any():
        nxt=m.copy()
        for y,x in zip(*np.where(m)):
            nb=[o[y+a,x+b] for a,b in ((1,0),(-1,0),(0,1),(0,-1)) if 0<=y+a<H and 0<=x+b<W and not m[y+a,x+b] and o[y+a,x+b] in (5,6,7)]
            if nb: o[y,x]=max(set(nb),key=nb.count); nxt[y,x]=False
        if (nxt==m).all(): break
        m=nxt
# --- MOND (toegestane afwijking): modelglimlach -> geel, rechte rode lijn op de hoogte van het midden van de modelmond
MONDZ=(jj>=12)&(jj<=17)&(ii>=14)&(ii<=42)&(cls==2)
MONDY=16; MONDX=(15,41)     # midden modelmond: rij 16 (x 20-32); breedte = modelmond van mondhoek tot mondhoek
# --- SPIRAAL
SPZ=(jj>=24)&(jj<=39)&(ii>=19)&(ii<=40)
spr=SPZ&(cls==2); sy_,sx_=np.where(spr)
SPC=((sx_.min()+sx_.max())/2,(sy_.min()+sy_.max())/2)
pr_red=np.isin(phr,[12,13,14]); AFZ=np.zeros((64,64),bool); AFZ[31:42,24:36]=True   # spiraal in de af-sprite (rood x 24-35, y 31-41)
ry,rx=np.where(pr_red&AFZ)
PH_BB=(rx.min(),rx.max(),ry.min(),ry.max()); PHC=((rx.min()+rx.max())/2,(ry.min()+ry.max())/2)
def spiraal(o,v):
    if v=='S1':
        # modelspiraal uit de reductie: rood blijft zoals het is (tinten per cel), niets veranderd
        return
    # S2: modelrood in de buik -> geel (uit de omgeving), dan de spiraal van de regionale Poliwhirl (af) 1-op-1 gecentreerd
    buurgeel(o,spr)
    dx=int(np.floor(SPC[0]-PHC[0]+0.5)); dy=int(np.floor(SPC[1]-PHC[1]+0.5))
    x0,x1,y0,y1=PH_BB
    for y in range(y0,y1+1):
        xr=np.where(pr_red[y]&AFZ[y])[0]
        if len(xr)==0: continue
        for x in range(xr.min(),xr.max()+1):      # per rij van het eerste tot het laatste rood: spiraal + geel ertussen
            p=phr[y,x]
            if p in (5,6,7,12,13,14): o[y+dy,x+dx]=p
    return (x0+dx,x1+dx,y0+dy,y1+dy)
# --- OGEN
def ogen(o,v):
    if v=='O1':
        # modelogen uit de reductie, technisch opgeschoond: wit/grijs -> 8/9, zwart/donker -> 1 (pupil en ring)
        for (y0,y1,x0,x1) in [(5,10,16,20),(4,10,32,40)]:
            for y in range(y0,y1+1):
                for x in range(x0,x1+1):
                    if cls[y,x]==3: o[y,x]=8 if lum[y,x]>=200 else 9
                    elif cls[y,x]==4 and lum[y,x]<40: o[y,x]=1
        return
    # O2: Gen 3-Poliwrath-ogen, 1 kolom en 1 rij geschrapt (verhouding oog/kop: Poliwrath 8/33, kop hier 29 breed)
    for (bx0,bx1,by0,by1,rand,tx,ty,scol,srow) in OOGPLAN:
        sub=pwr[by0:by1+1,bx0:bx1+1].copy()
        sub=np.delete(np.delete(sub,[srow-by0],0),[scol-bx0],1)
        h,w=sub.shape
        wit=np.isin(sub,[1,2,3])
        for j in range(h):
            for i in range(w):
                p=sub[j,i]; q=None
                if p==1: q=8
                elif p in (2,3): q=9
                elif p==0xa: q=1
                elif p==0xe: q=1
                elif p==0xc and any(0<=j+a<h and 0<=i+b<w and wit[j+a,i+b] for a,b in ((1,0),(-1,0),(0,1),(0,-1))): q=1
                if q is not None:
                    X=tx+i if rand=='L' else tx-(w-1)+i
                    o[ty+j,X]=q
# bron-vensters (x0,x1,y0,y1) in poliwrath gba, buitenrand-kant, doel-buitenrand x, doel-bovenrij, geschrapte kolom/rij
OOGPLAN=[(21,28,14,19,'L',16,5,23,17),     # linkeroog: buitenrand links -> modeloog buitenrand x16
         (38,46,14,19,'R',40,5,44,17)]     # rechteroog: buitenrand rechts -> modeloog buitenrand x40
BASIS=out.copy()
def maak(sv,ov):
    o=BASIS.copy()
    buurgeel(o,MONDZ)
    for x in range(MONDX[0],MONDX[1]+1): o[MONDY,x]=13
    spiraal(o,sv); ogen(o,ov)
    return o
