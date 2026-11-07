# Poedelmot: kleur r7 (maker, zuinig)

Maatstaven (Jordi): heel accuraat op het model, en een nette Gen 3-sprite volgens SPRITE_KERN. Gebouwd vanaf r6 (r6 ongewijzigd).

Bestanden: `raster.txt`, `poedelmot.png`, `normal.pal`, `palet.py`, `vel.py`/`vel.png` (r7 | r6 | bron 8× en close-ups), `controle.py` met `controle_uitvoer.txt`, `stappen/bouw7.sh`. Nieuwe laag: `k_r7.py`.

## Gedaan
- **Vleugels (voor en achter)**:
  - De tan vlakken staan nu op de plek en in de grootte van het model. Per pixel is de helderheid van `silhouet/gids_gemiddeld.png` (het verkleinde model) omgezet naar de vleugeltinten `A`/`9`/`7`/`6`/`5`. Dat is een script, daarna opgeschoond.
  - Een brede witte buitenrand (2 px binnen de rechterrand) op beide vleugels.
  - Langs de kop een dunne witte lijn (het witte randje van de vleugelvoet uit het model), met de voetlijn `4` ernaast.
- **Vleugelvoetlijn**: schuiner, van (36,30) naar (42,47), zoals in het model. Kop, vleugels en onderkant zijn hierop aangepast.
- **Buik/middenstuk** (x28–42, y44–56): lichter, volgens het model, een tint lichter gezet dan de gids aangeeft.
- **Sprietribben**: ongelijke afstand (2–3–2–3), één tint per rib.

## Controle
- Alpha-diff 0. Open randen 0 (uitzonderingen: klauwtjes, sprietpunt).
- Selout zonder afwisseling. Losse pixels 0, clusters < 3 px 0.
- Donker-aandeel 0,222.

## Eerlijke zwakke punten (naast het model op 8×)
- **Krulmotieven**: de golvende tan "wolkjes"-lijnen van het model staan er niet als lijnen. De gids is een gemiddelde per pixel, waardoor de krullen samensmelten tot vlekkerige tan vlakken. De plek en grootte kloppen, de krulvorm niet. Hiervoor is handwerk per krul op de model-close-up nodig (geen gids).
- **Buik**: nog een samenhangend tan vlak, minder losse plaatjes dan in het model.
- **Sprietribben**: lezen op 8× nog licht als raster.
- **Pluimen**: alleen de bovenkant is rond; de onderkant volgt het silhouet.
