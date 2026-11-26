# r15 (25 nov): vanaf r14/sprite.png, alleen de twee plekken die Jordi aanwees (jordi_afkappingen.png in r14):
#   "hier kappen de twee panelen onnodig af toch?"
# 1 PA (loopt achter mast PB door): in het model (model_r10 / model_gekozen) komt PA rechts van de mast weer tevoorschijn en
#   loopt door tot tegen de achterarm. In r14 eindigde PA op zijn geo10-binnenrand (x 38,7), achter PB. Nu: PA verlengd aan
#   het binnen-einde (x 1,4 langs u), de vakgrenzen blijven op dezelfde plek (alleen het laatste vak loopt door); alleen lege
#   pixels rechts van PB (x >= 38) worden PA; achter de arm/romp verdwijnt hij (romp blijft romp).
# 2 PF links boven PE: de witte driehoek x 27-33, y 42-46 was geen buis maar ingesloten modelachtergrond (tussen voorbuis,
#   PF en PE; de achtergrond-floodfill bereikte hem niet, dus de kale reductie maakte er wit romp van). In het model loopt
#   de onderrand van de voorbuis van (28,1; 45,6) naar (34,1; 41,1) (spritecoordinaten, gemeten op model_gekozen). Pixels
#   eronder: PF waar PF ligt (recept), anders transparant. Buispixels die nu aan PF/transparant grenzen: zwarte omlijning
#   (schaduwkant onder).
import os, sys, numpy as np
from PIL import Image
from collections import Counter
H=os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0,os.path.join(H,'..','r10','pijp')); from geo10 import GEO10
sys.path.insert(0,H); import recept
im=Image.open(os.path.join(H,'..','r14','sprite.png')); PALF=im.getpalette()[:48]; PAL=np.array(PALF).reshape(16,3)
A=np.array(im).astype(int); B=A.copy()
P0=np.load(os.path.join(H,'..','r14','P.npy'),allow_pickle=True).astype(object); P=P0.copy()
LOG=[]
def zet(x,y,c,deel,reden):
    if B[y,x]!=c: LOG.append((x,y,int(B[y,x]),int(c),deel,reden)); B[y,x]=c
# ---- geometrie PB/PF zoals r14 (nodig voor het PF-recept)
vB=np.array(GEO10['PB'][2])-np.array(GEO10['PB'][0]); sh=-vB/2*(2.0/(vB[0]/2/recept.S))
T0=np.array((123.0,100.0)); NPF=5; VAK=4*recept.S
GPF=(tuple(T0+sh),tuple(T0+sh+np.array((0,NPF*VAK))),tuple(T0+vB+sh))
recept.LIJN['PF']=[i/NPF for i in range(1,NPF)]; recept.TINT['PF']=[14]+[13]*(NPF-1)
# ---- 1. PA verlengen
E=0.4
T,R,L=map(np.array,GEO10['PA']); GPA=(tuple(T),tuple(T+(R-T)*(1+E)),tuple(L))
recept.LIJN['PA']=[p/(1+E) for p in (.25,.5,.75)]
IDA=recept.ideaal(GPA); SX=np.mgrid[0:64,0:64][1]
for y,x in zip(*np.where(IDA&(P=='')&(SX>=38))): P[y,x]='PA'
# ---- 2. driehoek onder de voorbuis
def onder(x,y): return y+.5 > 45.6+(x+.5-28.1)*(41.1-45.6)/(34.1-28.1)
DRIE=[(x,y) for y in range(41,48) for x in range(26,34) if P[y,x]=='#' and A[y,x]==15 and onder(x,y)]
IDF=recept.ideaal(GPF)
for x,y in DRIE: P[y,x]='PF' if IDF[y,x] else ''
# ---- recept PA en PF opnieuw (alleen schrijven waar het verschilt; reproduceert r14 elders)
for k,g in (('PA',GPA),('PF',GPF),('PE',GEO10['PE'])):
    for (x,y),c in recept.recept(k,g,P).items():
        r={'PE':'-','PA':'PA doorgelopen tot de achterarm (verlengd binnen-einde)','PF':'PF zichtbaar onder de voorbuis (driehoek was ingesloten achtergrond)'}[k] if P0[y,x]!=k else ('PE-rand: grenst nu aan de lege driehoek' if k=='PE' else 'recept opnieuw (rand/vak schuift mee)')
        zet(x,y,c,k,r)
for x,y in DRIE:
    if P[y,x]=='': zet(x,y,0,'driehoek','ingesloten achtergrond onder de voorbuis -> transparant')
# r14-regel "navy rand waar PF links aan romp grenst" geldt nog steeds voor PF-pixels die aan de buis grenzen? Nee: de buis
#   krijgt nu zelf zijn zwarte onderrand (hieronder), zoals een vorm die voor een andere ligt.
# losse gaatjes van 1 px in de driehoek (>=3 bezette 4-buren) worden buisrand (zwart), anders leest het als ruis
for x,y in DRIE:
    if B[y,x]==0 and sum(1 for dy,dx in ((1,0),(0,1),(-1,0),(0,-1)) if B[y+dy,x+dx]>0)>=3:
        P[y,x]='#'; zet(x,y,1,'driehoek','los gaatje van 1 px -> buisrand (zwart)')
def leeg(x,y): return not(0<=x<64 and 0<=y<64) or B[y,x]==0
NIEUW={(x,y) for x,y in DRIE}
for y in range(38,48):
    for x in range(24,36):
        if P[y,x]!='#' or (x,y) in NIEUW: continue
        if any((x+dx,y+dy) in NIEUW for dy,dx in ((1,0),(0,1),(-1,0),(0,-1))) and B[y,x] not in (1,):
            zet(x,y,1,'buis','onderrand voorbuis tegen PF/achtergrond (zwart, schaduwkant)')
assert len(np.unique(B))<=16
def opslaan(arr,path):
    i2=Image.fromarray(arr.astype(np.uint8),'P'); i2.putpalette(PALF); i2.save(path,transparency=0)
opslaan(B,os.path.join(H,'sprite.png')); np.save(os.path.join(H,'P.npy'),P.astype(str))
r=PAL[B].astype(np.uint8); r[B==0]=(235,240,235); Image.fromarray(r).resize((512,512),Image.NEAREST).save(os.path.join(H,'sprite_8x.png'))
d=(PAL[A]*0.45+255*0.55).astype(np.uint8); d[A==0]=(250,250,250); d[A!=B]=(220,30,30)
Image.fromarray(d).resize((512,512),Image.NEAREST).save(os.path.join(H,'diff_r14.png'))
last={}
for l in LOG: last[(l[0],l[1])]=l
fin=sorted([l for (x,y),l in last.items() if B[y,x]!=A[y,x]],key=lambda l:(l[4],l[1],l[0]))
with open(os.path.join(H,'log.txt'),'w') as f:
    f.write('x y oud->nieuw onderdeel reden (t.o.v. r14/sprite.png)\n')
    for l in fin: f.write('%d %d %d->%d %s %s\n'%l)
    f.write('\nTELLING\n')
    for (k,rr),n in sorted(Counter((l[4],l[5]) for l in fin).items()): f.write('%-9s %-70s %d\n'%(k,rr,n))
    f.write('totaal %d\nkleuren %d\n'%(len(fin),len(np.unique(B))))
for l in fin: print('%d %d %d->%d %s %s'%l)
