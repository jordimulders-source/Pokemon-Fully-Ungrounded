# Project Grounded – takenlijst

Eén lijst voor alles wat nog moet. Werkafspraken: `CLAUDE.md`; wat af is: `CHANGELOG.md`. Afgeronde punten hier weghalen en in de changelog zetten. Bron per punt tussen haakjes; details blijven in het brondocument.

**Volgorde (Jordi, 8–9 okt):** eerst de basiskaart vullen → dan de uitbreidingen → pas daarna gevechtsintro's en muziek.

**Prioriteit (Jordi, 9 okt):** ~~kratereilanden~~ → Beasts of Ruin → Spacetime Cave deel 1 (Lavender + Pokémon Tower, Cerulean Cave uit FRLG) → Zacian/Zamazenta + Mega Forest → Koraalkathedraal/Sea Shards → Yoshi's Island → overige Spacetime-locaties (met Jordi's input) → Spire → intro's/muziek → contests/Trick House/Dex. Eén agent tegelijk, zuinig.

---

## 1. Nu (fase: basiskaart vullen)
Gedaan sinds: kratereilanden Sootopolis (v0.9.165), extra dungeons (Granite-kristalgrot, Cave of Origin dieper, Shoal Frozen Depths, luchtbel-grot 128; v0.9.164), Tao-eiland met Reshiram/Zekrom/Kyurem/Ghetsis (v0.9.163), Birth Island weg + Beacon Isle met Lichteiland (v0.9.162), gifts/Deoxys-vormen/Stadium-pool (v0.9.161), Viagra Boys-intro + Kiyo (v0.9.160).
Gedaan (9 okt): kaartvulling 4 (v0.9.157: wild in alle dungeons, Granite Cave, Mt. Chimney, Shoal Cave eb/vloed, Seafloor, Cave of Origin) en zeevulling 4 (v0.9.159: alle onderwaterkaarten, diepzeetrog). Nog open:
2. **Koraalkathedraal (126) en Sea Shard-verzamelquest** bij de Diving Treasure Hunter (overgeslagen in v0.9.164). (VRAGEN_VOLGENDE O1/O4)

## 2. Daarna (uitbreidingen, in deze volgorde)
3. **Spacetime Cave bij Mossdeep** (lege plek op de Town Map), met warps naar: (9 okt; eerder 5–6 okt)
   - a. **Lavender Town + Pokémon Tower**
   - b. **National Park**, eventueel met **Ilex Forest** (Celebi)
     - Ontwerp (Jordi, 9 okt, 3 screenshots HGSS/DPPt-stijl als inspiratie): park in de vorm van een **Poké Ball**, relaxed en comfortabel. Bovenste helft hoog gras, onderste helft ander (donkerder) gras, het midden een fontein als knop van de bal, stenen paden in trapvorm eromheen, hekjes, lantaarns en bloemen langs de rand, bomen rondom. Onderaan een gang naar een pleintje met bankjes, een bloembak en een bord, en daar een warp naar **Ilex Forest**. Ingang rechts vanuit de Spacetime Cave: een poortgebouwtje aan de oostkant (zoals HGSS), binnen een FRLG-achtig poorthuis met een zijuitgang (pijl-warp `MB_EAST_ARROW_WARP`, werkt in de engine). Ekat-sets: Park Tileset, Park Gazebo, Pond and Bridge. Geen bug-catching-minigame.
     - **Ilex Forest** (Jordi, 9 okt, 4 screenshots GSC/HGSS als inspiratie; meer creatieve vrijheid): mysterieus. Basis zoals GSC/HGSS: dicht bos met kronkelpaden, poorthuis linksboven en linksonder, vijver linksboven, het **schrijn in het midden** (Celebi-quest), houten hekjes, bloemenpaadjes, Cut-boompjes. Eigen draai: mist/donkere tint, dwaalpaden. Hier komt de **Celebi-quest**.
   - c. **Cerulean Cave** met de echte Mewtwo (de grot achter Meteor Falls is een placeholder)
   - d. **Gen 4-meren** (Uxie, Mesprit, Azelf)
   - e. **?????-locatie → Yoshi's Island** (Shy Guy-quest, zie 4)
   - f. later eventueel **Area Zero** (paradoxen zijn gepauzeerd)
   - g. **Mt. Coronet als laatste post-game-quest:** als je de rest hebt, Dialga, Palkia en tot slot Arceus.
     - Ontwerp (Jordi, 9 okt; DPPt-kaarten als **inspiratie, niet perfect nabouwen**; beelden in `graphics/grounded/referenties/mt_coronet/`): je begint al hoog in de berg. **4F:** een sneeuwgebied buiten (grote terrasvormige sneeuwhelling rond de top, hoog gras, rotsen, bruggetjes) en drie verbonden grotkamers (1: grote kamer met waterval in het midden en trappen; 2: kleine kamer met twee items en een rots; 3: L-vormige gang). Je gaat naar buiten, loopt om de berg heen en komt via de 3e kamer van 4F naar **5F** (trapsgewijze grotkamer, Strength-rotsen). **6F:** smalle kamer met twee trappen omhoog en twee pilaren, bovenaan de lichte uitgang naar **Spear Pillar**.
