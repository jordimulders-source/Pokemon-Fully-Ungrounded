# Salticonda – kleurronde 3g (reparaties uit de keuring + Electric-hint)

Jordi (letterlijk): "repareer 1 t/m 4, en voeg een electric hint toe". Basis: `../kleur3f/`. Keuring: `../keuring/KEURING.md`.

## Bestanden
- `salticonda.png`, `salticonda_raster.txt` (letters als in 3f; `v` = index 15).
- `vel.png`: 3f en 3g op 4× en 1×, op licht en donker, de pre-evolutie op 2×/1× ernaast, uitsneden op 5×/8× (ringen, ring 3, onderrand, staart, glans).
- Scripts in `../scripts/`: `kleur3g.py` (alle ingrepen, per pixel), `check_kleur3g.py` (diff-bewijs), `vel_kleur3g.py`.

## Wat er veranderde
| Zone (3g-coördinaten) | Pixels | Wat |
|---|---|---|
| 4: verschuiving | hele sprite | 2 px omlaag. Rij 0–1 leeg (2 px lucht boven), rij 63 leeg. |
| 1: halsband (x 12–44, y 22–28) | 26 | De onderste twee rijen in het midden (x 19–26) 1 px omlaag; de onderrand zakt naar y 28. Runs gebroken: r→s op (34–35, 25), s→t op (37–39, 26), q→r op (30, 24). |
| 1: ring 2 (x 10–50, y 32–38) | 45 | Band per kolom 1 px omlaag op x 18–19, 22–28 en 31–32. Bovenrand nu 33 (3) · 34 (5) · 35 (4) · 36 (7) · 35 (4) · 34 (4) · 33 (4). Bevat 3 K→O-pixels van de rechterrand. |
| 1: ring 3 (x 4–52, y 45–52) | 32 | Band op x 20–27 1 px omlaag. Bovenrand nu 47 (3) · 48 (6) · 49 (6) · 50 (8) · 49 (7) · 48 (6) · 47 (4) · 46 (3) · 45 (4). |
| 2: onderrand (y 57–62) | 31 | Alle index 2 (K) op de onderste omlijning → index 1, van (3,57) tot (32,62). Index 2 blijft alleen als overgang linksonder op (1,55) en (2,56). |
| 2: schaduwkant rechts (x 40–63, y 23–40) | 11 | K→O langs de rechterrand van halsband en ring 2 (script bewijst: alleen K→O). |
| 3: staart (x 55–63, y 43–57) | 57 | Nieuwe staart (zie hieronder); de oude haak is weg. |
| 5: Electric-glans | 5 | (18–21, 24) en (32, 23): de crème glans in de halsband wordt warm lichtgeel. |
| **Buiten de zones** | **0** | Kop, kuif, neus, oog, wenkbrauw, korst en windingtinten zijn gelijk aan 3f (verschoven). In de rijen 0–23 zijn alleen (32,23) (glans) en (44,23) (K→O aan de rand van de halsband) veranderd. |

Totaal 207 pixels. Palet 0–14 gelijk aan 3f. Index 15 = (252, 232, 96).

**Staart.**
- Hij groeit uit de onderste winding: rechtsonder loopt de winding zonder omlijning door in de staart.
- Hij is 5 px dik aan de basis en wordt smaller naar een hals van 4 px.
- Op de hals zit een turquoise pekelnaad, als band van de anaconda.
- Daarop staat een zoutkegeltje van 6×5 px met omlijning. De punt is 1 px. Het licht komt van linksboven (a/b), rechts zit schaduw (d/e) en er loopt een okernaad (g) als korst door.

**Electric-hint.** Ik koos de "geladen glans op één ring". Losse vonkjes op ring 2 en 3 heb ik geprobeerd, maar die lazen als stof of ruis. Een blok van 2×2 geel las als een knoop of belletje. Een glansstreep van 4 px langs de band, plus één glinstering rechts, leest als oplichtend glas. Hij is geel en dus niet ijzig.

## Controle (`python3 scripts/check_kleur3g.py`)
- 64×64, mode P, transparency 0, 16 kleuren.
- Buiten de zones 0 pixels gewijzigd.
- Langste run van één turquoise index: halsband 8, ring 2 7, ring 3 8 (was 17/11/21).
- Aan de buitenrand alleen de indexen 1, 2, 3, 13 en 14. De pixels met 13 en 14 aan de rand zijn dezelfde als in 3f; er zijn geen nieuwe open randen.
- Donker aandeel (index 1): 0,036 → **0,057** (144 px). Pre-evolutie: 0,09.

## Checklist SPRITE_NORM (gerepareerde punten)
| # | Uitslag |
|---|---|
| 5 Geen rechte lijnen | ok. De ringen zakken in het midden 1 px door als een ellips. Runs zijn hooguit 8. De lichte bovenkant (r/q) en de donkere onderkant (t) blijven. |
| 8 Kenmerken op 1× | ok. De staart leest op 1× als een dikke staart met een kegeltje erop, niet meer als een haakje. |
| 9 Omlijning | ok. De onder- en rechterkant zijn bijna-zwart en de lichtkant links blijft h/K. Op licht heeft hij nu gewicht op de grond. |
| Lucht | ok: 2 px boven, 1 px onder. |
| 1, 2, 4, 10 | ongewijzigd ok. De staart zit vast (geen Escher) en heeft geen losse delen. |

## Eerlijk oordeel
- Naast 3f op 1× en 4× oogt hij niet vreemder: de kop is pixel voor pixel gelijk.
- De ringen buigen nu met de winding mee, de onderkant staat zwaarder en de staart is een echte staart met een zoutkegel.
- Het donkere aandeel is 0,057, dus het doel van ±0,06 uit de keuring is gehaald. Alle omlijning aan de grond- en schaduwkant is nu index 1. Meer donker zou betekenen dat ik in de vulling ga donkeren, en dat hoort niet bij deze opdracht.
- De Electric-hint is op 1× **net** te zien, zoals gevraagd. Mocht Jordi hem duidelijker willen, dan kan dezelfde glans ook op ring 2 (1–2 px).

## Lessen
- Breek je de banding door een band per kolom te verschuiven (de band zakt 1 px, de vrijgekomen pixel krijgt de kleur erboven), dan blijven de tinten en de dikte van de ring gelijk.
- Gebruik bij een wiscommando in een bewerkingsscript `-` voor "laten staan" en sluit die pixels expliciet uit. In een eerste versie wiste het script de lichaamsomlijning onder de staart.
- Een geel accent leest als "geladen" wanneer het een bestaande glans vervangt. Als losse stip leest het als ruis.
