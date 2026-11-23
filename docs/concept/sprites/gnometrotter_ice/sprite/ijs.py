# ijs.py: red.png -> red2.png. Regels op de kale/technische reductie, alles gestuurd door modelmetingen (meet.npz), niets getekend:
#  A. gat tussen de mutspunt-ijspegels en de rugkam: spritepixels met >= 45 % modelgat worden transparant (zoals het model), rand in 2
#  B. vlaktint met Gen 3-volume: per onderdeel score = modelhelderheid (3x3 binnen het onderdeel geeffend, gestandaardiseerd)
#     + lichtrichting (linksboven) + sikkel aan de schaduwkant (rand rechtsonder) -> 3 tinten op percentielen
#  C. baard (ijspegels): modelhelderheid per kolom verticaal geeffend (pegels zijn verticale banden), 3 tinten
#  D. facetten van de roze en blauwe ijsblokken: roze = donkere platen-naden (DK), blauw = barsten + naden (BR/DK), op lokaal maximum -> outline base 6/9
#  E. ruis < 3 px weg (meerderheid in het onderdeel)
import numpy as np; from scipy import ndimage as nd; from PIL import Image
from gemeen import *
from reductie_gedeeld import bron
o=lees('red.png'); zone=np.load('zone_af.npy'); M=np.load('meet.npz'); G=M['G']; BR=M['BR']; DK=M['DK']
gewijzigd={}
def zet(Y,X,k,why):
    if o[Y,X]!=k: gewijzigd.setdefault(why,[]).append((X,Y)); o[Y,X]=k
# A. gat
a=np.asarray(Image.open('../r3/gemini_r3_lijf.png').convert('RGB')).astype(int)
kand=(a.min(2)>=236)&((a.max(2)-a.min(2))<=6); lab,_=nd.label(kand); sub=lab[120:165,555:587]; h=lab==np.bincount(sub[sub>0]).argmax()
GAT=[]
for Y in range(8,18):
    for X in range(33,45):
        tw=c=0
        for u,v,w in bron(X,Y): tw+=w; c+=w*h[v,u]
        if c/tw>=0.45: GAT.append((Y,X))
for Y,X in GAT: zet(Y,X,0,'A gat'); zone[Y,X]=0
fg=o>0
for Y,X in GAT:
    for dy in (-1,0,1):
        for dx in (-1,0,1):
            y,x=Y+dy,X+dx
            if fg[y,x] and o[y,x]!=2: zet(y,x,2,'A gatrand')
def lijn(Y,X): return o[Y,X] in (1,BASIS[zone[Y,X]]) or (zone[Y,X] in (5,8,9) and o[Y,X]==6)
fg=o>0
# B/C. vlaktint
LR=np.array([-0.6,-0.8])
AANDEEL={'d':(0.24,0.34),'l':(0.28,0.28),'r':(0.32,0.14),'b':(0.20,0.36)}
for zz in ZNAAM:
    m=(zone==zz)&fg; v=m.copy()
    for Y,X in zip(*np.where(m)): v[Y,X]=not lijn(Y,X)
    if v.sum()<4: continue
    R=RAMP[zz]; fam='r' if R==ROZE else 'b' if R==BLAUW else 'l' if R==LICHT else 'd'
    g=np.where(v,np.nan_to_num(G,nan=np.nanmean(G[v])),0.0)
    if zz==4:   # baard: verticaal effenen (3 rijen) binnen het onderdeel; pegels = verticale banden
        k=np.ones((3,1))
    else: k=np.ones((3,3))
    gs=nd.convolve(g,k,mode='constant')/np.maximum(nd.convolve(v.astype(float),k,mode='constant'),1e-9)
    yy,xx=np.where(v); cy,cx=yy.mean(),xx.mean(); r=max(np.ptp(yy),np.ptp(xx))/2+1
    if zz==4:   # baard: horizontaal contrast t.o.v. de buren (+-2 kolommen), zodat de pegels als banden blijven staan
        hm=nd.convolve(gs*v,np.ones((1,5)),mode='constant')/np.maximum(nd.convolve(v.astype(float),np.ones((1,5)),mode='constant'),1e-9)
        gs=gs+1.2*(gs-hm)
    gz=(gs-gs[v].mean())/(gs[v].std()+1e-9)
    dist=nd.distance_transform_cdt(m,metric='taxicab')
    sc=np.zeros((64,64))
    for Y,X in zip(yy,xx):
        d=((X-cx)*LR[0]+(Y-cy)*LR[1])/r
        # sikkel: binnen 2 px van de rand van het onderdeel aan de schaduwkant (rand naar rechtsonder)
        nb=[(dy,dx) for dy in (-2,-1,0,1,2) for dx in (-2,-1,0,1,2) if not(0<=Y+dy<64 and 0<=X+dx<64) or not m[Y+dy,X+dx]]
        sik=0
        if nb:
            nv=np.mean(nb,0); nv=nv[::-1]; n=np.linalg.norm(nv)
            if n>0 and (nv/n)@(-LR)>0.3: sik=1
        wg=0.9 if zz==4 else 0.7; wd=0.35 if zz==4 else 0.8
        sc[Y,X]=wg*gz[Y,X]+wd*d-0.9*sik
    lo,hi=AANDEEL[fam]; s=sc[v]; t1=np.quantile(s,lo); t2=np.quantile(s,1-hi)
    if fam=='b': T=[9,10,11]
    else: T=R
    for Y,X in zip(yy,xx):
        k=T[0] if sc[Y,X]<t1 else T[2] if sc[Y,X]>=t2 else T[1]
        zet(Y,X,k,'B/C vlaktint')
