# Kay Pacha r1: kale reductie van het natieve modelraster + technische opschoning + oog (Jordi's toegestane afwijking).
# Run vanuit docs/concept/sprites/kay_pacha:  python3 sprite/r1/bouw.py
import sys,numpy as np; from PIL import Image
sys.path.insert(0,'sprite/r1'); from klassen import klassen
from collections import deque
D='sprite/r1/'
a,L,K=klassen(); H,W=K.shape
# --- franje: losse creme-componenten buiten de kop (antialiasrand) -> buurklasse/bg
def comps(mask):
    lab=np.zeros(mask.shape,int); n=0
    for y,x in zip(*np.where(mask)):
        if lab[y,x]: continue
        n+=1; q=deque([(y,x)]); lab[y,x]=n
        while q:
            cy,cx=q.popleft()
            for dy,dx in((1,0),(-1,0),(0,1),(0,-1)):
                yy,xx=cy+dy,cx+dx
                if 0<=yy<H and 0<=xx<W and mask[yy,xx] and not lab[yy,xx]: lab[yy,xx]=n; q.append((yy,xx))
    return lab,n
lab,n=comps(K==4); sz=np.bincount(lab.ravel()); sz[0]=0; kop=sz.argmax()
fr=(K==4)&(lab!=kop)
for _ in range(6):
    for y,x in zip(*np.where(fr)):
        nb=[K[y+dy,x+dx] for dy,dx in((1,0),(-1,0),(0,1),(0,-1)) if 0<=y+dy<H and 0<=x+dx<W and not fr[y+dy,x+dx]]
        if nb:
            if 0 in nb and L[y,x]>185: K[y,x]=0
            else:
                nb=[v for v in nb if v not in (0,4)] or [0]
                K[y,x]=max(set(nb),key=nb.count)
            fr[y,x]=False
# --- tonen per groep (natieve helderheid)
TH={2:[92,114],3:[108,138,160],4:[135,170,205]}   # groen 3 tinten; goud: lijn,schaduw,midden,licht; creme: lijn,donkertan,tan,licht
T=np.zeros((H,W),int)
for g,t in TH.items(): T[K==g]=np.digitize(L[K==g],t)
# palet = mediaan van de modelpixels per (groep,toon)
order=[(1,0),(2,0),(2,1),(2,2),(3,0),(3,1),(3,2),(3,3),(4,0),(4,1),(4,2),(4,3),(5,0)]
PAL=[(152,208,160)]
for g,t in order:
    m=(K==g)&(T==t) if g in TH else (K==g)
    PAL.append(tuple(int(v) for v in np.median(a[m],axis=0)))
IDX={k:i+1 for i,k in enumerate(order)}
# --- schaal: hoogte 162 natief -> 62 sprite
x0n,y0n=26,21; s=162/62; top,left=1,3
F=10; KU=np.kron(K,np.ones((F,F),int)); TU=np.kron(T,np.ones((F,F),int)); LU=np.kron(L,np.ones((F,F)))
S=np.zeros((64,64),int); info={}
# punt-voor-punt: elke lijnpixel (natief) -> dichtstbijzijnde spritepixel (lijnen blijven 1 px en doorlopend)
NG=np.zeros((64,64),int); NC=np.zeros((64,64,3),int)
def mid(m):
    """lijnen van 1-3 natieve px dik -> middelpunt (continu) van elke korte run, horizontaal en verticaal"""
    pts=[]
    for tr in (False,True):
        mm=m.T if tr else m
        for i in range(mm.shape[0]):
            r=mm[i]; j=0
            while j<len(r):
                if r[j]:
                    e=j
                    while e<len(r) and r[e]: e+=1
                    if e-j<=3: pts.append(((j+e)/2,i+0.5) if tr else (i+0.5,(j+e)/2))
                    j=e
                else: j+=1
    return pts
def tel(m,N,w=None):
    for (y,x) in mid(m):
        sx=int(np.floor((x-x0n)/s+left)); sy=int(np.floor((y-y0n)/s+top))
        if 0<=sx<64 and 0<=sy<64: N[sy,sx]+=1
NB=np.zeros((64,64),int)
tel((K==3)&(T==0),NG); tel(K==1,NB)
NC0=np.zeros((64,64),int); NC1=np.zeros((64,64),int)
tel((K==4)&(T==0),NC0); tel((K==4)&(T==1),NC1); NC[...,0]=NC0; NC[...,1]=NC1
for sy in range(64):
    for sx in range(64):
        ya=int(round((y0n+(sy-top)*s)*F)); yb=int(round((y0n+(sy-top+1)*s)*F))
        xa=int(round((x0n+(sx-left)*s)*F)); xb=int(round((x0n+(sx-left+1)*s)*F))
        if ya<0 or xa<0 or yb>H*F or xb>W*F or yb<=ya or xb<=xa: continue
        k=KU[ya:yb,xa:xb]; t=TU[ya:yb,xa:xb]; l=LU[ya:yb,xa:xb]; n=k.size
        fg=(k!=0).mean()
        if fg<0.45: continue
        fz=(k==1).sum()/n; fp=(k==5).sum()/n
        if fz>=0.50 or (NB[sy,sx]>=1 and fz>=0.15): S[sy,sx]=IDX[(1,0)]; continue
        if fp>=0.35: S[sy,sx]=IDX[(5,0)]; continue
        cnt={g:(k==g).sum() for g in (2,3,4,6)}
        g=max(cnt,key=cnt.get)
        if g==6: g=4
        if cnt[g]==0: S[sy,sx]=IDX[(1,0)]; continue
        m=(k==g); tv=t[m]; fr=np.bincount(tv,minlength=4)/m.sum()
        if g==3 and NG[sy,sx]>=1: S[sy,sx]=IDX[(3,0)]; continue          # goudlijn: punt-voor-punt gemapt
        if g==4 and NC[sy,sx,:2].sum()>=1:                                  # cremelijn (toon 0/1): punt-voor-punt gemapt
            c=NC[sy,sx]; S[sy,sx]=IDX[(4,0 if c[0]>c[1] else 1)]; continue
        if g==4: S[sy,sx]=IDX[(4,2 if fr[2]>fr[3] else 3)]; continue      # vlak: schaduw (tan) of licht, meeste wint
        lo=1 if g==3 else 0
        tl=lo+int(np.argmax(fr[lo:]))                                       # meest voorkomende toon (geen gemiddelde)
        S[sy,sx]=IDX[(g,tl)]
np.save(D+'kaal.npy',S)
def save(arr,name,pal):
    im=Image.fromarray(arr.astype('uint8'),'P'); p=[]
    for c in pal: p+=list(c)
    im.putpalette(p); im.save(D+name,transparency=0)   # palet precies 16 (of minder) kleuren
save(S,'kaal.png',PAL)
print('palet',len(PAL),PAL)
yy,xx=np.where(S>0); print('bbox x',xx.min(),xx.max(),'y',yy.min(),yy.max(),'px',(S>0).sum())
np.save(D+'pal.npy',np.array(PAL))
