# Schrappen (GEMINI.md, Gengas/Alphyena: "schrappen, niet hertekenen"): 75x85 natief -> 56x64 door 19 kolommen en 21 rijen weg te
# laten (schaal 0,753, gelijk in x en y). Eén schrapping per gelijk stuk (verhoudingen blijven), binnen het stuk de rij/kolom die het
# meest op zijn buur lijkt. Verschil met gezichts-/hemdklassen (oog, hemd, knoopjes) en in de gezichtszone weegt 10x.
# Elke overgebleven pixel is een modelpixel.
import numpy as np
GEZ=np.zeros((85,75),bool); GEZ[16:29,26:49]=True
def kosten(c,axis):
    w=np.where(np.isin(c,(4,5,11)),10,1); w=np.where(GEZ,np.maximum(w,10),w)
    A=c if axis==0 else c.T; W=w if axis==0 else w.T
    return np.array([((A[i]!=A[i+1])*np.maximum(W[i],W[i+1])).sum() for i in range(len(A)-1)])
def kies(c,n,axis,verboden=()):
    k=kosten(c,axis); N=c.shape[axis]; grenzen=np.linspace(0,N,n+1)
    gek=[]
    for s in range(n):
        lo,hi=int(np.ceil(grenzen[s])),int(np.floor(grenzen[s+1]))
        r=0
        while True:
            kand=[i for i in range(max(1,lo-r),min(hi+r,N-1)) if i not in verboden and i not in gek and all(abs(i-j)>=2 for j in gek)]
            if kand: break
            r+=1
        gek.append(min(kand,key=lambda i:(k[i],abs(i-(lo+hi)/2))))
    return gek,k
VR=set(range(18,23)); VK=set()
def schrap(c,nr=21,nk=19):
    rows,kr=kies(c,nr,0,VR); cols,kk=kies(c,nk,1,VK)
    return np.delete(np.delete(c,rows,0),cols,1),rows,cols,kr,kk
# Variant: samenvoegen i.p.v. weglaten. De geschrapte rij/kolom valt samen met de buur die er het meest op lijkt; per pixel wint
# de omlijning (K), dan oog/hemd (e, w, g), dan donkerrood (lijn), dan de buur zelf; achtergrond verliest van figuur.
# Zo blijven 1-px lijnen (antennes, vinger, randen) die toevallig in een geschrapte rij/kolom liggen bewaard. Elke pixel = modelpixel.
PRIO={1:5,11:4,5:4,4:4,6:3}
def _comb(t,o):
    r=t.copy()
    for i in range(len(t)):
        a,b=t[i],o[i]
        if a==0 and b!=0: r[i]=b
        elif b!=0 and PRIO.get(b,0)>PRIO.get(a,0): r[i]=b
    return r
def _merge(c,idx):
    c=c.copy(); weg=[]
    for i in sorted(idx):
        kand=[j for j in (i-1,i+1) if 0<=j<len(c) and j not in idx]
        j=min(kand,key=lambda j:(c[j]!=c[i]).sum())
        c[j]=_comb(c[j],c[i]); weg.append(i)
    return np.delete(c,weg,0)
def schrap_merge(c,nr=21,nk=19):
    rows,_=kies(c,nr,0,VR); cols,_=kies(c,nk,1,VK)
    s=_merge(c,rows); s=_merge(s.T,cols).T
    return s,rows,cols
