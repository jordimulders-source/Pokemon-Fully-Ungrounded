# Olinguito (Dark-starter, fase 1): front-sprite v1

Bestanden: `anim_front.png` (64×128, 2 frames, 16 kleuren, index 0 transparant), `normal.pal` (JASC), `compare.png` (naast Treecko, Torchic, Mudkip, Zigzagoon, Lileep, Vulpix, Makuhita; GBA en in-game; vergroot en op 1×).

## Ontwerp
- **Frame 1: de inbreker.** Zit rechtop als een teddybeer, kijkt driekwart naar links. De verste poot hangt voor de borst in de klassieke "sluip-inbreker"-houding, met drie lange haakklauwen die naar beneden bungelen (in het silhouet, zwart omlijnd zoals bij Sandshrew). De voorste poot klemt een gestolen bes op schoot; twee klauwen haken over de voorkant van de bes. De achtervoet heeft ook twee klauwen. Zo zitten de **lange klauwen** op drie plekken en zijn ze op 1× leesbaar.
- **Frame 2: "hehe".** Ogen dichtgeknepen (^ ^), bek open met één hoektand, voorste poot omhoog met gespreide klauwen (graai-gebaar), staart zwiept verder uit, kop 1 px omhoog. De bes ligt los op schoot. Verschil frame 1-2: 0,52 (Hoenn-mediaan 0,62).
- **Gezicht:** groot rond hoofd (±40% van de hoogte), korte crème snuit die links buiten de kopcontour steekt (teddybeer), zwart neusje met bruine glans, grote donkere ogen met een witte glans linksboven en een bruine iris onderin; verste oog smaller (driekwart). Kleine ronde oren met crème binnenkant.
- **Staart:** lang, pluizig (getande rand), krult achter het lijf omhoog; vage ringen in de donkerste tint (olinguito's hebben een zwak geringde staart; de echte ringen/het masker zijn voor de wasbeer-eindvorm).
- **Grootte:** 41 hoog × 45 breed, 1130 px (Treecko 967, Mudkip 852; de lange staart maakt hem iets groter). Voeten op y 57 → `frontPicYOffset = 6`.
- **Kleur en licht:** wollig oranjebruin, licht linksboven, selout: boven/links de donkerste vachttint, rechts/onder zwart. Dithering alleen als 1-2 px overgangsband tussen de vachttinten (wolligheid), 4%.

## Paletindeling (voor de 8 paletten)
| index | wat | groep |
|---|---|---|
| 0 | transparant | |
| 1–4 | vacht: hooglicht, **basis**, schaduw, donkerst (selout/plooien) | `vacht` |
| 5–7 | snuit, buik, binnenkant oren: licht, **basis**, schaduw | `creme` |
| 8–9 | klauwen: licht, schaduw | `klauw` |
| 10 | iris (en glans op de neus) | `oog` |
| 11 | donkerrood: schaduw/selout van de bes én binnenkant van de bek | (bes) |
| 12–13 | bes licht, bes basis (13 ook de tong in frame 2) | (bes) |
| 14 | wit: oogglans, bes-glans, hoektand | |
| 15 | omlijning #101010 (ook pupillen, neus, mond) | |

Receptvorm: `{'vacht': [1, 2, 3, 4], 'creme': [5, 6, 7], 'klauw': [8, 9], 'oog': [10]}`; de bes (11–13) en wit blijven in elke variant gelijk (gestolen bes, rode bek). De meest gebruikte tint per groep is de basis (vacht 2, crème 6). Snelle proef met een albino- en een zwarte vacht: alle lijnen blijven staan; bij albino vallen de ivoren klauwen wel minder op tegen de vacht (hun zwarte rand houdt ze leesbaar).

## check.py (`--stage 1`)
- Geen FOUT.
- LET OP **rand: aandeel zwart 0,63** (Hoenn fase 1 p90 0,58): bewust; rechts/onder zwart voor het in-game contrast (§0), en de klauwen zijn rondom zwart omlijnd. Het ligt op het niveau van de in-game Gen 3-set (58%).
- LET OP geen `back.png` en geen `icon.png`: nog niet gemaakt (niet in deze opdracht).
- OK: hoogte 41, breedte 45, oppervlak 1130, 15 kleuren, rand linksboven 0,27 / rechtsonder 0,11, licht −0,21/−0,20 (linksboven), schaduw 41%, dithering 4,1%, losse pixels 17, zwarte binnenlijnen 7,6%.
- species_info: `.frontPicSize = MON_COORDS_SIZE(48, 48)`, `.frontPicYOffset = 6`.

## Zelf nog niet tevreden over
- De voorste arm in frame 1 (rechts langs de buik) is smal en leest vooral als een donkere lijn.
- De opgeheven poot in frame 2 is wat dun; de gespreide klauwen staan dicht tegen het oor.
- De staartpunt is wat stomp; de ringen zijn bijna niet te zien (bewust zwak, maar mag iets duidelijker).
- Ten opzichte van de GBA-starters is hij donkerder/bruiner (zoals bedoeld voor het in-game contrast), maar daardoor ook minder "fris"; Jordi moet beoordelen of het oranje feller mag.

## Werkwijze (bron)
Opgebouwd met een vormgenerator (ellipsen + buis voor de staart, belichting en selout automatisch, schaal 0,82 voor lijf / 0,9 voor de kop) en daarna met de hand afgewerkt als ASCII-raster (kop, gezicht, armen, klauwen, voeten, bes), plus een automatische ditherband. De PNG zelf is de bron voor verdere handmatige aanpassingen.
