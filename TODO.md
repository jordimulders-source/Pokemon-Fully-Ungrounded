# Project Grounded – takenlijst

Eén lijst voor alles wat nog moet. Werkafspraken: `CLAUDE.md`; wat af is: `CHANGELOG.md`. Afgeronde punten hier weghalen en in de changelog zetten. Bron per punt tussen haakjes; details blijven in het brondocument.

**Volgorde (Jordi, 8–9 okt):** eerst de basiskaart vullen → dan de uitbreidingen → pas daarna gevechtsintro's en muziek.

**Prioriteit (Jordi, 9 okt, bijgewerkt):** ~~kratereilanden~~ → ~~Beasts of Ruin~~ → ~~Spacetime deel 1~~ → ~~Spacetime S1~~ (v0.9.178) → ~~Zacian/Zamazenta + Mega Forest~~ (v0.9.176) → ~~Koraalkathedraal/Sea Shards~~ (v0.9.179) → ~~National Park/Ilex/Eternatus~~ (v0.9.181) → ~~Yoshi's Island~~ (v0.9.194) → ~~meren~~ (v0.9.197) → ~~Mt. Coronet/Spear Pillar~~ (v0.9.198) → ~~Arceus/Azure Flute/Hall of Origin~~ (v0.9.207) + ~~Calyrex-quest~~ (v0.9.205–206) → Spire → intro's/muziek → contests/Trick House. Eén à twee agents tegelijk, zuinig. **Verhaallijn Spacetime: `SPACETIME_PLAN.md`.**

---

## 0. Testrun-aantekeningen (Jordi 15 okt)
- **Metronome** (held item) en **Muscle Band** krijgen nog een vindplaats (Metronome ligt nergens; Muscle Band alleen in Area Zero). Komt mee met Jordi's kladblok met aanpassingen. Idee: Muscle Band als fysieke tegenhanger van de Wise Glasses (Devon Corp 2F); Metronome bij een niche (Straight Line, Echoed Voice, Fury Cutter, Rollout).
- **Spire-rekenscripts opnieuw draaien** na de buffs van 15 okt (spire_pool.py + encounters.py): de uitvoer veranderde veel (±500 regels in SPIRE_BALANS/spire_encounters) en encounters.py gaf één keer exit 1; nog niet gecommit, eerst uitzoeken.

## 1. Nu (fase: basiskaart vullen)
Gedaan sinds: Yoshi's Island (v0.9.194), Area Zero (v0.9.193), park-vuur + Ilex-schrijn (v0.9.191), Glimwood (v0.9.189), trog 127 + Chargestone + Spacetime-items (v0.9.188), Virizion-kamer + wild Uncharted Isle (v0.9.186), Swords of Justice/Keldeo/Meltan (v0.9.182), National Park + Ilex (v0.9.181), Spacetime S2 + Chargestone Cave (v0.9.180), Koraalkathedraal + Sea Shards (v0.9.179), Spacetime S1 (v0.9.178), Mega Forest + Zacian/Zamazenta (v0.9.176), Spacetime Cave deel 1 (v0.9.173), Beasts of Ruin (v0.9.170), kratereilanden Sootopolis (v0.9.165), extra dungeons (Granite-kristalgrot, Cave of Origin dieper, Shoal Frozen Depths, luchtbel-grot 128; v0.9.164), Tao-eiland met Reshiram/Zekrom/Kyurem/Ghetsis (v0.9.163), Birth Island weg + Beacon Isle met Lichteiland (v0.9.162), gifts/Deoxys-vormen/Stadium-pool (v0.9.161), Viagra Boys-intro + Kiyo (v0.9.160).
Gedaan (9 okt): kaartvulling 4 (v0.9.157: wild in alle dungeons, Granite Cave, Mt. Chimney, Shoal Cave eb/vloed, Seafloor, Cave of Origin) en zeevulling 4 (v0.9.159: alle onderwaterkaarten, diepzeetrog). Nog open:

~~Beasts of Ruin bijwerken~~ (v0.9.174).

**Feedback Jordi 9 okt (volgende agents):**
**Feedback Jordi 9 okt (in uitvoering):**
- ~~Levelcurve~~ (v0.9.192), ~~evolutielevels + post-game wild per fase~~ (v0.9.202), ~~Dave/SickBlik lv 100~~ (v0.9.201). Mitch kiest zelf tussen thema A en B (v0.9.200). Mitch post-game-gevecht nog te bedenken.

