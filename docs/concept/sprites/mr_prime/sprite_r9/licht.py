# Volume per vorm (alleen tinten op bestaande pixels): lichtbron linksboven-voor. Per onderdeel (masker van bestaande
# pixels) een hoogteveld = wortel van de afstand tot de rand van het onderdeel (bol, zoals een kussen van stof), daarvan
# de normaal, belicht met L = linksboven + naar de kijker. De helderste pixels liggen dus binnen de vorm, verschoven naar
# linksboven (bolling), de donkerste als sikkel rechtsonder. Tinten per onderdeel op aandeel (geen effen vlakken).
import numpy as np
def afstand(M):
    H,W=M.shape; INF=99.; d=np.where(M,INF,0.)
    for _ in range(2):
        for y in range(H):
            for x in range(W):
                if not M[y,x]: continue
                for dy,dx,c in ((-1,0,1),(0,-1,1),(-1,-1,1.414),(-1,1,1.414)):
                    yy,xx=y+dy,x+dx
                    v=d[yy,xx] if 0<=yy<H and 0<=xx<W else 0.
                    d[y,x]=min(d[y,x],v+c)
        for y in range(H-1,-1,-1):
            for x in range(W-1,-1,-1):
                if not M[y,x]: continue
                for dy,dx,c in ((1,0,1),(0,1,1),(1,1,1.414),(1,-1,1.414)):
                    yy,xx=y+dy,x+dx
                    v=d[yy,xx] if 0<=yy<H and 0<=xx<W else 0.
                    d[y,x]=min(d[y,x],v+c)
    return d
def belichting(M,L=(-0.55,-0.6,0.58),macht=0.5,schaal=1.0,glad=2):
    d=afstand(M); h=np.where(M,(d/ max(d.max(),1))**macht*schaal*max(d.max(),1)**macht,0.)
    for _ in range(glad):   # gladstrijken van het hoogteveld (geen ribbels langs de middellijn)
        p=np.pad(h,1); h2=sum(p[1+dy:1+dy+h.shape[0],1+dx:1+dx+h.shape[1]] for dy in (-1,0,1) for dx in (-1,0,1))/9.
        h=np.where(M,h2,0.)
    gy,gx=np.gradient(h)
    n=np.stack([-gx,-gy,np.ones_like(h)],-1); n/=np.linalg.norm(n,axis=-1,keepdims=True)
    Lv=np.array([L[0],L[1],L[2]]); Lv=Lv/np.linalg.norm(Lv)
    return (n[...,0]*Lv[0]+n[...,1]*Lv[1]+n[...,2]*Lv[2])
def schaduw(C,M,aandeel,toon,zone,zet,vorm=None,**kw):
    """aandeel: fracties (donker..licht) per toon, bv (0.25,0.4,0.25,0.1) voor tonen (2,3,4,5)"""
    I=belichting(M if vorm is None else vorm,**kw); v=np.sort(I[M]); n=len(v); grens=[]; acc=0
    for f in aandeel[:-1]:
        acc+=f; grens.append(v[min(n-1,int(acc*n))])
    for y,x in zip(*np.where(M)):
        k=sum(I[y,x]>=g for g in grens); zet(zone,y,x,toon[k])
