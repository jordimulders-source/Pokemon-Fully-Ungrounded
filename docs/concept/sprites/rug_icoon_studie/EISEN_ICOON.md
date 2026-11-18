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
- **Alles iets boller/ronder** (Jordi: "ik merk dat alles een beetje bolliger/ronder is"; klopt met de gladdere, compactere omtrek, 0,44–0,91): kop, romp, dijen voller en ronder dan bij gewoon verkleinen.

**Wat niet mag:**
- Iets toevoegen dat niet in het ontwerp zit.
- Herkenningstekens laten vallen: die blijven, desnoods groter (Zangoose' rode litteken, Seviper's gele vlekken, Swellow's rode gezicht, Gardevoir's rode hoorn, Pikachu's rode wangen).
- Het gezicht of de oogstijl veranderen.
- Een vlakke "zak" zonder binnenvlakken: onder 10 vlakken leest een icoon als silhouet.

## 1c. Vanilla Gen 1–3, in-game set en fanmade Gen 9 (`icoon_groepen.py`; Jordi: "kijk ook naar hoe gen 9 iconen het doen, die zijn fanmade en maken complexe designs simpel, vergelijk deze met de 386 die vanilla zijn, dan zie je wat je eventueel kan smokkelen ook")
**Let op:** de game toont niet de originele GBA-iconen maar de **in-game set** (`icon.png`, `P_GBA_STYLE_SPECIES_ICONS = FALSE`): bijgewerkte iconen in DS-poses (Sentret op zijn staart, Raticate anders), `9_ingame_iconen_gen3.png`. Onze iconen staan daartussen. Gen 9 (`8_gen9_fanmade_iconen.png`) is door fans gemaakt in dezelfde stijl.
| Maat (p10 / mediaan / p90) | vanilla 1–3 (387) | in-game 1–3 (425) | fanmade Gen 9 (102) |
|---|---|---|---|
| hoogte | 16 / 20 / 22 | 17 / 21 / 25 | 16 / 22 / 28 |
| breedte | 16 / 21 / 27 | 16 / 22 / 29 | 16 / 22 / 30 |
| oppervlak (px) | 177 / 242 / 352 | 181 / 271 / 395 | 180 / 311 / 469 |
| kleuren | 6 / 8 / 10 | 7 / 9 / 11 | 7 / 9 / 11 |
| binnenlijnen / oppervlak | 0,10 / 0,18 / 0,26 | 0,09 / 0,16 / 0,25 | 0,10 / 0,15 / 0,24 |
| kleurvlakken | 10 / 18 / 28 | 11 / 20 / 32 | 14 / 25 / 42 |
| gaten | 0 / 0 / 2 | 0 / 0 / 2 | 0 / 0 / 3 |
| frame 2 anders | 0,12 / 0,31 / 0,51 | 0,13 / 0,31 / 0,50 | 0,17 / 0,39 / 0,52 |
| omlijning dicht | ja | ja | ja |

**Wat Gen 9 smokkelt (en dus mag, want het staat al in de game):**
- **Groter:** tot ±28 hoog en 30 breed, en een kwart meer oppervlak; complexe ontwerpen vullen het vak.
- **Detail via kleurvlakken in plaats van lijnen:** ±25 vlakken (tot 42) bij iets minder binnenlijnen (15%). Een complex ontwerp (Kingambit, Skeledirge, Tinkaton) houdt al zijn kleurzones, maar elk als klein vlakje.
- **Meer kleuren** (9–11) binnen hetzelfde gedeelde palet, ook als die "fout" zijn (Pawmot oranje, Kingambit geel).
- **Frame 2 mag meer bewegen** (39%: kop draaien, armen anders, Farigiraf's staartkop).
- **Wat Gen 9 níet doet:** de omlijning openlaten, nieuwe kenmerken toevoegen, of een complex ontwerp tot een kale vorm terugbrengen.

**Gevolg voor onze normen:** maatgevend is wat de speler ziet: de in-game set, met Gen 9 als ruimste grens. Het script gebruikt nu: kleuren 6–11, binnenlijnen 0,09–0,26, kleurvlakken 10–42.

## 1d. Hoekig of rond (`hoekig_meet.py`; Jordi over v3: "hij is nog steeds erg hoekig he")
| (p10 / mediaan / p90) | in-game 1–3 | Gen 9 | vanilla GBA | viscacha v3 |
|---|---|---|---|---|
| rechte randstukken (≥ 4 px recht) | 0,00 / 0,12 / 0,27 | 0,05 / 0,16 / 0,29 | 0,07 / 0,22 / 0,36 | **0,39** |
| diagonale trapjes per 100 randpixels | 47 / 55 / 62 | 46 / 53 / 62 | 43 / 50 / 58 | **40** |
Echte iconen hebben bijna geen rechte stukken van 4 px of langer: de omtrek loopt in schuine stapjes (1-1, 1-2, 2-1). Eis in het script: rechte stukken ≤ 0,27, trapjes ≥ 46.

## 1e. Strengere ontwerpregels en smokkelruimte (Jordi: "kijk ook naar pokemon in vergelijkbare poses en ga nog strenger kijken naar design regels" · "en vooral ook waar je mag smokkelen" · "wederom kijk bij bijv gen 9 pokemon" · "met complexe ontwerpen")
Bekeken: 20 kleine viervoeters in de in-game set (`10_poseburen_viscacha.png`: Raticate, Rattata, Eevee, Glameow, Purrloin, Meowth, Pachirisu, Minccino, Pawmi, Nickit, Rockruff, Litten, Persian, Electrike, Dachsbun, Yungoos, Bunnelby, Skwovet, Sandshrew, Zigzagoon) en complexe Gen 9-ontwerpen (`8_gen9_fanmade_iconen.png`, `11_gen9_complex_klein.png`).

**Regels (streng; elk icoon hierop nalopen):**
1. **Kop groot: ±40–50% van de figuur** bij kleine zoogdieren (Eevee, Rattata, Pachirisu, Minccino, Litten, Rockruff); het lijf is kort. Dit is de grootste chibi-stap, groter dan "iets groter".
2. **Ogen groot en leesbaar:** 2–3 px hoog, donker met 1 lichte pixel; het gezicht kijkt naar de kijker (driekwart).
3. **Poten zijn stompjes** van 2–3 px breed met een donkere teenlijn; meestal 2–3 zichtbaar, de verre donkerder. Een opgeheven poot is een rond wantje (Rockruff, Purrloin), geen blokje.
4. **Staart groot en eenvoudig:** één heldere vorm in twee tonen, vaak omhoog achter het lijf (Pachirisu, Eevee, Glameow, Minccino); het herkenningsteken aan het eind (pluim) groot.
5. **Omtrek rond:** schuine stapjes, geen lange rechte randen (§1d).
6. **Elke kleurzone van het ontwerp blijft**, desnoods als vlakje van 2–4 px (Gen 9: Kingambit, Skeledirge, Grafaiai).

**Smokkelruimte (mag, want staat al in de game):**
- **Pose aanpassen** naar een compacte, dynamische houding (springend/lopend naar links) als de front-pose op 20 px niet leest (Persian, Litten, Raticate, Rockruff wijken af van hun front).
- **Ledematen samenvoegen of weglaten** als ze niet lezen: Spidops' poten worden stompjes, Lokix' ledematen ingeklapt, Cyclizar's lijf klein achter een grote kop.
- **Proporties chibi** (kop tot de helft), lijf en poten korter.
- **Kleur flink laten verschuiven** naar het icoonpalet (Maschiff oranje, Mabosstiff roze, Greavard blauw).
- **Groter** tot ±25–28 hoog bij brede of complexe ontwerpen.
- **Herkenningsteken overdrijven** (Tinkaton's hamer, Kingambit's kroon, Dachsbun's staart).
- **Frame 2** mag kop/staart duidelijk bewegen.

- Jordi: "handige poses, dingen wegstoppen, zolang het maar consistent is en niet raar eruit ziet": een pose kiezen die makkelijk leest en lastige delen achter het lijf laten verdwijnen mag.

**Nooit:** kenmerken toevoegen, een herkenningsteken laten vallen, het gezicht/de oogstijl veranderen, de omlijning openlaten.

## 2. Handmatig (±1 minuut, op 1× tussen 4 echte iconen op groen)
- Dezelfde Pokémon: de herkenningstekens van de front staan erin (bij de viscacha: oren, gele wangpluk, getande staartpluk).
- Geen uitschieter: niet duidelijk groter, platter of feller dan de buren.

## 3. Overworld (zelfde aanpak, script volgt als het nodig is)
Normen uit 942 overworldsprites (HGSS-stijl): 192×32 (6 frames: voor 2, achter 2, opzij 2), figuur ongeveer even hoog als het icoon (0,83–1,20×), onderkant y 28–31, 9–15 kleuren in een eigen palet, zwarte omlijning rondom, loopframe even hoog als stilstaan.

## Herkenbaarheid eerst vastleggen
Jordi over viscacha v4: "kijk het type ontwerp is uitstekend, dit is super consistent met de andere sprites, alleen je herkent de viscacha niet goed meer terug." Les: de stijlregels (§1e) maken elk knaagdier gelijk. Daarom vóór het icoon per soort de **herkenningstekens van de front** opschrijven (vorm én maat: "lange rechtopstaande oren dicht bij elkaar", niet alleen "oren") en die in het icoon minstens even groot houden als bij verkleinen, liever overdreven. Handmatige toets: zou je de soort op 1× tussen de buren aanwijzen?

## Complexe ontwerpen
Jordi: "we hebben namelijk ook een aantal complexe designs en die moeten we ook kunnen omzetten". De smokkelregels van §1e zijn daarvoor bedoeld (naar Gen 9: Kingambit, Skeledirge, Tinkaton, Spidops, Grafaiai). Na de viscacha de werkwijze testen op één complex ontwerp (voorstel: spooktrein fase 3 of Krassault).

## Stand viscacha-icoon
`viscacha/icoon/maker/icon_v2.png`: 13/14; alleen detail te laag (binnenlijnen 9%, minimum 10%, mediaan 18%). Vorm: 13 kleurvlakken (norm 10–28, mediaan 18), 0,20 van de front (aan de lage kant), silhouet 0,60 (goed), 0 gaten.
