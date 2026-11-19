# Hoatzin fase 2, r7 (19 nov), maker

Op r6 (`r6.png`); silhouet 0 px anders (assert). Jordi: "het oog, de kuif, het hoofd, allemaal echt veel te blurry nog" + keurder r6.
`sh alles.sh` bouwt alles; regels en tellingen in `r7.log`. Palet = r6 (`normal.pal`).

## Kopvarianten (`kop_A/B/C.png`, `kop_vel.png`: model | A | B | C | r6 op 12×, plus 1×/2× licht/donker)
Buiten de kuifzone 0 px verschil tussen de varianten (gecontroleerd in `r7.py`). **`hoatzin.png` = B.**
- Strengen = rechte lijnen op modelplekken (begin/eind afgelezen op het 1024-model met spriteraster, `modelgrid.py`), gerasterd tot 1 px zonder trapjes. T1 links buiten, T2 verticaal (x11), T3, T4 lange diagonaal, T5 vlag rechts, T6 lange streng rechts, T7 onderste streng over de rug.
- Tussenruimte = vleugel erachter in de modeltoon (zonder bruin; drempels van r6 63/94): rustig mauve vlak.
- Kuifmassa (basis bij de kop) = cellen met ≥ 55 % bruin in het model (`kuifkaart.py`, vol model).
- **A**: 7 strengen van 1 px licht bruin (7), op de buitenrand donkerbruin; massa donkerbruin.
- **B**: 5 strengen (T1, T2, T4, T5, T6) van 2 px: licht 7 + donkere rand 6 aan de schaduwkant; massa donkerbruin.
- **C**: zoals het model: massa licht bruin (alle cellen ≥ 50 % bruin), 7 strengen als donkerbruine 1-px lijnen.
- Geprobeerd: strengen automatisch zoeken (Hough op donkerbruin); vond vooral schijnlijnen door de dichte massa, niet gebruikt.

## Gedeeld (alle varianten)
1. **Oog** pixel voor pixel uit **Latios** (`graphics/pokemon/latios/anim_front_gba.png`, x9–13 y17–21: rood oog op blauw gezicht), pupil op de modelplek (12,21). Omzetting: rood → 10, donkerrode pupil en zwart → 1, donkerblauwe oogrand → 8, Latios-wit → rood (geen oogwit, SPEC), behalve het witte pixel rechtsboven → glans (5). Variant met het Latios-wit als bleekroze (5) bekeken: leest als oogwit, niet gehouden.
2. **Gezicht**: vorm = modelblauw (≥ 40 % per cel) plus de oude oogpixels; vlak 9, rand 8 alleen onder/rechts (schaduwkant), geen 8/9-schaakbord meer.
3. **Snavel**: binnencellen e (14), f (15) waar het model licht is (≥ 95: rug (8,23)(7,24)(7,25)), buitenrand/onderkant/haakpunt 1.
4. **Waaier** (x36–56, y2–18): oude strepen weg; **6 schachten** uit de modelstreepkaart (1 px per rij, ≥ 3 px) + de lichte voorrand; **pengrenzen** uit de modelgroef (modelpixel ≥ 15 donkerder dan omgeving) als 1-px lijn index 2, alleen met 3/4 aan beide kanten (naast een schacht 1 px opgeschoven), geen 2×2. Patroon per pen: grens 2 · vlak 3 · schacht 5.
5. **Donkere onderkant** (x34–50, y25–33): vlak 2, lijnen = cellen met ≥ 30 % modelpixels < 30 helderheid, 2×2 en stukjes < 3 px weg → doorlopende diagonale 1-px lijnen.
6. **Buiklicht**: zelfde aantal px (16), gekozen op afstand tot een ellips gefit op de gladde modeltoon (≥ 124); hoeken ronder, midden (20,2; 40,6).

## Afwijking t.o.v. r6 (hoofdversie B)
| zone | px |
|---|---|
| kuif (kuifzone) | 114 |
| gezicht + oog | 23 |
| snavel | 8 |
| waaier | 54 |
| onderkant vleugel | 13 |
| buik | 4 |
| **totaal** | 213 |

Zwart binnen de figuur 3,6 % → 2,9 %; index 2: 19,8 % → 21,1 % (pengrenzen en onderkantvlak).

## Zelf gezien, open
- Oog = Latios-patroon in rood: een rood kruisje rond de zwarte pupil met glans; leest op 1× als rood oog, op 12× als "plus".
- Waaier is drukker dan r6 (6 schachten + pengrenzen per pen), zoals gevraagd; schachten op 45° worden trapjes van 1 px.
- Kuif: A/B hebben een donkere kap, C een lichtbruine (dichtst bij het model).
