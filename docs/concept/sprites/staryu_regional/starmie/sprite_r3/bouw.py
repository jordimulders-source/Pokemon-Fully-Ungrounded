# bouw.py r3: python3 sprite_r3/bouw.py SCHAAL DX DY NAAM
# Voorste ster opnieuw uit het model op SCHAAL (stappen r1: zigzag 1 px, juweelfacetten, ontkorrelen, koek in glazuur);
# achterster = donkere Gen 3-achterster verticaal gespiegeld op ware grootte (r2), herbelicht, chips in chocolade.
# bouw.py: regionale Starmie r1. Start = kale samenstelling (gereedschap/kaal.py), dan alleen technische stappen.
# Gebruik: cd starmie && python3 sprite_r1/bouw.py
import sys, json; sys.path.insert(0,'gereedschap'); import gemeen
S=float(sys.argv[1]); DX=int(sys.argv[2]); DY=int(sys.argv[3]); NAAM=sys.argv[4]
gemeen.S=S                                    # overlap() in gemeen leest deze schaal
from gemeen import *; S=gemeen.S
from kaal import voorste, PT, KT, tint
CHOC=15
a=natief(); vm=voor_mask(a)
F0,fm=voorste()
o=F0.copy(); log={}
def zet(x,y,k,stap):
    if o[y,x]!=k: o[y,x]=k; log.setdefault(stap,[]).append((x,y))
# --- ondergrond per spritepixel (paars/koek zonder wit en hagelslag), voor plekken waar wit/hagel verdwijnt
def ondergrond(X,Y):
    acc={'paars':[0,0],'koek':[0,0],'plijn':[0,0]}
    for u,v,w in overlap(X,Y):
        if not vm[v,u]: continue
        k=klasse(a[v,u])
        if k in acc: acc[k][0]+=w; acc[k][1]+=w*a[v,u].mean()
    if acc['paars'][0]+acc['plijn'][0]>=acc['koek'][0]:
        w=acc['paars'][0]+acc['plijn'][0]; L=(acc['paars'][1]+acc['plijn'][1])/max(w,1e-9); return tint(PT,L)
    return tint(KT,acc['koek'][1]/max(acc['koek'][0],1e-9))
# --- 1. witte glazuurlijnen: elke witte modelcel geprojecteerd op de sprite, dan uitgedund tot 1 px (Zhang-Suen)
W=np.zeros((64,64),bool)
for v,u in zip(*np.where(vm)):
    if klasse(a[v,u])=='wit':
        X=int(np.floor(CX+(u+0.5-GEM[0])*S)); Y=int(np.floor(CY+(v+0.5-GEM[1])*S)); W[Y,X]=True
def dun(m):
    m=m.copy(); ch=True
    while ch:
        ch=False
        for st in (0,1):
            weg=[]
            for y,x in zip(*np.where(m)):
                P=[m[y-1,x],m[y-1,x+1],m[y,x+1],m[y+1,x+1],m[y+1,x],m[y+1,x-1],m[y,x-1],m[y-1,x-1]]
                B=sum(P); A=sum((not P[i]) and P[(i+1)%8] for i in range(8))
                if 2<=B<=6 and A==1:
                    if st==0 and not (P[0] and P[2] and P[4]) and not (P[2] and P[4] and P[6]): weg.append((y,x))
                    if st==1 and not (P[0] and P[2] and P[6]) and not (P[0] and P[4] and P[6]): weg.append((y,x))
            for y,x in weg: m[y,x]=False; ch=True
    # pixel-perfect: L-hoekjes weg (pixel met een horizontale en verticale buur die niet nodig is voor samenhang)
    for y,x in zip(*np.where(m)):
        for dy,dx in ((-1,-1),(-1,1),(1,-1),(1,1)):
            if m[y+dy,x] and m[y,x+dx] and not m[y-dy,x-dx] and not m[y+dy,x+dx]:
                n=sum(m[y+j,x+i] for j in (-1,0,1) for i in (-1,0,1))-1
                if n==2: m[y,x]=False; break
    return m
Wd=dun(W)
for y,x in zip(*np.where(fm)):
    if Wd[y,x]: zet(x,y,11,'wit lijn')
    elif o[y,x]==11: zet(x,y,ondergrond(x,y),'wit lijn')