**In uitvoering (Jordi 9 okt):** grondige bugjacht richting 1.0 (agent: warps, crashes, grafische bugs, onafgemaakte kaarten, gevechten die niet passen; `AUDIT.md`). Gedaan: casino-odds/bookies/skip + Abandoned Ship (v0.9.216). Gedaan: Battle Casino (v0.9.213), Spear Pillar/Hall/constructen (v0.9.211), Enamorus (v0.9.212), Nep-Enut + Yoshi-huis (v0.9.208–210).
Trainer-id's: op (1184 en 854 gebruikt voor SickBlik); 851–853 vanilla Red/Leaf/Brendan-placeholder nog vrij te maken. Testers van Jordi als trainers: id's vrijmaken (bijv. scripted gevechten die een id delen).

~~Technische schuld bouwscripts~~ (v0.9.195–198: `check_levels.protect()` bewaakt levels en events; alle bouwscripts draaien zonder wijzigingen).

## 2. Daarna (uitbreidingen, in deze volgorde)
3. **Spacetime Cave bij Mossdeep** — verhaallijn in `SPACETIME_PLAN.md` (Jordi 9 okt). Locaties:
   - ~~S1~~ (v0.9.178). Open: `dex_beschikbaar.json`/`TEKSTEN_EVENTS.md` noemen Mewtwo nog bij Meteor Falls.
   - ~~a. Lavender Town + Pokémon Tower~~ (v0.9.173)
   - ~~b. National Park + Ilex Forest~~ (v0.9.181; Calyrex-quest v0.9.205): Calyrex/Eternatus/Celebi-quest (SPACETIME_PLAN); daarna Calyrex-quest met Glastrier/Spectrier (sneeuwgebied of nieuw eiland).
     - Ontwerp (Jordi, 9 okt, 3 screenshots HGSS/DPPt-stijl als inspiratie): park in de vorm van een **Poké Ball**, relaxed en comfortabel. Bovenste helft hoog gras, onderste helft ander (donkerder) gras, het midden een fontein als knop van de bal, stenen paden in trapvorm eromheen, hekjes, lantaarns en bloemen langs de rand, bomen rondom. Onderaan een gang naar een pleintje met bankjes, een bloembak en een bord, en daar een warp naar **Ilex Forest**. Ingang rechts vanuit de Spacetime Cave: een poortgebouwtje aan de oostkant (zoals HGSS), binnen een FRLG-achtig poorthuis met een zijuitgang (pijl-warp `MB_EAST_ARROW_WARP`, werkt in de engine). Ekat-sets: Park Tileset, Park Gazebo, Pond and Bridge. Geen bug-catching-minigame.
     - **Ilex Forest** (Jordi, 9 okt, 4 screenshots GSC/HGSS als inspiratie; meer creatieve vrijheid): mysterieus. Basis zoals GSC/HGSS: dicht bos met kronkelpaden, poorthuis linksboven en linksonder, vijver linksboven, het **schrijn in het midden** (Celebi-quest), houten hekjes, bloemenpaadjes, Cut-boompjes. Eigen draai: mist/donkere tint, dwaalpaden. Hier komt de **Celebi-quest**.
   - ~~c. Cerulean Cave met de echte Mewtwo~~ (v0.9.173).
   - ~~d. Gen 4-meren~~ (v0.9.197) (Uxie, Mesprit, Azelf): aparte kamer tussen ????? en Mt. Coronet, drie portalen (Acuity in sneeuw, Valor, Verity), grot in elk meer (SPACETIME_PLAN).
   - e. **?????-locatie → Yoshi's Island** (Shy Guy-quest, zie 4)
   - ~~f. Area Zero~~ (v0.9.193): flinke paradox-quest met Miraidon/Koraidon, beveiligingssystemen en Tera Cave/Terapagos (SPACETIME_PLAN; paradoxen niet meer gepauzeerd). Jordi 9 okt: een krater waar je steeds verder afdaalt, tot je in een surrealistische kristalgrot komt; hier de meeste creatieve vrijheid. Referenties: `graphics/grounded/referenties/area_zero/`.
   - ~~Chargestone Cave~~ (v0.9.180) (Jordi 9 okt): niet helemaal nabouwen, wel dat sfeertje (zwevende elektrische stenen, blauw licht) en de schaal; een elektrische grot. Referenties: `referenties/chargestone/` (1F, B1F, B2F uit B2W2).
   - ~~Glimwood Tangle~~ (v0.9.189) (Jordi 9 okt): sfeer van Glimwood + Ballonlea (lichtgevende paddenstoelen, donker sprookjesbos). Referenties: `referenties/glimwood_ballonlea/` en ongesorteerde sfeerbeelden in `referenties/sfeer_ongesorteerd/`.
   - ~~g. Mt. Coronet + Spear Pillar~~ (v0.9.198), ~~Arceus/Azure Flute/Hall of Origin~~ (v0.9.207). als je de rest hebt, Dialga, Palkia en tot slot Arceus.
     - Ontwerp (Jordi, 9 okt; ook 7F, sneeuwgebied, Spear Pillar en Hall of Origin in de referenties; DPPt-kaarten als **inspiratie, niet perfect nabouwen**; beelden in `graphics/grounded/referenties/mt_coronet/`): je begint al hoog in de berg. **4F:** een sneeuwgebied buiten (grote terrasvormige sneeuwhelling rond de top, hoog gras, rotsen, bruggetjes) en drie verbonden grotkamers (1: grote kamer met waterval in het midden en trappen; 2: kleine kamer met twee items en een rots; 3: L-vormige gang). Je gaat naar buiten, loopt om de berg heen en komt via de 3e kamer van 4F naar **5F** (trapsgewijze grotkamer, Strength-rotsen). **6F:** smalle kamer met twee trappen omhoog en twee pilaren, bovenaan de lichte uitgang naar **Spear Pillar**.
