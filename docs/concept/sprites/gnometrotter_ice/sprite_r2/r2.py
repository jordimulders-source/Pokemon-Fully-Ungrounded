# r2.py: Gnometrotter Ice ronde 2. Basis = r1 (../sprite/gnometrotter_ice.png, zelfde gedeelde reductie en onderdelen).
# Alles "neem over uit het model" (metingen hieronder), niets tekenen:
#  1 baard: ijspegels = kolombanden tussen de gemeten modelspleten (kolommen met minimale modelhelderheid), spitse punten op de
#    gemeten onderkant van elke pegel; tussen de punten komt terug wat er in het model achter zit (lijf/riem)
#  2 gat bij de mutspunt: rand volgens de DC-regel (lichtkant outline base, schaduwkant zwart) i.p.v. een kader; variant dicht
#  3 roze/blauwe delen uit het model geknipt (delen.py): voetballen, dijen, band, schouderovaal, arm/vuist; per deel een bol
#    (licht linksboven), grens tussen delen = 1 px lijn 6/9 op de gemeten modellijn; alleen modellijnen in de broek
#  4 haar R: alle pixels met helder modelijs (>= 40 %) in het plukje
import sys, numpy as np; from scipy import ndimage as nd; from PIL import Image
sys.path.insert(0,'../sprite')
from gemeen import *
from reductie_gedeeld import bron
from reductie_ice import laad
VARIANT=sys.argv[1] if len(sys.argv)>1 else 'open'
o=lees('../sprite/gnometrotter_ice.png'); zone=np.load('../sprite/zone_af.npy'); zone[o==0]=0
M=np.load('../sprite/meet.npz'); G=M['G']; DK=M['DK']
deel=np.load('deel.npy')
a,FG=laad(); LM=0.3*a[...,0]+0.59*a[...,1]+0.11*a[...,2]; f=np.load('../sprite/model_fam.npz')['f']; ZM=np.load('../sprite/model_zone.npz')['z']
r1=o.copy(); LOG={}
def zet(Y,X,k,why):
    if o[Y,X]!=k: LOG.setdefault(why,[]).append((int(X),int(Y))); o[Y,X]=k
def aandeel(X,Y,mask):
    tw=c=0
    for u,v,w in bron(X,Y): tw+=w; c+=w*mask[v,u]
    return c/tw
# ---------- 2. gat ----------
if VARIANT=='dicht':
    kand=(a.min(2)>=236)&((a.max(2)-a.min(2))<=6); lab,_=nd.label(kand); sub=lab[120:165,555:587]; h=lab==np.bincount(sub[sub>0]).argmax()
    for Y in range(8,18):
        for X in range(33,45):
            if o[Y,X]==0 and aandeel(X,Y,h)>0.2: zone[Y,X]=1; zet(Y,X,4,'gat dicht (mutskleur)')
    for Y in range(8,17):
        for X in range(35,43):
            if zone[Y,X]==1 and o[Y,X]==2 and all(o[Y+dy,X+dx]>0 for dy,dx in ((1,0),(-1,0),(0,1),(0,-1))): zet(Y,X,4,'gat dicht (mutskleur)')
# ---------- 4. haar R ----------
HELDER=(f==2)&(LM>=225); DONKER=(LM<110)&(f>0)
for Y in range(14,21):
    for X in range(32,42):
        if zone[Y,X] not in (1,3,6): continue
        h=aandeel(X,Y,HELDER)
        if h>=0.4: zone[Y,X]=3; zet(Y,X,14 if h>=0.75 else 13,'haar R')
