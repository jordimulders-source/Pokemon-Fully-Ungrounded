# Pitahaya-draak fase 3, sprite r8 (maker)

- **Basis:** `../sprite_r7/pitahaya3_r7.png`, palet ongewijzigd. Zie `../sprite_r7/NOTITIES.md` voor de paletwissel en de punten van r7.
- **Script:** `python3 maak_r8.py` schrijft `pitahaya3_r8.png` en `pitahaya3_r8_afwijkingen.txt` (83 px t.o.v. r7, elke pixel met een assert op de oude kleur). Het vel maak je met `python3 vel.py <tijdelijke map>`.
- **Vel:** r8 | r6 zonder tong | model op 8×; close-ups op 12× van nek/schouder, knots + rafels en verre arm; 1× en 2× naast Salamence, Tyranitar en Sceptile.

## Jordi (letterlijk, via coördinator)
- "verder mist die al het contrast dat sprites normaal wel hebben"
- "de dynamiek in de staart dragonfruit moet ook behouden blijven, dus de groene rafels"
- "degene aan het uiteinde is te groot en aan de beenzijde zijn ze verdwenen"

## Controle
- Kop: geen pinkpixel, oog of bekpixel gewijzigd. In het kopvak (x 0-20, y 12-30) zijn alleen 4 groene nekpixels donkerder gezet als slagschaduw van de kop: (20,24), (20,27), (19,28) en (20,29). De coördinator gaf dat vrij.
- Bek (x 0-12, y 26-38) is pixelgelijk aan r6 zonder tong. De buikzone is pixelgelijk aan r6 buik.
- Silhouet: alleen de 7 px van de rafel aan het uiteinde zijn weg. Het script controleert dat er precies die 7 verdwijnen: (13,50), (14,50), (12,51), (15,53), (14,54), (15,54) en (16,54).
- 14 kleuren incl. transparant.

## Per punt (px)
| stap | px | wat |
|---|---|---|
| 1 nek/schouder | 45 | Zie de punten hieronder. |
| 2 verre arm | 12 | Lichte kant in h (één tint lager dan het H van de nabije arm), vulling G, schaduwkant g. Hij blijft een stap donkerder dan de nabije arm. |
| 3 romp achter arm | 4 | (35,35) en (29-31,36) in G. De nabije arm (h/H) komt los van de romp. |
| 4 roze rug | 7 | Onderrand van de plaat bij de nek (28-30,23) in d tegen het groen. De grote plaat bij (40-44,26-29) was bijna helemaal r en heeft nu p linksboven. |
| 5a rafel aan het uiteinde | 8 | Kleiner gemaakt naar de maat in het model (zie de tabel hieronder). |
| 5b rafel aan de beenzijde | 9 | Schutblad terug op de modelplek, rechtsboven op de knots (x 27-28, y 51-54): lichte kant h, schaduwkant G, punt (27,54), en r ernaast in het roze. |

Stap 1 (nek/schouder) in detail:
- Het grote H-vlak is teruggebracht tot een band van 1-2 px direct onder de rugplaten.
- Slagschaduw van de kop op de nek (G).
- Schaduw langs de onderkant van de nek naar de buik.
- Spierlijn nek→schouder in G op de plek uit het model (24,27) → (29,29).
- Klein hooglicht op de schouderbolling (29-31,30-31), met schaduw erachter (33-35,30-31).

## Rafels: model vs sprite
Gemeten als modeldekking per spritecel; meer dan 50% telt als in het silhouet.

| rafel | model | r6/r7 | r8 |
|---|---|---|---|
| uiteinde, bovenste (punt) | punt (13,51); rij 50 alleen x 15-18 | punt (12,51); rij 50 x 13-18 | punt (13,51); rij 50 x 15-18 |
| uiteinde, tussen 1e en 2e rafel | rij 53 vanaf x 16, rij 54 vanaf x 17 (x 14-16: 10-44%) | rij 53 vanaf x 15, rij 54 vanaf x 14 | zoals het model; inham terug, rand (17,54) g |
| 2e rafel (links) | punt (15,55) | punt (15,55) | ongewijzigd |
| beenzijde (rechtsboven) | blad x 26,5-28, y 50,5-54, punt bij (28,54) | alleen (26-28,51) en (27-28,52) G; las als vlek | blad x 27-28, y 51-54, punt (27,54) |
| onder rechts | x 25-27, y 57-58 | (24-25,57), (25,58) h | ongewijzigd |

Tussen r6 en r7 is aan de groene rafels niets veranderd. r7 wijzigde in de knots alleen roze: bovenrand r, P-hooglicht, r-schaduw. De rafel aan de beenzijde ontbrak dus al in r6.

## Eerlijk oordeel op 1×
- De nek heeft nu licht boven, schaduw onder en een spier/schouderbolling. Hij is niet langer één vlakte.
- De knots leest met een smallere punt links en een blad rechts.
- Nog zwak: het blad aan de beenzijde is maar 2 px breed en leest op 1× vooral als lichte streep. Groter kan alleen door het silhouet aan te passen, en het model heeft het daar niet groter.
- De close-up-uitsneden van het model op het vel liggen niet helemaal gelijk met de sprite (box.py-geometrie). De 8×-rij is de betrouwbare vergelijking.
