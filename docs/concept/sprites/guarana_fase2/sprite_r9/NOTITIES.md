# Guaraná fase 2, ronde 9: buitenomlijning van de trossen (op r8a én r8b)

Jordi (letterlijk): "hij is nog wat blurry maar dat zit puur in de omlijning van de fruittrossen, de vormen lijken van een afstandje afgekapt,
alsof het rechte lijnen zijn ipv rondere vruchten".

Bestanden: `guarana2_r9a.png`, `guarana2_r9b.png`, `normal.pal` (= r8), `voor_jordi_r9_8x.png` (r9a | r9b | r8a, 8×, wit).
Bouwen vanuit `guarana_fase2/`: `python3 sprite_r9/bouw9.py && python3 sprite_r9/vel9.py`. Meten: `recht.py SPRITE` (rechte randstukken ≥ 3 px),
`grid.py`, `raster.py`. Beide varianten krijgen exact dezelfde 31 px wijziging (a en b verschillen alleen in de pupillen van L2/R2, zoals r8).

## Silhouet (benoemd, alle binnen 1 px van de trosrand)
Inkepingen (randpixel weg) waar twee vruchten elkaar raken:
- (7,26) linkertros links: tussen bovenste vrucht (rand x6, rij 23–25) en de vrucht met het L1-oog (rand x7, rij 27–28);
- (7,29) linkertros links: tussen de L1-vrucht en de vrucht eronder;
- (12,37) linkertros onder: tussen de onderste linkervrucht en de puntvrucht;
- (56,26) rechtertros rechts: waar de naad (rij 26, x54–56) de rand raakt;
- (52,36) rechtertros rechtsonder: tussen de twee onderste vruchten.
Bollingen (achtergrond erbij):
- (57,28)(57,29)(57,30) rechtertros rechts: die vrucht was een rechte rand op x56 over 7 rijen, nu boogje 56-57-57-57-56;
- (55,33)(54,34) rechtertros rechtsonder: rechte diagonaal (1 px per rij over 7 rijen) wordt een boogje.
Oude buitenlijn die nu binnen ligt → schaduwsikkel: (56,28–30), (54,33), (53,34).
Linkerrand linkertros is nu x6-6-6 | 8 | 7-7 | 8 | 7-6-6-6 (rij 23–33): per vrucht een boogje met een inkeping ertussen.
Middelste tros: niet aan het silhouet gekomen (grenst bijna overal aan blad en stam).

## Lijnkleur (zoals fase 1)
Elke trospixel aan de achtergrond is buitenlijn: zwart als de achtergrond rechts/onder ligt, lijnrood als hij links/boven ligt.
Herzien (16 px): lijnrood aan de schaduwkant → zwart (o.a. rechterrand linkertros (18,30)(18,31), (17,37), rechtertros (55,26)(57,23),
middelste tros rechts (34,16)(35,22)(34,23)); **oogwit op de buitenrand → zwart** (L5: (19,35)(18,36), lag al zo in r5–r8, gaf een open
witte rand); vultint op de rand → lijn ((7,25), (12,36), (51,36), (52,35)).
Geen vul-, glans- of oogwittint meer op de buitenlijn van de trossen.

## Wat nog afwijkt
- Rechte randstukken ≥ 3 px in de trossen: 8 → 7 (`recht.py`), maar alle overgebleven zijn de bolling van één vrucht (3 px, boogje 1-3-1),
  geen stuk over twee vruchten meer.
- De wijziging is bescheiden (31 px). Wil Jordi een duidelijker geschulpte rand (druiventros), dan kan per vrucht nog een tweede pixel
  naar buiten, maar dat raakt de ogen aan de rand (L1, L5, R6) en de lijn wordt dan 2 px tegen het oog.
- Niet keurder-getoetst.
