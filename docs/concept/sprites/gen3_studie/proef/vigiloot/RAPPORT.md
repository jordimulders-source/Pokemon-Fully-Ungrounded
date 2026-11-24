# Vigiloot: proef tintzones (24 nov)
Bron: `docs/concept/sprites/wasbeer/af/wasbeer.png` (niet aangeraakt). Gemaakt met een gerichte pixellijst (`maak_na.py`), zonder kwantiseren, middelen of blurren. Bewijs en vel komen uit `vel_en_bewijs.py` (beide vanuit de repo-root draaien).

Bestanden: `na.png` (hoofdversie, palet gelijk aan het origineel), `na_variant_palet5.png` (variant B: dezelfde pixels, alleen paletkleur 5 donkerder), `voor_na.png` (voor | na | B | Linoone, Zigzagoon, Ursaring, Kangaskhan op 6×, met 1× eronder), `diffkaart.png` (rood = gewijzigd, 8×).

## Diagnose (gemeten)
- De vachtramp 4/5/6/7 heeft helderheden 58/85/113/145: stappen van ±28, kleiner dan bij Ursaring (97/132/164, ±33) en Kangaskhan (64/126/164).
- Het lijf bestaat vooral uit schaduwtint 5 (274 px) en grondtint 6 (229 px); licht 7 komt maar 74 keer voor. Ursaring heeft zijn lichte tint op 396 px. Bij Vigiloot is er dus bijna geen lichte zone.
- De nabije dij (links) was in zijn geheel 5, met wat 6 bovenaan. Zo leest het grootste vlak als één donkere middentoon.
- De verre heup had licht als een smalle diagonale streep van 7 langs de plooi. De borst had een rafelige 6/5-grens, met een los 6-pixeltje in het lichte schoudervlak.
- Aan de lichtkant waren de onderarm, de bovenkant van de staart en de voeten zwart omlijnd.

## Wijzigingen per zone (gewijzigde pixels)
| Zone | px | Wat |
|---|---|---|
| Nabije dij | 40 | Licht 7 als één zone linksboven op de bolling (rij 39–44), daaronder grondtint 6, schaduw 5 als sikkel onderaan en tegen de bestaande plooilijn (4), met een harde grens die schuin van (27,43) naar (16,48) loopt |
| Verre heup/dij | 9 | De lichtstreep van 7 is een wig geworden die bovenaan breder is (rij 37–42); de schaduwsikkel 5 rechts en onder bestond al en is gebleven |
| Borst | 5 | De schaduwzone 5 rechts naast de draagband loopt nu als één vlak van rij 20 tot 24, met een harde grens |
| Schouder | 1 | Een los 6-pixeltje in de lichtzone is 7 geworden |
| Buitenlijn lichtkant | 26 | Zwart 1 is de donkerste eigen tint 2 geworden op de onderarm (4 px), de bovenkant van de staart (12 px, op één plek 4, zoals de rijen eronder al hadden), de onderkant van de staart (4 px), de rechtervoet (4 px) en de linkervoet (3 px). Zwart blijft aan de schaduwkant, aan de onderkant, in de kruisholte en in de binnenkant van de staartkrul. |
| **Totaal** | **81** | |

## Bewijs (uitvoer `vel_en_bewijs.py`)
```
alfa-diff 0 | gezicht-diff 0 | palet gelijk True | onderdelen (8-F) gewijzigd 0 | totaal 81
variant B index-diff t.o.v. na 0 | B andere paletkleuren [5] | index 5 in masker/ogen/neus (x9-25, y8-17) 0
```
- Silhouet: de transparantiemasker heeft 0 verschillen.
- Gezicht: de hele kop (rij 0–19, x 9–33, dus masker, ogen, neus, snuit en de lijn eromheen) heeft 0 verschillen, en het palet is gelijk. Ook in variant B zijn de pixels van het gezicht gelijk.
- Onderdelen: buidel, draagband, handen, buikvlek en de crème staartringen (indices 8–F en 3) hebben 0 verschillen. In de staart veranderde alleen de buitenlijn.
- Variant B: alleen paletkleur 5 is veranderd, van (100,82,68) naar (88,70,58). Index 5 komt niet voor in masker, ogen of neus, wel in de binnenkant van de oren en de zijkant van de kop, die daardoor ook iets donkerder worden.

