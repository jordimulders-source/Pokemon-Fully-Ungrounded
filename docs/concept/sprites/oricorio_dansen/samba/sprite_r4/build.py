# Volgorde: natief.py -> km.py -> reduce.py 2.9 0 0.97 -> plaats.py -> lijnen.py -> build.py -> render.py -> vel.py
# basis.npy (kale onderlaag) + lijnkaart.npy (modellijnen, kam-detectie) -> samba_kls.npy, met telling per stap in log.json
import numpy as np, json
from collections import Counter
from palet import NAMEN
I={n:i for i,n in enumerate(NAMEN)}
_,O,G1,G2,G3,G4,Y1,Y2,Y3,B1,B2,K1,K2,K3,W=range(15)
basis=np.load('basis.npy'); o=basis.copy(); H=W_=64; log={}
LK=np.load('lijnkaart.npy'); SC=np.load('lijnscore.npy'); LF=np.load('lijnfam64.npy')
def tel(k,n=1): log[k]=log.get(k,0)+n
def nb4(y,x): return [(y+dy,x+dx) for dy,dx in((-1,0),(1,0),(0,-1),(0,1)) if 0<=y+dy<H and 0<=x+dx<W_]
def nb8(y,x): return [(y+dy,x+dx) for dy in(-1,0,1) for dx in(-1,0,1) if (dy or dx) and 0<=y+dy<H and 0<=x+dx<W_]
def tr(y,x): return not(0<=y<H and 0<=x<W_) or o[y,x]==0
def comps(mask,n8=False):
    seen=np.zeros(mask.shape,bool); out=[]
    for y in range(H):
        for x in range(W_):
            if mask[y,x] and not seen[y,x]:
                st=[(y,x)]; seen[y,x]=True; pts=[]
                while st:
                    a,b=st.pop(); pts.append((a,b))
                    for yy,xx in (nb8(a,b) if n8 else nb4(a,b)):
                        if mask[yy,xx] and not seen[yy,xx]: seen[yy,xx]=True; st.append((yy,xx))
                out.append(pts)
    return out
VUL=(G1,G2,G3,G4,Y1,Y2,Y3,B1,B2,K1,K2,K3)
def buurvul(y,x,uit=()):
    c=Counter(o[a,b] for a,b in nb8(y,x) if o[a,b] in VUL and o[a,b] not in uit)
    return c.most_common(1)[0][0] if c else None
# 1. lijnen uit de kale reductie (verdund, rommelig) eerst terug naar vulkleur (meest voorkomende vulbuur), 3 rondes
for it in range(3):
    for y,x in zip(*np.where(o==O)):
        v=buurvul(y,x)
        if v: o[y,x]=v; tel('1_reductielijn_naar_vul')
vul=o.copy()   # vulkaart zonder lijnen (bewaard voor de lijntint)
# 2. modellijnen (kam-detectie) erop
for y,x in zip(*np.where(LK&(o>0))): o[y,x]=O; tel('2_modellijn')
# 3. buitenrand dicht
for y in range(H):
    for x in range(W_):
        if o[y,x]>O and any(tr(a,b) for a,b in [(y-1,x),(y+1,x),(y,x-1),(y,x+1)]): o[y,x]=O; tel('3_buitenrand')
np.save('stap3.npy',o); np.save('vul.npy',vul)
d=(o!=basis); log['totaal_afwijkend']=int(d.sum()); json.dump(log,open('log.json','w'),indent=0); print(log)
np.save('samba_kls.npy',o)
