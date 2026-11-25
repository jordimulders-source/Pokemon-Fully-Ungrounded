"""Capykart r14: alleen de blokkentoren + achterste hoepel (bovenstuk) opnieuw opgezet; rest = r13 pixel-identiek.
Drie gelijke kubussen met rechte, evenwijdige (horizontale) naden zoals het model, licht bovenrandje (bevel) onder
elke naad, licht voorvlak links / donker zijvlak rechts; dakje met 2 px overstek; voet op het dek met contactschaduw;
hoepel komt onder de voet vandaan en buigt over de dekrand (glans) naar beneden."""
import os, sys
from collections import Counter
from PIL import Image
HERE=os.path.dirname(os.path.abspath(__file__)); R13=os.path.join(HERE,'../r13')
VAR=sys.argv[1] if len(sys.argv)>1 else 'A'
cr=Image.open(os.path.join(R13,'capykart_creme.png')); wt=Image.open(os.path.join(R13,'capykart_wit.png'))
base=[[cr.getpixel((x,y)) for x in range(64)] for y in range(64)]
g=[r[:] for r in base]
# symbolen: per versie naar index
CRE={'1':1,'4':4,'5':5,'6':6,'7':7,'8':8,'D':13,'LB':11,'F':15,'B':11,
     'Yf':9,'Yr':9,'Ys':6,'Ysr':5,'Yl':4,
     'Rf':12,'Rr':14,'Rs':7,'Rsr':12,'Rl':7,
     'Af':10,'Ar':9,'As':8,'Asr':10,'Al':8,'H':8,'Hg':9}
WIT=dict(CRE, Yf=14, Yr=9, Rr=9)
T={}
# ---- toren: x46..57 (links lijn 46, voorvlak 47-52, zijvlak 53-56, rechts lijn 57) ----
L,FR,SD,RT=46,(47,52),(53,56),57
blocks=[('Y',11),('R',18),('A',25)]          # (kleur, naadrij erboven); blok = naad+1 .. naad+6
for c,seam in blocks:
    for x in range(L,RT+1): T[(x,seam)]='1'
    for y in range(seam+1,seam+7):
        T[(L,y)]=c+'l'; T[(RT,y)]='1'
        rim = (y==seam+1)
        for x in range(FR[0],FR[1]+1): T[(x,y)]=c+('r' if rim else 'f')
        for x in range(SD[0],SD[1]+1): T[(x,y)]=c+('sr' if rim else 's')
for x in range(L,RT+1): T[(x,32)]='1'     # voetlijn
# ---- dakje: x44..59, top rij 2, eavelijn rij 11 ----
Lp=[51,50,49,48,47,46,45,44]; Rp=[53,54,55,56,57,58,59,59]
T[(52,2)]='1'
for i,y in enumerate(range(3,11)):
    for x in range(Lp[i],Rp[i]+1):
        T[(x,y)]='LB' if x==Lp[i] else ('1' if x==Rp[i] else ('F' if x<=52 else 'B'))
for x in range(44,60): T[(x,11)]='1'
# ---- leegmaken oude toren (zone x>=44,y<=31 behalve de achtergrond links van x46) ----
for y in range(0,32):
    for x in range(44,64):
        if x>=46 or y<=11: g[y][x]=0
# ---- dek, contactschaduw, hoepel (rij 31-35) ----
def put(y,x0,s):
    s=s if isinstance(s,list) else list(s)
    for i,ch in enumerate(s):
        if ch!='?': T[(x0+i,y)]=ch
T[(58,31)]='4'
T[(58,32)]='D'; T[(59,32)]='4'
put(33,46,'4'+'D'*13+'54')            # x46..60: voet-schaduw x47-58, dek x59, rand x60
if VAR=='B': put(33,48,'H1')          # hoepel loopt tot onder de voet
put(34,46,'455HH1'+'5'*9+'4')        # x46..61
put(35,46,['4','4','5','Hg','H','1']+['5']*10+['4'])      # x46..62
M={'1':'1'}
def build(MAP):
    o=[r[:] for r in g]
    for (x,y),s in T.items(): o[y][x]=MAP[s]
    return o
gc=build(CRE)
# wit: zelfde pixels als crème buiten de toren; r13_wit als basis
wbase=[[wt.getpixel((x,y)) for x in range(64)] for y in range(64)]
gw=[r[:] for r in wbase]
for y in range(64):
    for x in range(64):
        if gc[y][x]!=base[y][x]: gw[y][x]=gc[y][x]
for (x,y),s in T.items(): gw[y][x]=WIT[s]
suf='' if VAR=='A' else '_'+VAR
def save(grid,src,name):
    o=Image.new('P',(64,64)); o.putpalette(src.getpalette()); o.putdata([v for r in grid for v in r]); o.save(os.path.join(HERE,name),transparency=0)
    o.convert('RGBA').resize((512,512),Image.NEAREST).save(os.path.join(HERE,name.replace('.png','_8x.png')))
save(gc,cr,f'capykart_creme{suf}.png'); save(gw,wt,f'capykart_wit{suf}.png')
# ---- controles ----
zone=lambda x,y: x>=42 and y<=35
hoep=lambda x,y: 48<=x<=51 and 33<=y<=45
Lg=[]
out=[(x,y) for y in range(64) for x in range(64) if gc[y][x]!=base[y][x] and not zone(x,y)]
Lg.append(f'pixels anders dan r13 buiten torenzone (x>=42,y<=35): {len(out)} (crème), {sum(1 for y in range(64) for x in range(64) if gw[y][x]!=wbase[y][x] and not zone(x,y))} (wit)')
sil=[(x,y) for y in range(64) for x in range(64) if (base[y][x]==0)!=(gc[y][x]==0)]
add=sum(1 for x,y in sil if base[y][x]==0)
Lg.append(f'silhouet: {len(sil)} px verschil, alle in torenzone: {all(zone(x,y) for x,y in sil)} ({add} erbij, {len(sil)-add} weg)')
fz=[(x,y) for x in range(28,32) for y in range(16,22)]+[(x,y) for x in range(17,24) for y in range(30,34)]+[(21,15),(22,15),(23,15),(21,16),(22,16),(23,16),(15,22),(16,22),(18,28),(19,28)]+[(x,30) for x in range(25,29)]
Lg.append(f'bevroren gezicht ({len(fz)} px): crème diff {sum(gc[y][x]!=base[y][x] for x,y in fz)}, wit diff {sum(gw[y][x]!=wbase[y][x] for x,y in fz)}')
for nm,gr in (('crème',gc),('wit',gw)): Lg.append(f'{nm}: {len(Counter(v for r in gr for v in r))} kleuren incl. transparant')
Lg.append(f'pixels anders in torenzone: {sum(1 for y in range(36) for x in range(42,64) if gc[y][x]!=base[y][x])}')
open(os.path.join(HERE,f'controle{suf}.txt'),'w').write('\n'.join(Lg)+'\n'); print('\n'.join(Lg))
