# fix.py: pixelreparaties op de kale reductie (kaal.npy) -> sprite.png. Elke wijziging met zone en reden.
import numpy as np
from PIL import Image
o=np.load('kaal.npy').copy(); k=o.copy()
I={'.':0,'#':1,'D':2,'P':3,'p':4,'W':5,'w':6,'l':7,'m':8,'T':9,'t':10}
FIX=[ # (zone, rij, kolom, nieuw, reden)
 # buitenlijn bol lichtkant: modelkleur (100,57,120) overal dezelfde donkerpaarse selout
 *[('omlijning',r,c,'D','selout lichtkant uniform (model 100,57,120)') for r,c in ((16,13),(16,14),(17,11),(17,12),(18,9),(18,10),(19,8),(20,7),(22,5),(22,6),(23,5),(24,4),(30,2),(34,2))],
 ('omlijning',38,3,'#','geen zwart/paars om en om: vanaf rij 37 zwart'),
 # voetje linksboven: onderrand doorlopend
 ('voet LB',15,18,'P','onderrand voet (model ppll gelijkspel)'),
 ('voet LB',12,23,'P','model-2 in antennevoet, paars i.p.v. lijftint'),
 # oog: buitenrand ring
 ('oog',27,7,'P','ringrand (model l2)'),('oog',27,8,'P','ringrand sluiten tegen lijf'),
 ('oog',27,13,'P','ringrand (model 2)'),('oog',28,7,'P','ringrand links sluiten (model Ph)'),
 ('oog',34,4,'D','ringrand links (model 2)'),('oog',35,4,'D','ringrand links (model 2)'),
 ('oog',36,15,'#','ringrand rechtsonder zwart zoals rij 31-35/37'),
 ('oog',39,8,'#','ringrand onder sluiten (model 2)'),
 # oog: ringvulling / binnenring
 ('oog',30,6,'p','wit gat in de ring (reductie)'),
 ('oog',35,6,'D','binnenring links (model 2), als rij 32-34'),
 ('oog',36,13,'P','binnenring rechtsonder (model 2)'),
 ('oog',37,11,'P','binnenring onder (model t22p)'),
 # pupil rond (4x5): uitsteeksel links weg, gat linksboven dicht
 ('oog',33,7,'T','pupiluitsteeksel -> iris (model tDt#)'),
 ('oog',35,8,'T','paarse pixel in iris onder pupil -> iris'),
 ('oog',32,8,'#','pupil rond: rij 32 = 8-11 zoals 33-34'), # naad: 1 px, eigen tint P (model 112,66,139), geen zwart/donkerpaars wisselend
 *[('naad',r,c,'P','naad uniform P (was D/p)') for r,c in ((27,30),(28,30),(29,29),(30,29),(31,29),(32,29),(34,27),(35,26),(37,24),(40,21),(41,19))],
 # lichtband naast de naad (model q, 1 modelpx) -> lijfbasis i.p.v. lichtpaars, anders leest de naad dubbel
 *[('naad',r,c,'w','lichtband naast naad -> lijf w') for r,c in ((26,31),(29,30),(34,28),(35,27),(36,26),(37,25),(38,24),(39,23),(40,22),(41,21),(42,18),(43,15),(43,16),(43,17))],
 *[('naad',44,c,'l','schaduwband onder naad (model qqqq) -> lijf l i.p.v. lichtpaars') for c in range(10,15)],
 # bolrand onder/rechts: model-reflectierand (163,137,194) en dubbele binnenlijn -> lijftinten
 *[('bol rand',r,c,'l','reflectierand (model h) -> lijf l') for r,c in ((49,14),(49,25),(49,27),(50,16),(50,17),(50,18),(51,19),(51,20),(51,22),(31,37),(32,37),(33,37),(36,37),(40,36),(43,34),(42,35),(50,25),(51,18))],
 ('bol rand',49,13,'m','dubbele binnenlijn onder (model P) -> diepe schaduw'),
 ('bol rand',50,15,'m','dubbele binnenlijn onder (model P) -> diepe schaduw'),
 # bol rechtsboven / voet RB: open rand sluiten
 ('bol rand',17,29,'D','buitenrand bol rechtsboven (model 2W)'),
 ('bol rand',17,28,'w','lijf naast buitenrand (model p, 1 px ruis)'),
 ('voet RB',18,29,'D','voetrand linksboven (model l2wP)'),
 ('voet RB',18,30,'D','open rand bovenkant voet sluiten (model 2h)'),
 ('voet RB',18,31,'D','open rand bovenkant voet sluiten (model Ph)'), # rimpixels oog/bol (model anti-aliasing l naast een lijn) -> lijf w
 *[('oog',r,c,'w','AA-randje (model l/1) naast oogring -> w') for r,c in ((28,6),(38,6),(40,8),(40,12),(36,16))],
 ('omlijning',40,4,'w','AA-randje (model l) naast buitenlijn -> w'),
 # voet LB: verlichte bovenkant donkerpaars i.p.v. zwart, open randen dicht
 *[('voet LB',12,c,'D','bovenrand voet aan lichtkant: D i.p.v. zwart (model #)') for c in (19,20,21)],
 ('voet LB',13,18,'D','open rand (p tegen transparant)'),('voet LB',14,17,'D','open rand (P tegen transparant)'),
]
for z,r,c,n,why in FIX: o[r,c]=I[n]
# antennes: bovenrand = D (outline base aan de lichtkant), onderrand/punt rechts = zwart; alleen P/p-pixels die aan transparant grenzen
ZONES={'A1':(5,12,23,45),'A2':(6,18,37,63),'A3':(31,38,39,63),'A4':(48,59,37,63)}
for z,(y0,y1,x0,x1) in ZONES.items():
    for y in range(y0,y1):
        for x in range(x0,x1):
            if o[y,x] in (3,4):
                if o[y-1,x]==0: FIX.append((z,y,x,'D','bovenrand antenne open -> D')); o[y,x]=2
                elif o[y+1,x]==0 or o[y,x+1]==0: FIX.append((z,y,x,'#','onder/punt antenne open -> zwart')); o[y,x]=1

