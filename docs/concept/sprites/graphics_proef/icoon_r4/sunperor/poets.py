"""r4 Sunperor: gerichte reparatie van r3 (icoon_r3/sunperor/icon_f1.png). Alleen twee punten:
 (1) kroon en kop apart geschaald (bouw.py: kop 1,25/1,45 x S rond het halsgewricht, kroon KR x S aan de kruin) -> kroon kleiner,
     gezicht (masker, ogen, haaksnavel) opnieuw gepoetst op de nieuwe plek;
 (2) lijfkleur: bruinzwart lijf werd grijs 1; pal5 blijft (beste palet gewogen naar oppervlak, zie pal.txt), maar de lijfvulling
     wordt 14 (98,98,90), de dichtstbijzijnde pal5-kleur voor front 2/3 (zoals Honchkrow/Noctowl/Murkrow hun lijf vullen).
Romp, staf, hand, vleugel en poten blijven pixel voor pixel r3 (alleen omgekleurd). python3 poets.py [KR] -> icon_f1.png"""
import sys,os,numpy as np
from collections import Counter
from PIL import Image
H=os.path.dirname(os.path.abspath(__file__))+'/'
KR=sys.argv[1] if len(sys.argv)>1 else '1.05'
sys.argv=['bouw.py','A',KR]; __file__=H+'bouw.py'
exec(open(H+'bouw.py').read().split("if __name__")[0])
r3=np.array(Image.open(H+'../../icoon_r3/sunperor/icon_f1.png')); c=r3.copy(); LOG=Counter()
def raster(zone,y,x0,rij):
    for i,ch in enumerate(rij):
        if ch==' ': continue
        v=0 if ch=='.' else int(ch,16)
        if c[y,x0+i]!=v: c[y,x0+i]=v; LOG[zone]+=1
# --- behouden uit r3: vleugel (rasters uit r3 poets/frame2) en staf (rij 16-17, x8-12) ---
V=[(13,23,'ff'),(14,22,'f66f'),(15,22,'f61f'),(16,22,'f61f'),(17,18,'ffff61e'),(18,18,'66666e'),(19,18,'11111e'),(20,18,'eeeee')]
houd=np.zeros_like(c,bool); houd[18:]=True
for y,x0,r in V: houd[y,x0:x0+len(r)]=True
houd[16:18,8:12]=True; houd[17,12]=True
c[~houd]=0
# --- LIJFKLEUR (punt 2): r3-omlijning 14 -> 15 (icon.png: omlijning 65), daarna lijfgrijs 1 -> 14 ---
c[c==14]=15; c[houd&(c==1)]=14
# --- KROON (punt 1): kroonlaag uit bouw.py (KR x S aan de kruin, volgt de kop) ---
k=laag(['kroon']); k[15:]=0
c[(c==0)&(k>0)]=k[(c==0)&(k>0)]
# --- KOP (punt 1): kop 1,25 x 1,45 x S; front x22-33 -> x12,4-17,8; rij 19-27 -> 12,9-17,1 (bouw.naar_icoon). Interieur x12-17, rij 13-17;
#  omlijning x11 en x18. Per icoonrij de frontrij(en) die erop vallen:
#  rij 13 = front 20-21: kruin bruinzwart (3/2 -> 14) met lichtbruin links (4 -> 6), rood aan de zijkant (5 -> a)
#  rij 14 = front 22: masker rood (5/6 -> a), witte snavelrug (26-27,22) -> x14 wit 3
#  rij 15 = front 23-24: ogen = wit met donkere pupil naar buiten: links (23,23) donker -> x12, (24,23) wit -> x13;
#           snavel (27,23) grijsblauw -> x14 grijs 1; rechts (29,23) wit -> x15, (30-31,23) donker -> x16; (32,23) rood -> x17
#  rij 16 = front 25-26: haaksnavel (23-26, grijsblauw) -> x12-14 grijs, rood (28-31) -> x15-17
#  rij 17 = front 27 (+26): onder de haak donker (24-25) -> x13, kin rood (26-29,26) -> x14-16, keel donker (30-31,27) -> x17
#  rij 12 = front 18-19: kroon (paarse rand links, oranje, rood) met de kruinlijn van de kop (26-28,19) -> x14-15
#  rij 13 = front 20-21: kroonrand links (rood) | kop: omlijning x12/x17, lichtbruin x13 (front 4), bruinzwart x14-16 (2/3 -> 14) | kroonrand rechts
#  rij 14 = front 22: onderrand van de kroon (omlijning) links x8-11 en rechts x18-22; masker rood met witte snavelrug x14
#  rij 15 = front 23-24: ogen wit met pupil naar buiten (pupil = front 2 -> 14): links x12-13, rechts x15-16; snavel grijs x14; rood x17
#  rij 16 = front 25-26: haaksnavel grijs x12-14 (punt links onder, front (23,26)), rood x15-17
#  rij 17 = front 26-27: donker onder de haak x12-13, kin rood x14-16, keel x17 (14)
raster('kroon',12,8,'fbddaaffaaaaaabf')
raster('kroon',10,10,'cdd')
raster('kop',13,8,'fbdaf6eeefaaaab')
raster('kop',14,8,'ffffaa3aaafffff')
raster('kop',15,9,'fffe313eaf')
raster('kop',16,11,'f111aaaf')
raster('kop',17,11,' ffaaaef')
# KROONPUNT (lappet 0,6xS aan de linker kroonrand, >= 2 px dik): als r3 (rij 15-17, x6-9), hangt nu aan de kroonrand (8,14)
raster('kroonpunt',14,7,'f'); raster('kroonpunt',15,6,'fadf'); raster('kroonpunt',16,6,'fbbf'); raster('kroonpunt',17,7,'ff')
# hals sluit aan: r3-rij 18 begon met omlijning op x12 en x17 -> blijft
# --- KROON poetsen: omlijning dicht, stippen, top rond ---
m=c>0; pad=np.pad(m,1); edge=m&~(pad[:-2,1:-1]&pad[2:,1:-1]&pad[1:-1,:-2]&pad[1:-1,2:])
for y,x in zip(*np.nonzero(edge)):
    if y<=14 and c[y,x] not in (15,): c[y,x]=15; LOG['kroonrand']+=1
