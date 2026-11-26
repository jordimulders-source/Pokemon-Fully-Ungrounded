# Basis r1: geschrapt (gespiegeld) model -> tinten uit de modelhelderheid per cel (A) + omlijning met licht van linksboven (B).
# Ogen, mond en spiraal komen als bovenlaag in varianten.py.
import numpy as np
from mat import mat as cls, L as lum, H, W
cls=cls.copy()
jj,ii=np.mgrid[0:H,0:W]
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
# zones (gemeten op de materiaalkaart, mat.py)
FIST=((jj>=19)&(jj<=36)&(ii<=15)) | ((jj>=19)&(jj<=35)&(ii>=39)&(ii<=55))   # vuisten (handschoenen)
EYEZ=(jj>=3)&(jj<=10)&(ii>=14)&(ii<=41)
ICE=((cls==3)|(cls==2))&~EYEZ&~((jj>=12)&(jj<=40)&(ii>=13)&(ii<=42))       # ijs + cinnaber, zonder ogen/mond/spiraal
glove=ICE&FIST&(cls==3)
crys=ICE&~glove
out=np.zeros((H,W),'uint8')
Y=cls==1; K=cls==4; I=cls==3; Rd=cls==2
# A: tinten per cel uit de modelhelderheid (drempels uit de histogrammen van het model)
def blur(v,m,s):
    r=max(1,int(3*s)); k=np.exp(-np.arange(-r,r+1)**2/(2*s*s))
    num=np.where(m,v,0.0); den=m.astype(float)
    for ax in (0,1):
        num=np.apply_along_axis(lambda x:np.convolve(x,k,'same'),ax,num)
        den=np.apply_along_axis(lambda x:np.convolve(x,k,'same'),ax,den)
    return num/np.maximum(den,1e-6)
SIG_K,SIG_Y=1.0,0.6     # lijf licht gladgestreken zoals bij de Poliwhirl (sigma 1,0 cel); geel minder, zodat de modelschaduwlijnen blijven
sb=blur(lum,K,SIG_K); out[K]=np.select([sb[K]>=56,sb[K]>=30],[4,3],2)
sy=blur(lum,Y,SIG_Y); out[Y]=np.select([sy[Y]>=196,sy[Y]>=156],[5,6],7)
out[I]=np.select([lum[I]>=222,lum[I]>=195,lum[I]>=150],[8,9,10],11)
out[Rd]=np.select([lum[Rd]>=125,lum[Rd]>=92],[12,13],14)
KAAL=out.copy()
# B: omlijning (rand = naast lucht); lichtkant per pixel uit de 3x3-luchtburen, licht van linksboven (na het spiegelen opnieuw bepaald)
def lucht(y,x): return y<0 or x<0 or y>=H or x>=W or out[y,x]==0
o=out.copy(); RAND=np.zeros((H,W),bool); SCHAD=np.zeros((H,W),bool)
for y in range(H):
    for x in range(W):
        v=out[y,x]
        if v==0 or not (lucht(y-1,x) or lucht(y+1,x) or lucht(y,x-1) or lucht(y,x+1)): continue
        sx=sum(dx for dy in (-1,0,1) for dx in (-1,0,1) if lucht(y+dy,x+dx)); sy=sum(dy for dy in (-1,0,1) for dx in (-1,0,1) if lucht(y+dy,x+dx))
        schaduw=(sx+sy)>0; RAND[y,x]=True; SCHAD[y,x]=schaduw
        if v in (2,3,4): o[y,x]=1
        elif v in (5,6,7): o[y,x]=1 if schaduw else 7
        elif glove[y,x]: o[y,x]=1 if schaduw else 11
        elif v in (8,9,10,11): o[y,x]=15 if schaduw else 11
        elif v in (12,13,14): o[y,x]=1 if schaduw else 14
out=o
# C: reparaties per pixel
FIX={(22,13):7}   # (x,y) neusgat links: modelcel donker-olijf (lum 58) viel in de lijfklasse -> 7 zoals het rechterneusgat en de Poliwhirl
for (x,y),v in FIX.items(): out[y,x]=v
# ruis: losse tintpixel (geen gelijke 4-buur) in lijf 3/4 en geel 5/6 -> meest voorkomende buurtint uit dezelfde groep (>=2 buren);
# 2 en 7 blijven (dat zijn de binnen-/schaduwlijnen van het model). Niet in ogen/mond/spiraal.
GRP={3:(2,3,4),4:(2,3,4),5:(5,6,7),6:(5,6,7)}
VRIJ=((jj>=3)&(jj<=11)&(ii>=14)&(ii<=42))|((jj>=12)&(jj<=17)&(ii>=14)&(ii<=42))|((jj>=24)&(jj<=39)&(ii>=19)&(ii<=40))
RUIS=[]
for y in range(H):
    for x in range(W):
        v=out[y,x]
        if v not in GRP or VRIJ[y,x] or (x,y) in FIX: continue
        nb=[out[y+a,x+b] for a,b in ((1,0),(-1,0),(0,1),(0,-1)) if 0<=y+a<H and 0<=x+b<W]
        if v in nb: continue
        same=[n for n in nb if n in GRP[v]]
        if len(same)>=2: out[y,x]=max(set(same),key=same.count); RUIS.append((x,y))
