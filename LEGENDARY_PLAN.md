> **Jordi (6 okt): legendaries voorlopig gepauzeerd** ("daar bedenken we wel iets voor, alles op zijn tijd"). Wél: Type: Null (Devon) en Magearna (Colress) als gifts, het **Tapu-eiland**, en **Cresselia op een nieuw eiland**. De rest wacht.

# LEGENDARY_PLAN: alle Pokémon verkrijgbaar (6 okt 2026)

Bronnen: `DEX_ANALYSE.md` (99 niet-verkrijgbaar), `KAART_REVIEW.md`, `ZEE_PLAN.md`, `TODO.md`, CHANGELOG (v0.8.120-125, v0.9.18/22). Dit is een voorstel; niets gebouwd.

## Uitgangspunten
- **De soorten zitten al in de ROM** (graphics + kreten; zie DEX_ANALYSE sectie 6). Verkrijgbaar maken kost alleen kaarten, scripts en intro's: kaart 5-15 KB, eigen intro 2-30 KB (herbruik per gezin met een ander palet).
- **Blauwdruk** = de bestaande post-game events: vaste ontmoeting (geen rondzwervers), na de Hall of Fame, `FLAG_HIDE_*` + één `VAR_*`-teller per cluster (flags: ±145 vrij, dus zuinig bundelen), debugmenu-regel "Legendary", teksten Engelse placeholders in huisstijl, eigen intro + thema (bestaand thema's hergebruiken). Bouwscript per kaart in `tools/grounded/maptools/`.
- **Immersie:** geen beeld/verwijzing naar een legendary die niet in de game zit; elk gebied past bij het element of de lore van zijn bewoner.
- **QoL:** geen verzamelminigames. Wat in de bronspellen een jacht was (Zygarde-cellen, 17 platen, wachten op weer) wordt zichtbaar en kort: 8-10 zichtbare cellen, platen optioneel.
- **Ruimte-tijdgrot:** Jordi ontwerpt die zelf (Dialga/Palkia, welke warps). Groepen die daar logisch bij horen staan hieronder als "via de ruimte-tijdgrot (Jordi)", zonder invulling.
- **Kaartgroep:** `gMapGroup_Grounded` heeft 53 van 128 plekken; ruim genoeg voor ±40 nieuwe kaarten.
- **ROM:** 32 MB minus `__rom_end` (0x09cff544) = ±3,0 MB vrij. Dit hele plan kost grofweg 1,0-1,4 MB.

## Per groep
Formaat: **Plek** / **Wanneer** / **Event** / **Maat + ROM** / **Intro**.

### 1. Kanto-vogels (Articuno, Zapdos, Moltres) - in Hoenn, elk in zijn eigen biome
- **Plek:** Moltres op de krater boven Mt. Chimney (top bestaat al); Zapdos in de Thunder Plains-Safarizone (op slot tot `FLAG_SAFARI_ZONES_OPEN`); Articuno in Ashfrost, een ijsgrot naast Crystal Cavity (Route 136, koude kant).
- **Wanneer:** post-game (Hall of Fame), Zapdos ook pas na de Rocket-quest.
- **Event:** elke vogel zit op een duidelijke "nest"-plek met een droge hint van een NPC (Moltres: een toerist die "zijn" vlam bewaakt; Zapdos: een bliksemafleider die zichzelf op een bord Zapdos noemt). Vast gevecht lv 70, geen Safari-regels.
- **Maat/ROM:** S, 3 mini-kaarten of hergebruik, ±45 KB. **Intro:** één transitie "vleugelslag" met 3 paletten (vuur/ijs/bliksem), ±12 KB.

### 2. Galar-vogels + Crown Tundra (zie groep 8)
Galar-vormen alleen in het speciale gebied (Ashfrost-noord), zie hieronder.

### 3. Celebi
- **Plek:** Petalburg Woods: nieuw Ilex-achtig schrijn achter Toadstool Hollow (kleine kaart, eigen palet).
- **Wanneer:** post-game, overdag.
- **Event:** een houthakker met een gedeukte zaag vertelt dat het bos "elke dag een beetje jonger wordt". Je loopt door een lus van drie schermen die steeds in een ander tijdperk staan (palet-wissel, geen puzzel); Celebi lv 70 bij het schrijn.
- **Maat/ROM:** S, 1-2 kaarten, ±20 KB. **Intro:** groene tijdgolf, ±10 KB.

### 4. Meertrio (Uxie, Mesprit, Azelf), Dialga/Palkia, Arceus, Area Zero (paradoxen, Koraidon/Miraidon, Terapagos)
**Via de ruimte-tijdgrot (Jordi).** Niet uitgewerkt. (Cresselia en Giratina-link: zie groep 5 en bestaande omgekeerde Sky Pillar.)

### 5. Cresselia
- **Plek:** nieuw eilandje "Fullmoon Island" in West-zee (Town Map rij 11-13, x 1-3, naast Nothing Island), vanaf Route 105.
- **Wanneer:** post-game, 's nachts (`IsNightTime` bestaat), na Darkrai.
- **Event:** na Darkrai geeft de graf-NPC op Mt. Pyre een Lunar Wing; die laat 's nachts een steiger bij Route 105 verschijnen. Een klein eiland met een rustige maanlichtvijver; Cresselia lv 70. Humor: een kampeerder met een zaklamp is "al drie nachten wakker, geen idee waarom".
- **Maat/ROM:** S, 1 kaart (Southern Island-kopie), ±15 KB. **Intro:** halve maan die omhoog zwaait, herbruik Darkrai-rook in licht, ±8 KB.

### 6. Swords of Justice (Cobalion, Terrakion, Virizion) + Keldeo
- **Plek:** drie verborgen kamers (kopie Regi-grotlayout): Cobalion in Granite Cave (diepste kamer), Terrakion in Victory Road (extra kamer), Virizion in Mangrove Mire. Keldeo in de Kubfu-dojo (Route 112), na de drie.
- **Wanneer:** post-game.
- **Event:** de dojo-meester vraagt "drie ridders" te vinden: elk wacht in een kamer met een steen met zwaardkerf; elk vecht met eerbiedige onzin ("duel, niet gevecht"). Keldeo is hun leerling in de dojovijver, en weigert zonder alle drie (je krijgt een Secret Sword van de meester).
- **Maat/ROM:** M, 3 kamers + dojo-uitbreiding, ±50 KB. **Intro:** gedeelde zwaardslag (4 paletten), ±10 KB.

### 7. Forces of Nature (Tornadus, Thundurus, Landorus) + Enamorus
- **Plek:** Weather Institute (Route 119) krijgt een dak ("windmeetpost"); Reveal Glass van Mirage Island; Enamorus op een klifschrijn op Route 122 (nu leeg).
- **Wanneer:** post-game.
- **Event:** de Weather-prof laat drie "stormcellen" op het dak los (experiment mislukt): Tornadus, Thundurus, Landorus als drie opeenvolgende gevechten, lv 70. Het Reveal Glass (Mirage Island, gratis zodra er een Wynaut-leraar is) zet ze in Therian-vorm. Enamorus: pas na de drie, een steiger/pad op Route 122 naar een schrijn met een lege ruimte; ze verschijnt als de andere drie zijn "gespiegeld".
- **Maat/ROM:** M, 2 kaarten + dak, ±40 KB. **Intro:** windvlaag/storm met 3 paletten, ±12 KB.

### 8. Crown Tundra (Ashfrost-noord): Galar-vogels, Kyurem, Zacian, Zamazenta, Eternatus, Calyrex, Spectrier
- **Plek:** uitbreiding noordelijk van Ashfrost (nieuwe kaarten, snow-tileset, ±5 kaarten); Town Map bestaande Ashfrost-vakken.
- **Wanneer:** na de Regigigas-tempel, post-game.
- **Event:** een Ashfrost-smid en zijn dochter hebben twee verroeste voorwerpen (Rusted Sword/Shield): zodra je ze door de Crown Shrine gewassen hebt komen Zacian en Zamazenta (twee gevechten). Bij zonsondergang valt een meteoriet in het noordelijke dal (de Darkest Day): Eternatus lv 75 (post-game, geen Spire-versie). Kyurem in een "Giant Chasm"-grot (na Reshiram en Zekrom, zie 9). Calyrex + Spectrier: kroonheiligdom, de koning (Calyrex lv 70) vraagt jou als "paardenjongen"; Spectrier is zijn paard. De drie Galar-vogels op de Freezing Peak: elk een eigen kamer, alleen hier (speciaal gebied, zoals Jordi wil).
- **Maat/ROM:** L, ±5-6 kaarten + tileset-aanvulling (primary komt uit snow, eigen secondary kost ±100-150 KB), totaal ±250-300 KB. **Intro:** Eternatus (zwarte aderen over het scherm, ±25 KB), Zacian/Zamazenta (paar, ±15 KB), Kyurem (ijsbarsten, ±12 KB), Calyrex (kroon, ±10 KB), Galar-vogels (hergebruik groep 1, ±3 KB).
- **Open:** Calyrex-fusievormen en Kyurem-Black/White staan waarschijnlijk uit in `species_enabled.h` (zie CLAUDE.md): eerst checken en in- of uitschakelen.

### 9. Tao-trio (Reshiram, Zekrom, Kyurem) - Dragon Island
- **Plek:** nieuw **Dragon Island** (Town Map zuidoost, rij 11-14, x 24-27, naast de dragon-encounters op Route 129-131): ruïnetoren (Dragonspiral-hommage) + kleine kaart eromheen.
- **Wanneer:** post-game, na Sootopolis (de draken-lore past bij Rayquaza).
- **Event:** op de bovenste verdieping twee stenen (Light, Dark). Beide twee gevechten, lv 70 (in de bronspellen mag je er één; hier beide voor verkrijgbaarheid, "de broers kunnen niet samen in een kamer"). Een Dragon Tamer-NPC (humor: "ze ruzien al drie eeuwen") legt uit waarom. Kyurem: zie groep 8.
- **Maat/ROM:** M, 2-3 kaarten, ±40 KB (herbruik Sootopolis/Meteor Falls-tilesets). **Intro:** Reshiram (witte vlam), Zekrom (zwarte bliksem), ±20 KB samen.

### 10. Safari-trio: Xerneas, Yveltal, Zeraora (+ Zapdos uit groep 1)
- **Plek:** Fairy Forest (Xerneas), Haunted Camp (Yveltal), Thunder Plains (Zeraora, naast Zapdos). Bestaande kaarten, kleine uitbreiding per zone.
- **Wanneer:** post-game, zones open.
- **Event:** diep in elke zone een afgezet "boom"/"cocon"/"kuil" die in de eerste bezoeken dicht zit; na de Hall of Fame open. Yveltal slaapt in een cocon die 's nachts gloeit. Zeraora is de "kat" onder de bliksemafleider (humor over katten).
- **Maat/ROM:** S, ±35 KB. **Intro:** Xerneas (levensboom), Yveltal (zwarte vleugels), ±20 KB; Zeraora herbruikt Raikou.

### 11. Type: Null + Silvally, Magearna, Poipole (gifts)
- **Plek/event:** Type: Null in een geheime kelder onder Devon Corp (Rustboro; Mr. Stone: "een mislukt beveiligingsproject, past niet in de kast"). Silvally via vriendschap; 17 Memories te koop in de Devon-winkel. Magearna: Colress geeft hem na de Plasma Frigate als "zijn betere werk". Poipole: zie groep 13.
- **Maat/ROM:** S, ±10 KB. **Intro:** geen.

### 12. Tapu-eiland (Tapu Koko, Lele, Bulu, Fini) + Alola-gifts
- **Plek:** nieuw eiland "Tapu Isle" in de Midden-zee (Town Map rij 7-9, x 12-16), vanaf Route 126.
- **Wanneer:** post-game.
- **Event:** vier schrijnen rond een open plein, elk met een eigen NPC-bewaker die niets weet. Elke Tapu vecht na een korte dans/stem-scène (lv 70). Het eiland is ook het **Alola-gebied** voor regionale vormen (zie groep 18). Mist zorgt voor een natuurlijke omheining.
- **Maat/ROM:** M-L, 2-3 kaarten, eigen tileset-aanvulling ±80 KB. **Intro:** één vier-kleuren transitie (veld van de Tapu), ±15 KB.

### 13. Necrozma + Ultra Space (los gebied in Hoenn, niet via de grot)
- **Plek:** Mossdeep Space Center (de buitenruimte bestaat al, Deoxys): een Ultra Wormhole opent na de Delta Episode.
- **Wanneer:** post-game, na Zinnia.
- **Event:** vijf "Ultra Space"-kamers met eigen palet (eigen tileset-aanvulling): Beast Park (Buzzwole, Pheromosa), Metal Ruins (Celesteela, Kartana, Stakataka), Voltage Hall (Xurkitree, Blacephalon), Void (Nihilego, Guzzlord), Poipole bij de uitgang (Poipole als gift, na vijf UB's; Naganadel via Dragon Pulse). Elke UB staat zichtbaar, vast gevecht lv 70; Necrozma op de laatste plek. Humor: "geen wifi in Ultra Space; wel een spiegel".
- **Maat/ROM:** L, 5-6 kaarten + Wormhole-tunnel + eigen tileset (±120 KB), totaal ±250 KB. **Intro:** Wormhole-ripple met palet per UB, ±25 KB; Necrozma eigen, ±20 KB.
- **Spire/Stadium:** Necrozma is al Spire-baas; Buzzwole/Pheromosa zitten in Brent's teams.

### 14. Ruïne-schatten (Wo-Chien, Chien-Pao, Ting-Lu, Chi-Yu)
- **Plek:** vier stakes in vier biomes: Mangrove Mire (Wo-Chien), Route 136/Ashfrost (Chien-Pao), Desert Underpass (Ting-Lu), Jagged Pass (Chi-Yu). Elk een mini-kamer (Regi-grotlayout).
- **Wanneer:** post-game.
- **Event:** op elke plek een houten paal ("do not pull" met een krijtstreepje). Als je hem uittrekt: gevecht met de bewoner (lv 70). Aan het eind klaagt een boze Rancher dat hij "vier palen" kwijt is. Geen verzamelplicht; in vrije volgorde.
- **Maat/ROM:** M, 4 kamers, ±45 KB. **Intro:** één transitie (breuk, 4 paletten), ±10 KB.

### 15. Desert Underpass: Zygarde
- **Plek:** Desert Underpass (3197 tiles, nu leeg) als "Terminus Cave"-hommage; 10 zichtbare Zygarde-cellen in het hol; Zygarde-cube bij de ingang (NPC "archeoloog" met Armaldo-grap).
- **Event:** na alle cellen verschijnt Zygarde (10% eerst, daarna 50%, daarna complete forme in drie gevechten, of één: voorstel één gevecht, lv 70).
- **Maat/ROM:** M, ±25 KB (dezelfde kaart). **Intro:** één, ±10 KB.

### 16. Diancie, Hoopa, Marshadow, Meloetta, Meltan/Melmetal
- **Diancie:** Starfall Grotto (Meteor Falls, nu leeg): kristalkamer met Carbink; Diancie lv 70. S, ±15 KB, transitie met diamantflits ±8 KB.
- **Hoopa:** Mirage Island/Route 130 (Wynaut-kleuterschool uit KAART_REVIEW): Hoopa is de "invalkleerkracht", portalen als ringen. Prison Bottle voor de Unbound-vorm. S, ±15 KB, ring-transitie ±10 KB.
- **Marshadow:** Mt. Pyre Exterior (leeg), 's avonds: je schaduw begint zelf te lopen; volg hem naar een gat in de rots. S, ±15 KB, schaduw-transitie ±10 KB.
- **Meloetta:** Lilycove Museum, achterkamer met een muziekdoos (Relic Song); of als hoofdprijs van het herziene contest-systeem (afhankelijk van `CONTESTS_VOORSTEL.md`). S, ±10 KB, geen eigen intro.
- **Meltan/Melmetal:** Route 126/127 Garbage Patch (drijvend afval, past bij KAART_REVIEW): Meltan wild (zeldzaam), Melmetal als "afvalberg" in het midden (lv 60). Mystery Box-NPC op Paradiso Resort. S-M, ±25 KB, geen eigen intro.

### 17. Spectrier en Calyrex: zie groep 8.

### 18. Regionale vormen (Alola/Galar/Hisui): alleen gifts of speciale gebieden
De 10 nog ontbrekende: Rattata, Raticate, Meowth, Persian (Alola), Farfetch'd + Sirfetch'd (Galar), Voltorb + Electrode (Hisui), Articuno/Zapdos/Moltres (Galar).
- **Alola (Rattata, Meowth):** Tapu-eiland (wild, speciaal gebied) en/of een Alola-toerist op Paradiso Resort die de eerste Rattata/Meowth geeft ("mijn kat is gewoon mijn kat, hij is niet zo anders").
- **Galar (Farfetch'd, Sirfetch'd):** gift van de Galar-Gentleman op Paradiso Resort (Farfetch'd met een prei); Sirfetch'd evolueert via drie krachtige treffers in één gevecht (zoals bronspel) of via het item "Leek"-alternatief.
- **Hisui (Voltorb):** zeemijnen op Route 126: item-ballen die Hisui-Voltorb zijn (grap); één gift via een zeeduiker, Electrode via Thunder Stone.
- **Galar-vogels:** Crown Tundra (groep 8).
- **Vraag:** 37 regionale vormen staan nu al in gewone wilde tabellen (o.a. Alola-Raichu en Alola-Marowak); die laten staan of verplaatsen? Ik stel voor: laten staan.

### 19. Pecharunt
- **Plek:** Fortree Jungle, een verborgen "Mochi-kamer" naast Ogerpon's heiligdom. **Wanneer:** na de Ogerpon-quest. **Event:** een kok geeft een Mochi-doos; de Loyal Three (Okidogi, Munkidori, Fezandipiti) moeten in je team zitten om hem te openen; Pecharunt lv 70. S, ±15 KB, intro ±8 KB.

## Over de Spear Pillar (kort)
Nabouw van Spear Pillar: één ronde top-plateau met ±25 vrije metatiles en eigen tileset (primary + secondary ±100-140 KB). Haalbaar, maar duur voor één kamer; goedkoper alternatief: Dialga en Palkia in de ruimte-tijdgrot zelf (Jordi bepaalt).

## Bouwvolgorde (rondes van 3-4 groepen)
1. **Ronde 1 (alleen bestaande kaarten, S):** 1 (Kanto-vogels), 10 (Safari-trio), 11 (Type: Null/Magearna), 19 (Pecharunt). ±150 KB.
2. **Ronde 2 (hidden rooms, M):** 6 (Swords + Keldeo), 7 (Forces + Enamorus), 14 (ruïne-schatten), 3 (Celebi). ±160 KB.
3. **Ronde 3 (zee- en lege plekken, S-M; vult ook KAART_REVIEW):** 5 (Cresselia/Fullmoon Island), 16 (Diancie, Hoopa, Marshadow, Meloetta, Meltan), 15 (Zygarde). ±110 KB.
4. **Ronde 4 (nieuwe eilanden, M-L):** 12 (Tapu-eiland + Alola-gifts), 9 (Dragon Island), 18 (regionale gifts, Paradiso Resort). ±150 KB.
5. **Ronde 5 (Crown Tundra, L):** 8 (Galar-vogels, Kyurem, Zacian/Zamazenta/Eternatus, Calyrex/Spectrier). ±270 KB. Kyurem pas na ronde 4.
6. **Ronde 6 (Ultra Space, L):** 13 (UB's, Necrozma, Poipole/Naganadel). ±250 KB.
7. **Ruimte-tijdgrot (Jordi ontwerpt):** Dialga, Palkia, Arceus, meertrio, Area Zero (paradoxen, Koraidon, Miraidon, Terapagos). Budget: 400-600 KB voor nagemaakte gebieden (eigen tilesets), apart voorleggen.
Totaal rondes 1-6: ±1,1 MB, past ruim in 3,0 MB.

## Battle Stadium en Spire
- **Stadium:** nieuwe benoemde personages uit de events (dojo-meester, Weather-prof, Ashfrost-smid, Mr. Stone, Dragon Tamer, Mochi-kok, Zygarde-archeoloog) met hun sterkste team in `pool.py`; legendaries zelf alleen als compagnon-/teamlid waar het past. Na elke ronde `pool.py` en `spire_pool.py`/`encounters.py` opnieuw draaien; Stadium-bracket blijft ±100 deelnemers.
- **Spire:** Eternatus, Necrozma en Terapagos blijven bazen; nieuwe verkrijgbare soorten komen automatisch in de rental-pool als de learnset-check ze goedkeurt; geen aanpassing van de bazen.

## Vragen voor Jordi
1. Zacian en Zamazenta beide en Reshiram en Zekrom beide (verkrijgbaarheid) akkoord?
2. Regionale vormen: de 37 bestaande wilde laten staan?
3. Kyurem-fusies, Calyrex-riders, Hoopa Unbound, Therian-vormen aan (soortenlijst `species_enabled.h`)?
4. Ultra Space: ingang via Mossdeep (voorstel) of ergens anders?
5. Meloetta: Lilycove Museum of hoofdprijs van het herziene contest-systeem?
