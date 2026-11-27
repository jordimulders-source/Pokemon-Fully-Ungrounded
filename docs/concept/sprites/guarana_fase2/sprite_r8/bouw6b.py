# Guarana fase 2, r6: afwerking van r5A in de stijl van fase 1 (zie NOTITIES.md).
# Draaien vanuit guarana_fase2/: python3 sprite_r6/fid.py && python3 sprite_r6/eig.py && python3 sprite_r6/bouw6.py
# Jordi r5: "grotendeels prima" -> de opbouw van r5 (silhouet, buitenlijn, naden, ogen) blijft; alleen:
#  1 horizontale donkere strepen opbreken (Jordi r5: "horizontale lijnen getrokken over de hele plant heen")
#  2 vulling per vrucht zoals fase 1 (midden als basis, hooglichtblokje linksboven, schaduwsikkel rechtsonder), glans 12 vervalt
#  3 groen per deel als buis zoals de rank van fase 1 (3 tinten + lijn), 13/15 vervallen
#  4 losse pixels weg (geen tintvlakje van 1 px midden in een vlak)
import sys, os; sys.path.insert(0,'sprite_r8')
import numpy as np; from PIL import Image
from gemeen2 import *; from hulp import *
import vrucht
SRC='sprite_r5/guarana2_r5_A.png'; UIT='sprite_r8/basis.png'
o5=np.array(Image.open(SRC)).astype(int); o=o5.copy()
OOG=np.load('sprite_r5/oog.npy'); eig=np.load('sprite_r8/eig.npy'); M64=np.load('sprite_r8/model64.npy')
LUM=.299*M64[...,0]+.587*M64[...,1]+.114*M64[...,2]
E=vrucht.ellipsen()
fg=o>0
def bg(y,x): return not ok(y,x) or not fg[y,x]
RAND=np.array([[fg[y,x] and any(bg(y+dy,x+dx) for dy,dx in N4) for x in range(64)] for y in range(64)])
LICHT=np.array([-1.0,-1.25,1.1]); LICHT/=np.linalg.norm(LICHT)
log={}
RIM=OOG&np.isin(o5,[1,2,3])
# eigenaar per roodpixel: ellips (vrucht.py), anders dichtstbijzijnde (BFS)
RODE=fg&np.isin(o5,[2,3,4,5,12,14])
own=np.where(eig>=0,eig,-1)
from collections import deque
q=deque((y,x) for y,x in zip(*np.where((own>=0)&(RODE|OOG)))); seen=(own>=0)&(RODE|OOG)
while q:
    y,x=q.popleft()
    for dy,dx in N4:
        yy,xx=y+dy,x+dx
        if ok(yy,xx) and (RODE[yy,xx] or OOG[yy,xx]) and not seen[yy,xx]: own[yy,xx]=own[y,x]; seen[yy,xx]=True; q.append((yy,xx))
EL,ne=label(OOG,N8)
for e in range(1,ne+1):
    m=EL==e; v=own[m]; v=v[v>=0]
    if len(v): own[m]=np.bincount(v).argmax()
GRN=np.isin(o5,[6,7,8,9,13,15])
# ---------- 0. ogen (Jordi r5: horizontale strepen ook langs oogranden/ooglidranden) ----------
# Pupillen en oogwit-vorm bovenin blijven; alleen de platte onderkanten worden rond:
#  middel-ogen (onderrand 4 px plat '.KKKK.'): onderste witrij krijgt randhoeken, onderrand 2 px ('.KWWK.' / '..KK..'), zoals het fase 1-oog;
#  half dichte ogen (lid, lidk): ooglid bovenaan blijft, het wit eronder wordt een halve maan ('.KWWK.'/'..KK..', lidk '.KWK.'/'..K..'),
#  zodat het ooglid een korte boog op zijn eigen vrucht is en geen streep van 3 rijen hoog.
PUP=np.load('sprite_r5/pupil.npy'); OOG=OOG.copy(); OOGWIJZ=[]
OGEN={'L1':('lid',6,26),'M2':('lidk',24,16),'M3':('lidk',20,19),'R4':('lidk',49,26),
      'L2':('middel',12,22),'M1':('middel',30,12),'R1':('middel',46,22),'R2':('middel',52,22)}
def zet(x,y,v,oog=True):
    if not ok(y,x) or RAND[y,x] or PUP[y,x]: return False
    if v in (2,10) and OOG[y,x] and o[y,x] in (10,11) and v==2: pass
    o[y,x]=v; OOG[y,x]=oog; OOGWIJZ.append((x,y,int(o5[y,x]),v)); return True
