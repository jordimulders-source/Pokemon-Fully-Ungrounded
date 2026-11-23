# Eindkeuring Gnometrotter Grass r16 (23 nov)

Gekeurd: `../sprite_r16/gnometrotter_grass.png`. Model: `../hybride/model_hybride.png`.
Opdracht (Jordi): "daarna mag die naar de eindkeuirng, goed kijken naar lijnen, kleuren, tinten, dragonflycave etc" (bij Ice: "streng maar geen onnodige fixes").
Maatstaf: Rock af, Ice af (eindkeuring `../../gnometrotter_ice/eindkeuring_r9/`), Gnomad/Gnomini, Gen 3 Shiftry/Nuzleaf/Sewaddle/Tropius.
Niet beoordeeld (bevroren): silhouet, romp met 2 naden, benen, neus/rechterschouder/linkerhand (= Rock), bladverdeling van de muts, neusboog in roze 6.

## Oordeel: BIJNA – 11 pixelreparaties (alleen lijnkleur), daarna PASS

Blind (1× en 8×, licht en donker): leest als houten kabouter met bladmuts en bladbaard; volume in muts, baard, romp, broek en schoenen; geen storing op 1×. Alle fouten zitten in de buitenlijn aan de lichte (linker) kant: zwart waar Rock af en Ice af de eigen donkerste tint hebben. Dit zijn exact de plekken die ook bij Ice gerepareerd zijn.

## Reparaties (x,y: oud → nieuw index)
| pixel | oud → nieuw | reden |
|---|---|---|
| (15,26) | 1 → 5 | linkerrand bladbaard gaat 5-5-1-1 (lichte kant); Rock af heeft hier de eigen selout (4), Ice na keuring ook |
| (16,27) | 1 → 5 | idem |
| (5,37) | 1 → 2 | linker (lichte) rand van de stok onder de vuist zwart, rest van die rand is 2; Rock af: 2 op de stoktop links |
| (17,37) | 1 → 2 | linkerrand houtriem zwart op de lichte kant en 1-2-1 om en om met (17,36); Rock af: 2 op (17,36)–(18,39), zwart pas vanaf (18,40) |
| (18,38) | 1 → 2 | idem |
| (18,39) | 1 → 2 | idem |
| (18,47) | 1 → 9 | linkerrand broek 9-1-1-9 (om en om); Rock af: 9 |
| (19,48) | 1 → 9 | idem |
| (39,49) | 1 → 9 | lichte binnenkant rechterbeen zwart; Rock af: 9 |
| (40,50) | 1 → 9 | idem |
| (41,51) | 1 → 9 | idem |

`raster.png`: links r16 met de 11 pixels rood omkaderd, rechts het resultaat (proef, niet in de repo). `vel.png`: model | Grass r16 8× | Rock af 8× | Ice af 8×.

## Metingen
**Lijnen** (`../../gnometrotter_rock/sprite_r9/meet.py`, zwart op de buitenrand):

| | boven | links | rechts | onder |
|---|---|---|---|---|
| Grass r16 | 24 % | 32 % | 90 % | 94 % |
| Grass na reparaties | 24 % | 23 % | 90 % | 89 % |
| Rock af | 26 % | 26 % | 90 % | 89 % |
| Ice af | 23 % | 25 % | 90 % | 90 % |

- Buitenrand alleen 1, 2, 5, 6, 9 (eigen donkerste tint per groep): geen lichte tint op de rand. Open randen: 0. Lijndikte 1 px.
- Om-en-om-script (enkel lijnpixel tussen twee van een andere lijnkleur op de rand): r16 1 geval (17,36), na reparaties 0 (Rock af 0, Ice af 0).
- Zwart links/boven verder alleen waar Rock het ook heeft: mutsrand rechtsboven, haarplukje (12–14,17–19), vuist, riemhoek (18,40)/(19,41), kruis (31,48)/(38,48), schoenen, gat in de muts. Takje (55,20): onderkant, mag.
- Binnenzwart 11 px (Rock 41, Ice 21), alleen vorm over vorm (vuist, stok, hand).

**Kleurtinten** (helderheid)
| groep | tinten | stappen |
|---|---|---|
| blad | 14 194 / 13 158 / 12 104 / 5 61 (lijn + diepste schaduw) | 36 / 54 / 43 |
| hout | 4 124 / 3 88 / 2 55 (lijn + diepste schaduw) | 36 / 33 |
| roze (gelijk aan Rock) | 15 206 / 8 183 / 7 139 / 6 105 | |
| broek (gelijk aan Rock) | 11 173 / 10 134 / 9 97 | |

- Elke vorm ≥ 3 tinten (hout en broek: 2 vultinten + lijntint die ook schaduw is, net als de broek bij Rock/Ice; Shiftry-hout 71/115/149 is vergelijkbaar).
- Bladstap 13→12 is 54, iets groter dan Shiftry (116→161 = 45) en Sewaddle (45/40); Ice af had 47. Leest goed, geen fout; geen paletwijziging nodig.
- Tintvlekjes < 3 px (zonder lijnkleuren): Grass 5,2 %, Rock af 5,0 %, Ice af 4,6 %. De meeste zitten in de stam/takjes (hout 3/4) en de bladpunten; gelijk aan de maatstaf.
- Geen banding buiten wat Rock ook doet: stam als staande cilinder 2|4|2|3|3|1, zoals rots en stok bij Rock (goedgekeurd). Riem: 4 boven, 3 midden, 2 onder (ring van bovenaf belicht).

**Schaduw**: één lichtbron linksboven: muts E/D links → C → 5 rechts, haar- en baardbladeren licht links/boven, stam licht links, riem licht boven, romp/broek/handen als Rock af. Geen pillow shading. Groot mutsblad heeft een middenvlak C met lichte rand en nerven in 5: past bij Gen 3-bladeren (Tropius) en de vorm is bevroren ("het grote blad klopt").

## Niet als fout gemeld (gemeten, klopt met de maatstaf of te klein)
- Zwart in het gat van de muts ((39,11), (41,12), (38,13), (39,15)): Rock af heeft daar ook zwart ((39,10), (37,12), (38,14)).
- Rechterrand muts 5-5-5-1: diepste bladtint als schaduwsikkel vóór het zwart, zoals 2 bij hout.
- Bladstap 54 (zie boven).
