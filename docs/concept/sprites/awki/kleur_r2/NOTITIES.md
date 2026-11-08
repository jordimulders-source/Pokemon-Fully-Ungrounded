# Awki – kleur ronde 2

**Bestanden:** `awki.png` (64×64, geïndexeerd, index 0 transparant), `normal.pal`, `raster.txt`, `vel.png` (r2 | r1 | model op 8×; close-ups kop+kuif en opgeheven vleugel op 12× naast het model; extra rij: alleen de vleugellijnen (1/2/5, rest vervaagd) naast het model, opgeheven en gevouwen vleugel op 12×; 1×/2× licht en donker + model 1×).
**Keten:** `stappen/maak.sh`: `r1.txt` (= kleur_r1/raster.txt) → masker-index D wordt omlijning 1 (`basis2.txt`) → `e_rep2.txt` (handwerk, ed.py-formaat) → `r2.txt` = `raster.txt` → `awki.png`. Nieuw meetscript `lijn.py` (per spritepixel het donkerste van de 4 halve modelvakken = waar de lijnen in het model liggen). Gereedschap verder als r1 (paden naar kleur_r2/normal.pal).

## Palet (wijzigingen t.o.v. r1)
- **D = karmijn (158,46,46)**, nieuw, gemeten mediaan van het rode vleugelvlak in het model (158,47,46). Plek vrijgemaakt door het masker (oude D 45,44,50) samen te voegen met omlijning 1.
- 5 donkerrood (112,38,38) = veerlijnen in karmijn (model lijnkern 110,40,40).
- 6 rood (196,72,46) iets lichter/oranjer (kuif model 197,66,46; staart roest).
- B wit (234,232,224) iets warmer/minder fel; C grijs (152,146,144) iets lichter/warmer (keelschaduw, snavel).
- E lavendel (206,194,250) en F (128,104,200) lichter (model E 204,190,250, F-zone 170,149,205).
- Geen aparte crèmeplek: de enige vrijgemaakte plek is naar het karmijn gegaan (Jordi: vleugellijnen het belangrijkst). Crème van de keel = C.

## Reparaties
**(Jordi) Vleugellijnen, eerst.** Opgeheven vleugel rij 15–33 opnieuw ingekleurd op `rgb.py`/`fijn.py`/`lijn.py`. Elke veer heeft nu één doorlopende scheidingslijn van de zwarte tiplijn naar de schouder, taps, per zone van kleur: in geel oker 8, in oranje rood 6, in karmijn donkerrood 5 (kern 2 in de dikke lijn).
- S1: (8,9–11) 1 → (9,12),(10,13),(10,14) 8 → (11,15),(12,16),(13,17) 6 → (14,17),(15,18),(15–16,19),(16,20) 5 (model fijn 8 op (9.5,12.5),(10,14); r op (11.5,15)–(13.5,17); 5 op (14,17)–(16.5,20)).
- S2: tiplijn (6,15)→(9,18) → (10–11,19),(12,20),(13,21) 6 → (14–15,21),(15–16,22) 5 (model 'rrr' x10–11 rij 19, 5 x14–16 rij 20.5–22.5).
- S3: tiplijn (6,21),(7,22) → (8–10,23) 8 → (11,23),(12,24) 6 → (13–14,24) 5, (14,25)5 (15–16,25)2 (17,25)5, (15–17,26) 5: de dikke donkere streep van het model (5222255 op rij 25).
- S4: tiplijn (7–11,26–27) → (12,28) 8 → (13,28) 6 → (14–18,28) 5 (model 5 x15–19 rij 27.5–28).
- S5: tiplijn (10–11,31) → (12–14,31) 8 → (15–16,30) 6 (model 6 x14–16.5 rij 30.5). S6: tiplijn (12–14,34) → (15,34),(16,33) 8 → (17,33) 6.
- Rand rood|bruine voorrand blijft een lijn 5 (16,16)→(19,19)→(19,25)→(20,26) zoals r1.
- **Gevouwen vleugel:** r1 lag al op het modelgemiddelde (gem.py: binnenrand 2, band rij 40–41, diagonaal (45,42)→(47,46) naar de donkere buitenrand, lichte pennen 3). Aangevuld: lijn A (42,37)–(42,38) in 2 (model x42.5 rij 37–38, sluit aan op de donkere rand) en lijn B (39,39) in 2 (model x39.5 rij 38.5–40, sluit aan op de band). Geen zwart in het vlak.

