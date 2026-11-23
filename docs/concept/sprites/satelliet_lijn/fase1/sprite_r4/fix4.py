# fix4.py: reparaties op de kale reductie (kaal.npy, factor 0,617) -> sprite.png. Elke wijziging met zone en reden.
import numpy as np
from PIL import Image
k=np.load('kaal.npy'); o=k.copy()
I={'.':0,'#':1,'D':2,'P':3,'p':4,'W':5,'w':6,'l':7,'m':8,'T':9,'t':10}
LOG=[]
def S(z,r,c,n,why):
    LOG.append((z,r,c,n,why)); o[r,c]=I[n]
def many(z,pts,n,why):
    for r,c in pts: S(z,r,c,n,why)
# ---- bol: selout lichtkant uniform D, vanaf rij 38 zwart
many('omlijning',[(22,17),(22,18),(23,15),(23,16),(24,14),(25,13),(26,12),(27,11),(28,11),(30,10),(33,9),(36,9)],'D','selout lichtkant uniform D (model 100,57,120)')
S('omlijning',39,9,'#','geen D tussen zwart (rij 38-40 zwart)')
# ---- bol onderrand: reflectierand (model h) -> l; L-hoeken in de zwarte trap linksonder weg
many('bol rand',[(48,20),(48,21),(48,27),(49,22),(49,23),(49,24),(49,25)],'l','reflectierand (model 163,137,194) -> lijf l')
S('bol rand',44,13,'l','zwarte L-hoek linksonder -> vulling'); S('bol rand',45,14,'m','zwarte L-hoek -> vulling'); S('bol rand',48,19,'m','zwarte L-hoek -> vulling')
# ---- oog: buitenrand D (licht) / zwart (schaduw), vulling p, iris, pupil rond
many('oog',[(30,13),(30,14),(30,15),(30,16),(30,17),(31,12),(31,18),(32,12),(32,19),(33,11),(33,19)],'D','buitenrand oogring (lichtkant) dicht')
many('oog',[(34,11),(35,11),(36,11),(37,11)],'D','buitenrand oogring links (was p)')
many('oog',[(34,12),(35,12),(36,12),(33,12),(32,16)],'p','ringvulling (was D/w/P: binnenring past niet op deze maat)')
many('oog',[(35,18),(36,18)],'P','ringvulling schaduwkant (was D)')
S('oog',35,13,'T','pupiluitsteeksel -> iris'); S('oog',38,16,'T','iris onder (model m)')
S('oog',38,12,'P','ringvulling i.p.v. zwarte hoek'); S('oog',39,13,'P','ringvulling i.p.v. zwarte hoek'); S('oog',39,12,'#','buitenrand linksonder sluiten (model l)')
# ---- naad: 1 px P, lip ernaast w
many('naad',[(30,31),(31,31),(32,30),(33,30),(36,29),(37,28),(38,26),(38,27),(41,22),(42,12),(43,15),(43,16),(43,17),(43,18),(43,19)],'P','naad 1 px, tint P')
many('naad',[(36,28),(39,26),(40,25),(41,24),(42,22),(43,20)],'w','lip naast de naad -> w')
# ---- voet LB
many('voet LB',[(19,22),(19,23),(19,24)],'D','bovenkant voet lichtkant D i.p.v. zwart')
S('voet LB',20,21,'D','open rand links'); S('voet LB',20,25,'P','zwarte binnenpixel tussen voet en antenne -> P')
# ---- antennes: per kolom bovenrand D, onderrand zwart, binnen >=2 kleur (zo nodig 1 px erbij onderaan)
ANT={'A1':(26,41,13,22,(38,39,40)),'A2':(42,55,13,24,(53,54)),'A3':(39,55,32,41,(53,54)),'A4':(38,54,46,56,(52,53))}
for z,(x0,x1,y0,y1,tip) in ANT.items():
    for x in range(x0,x1):
        col=o[y0:y1,x]; nz=np.where(col>0)[0]
        if len(nz)==0: continue
        t=y0+nz[0]; b=t
        while b+1<y1 and o[b+1,x]>0: b+=1   # alleen de eerste aaneengesloten run (de antenne zelf)
        if (b-t+1)<4 and x not in tip:
            S(z,b+1,x,'#','NIEUW (niet uit reductie): antenne 1 px verdikt onderaan langs de modelas'); b+=1
        if o[t,x]!=2: S(z,t,x,'D','bovenrand antenne D')
        if o[b,x]!=1: S(z,b,x,'#','onderrand antenne zwart')
        for y in range(t+1,b):
            if o[y,x] in (1,2): S(z,y,x,'P','binnen antenne: lijnpixel -> kleur')
