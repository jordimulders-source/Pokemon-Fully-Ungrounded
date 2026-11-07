# Hitmongroove: sprite naar het Gemini-model, ronde 4 (maker)

Basis: `ronde3/raster.txt` (torso c). Jordi over r3, letterlijk: "c is wel prima al, moet denk ik nog iets meer volgens de dragonflycave en gen 3 sprite regels, maar het lijkt het minst op een bulge".

## Opgeleverd
| Bestand | Wat |
|---|---|
| `capoeira.png` + `raster.txt` | Alle reparaties 1–9 uit `ronde3/KEURING.md` (torsoglans als sikkel linksboven). |
| `capoeira_glansmidden.png` + `raster_glansmidden.txt` | Alles behalve reparatie 3: glans blijft in het midden zoals c; 4 (schaduwvlek lichtkant weg) en 5 (tapse sikkel) wel. |
| `vel.png` | r4 · glansmidden · r3 · model op 8×; torso r4 · glansmidden · r3 · model op 12×; 1× en 2× op licht en donker. |
| `hand_reparaties.txt` | Elke pixel met de hand: `nummer x,y oud->nieuw`. |
| `pas_toe.py` | Zet de handlijst op het raster en controleert per pixel de oude waarde (stopt bij een verschil). |
| `vel.py` | Montage van het vel. |

De scripts doen alleen montage, png en controle (`ronde3/gereedschap/maak.py`, `controle.py`).

## Uitgevoerd
- Alle benoemde pixels van reparaties 1–7 precies zoals de keuring; elke oude waarde klopte met de keuring.
- Optioneel 8 (schaduwstrook rechts van de kop taps) en 9 (witte tenen selout 7): allebei uitgevoerd; ze halen banding en zwarte lichtkant weg.
- **Eén pixel extra, niet benoemd:** (52,7) van 1 naar F. Na reparatie 9 werd die zwarte teennaad van de rechtervoet een losse zwarte stip (de pixels erboven werden 7). Als F vormt hij met (52,6) en (52,8) één donkerblauwe binnenlijn tussen voet en teen, wat de bedoeling van de naad houdt.

## Controle (beide pngs)
- 16 kleuren incl. transparant, index 0 transparant.
- 0 losse omlijningspixels in een vlak.
- Silhouet t.o.v. r3: 0 px verschil. T.o.v. het model: 43 px, zoals r1–r3.
- Randpixels die niet 1/5/D/F zijn: 12, alle 12 zijn de bedoelde selout (A naast geel, 7 naast wit): (12,4), (11,5), (10,6), (54,6), (19,11), (20,12), (21,13), (22,15), (28,43), (28,44), (30,51), (30,52).
- Kleine vlakjes: alleen de bedoelde (de diagonale selout langs het linkerbeen, het gedraaide koord in de steunarmband, vlecht, glimpjes).

Niet gecommit, geen keurder gestart.
