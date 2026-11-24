# Ronde 2: benoemde reparaties van de keuring op r1 (coördinator, 22 nov). Basis = sprite_r1/baltoy_r1.txt; diff t.o.v. r1 per zone.
# Canvas (x,y) uit de opdracht = sprite (rij y-15, kol x-8).
import sys, numpy as np; from PIL import Image
sys.path.insert(0,'gereedschap'); from bouw_pal import PAL
ORDE='.KDdmlhRr'
r1=[list(r) for r in open('sprite_r1/baltoy_r1.txt').read().split()]; H,W=len(r1),len(r1[0])
g=[r[:] for r in r1]; E=[]
def zet(y,x,c,zone): g[y][x]=c; E.append((zone,y,x))
# 4. rechteroog 1 kolom smaller (8 -> 7, zoals het linkeroog en het model): kolom 26 (midden van het oog) eruit, 27-30 schuiven 1 naar links,
#    kolom 30 houdt zijn eigen inhoud. Rijen 14-20. Daardoor wordt de losse donkerrode (17,30) een paar van 2 px.
for y in range(14,21):
    oud=r1[y][:]
    for x in range(26,30): zet(y,x,oud[x+1],'rechteroog')
zet(14,29,'R','rechteroog')   # rode band rechts niet 1 px korter laten worden door de verschuiving (r1 had hier R)
# 5. losse donkerrode pixel (15,15) -> licht rood
zet(15,15,'R','rood')
# 2. hoofdband (rij 4-10) uit het model (natieve klassen rij 6-14): chakana = lichte kruisvorm (h) met lijn D
#    verticale arm kol 18-19 (rij 4-6 en 8-10), horizontale arm rij 7 kol 15-21, middenstip (7,18) d (model: donkere stip),
#    rechts van de verticale arm de grijze afschuining kol 20 (m) zoals het model, omlijning D.
for y in (4,5,6,8,9,10):
    zet(y,17,'D','chakana'); zet(y,18,'h','chakana'); zet(y,19,'h','chakana'); zet(y,21,'D','chakana')
for x in (14,15,16,17): zet(6,x,'D','chakana'); zet(8,x,'D','chakana')
for x in (21,22): zet(6,x,'D','chakana'); zet(8,x,'D','chakana')
zet(7,14,'D','chakana'); zet(7,22,'D','chakana')
for x in (15,16,17,19,20,21): zet(7,x,'h','chakana')
zet(7,18,'d','chakana')
#    trap links (één doorlopende D-lijn): (4,14) (5,12-14) (6,11-12) (7,11) (8,9-10) (9,9) (10,9)
for y,x in ((4,14),(5,12),(5,13),(5,14)): zet(y,x,'D','trap links')
#    tweede trap rechts van de chakana (natief kol 32-33, rij 12-14): D
for y,x in ((8,24),(8,25),(9,24),(10,24)): zet(y,x,'D','trap rechts')
#    losse h-/d-vlekjes naar l
for y,x in ((4,15),(4,16),(4,22),(4,23),(8,11),(9,10),(10,10)): zet(y,x,'l','vlekjes')
# 3. schaduw onderaan de punt: sikkel m langs de linkeronderrand, 1 px l naast de ribbe (kol 27 blijft l)
for y,x in ((43,23),(43,24),(44,24),(44,25),(45,25),(45,26),(46,26)): zet(y,x,'m','punt-schaduw')
# 1. rechterarm: dikte en armeind uit het verkleinde model, lijn buiten de vulling; vulling 4-5 px, knots 5 breed (rij 35-39),
#    afgerond (rij 40-41); bovenkant l, binnenkant m (zoals de linkerarm).
ARM={32:(38,39,44),33:(38,39,44),34:(39,40,45),35:(40,41,46),36:(40,41,46),37:(40,41,46),38:(40,41,46),39:(40,41,46),40:(41,42,45)}
for y in range(32,42):
    for x in range(37,47):
        if g[y][x]!='.' and x>=37: pass
    for x in range(37,47): 
        if (y,x)!=(32,37): g[y][x]=g[y][x]
for y,(kin,f0,kuit) in ARM.items():
    for x in range(37,47):
        if x<kin: c='.' if r1[y][x] in '.K' and x>=38 else r1[y][x]
        elif x==kin or x==kuit: c='K'
        elif x<kuit:
            n=kuit-f0; i=x-f0
            c='m' if (i<2 or (y>=39 and i<3) or y==40) else 'l'
        else: c='.'
        if g[y][x]!=c: zet(y,x,c,'rechterarm')
for x in range(37,47):
    c='K' if 42<=x<=44 else '.'
    if g[41][x]!=c: zet(41,x,c,'rechterarm')
OUT='sprite_r2/'
open(OUT+'baltoy_r2.txt','w').write('\n'.join(''.join(r) for r in g)+'\n')
pal=[PAL[c] for c in ORDE]; flat=sum(pal,())
idx=np.zeros((64,64),'uint8'); oy=64-H-1; ox=(64-W)//2
for y in range(H):
    for x in range(W): idx[oy+y,ox+x]=ORDE.index(g[y][x])
im=Image.fromarray(idx,'P'); im.putpalette(list(flat)+[0]*(48-len(flat))); im.save(OUT+'baltoy_r2.png',transparency=0)
rgb=Image.open(OUT+'baltoy_r2.png').convert('RGBA'); bg=Image.new('RGBA',(64,64),(255,255,255,255)); bg.alpha_composite(rgb)
bg.convert('RGB').resize((512,512),Image.NEAREST).save(OUT+'baltoy_r2_8x.png')
from collections import Counter
d=[(y,x) for y in range(H) for x in range(W) if g[y][x]!=r1[y][x]]
zones={}
for z,y,x in E:
    if g[y][x]!=r1[y][x]: zones[(y,x)]=z
with open(OUT+'diff_r2.txt','w') as f:
    c=Counter(zones.get(p,'?') for p in d)
    f.write('pixels anders dan r1: %d per zone %s\n'%(len(d),dict(c)))
    for y,x in d: f.write('%s (%d,%d) canvas(x%d,y%d) %s->%s\n'%(zones.get((y,x),'?'),y,x,x+ox,y+oy,r1[y][x],g[y][x]))
print(len(d),dict(c))