4. **Yoshi's Island / Shy Guy-quest:** top-down in Pokémon-stijl, maar grafisch compleet anders (dat is de grap), uit Jordi's sheets (`graphics/*Yoshi*`, `bg*.png`, `misc*.png`, `world-map.png`). Shy Guys = parodie op een evil team, praten niet (sarcasme tussen haakjes). Multi battles samen met Yoshi tegen een reeks Shy Guys → Commander Boo → Wario zit erachter. Wacht deels op Jordi's assets. (8–9 okt)
6. **Regionale vormen:** Alola-Rattata/-Meowth en Galar-Farfetch'd zijn gifts (v0.9.161); de Galar-vogels horen bij de gepauzeerde Crown Tundra. (6 okt; LEGENDARY_PLAN groep 18)
7. **Contests reworken:** Jordi bedenkt zelf de ideeën; voorstel ligt klaar (QoL-pakket eerst: Berry Blender als menu, kortere wachttijden). (5–6 okt; CONTESTS_VOORSTEL)
8. **Trick House vervangen?** Wacht op Jordi's idee. (okt)
9. **The Spire (na Jordi's test, `SPIRE_TESTCHECKLIST.txt`):** gewone gevechten per deel van de act, één elite-pool per act, gevechten meer als puzzel. Nog open: codex, golven (derde vijand), dramatischer baas-intro, ja/nee bij de receptioniste, echte teksten. (okt; SPIRE_DESIGN "Nog open")
11. **Overige legendaries: gepauzeerd** (zie Besloten). Plan per groep klaar in LEGENDARY_PLAN: Kanto-vogels, Swords of Justice + Keldeo, Enamorus, Crown Tundra, Safari-trio (Xerneas/Yveltal/Zeraora), Ultra Space + Necrozma, ruïne-schatten, Zygarde, Diancie, Marshadow, Meloetta, Meltan, Pecharunt.
12. **Eigen Grounded-Pokédex** zonder weggelaten soorten: Jordi kiest de groepen. (6 okt; DEX_ANALYSE 6)

## 3. Daarna: gevechtsintro's en muziek
**Jordi 9 okt:** intro's van (nieuwe) legendaries bedenkt hij zelf; thema's nog niet maken: nieuwe legendaries gebruiken `MUS_RG_VS_LEGEND` (Kanto Legendary) tot hij ermee komt.
**Intro's** (filmspeler `film.py`; alle gymleiders en de lijst van 5 okt zijn af, v0.9.92–0.9.143):
- Shy Guy (idee van Jordi), Commander Boo en Wario (Yoshi's Island). (8 okt)
- Cresselia (nu vanilla). (v0.9.122)
- Nieuwe legendaries uit de uitbreidingen: Reshiram, Zekrom, Kyurem, Spacetime Cave (Mewtwo-Cerulean, meertrio, Celebi, Dialga, Palkia, Arceus).
- Maxie & Archie: Jordi was "geen grote fan", sterker maken. (5 okt)

**Muziek** (status uit `tools/grounded/MUZIEK.md` en de changelog):
- Wacht op Jordi's oordeel: **Neo Plasma** v12k (v0.9.109), **Brawly** v6 Rocky-stijl (v0.9.98), **Regigigas** v5, **Burglar** v1 (v0.9.93). Batch 5 (v0.9.88) was verder "zeer tot gematigd tevreden".
- Nog te maken: **Volcanion**, **Cresselia**, **Battle Stadium** (arena + finale, MUZIEK_KANDIDATEN A5), muziek voor de nieuwe uitbreidingen (Tao-eiland, Spacetime Cave, Yoshi's Island/Boo-thema: Jordi uploadt de Boo-bron).
- Route-remixes, allemaal nog niet gemaakt (MUZIEK_KANDIDATEN C): Route 135/136 winter, Fortree Jungle, Mangrove Mire, Toadstool Hollow, Safari (Fairy Forest / Thunder Plains / Haunted Camp), The Spire (per act + elite/baas), Meteor Falls (kosmisch), Flower Paradise / Liberty Garden.
- Delta Episode: MIDI's voor **The Heirs to Eternity** en **The Lament of Falling Stars** (Jordi levert of wij zoeken). (4 okt)
- Na de beta: Ho-Oh helderder, minder stotterende percussie. (6 okt)

## Antwoorden Jordi 9 okt (verwerkt)
- **Tao-eiland:** Dragon Tamers, verzekeringsexpert en drakentabellen blijven (alleen Gerald weg). Kyurem neutraal (geen Black/White-vorm). **Ghetsis** moet nog ergens in de wereld komen: hij geeft de **DNA Splicers**.
- **Beacon Isle:** het lichteiland krijgt een kleine grot met zeldzame wilde soorten en één sterk gevecht.
- **Spacetime Cave-warps:** Cerulean Cave, Lavender Town + Pokémon Tower, National Park + Forest-tunnel naar Ilex Forest (Celebi), een representatie van de Gen 4-meren, Mt. Coronet + Spear Pillar (+ de trap naar Arceus, aan het einde), Chargestone Cave (of een versie daarvan), Glimwood Tangle, Area Zero, en ????? naar Yoshi's Island. De Mewtwo-grot in Meteor Falls verdwijnt uiteindelijk. **Per locatie eerst input van Jordi** (volledig nabouwen of eigen richting, welke assets).
- **Delta Episode:** Deoxys is beloning genoeg. Idee: een plek waar je Deoxys met de meteorieten van vorm laat wisselen.
- **Contests:** helemaal herbouwen, maar achteraan de lijst.
- **Beasts of Ruin (Jordi 9 okt):** Wo-Chien, Chien-Pao, Ting-Lu en Chi-Yu, elk "gesealed" op een lege plek in de wereld, bijv. Chi-Yu in een kamer bovenin Jagged Pass die naar een vurig gebied leidt. Hun thema nabouwen (Jordi is er weg van).
- **Zacian en Zamazenta (Jordi 9 okt):** in een gebied achter een roadblock; een heel lichte visuele hint in het Mini Forest (Route 102), dat uiteindelijk het **Mega Forest** wordt, waar later meer kan.

## 4. Open vragen voor Jordi
(Vragen 1–3, 5 en 7 van 9 okt zijn beantwoord en verwerkt; zie hierboven.)
1. **Yoshi's Island:** zijn alle assets binnen, en heb je al een idee voor de Shy Guy-intro?
2. **Spacetime Cave:** per locatie input (volledig nabouwen of eigen richting, welke assets). Cerulean Cave, Lavender Town en Pokémon Tower worden kopieën van FRLG.
3. **Altering Cave** elke dag andere soorten, en **Abandoned Ship** met een nachtelijk benedendek: nog gewenst? (VRAGEN_VOLGENDE 2; Mirage Tower terug vervalt, Hoopa heeft hem "opgevouwen")
4. **Extra signatures** die nog niet gekozen zijn: Feud Claw/Grudge Fang (Zangoose/Seviper), Firefly Signal (Volbeat/Illumise). Wel of niet? (VRAGEN_VOLGENDE 6)
5. **Gen 4+-trainersprites** (Greenphx; HGSS/BW-sheets in `graphics/`): welke personages eerst? En krijgt V een eigen sprite?
6. **Frontier-rentals** afstemmen op de gewijzigde soorten en moves: nog gewenst? (backlog okt)
7. **Grounded-Pokédex:** welke groepen weglaten (Ultra Beasts, paradoxen, ...)? (DEX_ANALYSE 6)

## 5. Besloten / bewust niet
- **Volgorde:** basiskaart → uitbreidingen → intro's en muziek. (8–9 okt)
- **Birth Island weg** (kaart, event, ticket). Deoxys alleen in de ruimte. (5 en 9 okt)
- **Gerald weg** (Dragonspine wordt het Tao-eiland). (9 okt)
- **Legendaries gepauzeerd** (6 okt), behalve: Type: Null + Magearna (gifts), Tapu Isle en Cresselia (gedaan), Hoopa en de Forces (gedaan), en sinds 9 okt het Tao-trio en de Spacetime Cave (Mewtwo, Celebi, meertrio, Dialga, Palkia, Arceus).
- **Paradox-Pokémon gepauzeerd**; Area Zero hooguit later via de Spacetime Cave. (8 okt)
- **Ultra Space** wordt een los gebied, niet via de Spacetime Cave (gepauzeerd). In de Spacetime Cave geen vogellocaties en geen Fullmoon Island. Ilex Forest mag nu wel, voor Celebi. (6 en 9 okt)
- **Geen Mega Evolution, Z-moves, Dynamax of Tera voor de speler.** De vormen staan alleen aan voor Spire-bazen en trainers. (begin changelog; v0.8.104)
- **Verborgen abilities zijn niet verkrijgbaar** (geen Ability Patch, DexNav uit); een sterke ability hoort in slot 1/2. (5 okt)
- **Jirachi blijft in Fallarbor**, Lugia op Whirl Island. (5 okt)
- **Muziek alleen als MIDI**, geen gestreamde mp3-samples. (4 okt)
- **Geen eigen thema** voor Archie/Maxie (werkstraf), Team Rocket (Petrel) en Deoxys. N's thema is weg (kapotte bron). (5 okt; v0.9.147)
- **Ho-Oh v2 is voldoende voor de beta.** (6 okt)
- **Geen back sprites**: in het Stadium geen trainer-backs aan onze kant. (4 okt)
- **Stadium:** alleen echt iconische personages in de pool; duo's worden willekeurig gekoppeld. (v0.9.123; 5 okt)
- **Grap-trainers** met extreem lage levels alleen vroeg in de game. (v0.9.119)
- **Geen TM's als beloning** (alle TM01–59 liggen al). (okt)
- **Geen minigames** (vissen, visserstoernooi, Pokéblocks: menu i.p.v. Blender). (QoL)
- **Geen Jessie en James.** (v0.9.15)
- **Kecleon** is van Keccles: niet als winkelier of losse NPC.
- **Elemental monkeys** blijven weg.
- **Dialogen van Trick House, Battle Frontier en Battle Tents** blijven vanilla tot na de beta.