# dikte herstellen langs de modelas (antennes >= 2 px kleur + omlijning)
for z,r,c,n,why in (('A1',12,30,'P','dubbele zwarte trap -> kleur, antenne 2 px dik (model #)'),
                    ('A3',33,54,'p','terug naar modelkleur (model pP), anders 1 px dik'),
                    ('A3',32,54,'D','NIEUW (niet uit model): bovenrand 1 px verlengd zodat x54 dicht is')):
    FIX.append((z,r,c,n,why)); o[r,c]=I[n]
np.save('sprite.npy',o)
PAL=[(152,208,160),(24,20,32),(84,46,108),(118,70,150),(168,118,202),(255,255,255),(226,220,244),(174,162,218),(130,114,184),(56,128,140),(140,204,200)]
p=Image.fromarray(o.astype('uint8'),'P'); pal=[v for c in PAL for v in c]; p.putpalette(pal+[0]*(48-len(pal))); p.save("sprite.png",transparency=0,bits=4)
from collections import Counter
print('afwijkingen van kale reductie per zone:',Counter(z for z,r,c,n,w in FIX if k[r,c]!=I[n]),'totaal',int((o!=k).sum()))
print('kleuren',len(set(o.ravel()))-1)
# eindtelling: per pixel de laatste reparatie, alleen echte verschillen met de kale reductie
last={}
for z,r,c,n,why in FIX: last[(r,c)]=(z,n,why)
from collections import defaultdict
per=defaultdict(list)
for (r,c),(z,n,why) in last.items():
    if o[r,c]!=k[r,c]: per[z].append((r,c,".#DPpWwlmTt"[k[r,c]],n,why))
with open('afwijkingen.txt','w') as fh:
    for z in sorted(per):
        fh.write(f'## {z}: {len(per[z])} px\n')
        for r,c,old,n,why in sorted(per[z]): fh.write(f'  (rij {r}, kol {c}) {old} -> {n}  {why}\n')
print({z:len(v) for z,v in per.items()},'som',sum(len(v) for v in per.values()),'echte diff',int((o!=k).sum()))
