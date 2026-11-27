# Guarana fase 2, r10: buitenrand van de drie trossen geschulpt (per vrucht een bolling, inkeping ertussen). Vanuit guarana_fase2/:
#   python3 sprite_r10/bouw10.py
# Jordi r8: "hij is nog wat blurry maar dat zit puur in de omlijning van de fruittrossen, de vormen lijken van een afstandje afgekapt,
# alsof het rechte lijnen zijn ipv rondere vruchten". Start = r9a/r9b; beide krijgen exact dezelfde wijziging.
# Werkwijze: DEL (randpixel weg = inkeping), ADD (achtergrond erbij = bolling), daarna lijnkleur zoals fase 1 (zwart als de achtergrond
# rechts/onder ligt, lijnrood links/boven) en oude buitenlijn die nu binnen ligt -> vruchttint (VUL, of automatisch: S aan de schaduwkant
# rechts/onder, M aan de lichtkant). Oogwit en pupil worden nooit gewijzigd (assert).
import sys; sys.path.insert(0,'sprite_r9'); import numpy as np; from PIL import Image; from gemeen2 import *; from hulp import *
K,L,S,M,H=1,2,3,4,5; W,G=10,11
DEL=[]; ADD=[]; VUL={}
# ---------- linkertros ----------
DEL+=[(6,25)]                         # bovenste vrucht: rand 6-6-7, inkeping (8,26)
ADD+=[(5,32),(5,33),(6,34)]           # vrucht rij 30-34 bolt uit: 7-6-5-5-6
ADD+=[(8,35),(8,36),(9,37),(10,38),(11,38)]   # vrucht rij 35-38 linksonder bolt uit: 8-8-9-10, onderkant x10-11
DEL+=[(13,37)]                        # inkeping tussen die vrucht en de puntvrucht (met (12,37),(12,38))
DEL+=[(19,29)]                        # rechterrand: inkeping tussen de L3-vrucht en de L4-vrucht (was rechte diagonaal 21-20-19-18)
ADD+=[(19,30),(19,31)]                # L4-vrucht bolt 1 px om het oog heen
DEL+=[(19,32)]                        # inkeping tussen L4- en L5-vrucht
ADD+=[(20,33),(20,34)]                # L5-vrucht bolt 1 px om het oog heen
VUL.update({(8,34):L,(6,32):H})       # (8,34) wordt naad tussen twee vruchten; bolling linksboven krijgt licht
# ---------- rechtertros ----------
ADD+=[(57,27),(58,29),(58,30),(57,31)]          # vrucht rij 27-31: 57-57-58-58-57 (was 56-57-57-57-56 + diagonaal)
ADD+=[(56,33),(55,34),(56,34),(54,35),(55,35),(52,36),(53,36)]   # vrucht rij 32-36 rechtsonder: 56-56-55-53 i.p.v. rechte diagonaal
VUL.update({(51,36):L})               # tros-punt / vrucht erboven: naad
ADD+=[(41,28),(42,29)]                # linkerrand: R1-vrucht bolt uit (41-42 i.p.v. 42-42-43)
DEL+=[(43,32)]                        # inkeping tussen kleine vrucht (rij 30-32) en de oogvrucht eronder
ADD+=[(43,31)]                        # kleine vrucht rij 30-32 bolt 1 px uit (44-43-44)
ADD+=[(42,33),(42,34),(43,35)]        # oogvrucht linksonder bolt 1 px om het oog heen
# ---------- middelste tros: rand tegen blad/stam (geen achtergrond) -> per vrucht een boog met lijnrood, inkeping = blad ----------
l,sg,m=6,7,8   # groen: lijn-/donker, schaduw, midden
GRENS={
 # bovenste vrucht (rij 12-15): top 26-27, dan 24-28, links 23-23; inkeping (28-29,12) naar het blad
 (25,12):m,(26,12):L,(27,12):L,(28,12):sg,(29,12):sg,(24,13):L,(28,13):L,(23,14):L,(30,12):L,
 # vrucht J (rij 16-18): inkeping op rij 15, bolling 21-21-22
 (21,15):l,(22,15):l,(21,16):L,(22,16):L,(23,16):H,(21,17):L,(22,17):H,(21,18):sg,(22,18):L,
 # vrucht C (rij 22-25): inkeping op rij 22 en 25, bolling 21-21
 (21,22):sg,(21,23):L,(22,23):H,(21,24):L,(21,25):sg,(22,25):L,
 # onderste vrucht (rij 26-30), linkerkant tegen de stam: lijnrood
 (25,26):L,(24,27):L,(24,28):L,(25,29):L,
}
h=9
GRENS.update({
 # linkertros bovenkant tegen het blad: bovenste vrucht top 8-9 (was vlak 7-10), vrucht ernaast top met lijnrood
 (7,22):h,(10,22):sg,(8,22):L,(9,22):L,(13,21):L,(14,21):L,(12,22):L,
 # rechtertros linksboven tegen het blad: vrucht P 46-45-45, inkeping, vrucht E 43-42 (was diagonaal 46-45-44-42-42-42)
 (44,24):sg,(42,25):sg,(46,22):L,(45,23):L,(45,24):L,(43,25):L,
 # rechtertros bovenkant: vruchttoppen met lijnrood
 (47,21):L,(52,21):L,(54,21):L,
})
DEL+=[(34,24)]                        # middelste tros rechts: inkeping tussen de M3-oogvrucht en de stam (rand was 34-34-34)
TROSBOX=[(4,20,23,42),(40,20,62,41),(16,8,38,30)]
ROOD=(1,2,3,4,5,10,11)
def bg(o,y,x): return not ok(y,x) or o[y,x]==0
def intros(x,y): return any(x0<=x<x1 and y0<=y<y1 for x0,y0,x1,y1 in TROSBOX)
def rand(o,x,y): return [(dy,dx) for dy,dx in N4 if bg(o,y+dy,x+dx)]
def trosrood(o,x,y):  # rode/oog-pixel van een tros (zwart dat alleen aan groen grenst telt niet)
    if o[y,x] not in ROOD or not intros(x,y): return False
    if o[y,x]==1 and not any(ok(y+dy,x+dx) and o[y+dy,x+dx] in (2,3,4,5,10,11) for dy,dx in N8): return False
    return True