# --- 1b. juweel: omtrek en facetlijnen (paarse lijn + zwart in het model, natief u35-60, v38-61) op dezelfde manier
#         geprojecteerd en uitgedund; de reductie maakte ze tot een vage vlek. Weggevallen lijnpixels -> paarse vultint.
J=np.zeros((64,64),bool); JB=np.zeros((64,64),bool)
for v in range(38,62):
    for u in range(35,61):
        X=int(np.floor(CX+(u+0.5-GEM[0])*S)); Y=int(np.floor(CY+(v+0.5-GEM[1])*S)); JB[Y,X]=True
        if klasse(a[v,u]) in ('plijn','zwart'): J[Y,X]=True
Jd=dun(J)
def paars_zonder_lijn(X,Y):
    s=w0=0
    for u,v,w in overlap(X,Y):
        if klasse(a[v,u])=='paars': s+=w*a[v,u].mean(); w0+=w
    return tint(PT,s/w0) if w0 else 8
for y,x in zip(*np.where(JB&fm)):
    if o[y,x] in HAGEL or o[y,x]==11: continue
    if Jd[y,x]: zet(x,y,7,'juweel lijn')
    elif o[y,x] in (7,1): zet(x,y,paars_zonder_lijn(x,y),'juweel lijn')
# --- 2. ontkorrelen glazuur en koek: tintvlekjes < 3 px (paars donker/midden/licht, koek S/O/M/L) nemen de buurtint
#        van dezelfde groep aan; lijnen (zwart, D, paarse lijn), wit en hagelslag blijven.
for rnd in range(3):
    for k in (8,9,10,3,4,5,6):
        lab,n=label(o==k,acht=False)
        for i in range(1,n+1):
            p=np.argwhere(lab==i)
            if len(p)>=3: continue
            grp=PAARS if k in PAARS else KOEK
            for y,x in p:
                nb=[o[y+dy,x+dx] for dy,dx in ((-1,0),(1,0),(0,-1),(0,1)) if o[y+dy,x+dx] in grp and o[y+dy,x+dx] not in (k,2,7)]
                if nb and fm[y,x]==True: zet(x,y,max(set(nb),key=nb.count),'ontkorrelen')
# --- 4c. koektint midden in het glazuur (alle 4 buren paars/wit/hagel): mengpixel van de reductie -> paarse ondergrond
for y,x in zip(*np.where(fm&np.isin(o,list(KOEK)))):
    nb=[o[y+dy,x+dx] for dy,dx in ((-1,0),(1,0),(0,-1),(0,1))]
    if all(v in PAARS|HAGEL|{11} for v in nb): zet(x,y,paars_zonder_lijn(x,y),'koek in glazuur')

# ===== achterster: donkere Gen 3-achterster (set A) verticaal gespiegeld, ware grootte, verschoven DX/DY =====
from gen3 import TIPS, C
gemeen.PAL[6]=(250,218,128); gemeen.PAL[15]=(124,80,56)   # geel hagel + koek licht samen; 15 = chocolade
o[(o==15)&fm]=6; F0=o.copy()                               # voorste ster na reparaties = basis voor kaal_*.png
from voor import vul_gaten
g,_=laad_g3(); SETA=('top','r','br','bl','l')
kaal=np.where(fm,F0,0)
B=np.zeros((64,64),int); LAB=np.full((64,64),'',object)
for y,x in zip(*np.where(np.isin(g,[1,2,3,4,14]))):
    n=punt_van(x,y)
    if n not in SETA: continue
    v=g[y,x]
    if v==4:
        rand=any(g[y+j,x+i] in (0,14) or punt_van(x+i,y+j)!=n or g[y+j,x+i] in (5,6,7,8) for j,i in ((-1,0),(1,0),(0,-1),(0,1)))
        v=4 if rand else 5
    X=x+DX; Y=60-y+DY
    if 0<=X<64 and 0<=Y<64 and not fm[Y,X]: B[Y,X]=v; LAB[Y,X]=n
cx,cy=C[0]+DX,60-C[1]+DY; info={}
for n in SETA:
    tx,ty=TIPS[n]; tx,ty=tx+DX,60-ty+DY
    ax=np.array([tx-cx,ty-cy],float); ax/=np.linalg.norm(ax)
    perp=np.array([-ax[1],ax[0]]); licht=1 if perp@np.array([-1,-1])>0 else -1
    pts=[(x,y) for y,x in zip(*np.where(LAB==n))]; side={}
    for t in (1,2,3,5):
        s_=[np.sign(np.array([x-cx,y-cy])@perp) for x,y in pts if B[y,x]==t]
        if s_: side[t]=np.mean(s_)*licht
    lit=[t for t in side if side[t]>0]; sch=[t for t in side if side[t]<=0]
    m={4:2,14:1}
    for t in lit: m[t]=5 if t==min(lit) else 4
    for t in sch: m[t]=3 if t==max(sch) else 4
    info[n]=m
    for x,y in pts:
        zet(x,y,m[B[y,x]],'achterster'); kaal[y,x]=m[B[y,x]]
