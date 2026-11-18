# Eisenlijst party-icoon (en overworld) — 18 nov

Jordi: "eigenlijk moeten we een soort eisenlijst maken op basis van de al bestaande sprites, laten we eerlijk zijn, itt de battle sprites gaan mensen hier niet minutenlang naar kijken en analyseren" · eerder: iconen en overworld "moeten gewoon consistent zijn, maar hoeven eecht niet hoogstondig pixel art te gaan worden".

**Jordi ziet pas een af-versie (18 nov):** "ik wil pas een versie zien als die echt af is, dus geen losse pixels, een icoon die net zo goed is als degene die al in de game zitten, daar heb je nu alle tools voor". Interne lus: maker → script → Claude op 8× naast echte iconen → verse keurder (streng, eis 0 eerst) → reparaties → pas dan Jordi. Alleen echte keuzes (zoals A/B/C) eerder.

**Afspraak:** een icoon is af als het script alles OK geeft en de korte handmatige blik (punt 2) klopt. Geen keurrondes daarbovenop.

## Stand 18 nov: iconen geparkeerd
Jordi: "want het is nog steeds compleet giswerk waar ik van alles moet verbeteren" · "dus we zijn al uren geen stap verder". Na ±12 rondes (Gemini, verkleinen, handwerk, chibi-model, onderdelen-methode) geen icoon dat af is. Wat werkte: onderdelen-methode voor lijf/verhoudingen/plaatsing (a2), de eisenlijst als maat. Wat niet werkte: kleine kenmerken in de kop (oog, kraag, wang) laten ontstaan door verkleinen of door makers; dat is herontwerpen in het klein, en dat kunnen wij niet zonder Jordi's krabbel. Iconen staan stil tot de fase voor alle soorten; dan eerst een nieuwe aanpak voor het gezicht bedenken, niet dezelfde rondes herhalen. Jordi: "iconen zijn minder belangrijk maar ze moeten wel herkenbaar zijn" (de ondergrens blijft eis 0).

## Voorstel na overleg met een agent (18 nov): vormpunten
Map `advies_vormpunten/` (scripts + vellen). Kern: elke pixel in het gezicht komt uit (a) hoekpunten die Claude op de front afleest (kop, oren, kenmerken als polygonen), (b) vaste, eenmaal goedgekeurde bouwstenen (oog-types) of (c) vaste rasterregels; het lijf blijft de onderdelen-methode. Jordi keurt de vormpunten op frontmaat (`vormpunten_vel.png`) en kiest uit factorvarianten; feedback gaat naar een punt of factor, nooit naar pixels. Letterlijk een krabbel rasteren mislukt (`k_0.3.png`); een krabbel is een vormopdracht. Proef: `kv3b.png` (gesloten kop, leesbaar oog, geen blur; nog niet af: schaduw, binnenlijnen, kraag-zigzag, frame 2). Jordi: aantal nieuwe iconen "correct, misschien max 200". Over de proef kv3b: "Rechts is wel de minste van de hele lijst he, staart, poten, lichaam zijn ok, maar het hoofd is nog lang niet goed." → vormpunten-proef bewijst nog niets voor het hoofd.