## Wat ik zelf nog zwak vind
- **Het effect van `na.png` is klein.** Naast Linoone en Ursaring blijft het lijf een donkere, grauwe middentoon. De vlekken waren hier minder het probleem; de oorzaak zit vooral in het palet: de ramp is te donker en de stappen zijn te klein. Met zones alleen los je dat niet op.
- **Variant B geeft duidelijk meer licht/donker-contrast**, maar daarmee zitten tint 5 (74) en lijntint 4 (58) dicht bij elkaar, zodat schaduw en plooilijnen op de dijen bijna samenvallen. Lichtere tinten 6 en 7 (zoals Linoone en Ursaring hebben) zouden beter zijn, maar 6 en 7 zitten in het gezicht (voorhoofd tussen het masker, glimpje op de neus (11,16)). Dat vraagt een keuze van Jordi: mag het palet van het gezicht mee veranderen, of komt er een aparte vachttint bij? Het palet is vol (15 kleuren).
- Het lichte schoudervlak heeft nog steeds een kern van 3 binnen 7 binnen 6 (3 px glans). Dat neigt naar een kussen. Ik heb het laten staan omdat het een compacte glans is.
- Ik heb geen plooilijntjes van 1 px toegevoegd zoals Kangaskhan die heeft (bijvoorbeeld tussen de bovenarm en de borst). Die zouden een nieuwe vorm suggereren die niet in het model staat. Daardoor blijft de borst één groot vlak zonder vormaanduiding.
- De lichtzone van de nabije dij ligt als een band langs de linker buitenlijn. Dat volgt de cilindervorm, maar het grenst aan banding.
- De verre heup is maar licht aangepast. De wig van 7 ligt nog vlak naast de plooilijn, dus ook daar is er wat randlicht.

---
# Ronde 2: variant C (`na_C.png`, vel `voor_na_C.png`)
Opdracht van de coördinator: til de vachtramp op naar de afstanden van Ursaring (grijsbruin houden), zet 4 en 5 verder uit elkaar, maak de grondtint de grootste massa met licht als zone, haal de 3-in-7-in-6-kern weg en leg het licht op de dij op de bolling. A en B zijn blijven staan. C bouwt voort op A (`maak_C.py`), het bewijs staat in `bewijs_C.py` en het vel toont voor | A | C | Ursaring | Linoone op 6× en 1×.

## Palet (helderheid voor → C)
| Index | Voor | C | Helderheid |
|---|---|---|---|
| 4 (lijn/plooi) | (68,55,48) | (58,46,40) | 58 → 49 |
| 5 (schaduw) | (100,82,68) | (110,92,78) | 85 → 96 |
| 6 (grond) | (130,110,90) | (146,126,106) | 113 → 130 |
| 7 (licht) | (162,142,116) | (180,160,134) | 145 → 163 |
| 3 (glans/draagband) | (198,180,152) | ongewijzigd | 182 |

De stappen zijn nu 47 / 34 / 33 / 19 (Ursaring: 33 / 35 / 32). De kleur blijft grijsbruin (R−G ≈ G−B ≈ 20). Masker en ogen gebruiken 1, 2, 4, E en F; daarvan is alleen 4 veranderd, en die is donkerder geworden. Kleur 3 heb ik niet lichter gemaakt, omdat hij dan samenvalt met crème 9 (214,198,166).

## Pixels (C t.o.v. A: 39; C t.o.v. origineel: 111)
| Zone | px t.o.v. A | Wat |
|---|---|---|
| Schouder/borst | 11 | Eén lichtzone 7 (rij 21–27, wig van linksboven). De glanskern 3 is weg, en de lichtzone loopt door op de bovenborst. |
| Nabije dij | 11 | Het licht 7 ligt als wig op de bolling bovenaan (rij 39–43) en loopt niet meer als band langs de rand naar beneden. Daaronder grond 6 en een sikkel 5 onder en tegen de plooi. |
| Verre dij | 17 | De schaduwsikkel 5 aan de rechterkant is 2 px smaller geworden (rij 36–44), dus de grondtint 6 is groter. |

Verdeling op het lijf (rij 20–51), voor → C: licht 7 50 → 88, grond 6 169 → 176, schaduw 5 204 → 162. De grondtint is nu de grootste massa en de schaduw niet meer.

## Bewijs (uitvoer `bewijs_C.py`)
```
mode/size/kleuren P (64, 64) 16
alfa-diff 0
gezicht index-diff (kop rij 0-19, x 9-33) 0
onderdelen (index 8-F) gewijzigd 0
andere paletkleuren [4, 5, 6, 7]  (zie tabel)
pixeldiff C t.o.v. origineel 111 | t.o.v. A 39
```

## Wat ik aan C zelf nog zwak vind
- De lichtzone op de borst is een grote, vrij rechte wig. Ursaring breekt zijn licht op door spierplooien, en hier zijn geen plooilijntjes toegevoegd, omdat die niet in het model staan.
- De stap 7 → 3 is maar 19. De resten van 3 (voorhoofd, draagband) springen daardoor minder uit dan eerst.
- Door het nieuwe palet zijn ook de kop (voorhoofd, oren, glimpje op de neus) en de draagband lichter geworden. De indexen daar zijn diff 0, maar de kleur is wel anders.
- Er zit nog veel 5 in het onderbeen en onder de buidel (slagschaduw). Dat is bewust gebleven, maar het maakt de onderkant zwaar.
- De lichte wig op de verre heup ligt nog naast de plooilijn (zelfde punt als bij A).
