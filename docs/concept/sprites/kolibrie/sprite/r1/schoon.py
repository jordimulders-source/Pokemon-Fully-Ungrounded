# Opschonen naar Gen 3 op de kale reductie (vorm bevroren). Logt per zone het aantal gewijzigde pixels.
import sys,json,numpy as np; from PIL import Image
from palet import PAL
from check import rand
L=np.array([sum(c*w for c,w in zip(p,(0.3,0.6,0.1))) for p in PAL])
LICHT=[12,13,14]
def comps8(a,mask=None):
    H,W=a.shape; seen=np.zeros_like(a,bool); out=[]
    for y in range(H):
        for x in range(W):
            if a[y,x]==0 or seen[y,x]: continue
            v=a[y,x]; st=[(y,x)]; seen[y,x]=1; c=[]
            while st:
                p=st.pop(); c.append(p)
                for dy in (-1,0,1):
                    for dx in (-1,0,1):
                        q=(p[0]+dy,p[1]+dx)
                        if 0<=q[0]<H and 0<=q[1]<W and not seen[q] and a[q]==v: seen[q]=1; st.append(q)
            out.append((v,c))
    return out
def vleugeltoon(a,lum,zone,drempels=(187,225)):
    """lichte vleugelvlakken: gladde toonkaart van het model (3x3, midden telt dubbel) -> 3 tinten c/d/e"""
    H,W=a.shape; out=a.copy()
    for y,x in zip(*np.where(zone & np.isin(a,LICHT))):
        s=0;w=0
        for dy in (-1,0,1):
            for dx in (-1,0,1):
                yy,xx=y+dy,x+dx
                if 0<=yy<H and 0<=xx<W and zone[yy,xx] and a[yy,xx] in LICHT:
                    k=2 if dy==dx==0 else 1; s+=lum[yy,xx]*k; w+=k
        t=s/w; out[y,x]=12 if t<drempels[0] else (13 if t<drempels[1] else 14)
    return out
def vleugeldrempel(a,lum,zone,regels):
    """vleugelvlakken direct op de modeltoon (het model heeft schone banden/strepen): regels=[(bovengrens,index),...]"""
    out=a.copy()
    for y,x in zip(*np.where(zone & np.isin(a,LICHT+[4,11]))):
        t=lum[y,x]
        if t<110: continue
        for g,i in regels:
            if t<g: out[y,x]=i; break
    return out
def randlijn(a,zone,kleur=12):
    """lichte pixels (d/e) op de buitenrand van een licht onderdeel -> selout c (Venomoth: vleugelrand in middentint)"""
    out=a.copy(); r=rand(a)
    m=r&zone&np.isin(a,[13,14]); out[m]=kleur; return out
def spikkels(a,zone,beschermd):
    """losse vlakjes (<3 px, 8-buren) -> meest voorkomende 4-buur (geen zwart/transparant tenzij niets anders)"""
    out=a.copy()
    for v,c in comps8(a):
        if v==1 or len(c)>=3: continue
        for y,x in c:
            if not zone[y,x] or beschermd[y,x]: continue
            nb=[a[y+dy,x+dx] for dy,dx in ((1,0),(-1,0),(0,1),(0,-1)) if 0<=y+dy<64 and 0<=x+dx<64]
            nb=[n for n in nb if n not in (0,1,v)]
            if nb: out[y,x]=max(set(nb),key=nb.count)
    return out
def zones_log(a0,a1,Z):
    d=a0!=a1; res={k:int((d&m).sum()) for k,m in Z.items()}; res['totaal']=int(d.sum()); return res
def save(idx,path):
    im=Image.fromarray(idx.astype('uint8'),'P'); im.putpalette(sum(PAL,())); im.save(path,transparency=0)
def buitenlijn(a,zone,lijn=1,schaduwkant=((1,0),(0,1),(1,1),(1,-1))):
    """1 px buitenlijn: randpixel in zone dat aan de schaduwkant (onder/rechts) aan transparant grenst -> zwart.
    Lichtkant (boven/links) blijft selout uit het model."""
    out=a.copy(); H,W=a.shape
    for y,x in zip(*np.where(zone&(a>0)&(a!=lijn))):
        for dy,dx in schaduwkant:
            yy,xx=y+dy,x+dx
            if not(0<=yy<H and 0<=xx<W) or a[yy,xx]==0:
                # alleen als er geen lijn tussen zit: buur in tegengestelde richting is figuur
                out[y,x]=lijn; break
    return out
def oog(a,x,y,rest=2):
    """oog van frame 1 (glans boven-links, iris blauwgroen + licht blauwgroen) op (x,y)=glans"""
    a=a.copy(); a[y,x]=14; a[y+1,x]=9; a[y+1,x+1]=10; return a
def toonband(a,lum,zone,regels,glad=True):
    """donkere banden (staartkrul): gladde toonkaart van het model binnen de zone -> tinten volgens regels"""
    out=a.copy(); H,W=a.shape
    for y,x in zip(*np.where(zone&(a>0))):
        if glad:
            s=0;w=0
            for dy in (-1,0,1):
                for dx in (-1,0,1):
                    yy,xx=y+dy,x+dx
                    if 0<=yy<H and 0<=xx<W and zone[yy,xx] and a[yy,xx]>0:
                        k=2 if dy==dx==0 else 1; s+=lum[yy,xx]*k; w+=k
            t=s/w
        else: t=lum[y,x]
        for g,i in regels:
            if t<g: out[y,x]=i; break
    return out
