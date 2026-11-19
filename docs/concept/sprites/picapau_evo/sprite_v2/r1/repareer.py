# Reparaties op schoon.npy, elk benoemd en gemeten op het model -> r1.npy. Telt per zone de afwijking van de kale reductie.
# codes: 1 zwart, 2/3/4 bruin l/m/d, 5/6/7 creme l/m/d, 8 wang, 9/10/11 grijs l/m/d, 12/13 geel l/d, 14 wit, 15 selout bruin
import numpy as np
from celregel import cel
from kuif import U, L as KL, cells, pp
o=np.load('schoon.npy').copy(); kaal=np.load('kaal.npy'); H,W=o.shape
R={}
def zet(zone,lst):
    for x,y,v in lst:
        if o[y,x]!=v: R.setdefault(zone,[]).append((x,y,int(o[y,x]),v)); o[y,x]=v
def ring(zone,mask):
    # buitenlijn: gekleurde pixel in de zone die aan achtergrond grenst -> zwart (bruin aan de lichtkant -> selout)
    lst=[]
    for y,x in zip(*np.where(mask)):
        v=o[y,x]
        if v in (0,1,15): continue
        nb=[(y-1,x),(y+1,x),(y,x-1),(y,x+1)]
        bg=[0<=a<H and 0<=b<W and o[a,b]==0 for a,b in nb]
        if any(bg): lst.append((x,y,15 if v in (2,3,4) and (bg[0] or bg[2]) and not (bg[1] or bg[3]) else 1))
    zet(zone,lst)
# 1 kuif: middenlijn van beide slierten gemeten op het model (kuif.py), krul en haakje in de punten
z=np.load('lucht.npy'); kz=np.zeros_like(z); kz[0:11,12:49]=True; kz&=z
S=pp(cells(U)|cells(KL))
zet('kuif',[(x,y,1 if (y,x) in S else 0) for y,x in zip(*np.where(kz))]+[(x,y,1) for y,x in S])
# 1b krul en haakje leesbaar (model: spiraal ±2,6 px rond (45,4.6); haakje onderaan bij (41,9) met de punt omhoog):
#    krul = ruitje rond 1 gat op (45,4), haakje = J met het gat op (40,8)
zet('krul',[(44,5,0),(46,5,0),(45,6,0),(45,5,1),(46,4,1),(45,3,1),(44,4,1),(45,4,0)])
zet('haakje',[(40,8,0),(41,9,0),(39,7,1),(39,8,1),(40,9,1),(41,8,1)])
# 2 oog: glans wit linksboven (model: wit op x19 r11, bij de kale reductie achtergrond -> gat), oog rond naar het model
zet('oog',[(19,11,14),(20,11,1),(19,10,3),(21,13,5)])
# 3 snavel: celregel-model (bovenlijn d 24-26% als donkerbruine binnenlijn, punt grijs, onderlijn gesloten)
zet('snavel',[(14,12,4),(15,12,4),(12,14,9),(10,15,9),(9,16,0),(10,16,1),(16,16,10)])
# 4 bliksem: celregel op het model (>=50% wit = leeg, >=30% zwart = lijn), daarna buitenlijn
bz=np.zeros((H,W),bool); bz[27:44,0:11]=True; bz[44:49,0:13]=True
zet('bliksem',[(x,y,cel(x,y,zw=0.30)) for y,x in zip(*np.where(bz))])
ring('bliksem',bz)
# 5 poten: celregel (zw 33%) + buitenlijn
pz=np.zeros((H,W),bool); pz[44:54,17:31]=True
zet('poten',[(x,y,cel(x,y,zw=0.33)) for y,x in zip(*np.where(pz)) if cel(x,y,zw=0.33) in (0,1,9,10,11)])
ring('poten',pz)
np.save('r1.npy',o)
tot=0
for zn,l in R.items():
    print('%-10s %3d px'%(zn,len(l))); tot+=len(l)
d=(o!=kaal).sum(); print('totaal reparaties',tot,'| verschil met kale reductie (incl. schoon)',d)
