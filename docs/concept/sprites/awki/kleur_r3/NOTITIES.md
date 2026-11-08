# Awki – kleur ronde 3

**Bestanden:** `awki.png` (64×64, geïndexeerd), `normal.pal` (ongewijzigd t.o.v. r2), `raster.txt`, `vel.png` (r3 | r2 | model op 8×; close-ups kop+kuif en vleugel op 12× naast het model; vleugellijnen apart; 1×/2× licht en donker + model 1×).
**Keten:** `stappen/maak.sh`: `r2.txt` (= kleur_r2/raster.txt) → `e_rep3.txt` (handwerk, ed.py-formaat) → `r3.txt` = `raster.txt` → `awki.png`. `ed.py` gerepareerd (split op de eerste '='). Nieuw meetscript **`kw.py X0 Y0 X1 Y1 [raster]`**: per spritepixel de vier kwartvakken van het model (lb rb / lo ro) als paletletter, met de huidige letter ervoor; alle keuzes hieronder staan zo gemeten (notatie `kw` = die vier letters).

## 1. Gele veerpunten opgeheven vleugel
Gemeten per veer (F1 boven … F8 onder) met kw/fijn. Uitkomst: r2 lag op de meeste plekken al op de modelpixels; de echte afwijkingen waren de start van F1|F2, de onderrand van F3, de dikte van F5/F6 en ontbrekende okerbovenranden. Gerepareerd:
- **F1|F2:** de lijn begint nu in de kerf en loopt diagonaal: (7,9)1, (7,10)1 → (8,11) oker → (9,12) oker → (10,13) goud 9 → (10,14) oker → rood 6 (11,15) → … (r2: verticaal zwart (8,9–11)). Model: 2/1 op x7.5 rij 9.5–10, 5/8 op (8,11), 8 op (9.5,12.5) en (10,14).
- **F3|F4:** donkere onderrand F3 (5,20)1 (kw B4.3), (6,21)1, (7,21) bruin 2 (kw 8AB2); daarna de **okerbovenrand van F4** als één rij (5–8,22) → (9,23),(10,23) (model 8888 op rij 22.5–23); het zwarte pixel (7,22) is oker geworden, (8,23) geel.
- **F4:** punt linksonder (6,25) oker i.p.v. zwart (model C/B, licht); de onderlijn begint op (7,26).
- **F5|F6:** lijn een rij hoger, op het model (kw rij 30: 3/22222): (8–9,30)1, (10–11,30) bruin 2, (12–13,30) oker, (14–16,30) rood 6. F5 is daardoor niet meer te dik; **F6 krijgt een eigen okerbovenrand** (10–12,31) (model B9888) i.p.v. zwart.
- **F6:** onderste rij goudschaduw 9 (12–16,33) (model 9 op rij 33.5), oker (17,33) als overgang naar het oranje (model 888 op rij 33.5), (20,34) rood 6 (model 66).
- **F7|F8:** scheiding (17,35)9, (18,35)8 (model 9 88); onderrand F8 (18,37) zwart, (19,37) oker.
- Silhouet ongewijzigd (zie controle). De kerven tussen de vingers liggen in het silhouet vast; de veren kunnen daardoor niet langer of losser worden dan het masker toelaat.

## 2. Lijnen in het karmijn
Model per kwartvak gevolgd; de blokjes eruit, lijnen als doorlopende diagonalen:
- L1 (14,17)-(15,18)-(16,19)-(16,20) in 5, (15,19) karmijn (kw D5DD) → zuivere diagonaal i.p.v. trapje.
- L2 (13,21)6-(14,21)5-(15,22)5-(16,22)5, (15,21) karmijn.
- L3 (12,24)6-(13,24)6-(14,24)5-(15,25)2-(16,25)2-(17,25)5; het blok (15–17,26) 555 en (14,25) zijn karmijn (model D): de dikke streep van het model blijft, maar als taps lijntje.
- L4 rij 28: donkerrood x15–19 (model 555555555 x15–19; r2 x14–18), x13–14 rood 6 (kw DD97/DD77).
- L5: rij 30 x14–16 rood 6 en rij 31 x19–20 rood 6 (model 66666 rij 30.5, 666 rij 31).