# C2. baard: de donkere omlijning tussen de ijspegels in het model (DK = aandeel modellijn >= 0,14, horizontaal lokaal maximum)
#     als lijn 2, alleen waar ze >= 3 px verticaal doorloopt (grote vormen, geen losse donkere pixels)
sp=np.zeros((64,64),bool)
for Y,X in zip(*np.where((zone==4)&fg)):
    if lijn(Y,X): continue
    if DK[Y,X]>=0.14 and DK[Y,X]>=DK[Y,X-1] and DK[Y,X]>=DK[Y,X+1]: sp[Y,X]=True
lb,n=nd.label(sp,structure=np.ones((3,3)))
for i in range(1,n+1):
    mm=lb==i; ys,xs=np.where(mm)
    if np.ptp(ys)+1>=3:
        for Y,X in zip(ys,xs): zet(Y,X,2,'C2 pegelspleet')
# D. facetten roze/blauw: barst of naad in het model (>= 0,22 van het spritevlak) op een lokaal maximum, niet naast een lijn
def nms(A,Y,X):
    c=A[Y,X]; return (c>=A[Y,X-1] and c>A[Y,X+1]) or (c>=A[Y-1,X] and c>A[Y+1,X])
FAC=[]
for zz in (6,7,8,9,12):
    for Y,X in zip(*np.where((zone==zz)&fg)):
        if lijn(Y,X): continue
        A=DK if zz in (6,7,8,9) else np.maximum(BR,DK)   # roze: platen-naden (donker in het model); blauw: barsten + naden
        if A[Y,X]<0.22 or not nms(A,Y,X): continue
        if sum(lijn(Y+dy,X+dx) for dy,dx in ((1,0),(-1,0),(0,1),(0,-1)) if zone[Y+dy,X+dx]==zz)>=2: continue
        FAC.append((Y,X,BASIS[zz]))
for Y,X,k in FAC: zet(Y,X,k,'D facet')
# E. ruis
for _ in range(2):
    for k in set(o[fg].ravel())-{1,2,6,9,15}:
        lb,n=nd.label((o==k)&fg,structure=np.ones((3,3)))
        for i in range(1,n+1):
            mm=lb==i
            if mm.sum()>=3: continue
            ys,xs=np.where(mm); z=zone[ys[0],xs[0]]
            rr=nd.binary_dilation(mm,structure=np.ones((3,3)))&~mm&(zone==z)
            t=o[rr]; t=t[(t!=k)&np.isin(t,RAMP[z]+[9])]
            if len(t):
                for Y,X in zip(ys,xs): zet(Y,X,np.bincount(t).argmax(),'E ruis')
np.save('zone_af.npy',zone)
opslaan(o,'red2.png')
for k,v in gewijzigd.items(): print(k,len(v))
