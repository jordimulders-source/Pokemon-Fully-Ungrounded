# Guarana fase 2, r9: alleen de buitenomlijning van de trossen. Draaien vanuit guarana_fase2/: python3 sprite_r9/bouw9.py
# Jordi r8: "hij is nog wat blurry maar dat zit puur in de omlijning van de fruittrossen, de vormen lijken van een afstandje afgekapt,
# alsof het rechte lijnen zijn ipv rondere vruchten".
# 1 silhouet: per vrucht een boogje, inkeping waar twee vruchten elkaar raken (alleen hieronder benoemde pixels, alle binnen 1 px van de rand).
# 2 lijnkleur zoals fase 1: elke trospixel aan de achtergrond = buitenlijn, zwart waar de achtergrond rechts/onder ligt, lijnrood waar hij
#   links/boven ligt; geen vul- of oogwittint op de buitenlijn. Oud-lijnpixels die binnen komen te liggen -> vulling (benoemd).
import sys; sys.path.insert(0,'sprite_r9'); import numpy as np; from PIL import Image; from gemeen2 import *; from hulp import *
K,L,S,M,H=1,2,3,4,5; W=10
WEG=[  # (x,y): randpixel weg -> inkeping
 (7,26),   # linkertros links: grens bovenste vrucht (rij 23-25 op x6) / vrucht met L1-oog (rij 27-28 op x7), inkeping naar x8
 (7,29),   # linkertros links: grens vrucht met L1-oog / vrucht eronder, inkeping naar x8
 (12,37),  # linkertros onder: grens onderste-linkervrucht / puntvrucht, inkeping
 (56,26),  # rechtertros rechts: naad (rij 26, x54-56) raakt de rand -> inkeping
 (52,36),  # rechtertros rechtsonder: grens tussen de twee onderste vruchten
]
BIJ=[  # (x,y): achtergrond erbij -> bolling
 (57,28),(57,29),(57,30),   # rechtertros rechts: vrucht rij 27-31 bolt 1 px uit (was recht x56 over 7 rijen)
 (55,33),(54,34),           # rechtertros rechtsonder: vrucht rij 32-35 rond i.p.v. rechte diagonaal
]
VULNAAR={(56,28):S,(56,29):S,(56,30):S,(54,33):S,(53,34):S}   # oude buitenlijn die binnen komt te liggen: schaduwsikkel (rechts/onder)
TROSBOX=[(4,20,22,42),(40,20,62,41),(16,8,38,30)]   # x0,y0,x1,y1 van de drie trossen (alleen daar lijnkleur herzien)
def bg(o,y,x): return not ok(y,x) or o[y,x]==0
def maak(src,uit):
    o=np.array(Image.open(src)).astype(int); o0=o.copy()
    for x,y in WEG: assert o[y,x] in (1,2,3,4,5),(x,y,o[y,x]); o[y,x]=0
    for x,y in BIJ: assert o[y,x]==0,(x,y); o[y,x]=K
    for (x,y),v in VULNAAR.items(): o[y,x]=v
    LOG=[]
    def intros(x,y): return any(x0<=x<x1 and y0<=y<y1 for x0,y0,x1,y1 in TROSBOX)
    for y in range(64):
        for x in range(64):
            if o[y,x] not in (1,2,3,4,5,10,11) or not intros(x,y): continue
            nb=[(dy,dx) for dy,dx in N4 if bg(o,y+dy,x+dx)]
            if not nb: continue
            # alleen rode/oog-pixels (niet de groene lijnen); zwart dat alleen aan groen en achtergrond grenst (stam-/bladlijn) overslaan
            if o[y,x]==1 and not any(ok(y+dy,x+dx) and o[y+dy,x+dx] in (2,3,4,5,10,11) for dy,dx in N8): continue
            v=K if any(e in ((1,0),(0,1)) for e in nb) else L
            if o[y,x]!=v: LOG.append((x,y,int(o[y,x]),v)); o[y,x]=v
    assert ((o>0)!=(o0>0)).sum()==len(WEG)+len(BIJ)
    opslaan(o,uit)
    return o,o0,LOG
if __name__=='__main__':
    for v in ('a','b'):
        o,o0,LOG=maak('sprite_r8/guarana2_r8%s.png'%v,'sprite_r9/guarana2_r9%s.png'%v)
        print(v,'anders dan r8',int((o!=o0).sum()),'| lijnkleur herzien',LOG)
    open('sprite_r9/normal.pal','w').write(open('sprite_r8/normal.pal').read())