4. ~~**Yoshi's Island / Shy Guy-quest**~~ (v0.9.194): top-down in Pokémon-stijl, maar grafisch compleet anders (dat is de grap), uit Jordi's sheets (`graphics/*Yoshi*`, `bg*.png`, `misc*.png`, `world-map.png`). Shy Guys = parodie op een evil team, praten niet (sarcasme tussen haakjes). Multi battles samen met Yoshi tegen een reeks Shy Guys → Commander Boo → Wario zit erachter. Wacht deels op Jordi's assets. (8–9 okt)
6. **Regionale vormen:** Alola-Rattata/-Meowth en Galar-Farfetch'd zijn gifts (v0.9.161); de Galar-vogels horen bij de gepauzeerde Crown Tundra. (6 okt; LEGENDARY_PLAN groep 18)
7. **Contests reworken:** Jordi bedenkt zelf de ideeën; voorstel ligt klaar (QoL-pakket eerst: Berry Blender als menu, kortere wachttijden). (5–6 okt; CONTESTS_VOORSTEL)
8. **Trick House vervangen?** Wacht op Jordi's idee. (okt)
9. **The Spire (na Jordi's test, `SPIRE_TESTCHECKLIST.txt`):** gewone gevechten per deel van de act, één elite-pool per act, gevechten meer als puzzel. Nog open: codex, golven (derde vijand), dramatischer baas-intro, ja/nee bij de receptioniste, echte teksten. (okt; SPIRE_DESIGN "Nog open")
11. **Overige legendaries: gepauzeerd** (zie Besloten). Plan per groep klaar in LEGENDARY_PLAN: Kanto-vogels, Swords of Justice + Keldeo, Enamorus, Crown Tundra, Safari-trio (Xerneas/Yveltal/Zeraora), Ultra Space + Necrozma, ruïne-schatten, Zygarde, Diancie, Marshadow, Meloetta, Meltan, Pecharunt.
13. ~~**Abandoned Ship**~~ (v0.9.216) met een nachtelijk benedendek (Jordi 9 okt: prima).
14. ~~**Frontier-rentals**~~ (v0.9.215) afstemmen op de gewijzigde soorten en moves: zodra de wereld genoeg gevuld is (Jordi 9 okt).
15. ~~**Meltan**~~ (v0.9.182) als gift, evolueert in **Melmetal** door te levelen met een Metal Coat (Jordi 9 okt; plek nog kiezen).
16. ~~**Enamorus**~~ (v0.9.212) (Jordi 9 okt): zwerft rond zoals de andere Forces. Zodra die allemaal gevangen zijn, hebben bepaalde stadjes kans op Enamorus: overal hartjes en NPC's die avances naar elkaar maken; één van de koppels is **Birch met een hoop stront**.
18. ~~**Swords of Justice + Keldeo**~~ (v0.9.182) (Jordi 9 okt): Cobalion (diepste kamer Granite Cave), Terrakion (extra kamer Victory Road), Virizion (Mangrove Mire), zonder quest (zoals Gen 5). Heb je alle drie, dan belt **Mr. Briney** via de PokéNav: hij ziet iets heel geks in het water. Bij hem in de boot, fade-out, hij vaart je naar een plek die niet op de kaart staat: een pas ontstaan eiland met draaikolken; hij zet je af en daar staat **Keldeo**.
17. ~~**Altering Cave**~~ (v0.9.221): Ultra Wormhole naar Ultra Space.

## 3. Daarna: gevechtsintro's en muziek
**Jordi 9 okt:** intro's van (nieuwe) legendaries bedenkt hij zelf; thema's nog niet maken: nieuwe legendaries gebruiken `MUS_RG_VS_LEGEND` (Kanto Legendary) tot hij ermee komt.
**Intro's** (filmspeler `film.py`; alle gymleiders en de lijst van 5 okt zijn af, v0.9.92–0.9.143):
- Shy Guy (idee van Jordi), Commander Boo en Wario (Yoshi's Island). (8 okt)
- Cresselia (nu vanilla). (v0.9.122)
- Nieuwe legendaries uit de uitbreidingen: Reshiram, Zekrom, Kyurem, Spacetime Cave (Mewtwo-Cerulean, meertrio, Celebi, Dialga, Palkia, Arceus).
- Maxie & Archie: Jordi was "geen grote fan", sterker maken. (5 okt)

~~**Trainerklasse-intro's v2**~~ (v1.0.0): Fisherman, Guitarist, Hiker, Psychic, Bird Keeper, Bug Catcher, Battle Girl, Pokéfan, Collector, Aroma Lady, Parasol Lady, Ninja Boy.

**Muziek** (status uit `tools/grounded/MUZIEK.md` en de changelog):
- Wacht op Jordi's oordeel: **Neo Plasma** v12k (v0.9.109), **Brawly** v6 Rocky-stijl (v0.9.98), **Regigigas** v5, **Burglar** v1 (v0.9.93). Batch 5 (v0.9.88) was verder "zeer tot gematigd tevreden".
- Nog te maken: **Volcanion**, **Cresselia**, **Battle Stadium** (arena + finale, MUZIEK_KANDIDATEN A5), muziek voor de nieuwe uitbreidingen (Tao-eiland, Spacetime Cave, Yoshi's Island/Boo-thema: Jordi uploadt de Boo-bron).
- Route-remixes, allemaal nog niet gemaakt (MUZIEK_KANDIDATEN C): Route 135/136 winter, Fortree Jungle, Mangrove Mire, Toadstool Hollow, Safari (Fairy Forest / Thunder Plains / Haunted Camp), The Spire (per act + elite/baas), Meteor Falls (kosmisch), Flower Paradise / Liberty Garden.
- **Battle! Area Zero** (na het Area Zero main theme): opnieuw bouwen op de Area Zero Wild Battle Music uit Scarlet/Violet (op `master`: "Pokémon Scarlet & Violet - Area Zero Wild Battle Music (HQ).mp3"), stap voor stap met losse A/B per laag, met de samples van het main theme. Daarna paradoxen/Koraidon/Miraidon/Terapagos, wilde gevechten in Area Zero en het Zero Lab erop.
- **Wario** krijgt een eigen Wario-thema (Jordi 10 okt). **Ultra Beasts**: eigen thema bouwen (Rainbow Road is te euforisch).
- **Laatste nieuwe thema's (Jordi 10 okt; budget samen ±1 MB, liefst ±260–580 KB):** volgorde (1) **generiek legendary-thema** voor alle overige legendaries: episch, puur Hoenn-soundfont (percussie als Weather Trio, trompetten van de E4), stock-instrumenten; (2) **Arceus** uit `Battle_Arceus.mid` en (3) **Dialga/Palkia** uit `DialgaPalkiaMIDIBeta.mid` (beide op `master`), eerst met bestaande instrumenten; (4) **Mew**: remix van Battle! Mewtwo, minder evil/sinister, nieuwsgierig, 'de originator, geen kloon'; (5) **Ultra Beasts**: battle-regels maar maf, alsof het uit een andere dimensie komt; (6) **Legendary Birds**: voor de 1.0 het generieke legendary-thema; mogelijk een eigen thema na de 1.0 (Jordi 11 okt). Daarna alleen bij ruimte: Calyrex + paarden, Terapagos, Necrozma, Meloetta. De rest krijgt geen nieuw thema. Na elk nummer de resterende ROM-ruimte melden. Rainbow Road en Bowser Castle (MKSC, in de ROM): nog een functie zoeken.
- Delta Episode: MIDI's voor **The Heirs to Eternity** en **The Lament of Falling Stars** (Jordi levert of wij zoeken). (4 okt)
- Na de beta: Ho-Oh helderder, minder stotterende percussie. (6 okt)
- **HQ-mixer (v0.9.245): goedgekeurd** (Jordi 10 okt: lost de YI-overload op). Eventueel nog een hogere mixerfrequentie (26.758/31.536 Hz) proberen: de HQ-mixer is sneller dan de oude, en meer Hz verdeelt de resterende 8-bit-ruis over een bredere band. Uitzetten: `M4A_HQ_MIXER 0` in `include/config/m4a_mixer.h`.

## Antwoorden Jordi 9 okt (verwerkt)
- **Tao-eiland:** Dragon Tamers, verzekeringsexpert en drakentabellen blijven (alleen Gerald weg). Kyurem neutraal (geen Black/White-vorm). ~~**Ghetsis** met de **DNA Splicers**~~ (v0.9.163, Frost Hollow).
- ~~**Beacon Isle**~~ (v0.9.162, `BeaconIsle_Grotto` met Tallow): het lichteiland krijgt een kleine grot met zeldzame wilde soorten en één sterk gevecht.
- **Spacetime Cave-warps:** Cerulean Cave, Lavender Town + Pokémon Tower, National Park + Forest-tunnel naar Ilex Forest (Celebi), een representatie van de Gen 4-meren, Mt. Coronet + Spear Pillar (+ de trap naar Arceus, aan het einde), Chargestone Cave (of een versie daarvan), Glimwood Tangle, Area Zero, en ????? naar Yoshi's Island. De Mewtwo-grot in Meteor Falls verdwijnt uiteindelijk. **Per locatie eerst input van Jordi** (volledig nabouwen of eigen richting, welke assets).
- ~~**Delta Episode**~~ (v0.9.161, meteoriet in Mossdeep): Deoxys is beloning genoeg. Idee: een plek waar je Deoxys met de meteorieten van vorm laat wisselen.
- **Contests:** helemaal herbouwen, maar achteraan de lijst.
- ~~**Beasts of Ruin**~~ (gedaan v0.9.170; thema nabouwen staat nog bij muziek) **(Jordi 9 okt):** Wo-Chien, Chien-Pao, Ting-Lu en Chi-Yu, elk "gesealed" op een lege plek in de wereld, bijv. Chi-Yu in een kamer bovenin Jagged Pass die naar een vurig gebied leidt. Hun thema nabouwen (Jordi is er weg van).
- **Zacian en Zamazenta (Jordi 9 okt):** in een gebied achter een roadblock; een heel lichte visuele hint in het Mini Forest (Route 102), dat uiteindelijk het **Mega Forest** wordt, waar later meer kan.

## 4. Open vragen voor Jordi
0. **Trainer-id's zijn op** (9 okt; zie Lessen in CLAUDE.md). Jordi 9 okt: niet erg; Shy Guys worden wel trainers. Wordt het krap, dan halen we elders iets weg.
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
- **Geen charms** (Shiny/Oval/Catching/Exp. Charm). (9 okt)
- **Kecleon** is van Keccles: niet als winkelier of losse NPC.
- ~~**Elemental monkeys** blijven weg.~~ Sinds 9 okt toegestaan op passende routes.
- **Dialogen van Trick House, Battle Frontier en Battle Tents** blijven vanilla tot na de beta.
- **Na de 1.0:** extra shinies (7 kleurvarianten per Pokémon, afgeleid uit de persoonlijkheid: geen save-ruimte; ±250 KB voor gevechtssprites, ±500 KB met overworld; automatisch genereren + door Jordi laten keuren). Eerst kijken wat er na de 1.0 weg kan. (Jordi 10 okt)
- **Muziek-lint:** `music_lint.py` en `musiclib.release_ticks` laten rekenen met de echte m4a-envelope (`channel_end()` in `route119_battle_theme.py`); andere nummers kunnen ongemerkt noten verliezen.

## Kleurvarianten ("skins") — techniek klaar; recepten per groepje (eerste groep: Kanto-starters, 15 okt)
Besloten:
- Elke Pokémon krijgt een **kleurvariant** uit zijn personality (geen save-ruimte, blijft bij ruilen/evolueren). Verdeling: normaal 75%, dan 10 / 6 / 4 / 3 / 1,5 / 0,5% (zeldzamer = opvallender; Jordi 15 okt: akkoord). Geen naam in het summary-scherm.
- **Shiny blijft apart** en is de enige met sparkle; kans 1/1024 (gedaan).
- Varianten gelden overal waar het gevechts-/menupalet gebruikt wordt (gevecht, summary, pc, evolutie, contest); niet in de Pokédex. Volgers staan uit in deze rom, dus geen overworld-paletten nodig.
- Trainers (ook Frontier): standaard **normaal** (Jordi 15 okt); vaste variant met `Variant: 0–6` in trainers.party. Later eventueel: Archie/Maxie in Aqua/Magma-kleuren.
- **Evolutielijnen consistent:** variant k van Charmander hoort bij variant k van Charizard (zelfde recept per lijn); soorten die bij het evolueren van kleur wisselen mogen dat ook in hun varianten (`'soort:onderdeel'` in recipes.py).
- Werkwijze (Jordi 15 okt): Hoenn-dex eerst (vanilla 202, volgorde `HOENN_DEX_*`; groep 1 starters ✔, groep 2 ✔, groep 3 Taillow–Breloom ✔, groep 4 ✔, groep 5 ✔, groep 6 Sableye–Minun (wacht op Jordi); volgende: Volbeat/Illumise, Roselia, Gulpin, Carvanha, Wailmer, Numel), **per groepje** evolutielijnen recepten maken → contactvel (`sheet.py`) → Jordi keurt → volgende groep. Alleen soorten met een recept krijgen varianten (de rest blijft normaal). Per lijn: `ramps.py <map> [indexkaart.png]` voor de kleurgroepen, recept in `recipes.py`, `variants.py` draaien. Delen ogen een index met een ander onderdeel: eigen index via `sprite_fixes.py`. Nog te doen: Mega/Gmax-vormen (submappen) meenemen.
- Schatting: Hoenn-test ±1–1,7 M tokens, rest van de dex ±1–2 M.

Recepten (Jordi 15 okt; niet 1000 × 7 handpicken, maar deze filosofie toepassen):
- **Zwart** (zoals shiny Rayquaza) en **albino**.
- **Starters elkaars kleuren:** Bulbasaur/Charmander/Squirtle (en elke startergeneratie) in elkaars neutrale kleuren.
- **Anime-versies:** bijzondere kleuren uit de anime (Ash's Noctowl, roze Butterfree, de roze Pokémon van het eiland).
- **Smash Bros-kleuren:** iconische alternatieve kostuums uit Smash horen bij de opties.
- **Grounded dierenvormen:** echte ondersoorten/kleurvormen (Ducklett als eendensoorten; Grimer/Trubbish als soorten afval).
- **Esthetisch vet:** felle, crispe kleuren die er gewoon goed uitzien.
- **Cosplay/job/lore/reference:** clown, mythen/legendes, andere games (Samus, Link, Cuphead, Shovel Knight, Pizza Tower, Yoshi, Mario, ...).
- **Verwante Pokémon** geven elkaar hun kleurpatroon.
- Een aantal krijgt **Pikachu-kleuren** of een **Poké Ball-palet** (Voltorb/Electrode: Great/Ultra/Master/Premier).
- **Neon/cyberpunk** en andere populaire kleurenpaletten.
- **Vermijden:** echt rare of vloekende kleuren (tenzij specifiek grappig), en varianten die nauwelijks verschillen van normaal (geen "shiny Garchomp"-situatie; bijv. teal Squirtle lijkt op de gewone).
- **Per onderdeel kleuren, niet één tint over alles** (Jordi 15 okt): een Pokémon bestaat uit meerdere kleurgroepen (lijf, buik, vlam, bloem, ogen); pas er één of meer aan en houd de schaduwen erin. Vuur mag spelen: blauwe, groene, witte vlam (met tinten); **vlam in contrast met de huid** (Jordi 15 okt), liefst realistische vlamkleuren (wit, blauw, groen, violet, karmijn).
- **Zwart:** schaduwen juist versterken (`'l': 1.3`), anders wordt een kleine sprite een vormloze vlek.
- Past bij de rom zelf: typing/abilities van revisies meenemen (Shiftry Grass/Ice = winterdemon).
- Geen kleuren van een echte regionale vorm van dezelfde soort (Galar-Zigzagoon: verwarrend; Jordi).
- **0,5% gevarieerd houden** (Jordi 15 okt): neon/vaporwave niet standaard; meer soorten patronen en thema's (popcultuur, mythen, materialen). Hoogtepunt volgens Jordi: Oni-Shiftry (thema dat bij de soort past).
- **Metalen en edelstenen** (Jordi 15 okt): goud, zilver, brons, koper, diamant, robijn, smaragd, saffier enz. voor Pokémon die op erts/gesteente gebaseerd zijn (Geodude, Nosepass, Aron, Carbink...).
- **Shiny eerst bekijken** (kolom 2 van het contactvel) vóór je een thema kiest: Geodude/Graveler goud, Azumarill geel, Skitty oranje, Nosepass bruin.
- Voorbeelden die Jordi geniaal vond: Toad (Breloom), amethistzwam, Kumamon, Mewtwo-kleuren (Abra), Garfield, Oni-Shiftry, Okami-Poochyena; en evolutiewissels (Magikarp ↔ Gyarados).
- Gepaarde soorten (Plusle/Minun, Volbeat/Illumise): binnen één variant contrasteren, niet dezelfde kleur.
- Pokémon-games als thema (Sableye: Gold/Silver/Crystal enz.) viel goed; een sprite met meerdere edelstenen/onderdelen kan per onderdeel een eigen kleur krijgen (sprite_fixes).
- Varianten onderling en t.o.v. shiny vergelijken: twee blauwe in één lijn = één vervangen.
- **Albino:** gebroken wit met volledige schaduwen (de belichte rand is de hoofdkleur van het lijf: nooit puur wit, anders valt de omlijning weg), **rode ogen**, donkerdere vlekken blijven donkerder, een andere kleur bol/bloem; een witte vlam houdt tinten.

## Wiki / encyclopedie — start na Jordi's volledige testrun (Jordi 15 okt)
- Generator `tools/grounded/wiki/build_wiki.py` leest de **code zelf** (species_info, `gen_9.h`, moves_info.h, items.h, wild_encounters.json, trainers.party, map-scripts) en maakt een statische site; opnieuw draaien na elke wijziging.
- **Focus op wijzigingen:** automatisch vergelijken met de originele pokeemerald-expansion (labels "gewijzigd"/"nieuw", met oud → nieuw), filters als "alleen gewijzigd".
- Onderdelen: Pokédex (types, stats, abilities, evolutielevels, learnsets, vindplaatsen), moves, items/TM's met vindplaats, trainers/gyms, tips & tricks/QoL (met de hand, eerste versie uit CLAUDE.md + changelog).
- Wiki-opzet: een eigen pagina per Pokémon/move/item/locatie met onderlinge links, zoekbalk via een zoekindex in de browser (bijv. Pagefind). Sprites uit `graphics/pokemon/`, ingekleurd per palet: normaal, shiny en de kleurvarianten ("skins") met afbeelding.
- **Openbaar voor vrienden/testers:** statische HTML naar een apart openbaar repo met GitHub Pages; spoilers (legendaries, post-game, Spacetime) achter uitklapblokken, geen debug-info, geen ROM.
