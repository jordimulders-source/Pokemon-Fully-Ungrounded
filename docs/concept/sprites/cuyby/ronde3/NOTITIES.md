# Cuyby fase 1, ronde 3: polijstronde volgens de spritingregels

Basis: **ronde 2** (Jordi: "beetje een Hamtaro-look, maar dat zou een Pokémon kunnen zijn", voor 90% goed). Ontwerp: concept C2. Het silhouet, de pose, de driekleur, de ogen en de lokken zijn niet veranderd: oppervlak 789 px, 31×32, gelijk aan ronde 2. De hele sprite staat als tekstraster in `bron/cuyby.py`. Ik heb hem rij voor rij met de hand herschreven vanuit het raster van ronde 2.

## Wat er gepolijst is (tegen de blinde test van ronde 2)
| Klacht blinde test | Ronde 3 |
|---|---|
| grote rechte kleurvlakken zonder overgang | Het **crème** heeft nu een hooglicht (a) linksboven op het voorhoofd. De schaduw (c) loopt in een band langs het oranje, waar de bol wegdraait, en neemt onderaan toe. Het **oranje** heeft een hooglicht bij de scheiding en een gekartelde vachtgrens tussen basis en schaduw. Het **zwart** heeft een glansband langs de belichte bovenrand in plaats van losse spikkels. |
| schaduw volgt het volume nauwelijks | De grens tussen licht en schaduw ligt nu schuin van rechtsboven naar linksonder (de evenaar van de bol). Onder de evenaar wordt de linkerkant schaduw met een zwarte omlijning. De haarstrengen (c) lopen recht naar de lokscheidingen. |
| dunne, onderbroken omlijning | De crème-omlijningsbasis is donkerder: 139,106,65 in plaats van 164,131,90, dat als gat las. Onder de evenaar en onderaan de lokken is de omlijning zwart. De lokscheidingen gaan van omlijningsbasis (boven) naar zwart (onder), zoals de overgang langs de omtrek in de gids. |
| linkeroog valt weg in het zwart | Er zit een lichte rand (g, de glanstint van het zwart) rond het hele oog, ook erboven. Het oog heeft een witte glans linksboven en een bruine weerkaatsing rechtsonder. |
| (eigen) zwart vlak met zwarte rand | Waar de glansband tegen de rand ligt, is de omlijning de basistint van het zwart (G), net als bij Scorplack in de gids. Elders blijft hij zwart. |

## Checklist SPRITING.md
| Regel | Toegepast |
|---|---|
| 1. Geen vormgereedschap | Ja: één tekstraster, geen automatische schaduw of omlijning (ronde 2 had nog een paar automatische randcorrecties; die zijn nu met de hand in het raster verwerkt). |
| 2. Werkwijze | Polijstronde: de bestaande sprite als basis, per zone (zwart, crème, oranje, lokken, ogen) met de hand bijgewerkt. |
| 3. Curven, geen spiegelen | Het silhouet is ongewijzigd: de stairstep-bol van Jigglypuff, zonder hoeken in de rondingen. De oren zijn verschillend (zwart en oranje, andere vorm). De lokken verschillen in breedte. |
| 4. Palet 3 tinten + omlijning | Crème a/b/c + e. Oranje o/O/q + Q (Vulpix-ramp 238,156,74 / 205,123,41 met een lichter hooglicht). Zwart g/G, met de omlijning als schaduw (Scorplack-aanpak voor donkere kleuren). Roze 2 tinten, oog + weerkaatsing. 16 kleuren, index 0 transparant. |
| 5. Licht linksboven, evenaar | Zie boven. Het oranje zit aan de schaduwkant en is dus grotendeels schaduw, met licht alleen bij de scheiding. |
| 6. Ogen | Glans linksboven (2×2, zoals Skitty/Jigglypuff), gekleurde weerkaatsing rechtsonder en een lichte rand om het linkeroog. |
| 7. Vacht gekarteld | De grens tussen oranje basis en schaduw is gekarteld. De strengen in het crème lopen in de haarrichting (verticaal naar de lokken). Haarstreken in het zwart lopen richting de scheiding. |
| 8. Omlijning per kleurgroep, 1 px, lichter alleen binnen | Belichte kant: omlijningsbasis (e, Q) en G naast de glansband. Schaduwkant en onderkant: zwart. Overal 1 px. |
| 9. Frames | 64×128, 2 frames. Frame 2 is een popcornsprongetje: 1 px omhoog en het mondje open. |