# STAFKOP 1 rij hoger (rij 16, x9-10 goud zoals de rij eronder): anders vormen kroonrand (rij 14), tussenrij 15 en stafrand (rij 16)
#  een zwart blok van 3 rijen links van het gezicht; in de front staat de stafkop even hoog als de kroonrand (rij 18-22)
raster('staf',16,9,'89')
# PAARSE KROONRAND (front: de waaier is paars omrand, lila waar het licht valt): de r3-rand ging bij het omlijnen verloren.
#  Kroonpixels in rij 6-11 die aan de buitenomlijning grenzen: links van het midden lila c, rechts paars b (zoals r3: 'fccddc9bff')
m=c>0; pad=np.pad(m,1); buiten=m&~(pad[:-2,1:-1]&pad[2:,1:-1]&pad[1:-1,:-2]&pad[1:-1,2:])
rand=[]
for y in range(6,12):
    for x in range(32):
        if c[y,x] in (0,15): continue
        if any(buiten[y+dy,x+dx] for dx,dy in ((0,-1),(-1,0),(1,0))): rand.append((x,y))
for x,y in rand: c[y,x]=12 if x<14 else 11; LOG['kroonrand paars']+=1
# STIPPEN: 15 in de front; kroon is kleiner (1,05 x S) -> 6 stippen van 1 px (geel 9) op hun afgebeelde plek, op een boog zoals de front,
#  niet op de rand, niet naast elkaar: front (15,14),(19,10),(23,7),(29,6),(37,10),(42,14) -> onderstaande
for x,y in [(10,11),(11,9),(13,8),(15,8),(18,9),(20,11)]:
    if c[y,x] not in (0,15): c[y,x]=9; LOG['stippen']+=1
# ONDERRAND lichter (Gen 3/icoon_check: omlijning boven 15, onder 14): randpixels in de onderste helft (rij >= 18) worden 14,
#  behalve waar ze aan de nu donkere lijfvulling 14 grenzen (daar blijft 15, anders valt de lijfrand weg)
m=c>0; pad=np.pad(m,1); buiten=m&~(pad[:-2,1:-1]&pad[2:,1:-1]&pad[1:-1,:-2]&pad[1:-1,2:])
c0=c.copy()
for y,x in zip(*np.nonzero(buiten)):
    if y>=18 and c0[y,x]==15 and not any(c0[y+dy,x+dx]==14 for dx,dy in ((1,0),(-1,0),(0,1),(0,-1))): c[y,x]=14; LOG['onderrand']+=1
if __name__=='__main__':
    im=Image.fromarray(c,'P'); im.putpalette(IP.flatten().tolist()); im.save(H+'icon_f1.png',transparency=0)
    print(dict(LOG))