def vrij(x,y): return ok(y,x) and fg[y,x] and not RAND[y,x] and not OOG[y,x] and not PUP[y,x] and o[y,x] in (2,3,4,5,12,14)
for nm,(sr,X,Y) in OGEN.items():
    if sr=='middel':
        # rij 3: 'OWWWWK' -> '.KWWK.' ; rij 4: '.KKKK.' -> '..KK..'
        if OOG[Y+3,X+1] and o[Y+3,X+1]==10: zet(X+1,Y+3,2)
        if OOG[Y+3,X+4] and o[Y+3,X+4]==10: zet(X+4,Y+3,2)
        if OOG[Y+3,X+5] and o[Y+3,X+5]==2: zet(X+5,Y+3,4,False)
        for xx in (X+1,X+4):
            if OOG[Y+4,xx] and o[Y+4,xx]==2: zet(xx,Y+4,4,False)
    else:
        w=6 if sr=='lid' else 5; mid=[X+2,X+3] if sr=='lid' else [X+2]
        if all(vrij(xx,Y+3) for xx in mid) and all(OOG[Y+2,xx] for xx in mid):
            for xx in mid: zet(xx,Y+2,10); zet(xx,Y+3,2)
        else: print('lid niet rond (geen plek):',nm)
# donkere pixel (naad/diep rood) die een oogrand horizontaal verlengt -> vulling (wordt hieronder per vrucht ingekleurd)
for y,x in zip(*np.where(fg&~RAND&~OOG&np.isin(o,[2,14]))):
    if any(ok(y,xx) and OOG[y,xx] and o[y,xx] in (1,2) for xx in (x-1,x+1)):
        if not any(ok(y+dy,x+dx) and GRN[y+dy,x+dx] for dy,dx in N4): o[y,x]=4; OOGWIJZ.append((int(x),int(y),int(o5[y,x]),'vul'))
RIM=OOG&np.isin(o,[1,2,3]); EL,ne=label(OOG,N8)
# ---------- 1. horizontale strepen ----------
DONK={1,2,14,6}
def strepen(o):
    res=[]
    for y in range(64):
        x=0
        while x<64:
            if o[y,x] in DONK and fg[y,x]:
                x0=x
                while x<64 and o[y,x] in DONK and fg[y,x]: x+=1
                if x-x0>=3:
                    oog=[bool(OOG[y,i]) for i in range(x0,x)]
                    ids=set()
                    for i in range(x0,x):
                        if OOG[y,i]: ids.add(('oog',int(EL[y,i])))
                        elif o[y,i]==6 or GRN[y,i]: ids.add('groen')
                        else: ids.add(('v',int(own[y,i])))
                    res.append((y,x0,x-1,ids))
            else: x+=1
    return res
def vul_van(y,x):
    # tint van de vrucht waar deze pixel bij hoort: de meest voorkomende vulling van dezelfde eigenaar in de 8-buurt
    nb=[o[y+dy,x+dx] for dy,dx in N8 if ok(y+dy,x+dx) and o[y+dy,x+dx] in (3,4,5,12,14) and own[y+dy,x+dx]==own[y,x] and not OOG[y+dy,x+dx]]
    return max(set(nb),key=nb.count) if nb else 3
voor=strepen(o); BREAK=[]
for (y,x0,x1,ids) in voor:
    if len(ids)<2: continue          # één oogrand of één naad: hoort bij één vorm
    xs=list(range(x0,x1+1))
    # oogrand blijft (bevroren); naadpixels in het verlengde van een oogrand of tussen twee onderdelen worden vulling van hun eigen vrucht,
    # tenzij de pixel de enige scheiding is met een vrucht/oog direct boven of onder (dan wordt de naad een boogje: laat de middelste staan)
    for x in xs:
        if OOG[y,x] or RAND[y,x] or o[y,x] not in (2,14): continue
        if any(ok(y,xx) and GRN[y,xx] for xx in (x-1,x+1)) or any(ok(yy,x) and GRN[yy,x] for yy in (y-1,y+1)): continue
        hbuur=[xx for xx in (x-1,x+1) if ok(y,xx) and o[y,xx] in DONK]
        rim_naast=any(ok(y,xx) and RIM[y,xx] for xx in (x-1,x+1))
        # verticale scheiding nodig? boven en onder verschillende vruchten en geen andere lijn ertussen
        b=(y-1,x); n=(y+1,x)
        scheidt=ok(*b) and ok(*n) and RODE[b] and RODE[n] and own[b]!=own[n] and o[b] not in DONK and o[n] not in DONK
        if rim_naast or (len(hbuur)==2 and not scheidt) or (len(hbuur)==1 and not scheidt):
            BREAK.append((x,y))
