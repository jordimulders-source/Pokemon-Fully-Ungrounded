# Eisenlijst party-icoon (en overworld) — 18 nov

Jordi: "eigenlijk moeten we een soort eisenlijst maken op basis van de al bestaande sprites, laten we eerlijk zijn, itt de battle sprites gaan mensen hier niet minutenlang naar kijken en analyseren" · eerder: iconen en overworld "moeten gewoon consistent zijn, maar hoeven eecht niet hoogstondig pixel art te gaan worden".

**Afspraak:** een icoon is af als het script alles OK geeft en de korte handmatige blik (punt 2) klopt. Geen keurrondes daarbovenop.

## 1. Automatisch (`icoon_check.py icon.png front.png`)
Normen = p10–p90 van de 385 originele Gen 1–3-iconen.
| Eis | Norm |
|---|---|
| Formaat | 32×64 (2 frames), modus P, index 0 transparant |
| Palet | precies één van `icon_palettes/pal0–5` (zand/bruin: pal2) |
| Hoogte | volgens fronthoogte (front 25→15, 35→18, 45→21, 54→22, 61→24), ±3 |
| Breedte | 16–27 |
| Onderkant / midden | y 27–30 / x 14,5–16,5 |
| Kleuren | 6–10 |
| Omlijning | dicht (≥95% van de randpixels donker); boven donkerder (index 15) dan onder (index 14) |
| Detail | donkere binnenlijnen (incl. oog) 10–26% van het oppervlak, Gen 3-mediaan 18% |
| Frame 2 | voeten op dezelfde rij, bovenkant hooguit 2 px verschoven, 10–50% anders |
| Pose | silhouet van de verkleinde front (IoU ≥ 0,55); anders alleen met reden (lange/rechtopstaande figuur) |

## 2. Handmatig (±1 minuut, op 1× tussen 4 echte iconen op groen)
- Dezelfde Pokémon: de herkenningstekens van de front staan erin (bij de viscacha: oren, gele wangpluk, getande staartpluk).
- Geen uitschieter: niet duidelijk groter, platter of feller dan de buren.

## 3. Overworld (zelfde aanpak, script volgt als het nodig is)
Normen uit 942 overworldsprites (HGSS-stijl): 192×32 (6 frames: voor 2, achter 2, opzij 2), figuur ongeveer even hoog als het icoon (0,83–1,20×), onderkant y 28–31, 9–15 kleuren in een eigen palet, zwarte omlijning rondom, loopframe even hoog als stilstaan.

## Stand viscacha-icoon
`viscacha/icoon/maker/icon_v2.png`: 13/14; alleen detail te laag (binnenlijnen 9%, minimum 10%, mediaan 18%).