**(1) Gat vleugel/hals:** (23–24, 23–26) transparant, **silhouet-diff 8 px precies daar**. Bovenrand (22–27,22) = kin/ondersnavel 1-2-2-2-2-1 (model 39/65/68/62/59/47); links blijft de vleugelrand 1 (x22), rechts de keelrand 1 (x25), onder 1 (rij 27).
**(2) Keel:** modelvorm gemeten per pixel (rij 22–27): wit x28–31 direct onder het masker (r1 had daar 4 grijze C), crème/grijs C alleen op de modelplekken: kin (27,23),(26–27,24) (model 191,172,150 / 202,186,160 / 226,220,205), rechterrand (33,24),(32,25),(31,26), onderrand (26–28,27) (model 186/243/227); (26,23) bruin 3, (27,28) bruin 4. Toon keel 174 vs model 184. Smaller door het gat en schuin aflopend rechts.
**(3) Vleugelbanden:** het oude rood 6 in het vleugelmidden is karmijn D geworden; grens oranje|karmijn op de gemeten modelpixels: x13–14 in rij 16–23, x12–13 in rij 24–28, karmijn tot x22 in rij 28–31, x20–22 in rij 32–33. Oranje band x10–13, geel/oker daarbuiten. Toon vleugel 130 vs model 134 (r1 135/135, nu donkerder door het karmijn, zoals het model).
**(4) Kuifbasis/voorhoofd:** de losse spikkels vervangen door één donkerrode lijn (27,15)–(28,16)–(29,16) (model 5 op x27.5 rij 15.5–16, 5/D op x27.5–30 rij 16–16.5) tussen kuif en geel voorhoofdsrandje; voorhoofd rij 16–18 rustig A/9 met oker 8 tegen het oog ((29,18), model 180,141,64); (30–31,16) 9 i.p.v. 9/A-wisseling. Kuif: lengtestrepen 7 netjes op de modelplekken ((38,7),(37–39,10),(38,11) rood zoals het model), top (38,6) 6. Kuif niet dikker (geen vormwijziging).
**(5) Kuif/lavendel lichter:** via palet (6, E, F) en selout (32,10) 8. Toon kuif 128 vs 139 (r1 125); het resterende verschil zit in de randpixels waar Gemini een gloed heeft (toon.py: binnenvlak ±0, rand −4 tot −14). Lavendel 148 vs 147 (r1 123).
**(6) Masker/oog:** masker = omlijning 1 (oude D, 45,44,50, samengevoegd). Kleiner op de modelpixels: (34,20) oker 8 (model 127,103,47 = rand oorvlek), (29,21) bruin 3 (model 119,74,77), (31,17) 9 (model 222,192,71); bovenrand (32,17) 2. Proef met masker = bruin 2 (gemeten toon 47 ligt dichter bij 2) liet het masker op 8× wegvallen in de kop; zwart leest als het model. Oog ongewijzigd: glans B (30,19), iris 8 (31,19–20); de pupil valt nu samen met het masker (model: pupil 33 vs masker 47, op 1× niet te zien).
**(7) Staart:** alleen tint via palet 6 (oranjer). Toon staart 81 vs model 82 (r1 79/84).

## Controle
- `controle.py`: px 1388, **silhouet-diff 8** (alleen het gat). Kleine clusters alleen bestaande lijnuiteinden (tiplijnen (6,21)/(7,22), (8,30), (10–11,31), (19,38), kin (28,21)/(27,22), poten). Geen losse tintvlakjes.
- `rand.py` 0. `los1.py`: alleen lijnuiteinden (veernaden, pupil/oog, kinlijn, buiklijn).
- Toon (toon2, vlakpixels): vleugel 130/134, kop 126/128, keel 174/184, buik 116/116, gevouwen vleugel 81/83, poten 85/81, staart 81/82, kuif 128/139, lavendel 148/147.

## Open / ter info
- Geen eigen crèmetint in de keel (paletplek naar karmijn); C is een compromis tussen snavelgrijs en keelcrème.
- Kuif blijft iets donkerder dan het model door de omlijning waar Gemini gloed heeft.
- Snavel (2 px dik, alles C) en het rode vlakje zijn niet aangeraakt (niet in de opdracht); het model heeft een tweetonige snavel (boven ±145, onder ±95).