# ---------- 3. roze/blauwe delen ----------
DE=deel.copy(); DE[DE==9]=10                                # klein stukje bovenaan de rechterdij (barst) hoort bij de dij
DE[(DE==10)&(np.arange(64)[:,None]>=51)]=20                 # rechtervoet: onder de gemeten modellijn Y 50 (X 40-48)
for Y,X in zip(*np.where((DE==10)&(np.arange(64)[:,None]==50)&(np.arange(64)[None,:]>=40))): DE[Y,X]=20  # lijnrij zelf -> voet (lijn komt op de voet, die vooraan ligt)
ROOD=np.isin(zone,[5,6,7,8,9]); BL=zone==12
for fam in (ROOD,BL):
    heb=fam&(DE>0); leeg=fam&(DE==0)
    if heb.any():
        _,(iy,ix)=nd.distance_transform_edt(~heb,return_indices=True); DE[leeg]=DE[iy[leeg],ix[leeg]]
DE[~(ROOD|BL)]=0
# kleine snippers (< 4 px) -> buur
for _ in range(2):
    for i in np.unique(DE[DE>0]):
        lb,n=nd.label(DE==i)
        for j in range(1,n+1):
            m=lb==j
            if m.sum()<4:
                r=nd.binary_dilation(m)&~m&(DE>0)
                if r.any(): DE[m]=np.bincount(DE[r]).argmax()
ROND={1:5,3:6,5:8,6:7,8:9}                                  # neus, schouderovaal, arm R, vuist, hand R: ronde delen
DNAAM={1:'neus',2:'nek',3:'schouderovaal',4:'lijf',5:'arm R',6:'vuist',7:'arm L',8:'hand R',10:'rechterdij',11:'band',12:'linkerdij',13:'linkervoet',20:'rechtervoet'}
l3=np.array([-0.55,-0.6,0.58]); l3/=np.linalg.norm(l3)
def bol(m,Y,X):
    yy,xx=np.where(m); cx,cy=(xx.min()+xx.max()+1)/2,(yy.min()+yy.max()+1)/2; rx,ry=(np.ptp(xx)+1)/2,(np.ptp(yy)+1)/2
    nx=(X+0.5-cx)/rx; ny=(Y+0.5-cy)/ry; r=nx*nx+ny*ny
    n=np.array([nx,ny,np.sqrt(max(0.04,1-min(r,0.96)))]); n/=np.linalg.norm(n); return float(n@l3)
for i in np.unique(DE[DE>0]):
    m=DE==i; blauw=i>=10
    for Y,X in zip(*np.where(m)):
        t=bol(m,Y,X)
        if blauw: k=11 if t>=0.30 else (10 if t>=-0.45 else 9)
        else: k=15 if t>=0.85 else (8 if t>=0.12 else 7)
        zet(Y,X,k,'volume '+DNAAM.get(i,str(i)))
# slagschaduw (model: donkerroze) onder muts/neus/baard/haar op lijf en nek
for Y,X in zip(*np.where(np.isin(DE,[2,4]))):
    if DE[Y,X]==2 or any(0<=Y-k and zone[Y-k,X] in (1,2,3,4,5) for k in (1,2)): zet(Y,X,7,'slagschaduw')
# ---------- 1. baard ----------
B=zone==4
kol={}
for X in range(14,33):
    v=[G[Y,X] for Y in range(24,35) if B[Y,X] and not np.isnan(G[Y,X])]
    if v: kol[X]=np.mean(v)
xs=sorted(kol); SPLEET=[X for X in xs[1:-1] if kol[X]<kol[X-1] and kol[X]<kol[X+1] and X-1 in kol and X+1 in kol]
print('baard: kolomhelderheid',{k:int(v) for k,v in kol.items()},'spleten',SPLEET)
grenzen=[min(xs)-1]+SPLEET+[max(xs)+1]
BEARD=ZM==4
bot={X:max([Y for Y in range(20,42) if aandeel(X,Y,BEARD)>=0.3],default=0) for X in xs}
PEGELS=[]
for g0,g1 in zip(grenzen[:-1],grenzen[1:]):
    cols=list(range(g0+1,g1))
    if not cols: continue
    T=max(bot[X] for X in cols); c=(cols[0]+cols[-1])/2; PEGELS.append((cols,T))
    for X in cols:
        onder=T-int(round(abs(X-c)))                      # spitse punt: midden het diepst, 1 rij hoger per kolom naar de rand
        for Y in range(onder+1,64):
            if zone[Y,X]==4:                               # tussen de punten: wat in het model achter de pegels zit
                p=aandeel(X,Y,f==3); zone[Y,X]=6 if p>=0.3 else 10; DE[Y,X]=4 if p>=0.3 else 0
                zet(Y,X,7 if p>=0.3 else 13,'baard: tussen de punten')