S('A2',16,54,'#','punt antenne 2 rechts: open rand (P tegen transparant) -> zwart')
# ---- tweede pas: voetjes, wortels, zwarte hoeken
S('A1',19,25,'D','open bovenrand bij de wortel')
S('A2',21,40,'D','open bovenrand'); S('A2',22,37,'D','open bovenrand bij de wortel')
S('A2',21,38,'D','NIEUW (niet uit reductie): bovenrand wortel 1 px, zodat kol 38 2 px kleur houdt')
S('bol rand',22,29,'D','buitenrand bol rechtsboven (lichtkant)')
many('voet RB',[(23,30),(23,31),(23,32)],'D','open bovenrand (lijftint/p tegen transparant)')
S('voet RB',22,34,'D','bovenkant voet lichtkant D i.p.v. zwart')
many('voet RB',[(25,30),(26,30)],'D','linkerrand voet (lichtkant)')
many('voet RB',[(28,32),(27,35),(24,35)],'P','zwarte L-hoek -> vulling')
many('voet RO',[(44,32),(44,34),(45,31)],'D','bovenkant/linksboven voet lichtkant D i.p.v. zwart')
many('voet RO',[(48,34),(48,35)],'P','zwart 2x2/L onderaan voet -> vulling')
many('A4',[(47,36),(47,37)],'D','bovenrand wortel antenne 4 (lichtkant) D i.p.v. zwart')
S('A4',49,37,'P','D binnen de antenne -> kleur')
S('A3',36,38,'D','bovenrand wortel antenne 3 (lichtkant) D i.p.v. zwart')
S('A2',24,38,'P','zwarte L-hoek onderrand wortel -> kleur')
S('voet RO',48,34,'#','terug naar reductie (rand)')
S('voet RO',48,31,'P','zwarte L-hoek -> vulling voet')
S('bol rand',23,17,'W','losse w-pixel -> hooglicht')
S('naad',32,31,'w','lichtpaars naast naad -> lip w')
many('bol rand',[(31,36),(32,36),(38,36),(39,36),(48,27)],'m','losse reflectiepixel (l) in diepe schaduw -> m')
S('bol rand',50,25,'.','onderrand 4 px vlak -> 3 (rondheid, 1 px eraf)')
S('bol rand',49,25,'#','onderrand sluiten na (50,25)')
S('bol rand',43,11,'#','NIEUW (niet uit reductie): trap linksonder 2-1-2 -> 2-2-1, spiegel van linksboven (rondheid)')
S('bol rand',43,12,'l','was buitenlijn, ligt nu binnen de nieuwe rand')
S('oog',34,16,'T','pupilhoek rechtsboven -> iris: pupil 2-3-3-2 (rond i.p.v. blok)')
np.save('sprite.npy',o)
PAL=[(152,208,160),(24,20,32),(84,46,108),(118,70,150),(168,118,202),(255,255,255),(226,220,244),(184,174,226),(140,126,194),(56,128,140),(140,204,200)]
p=Image.fromarray(o.astype('uint8'),'P'); pal=[v for c in PAL for v in c]; p.putpalette(pal+[0]*(48-len(pal))); p.save('sprite.png',transparency=0,bits=4)
last={}
for z,r,c,n,why in LOG: last[(r,c)]=(z,n,why)
from collections import defaultdict
per=defaultdict(list)
for (r,c),(z,n,why) in last.items():
    if o[r,c]!=k[r,c]: per[z].append((r,c,".#DPpWwlmTt"[k[r,c]],n,why))
with open('afwijkingen.txt','w') as fh:
    for z in sorted(per):
        fh.write(f'## {z}: {len(per[z])} px\n')
        for r,c,old,n,why in sorted(per[z]): fh.write(f'  (rij {r}, kol {c}) {old} -> {n}  {why}\n')
print({z:len(v) for z,v in per.items()},'diff',int((o!=k).sum()),'nieuw',int(((o>0)&(k==0)).sum()),'px',int((o>0).sum()),'zwart',int((o==1).sum()))
