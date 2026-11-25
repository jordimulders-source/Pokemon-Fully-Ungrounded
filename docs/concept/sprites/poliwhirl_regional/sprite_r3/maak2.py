# r2: basis (geel voorrang) + ogen Gen 3-Poliwhirl op eigen pixelmaat (geen extra ring) + spiraal S1 of S2.
import numpy as np; from PIL import Image
import varianten as V
from s1 import pad, FEND
from palet import PAL
H,W=V.H,V.W; jj,ii=V.jj,V.ii
ROOT='../../../../../'
pw=V.pw
B=V.BASIS.copy()
# --- ogen: rond het oog de kop uit het model (MODELOOG); modelwit dat niet onder het nieuwe oog valt -> buur uit de kop
OOGZ=((ii>=11)&(ii<=21)|(ii>=24)&(ii<=34))&(jj<=9)
def oogmasker(c0,c1,r0,r1):
    sub=pw[r0:r1+1,c0:c1+1]; m0=np.isin(sub,[1,2,3,8,9,15]); m=np.zeros_like(m0)
    st=[(sub.shape[0]//2,sub.shape[1]//2)]
    while st:
        j,i=st.pop()
        if j<0 or i<0 or j>=m.shape[0] or i>=m.shape[1] or m[j,i] or not m0[j,i]: continue
        m[j,i]=True; st+=[(j+1,i),(j-1,i),(j,i+1),(j,i-1)]
    return sub,m
OOGEN=[((19,27,12,20),(16,4.5)),((36,46,12,20),(29,4.5))]
OOGTEL=[]
def ogen(o):
    o[OOGZ]=V.MODELOOG[OOGZ]
    geplakt=np.zeros((H,W),bool)
    for (c0,c1,r0,r1),(cx,cy) in OOGEN:
        sub,m=oogmasker(c0,c1,r0,r1); yy,xx=np.where(m)
        dx=int(round(cx-(xx.min()+xx.max())/2)); dy=int(round(cy-(yy.min()+yy.max())/2))
        for j,i in zip(yy,xx): o[j+dy,i+dx]=V.OOGMAP[sub[j,i]]; geplakt[j+dy,i+dx]=True
        OOGTEL.append((int(m.sum()),(xx.min()+c0,xx.max()+c0,yy.min()+r0,yy.max()+r0),(xx.min()+dx,xx.max()+dx,yy.min()+dy,yy.max()+dy)))
    # resten van het modeloog (wit/ijs) buiten de nieuwe ogen -> meest voorkomende niet-ijsbuur
    rest=OOGZ&~geplakt&np.isin(o,[8,9,10,11])&~V.crys
    for _ in range(4):
        for y,x in zip(*np.where(rest)):
            nb=[o[y+a,x+b] for a,b in ((1,0),(-1,0),(0,1),(0,-1)) if 0<=y+a<H and 0<=x+b<W and o[y+a,x+b] not in (0,8,9,10,11)]
            if nb: o[y,x]=max(set(nb),key=nb.count); rest[y,x]=False
    return geplakt
# --- spiraal
SPC=(22.5,23.5)
def s1(o):
    V.geel_onder(o); P=pad(*SPC,FEND)
    for x,y in P: o[y,x]=13
    return P
src=open('../../poliwag_regional/sprite_r1/build.py').read(); i=src.index('SPIRAAL={'); PWG=eval(src[i+8:src.index('}',i)+1])
WEG=[(12,31),(13,30)]   # buiteneinde Poliwag (2 donkerrode staartpixels) weg: einde stopt 2 rijen hoger, op (14,29)
def s2(o,dx=13,dy=-1):
    V.geel_onder(o); P=[]
    for (x,y),v in PWG.items():
        if (x,y) in WEG: continue
        o[y+dy,x+dx]=v; P.append((x+dx,y+dy))
    return P
def maak(sv):
    o=B.copy(); ogen(o); P=s1(o) if sv=='S1' else s2(o); return o,P
