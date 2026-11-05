# Kolibrie pre-evo – kleur r10 (maker)

Jordi (letterlijk): "maak de vorm van hals naar buik zoals in deze foto, dus eerst licht inkepend en dan bolle buik. De buik zelf is goed, pootjes zijn ook goed". Foto: `referenties/jordi_8_moeder_hals_buik.png`.

Bron: `bouw.py` = `kleur_r9/raster.txt` + 5 rijstukken in de zone hals→borst (x16–21, y24–28) → `raster.txt` + `kolibrie_pre.png`. Palet ongewijzigd. `controle.py`, `vel.py` → `vel.png` (r10 op 4× en 1× licht/donker naast r9 en de foto, gespiegeld zodat hij ook naar links kijkt).

## Wat er veranderde
- Linkerrand (eerste pixel per rij), r9 → r10: rij 24 16→17, rij 25 16→18, rij 26 17→19, rij 27 17→19, rij 28 17→18; daarna de bestaande buik (18,18,18,19,19,19,20,20,21,21,22…).
- De keel loopt nu vanaf de kin (x16, rij 22–23) in een zachte holle curve 1 px dieper naar binnen dan de buik (17,18,19,19) en buigt dan vloeiend terug naar de bolle buik (18 op rij 28–31). Er zit geen knik in: de stappen zijn 0,1,1,1,0,−1,0,0,0,1.
- Belijning: lichtkant, dus overal `2` (selout), geen zwart erbij en geen wisselende 1/2.
- Licht/schaduw: in de holte onder de kin een tapse schaduw `5` (19–20,25), (20,26), (20,27) (4 px, één cluster), die op rij 28 overgaat in het witte buikvlak.

## Controle (`python3 controle.py`)
- 17 px gewijzigd, **0 buiten de zone**. Alpha-diff met r9: 8 px, alle in de zone. Totaal 606 px (r9: 614).
- Buik, pootjes, snavel, oog en de rest: pixel voor pixel r9.
- Open randen: 0. Losse pixels/clusters < 3 px: alleen de al goedgekeurde (oogglans, onderglans, tapse vleugelrand (32,30) en (32,34)).

## Eerlijke zwakke punten
- De inkeping is 1 px diep ten opzichte van de buik. Op 4× zie je hem duidelijk, op 1× als een smallere hals. Dieper (2 px) zou de kop meer losmaken van het lijf, dus dat heb ik niet gedaan.
- Het lijf is aan de linkerkant 8 px kleiner geworden; de kop leest daardoor iets groter.
