# bouw.py: regionale Starmie r1. Start = kale samenstelling (gereedschap/kaal.py), dan alleen technische stappen.
# Gebruik: cd starmie && python3 sprite_r1/bouw.py
import sys; sys.path.insert(0,'gereedschap'); from gemeen import *; from kaal import kaal, PT, KT, tint
a=natief(); vm=voor_mask(a)
K0,fm,extra=kaal(); opslaan(K0,'sprite_r1/kaal.png')
o=K0.copy(); log={}
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
# --- 3. buitenlijn: rand naar transparant rechts/onder = zwart, links/boven = koek donker (gekleurde selout)
fg=o>0
for y,x in zip(*np.where(fg)):
    r=not fg[y,x+1]; b=not fg[y+1,x]; l=not fg[y,x-1]; t=not fg[y-1,x]
    if not (r or b or l or t): continue
    if o[y,x]==1: continue
    if r or b: zet(x,y,1,'buitenlijn')
    elif o[y,x]!=2: zet(x,y,2,'buitenlijn')
# --- 4. binnenlijn achterste punt tegen de voorste ster: achterpixel die aan de voorste ster grenst = koek donker
for y,x in zip(*np.where((o>0)&~fm)):
    if o[y,x] in (1,2): continue
    if any(fm[y+dy,x+dx] and o[y+dy,x+dx]!=1 for dy,dx in ((-1,0),(1,0),(0,-1),(0,1))): zet(x,y,2,'binnenlijn achter')
# --- 4b. losse zwarte pixels (geen zwarte 8-buur) -> koek donker lijn
for y,x in zip(*np.where(o==1)):
    if all(o[y+dy,x+dx]!=1 for dy in (-1,0,1) for dx in (-1,0,1) if dy or dx): zet(x,y,2,'losse zwarte pixel')
# --- 4c. koektint midden in het glazuur (alle 4 buren paars/wit/hagel): mengpixel van de reductie -> paarse ondergrond
for y,x in zip(*np.where(fm&np.isin(o,list(KOEK)))):
    nb=[o[y+dy,x+dx] for dy,dx in ((-1,0),(1,0),(0,-1),(0,1))]
    if all(v in PAARS|HAGEL|{11} for v in nb): zet(x,y,paars_zonder_lijn(x,y),'koek in glazuur')
o_noch=o.copy()
# --- 5. chocoladechips (2 px, koek donker) op elke achterste punt, alleen op vulpixels (O/M) die niet aan een lijn liggen
CHIPS=__import__('json').load(open('sprite_r1/chips.json')) if len(sys.argv)<2 else []
for x,y,dx,dy in CHIPS:
    for xx,yy in ((x,y),(x+dx,y+dy)):
        assert o[yy,xx] in (3,4,5) and not fm[yy,xx], (xx,yy,o[yy,xx])
        zet(xx,yy,2,'chips')
opslaan(o,'sprite_r1/starmie_r1.png'); toon(o)
for k,v in log.items(): print(k,len(v),v if len(v)<40 else '')
