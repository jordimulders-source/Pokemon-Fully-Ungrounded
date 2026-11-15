# Keuring welp r8 (onafhankelijke keurder, 15 nov)

**Oordeel: FAIL** (dicht bij af; lijf, poot, staart en band zijn nu netjes, maar het gezicht haalt het model nog niet: de mond leest als zwarte haak, de tong als staafje, en het oog heeft twee glansjes).

Werkwijze: eerst blind; daarna `r7/keuring.md` gelezen en r7→r8 gedifft (49 px). Vergelijkingen: sprite 8× naast het model (bbox model x 97–942 / y 194–942 → sprite x 7–57 / y 18–63); kop op 12× naast het model, ook het model box-verkleind op het 64-raster; 1× en 3× naast Growlithe, Vulpix, Skitty (`anim_front_gba`) en `af/steenjaguar.png`; clusterscript (vlakjes ≤ 2 px).

Palet-letters hieronder: A zwart (22,11,17), B (59,34,36), C (98,64,60), E (136,96,88), H (170,128,114), K (204,166,148), D lila-donker (113,86,97), J lila (174,152,181), L oog (188,178,164), N wit, F tong-donker (186,96,98), I tong-licht (230,140,134).

## Hoofdvraag
Op 1× leest hij goed: zittende welp die zijn poot likt, gehakte-steenfacetten, geen kussen, past qua formaat en kleurwerk naast Growlithe/Vulpix en de volwassen vorm. Het 3D-idee staat. Maar naast het model op 8×/12× is het gezicht nog het zwakke punt: in het model is het een open, blije bek met een tong die over de lip naar de poot krult; in de sprite een zwarte lijn die bij de mondhoek omhoog haakt, met een rechte roze staaf eronder. Dat is precies de "rommelige mond"-lezing waar Jordi op afkeurt. Ik zou hem zo niet trots laten zien; na de drie kleine MOET-reparaties wel.

## Eis 1: trouw aan het model
| Onderdeel | Oordeel |
|---|---|
| Oren | OK |
| Voorhoofdsband | OK: gesloten, één lila vlak met binnenlijn D (14,24)→(19,21); rechtereinde nu gaaf (r7 MOET 2 opgelost). Golf en binnenlijn over de hele lengte: zie MAG |
| Oog | Vorm OK, maar **twee witte glansjes** (17,27) en (20,27) aan weerszijden van de pupil; model heeft er één (MOET 3) |
| Ver oog | toegestaan; (11,27) N blijft |
| Snuit / neus | OK: driehoek met punt (11,33) (r7 MOET 1 opgelost). Kleinigheid zie MAG |
| Mond | **AFWIJKING** (MOET 1): zwarte haak (17–18,34) + (18,35) loopt boven de lip omhoog; model = mondhoek die naar onder/achter afloopt |
| Tanden | OK in plek (12,36), (15,36), (16,38); onderkaak zie MAG |
| Tong | **AFWIJKING** (MOET 2): rechte staaf x12–14 y36–40; model = tong die naar links over de poot krult (tip breder, naar links). Plus open rand op (11,37) |
| Opgeheven poot / tenen | OK (r7 MOET 3 opgelost) |
| Elleboog | OK (r7 MOET 5 opgelost) |
| Borst, romp/facetten, dij, voeten | OK |
| Staart met ring | OK (r7 MAG deels uitgevoerd) |
| Spiralen | buiten beoordeling (volgende ronde) |

## Eis 2: Gen 3-techniek
- 14 kleuren + transparant; bruin 5 tinten incl. K als 4e licht (toegestaan); stappen ±30–40: OK.
- Geen pillow shading, geen banding op het lijf; losse 1–2 px-clusters zijn alleen lijnen (band, rug, spiralen) en glans: OK.
- Resterend: open buitenrand naast de tong (11,37), lichte pixel in de neusrand (9,32).

## Status r7-punten
1. Neus: **opgelost**. 2. Bandeinde: **opgelost**. 3. Tenen: **opgelost**. 4. Tongrand: **opgelost** ((11,39) nu B). 5. Elleboog: **opgelost**.
MAG r7: rug dubbele rand opgelost; staart rechterkolom opgelost; schouderspiraal-korrel weg. Mondlijn (11–16,35) nog steeds kaarsrecht en de r7-keurder keurde de mond "OK"; ik niet (zie MOET 1).

## MOET-reparaties
1. **Mondhoek zonder haak (x17–18, y33–35).** Nu (17,34)A, (18,34)A, (18,35)A en (18,33)B vormen samen met de lip y35 een L/haak die omhoog wijst. Maak (17,34) en (18,34) → C, (18,33) → E, (18,35) → B. Zwart blijft alleen de lip (11–16,35) en de hoek (18,36–37), zodat de mond naar onder afloopt zoals in het model.
2. **Tong krult naar links over de poot (x10–14, y37–40).** Nu een rechte staaf van 3 px (x12–14) met een gat in de buitenlijn op (11,37). Maak: (11,37) → B (rand dicht); (11,39) → I en (11,40) → I (tip wordt 3 px breed: x11–13); (10,39) en (10,40) → B als buitenlijn van de tip. De groef F op x13 en de lichte kolom x12 blijven; tip raakt de poot op y41.
3. **Eén glans in het oog (20,27).** (20,27) N → L. Alleen (17,27) blijft wit, linksboven van de pupil zoals in het model.

## MAG-punten
- Voorhoofdsband: binnenlijn D stopt bij (19,21); in het model loopt de groef als golf door tot het rechtereinde. Eventueel (20,21) of (21,21) → D voor één extra stap; bij de spiraalronde meenemen.
- Onderkaak: model toont twee ondertanden rechts van de tong; sprite heeft er één (16,38). Een tweede op (17,38)? Alleen als het niet als blokje leest.
- Mondlijn (11–16,35): 6 px kaarsrecht zwart; (11,35) → B maakt hem taps naar de snuitpunt.
- Neusrand (9,32) C op de buitenlijn tussen twee B's: → B.
- Spiralen (volgende ronde): schouderspiraal heeft losse M-pixels (25,40), (25,44–45); dijspiraal M-fragmenten (43–44,53).
