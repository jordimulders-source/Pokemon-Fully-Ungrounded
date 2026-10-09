# Project Grounded – takenlijst

Eén lijst voor alles wat nog moet. Werkafspraken: `CLAUDE.md`; wat af is: `CHANGELOG.md`. Afgeronde punten hier weghalen en in de changelog zetten. Bron per punt tussen haakjes; details blijven in het brondocument.

**Volgorde (Jordi, 8–9 okt):** eerst de basiskaart vullen → dan de uitbreidingen → pas daarna gevechtsintro's en muziek.

**Prioriteit (Jordi, 9 okt, bijgewerkt):** ~~kratereilanden~~ → ~~Beasts of Ruin~~ → ~~Spacetime deel 1~~ → ~~Spacetime S1~~ (v0.9.178) → ~~Zacian/Zamazenta + Mega Forest~~ (v0.9.176) → ~~Koraalkathedraal/Sea Shards~~ (v0.9.179) → ~~National Park/Ilex/Eternatus~~ (v0.9.181) → ~~Yoshi's Island~~ (v0.9.194) → meren (portalen) → Giratina-gang → Mt. Coronet/Spear Pillar → Arceus/Azure Flute/Hall of Origin → Spire → intro's/muziek → contests/Trick House. Eén à twee agents tegelijk, zuinig. **Verhaallijn Spacetime: `SPACETIME_PLAN.md`.**

---

## 1. Nu (fase: basiskaart vullen)
Gedaan sinds: Yoshi's Island (v0.9.194), Area Zero (v0.9.193), park-vuur + Ilex-schrijn (v0.9.191), Glimwood (v0.9.189), trog 127 + Chargestone + Spacetime-items (v0.9.188), Virizion-kamer + wild Uncharted Isle (v0.9.186), Swords of Justice/Keldeo/Meltan (v0.9.182), National Park + Ilex (v0.9.181), Spacetime S2 + Chargestone Cave (v0.9.180), Koraalkathedraal + Sea Shards (v0.9.179), Spacetime S1 (v0.9.178), Mega Forest + Zacian/Zamazenta (v0.9.176), Spacetime Cave deel 1 (v0.9.173), Beasts of Ruin (v0.9.170), kratereilanden Sootopolis (v0.9.165), extra dungeons (Granite-kristalgrot, Cave of Origin dieper, Shoal Frozen Depths, luchtbel-grot 128; v0.9.164), Tao-eiland met Reshiram/Zekrom/Kyurem/Ghetsis (v0.9.163), Birth Island weg + Beacon Isle met Lichteiland (v0.9.162), gifts/Deoxys-vormen/Stadium-pool (v0.9.161), Viagra Boys-intro + Kiyo (v0.9.160).
Gedaan (9 okt): kaartvulling 4 (v0.9.157: wild in alle dungeons, Granite Cave, Mt. Chimney, Shoal Cave eb/vloed, Seafloor, Cave of Origin) en zeevulling 4 (v0.9.159: alle onderwaterkaarten, diepzeetrog). Nog open:

~~Beasts of Ruin bijwerken~~ (v0.9.174).

**Feedback Jordi 9 okt (volgende agents):**
**Feedback Jordi 9 okt (in uitvoering):**
- ~~Levelcurve~~ (v0.9.192). **Open voor Jordi:** evolutie-advies in `LEVELCURVE.md` (Hydreigon 53→64, Dragapult 50→60, Volcarona 40→59, Mienshao, Mandibuzz, Klinklang, Vanilluxe terug naar ±officieel?) en ±650 wilde slots ver boven hun evolutielevel (laat in de game evoluties zetten?). Dave/SickBlik/Mitch hebben nog geen post-game-gevecht (komt dat er, dan lv 100).

**Technische schuld:** de bouwscripts (`spacetime_cave.py`, `area_zero.py`, `national_park.py`, `chargestone.py`, `glimwood.py`, `swords_keldeo.py`, `mega_forest.py` e.a.) bevatten nog de levels van vóór de levelcurve (v0.9.192): opnieuw draaien zet trainer-, wilde en `setwildbattle`-levels terug. Levels in de scripts gelijktrekken (of de levelcurve als laatste stap laten toepassen) voordat ze weer gedraaid worden.