def maak(src,uit):
    o=np.array(Image.open(src)).astype(int); o0=o.copy()
    oud_rand={(x,y) for y in range(64) for x in range(64) if trosrood(o,x,y) and rand(o,x,y)}
    for x,y in DEL: assert o[y,x] in (1,2,3,4,5),(x,y,o[y,x]); o[y,x]=0
    for x,y in ADD: assert o[y,x]==0,(x,y,o[y,x]); o[y,x]=K
    # oude rand die nu binnen ligt -> vruchttint
    for x,y in sorted(oud_rand):
        if o[y,x] in (W,G) or rand(o,x,y): continue
        if (x,y) in VUL: continue
        # richting waar de achtergrond lag: rechts/onder -> schaduw, anders midden
        nb=[(dy,dx) for dy,dx in N4 if (x+dx,y+dy) in ADD]
        o[y,x]=S if any(d in ((1,0),(0,1)) for d in nb) else M
    for x,y in ADD:   # 2 diep toegevoegd (niet aan de achtergrond)
        if not rand(o,x,y) and (x,y) not in VUL: o[y,x]=S
    for (x,y),v in VUL.items(): o[y,x]=v
    for (x,y),v in GRENS.items(): o[y,x]=v
    # lijnkleur zoals fase 1 op de hele trosrand
    LOG=[]
    for y in range(64):
        for x in range(64):
            if not trosrood(o,x,y) or o[y,x] in (W,G): continue
            nb=rand(o,x,y)
            if not nb: continue
            v=K if any(e in ((1,0),(0,1)) for e in nb) else L
            if o[y,x]!=v: LOG.append((x,y,int(o[y,x]),v)); o[y,x]=v
    assert ((o0==W)|(o0==G)).sum()==((o==W)|(o==G)).sum() and (o[(o0==W)|(o0==G)]==o0[(o0==W)|(o0==G)]).all(), 'oogwit gewijzigd'
    assert ((o>0)!=(o0>0)).sum()==len(DEL)+len(ADD)
    assert all(o0[y,x] in (2,3,4,5) for (x,y) in GRENS), [((x,y),o0[y,x]) for (x,y) in GRENS if o0[y,x] not in (2,3,4,5)]
    opslaan(o,uit)
    return o,o0,LOG
if __name__=='__main__':
    for v in ('a','b'):
        o,o0,LOG=maak('sprite_r9/guarana2_r9%s.png'%v,'sprite_r10/guarana2_r10%s.png'%v)
        print(v,'anders dan r9',int((o!=o0).sum()),'| silhouet',len(DEL)+len(ADD),'| lijnkleur',LOG)
    open('sprite_r10/normal.pal','w').write(open('sprite_r9/normal.pal').read())
