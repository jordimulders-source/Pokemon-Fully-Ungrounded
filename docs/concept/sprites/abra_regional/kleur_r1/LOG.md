# Regionale Abra, kleur_r1 (maker-agent, 13 nov)

Methode: Krassault (model OVERNEMEN, niet hertekenen). Model: `../referenties/gemini_gekozen.png`.

## Stappen en scripts
1. `pitch.py`: randsterkte per kolom-/rijgrens → **pitch 8,00 px op beide assen**, rastergrens bij 6,75 (+8k).
   (16 px scoort even hoog, maar beide fases van 16 (6,75 en 14,75) scoren gelijk → het echte raster is 8 px.)
2. `natief.py`: mediaan van het middelste 4×4-blok per cel → `natief.png` (127×127); **figuur 96×96 natief**.
3. Schaal: 96 px past niet in 64. Exacte **2×2-reductie** (`half2.py`, offset oy=0 ox=1) → **figuur 48×49, 1071 px**.
   Ter vergelijking: Abra (Gen 3) 50×41, 951 px; regionale Kadabra 63×54, 1232 px. 1,5× zou 1810 px geven (groter dan de Kadabra), dus 2× is de juiste maat voor fase 1.
   De vier offsets zijn vergeleken (gemiddelde helderheidsfout t.o.v. natief 35,5–36,5, vrijwel gelijk); ox=1 gekozen omdat daar het gesloten oog en de lijnen het minst breken.
   Regels in `half2.py` (niets getekend, elke pixel komt uit zijn 2×2-modelblok):
   - silhouet: blok is figuur als ≥ 2 van 4 modelpixels figuur zijn (ook gaten: kerf in het oor, gat onder de kop, gaatjes tussen vingers blijven);
   - buitenrand = 1 px omlijning waar het model zwart heeft (blok of 1-px-ring eromheen); waar het model zelf een gekleurde rand heeft (bovenkant staart) blijft de modeltoon;
   - binnenlijn: blok met ≥ 2 zwarte modelpixels; blok met 1 zwarte pixel alleen als brug tussen twee lijnstukken;
   - vulling: meest voorkomende modeltoon in het blok (gelijkspel: tint linksboven, anders de donkerste).
   Resultaat = `onderlaag.png`.
4. `repareer.py`: alleen Gen 3-reparaties op de onderlaag → `abra_r1.png`.
5. `maak_vel.py` → `abra_r1_8x.png`, `vel.png`.

## Palet (10 kleuren + transparant; = de tonen van het model, k-means op natief.png)
| idx | RGB | helderheid | rol |
|---|---|---|---|
| 0 | (255,0,255) | – | transparant |
| 1 | (14,13,22) | 14 | omlijning |
| 2 | (49,48,61) | 50 | donkere schouders/lijf |
| 3 | (71,68,87) | 71 | |
| 4 | (89,88,103) | 90 | lichte schoudertint |
| 5 | (115,111,132) | 115 | |
| 6 | (130,126,150) | 132 | huid schaduw |
| 7 | (142,139,158) | 142 | |
| 8 | (161,158,174) | 161 | |
| 9 | (180,179,191) | 180 | huid |
| 10 | (209,206,219) | 208 | glans linksboven |

Ter info (geen wijziging): de regionale Kadabra gebruikt 96/146/184/220 met meer violet (bv. (146,140,170)); de modeltonen van deze Abra zijn grijzer met een lichte violette zweem. Voorstel ter keuze voor Jordi/coördinator: de huidtonen 6/9/10 naar de Kadabra-tonen trekken ("zelfde huidskleur als de rest"); niet gedaan, want het model is wet.

## Gerepareerde pixels (12, x,y in 64×64)
| x,y | van → naar | reden |
|---|---|---|
| 33,16 | 10 → 1 | lichte tint op de buitenrand (oorpunt) → omlijning |
| 27,20 | 9 → 1 | idem (oor) |
| 30,43 | 9 → 1 | idem (hand) |
| 12,47 | 10 → 1 | idem (linkervoet) |
| 15,49 | 10 → 1 | idem (linkervoet) |
| 18,49 | 9 → 1 | idem (linkervoet) |
| 16,50 | 9 → 1 | idem (linkervoet) |
| 30,56 | 9 → 1 | idem (voet midden) |
| 49,58 | 9 → 1 | idem (staart) |
| 29,28 | 9 → 1 | gesloten rechteroog: modelstreep natief (42,59)…(46,55) viel door de reductie half weg (1 zwarte modelpixel per blok) |
| 28,30 | 9 → 1 | idem |
| 22,30 | 2 → 1 | gesloten linkeroog: modelstreepje natief (47,44)(47,45) werd donkergrijs |

Niet aangeraakt: vlekjes en streepjes (Jordi: "behoud die vibe"), kerf in het oor (gat bij 31,18 komt uit het model), de gekleurde bovenrand van de staart (zo in het model), mond (geen).

## Zelfgeziene zwakke punten (open)
- **Handen/vingers**: het model heeft vingers van 1 px met 1 px tussenruimte; op 2× worden ze een onrustige vlek van lijn- en tintpixels. Het silhouet en de tonen volgen het model, maar de vingers zijn niet meer als vingers te tellen. Oplossen zonder hertekenen kan niet; voorstel: Jordi kiest of de handen per pixel uit het model "getrokken" mogen worden (gekozen pixels uit het 2×2-blok i.p.v. de meerderheid).
- **Omlijning 33%** van de pixels: zwaarder dan Gen 3-gemiddeld (±25%), omdat het model veel binnenlijnen heeft (schouders, armen, staartsegmenten).
- **Linkeroog** is 1 px; het model toont een kort streepje (2 natieve px). Leest op 1× nauwelijks; het rechteroog leest wel.
- Linksonder de kop (donkere onderkant van de snuit) is wat rommelig, zoals in het model.
