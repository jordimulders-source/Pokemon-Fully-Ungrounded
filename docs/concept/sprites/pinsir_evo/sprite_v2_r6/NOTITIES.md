# Pinsir-evolutie v2, frontsprite r6 (23 nov)

r6 = r5 met twee reparaties: (1) het palet naar de modeltinten, (2) de banding in rug B eruit. Alles daarbuiten is pixelgelijk aan r5 (`bouw.py` controleert dat), op 5 px in de verre scheen na (zie onder).
Bouwen vanuit `docs/concept/sprites/pinsir_evo/`:
`python3 sprite_v2_r6/bouw.py && python3 sprite_v2_r6/vellen.py` (de meting in `helderheid.md` komt uit `vlakken.py`).

## 1. Palet (`palet.py`)
De tinten zijn per kleurgroep in het model gemeten (`natief_ruw`, mediaan per helderheidsband):
- bruin: L52 (63,48,36), L95 (111,91,69), L125 (146,120,94), L148 (166,143,118);
- room: (192,173,136), (227,212,178), (245,234,192);
- rood: (86,36,35), (104,45,42), (160,92,77);
- oog: (244,232,179);
- lijn: (44,30,21).

Wat er per kleurgroep verandert:
- **Bruin.**
  - De tint volgt nu de modelkleur per helderheid; tussen de ankers wordt geïnterpoleerd. De donkere tinten van r5 waren roder dan het model: index 3 (88,66,48) en index 2 (46,32,22).
  - Niveaus 3/4/5/14 = L 68/101/133/166, dus stappen van 33/32/33. De niveaus zijn zo gekozen dat de helderheid per vlak klopt (zie onder). Stappen van 35–50 zouden de lichte vlakken 8–10 boven het model brengen: dat botst met het doel van ±5.
  - Lijnbruin 2 = L50, het donkerste modelbruin. De donkerste vultint (3) ligt daar 18 boven.
  - Buitenlijn 1 = (30,21,15). Dat is iets donkerder dan de modellijn (44,30,21), zodat 1 de donkerste kleur blijft.
- **Room:** van het model overgenomen; 8 is iets warmer.
- **Rood:** minder verzadigd, zoals het model. 11 ging van (150,66,56) naar (140,74,63), 12 van (172,98,82) naar (164,98,82), en 9 en 10 zijn lichter.
- **Oog:** naar het model (244,232,170).
- De verdeling van licht en schaduw (welke index waar staat) is die van r5.

Helderheid per vlak, sprite tegen model, zonder lijnpixels (`helderheid.md`):
- Binnen ±5: kopschild, koepel, nabije arm, rug, staart, nabije dij, nabije scheen, buik en kaken.
- Gezicht −7: het gezicht van r4 is pixelgelijk gehouden.
- Verre zijde −8 tot −11 (verre arm, verre dij, verre scheen). Bewust: in r5 is het verre been "een stap donkerder" gemaakt.
- De verre scheen stond op −16. Het midden (5 px: (20–21,55–56) en (19–20,57)) ging van 3 naar 4, en nu staat hij op −11.

## 2. Rug B zonder banding
- In r5 lag onder elke naad een lichte rij en erboven een donkere. Dat gaf evenwijdige strepen langs de rugrand.
- **Rugzone.** De rug van r4 B, met uitzondering van:
  - de koepel en de arm (r5-zones + 1 px);
  - de stekels en de rugrand (alles binnen 2 px van transparant);
  - de heup en de dij.
- **Naden.** De naden (1/2) blijven op hun modelplek, er is geen lijnpixel veranderd. Alleen de vultinten 3/4/5/14 zijn opnieuw verdeeld.
- **Platen.** De platen zijn de vlakken tussen de naden: 3 stuks, van 90, 58 en 25 px. Alleen voor het indelen zijn de twee lange naden 2–3 px doorgetrokken tot de rand van de zone.
- **Per plaat een bolle vorm, zoals Aggron en Tyranitar hun platen opbouwen:**
  - de positie in de plaat telt 85 % langs de plaat (linksboven → rechtsonder) en 15 % dwars erop;
  - het eerste 28 % wordt een licht vlak 5, met 2–3 px hooglicht 14 in de linkerbovenhoek;
  - het laatste 28 % wordt schaduw 3, het midden 4;
  - het licht is dus een vlak aan het begin van de plaat, geen streep langs de naad.
- In totaal 94 px veranderd.
- **Niet aangeraakt:** de randstrook direct onder de rugstekels (stekelflanken met licht/donker, ±15 px). Daar staat nog een korte lichte rij, maar die hoort bij de stekelflanken.

## Zelf gekeken op 1×/2× naast Tyranitar/Aggron/Pinsir
- Beter dan r5: de rug leest als 3 grote platen zonder strepen, de hele sprite is iets lichter en minder rood, en de kaken zijn minder fel.
- **Nog over, niet gerepareerd:**
  - De nabije arm is op 1× nog minder duidelijk dan in het model. Het lijf eromheen heeft dezelfde tinten.
  - De gezichtsvlakken zijn 7 donkerder dan het model. Het gezicht van r4 is bewust gehouden.
  - De verre zijde is 8–11 donkerder dan het model, zoals in r5 gevraagd.
- Er is geen keurder gebruikt.

## Bestanden
- `pinsir_evo_v2_r6.png`: de sprite. Geïndexeerd, index 0 transparant, 15 kleuren.
- `bouw.py` en `palet.py`.
- `vlakken.py` en `helderheid.md`: de meting per vlak.
- `onderdelen.png`: rug, hoofd, armen en benen op 12×, telkens r6 | r5 | model.
- `vel.png`: r6 | r5 | model op 6×, daaronder 1× en 2× naast Tyranitar, Aggron en Pinsir, op wit en op donker.
