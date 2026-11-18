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

## 1b. Hoe simpel t.o.v. de front (`vorm_meet.py icon.png front.png`; Jordi: "ook qua vormen misschien nog, van hoe simplistisch zijn de iconen tov de sprites" · "wat mag wel wat mag niet")
Gemeten over 385 Gen 1–3-iconen (p10–p90, mediaan):
| Maat | Norm | Betekenis |
|---|---|---|
| kleurvlakken in het icoon | 10–28 (18) | aantal losse vlakjes van één kleur (≥ 2 px), zonder omlijning |
| vlakken icoon / front | 0,18–0,48 (0,29) | het icoon houdt ongeveer een derde van de vlakken van de front |
| silhouet-grilligheid icoon / verkleinde front | 0,44–0,91 (0,66) | de omtrek is gladder en compacter dan bij gewoon verkleinen |
| gaten (doorkijkjes) | 0–2 | gaten in de front worden meestal dichtgemaakt |

**Wat mag** (Game Freak doet het, zie `5_icoon_vs_front.png` en `7_icoon_vs_front_vereenvoudiging.png`):
- Een lange, hoge of uitgespreide figuur compacter neerzetten (Gardevoir opgerold, Milotic gekruld, Flygon vleugels dicht, Breloom gehurkt). Een compacte front houdt zijn pose.
- De kop iets groter maken (Absol, Pikachu, Breloom, Kecleon).
- Lange delen inkorten (Swellow's staartveren, Seviper's staart), dunne delen dikker maken (minstens 2 px).
- Kleine details weglaten (vleugeladers van Ninjask, losse vachtplukjes, klauwtjes), doorkijkjes dichtmaken.
- Kleur laten verschuiven naar het icoonpalet (Wailord paars, Milotic rozer).

- **Wel moet: vormen blijven vormen** (Jordi: "vormen probeert die nog wel wat van te maken he ipv vierkantjes" · "dus dat is nog een goede wel"): ronde delen rond, met schuine stapjes en curven zoals in de front; geen blokjes, rechte randen of rechthoekige vlakken waar het dier rond is.

**Wat niet mag:**
- Iets toevoegen dat niet in het ontwerp zit.
- Herkenningstekens laten vallen: die blijven, desnoods groter (Zangoose' rode litteken, Seviper's gele vlekken, Swellow's rode gezicht, Gardevoir's rode hoorn, Pikachu's rode wangen).
- Het gezicht of de oogstijl veranderen.
- Een vlakke "zak" zonder binnenvlakken: onder 10 vlakken leest een icoon als silhouet.

## 2. Handmatig (±1 minuut, op 1× tussen 4 echte iconen op groen)
- Dezelfde Pokémon: de herkenningstekens van de front staan erin (bij de viscacha: oren, gele wangpluk, getande staartpluk).
- Geen uitschieter: niet duidelijk groter, platter of feller dan de buren.

## 3. Overworld (zelfde aanpak, script volgt als het nodig is)
Normen uit 942 overworldsprites (HGSS-stijl): 192×32 (6 frames: voor 2, achter 2, opzij 2), figuur ongeveer even hoog als het icoon (0,83–1,20×), onderkant y 28–31, 9–15 kleuren in een eigen palet, zwarte omlijning rondom, loopframe even hoog als stilstaan.

## Stand viscacha-icoon
`viscacha/icoon/maker/icon_v2.png`: 13/14; alleen detail te laag (binnenlijnen 9%, minimum 10%, mediaan 18%). Vorm: 13 kleurvlakken (norm 10–28, mediaan 18), 0,20 van de front (aan de lage kant), silhouet 0,60 (goed), 0 gaten.
