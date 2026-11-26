# Guarana fase 2, r8. Draaien vanuit guarana_fase2/: python3 sprite_r8/bouw6b.py && python3 sprite_r8/bouw8.py
# Basis = bouw6b (= r6-afwerking, maar achterste vruchten met dezelfde tinten als fase 1) + de r7-pupillen (diff r7-r6).
# Daarna benoemde reparaties (Jordi r7, zie NOTITIES). Elke pixel staat hieronder met reden.
import sys; sys.path.insert(0,'sprite_r8'); import numpy as np; from PIL import Image; from gemeen2 import *
K,L,S,M,H=1,2,3,4,5; l,s,m,h=6,7,8,9; W,g=10,11
b=np.array(Image.open('sprite_r8/basis.png')).astype(int)
r6=np.array(Image.open('sprite_r6/guarana2_r6.png')).astype(int); r7=np.array(Image.open('sprite_r7/guarana2_r7.png')).astype(int)
o=b.copy(); d7=r7!=r6; o[d7]=r7[d7]
LOG=[]
def zet(lijst,why):
    for x,y,v in lijst:
        if o[y,x]!=v: LOG.append((why,x,y,int(o[y,x]),v)); o[y,x]=v
# 2. R6 (rechtertros, 2e oog van rechts onderin) had geen pupil: wit (44,33)(45,33g)(45,34)(46,34)(45,35)(46,35), de 2x2 van r7 viel op de
#    buitenlijn. Pupil 2 px links in het wit (iets linksonder vanaf het midden), wit rechts en boven blijft.
#    r7 zette (44,34) zwart naast de zwarte buitenlijn -> één zwarte klont. (44,34) weer wit, pupil 2 px in de middenkolom, onderste helft.
zet([(44,34,W),(45,34,K),(45,35,K)],'R6 pupil')
# 3. M3 (middelste tros, links onder M2): in het model een half dicht oog (natief rond (70,82) -> sprite (21,20): dik lid, wit halve maan,
#    pupil links). Het lid was schaduwrood = zelfde tint als de vrucht erboven, dus het oog verdween. Lid + rand nu lijnrood rondom:
#    .LLL. / LKWWL / .LWL. / ..L..
zet([(21,19,L),(22,19,L),(23,19,L),(20,20,L)],'M3 lid lijnrood')
# M2 (zelfde probleem, onder de bovenste vrucht): lid lijnrood, linkerhoek lijnrood; (24,16) wordt vrucht (anders 4 px streep)
zet([(25,16,L),(26,16,L),(27,16,L),(24,17,L),(24,16,S)],'M2 lid lijnrood')
# 4. Middelste tros boven: bovenste linkervrucht ('_', x24-28 y12-15) en de vrucht van M1 (x29-32 y11-13) opnieuw ingekleurd als fase 1-vrucht:
#    lijn boven (groene lijn aan de bladkant), hooglicht linksboven, midden, schaduwsikkel rechtsonder, 1 px naad (x29) i.p.v. 2 px (x28-29).
# (geen groene lijn over de hele bovenkant: dat gaf een horizontale streep van 8 px; alleen de toppixel van de M1-vrucht als selout)
zet([(31,11,L)],'boven: top M1-vrucht')
zet([(25,12,H),(26,12,H),(27,12,M),(28,12,M),(29,12,L),(30,12,H),(31,12,H),(32,12,M)],'boven rij 12')
zet([(24,13,H),(25,13,H),(26,13,M),(27,13,M),(28,13,S),(29,13,L),(30,13,M)],'boven rij 13')
zet([(23,14,M),(24,14,M),(25,14,M),(26,14,M),(27,14,M),(28,14,S),(29,14,L),(30,14,S)],'boven rij 14')
zet([(23,15,L),(24,15,M),(25,15,M),(26,15,S),(27,15,S),(28,15,S),(29,15,L),(30,15,S)],'boven rij 15')
basis=o.copy()
# 1. L2 (bovenste oog linkertros, wit x13-16 y23-25) en R2 (rechtsboven rechtertros, wit x53-56 y23-25) kijken naar het midden.
#    oude pupilpixels -> wit; (a) pupil midden in het wit, (b) pupil naar het midden van de sprite (L2 rechts, R2 links). 3 px (L-vorm) zoals r5.
OUD={'L2':[(13,24),(13,25),(14,25)],'R2':[(54,24),(54,25),(55,25)]}
VAR={'a':{'L2':[(14,24),(15,24),(14,25)],'R2':[(54,24),(55,24),(54,25)]},
     'b':{'L2':[(15,24),(16,24),(15,25)],'R2':[(53,23),(53,24),(54,24)]}}
for v in ('a','b'):
    o=basis.copy()
    for n in OUD:
        for x,y in OUD[n]:
            if o[y,x]==K: o[y,x]=W
        for x,y in VAR[v][n]: o[y,x]=K
    # wit dat op een randplek (onderrand van r6-ronding) terechtkomt, is gecontroleerd: alle pixels liggen binnen het oog
    assert ((o>0)==(r7>0)).all(),'silhouet'
    opslaan(o,'sprite_r8/guarana2_r8%s.png'%v)
    print(v,'anders dan r7:',int((o!=r7).sum()))
open('sprite_r8/normal.pal','w').write(open('sprite_r6/normal.pal').read())
import json; open('sprite_r8/log.txt','w').write('\n'.join(map(str,LOG))); print(len(LOG),'px benoemd, zie log.txt')