# gaten tussen achterster en voorste ster (daar lag in de Gen 3 de voorste ster/kern over de achterste): tint van de
# dichtstbijzijnde achterpixel van de achterster (geen nieuwe vorm buiten het omhulsel)
f=o>0; gat=vul_gaten(f)&~f
for y,x in zip(*np.where(gat)):
    ys,xs=np.where((o>0)&~fm&(o!=1)); k=np.argmin((xs-x)**2+(ys-y)**2)
    zet(x,y,o[ys[k],xs[k]],'gat gevuld'); LAB[y,x]=LAB[ys[k],xs[k]]; kaal[y,x]=o[y,x]
opslaan(kaal,'sprite_r3/kaal_%s.png'%NAAM)
# --- buitenlijn: rand naar transparant rechts/onder = zwart, links/boven = koek donker
fg=o>0
for y,x in zip(*np.where(fg)):
    r=not fg[y,x+1]; b=not fg[y+1,x]; l=not fg[y,x-1]; t=not fg[y-1,x]
    if not (r or b or l or t) or o[y,x]==1: continue
    if r or b: zet(x,y,1,'buitenlijn')
    elif o[y,x]!=2: zet(x,y,2,'buitenlijn')
# --- binnenlijn achter tegen voorste ster
for y,x in zip(*np.where((o>0)&~fm)):
    if o[y,x] in (1,2): continue
    if any(fm[y+dy,x+dx] and o[y+dy,x+dx]!=1 for dy,dx in ((-1,0),(1,0),(0,-1),(0,1))): zet(x,y,2,'binnenlijn achter')
# --- losse zwarte pixels -> koek donker
for y,x in zip(*np.where(o==1)):
    if all(o[y+dy,x+dx]!=1 for dy in (-1,0,1) for dx in (-1,0,1) if dy or dx): zet(x,y,2,'losse zwarte pixel')

# --- chips: 2 per punt, 2 px, chocolade, op de lichte facet (koek midden), 4 buren vulling, dicht bij de tip, >=3 px uit elkaar
FILL=(3,4,5); chipl={}
def binnen(x,y): return o[y,x] in FILL and not fm[y,x] and all(o[y+dy,x+dx] in FILL and not fm[y+dy,x+dx] for dy,dx in ((-1,0),(1,0),(0,-1),(0,1)))
for n in SETA:
    kand=[]
    for y,x in zip(*np.where(LAB==n)):
        if o[y,x]!=5 or not binnen(x,y): continue
        if o[y,x+1]==5 and binnen(x+1,y): kand.append((x,y,x+1,y))
        elif o[y+1,x]==5 and binnen(x,y+1): kand.append((x,y,x,y+1))
    tx,ty=TIPS[n]; tx,ty=tx+DX,60-ty+DY
    kand.sort(key=lambda c:(c[0]-tx)**2+(c[1]-ty)**2); gek=[]
    for c in kand:
        if all(max(abs(c[0]-k[0]),abs(c[1]-k[1]))>=3 for k in gek): gek.append(c)
        if len(gek)==2: break
    for x0,y0,x1,y1 in gek: zet(x0,y0,CHOC,'chips'); zet(x1,y1,CHOC,'chips')
    chipl[n]=[tuple(int(v) for v in c) for c in gek]
opslaan(o,'sprite_r3/%s.png'%NAAM)
print(NAAM,'schaal',S,'DX',DX,'DY',DY)
fy,fx=np.where(fm)
for n,nm in zip(SETA,('onder','rechtsonder','rechtsboven','linksboven','links')):
    ys,xs=np.where(LAB==n)
    L=max((np.sqrt(((fx-x)**2+(fy-y)**2).min()) for y,x in zip(ys,xs)),default=0)
    print('%-12s px %3d  lengte buiten voorste ster %.1f  chips %s'%(nm,len(ys),L,chipl[n]))
for k,v in log.items(): print(k,len(v),v if len(v)<30 else '')
fg=o>0; yy,xx=np.where(fg); print('voorste ster %d px (x%d-%d, %d breed); figuur x%d-%d y%d-%d %dx%d, %d px'%(fm.sum(),np.where(fm)[1].min(),np.where(fm)[1].max(),np.ptp(np.where(fm)[1])+1,xx.min(),xx.max(),yy.min(),yy.max(),xx.max()-xx.min()+1,yy.max()-yy.min()+1,fg.sum()))