## 2. Daarna (uitbreidingen, in deze volgorde)
3. **Spacetime Cave bij Mossdeep** — verhaallijn in `SPACETIME_PLAN.md` (Jordi 9 okt). Locaties:
   - ~~S1~~ (v0.9.178). Open: de meren-scheur staat nu al open ("overkant laadt nog"), terwijl de meren-kamer volgens het plan pas na ????? komt: dichtzetten? `dex_beschikbaar.json`/`TEKSTEN_EVENTS.md` noemen Mewtwo nog bij Meteor Falls.
   - ~~a. Lavender Town + Pokémon Tower~~ (v0.9.173)
   - b. **National Park + Ilex Forest**: Calyrex/Eternatus/Celebi-quest (SPACETIME_PLAN); daarna Calyrex-quest met Glastrier/Spectrier (sneeuwgebied of nieuw eiland).
     - Ontwerp (Jordi, 9 okt, 3 screenshots HGSS/DPPt-stijl als inspiratie): park in de vorm van een **Poké Ball**, relaxed en comfortabel. Bovenste helft hoog gras, onderste helft ander (donkerder) gras, het midden een fontein als knop van de bal, stenen paden in trapvorm eromheen, hekjes, lantaarns en bloemen langs de rand, bomen rondom. Onderaan een gang naar een pleintje met bankjes, een bloembak en een bord, en daar een warp naar **Ilex Forest**. Ingang rechts vanuit de Spacetime Cave: een poortgebouwtje aan de oostkant (zoals HGSS), binnen een FRLG-achtig poorthuis met een zijuitgang (pijl-warp `MB_EAST_ARROW_WARP`, werkt in de engine). Ekat-sets: Park Tileset, Park Gazebo, Pond and Bridge. Geen bug-catching-minigame.
     - **Ilex Forest** (Jordi, 9 okt, 4 screenshots GSC/HGSS als inspiratie; meer creatieve vrijheid): mysterieus. Basis zoals GSC/HGSS: dicht bos met kronkelpaden, poorthuis linksboven en linksonder, vijver linksboven, het **schrijn in het midden** (Celebi-quest), houten hekjes, bloemenpaadjes, Cut-boompjes. Eigen draai: mist/donkere tint, dwaalpaden. Hier komt de **Celebi-quest**.
   - ~~c. Cerulean Cave met de echte Mewtwo~~ (v0.9.173).
   - d. **Gen 4-meren** (Uxie, Mesprit, Azelf): aparte kamer tussen ????? en Mt. Coronet, drie portalen (Acuity in sneeuw, Valor, Verity), grot in elk meer (SPACETIME_PLAN).
   - e. **?????-locatie → Yoshi's Island** (Shy Guy-quest, zie 4)
   - ~~f. Area Zero~~ (v0.9.193): flinke paradox-quest met Miraidon/Koraidon, beveiligingssystemen en Tera Cave/Terapagos (SPACETIME_PLAN; paradoxen niet meer gepauzeerd). Jordi 9 okt: een krater waar je steeds verder afdaalt, tot je in een surrealistische kristalgrot komt; hier de meeste creatieve vrijheid. Referenties: `graphics/grounded/referenties/area_zero/`.
   - ~~Chargestone Cave~~ (v0.9.180) (Jordi 9 okt): niet helemaal nabouwen, wel dat sfeertje (zwevende elektrische stenen, blauw licht) en de schaal; een elektrische grot. Referenties: `referenties/chargestone/` (1F, B1F, B2F uit B2W2).
   - ~~Glimwood Tangle~~ (v0.9.189) (Jordi 9 okt): sfeer van Glimwood + Ballonlea (lichtgevende paddenstoelen, donker sprookjesbos). Referenties: `referenties/glimwood_ballonlea/` en ongesorteerde sfeerbeelden in `referenties/sfeer_ongesorteerd/`.
   - g. **Mt. Coronet als laatste post-game-quest:** als je de rest hebt, Dialga, Palkia en tot slot Arceus.
     - Ontwerp (Jordi, 9 okt; ook 7F, sneeuwgebied, Spear Pillar en Hall of Origin in de referenties; DPPt-kaarten als **inspiratie, niet perfect nabouwen**; beelden in `graphics/grounded/referenties/mt_coronet/`): je begint al hoog in de berg. **4F:** een sneeuwgebied buiten (grote terrasvormige sneeuwhelling rond de top, hoog gras, rotsen, bruggetjes) en drie verbonden grotkamers (1: grote kamer met waterval in het midden en trappen; 2: kleine kamer met twee items en een rots; 3: L-vormige gang). Je gaat naar buiten, loopt om de berg heen en komt via de 3e kamer van 4F naar **5F** (trapsgewijze grotkamer, Strength-rotsen). **6F:** smalle kamer met twee trappen omhoog en twee pilaren, bovenaan de lichte uitgang naar **Spear Pillar**.
