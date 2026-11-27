# bouw.py r5: python3 sprite_r5/bouw.py NAAM [SCHAAL] [licht|sterk]  (model = gemini/r4_starmie.webp)
# Hele model r4 1-op-1: voorste ster = r1-stappen, achterpunten = reductie van het model (koektinten, chips).
# STOMP licht/sterk: elke achterpunt minder puntig zoals de Gen 3 Starmie (alleen weghalen binnen het modelsilhouet, stomp.py).
# bouw.py: regionale Starmie r1. Start = kale samenstelling (gereedschap/kaal.py), dan alleen technische stappen.
# Gebruik: cd starmie && python3 sprite_r1/bouw.py
import sys, json; sys.path.insert(0,'gereedschap'); import gemeen
S=float(sys.argv[2]) if len(sys.argv)>2 else 0.66; NAAM=sys.argv[1] if len(sys.argv)>1 else 'starmie_r5'; STOMP=sys.argv[3] if len(sys.argv)>3 else ''
gemeen.S=S                                    # overlap() in gemeen leest deze schaal
from gemeen import *; S=gemeen.S
sys.path.insert(0,'sprite_r5/gereedschap'); import voor_r4, kaal as _k
natief=voor_r4.natief; figuur=voor_r4.figuur; voor_mask=voor_r4.voor_mask
_k.natief=voor_r4.natief; _k.voor_mask=voor_r4.voor_mask; gemeen.MODEL='referenties/model_r4.png'
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


# ===== achterpunten: reductie van het model (figuur buiten de voorste ster) =====
gemeen.PAL[6]=(250,218,128); gemeen.PAL[15]=(124,80,56)   # geel hagel + koek licht samen; 15 = chocolade
o[(o==15)&fm]=6
fig=figuur(a); BK=fig&~voor_mask(a)
def kl(c):
    r,g_,b=[int(v) for v in c]; L=(r+g_+b)/3
    if L<60: return 'zwart'
    if b>=40 and r<150 and L<115 and r-b<95: return 'chip'
    return 'koek'
KB=np.full((99,99),None,object)
for v,u in zip(*np.where(BK)): KB[v,u]=kl(a[v,u])
# chipclusters die aan de voorste ster of de achtergrond grenzen zijn lijnen, geen chips
# r4: de chips zijn donkerder (deels < L60); compacte donkere clusters (chip of zwart, <= 8 cellen) die niet aan de
# voorste ster of de achtergrond grenzen = chip; overige 'chip'-cellen zijn lijnen (koek)
cm=np.vectorize(lambda k:k in ('chip','zwart'))(KB); lab,n=label(cm)
for i in range(1,n+1):
    p=np.argwhere(lab==i)
    rand=any((not BK[v+j,u+k]) for v,u in p for j,k in ((-1,0),(1,0),(0,-1),(0,1)))
    for v,u in p:
        if len(p)<=8 and not rand: KB[v,u]='chip'
        elif KB[v,u]=='chip': KB[v,u]='koek'
BM=np.zeros((64,64),bool)
for Y in range(64):
    for X in range(64):
        if fm[Y,X]: continue
        fr={}; Ls=[]; tw=0
        for u,v,w in overlap(X,Y):
            k=KB[v,u]
            if k is None: continue
            tw+=w; fr[k]=fr.get(k,0)+w
            if k=='koek': Ls.append((w,a[v,u].mean()))
        if tw<0.5: continue
        BM[Y,X]=True; f_={k:x/tw for k,x in fr.items()}
        if f_.get('zwart',0)>=0.3: k=1
        elif f_.get('chip',0)>=0.3: k=CHOC
        else: k=tint(KT,sum(w*l for w,l in Ls)/sum(w for w,l in Ls)) if Ls else 2
        o[Y,X]=k
from voor import vul_gaten
gat=vul_gaten(o>0)&~(o>0)
print('gaten tussen voor en achter',int(gat.sum()))
# punten benoemen: meerderheid van de modelpunt onder elke spritepixel
PN=voor_r4.punten(a); PNAAM=np.full((64,64),'',object)
for Y,X in zip(*np.where(BM&~fm)):
    c={}
    for u,v,w in overlap(X,Y):
        if PN[v,u]: c[PN[v,u]]=c.get(PN[v,u],0)+w
    PNAAM[Y,X]=max(c,key=c.get) if c else ''
np.save('sprite_r5/gereedschap/pnaam.npy',PNAAM.astype(str))
kaal=o.copy(); opslaan(kaal,'sprite_r5/kaal_%s.png'%NAAM)
# --- ontkorrelen achterpunten: koekvlekjes < 3 px nemen de buurtint (geen chips, geen lijn D)
for rnd in range(3):
    for k in (3,4,5,6):
        lb,nn=label((o==k)&BM,acht=False)
        for i in range(1,nn+1):
            p=np.argwhere(lb==i)
            if len(p)>=3: continue
            for y,x in p:
                nb=[o[y+dy,x+dx] for dy,dx in ((-1,0),(1,0),(0,-1),(0,1)) if BM[y+dy,x+dx] and o[y+dy,x+dx] in (3,4,5,6) and o[y+dy,x+dx]!=k]
                if nb: zet(x,y,max(set(nb),key=nb.count),'ontkorrelen achter')
if STOMP:
    exec(open('sprite_r5/stomp.py').read())
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

CHIPSKIP=True

opslaan(o,'sprite_r5/%s.png'%NAAM)
print(NAAM)
for nm in ('linksboven','rechtsboven','linksonder','rechtsonder','onder'): print(nm,'px',int(((PNAAM==nm)&(o>0)).sum()),'chips',int(((PNAAM==nm)&(o==CHOC)).sum()))
for k,v in log.items(): print(k,len(v),v if len(v)<30 else '')
fg=o>0; yy,xx=np.where(fg); print('figuur x%d-%d y%d-%d %dx%d, %d px'%(xx.min(),xx.max(),yy.min(),yy.max(),xx.max()-xx.min()+1,yy.max()-yy.min()+1,fg.sum()))