## Meting omlijning (frame 1)
| | oppervlak | b×h | donkere buitenrand | waarvan zwart | detail | verzadiging |
|---|---|---|---|---|---|---|
| **ronde 3** | 789 | 31×32 | 0,60 | 0,53 | 1,52 | 0,41 |
| ronde 2 | 789 | 31×32 | 0,56 | 0,00* | 1,55 | 0,40 |
| Jigglypuff | 747 | 32×33 | 0,35 | 0,35 | 1,71 | 0,43 |
| Whismur | 884 | 38×37 | 0,53 | 0,53 | 1,42 | 0,48 |
| Skitty | 934 | 41×40 | 0,38 | 0,38 | 1,83 | 0,51 |
| Vulpix | 1119 | 48×40 | 0,45 | 0,45 | 1,88 | 0,67 |

\* De omlijning van ronde 2 (49,32,32) viel net boven de grens voor 'zwart'. De nieuwe K (41,24,24) valt eronder. Het echte verschil is dus kleiner dan 0,00 → 0,53.

Het donkere aandeel (0,60) ligt boven Jigglypuff. Dat komt door het zwarte vlak: een kwart van de omtrek is zwarte vacht. Het crème en oranje hebben nu wel per kleurgroep een omlijning.

## Extra lessen uit de gids zelf (niet in SPRITING.md)
- **Scorplack (donkere kleur):** begin bij de schaduwkleur als basis en bouw daarop meerdere lagen hooglicht. De omlijning is donkerder dan de schaduw, en de schaduwkleur omlijnt de hooglichten. Zo is het zwarte vlak gedaan (G basis, g glansband, K omlijning, G als omlijnings-hooglicht naast de band).
- **Recolor-regel 4:** lichte kleuren (het crème) houden een duidelijk donkere omlijning. Daarom is de crème-omlijningsbasis donkerder gemaakt in plaats van de schaduwtint als rand te gebruiken.
- **Overgang langs de omtrek** (revamp-stappen): van omlijningsbasis naar zwart. Dat geldt hier ook voor de lokscheidingen (boven e, onder K).
- **Shine is niet hooglicht:** wit (a) staat alleen in de ogen en als klein hooglicht op het voorhoofd, niet als losse glimlichtjes op de vacht.

## Eigen oordeel
- Dichter bij Gen 3 dan ronde 2. De bol leest nu als een bol in plaats van drie vlakke stroken. Het linkeroog staat los van het zwart. De lokken onderaan hebben een duidelijke rand.
- **Wat ik bewust niet heb veranderd:** de frontale houding en de middenscheiding. Dat is het ontwerp dat Jordi goedkeurde. Een 3/4-draai zou een nieuwe ronde zijn, geen polijstronde.
- **Nog open:**
  - het mondje (een klein 'Y' van omlijningsbasis) kan beter;
  - het zwarte vlak blijft het donkerste deel van de rand.

## Bestanden
- `anim_front.png` (64×128), `normal.pal`, `compare.png`
- `bron/cuyby.py`: raster en palet. Draaien vanuit de repo-root: `python3 docs/concept/sprites/cuyby/ronde3/bron/cuyby.py docs/concept/sprites/cuyby/ronde3`. Het script gebruikt `lib.py` uit `nachtaap/ronde7/bron/`.
- `bron/raster_f1.txt` en `raster_f2.txt`: het eindraster per frame
- Het vergelijkingsvel maakt `nachtaap/ronde7/bron/vellen.py`.