4. ~~**Yoshi's Island / Shy Guy-quest**~~ (v0.9.194): top-down in Pokémon-stijl, maar grafisch compleet anders (dat is de grap), uit Jordi's sheets (`graphics/*Yoshi*`, `bg*.png`, `misc*.png`, `world-map.png`). Shy Guys = parodie op een evil team, praten niet (sarcasme tussen haakjes). Multi battles samen met Yoshi tegen een reeks Shy Guys → Commander Boo → Wario zit erachter. Wacht deels op Jordi's assets. (8–9 okt)
6. **Regionale vormen:** Alola-Rattata/-Meowth en Galar-Farfetch'd zijn gifts (v0.9.161); de Galar-vogels horen bij de gepauzeerde Crown Tundra. (6 okt; LEGENDARY_PLAN groep 18)
7. **Contests reworken:** Jordi bedenkt zelf de ideeën; voorstel ligt klaar (QoL-pakket eerst: Berry Blender als menu, kortere wachttijden). (5–6 okt; CONTESTS_VOORSTEL)
8. **Trick House vervangen?** Wacht op Jordi's idee. (okt)
9. **The Spire (na Jordi's test, `SPIRE_TESTCHECKLIST.txt`):** gewone gevechten per deel van de act, één elite-pool per act, gevechten meer als puzzel. Nog open: codex, golven (derde vijand), dramatischer baas-intro, ja/nee bij de receptioniste, echte teksten. (okt; SPIRE_DESIGN "Nog open")
11. **Overige legendaries: gepauzeerd** (zie Besloten). Plan per groep klaar in LEGENDARY_PLAN: Kanto-vogels, Swords of Justice + Keldeo, Enamorus, Crown Tundra, Safari-trio (Xerneas/Yveltal/Zeraora), Ultra Space + Necrozma, ruïne-schatten, Zygarde, Diancie, Marshadow, Meloetta, Meltan, Pecharunt.
13. **Abandoned Ship** met een nachtelijk benedendek (Jordi 9 okt: prima).
14. **Frontier-rentals** afstemmen op de gewijzigde soorten en moves: zodra de wereld genoeg gevuld is (Jordi 9 okt).
15. ~~**Meltan**~~ (v0.9.182) als gift, evolueert in **Melmetal** door te levelen met een Metal Coat (Jordi 9 okt; plek nog kiezen).
16. **Enamorus** (Jordi 9 okt): zwerft rond zoals de andere Forces. Zodra die allemaal gevangen zijn, hebben bepaalde stadjes kans op Enamorus: overal hartjes en NPC's die avances naar elkaar maken; één van de koppels is **Birch met een hoop stront**.
18. ~~**Swords of Justice + Keldeo**~~ (v0.9.182) (Jordi 9 okt): Cobalion (diepste kamer Granite Cave), Terrakion (extra kamer Victory Road), Virizion (Mangrove Mire), zonder quest (zoals Gen 5). Heb je alle drie, dan belt **Mr. Briney** via de PokéNav: hij ziet iets heel geks in het water. Bij hem in de boot, fade-out, hij vaart je naar een plek die niet op de kaart staat: een pas ontstaan eiland met draaikolken; hij zet je af en daar staat **Keldeo**.
17. **Altering Cave:** locatie behouden, koppelen aan een nog te bepalen legendary-quest.

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
- ~~**Beasts of Ruin**~~ (gedaan v0.9.170; thema nabouwen staat nog bij muziek) **(Jordi 9 okt):** Wo-Chien, Chien-Pao, Ting-Lu en Chi-Yu, elk "gesealed" op een lege plek in de wereld, bijv. Chi-Yu in een kamer bovenin Jagged Pass die naar een vurig gebied leidt. Hun thema nabouwen (Jordi is er weg van).
- **Zacian en Zamazenta (Jordi 9 okt):** in een gebied achter een roadblock; een heel lichte visuele hint in het Mini Forest (Route 102), dat uiteindelijk het **Mega Forest** wordt, waar later meer kan.

## 4. Open vragen voor Jordi
0. **Trainer-id's raken op:** nog 50 vrij (1017–1019, 1026–1029, 1049, 1055–1059, 1068–1069, 1080–1099, 1107–1109, 1124–1129, 1180–1185). Jordi 9 okt: niet erg; Shy Guys worden wel trainers. Wordt het krap, dan halen we elders iets weg.
2. Chargestone (Colress + Zeraora) en Glimwood (Ballonlea-heks i.p.v. Opal, Xerneas/Yveltal): akkoord (9 okt).
3. **Nog te bedenken (Jordi 9 okt):** plekken voor Kanto-/Galar-vogels, ~~Swords of Justice~~ (zie 18), Ultra Space (Cosmog-lijn, Necrozma, Ultra Beasts), Meloetta, Diancie, Zygarde. **Pecharunt** misschien in Yoshi's Island. **Marshadow:** post-game tijdens het gevecht tegen **Keccles in de Battle Frontier** springt hij uit je schaduw, wil samen met een sterke trainer strijden en hoort daarna bij je; Keccles: "wow, daar kan ik nog wat van leren. Dát is pas camouflage."

## 5. Besloten / bewust niet
- **Geen Grounded-Pokédex:** gewoon de National Dex met alles, vanaf het begin. **Signatures gepauzeerd**; Gen 4+-trainersprites voorlopig niet nodig. (9 okt)
- **Spacetime-locaties** zijn andere dimensies: niet vliegbaar. (9 okt)
- **Volgorde:** basiskaart → uitbreidingen → intro's en muziek. (8–9 okt)
- **Birth Island weg** (kaart, event, ticket). Deoxys alleen in de ruimte. (5 en 9 okt)
- **Gerald weg** (Dragonspine wordt het Tao-eiland). (9 okt)
- **Legendaries gepauzeerd** (6 okt), behalve: Type: Null + Magearna (gifts), Tapu Isle en Cresselia (gedaan), Hoopa en de Forces (gedaan), en sinds 9 okt het Tao-trio en de Spacetime Cave (Mewtwo, Celebi, meertrio, Dialga, Palkia, Arceus).
- **Paradox-Pokémon:** alleen in Area Zero (Spacetime Cave); ze tellen niet als legendaries. (9 okt)
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
