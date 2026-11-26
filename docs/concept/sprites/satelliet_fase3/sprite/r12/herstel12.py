# r12 (25 nov): vanaf r11/sprite.png; ogen niet aangeraakt.
# Jordi over r11: "ik vind de ogen nu goed anders. Bovenste paneel moet alleen ietsje naar links, omdat het nu op een vlag
#   lijkt, maar de stok moet in het midden zitten ipv helemaal links, zelfde voor onderste paneel. Verder lijkt onderste en
#   rechtsboven allebei nog lichtjes afgekapt he. Ik snap dat ze overlappen, maar zijn nog een paar pixels leeg waar ze niet
#   overlappen"
# 1 PB en PF met de halve paneelbreedte terug langs de breedterichting (-(L-T)/2, dus naar links en iets omhoog): de stok
#   (oude linkerrand x = 123 model = 34,1 sprite) loopt nu over de middellijn v = 0,5, op dezelfde hoogte. Lengte, vakken en recept gelijk. Voor/achter (achter -> voor): PC, PA, PB, PF, PE,
#   romp; PB voor PA, PF achter PE en achter de voorbuis (romp blijft romp).
# 2 PC, PE en PF compleet: lege pixels binnen het eigen parallellogram (pixelmidden binnen) worden paneel; geen
#   "losse hoekpunt"-weghaalregel meer (die maakte de punten afgekapt). PA alleen waar PB hem eerst bedekte.
# Daarna het recept (recept.py = herstel10, reproduceert r11 met 0 afwijkingen) op PA/PB/PC/PE/PF; romprandpixels die nu
# aan transparant grenzen krijgen de omlijningsregel (zwart onder/rechts, navy elders).
import os, sys, numpy as np
from PIL import Image
from collections import Counter
H=os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0,os.path.join(H,'..','r10','pijp')); from geo10 import GEO10
sys.path.insert(0,H); import recept
im=Image.open(os.path.join(H,'..','r11','sprite.png')); PALF=im.getpalette()[:48]; PAL=np.array(PALF).reshape(16,3)
A=np.array(im).astype(int); B=A.copy()
P0=np.load(os.path.join(H,'..','r11','P_r11.npy'),allow_pickle=True).astype(object); P=P0.copy()
LOG=[]
def zet(x,y,c,deel,reden):
    if B[y,x]!=c: LOG.append((x,y,int(B[y,x]),int(c),deel,reden)); B[y,x]=c
G=dict(GEO10); G['PF']=((123.0,100.0),(123.0,147.0),(145.46913591942328,108.98765436776931))   # r11: PF volle lengte 47
def schuif(g):
    T,R,L=map(np.array,g); dv=-(L-T)/2      # halve breedte terug langs de breedterichting: stok (v=0) wordt middellijn,
    return tuple(tuple(p+dv) for p in (T,R,L)), dv   # en waar de stok het paneel raakt blijft op dezelfde hoogte
G['PB'],dxb=schuif(G['PB']); G['PF'],dxf=schuif(G['PF'])
ID={k:recept.ideaal(G[k]) for k in ('PA','PB','PC','PE','PF')}
# 1. eigendom opnieuw
P[(P=='PB')|(P=='PF')]=''
vrij=(P=='')
for y,x in zip(*np.where(vrij&ID['PC'])): P[y,x]='PC'
for y,x in zip(*np.where(vrij&ID['PA']&(P0=='PB'))): P[y,x]='PA'          # PA alleen waar PB hem bedekte
for y,x in zip(*np.where(ID['PB']&((P=='')|(P=='PA')))): P[y,x]='PB'       # PB voor PA, achter de romp
for y,x in zip(*np.where(ID['PF']&(P==''))): P[y,x]='PF'                   # PF achter romp/voorbuis
for y,x in zip(*np.where(ID['PE']&((P=='')|(P=='PF')))): P[y,x]='PE'       # PE voor PF
# PA: vrijgekomen losse punt (<=1 PA-buur) weg, zoals herstel10 bij scherpe hoeken
for y,x in zip(*np.where((P=='PA')&(P0!='PA'))):
    if sum(1 for dy,dx in ((-1,0),(1,0),(0,-1),(0,1)) if P[y+dy,x+dx]=='PA')<=1: P[y,x]=''
