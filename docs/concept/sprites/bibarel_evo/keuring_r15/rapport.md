# Keuring hele sprite: Bibarel-evolutie `sprite_r15` → `sprite_r16` (24 nov)

Jordi: "ja de hele sprite moet goed gekeurd worden, hij moet consistent zijn met andere sprites".
Maatstaf: echte Gen 3-vachtsprites (Bibarel, Ursaring, Linoone, Furret, Swampert, Sentret, Teddiursa; frame 1) en onze goedgekeurde sprites (Alphyena, Dundragoon, Gnomad, Coathief). Geen eigen strengere regels. Vorm, silhouet, tuinbroekvorm, potlood, staart, tanden, ogen, neus en klep zijn bevroren.

## 1. Blind oordeel (eerst, zonder getallen; `blind_4x.png`)
Op 1×, 2× en 4× leest r15 als een Gen 3-sprite naast Bibarel en Ursaring: zelfde bruin (c/d/b liggen binnen ±8 RGB van Bibarels eigen palet), licht linksboven, zwarte buitenlijn aan de schaduwkant, gekleurde lijn aan de lichtkant. De drukste zone is de kraag onder de snuit (kleine bollen met eigen lijnen). Rechterarm en dijen hebben grotere tintvlakken. Bij nader kijken (16×) zag ik één plek die tegen het licht ingaat: zie 3.

## 2. Getallen (`meet.py`, `vergelijk.png`)
Vacht = bruine vulling zonder lijn. "grens" = aantal tintgrenzen per 100 vachtpixels (hoe vlekkerig). "vlak≥20" = deel van de vacht in tintvlakken van minstens 20 px.

| Sprite | vacht px | tinten | stappen (L) | eilandjes <3 px /100 | vlak≥20 | grens /100 | zwart | buitenrand zwart licht/schaduw | binnen zwart /100 px |
|---|---|---|---|---|---|---|---|---|---|
| **r15** | 813 | 3 | 37, 37 | **2,0** | 67% | 32 | 7,4% | 26 / 74% | 1,4 |
| **r16** | 813 | 3 | 37, 37 | 2,0 | 67% | 32 | 7,4% | 26 / 74% | 1,4 |
| Bibarel | 650 | 2 | 41 | 2,3 | 90% | 13 | 12,2% | 43 / 71% | 5,5 |
| Ursaring | 1565 | 3 | 23, 34 | 4,5 | 88% | 21 | 9,3% | 46 / 62% | 2,4 |
| Swampert | 810 | 3 | 16, 33 | 2,2 | 88% | 13 | 18,9% | 49 / 65% | 10,6 |
| Linoone | 485 | 4 | 23, 9, 24 | 16,1 | 59% | 26 | 13,8% | 26 / 66% | 4,5 |
| Furret | 487 | 2 | 31 | 9,0 | 82% | 15 | 4,9% | 5 / 39% | 1,7 |
| Sentret | 452 | 4 | 23, 19, 29 | 14,6 | 61% | 35 | 18,0% | 55 / 83% | 3,7 |
| Teddiursa | 449 | 4 | 24, 20, 22 | 10,5 | 57% | 35 | 13,8% | 23 / 53% | 6,3 |
| Alphyena (af) | 1069 | 5 | 36, 21, 37, 37 | 4,9 | 73% | 29 | 19,2% | 66 / 99% | 8,4 |
| Coathief (af) | 268 | 2 | 41 | 0,0 | 95% | 21 | 31,6% | 83 / 83% | 15,0 |
| Gnomad (af) | 576 | 4 | 25, 45, 20 | 7,5 | 76% | 49 | 12,2% | 0 / 66% | 4,4 |

Crème (tuinbroek): r15 stappen 26/26, Furret-crème 25/24/33, Ursaring-geel 41/30. Grens 32/100 (Furret 29, Ursaring 33).

Per zone (r15): zonder kraag zit 22% van de vacht in vlakken <20 px (grote sprites: Bibarel 10, Ursaring 12, Swampert 12, Alphyena 27, Gnomad 24). Alleen de kraag: 71%, grens 38/100. Gen 3-koppen met vacht: Bibarel 25, Ursaring 36, Teddiursa 37.

