# Pitahaya-draak fase 1, sprite r2 (maker)

Alleen de drie benoemde reparaties van de coördinator op r1. Niets getekend.
Bevroren en met script bewezen: silhouet-diff 0, gezichtsgebied x 18–34 / y 22–34 diff 0 (ogen, D-pixels, mond, tandje), buitenlijn (alle randpixels), zwarte lijnen, binnenlijnen uit de reductie (mondlijn, schubnaden, ribbels), amber, wit, mauve.

Script: `maak_r2.py` (aanroep `python3 maak_r2.py 3.5 pitahaya_r2.png 2.0`), invoer `pitahaya_r1.png` + `kaal_info.npz` + `natief.png` + `groepen.py` (kopieën uit `sprite_r1/`). Wijzigingen per pixel: `afwijkingen_r1.txt`. Vel: `vel.py` → `vel.png` (r2 | r1 | model op 8×; 1× en 2× op licht en donker).

## 1. Vulling via een toonkaart van het model
- Per kleurgroep (roze, groen) de luminantie van de natieve modelpixels gladgestreken met een gauss binnen de groep (genormaliseerd, dus geen lekken uit lijn of achtergrond): **roze σ = 2,0, groen σ = 3,5** natieve px. Per spritepixel het gemiddelde van zijn 3×3-blok.
- Kwantiseren: de drempels komen uit de eigen toonverdeling van r1 (per groep evenveel px per tint als de kale reductie gaf). Daardoor blijven de hoeveelheden licht en schaduw gelijk (volume), maar volgt de plaatsing de gladde toonkaart: licht linksboven, schaduw als sikkel rechtsonder.
- 1b: een losse pixel die de toonkaart achterlaat (4-verbonden cluster van 1) neemt de meest voorkomende 4-buur uit dezelfde groep aan.
- Geprobeerd en verworpen:
  - **Drempels op de modeltinten (dichtstbijzijnde helderheid):** σ 0,7–5 gaf óf meer eilandjes dan r1, óf het lichtgroen verdween (34 → 17–22 px, armen en dijen plat).
  - **Roze σ 3,5:** de lichte voorhoofdschubben vielen weg, de kop werd platter.

## 2. Schubranden rechts (x 39–45, y 8–30)
Een zwarte pixel die geen randpixel is en waar het model ≤ 3 zwarte px in het blok heeft (hooguit één modelrij = dunne lijn), wordt de donkerste tint van de omringende groep: roze idx 2, groen idx 8. **9 px.**
De overige zwarte pixels daar zijn buitenlijn aan de schaduwkant, of het model heeft er 5–9 zwarte px per blok: de dikke zwarte schaduwrand onder elke schubpunt. Die blijven zwart.

## 3. Palet groen (alleen waarden, 0 px)
| idx | r1 | lum | r2 | lum |
|---|---|---|---|---|
| 8 | (53,87,57) | 73 | (48,80,52) | 67 |
| 9 | (80,113,76) | 98 | ongewijzigd | 98 |
| 10 | (107,137,94) | 123 | (115,147,101) | 132 |
| 11 | (146,172,126) | 158 | (155,183,134) | 169 |

- Stappen worden 31 / 34 / 37 (waren 25 / 25 / 35).
- Kleuraard gelijk: elke kleur is r1 × één factor (0,91 / 1,07 / 1,06).

## Afwijkingen t.o.v. r1 (79 px van 1087; per pixel de laatste stap)
| Stap | hoofd/gezicht | schubpunten | lijf | armen | poten | totaal |
|---|---|---|---|---|---|---|
| 1 toonkaart vulling | 22 | 15 | 3 | 16 | 9 | 65 |
| 1b losse toonpixel | 1 | 2 | 1 | 0 | 1 | 5 |
| 2 schubrand zwart → selout | 9 | 0 | 0 | 0 | 0 | 9 |
| 3 palet | 0 | 0 | 0 | 0 | 0 | 0 |

- Zones: hetzelfde als in r1. "hoofd/gezicht" is de kop buiten het bevroren gezichtsgebied.
- Vulvlakjes < 3 px (tinten 3–5, 9–11): r1 34 → r2 32 (roze 10 → 8, lijf 9 → 10).

## Zelf vergeleken (r2 naast r1 op 1×, 2×, 8×)
- **Beter:**
  - Het lijf heeft nu een lichte kant links op armen en dijen en schaduw rechts, zoals het model.
  - Het groen heeft duidelijk meer contrast.
  - De kop is iets rustiger, met het licht gegroepeerd linksboven; de lichte voorhoofdschubben zijn behouden. Niet platter dan r1.
- **Beperkt:**
  - De winst in de kop is klein. De donkere roze schubnaden (binnenlijnen, bevroren) en de kleine groene punten blijven het patroon bepalen.
  - De kruin blijft gevlekt doordat het model daar zelf naden en punten heeft.
- **Rechterkant kop:** nog vrij zwart. Alleen 9 px voldeden aan "dunne lijn in het model"; de rest is buitenlijn of de dikke modelschaduw onder de punten. Verder lichter maken zou van het model afwijken.