for x,y in BREAK: o[y,x]=-1
for x,y in BREAK: o[y,x]=vul_van(y,x)
log['strepen_voor']=len(voor); log['opgebroken_px']=len(BREAK)
# ---------- 2. vrucht-vulling zoals fase 1 ----------
VR=fg&~RAND&~OOG&np.isin(o,[3,4,5,12,14])
lab,nl=label(VR)
REG=np.zeros((64,64),int); nreg=0
for k in range(1,nl+1):
    m=lab==k
    for f in set(own[m].tolist()):
        mm=m&(own==f)
        L2,n2=label(mm)
        for j in range(1,n2+1): nreg+=1; REG[L2==j]=nreg
def ramp(f): return (3,4,5)   # r8: achterste vruchten zelfde tinten als fase 1 (geen donkerdere set)
ninfo=[]
for r in range(1,nreg+1):
    P=[tuple(p) for p in zip(*np.where(REG==r))]; n=len(P); f=own[P[0]]; S_,Mi,Hi=ramp(f)
    # bol: middelpunt/vorm = de hele vrucht (ellips) als die er is, anders het vlak zelf
    if f>=0: mu,Ci=E[f]['mu'],E[f]['Ci']/vrucht.T2
    else:
        ys=np.array([p[0] for p in P]); xs=np.array([p[1] for p in P]); mu=np.array([xs.mean()+.5,ys.mean()+.5]); Ci=np.eye(2)/max(2.,n/3)
    t=[]
    for y,x in P:
        d=np.array([x+0.5,y+0.5])-mu; r2=min(d@Ci@d,1); g=Ci@d; g=g/(np.linalg.norm(g)+1e-9)*np.sqrt(r2)
        nv=np.array([g[0],g[1],np.sqrt(max(0.05,1-r2))]); nv/=np.linalg.norm(nv); t.append(nv@LICHT)
    t=np.array(t); lum=np.array([LUM[p] for p in P]); z=(lum-lum.mean())/(lum.std()+1e-6) if n>2 else lum*0
    t=t+0.10*z
    S=set(P); idx={p:i for i,p in enumerate(P)}
    def ro(y,x): return any((y+dy,x+dx) not in S for dy,dx in ((1,0),(0,1)))
    for p in P: o[p]=Mi
    order=list(np.argsort(t))
    # schaduwsikkel: pixels aan de rand rechts/onder, donkerste eerst, ±28 % (fase 1: 27 van 98 vulpixels)
    nS=int(round(0.30*n)) if n>=4 else (1 if n==3 else 0)
    k=0
    for i in order:
        if k>=nS: break
        if ro(*P[i]) and t[i]<=np.percentile(t,60): o[P[i]]=S_; k+=1
    # hooglicht: blokje linksboven (2-4 px), groeit vanuit de lichtste pixel; fase 1: 17 van 98
    if n>=4:
        nH=int(np.clip(round(0.17*n),2,5)); H=[P[order[-1]]]
        while len(H)<nH:
            best=None
            for hy,hx in H:
                for dy,dx in N4:
                    qq=(hy+dy,hx+dx)
                    if qq in S and qq not in H and o[qq]==Mi:
                        if best is None or t[idx[qq]]>best[0]: best=(t[idx[qq]],qq)
            if best is None: break
            H.append(best[1])
        if len(H)>=2:
            for p in H: o[p]=Hi
    ninfo.append((r,n))