for X in SPLEET:                                            # spleetkolom: 1 rij hoger dan de buren
    nb=[Y for Y in range(64) if zone[Y,X-1]==4]+[Y for Y in range(64) if zone[Y,X+1]==4]
    if not nb: continue
    for Y in range(64):
        if zone[Y,X]==4 and Y>=min(max(Y2 for Y2 in range(64) if zone[Y2,X-1]==4),max(Y2 for Y2 in range(64) if zone[Y2,X+1]==4)):
            p=aandeel(X,Y,f==3); zone[Y,X]=6 if p>=0.3 else 10; zet(Y,X,7 if p>=0.3 else 13,'baard: tussen de punten')
print('pegels (kolommen, punt-rij):',PEGELS)
for cols,T in PEGELS:
    for X in cols:
        for Y in range(64):
            if zone[Y,X]!=4: continue
            k=14 if X==cols[0] else 13                     # licht links (lichtrichting), midden
            if len(cols)>=3 and X==cols[-1]: k=12          # schaduwzijde rechts
            zet(Y,X,k,'baard: pegelband')
for X in SPLEET:
    for Y in range(64):
        if zone[Y,X]==4: zet(Y,X,12,'baard: spleet (modelschaduw)')
# ---------- lijnen ----------
fg=o>0
OUT=np.zeros((64,64),bool)
for Y,X in zip(*np.where(fg)):
    if any(not(0<=Y+dy<64 and 0<=X+dx<64) or not fg[Y+dy,X+dx] for dy,dx in ((1,0),(-1,0),(0,1),(0,-1))): OUT[Y,X]=True
LR=np.array([-0.6,-0.8])
def normaal(Y,X):
    v=np.zeros(2)
    for dy in (-1,0,1):
        for dx in (-1,0,1):
            if (dy or dx) and (not(0<=Y+dy<64 and 0<=X+dx<64) or not fg[Y+dy,X+dx]): v+=(dx,dy)
    n=np.linalg.norm(v); return v/n if n else v
WERK=np.isin(zone,[4,12])|(DE>0)|np.isin(zone,[3])
# gatrand (open) en buitenlijn van de bewerkte delen: DC-regel
GATRAND=np.zeros((64,64),bool); GATRAND[7:17,34:44]=True
for Y,X in zip(*np.where(OUT&(WERK|GATRAND))):
    if zone[Y,X]==0: continue
    zet(Y,X,BASIS[zone[Y,X]] if normaal(Y,X)@LR>0.35 else 1,'buitenlijn (DC)')
# baard vooraan: rand tegen lijf/riem = 2
rank={p:i for i,p in enumerate(PRIO)}
for Y,X in zip(*np.where((zone==4)&fg&~OUT)):
    if any(zone[Y+dy,X+dx]!=4 and zone[Y+dy,X+dx]>0 and rank[zone[Y+dy,X+dx]]>rank[4] for dy,dx in ((1,0),(0,1),(0,-1))): zet(Y,X,2,'baard: rand')
# haar R vooraan: muts/lijf-pixel onder of naast het plukje met donkere modellijn (>= 20 %) = lijn
for Y in range(14,22):
    for X in range(31,43):
        if zone[Y,X] in (1,6) and o[Y,X]>0 and any(zone[Y+dy,X+dx]==3 for dy,dx in ((1,0),(-1,0),(0,1),(0,-1))) and aandeel(X,Y,DONKER)>=0.2:
            zet(Y,X,2 if zone[Y,X]==1 else 6,'haar R: modellijn')
