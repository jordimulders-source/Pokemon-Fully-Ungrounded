# Kolibrie pre-evo – kleur r7 (maker)

Jordi koos oog S ("de eerste is het beste"; L afgekeurd: "geen idee wat voor monster je van de 3e gemaakt hebt") en vroeg om een eindkeuring met nadruk op de belijning. Uitgevoerd: alle reparaties R1–R9 uit `kleur_r6/EINDKEURING.md` op `kleur_r6/raster_S.txt` (alleen indexwissels). R7 (snavel (15,17),(15,20) `F`→`2`) is door Claude goedgekeurd: alleen kleur, vorm gelijk. Niet uitgevoerd: de punten onder "Voor Jordi" (snavelvulling, lila, pootjes, alpha-trapjes).

Bron: `reparaties.py` (R1–R9 als lijst met coördinaten) → `raster.txt` + `kolibrie_pre.png`; `palet.py`/`normal.pal` ongewijzigd t.o.v. r6; `controle.py`; `clusters.py`; `vel.py` → `vel.png` (r7 naast r6 S, Taillow, Starly; 4× en 1×, licht en donker).

## Controle (`python3 controle.py`)
- alpha-diff met r6 S: **0**.
- **36 px gewijzigd = precies de 36 px uit het rapport**; geen pixel buiten het rapport, geen rapportpixel zonder effect. Per pixel (oud→nieuw):
  - R1: (32,23) (34,24) (35,24) (38,26) `2`→`1`
  - R2: (26,14) `2`→`1`
  - R3: (43,37) (42,38) (43,38) (42,39) (43,39) (42,40) (43,40) (44,40) `2`→`3`
  - R4: (35,40) (32–35,41) (32–35,42) `2`→`3`
  - R5: (35,34) (35,35) (35,36) `A`→`8`
  - R6: (29,17) (29,18) `E`→`B`
  - R7: (15,17) (15,20) `F`→`2`
  - R8: (28,43) `D`→`C`, (28,44) `C`→`D`
  - R9: (32,30) (31,31) (31,32) (31,33) (32,34) `2`→`3`
- Open randen: 0. `F` wordt niet meer gebruikt (vrije paletplek).
- Losse pixels / clusters < 3 px: 4. (23,19) `7` en (23,20) `5` = glans en onderglans van het oog (bewust). **(32,30) en (32,34) `3`** = de lichte stukjes van de tapse vleugelrand uit R9. Ze zitten tussen `2`-randpixels en volgen de rand als lijn, maar zijn als tintvlak los.

## Eerlijke zwakke punten
1. Door R9 bestaat de vleugelvoorrand op rij 30–34 uit `2`/`3` door elkaar ((32,29) `2`, (32,30) `3`, (31,31–33) `3`, (32,34) `3`, (32,35) `2`). Volgens het rapport is dat bedoeld (taps selout), maar het script telt (32,30) en (32,34) als losse pixels. Op 4× leest de rand op het belichte stuk nu zachter; op 1× zie je de vleugel nog als plaat, maar minder gescheiden van de flank dan in r6.
2. Blijft (voor Jordi, niet uitgevoerd): de snavel leest op 1× als twee sprietjes; de sprite is fletser dan Taillow/Starly; de pootjes zijn twee oranje stipjes; trapjes in de omtrek (rug (37,25), kop linksboven, vleugelpunt onderaan) vragen een alpha-wijziging.

## Lessen
- Reparaties uit een keuring als lijst met coördinaten in een script zetten en het controlescript elke gewijzigde pixel laten terugmelden tegen die lijst. Dan is "precies het rapport, niets meer" in één run bewezen.