## 3. Kuif
Silhouet ongewijzigd. Op de modelpixels:
- **Rode selout aan de lichtkant**: bovenrand (37–38,6),(36,7),(35,8),(34,9) karmijn D (model D66D/C6D6/D666), (33,9) oker als overgang naar de gouden voet (model B996). r2 had daar rood 6 en één donkerrode 5.
- **Lavendel**: donkere F-band x40–42 (model FFFF op (40–42,6),(41–42,7)); lichte E alleen in de punt rechtsboven.
- **Strepen**: oranje streep (33–36,10)-(36–37,9)-(37–38,8) (model 7777/6777/7776), karmijn schaduwstreep (38–39,10)-(40,9)-(41,8) en (40,11) (model DD77/DD66/66DD), tweede oranje streep (37–38,11)-(34–36,12), gouden voet met lichte strepen A (29,14),(32,14) (model 8AA9/89AA) en een oranje streepje (33,13) (model 7799). Punt (39,7) rood 6 (model 6676): de strepen lopen smaller uit naar de lavendel punt.
- Onderrand: zwart aan de schaduwkant (onveranderd, silhouet).

## 4. Kuifvoet / voorhoofd en rood vlakje
- De drie donkerrode 5-spikkels in het geel weg: lijn kuif|toef nu bruin 3 (27,15),(28,16) → oker (29,16) (model 125,86,61 / 133,69,21 / 175,115,60); (32,15) 4 (model 129,78,50). Toef verder geel A/9 als r2.
- Rood vlakje: links rood 6 (28,19),(28,20) (model 200,58,42), rechts karmijn D (29,19),(29,20) (model 140,58,36 / 140,34,30); rand naar de snavel bruin 3 (27,19),(27,20) (model 113,66,42 / 96,58,42).

## 5. Oog
Gemeten op halve pixels: model-oog x30.2–32.0, y18.8–20.6 (±2×2 px): glans linksboven, donkere pupil links-midden (94,73,64), tan iris rechts (169,139,94 / 168,139,100). Sprite: **2×2** = glans B (30,19), iris oker 8 (31,19),(31,20), pupil bruin 3 (30,20) (r2: zwart, viel weg in het masker). Masker eromheen ongewijzigd (= model).

## 6. Snavel tweetonig
Boven licht C als rugrand die naar de punt afloopt (24–25,20),(22–23,21) (model 143/127/154), onder 4 (26,20),(24–26,21) (model 93/108/98/91), onderrand 2 blijft. Geen neutraal middengrijs in het palet: 4 is iets bruiner dan het model (lum 105 vs 97). (22,21) is C i.p.v. model-donker, om geen los 1-px vlakje te maken.

## Controle
- Silhouet-diff **8** (alleen de gat-pixels (23–24, 23–26) uit r2). `rand.py` 0.
- `controle.py`: nieuwe kleine clusters zijn alleen lijnstukken/taps ((7,9–10), (7,21), (10–11,30), (10,13), (17,35), (14,24), (17,25), (8,11)-(9,12)), het rode vlakje (2+2 px) en de kuiflichtstreep (29,14)-(28,15). Geen losse tintvlakjes.
- `los1.py`: alleen lijnuiteinden en maskerrand (30,21).
- Toon (toon2, vlakpixels sprite/model): vleugel 130/136 (r2 131), kuif 132/140 (r2 133), kop 132/128, snavel 91/93 (r2 102).

## Open / ter info
- Reparatie 1: de grootste winst zit in F1|F2, F3|F4 en F5|F6; de rest van de vingers lag al op het model. Langer of losser dan nu kan alleen met een silhouetwijziging (niet toegestaan).
- Snavel-onderhelft in 4 is warmer dan het grijze model (geen vrije paletplek).