# grens tussen delen: 1 px op de pixel met de meeste modellijn, op het voorste deel bij gelijkspel
VOOR={1:0,8:1,6:2,7:3,5:4,3:5,2:6,4:7,20:8,13:9,12:10,10:11,11:12}
for Y,X in zip(*np.where((DE>0)&~OUT)):
    for dy,dx in ((1,0),(0,1)):
        y,x=Y+dy,X+dx
        if DE[y,x]>0 and DE[y,x]!=DE[Y,X] and not OUT[y,x]:
            if o[Y,X] in (6,9) or o[y,x] in (6,9): continue
            # rond deel krijgt zijn eigen ring hieronder
            if DE[Y,X] in ROND or DE[y,x] in ROND: continue
            p,q=(Y,X),(y,x)
            if DK[Y,X]==DK[y,x]: kies=p if VOOR.get(DE[Y,X],9)<VOOR.get(DE[y,x],9) else q
            else: kies=p if DK[Y,X]>DK[y,x] else q
            zet(kies[0],kies[1],9 if DE[kies]>=10 else 6,'grens tussen delen (modellijn)')
# naden binnen een blauw deel en het lijf: modellijn >= 0,22, lokaal maximum, doorlopend >= 3 px
nd_=np.zeros((64,64),bool)
for Y,X in zip(*np.where(np.isin(DE,[4,10,11,12,13,20])&~OUT)):
    if DK[Y,X]>=0.22 and ((DK[Y,X]>=DK[Y,X-1] and DK[Y,X]>=DK[Y,X+1]) or (DK[Y,X]>=DK[Y-1,X] and DK[Y,X]>=DK[Y+1,X])): nd_[Y,X]=True
lb,n=nd.label(nd_,structure=np.ones((3,3)))
for j in range(1,n+1):
    m=lb==j
    if m.sum()>=3:
        for Y,X in zip(*np.where(m)): zet(Y,X,9 if DE[Y,X]>=10 else 6,'naad in deel (modellijn)')
# ronde delen: ring 6, zwarte boog linksmidden-linksonder-ondermidden (SPRITE_KERN)
for i in ROND:
    m=DE==i
    if not m.any(): continue
    yy,xx=np.where(m); cy,cx=yy.mean(),xx.mean()
    rand=m&nd.binary_dilation(~m,structure=np.array([[0,1,0],[1,1,1],[0,1,0]]))
    for Y,X in zip(*np.where(rand)):
        hh=np.degrees(np.arctan2(Y-cy,X-cx)); zet(Y,X,1 if (80<=hh<=190 and (OUT[Y,X] or i==1)) else 6,'ring '+DNAAM[i])
# arm L (dunne arm): boven- en onderrij lijn, midden 8, onder 7
m=DE==7
for X in np.unique(np.where(m)[1]):
    ys=np.where(m[:,X])[0]
    for Y in ys:
        if Y==ys.min(): k=6
        elif Y==ys.max(): k=1 if OUT[Y,X] else 6
        elif Y==ys.max()-1: k=7
        else: k=8
        zet(Y,X,k,'arm L')
# tintvlekjes < 3 px in delen -> buurtint
for i in np.unique(DE[DE>0]):
    for k in (7,8,10,11,15):
        lb,n=nd.label((o==k)&(DE==i),structure=np.ones((3,3)))
        for j in range(1,n+1):
            mm=lb==j
            if mm.sum()>=3 or (k==15): continue
            r=nd.binary_dilation(mm,structure=np.ones((3,3)))&~mm&(DE==i); t=o[r]; t=t[~np.isin(t,[1,6,9,k])]
            if len(t):
                for Y,X in zip(*np.where(mm)): zet(Y,X,np.bincount(t).argmax(),'ruis')
np.save('zone_r2.npy',zone); np.save('deel_r2.npy',DE)
uit='gnometrotter_ice.png' if VARIANT=='open' else 'gnometrotter_ice_gatdicht.png'
opslaan(o,uit)
d=(o!=r1)
print(uit,'anders t.o.v. r1:',d.sum(),' silhouet t.o.v. r1:',((o>0)!=(r1>0)).sum())
for k,v in LOG.items(): print('  %-34s %3d'%(k,len(v)))