log['vruchtvlakken']=nreg
# ---------- 3. groen ----------
GZ=fg&~RAND&~OOG&np.isin(o5,[7,8,9,13,15])
glab,ng=label(GZ)
nblad=0
for k in range(1,ng+1):
    m=glab==k; P=[tuple(p) for p in zip(*np.where(m))]; n=len(P)
    ys=np.array([p[0] for p in P]); ml=LUM[m].mean()
    if ml>=117 and ys.mean()<30 and n<30:
        # blad: lobtinten van r5 (uit het model: lichte lob / donkere helft), 13 en 15 -> schaduw
        nblad+=1
        for p in P: o[p]={13:7,15:7}.get(o5[p],o5[p])
        # lichte lob krijgt hooglicht aan de lichtkant (boven/links tegen de lijn), zoals de rank van fase 1; alleen in lobben van >= 3 px
        L8,n8=label(m&(o==8))
        for j in range(1,n8+1):
            Q=[tuple(p) for p in zip(*np.where(L8==j))]
            if len(Q)<3: continue
            lq=np.array([LUM[p] for p in Q]); med=np.median(lq)
            for (y,x),l in zip(Q,lq):
                rand_lb=any(not ok(y+dy,x+dx) or o[y+dy,x+dx] not in (7,8,9) for dy,dx in ((-1,0),(0,-1)))
                if rand_lb and l>=med: o[y,x]=9; log['blad_hooglicht']=log.get('blad_hooglicht',0)+1
        continue
    s=float(np.clip(np.sqrt(n)/3.0,0.8,2.4)); Bm=gauss(m,s); gy,gx=np.gradient(Bm); nz=0.30/s
    t=np.array([(lambda nv:nv@LICHT/np.linalg.norm(nv))(np.array([-gx[p],-gy[p],nz])) for p in P])
    lum=LUM[m]; z=(lum-lum.mean())/(lum.std()+1e-6) if n>2 else lum*0
    t=t+0.3*np.std(t)*z
    qn=(np.argsort(np.argsort(t))+0.5)/n
    donker=ml<100     # achterste streng in de twist (model donker): schaduw + midden
    if donker: band=np.where(qn<0.5,0,1)
    elif n>=6: band=np.searchsorted([.27,.78],qn)
    elif n>=3: band=np.searchsorted([.34,.80],qn)
    else: band=np.full(n,1)
    for p,b in zip(P,band): o[p]=(7,8,9)[b]
log['bladvlakken']=nblad
# ---------- 4. losse pixels ----------
VULR=(14,3,4,5); VULG=(7,8,9)
ZONE=(VR|GZ)
for ronde in range(3):
    v=o.copy(); n_=0
    for y,x in zip(*np.where(ZONE)):
        k=v[y,x]; fam=VULR if k in VULR else VULG if k in VULG else None
        if fam is None: continue
        same=lambda yy,xx: ZONE[yy,xx] and v[yy,xx] in fam and (fam is VULG and glab[yy,xx]==glab[y,x] or fam is VULR and REG[yy,xx]==REG[y,x])
        nb=[v[y+dy,x+dx] for dy,dx in N4 if ok(y+dy,x+dx) and same(y+dy,x+dx)]
        nb8=[v[y+dy,x+dx] for dy,dx in N8 if ok(y+dy,x+dx) and same(y+dy,x+dx)]
        if not nb or k in nb: continue
        if k in nb8 and k in (3,14,7): continue    # diagonale sikkel mag (fase 1)
        o[y,x]=max(set(nb),key=nb.count); n_+=1
    log['los_%d'%ronde]=n_
# diep rood (sikkel achterste vrucht) met een donkere buur links/rechts leest als dikke lijn -> schaduw 3
D14=[]
for y,x in zip(*np.where(o==14)):
    if any(ok(y,xx) and o[y,xx] in DONK for xx in (x-1,x+1)): D14.append((y,x))
for p in D14: o[p]=3
log['diep_rood_naar_schaduw']=len(D14)
na=strepen(o)
# ---------- controle ----------
assert ((o>0)==(o5>0)).all(), 'silhouet veranderd'
assert (o[PUP]==o5[PUP]).all(), 'pupil veranderd'
assert (o[RAND]==o5[RAND]).all(), 'buitenlijn veranderd'
GEBRUIKT=sorted(set(o.ravel().tolist())); PAL6=[PAL[i] if i in GEBRUIKT or i==0 else (0,0,0) for i in range(16)]
pal_schrijven('sprite_r8/normal.pal',PAL6); opslaan(o,UIT,PAL6)
np.save('sprite_r8/own.npy',own)
print(log); print('ogen gewijzigd (x,y,oud,nieuw):',OOGWIJZ); print('kleuren',sorted(set(o.ravel().tolist())))
fmt=lambda L:[(y,x0,x1,len(i)) for y,x0,x1,i in L]
print('strepen >=3 voor (y,x0,x1,#onderdelen):',fmt(voor)); print('na:',fmt(na)); print('opgebroken (x,y):',BREAK)
