# Onderlaag r1: Hauntflare-methode (oppervlak-middeling van het natieve model naar 64 breed) maar per kleurgroep:
# per spritepixel telt welke modelgroep het grootste oppervlak heeft (zwart/fel groen/bleek groen/roest/ijzer),
# en alleen die modelpixels worden gemiddeld en naar de modeltinten van die groep gekwantiseerd.
# Lijnbehoud: bedekt zwart >= LT van de cel, dan zwart (1-px lijnen zoals pupil en wenkbrauw vallen anders weg).
# Gebruik: python3 bouw.py [LT] [T] [out]
import sys, colorsys; from PIL import Image; import numpy as np
LT=float(sys.argv[1]) if len(sys.argv)>1 else 0.3
T=float(sys.argv[2]) if len(sys.argv)>2 else 0.5
OUT=sys.argv[3] if len(sys.argv)>3 else 'onderlaag.png'
LTO=float(sys.argv[4]) if len(sys.argv)>4 else LT   # lagere lijndrempel in de oogzone (pupillen zijn 1 modelpixel)
EZ=(11,37,42,52)
GT=float(sys.argv[7]) if len(sys.argv)>7 else 1.0   # drempel fel groen in de mondzone
MZ=(10,42,49,67)                                      # mondzone, natieve coordinaten                                     # oogzone, natieve coordinaten x0,x1,y0,y1
a=np.asarray(Image.open('../model/natief.png').convert('RGB')).astype(float)
wit=(a.min(2)>=0xe0)
ys,xs=np.where(~wit); x0,x1,y0,y1=xs.min(),xs.max()+1,ys.min(),ys.max()+1
a=a[y0:y1,x0:x1]; wit=wit[y0:y1,x0:x1]
def groep(p):
    r,g,b=p; h,l,s=colorsys.rgb_to_hls(r/255,g/255,b/255)
    if r+g+b<150: return 0                      # zwart (lijn)
    if g>r+20: return 1 if s>0.47 else 2         # fel groen / bleek groen
    if r>g+20: return 3                          # roest
    return 4                                     # ijzer
G=np.full(wit.shape,-1)
for y,x in zip(*np.where(~wit)): G[y,x]=groep(a[y,x])
TINTEN={0:1,1:2,2:3,3:3,4:3}
def kmeans(X,k,it=60):
    l=X.sum(1); c=np.array([X[(l>=np.quantile(l,i/k))&(l<=np.quantile(l,(i+1)/k))].mean(0) for i in range(k)])
    for _ in range(it):
        lab=((X[:,None]-c[None])**2).sum(2).argmin(1)
        c=np.array([X[lab==j].mean(0) if (lab==j).any() else c[j] for j in range(k)])
    return c[np.argsort(-c.sum(1))]
pal=[(0,0,0)]; gidx={}
for g,k in TINTEN.items():
    X=a[G==g]; uniq=np.unique(X,axis=0)
    for cc in kmeans(X,k):
        m=uniq[((uniq-cc)**2).sum(1).argmin()]; gidx.setdefault(g,[]).append(len(pal)); pal.append(tuple(int(v) for v in m))
W=64; s=W/(a.shape[1]+1); H=round((a.shape[0]+1)*s)
R=10
DX=int(sys.argv[5]) if len(sys.argv)>5 else 0; DY=int(sys.argv[6]) if len(sys.argv)>6 else 0   # fase van het raster in 1/10 modelpixel
def big(arr):
    b=np.kron(arr,np.ones((R,R,1)) if arr.ndim==3 else np.ones((R,R)))
    pw=((DY,R-DY),(DX,R-DX))+(((0,0),) if arr.ndim==3 else ())
    return np.pad(b,pw)[:b.shape[0]+R,:b.shape[1]+R]
def area(arr): return np.asarray(Image.fromarray(arr.astype('float32')).resize((W,H),Image.BOX))
A=area(big((~wit).astype(float)))
cov={g:area(big((G==g).astype(float))) for g in TINTEN}
col={g:np.stack([area(big(a[...,k]*(G==g))) for k in range(3)],2)/np.maximum(cov[g],1e-6)[...,None] for g in TINTEN}
out=np.zeros((64,64),'uint8'); oy=64-H
for y in range(H):
    for x in range(W):
        if A[y,x]<T: continue
        lt=LTO if (EZ[0]<=x/s+x0<=EZ[1] and EZ[2]<=(y)/s+y0<=EZ[3]) else LT
        if cov[0][y,x]>=lt: g=0
        elif GT<1 and MZ[0]<=x/s+x0<=MZ[1] and MZ[2]<=y/s+y0<=MZ[3] and cov[1][y,x]>=GT: g=1   # mondzone: fel groen voorrang (smalle tandpunten)
        else: g=max([1,2,3,4],key=lambda q:cov[q][y,x])
        P=np.array([pal[i] for i in gidx[g]]); out[oy+y,x]=gidx[g][((P-col[g][y,x])**2).sum(1).argmin()]
im=Image.fromarray(out,'P'); flat=[v for p in pal for v in p]; flat+=[0]*(768-len(flat)); im.putpalette(flat); im.save(OUT,transparency=0)
print('maat',W,H,'palet',len(pal)); [print(g,[(i,pal[i],int((out==i).sum())) for i in ii]) for g,ii in gidx.items()]