Lezing van de getallen:
- **Tinten en contrast**: 3 vachttinten + lijn, stappen 37/37. Dat ligt binnen Gen 3 (16–41) en is gelijk aan onze sprites (Alphyena 36/37). Het palet hoeft niet bijgesteld te worden. Crème 26/26 is gelijk aan Furret. Het punt "crème te zacht" uit de vorige keuring vervalt daarmee.
- **Rust/strakheid**: r15 heeft de minste losse pixels van alle sprites (2,0/100). Zijn rust komt dus niet van middelen. De tintgrenzen zijn hard.
- **Vlekkerigheid**: buiten de kraag (22%) zit r15 tussen Ursaring/Swampert en Alphyena/Gnomad in. De kraag is de drukste zone (grens 38), maar ligt in de lijn van Gen 3-koppen met vacht (Ursaring 36, Teddiursa 37). Hij is druk door de bevroren bollen, elk met een eigen lijn. Gladder maken zou pixelblur zijn (SPRITE_KERN), dus dat is niet gedaan.
- **Lijnen**: de buitenrand aan de schaduwkant is 74% zwart (Gen 3: 39–83), aan de lichtkant 26% (Gen 3: 5–55). Er is weinig zwart in de binnenlijnen (1,4/100, Furret 1,7, Ursaring 2,4). Dat komt doordat de binnenlijnen eigen bruin b zijn. Dat is consistent, geen afwijking.

## 3. Bevindingen per zone (licht linksboven, schaduw als vorm, model als bron)
Ik heb de model-luminantie op het spriteraster geprojecteerd (`proj.py`, `model_proj_8x.png`) en elke plek in de vacht opgezocht waar een lichtere tint ónder een donkerdere ligt. Op één na volgen ze allemaal het model.
- Helm: hooglicht f linksboven, schaduw c rechts. De d-band uit het model is smal. Overslaan van f naar c is gewoon in Gen 3 (Teddiursa 58%, Ursaring 17% van de tintgrenzen; r15 5%). OK.
- Rechterarm: slagschaduw van de kraag over de schoudertop (model 107–130), hooglichtsikkel f linksboven op schouder en onderarm, c-sikkel rechts, armholte c (model 96–106). Dat volgt de bolling zoals bij Ursaring. OK.
- Linkerarm: d boven, c onder. OK.
- Dijen: links een f-sikkel linksboven en c onder. Rechts f linksboven van het midden (model 150–165) met een c-sikkel rechts en onder. Dat is geen pillow: de lichte kant (links) heeft geen donkere rand. OK. Het streepje c (45–47,48) is de schaduw onder de poot.
- Kraag/gezicht: elke bol heeft licht linksboven en donker rechtsonder. **Uitzondering: de bol onder rechts.** Daar ligt (32–34,31) d ónder de c-schaduw van (31–35,30), direct boven de onderlijn: licht van onderen. Het model is daar juist donker (L 72–88, erboven 108–113).
- Tuinbroek: C links, M midden, S rechts. Zakrand: bevroren. OK.
- Staart, potlood: bevroren, licht klopt.

## 4. Gerepareerd (`../sprite_r16/bouw.py`)
| Zone | px | Wat |
|---|---|---|
| kraagbol onder rechts | 3 | (32,31), (33,31), (34,31) d → c. De bol is nu boven licht en onder donker, zoals het model en de andere bollen. |

Er is buiten deze zone niets veranderd (diff 0, met assert bewezen). Het silhouet en de lijnpixels (K/b) zijn ongewijzigd en het palet ook (15 + transparant). De getallen van r16 zijn gelijk aan die van r15, op grens 31,7 na. Bewust níet gedaan: de kraag gladder maken, vlakken samenvoegen of tinten middelen (zou pixelblur zijn).

## 5. Oordeel: PASS (r16)
Over de hele sprite is r16 consistent met de Gen 3-vachtsprites en met onze goedgekeurde sprites. Dat geldt voor het aantal tinten, de helderheidsstappen, de losse pixels, de grootte van de tintvlakken, de lijnkleur per kant en de lichtrichting. Alle getallen liggen binnen het bereik van de referenties. Het drukste punt is de kraag, maar die zit op het niveau van Ursaring- en Teddiursa-koppen.
Ter info voor Jordi (geen fout): r15/r16 heeft minder zwart (7,4%) dan Bibarel (12,2%) en Ursaring (9,3%). Dat komt doordat de binnenlijnen bruin zijn, net als bij Furret (4,9%). Op 1× valt het niet op.

## Bestanden
- `rapport.md` (dit), `vergelijk.png` (r15 naast 11 sprites op 3× met de getallen), `blind_4x.png` (eerste blik)
- `meet.py` (alle getallen; `python3 docs/concept/sprites/bibarel_evo/keuring_r15/meet.py [r16]` vanuit de repo-root), `laad.py`, `proj.py` + `model_proj.npy`/`model_proj_8x.png` (model op het 64-raster), `modeltoon.py`, `vel_blind.py`, `vergelijk.py`
- `../sprite_r16/`: `sprite.png`, `sprite_8x.png`, `vel.png` (r16 | r15 8× gemarkeerd; kraag 16×; naast referenties 2×; 1× licht/donker), `bouw.py`