## Lessen viscacha-icoon in één lijst (afvinken bij elk nieuw icoon en elke ronde)
Jordi (18 nov): "het zou zonde zijn als je weer alles compleet anders gaat doen dan eerst, dus probeer die lessen mee te nemen".
1. Lijkt op de front: vormen en gebaren uit de front, niets verzinnen (eis 0).
2. Werkwijze: onderdelen van de front apart verkleinen met vaste factoren (`viscacha/icoon/onderdelen/bouw2.py`); feedback = factor aanpassen, varianten naast elkaar.
3. Aanhechtingen vast: oren op de kop, poten aan het lijf; niets zweeft ("1 oor vliegt ook").
4. Oog = opbouw van de front, kleiner: viscacha = zwart blok met 1 witte glanspixel in de bovenste rij + bruin ooglid; nooit andersom (wit met zwarte pupil), nooit het oog van een andere soort.
5. Oog op de plek van de front: viscacha = direct naast de wang (gele pluk), kleiner dan in de front ("het oog zit naast de wang maar kleiner"); plek berekenen met de transformatie, niet gokken.
6. Geen pixelblur en geen losse pixels: elk cluster een bewuste vorm; zelf op 8× naast in-game iconen kijken.
7. Snorharen 1 px dun; geen strook van 2 px.
8. Rond waar het dier rond is, punten puntig; poten als stompjes 2–3 px; buik naar verhouding kleiner ("enorme buik").
9. Herkenningstekens groot: lange oren dicht bij elkaar, snuit naar linksonder, elektrisch motief op wang en nek getand geel, opgeheven voorpoot, ronde dij, staart.
10. Wat goed is blijft staan (viscacha: de staart van v8, pixel voor pixel; stijl van v4). "niet koppig doen, niet opnieuw tekenen" (Jordi): alleen poetsen en benoemde punten repareren.
11. Hoek: echt diagonaal zoals Rattata/Dedenne.
12. Jordi ziet pas een af-versie (alleen echte keuzes eerder).
13a. Kleine details hoeven niet perfect (Jordi over de wangplukken: "bij zulke dingen gaat herkenbaarheid over detail"): aanwezig en op de goede plek is genoeg; de grote vormen (kop, snuit, oren, oog) moeten wel kloppen. Jordi: "herkenbaarheid zit hem vaak in het hoofd en aanwezigheid van belangrijke features" · "bijv kadabra zonder lepel is geen kadabra, drowzee zonder snuit ook niet, poliwag zonder roze neus is geen poliwag, wooper zonder blij gezicht en 2 takjes op zijn hoofd is geen wooper, sudowoodo zonder groene ballen is geen sudowoodo". Per soort vóór het icoon 2–4 **onmisbare kenmerken** opschrijven (viscacha: lange oren, slaperig oog, gele kraag en wangpluk, staart met vlampluim); die moeten duidelijk te zien zijn, de rest mag eenvoudig.
13b. Keuzes tussen kenmerken: kijk wat bestaande iconen doen (Jordi: "kijk vooral naar wat de andere iconen doen wanneer er gekozen moet worden tussen bepaalde features"). Snorharen: zie 13c (korte lijntjes buiten het silhouet blijven, over het lijf verdwijnen).
13c. Gepaarde kenmerken aan één kant (Jordi: "zijn er pokemon waar een feature aan 1 kant wordt weggelaten en aan de andere kant niet?"; `14_eenzijdige_kenmerken.png`): ja. Pikachu, Raichu, Pachirisu en Emolga tonen in hun front twee wangen, in het icoon (meer van opzij) maar één. Wat aan de verre kant achter de kop valt, verdwijnt. Snorharen (op 8× bekeken, `17_snorharen_8x.png`; Jordi: "raticate en dedenne behouden ze juist"): Raticate, Dedenne, Rattata en Persian houden korte snorhaarlijntjes van 1 px die BUITEN het silhouet voor de snuit uitsteken, in de donkere lijnkleur; snorharen over het lijf verdwijnen. (Eerdere conclusie "laten ze weg" was fout: op 4× gekeken.)
13d. Gekleurde vlekken binnen het silhouet (wangen, kragen, strepen; `15_geel_gba.png`, `16_geel_latere_gens.png`; Pikachu, Raichu, Plusle, Manectric, Jolteon, Dedenne, Pachirisu, Emolga, Togedemaru, Toxtricity, Sandy Shocks): **geen donkere lijn binnenin**, de vlek ligt direct tegen de lijfkleur; alleen waar ze de buitenrand raakt krijgt ze de gewone omlijning. Maat: kleine compacte blokjes van 2–6 px (Pachirisu-wang 4 px, Dedenne ±6, Emolga 3–4), dunne vormen uit de front worden 1–2 px brede vlekken; de precieze vorm doet er weinig toe (Jordi: herkenbaarheid zit niet in dat detail).
13e. Elementen die in de front al 1 px dun zijn (Jordi: "kijk vooral naar elementen die in de frontsprite al heel klein zijn" · "de snorharen zijn al 1 pixel breedte, itt dedenne en raticate"; `18_kleine_details.png`, front 4× naast icoon 8×): Meowth, Persian en Glameow (snorharen van 1 px) houden 1–3 korte stompjes van 1 px in de lijnkleur, buiten het silhouet voor de snuit; over het lijf verdwijnen ze. Cutiefly houdt dunne antennes als 1-px lijntje; Venonat maakt zijn dunne antennes juist dikker (2 px, overdreven) omdat ze een herkenningsteken zijn. Buizel en Skitty laten fijne details weg. Regel: 1-px details worden kort (1–3 px), blijven 1 px dun in de lijnkleur, alleen buiten het silhouet; alleen een onmisbaar kenmerk wordt verdikt.
13f. Drukke ontwerpen met veel overlap (Jordi: "zoek naar sprites die druk zijn en waar veel overlap is"; `19_drukke_ontwerpen.png`: Lucario, Greninja, Zoroark, Infernape, Decidueye, Incineroar, Kingambit, Grimmsnarl, Hydreigon): overlappende kleine delen smelten samen tot één massa (Hydreigons koppen en vleugels, Decidueyes kap); het herkenningsteken blijft als groot kleurvlak (Greninjas tongsjaal, Kingambits kroon, Infernapes vlam, Zoroarks manen); dunne lijnen en linten óver het lijf (Lucario's borststekel, Decidueyes koord, Kingambits linten) verdwijnen of worden een paar losse kleurpixels; patronen worden 1–2 px vlekjes (Greninja wit, Incineroar strepen); kleur schuift mee naar het palet.
13h. Dragapult-lijn (Jordi: "hoe doet dragapult het bijv"; `21_dragapult.png`): de dunne roze strepen over borst en kop (in de front 1–2 px, over andere delen heen) blijven in het icoon als korte streepjes en vlekjes van 1–2 px in hun eigen kleur (roze), niet weggelaten en niet in de lijnkleur; de overlappende koppen/Dreepy's smelten samen, hun gele ogen blijven als gele blokjes.
13i. Sinistcha/Poltchageist (Jordi: "en sinistcha"; `22_sinistcha.png`; kleuren op het vel volgen het icoonpalet en kunnen afwijken): Sinistcha's dunne theedraden over het groene lijf blijven als een paar korte strengen van 1–2 px in hun eigen (gele) kleur; Poltchageist's fijne krul op de kom wordt een vereenvoudigd patroon van 2 px dik, de dunne druppels verdwijnen grotendeels.
13g. Jordi na eigen zoektocht: "blijkbaar zijn er geen pokemon met 1 sprite dikke features" (over het lijf). Er is dus geen vergelijkingsmateriaal; voor de viscacha blijft de keuze van a9: rechtersnorharen over de borst weg, links kort. Eerdere notitie, alleen ter naslag: dunne lijnen die over het lijf lopen (overlap; `20_overlap_dunne_lijnen.png`; Jordi: "overlap"): Whiscash (gele snorharen, één krult over het lijf), Barboach, Dewott (witte snorharen aan beide kanten, ook over het lijf), Samurott (witte snor over de borst): de lijn BLIJFT, 1 px dik, in zijn EIGEN kleur die contrasteert met het lijf (geel, wit), niet in de donkere lijnkleur. Zo leest hij als snorhaar en niet als omlijning. (Les a8: rechtersnorharen in donkergrijs over de borst werden een donkere vlek; de fout was de kleur, niet de aanwezigheid.)
13. Schaduw en kleur (Jordi: "schaduw en kleur zijn ook belangrijk he, vergeet de lessen niet die we eerder vandaag hadden opgesteld"): niet "plat van kleur"; pal2 heeft maar 2 zandtinten, dus diepte = verre delen bruin, nabije licht, licht linksboven en schaduw rechtsonder per deel; detail met donkergrijze binnenlijnen (±15%) en ±20 kleurvlakken; omlijning boven index 15, onder 14; geel motief in goud (8) met geel (9) als licht; bef rond met lichte rand.

## Rekenen, niet schatten (Jordi, 18 nov: "de wiskunde is ontzettend belangrijk voor het icoon")
Elke maat en plek in het icoon volgt uit een meting: aandeel van een kenmerk in de kop of het lijf in de front (bijv. viscacha-wangpluk 3,8% van de kop, kraag 9,9%), de plek berekend via de transformatie, en de factoren uit de meetstudie op bestaande iconen (`verhoudingen/STUDIE_VERHOUDINGEN.md`). Opdrachten aan makers geven doelgetallen; rapporten melden de gemeten waarden. Jordi: "het is een combinatie van de sprite, maar ook de studie van wat gamefreak/de poke-emerald decomp gasten doen met de sprites naar icoon": maten uit onze front × de regels uit de meetstudie (kop ×1,25, lijf ×0,95, oog verschuift niet binnen de kop, minimummaten voor kleine delen). Marge (Jordi: "je mag natuurlijk een marge aanhouden omdat niet elke pokemon dezelfde vorm heeft"): de p25–p75-spreiding uit de studie is de marge; binnen die marge kiezen naar wat het best op de front lijkt.

## 0. BELANGRIJKSTE EIS: hij lijkt op de echte Pokémon
Jordi (18 nov): "dat is het belangrijkste van de hele eisenlijst, hij moet lijken op de echte pokemon". Alle andere eisen komen hierna. Het icoon is de front (onze goedgekeurde sprite) in het klein: kopvorm, gezicht, oren, kenmerken en kleurverdeling overgenomen, niet bedacht. Toets als eerste: leg het icoon naast de verkleinde front; vorm voor vorm moet het hetzelfde zijn, alleen eenvoudiger. Een icoon dat alle scriptpunten haalt maar niet op de front lijkt, is afgekeurd (viscacha v5).

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

- **Kopvorm uit de front, niet bedenken** (viscacha v5, Jordi: "de rest van het hoofd is volledig verknald, vergelijk het maar met het model qua vorm, totaal anders"): de kop van het icoon is de kop van de front verkleind (eventueel met een grotere factor dan het lijf voor de chibi-maat), daarna alleen opgeschoond.

- **Puntige delen** (`12_puntige_koppen.png`: Inkay, Sharpedo, Kingdra, Seadra, Kabutops, Malamar; Jordi over Krassault: "het hoofd mag iets puntiger denk ik"): een punt blijft een punt, zo lang als in de front of langer. De randen lopen als rechte 45°-diagonaal (trapjes van 1-1) naar een tip van 1 px; niet afronden. De tip krijgt vaak een lichte pixel. Ronde delen rond, puntige delen puntig: het ronder maken (§1e) geldt niet voor punten.

- **Geen pixelblur ingezoomd** (viscacha v7, Jordi: "van een afstandje lijken ze ok, maar als je inzoomt wordt het pixelblur"): elk cluster is een bewuste vorm; ogen en kleine koppen als schoon cluster in de vorm van ONZE front (niet het oog van een andere soort: Jordi, "dat is een totaal ander oog"); een echt icoon mag alleen laten zien hoe zo'n oog op icoonmaat in pixels wordt opgebouwd, nooit de verkleiningsresten laten staan. Altijd zelf op 8× kijken vóór het naar Jordi gaat.
- **Oog: hetzelfde idee, kleiner** (Jordi, viscacha: "De viscacha heeft een zwart oog met een witte pixel erin ... Dus kleiner, maar hetzelfde idee"): bepaal eerst de opbouw van het front-oog (wit oog met pupil, of donker oog met lichtpuntje; ooglid; kleur) en houd die opbouw in het icoon.
- **Hoek: echt diagonaal** (Jordi: "kijk hoe rattata en dedenne bijv echt diagonaal staan"): driekwartstand, lijf schuin naar de kijker, kop naar voren-links.

- **Herkenbaar = dezelfde gebaren, niet dezelfde verhoudingen** (Jordi over de viscacha-staart: "de staart is perfect omdat de manier waarop die krult onmiskenbaar dezelfde manier is, de verhouding is niet hetzelfde, maar hij is herkenbaar"): neem per onderdeel de lijn/het gebaar van de front over (hoe iets krult, buigt, waar het oog zit, hoe de oren staan); de maat mag chibi worden.
- **Anatomie (Jordi):** "een nek wordt nog wel eens weggehaald, poten verkleind, een buik wordt naar verhouding kleiner, maar hij is ontzettend herkenbaar, wat de pokemon uniek maakt blijft telkens goed te zien".
- **Krabbel van Jordi als vormkaart** (viscacha v8): hij tekent de vormlijnen van de front over het icoon; die lijnen zijn de opdracht.

## Complexe ontwerpen
Jordi: "we hebben namelijk ook een aantal complexe designs en die moeten we ook kunnen omzetten". De smokkelregels van §1e zijn daarvoor bedoeld (naar Gen 9: Kingambit, Skeledirge, Tinkaton, Spidops, Grafaiai). Na de viscacha de werkwijze testen op één complex ontwerp (voorstel: spooktrein fase 3 of Krassault).

## Stand viscacha-icoon
`viscacha/icoon/maker/icon_v2.png`: 13/14; alleen detail te laag (binnenlijnen 9%, minimum 10%, mediaan 18%). Vorm: 13 kleurvlakken (norm 10–28, mediaan 18), 0,20 van de front (aan de lage kant), silhouet 0,60 (goed), 0 gaten.
