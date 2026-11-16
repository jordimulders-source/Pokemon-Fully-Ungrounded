# Eindkeuring spooktrein fase 1 (kandidaat)

Keurder: verse, onafhankelijke agent (16 nov). Alleen de uitvoering gekeurd, niet het ontwerp (stapel, ogen variant D en grotere stukken zijn door Jordi goedgekeurd).
Bekeken op 1×, 2×, 4× en 8×, naast de echte Gen 3-sprites (`anim_front_gba.png` + `normal_gba.pal`) van Magnemite, Aron, Nosepass, Registeel, Magneton en Mawile.

## Metingen
- 64×64, bbox x 8–56, y 19–62 (49×44 px). **12 kleuren + transparant** (≤ 16).
- Bruin: lijn (30,23,14) L24 · b (67,52,37) L55 · r (95,75,58) L79 · m (118,90,67) L96 · l (159,126,101) L133 · h (179,155,135) L160 (13 px glans).
- Grijs: g (54,51,43) L51 · G (78,74,68) L75 · s (123,121,117) L121 · S (163,155,147) L156. Ogen: (216,200,176) en (240,232,216).
- Stappen bruin: 24 / **17** / 37 / 27; grijs: 24 / 46 / 35. Norm (Taillow, SPRITE_KERN): ±30–40.
- Buitenrand: 120 px lijnkleur, 50 px b/g als selout (lichtkant en de gaten tussen de spaken), 12 px m/l (alleen de bovenrand van de schoorsteen).
- Losse pixels (geen buur van dezelfde kleur, 8 richtingen): 75 van 1307 = 5,7 %. Gen 3: Skarmory 5,5 %, Sudowoodo 5,7 %, Aron 8,1 %, Registeel 2,4 %. Binnen de norm.
- Gemiddelde helderheid: kandidaat L76, model L79; Gen 3-staal: 116–164.

## Oordeel per onderdeel
| Onderdeel | Oordeel |
|---|---|
| Lijnen | **FAIL (klein)**: bovenrand schoorsteen, zie 1 |
| Selout | PASS (b/g aan de lichtkant, zwart aan de schaduwkant; hoeken van de plank b/#/b zijn anti-aliasing, op 1× onzichtbaar) |
| Schaduw/lichtbron | PASS (licht linksboven overal consequent: rand van de schoorsteen, grijze plaat, band van het wiel, plank; grijze plaat onderaan is donker links door slagschaduw van de plank, geen pillow) |
| Kleuren/ramps/aantal | **FAIL (klein)**: r en m te dicht bij elkaar, zie 2 |
| Banding/jaggies/losse pixels | PASS, met één kleine breuk in de staaf (zie 3, optioneel) |
| Leesbaarheid op 1× | PASS (schoorsteen met twee ogen, spaakwiel met gaten, grijze plaat en plank lezen meteen) |
| Gen 3-stijl naast echte sprites | PASS na 1 en 2 (lijnvoering, pixelmaat en ruis vergelijkbaar met Skarmory/Magneton) |

## Reparaties
1. **Bovenrand schoorsteen dambordt** (rij 19: m l m l m) en heeft lichte kleur l op de buitenrand. Zet de lichte buitenrandpixels op m (118,90,67), zodat m een doorlopende selout is en de l-band daaronder één lijn wordt:
   (23,19), (25,19), (21,20), (19,21): l → m (118,90,67).
2. **Bruine ramp r→m maar 17 helderheid**: op 1× vallen r en m samen, waardoor wiel, schacht en midden een bruine brij worden (Jordi: "een bruine brei moet het niet worden"). Alleen het palet aanpassen, geen pixels:
   m (118,90,67) → (134,101,74) (L≈108); l (159,126,101) → (170,135,105) (L≈142). Stappen worden 24 / 29 / 34 / 18 (h is glans). Proef: spaken en schacht lezen duidelijk beter, de sprite blijft dezelfde.
3. Optioneel: de lichte staaf (diagonaal van (38,39) naar (29,44)) is onderbroken tussen (33,42) en (31,43). (32,43) m → l, zodat het lijntje doorloopt.

## Ter info voor Jordi (geen fout in de uitvoering)
- De sprite is veel donkerder dan echte Gen 3-staalsoorten (L76 tegen 116–164). Dat volgt het model (L79), dus trouw. Na reparatie 2 iets lichter.
- De wagen van fase 2 is duidelijk lichter roestbruin dan deze hoop; als de lijn als familie moet lezen, kan het palet van fase 1 later naar dat van fase 2 schuiven.

**Eindoordeel: FAIL (klein): reparatie 1 en 2 (en eventueel 3), daarna PASS zonder nieuwe keuring van het ontwerp.** Niets in de kandidaat gewijzigd; proefversie alleen in de scratchpad van de keurder.
