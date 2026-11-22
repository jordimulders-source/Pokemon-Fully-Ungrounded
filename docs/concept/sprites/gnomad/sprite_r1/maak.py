# maak.py: vol.png + benoemde reparaties + Jordi's toegestane afwijkingen (snor iets rafeliger, riem als band) -> gnomad_A.png / gnomad_B.png
# Telt per zone de afwijking t.o.v. de kale reductie (kaal.png, zelfde palet op kleur vergeleken).
import numpy as np
from gemeen import *
o=lees('vol.png'); zone=np.load('zone.npy').copy(); L=np.load('lijn.npy').copy()
# verdwaalde mutszone-pixel midden in het lijf (modelvouwlijn die bij de muts werd ingedeeld) -> lijf, geen lijn
for Y,X in zip(*np.where((zone==1)&(np.arange(64)[:,None]>=39))): zone[Y,X]=5; L[Y,X]=False; print('mutspixel in lijf ->',X,Y)
PA=list(PAL_A); PA[14]=(174,130,90); PA[15]=(104,68,48)       # A: warm leerbruin (licht, donker); 14 is ook de selout van de snor
PB=list(PA);    PB[15]=(40,66,104)                             # B: riem in Gnomini's donkerblauw (9) + diep indigo (15)
K,E,C,D=1,14,12,13
def zet(lst,tag):
    for x,y,k in lst: o[y,x]=k
# 1. reductiefouten (technisch): verdwaalde mutspixel + gat in de linkersnor, linkerrand snor zonder zwart/selout om en om
FIX=[(10,35,E),(11,35,D),(11,33,K),(11,36,C),(12,38,K)]
SNORFIX=list(FIX)
# binnenrand van de mutsflap (kant naar het gat, schaduwzijde): selout en zwart wisselden per rij af -> zwart, zoals in het model
FIX+=[(x,y,K) for x,y in ((44,26),(45,28),(46,30),(47,32),(42,14))]
# 2. neusglans (model: lichtere vlek linksboven op de neus; bij Gnomini ook)
FIX+=[(17,28,D),(18,28,D),(17,29,D)]
# 3. snor iets rafeliger (Jordi r1): puntje aan de linker pluk, inkeping onderrand links en rechts, inkeping rechteruiteinde
RAF=[(9,32,0),(10,32,K),                     # linkeruiteinde: onderkant bovenste pluk 1 px ingesneden (pluk steekt los uit; proef met 1 px verder naar buiten las als takje)
     (15,37,K),                               # onderrand linkerlob: inkeping -> twee plukjes
     (26,38,K),                               # onderrand onder de neus: inkeping
     (42,31,K),                               # rechteruiteinde: inkeping tussen twee plukjes
     (37,33,E)]                               # binnenlijn rechtersnor zachter (model: olijfkleurige lijn, geen zwart)
zet(FIX,'fix'); zet(RAF,'raf')
for x,y,k in RAF+SNORFIX:
    if k and (zone[y,x]==0 or (zone[y,x]==1 and y>=28)): zone[y,x]=3 if x<32 else 4
    if k==0: zone[y,x]=0
# 4. riem: band van 2-3 px die de bol volgt (glimlachboog, zoals Gnomini's streep), op de grens roze/blauw.
#    boven de band: roze (lijf), eronder: blauw (broek); tonen per pixel opnieuw met dezelfde belichting als volume.py
body=np.isin(zone,(5,8))&~L
cx,cy,rx,ry=27.0,45.5,14.0,8.5
l=np.array([-0.55,-0.6,0.58]); l/=np.linalg.norm(l)
def I(X,Y):
    nx=(X+0.5-cx)/rx; ny=(Y+0.5-cy)/ry; r2=nx*nx+ny*ny
    n=np.array([nx,ny,np.sqrt(max(0.04,1-min(r2,0.96)))]); n/=np.linalg.norm(n); return float(n@l)
def top(X):
    u=(X-25.0)/14.0; return 40.6+3.4*(1-u*u)+0.8*u
riem=np.zeros((64,64),bool)
for Y,X in zip(*np.where(body)):
    t=int(round(top(X))); dik=3 if abs((X-25)/14)<0.65 else 2
    if t<=Y<t+dik:
        riem[Y,X]=True; onder=(Y==t+dik-1)
        o[Y,X]=15 if (X>=31 or (onder and X>=22)) else 14
    elif Y<t:
        o[Y,X]=8 if I(X,Y)>=0.30 else 7; zone[Y,X]=5
    else:
        i=I(X,Y); o[Y,X]=11 if i>=0.25 else (10 if i>=-0.25 else 9); zone[Y,X]=8
# slagschaduw onder snor/neus blijft (volume.py): opnieuw toepassen op roze boven de riem
for Y,X in zip(*np.where(body&(zone==5)&~riem)):
    if zone[Y-1,X] in (1,2,3,4) or (L[Y-1,X] and zone[Y-2,X] in (1,2,3,4)): o[Y,X]=7
# lijnpixels op de grens lijf/broek naast arm R (oude modellijn van de broekgrens, nu boven de riem): roze lijnkleur
for Y,X in zip(*np.where(L&np.isin(zone,(5,8)))):
    if o[Y,X] in (9,10,11) and Y<int(round(top(X))): o[Y,X]=K if o[Y,X]==9 else 6
# buitenrand links van broek/riem: geen zwart en selout om en om
for x,y,k in [(14,45,9),(14,43,9)]: o[y,x]=k
oA=o.copy()
# B: riem in donkerblauw: licht deel = 9 (Gnomini-streep), donker deel = indigo (15 in PB)
oB=o.copy(); oB[riem&(o==14)]=9
opslaan(oA,'gnomad_A.png',PA); opslaan(oB,'gnomad_B.png',PB)
np.save('zone_af.npy',zone); np.save('riem.npy',riem)
kaal=lees('kaal.png'); P=np.array(PAL,float); PAn=np.array(PA,float)
print('afwijking t.o.v. de kale reductie (A), per zone: px anders / px zone  [waarvan lijn | riem]')
for zz,n in ZNAAM.items():
    m=zone==zz; d=m&(np.abs(PAn[oA]-P[kaal]).sum(2)>0)&((oA>0)|(kaal>0))
    print('   %-7s %3d / %3d   [%d | %d]'%(n,d.sum(),m.sum(),(d&L).sum(),(d&riem).sum()))
print('   silhouet: %d px anders'%((oA>0)!=(kaal>0)).sum())