REDEN={'PA':'vrijgekomen achter PB (PB naar links)','PB':'PB symmetrisch om de stok (naar links)','PC':'PC compleet (lege pixel binnen het parallellogram)',
       'PE':'PE compleet (lege pixel binnen het parallellogram)','PF':'PF symmetrisch om de stok (naar links)'}
for k in ('PA','PB','PC','PE','PF'):
    for (x,y),c in recept.recept(k,G[k],P).items():
        r=REDEN[k] if P0[y,x]!=k else 'recept opnieuw (rand/lichte rand verschuift mee)'
        if k=='PF' and P0[y,x]!=k and A[y,x]==0: r='PF compleet / naar links (nieuw zichtbaar)'
        zet(x,y,c,k,r)
# PF valt nu half achter de voorbuis: waar een PF-vakpixel links aan romp grenst, navy paneelrand (anders loopt het lichte
#   vak zonder lijn in de witte buis over)
for y,x in zip(*np.where(P=='PF')):
    if P[y,x-1]=='#' and B[y,x] not in (1,2): zet(x,y,2,'PF','rand waar PF achter de voorbuis verdwijnt (navy)')
for y,x in zip(*np.where((P=='')&(B>0)&((P0=='PB')|(P0=='PF')))): zet(x,y,0,'leeg','paneelpixel buiten het nieuwe parallellogram -> transparant')
def leeg(x,y): return not(0<=x<64 and 0<=y<64) or B[y,x]==0
for y,x in zip(*np.where(P=='#')):
    if B[y,x]==0: continue
    lo,lr,lb,ll=leeg(x,y+1),leeg(x+1,y),leeg(x,y-1),leeg(x-1,y)
    if not(lo or lr or lb or ll) or A[y,x] in (1,2): continue
    if not any(leeg(x+dx,y+dy) and not(A[y+dy,x+dx]==0 if 0<=x+dx<64 and 0<=y+dy<64 else True) for dy,dx in ((1,0),(0,1),(-1,0),(0,-1))): continue
    zet(x,y,1 if (lo or lr) else 2,'omlijning','romprand grenst nu aan transparant')
assert len(np.unique(B))<=16
def opslaan(arr,path):
    i2=Image.fromarray(arr.astype(np.uint8),'P'); i2.putpalette(PALF); i2.save(path,transparency=0)
opslaan(B,os.path.join(H,'sprite.png')); np.save(os.path.join(H,'P_r12.npy'),P.astype(str))
r=PAL[B].astype(np.uint8); r[B==0]=(235,240,235); Image.fromarray(r).resize((512,512),Image.NEAREST).save(os.path.join(H,'sprite_8x.png'))
d=(PAL[A]*0.45+255*0.55).astype(np.uint8); d[A==0]=(250,250,250); d[A!=B]=(220,30,30)
Image.fromarray(d).resize((512,512),Image.NEAREST).save(os.path.join(H,'diff_r11.png'))
last={}
for l in LOG: last[(l[0],l[1])]=l
fin=[l for (x,y),l in last.items() if B[y,x]!=A[y,x]]
with open(os.path.join(H,'log_herstel12.txt'),'w') as f:
    f.write('verschuiving PB %s spritepx, PF %s spritepx\n'%(np.round(dxb/recept.S,2),np.round(dxf/recept.S,2)))
    f.write('x y oud->nieuw onderdeel reden (t.o.v. r11/sprite.png)\n')
    for l in sorted(fin,key=lambda l:(l[4],l[1],l[0])): f.write('%d %d %d->%d %s %s\n'%l)
    f.write('\nTELLING\n')
    for (k,rr),n in sorted(Counter((l[4],l[5]) for l in fin).items()): f.write('%-9s %-60s %d\n'%(k,rr,n))
    f.write('totaal %d\nkleuren %d (incl. transparant)\n'%(len(fin),len(np.unique(B))))
print('PB',np.round(dxb/recept.S,2),'PF',np.round(dxf/recept.S,2))
print('anders dan r11:',len(fin)); print(sorted(Counter((l[4],l[5]) for l in fin).items()))
