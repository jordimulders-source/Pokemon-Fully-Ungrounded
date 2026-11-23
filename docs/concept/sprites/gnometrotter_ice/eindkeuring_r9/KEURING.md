# Eindkeuring Gnometrotter Ice r9 (23 nov)

Gekeurd: `../sprite_r9/gnometrotter_ice.png`. Model: `../r3/gemini_r3_lijf.png`.
Opdracht (Jordi): "ijs moet eindkeuring qua dragonflycave, kleurtinten, schaduw, lijnen, streng maar geen onnodige fixes".
Maatstaf: Rock af (`../../gnometrotter_rock/af/`, keuring r15 PASS), Gnomad, Gen 3 Regice/Glalie/Avalugg. Niet beoordeeld (bevroren/vorm): silhouet, neus (Jordi: naar Rock kopiëren), muts/rugijs-grens, haar, ijsfacetten.

## Oordeel: BIJNA – 13 pixelreparaties (alleen lijnkleur), daarna PASS

Blind (1× en 8×, licht en donker): leest als ijskabouter, volume in muts, baard, lijf, broek en schoenen; geen storing op 1×. Alle fouten zitten in de buitenlijn: lichte tint op de rand en zwart op de lichte (linker) kant waar Rock af de eigen lijntint heeft.

## Reparaties (x,y: oud → nieuw index)
| pixel | oud → nieuw | reden |
|---|---|---|
| (22,6) | 3 → 2 | lichte tint op de buitenrand van de muts (DC: nooit lichter aan de buitenkant); Rock af heeft hier 2 |
| (19,11) | 3 → 2 | idem, mutsrand links |
| (51,16) | 3 → 2 | lichte tint op de bovenrand van de ijspiek; lijn wordt 2-2-2 zoals (52,15) en (50,17) |
| (15,26) | 1 → 2 | linkerbaardrand gaat 2-2-1-1-2 (zwart/donker om en om, lichte kant); Rock af: eigen lijntint |
| (16,27) | 1 → 2 | idem |
| (17,37) | 1 → 2 | linkerrand baardpegel/riem zwart op de lichte kant; Rock af heeft 2 op (17,37)–(18,39), zwart pas vanaf (18,40) |
| (18,38) | 1 → 2 | idem |
| (18,39) | 1 → 2 | idem |
| (18,47) | 1 → 9 | linkerrand broek 9-1-1-9 (om en om); Rock af: 9 |
| (19,48) | 1 → 9 | idem |
| (39,49) | 1 → 9 | linker (lichte) binnenkant rechterbeen zwart; Rock af: 9 |
| (40,50) | 1 → 9 | idem |
| (41,51) | 1 → 9 | idem, nu ook geen 1-9-2 meer naar de schoen |

`raster.png`: links r9 met de 13 pixels rood omkaderd, rechts het resultaat (proef, niet in de repo gezet). `vel.png`: model | Ice r9 8× | Rock af 8×.

## Metingen
**Lijnen** (`../../gnometrotter_rock/sprite_r9/meet.py`, zwart op de buitenrand):

| | boven | links | rechts | onder |
|---|---|---|---|---|
| Ice r9 | 23 % | 34 % | 90 % | 96 % |
| Ice na reparaties | 23 % | 25 % | 90 % | 90 % |
| Rock af | 26 % | 24 % | 90 % | 89 % |
| Gnomad | 17 % | 24 % | 80 % | 83 % |

- Buitenrand na reparaties alleen 1, 2, 6, 9 (eigen donkerste tint per groep); in r9 3× tint 3 op de rand. Om-en-om-script (enkel lijnpixel tussen twee van een andere lijnkleur): r9 5 gevallen, na reparaties 0 op de lichte kant (Rock af: 0). Open randen: 0. Lijndikte 1 px.
- Zwart boven/links verder alleen waar Rock het ook heeft: mutsrand rechtsboven (40–43,4–7), plukje (12–14,17–19), neus (bevroren), vuist (2–3,33–36), riemhoek (18,40)/(19,41), handen, schoenzolen.
- Binnenzwart 21 px (Rock 37), alleen vorm over vorm (neus, vuist, kruis, broekzoom).

**Kleurtinten**
| groep | tinten (helderheid) | lijn |
|---|---|---|
| muts, rugijs, stok | 5 235 / 4 200 / 3 153 | 2 85 |
| baard, haar, riem, zolen | E 248 / D 225 / C 188 | 2 85 |
| roze (gelijk aan Rock) | F 206 / 8 183 / 7 139 | 6 105 |
| broek (gelijk aan Rock) | C 205 / B 173 / A 134 | 9 97 |

- Elke vorm ≥ 3 tinten. Stap E→D is 23 en 4→3 is 47, maar dat is Gen 3-ijs (Glalie wit 239/248, Regice 248/219/191/158): geen fout.
- Tintvlekjes < 3 px (zonder lijnkleuren 1/2/6/9): Ice 4,7 %, Rock af 4,8 %. Geen banding buiten wat Rock ook doet (stok en rugijs als staande cilinder 2|5|4|3|1, zoals rots en stok bij Rock).

**Schaduw**: één lichtbron linksboven: muts 5 links → 3 rechts, baard E/D links → C rechts, schoenen E → C, lijf/broek/handen gelijk aan Rock af; rugijs donkerder achter de muts met één lichte ribbe (leest als slagschaduw). Geen pillow shading.

## Niet als fout gemeld (gemeten, klopt met de maatstaf of te klein)
- Riemonderkant in 2 (bijv. (31–34,42), (26–29,43)) waar Rock zwart heeft: binnenlijn in de donkerste eigen tint mag (DC r. 421–423), contrast met de broek is duidelijk.
- (49,17) enkele 4 op de ijspiek: glans.
- Horizontale 2-lijn (20–22,41) over de baardpegel: vorm, niet gekeurd.
