# Uku Pacha – eindkeuring (Dragonfly Cave)

Start: `../r7/uku_pacha_r7A.png`. Resultaat: `uku_pacha_e.png` (64×64, geïndexeerd, index 0 transparant, 16 kleuren).
Opnieuw maken: `python3 e1_bewerk.py && python3 e2_maak.py && python3 vel.py` (rasters `raster_r7A.txt` → `raster_e1.txt` → `raster_e.txt`).
Hulpscripts: `lib.py`, `zoom.py`, `lum.py`, `dekking.py` (eerdere poging), `clusters.py` (tintvlakjes < 3 px).
Vel: `vel.png` (eind | r7A | model op 8×; close-ups 12× geestvlam, rechtervleugel, linkerkop, rechterkop, kronkels; 1×/2× licht en donker; naast Arbok, Seviper, Gyarados, Milotic, Rayquaza `_gba`).

152 pixels anders dan r7A. Elke ingreep staat met reden in `e1_bewerk.py`/`e2_maak.py`.

## 1. Rechte lijnen (Jordi: "geestvlam naast de staart, de rechtervleugel, het hoofd van links")
Randen gemeten tegen de modeldekking per pixel (`dekking.py`); alleen pixels met modeldekking toegevoegd/weggehaald.
- **Geestvlam**: bovenste sliert was een rechte rij van 8 `l` (r24); nu een boog met randlopen 1,1,1,2,3,2,1 en een lichte kern in de sliert. Middelste sliert boven de vleugelpunt: bult (model 40 % op r30) en een trapsgewijze onderrand i.p.v. 5 recht (r32). Bij de staart: dubbele `l`-band (r42+r43) → 1 px rand, kern p/w uit het model.
- **Rechtervleugel**: bovenrand 8 recht → polsbult (model) en dan aflopend naar de punt (lopen 2,5,4). Vleugelpunt houdt een zwarte rand aan de geestkant (schaduwkant, vleugel ligt ervóór).
- **Linkerkop**: hoek schedel/45°-schuine → bolle boog (randlopen 1,1,0,1,1,1,2,4,8), snuit rond.
- **Elders**: lijn tussen onderste kronkel en middenkronkel (9 recht, r60) → doorhangende boog zoals in het model.

Alpha-wijzigingen (14): erbij (12,9) (13,9) (1,17) [kop]; (56,18) (57,22) (54,23) (55,23) (56,23) (56,30) (57,30) (57,33) [geest]; weg (7,10) [kop], (43,30) [vleugel], (61,32) [geest].

## 2. Belijning
- Buitenlijn: gekleurd aan de lichtkant (kop/vleugel `D`, hals/kronkel `n`, geest `l`), zwart vanaf linksmidden via onder naar rechts. Nieuw: bovenrand linkerkronkel zwart → `n` (9 px).
- Binnenlijnen: zwart → eigen donkerste tint (`n` lijf, `D` vleugel), behalve waar de lijn aan de schaduwtint `d` grenst (DC: zwart alleen als diepste schaduw). Een eerste versie met álle binnenlijnen in `n` werd zichtbaar wazig (Jordi's "blurry"); daarom die uitzondering. Gezichten (ogen, mond, tong, tanden) niet aangeraakt.
- Alle bestaande lijnen blijven; alleen tint en loop.

## 3. Schaduw
Licht linksboven klopt per onderdeel (koppen h → B → D, hals b → d rechts, kronkels lichtrand onder zoals het model). Tintvlakjes < 3 px gecontroleerd: één los `m`-pixel (25,47) naar het vlak eronder; de rest zijn lijnen, ogen of overgangen die het model per pixel steunt. Geen vlakken gladgestreken.

## 4. Tinten
Lichaamsladder had te kleine stappen (n-d-s-m: 28/23/27, "grijze brei"-risico). Nieuw: n (32,44,70), d (60,72,98), s (84,104,136), m (114,138,168) → stappen 28/29/37, schaduwkant iets blauwer. Overige tinten ongewijzigd. 16 kleuren incl. transparant.

## 5. Niet aangeraakt (gecontroleerd in `e2_maak.py`)
Linkeroog (10,16–17) zwart naast wit (11,16–17); rechterpupil (39,5) zwart tussen koptint (38,5) en geel (40,5). Tongvork, mondlijn en lichtere streep rechterkop, borstplaten ongewijzigd.

## Ter info voor Jordi (geen wijziging gedaan)
- De onderste rand (r60 x10–19 en r63) is lang recht, maar volgt het model (kronkel ligt op de grond).
- Lijn r48 x32–38 in de rechterkronkel is in het model ook vrijwel vlak; laten staan.
