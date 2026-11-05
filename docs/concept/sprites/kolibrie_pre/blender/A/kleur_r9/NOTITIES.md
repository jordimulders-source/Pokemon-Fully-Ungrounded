# Kolibrie pre-evo – kleur r9 (maker)

Jordi (letterlijk): "het moeten wel echt kleine pootjes zijn he" · "waar je nu mee bezig bent is prima alleen er moet iets meer een hoek in, ze kunnen niet zomaar naast elkaar".
Uitgevoerd: precies de reparaties uit `kleur_r8/KEURING.md` §4 (FAIL 1 linker buik, FAIL 2 pootjes) plus het optionele (40,29) en (40,30) `A`→`8`. Niets anders.

Bron: `reparaties.py` (rapportlijst; `0` = transparant) op `kleur_r8/raster.txt` → `raster.txt` + `kolibrie_pre.png`; palet ongewijzigd; `controle.py`; `vel.py` → `vel.png` (alleen sprites: r9 op 4× en 1× licht/donker naast r8, Taillow, Starly).

## Controle (`python3 controle.py`)
- 44 px gewijzigd, alle in het rapport (buik 19, verre poot 7, nabije poot 7, leeg 8, optioneel 2). Niet in het rapport: geen. Eén rapportpixel had geen effect: (27,45) stond in r8 al op `1`. De volledige lijst oud→nieuw staat in de uitvoer van het script.
- Totaal 614 px, gelijk aan het getal van de keurder; de onderkant is identiek aan het schema in het rapport.
- Open randen: 0. Losse pixels: alleen de al goedgekeurde (oogglans (23,19), onderglans (23,20), tapse vleugelrand (32,30) en (32,34)).

## Eerlijke zwakke punten
- Op 1× zijn de pootjes nu een oranje stipje met een donker stipje erachter; de tenen zie je pas op 4×.
- De borst links is 1–2 px voller geworden (bewust, voor de bolle boog).
- Ongewijzigd: de snavel (niet gekeurd, Jordi), de zachte contrasten van mild lila.
