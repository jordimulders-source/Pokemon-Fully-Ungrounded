# Changelog – Pokémon Fully Ungrounded

De changelog van Pokémon Ungrounded staat in `docs/ungrounded/CHANGELOG_UNGROUNDED.md` (inclusief alle Pokémon-revisies, die in dit project gelden).

### [v0.0.1] - Fork van Pokémon Ungrounded
- Nieuwe repo `Pokemon-Fully-Ungrounded` met de volledige geschiedenis van Ungrounded (basis: `claude/dazzling-babbage-ud6oxr`, 22 okt) en daarmee van pokeemerald-expansion 1.14.4.
- Opgeruimd: 72 bronbestanden in de hoofdmap (mp3's, zips, gsf-rips, losse plaatjes en MIDI's); 35 plannings-/ontwerpdocumenten van Ungrounded naar `docs/ungrounded/`.
- Nieuw: `docs/concept/IDEEEN.md` (brainstorm), `TODO.md` (fases van het skelet), CLAUDE.md bijgewerkt voor het nieuwe project.

### [v0.0.2] - Spire, Battle Stadium en Battle Casino eruit; concept en regiokaart
- **Verwijderd:** The Spire (code, kaart, graphics, save-blok, alle gevechtshooks), het Battle Stadium (72 Stadium-trainers, 130 partners, 49 ongebruikte trainerfoto's, kaarten, slides) en het Battle Casino (kaart, specials, flags). Gewone gevechten werken zoals voorheen; gimmicks blijven uit. `VAR_STADIUM_STATE`/`VAR_CASINO_BETS` zijn weer vrij (`VAR_UNUSED_0x40B8`/`0x40BB`). ROM: 492 KB → 814 KB vrij.
- Bewust blijven staan: 7 ongebruikte Kanto/N-overworldsprites (hernummeren is riskant), Stadium-trainerklassen, de trainerfoto-generatoren (maken ook nog gebruikte foto's), de Frontier-kaarten (gaan mee met Hoenn).
- **Concept:** `docs/concept/CONCEPT.md` (besloten: starters Fighting → Dark → Psychic, gym 1 Ground in Uyuni, gym 2 Ice, gymtypes en E4, Inca-trio + Pachamama, toon) en `docs/concept/IDEEEN.md`.
- **Regiokaart, schets 1:** `docs/concept/regiokaart_namen.png`, met `tools/concept/regiokaart.py` in de stijl van de Emerald-kaart (kleuren en stadsiconen uit `graphics/pokenav/region_map`).

### [v0.0.3] - Spacetime en Ultra Space eruit (deel 1); concept, sprites en tilesets
- **Verwijderd:** de kaartgroepen Spacetime en Ultra Space (66 kaarten, 63 layouts, 65 tilesets), Azure Flute, Gen 1-GHOST, Ultra-portalen, 71 trainers (o.a. Shy Guy), 18 trainerfoto's, Yoshi/Calyrex-partners, 33 overworld-sprites, de Wario/Boo/Shy Guy-transities. Keccles blijft. ROM: 814 KB → 1,94 MB vrij. Muziek van die gebieden staat er nog (zie `docs/concept/STAND_TECHNIEK.md`).
- **Concept:** opgesplitst in CONCEPT/REGIO/VERHAAL/POKEMON/MUZIEK; dex-selectie voorlopig af (±441 soorten); gymlocaties; protagonist, Keccles als compagnon.
- **Sprites:** starters fase 1, rondes 1–4 (`docs/concept/sprites/`), spriteplan met Pokémon-design-sectie.
- **Tilesets:** assetbibliotheek (`tilesets/`), Andes-primary, La Paz en altiplano ronde 2, `TILESET_PLAN.md`.

### [v0.0.4] - Alle Ungrounded-muziek eruit; concept aangevuld
- **Verwijderd:** alle eigen muziek van Ungrounded (songs 610–725: eigen composities, covers, gym-/legendary-/personagethema's, alle remixes, nachtversies, YI/MKSC/WL4-rips, Area Zero, Poké Tower-remix), 143 voicegroups, 490 samples, 72 generatorscripts. Alleen de vanilla-/FRLG-muziek en **Battle! Keccles** (nu song 610) blijven; HQ-mixer blijft. Legendaries vechten op vanilla-muziek (Rayquaza, Regi, Mew, Mewtwo, Deoxys, beasts, overige `MUS_RG_VS_LEGEND`). ROM: 1,94 MB → 7,42 MB vrij.
- **Concept:** de OST wordt grotendeels nieuw; Quaxly-lijn in de dex (444 soorten); Kecleon vast in de dex; legendaries voorlopig alleen Mew, Mewtwo, Zarude; regional forms: Lotad (reuzenwaterlelie, stapstenen), Yanma (Dragon), Natu/Xatu (nominatie, Nazca-kolibrie); fakemon: mug (Poison/Electric), Flamigo-evolutie, pauw/zonneral met carnavalsinspiratie; Laguna Colorada en Isla Incahuasi komen in de game.

### [v0.0.5] - Intro's en films eruit; concept aangevuld
- **Verwijderd:** alle legendary-intro's, de gym-, rivaal- en personage-intro's en films (Steven, Wally, Colress, SickBlik e.d.), de soort-intro's (Pikachu, Magikarp, Psyduck, Koffing, Zangoose, Seviper, Zarude), de route-transities per gebied, 37 generatorscripts, 335 transitiegraphics en de bouwscripts van Spacetime/Ultra Space/YI/Glimwood/Chargestone/Coronet/Hall of Origin/lakes/National Park. Legendaries vallen terug op vanilla-transities (Groudon/Kyogre/Rayquaza/Regi's eigen, de rest Blur). **Blijven:** de klasse-intro's, alles van Keccles, de zee-/onderwatertransitie, alle tilesets en graphics-bronnen. ROM: 7,42 MB → 9,30 MB vrij.
- **Plan:** `docs/concept/PLAN_HOENN_ERUIT.md` (hele Hoenn-wereld eruit in 9 stappen).
- **Concept:** DJ Rotom (Electric/Steel, inspiratie in `docs/concept/sprites/dj_rotom/`), Cuyby (originele Normal-cavialijn), Carbink terug (carbunclo), ideeën: ruïne-Pokémon (Rock/Ghost of Rock/Psychic), jaguar, cactusopties (zuilcactus, regional forms van Cacnea/Maractus).

### [v0.0.6] - De Hoenn-wereld eruit (stap 1–6); concept: routes, dungeons, mythologie, gymlevels
- **Skelet:** nieuwe kaartgroep `gMapGroup_FullyUngrounded` (bouwscript `tools/grounded/maptools/skelet_maps.py`, bewaarlijst `skelet_keep.py`): StartTown (plaatshouder, kopie van Oldale), Pokémon Center 1F/2F en Mart (precies zoals ze waren), zeven stock-interieurs, en een TestMap (Route 102 met wilde Pokémon, water, bessenbomen, Keccles, PC). Nieuw spel start in StartTown; uitwitten naar het Pokémon Center. Debug Zone warp bijgewerkt.
- **Weg:** 648 kaarten, 542 layouts (12 blijven), 22 heal locations, alle wilde tabellen behalve de TestMap, 1036 trainerteams (behalve Keccles en wat algemene scripts nog nodig hebben: Burglars, Gabby & Ty, Phillip, SickBlik), rematchtabel en Match Call als plaatshouder. Tilesets en graphics blijven. Een overgangsheader (`include/constants/map_compat.h` + stubs) houdt de oude C-code bouwbaar tot stap 7. ROM: 9,30 MB → 11,32 MB vrij.
- **Let op:** oude saves en savestates werken niet meer (nieuw spel nodig). Testen: `warp MAP_TEST_MAP, x, y`.
- **Concept:** gymvolgorde en -plekken akkoord (Ice in de Cordillera Real), Fly na gym 4, routes per segment (`ROUTEPLAN.md`), originele dungeons (`DUNGEONS.md`), mythologie (`MYTHOLOGIE.md`), Titicaca met verzonken stad, Inca Trail als Victory Road, Galápagos (vangen zonder gevecht), Mew-dungeon in Guyana, Zarude diep in de jungle, legendary-plekken rond het startgebied, gymlevels 18–75 en League 80–90.

### [v0.0.7] - Pokémon buiten de dex eruit; starters ronde 5; 100 fakemon-pitches
- **Verwijderd uit de ROM:** 326 families (212 uit categorie C, 114 legendaries/mythicals/Ultra Beasts/paradoxen) en alle Mega-, Gmax-, Ultra Burst-, Tera- en Primal-vormen, plus 51 losse vormen (o.a. niet-gekozen regionale vormen, totems, Tyrogue/Hitmonlee/Hitmonchan; gewone Meowth/Persian en Grimer/Muk: Galar-Meowth en Hoenn-Grimer zijn de basisvorm). Behouden: 440 dexnummers / 582 soortconstanten, met Mew, Mewtwo en Zarude. Kreten 8,39 → 3,71 MB, Pokémon-data 4,58 → 2,17 MB. ROM: 11,32 MB → 18,5 MB vrij. Bronbestanden blijven in de repo; terughalen = één schakelaar. Lijst: `docs/concept/DEX_IN_ROM.md`.
- Starterkeuze is tijdelijk Bramblin/Charcadet/Quaxly; testmon in CLAUDE.md is nu Mewtwo.
- **Sprites:** starters ronde 5 (nachtaap: lijf ronde 4 + nieuwe ogen; olinguito: met de hand per pixel, Hoenn-starterformaat).
- **Concept:** `FAKEMON_PITCH.md` (100 pitches), Spaceworld-ontwerpen (Norowara, Kyonpan vrijwel zeker; Raitora als jaguar), gymlevels, routeplan.

### [v0.0.8] - Eerste Fully Ungrounded-muziek, regiokaart 3, sprites Cuyby en DJ Rotom
- **Muziek:** gedeelde Zuid-Amerikaanse instrumentenset (`tools/grounded/fu_samples.py`, 39 samples in `sound/direct_sound_samples/fu/`, voicegroup `fu`): charango, quena, zampoña, accordeon, trombone, nylongitaar, cuíca, 808-bas, supersaw, en slagwerk (dembow, bombo, cajón, bongó, conga's, güiro, shaker, claves, caixa, surdo, tamborim, agogô, apito). Zes originele schetsen als songs 611–616 (`tools/grounded/fu_themes.py`): instrumentendemo, altiplano-route, wild gevecht (Andes), La Paz, reggaeton-bende, samba; nog niet aan kaarten gekoppeld. Previews in `docs/concept/muziek/previews/`. Kosten ±205 KB.
- **Regiokaart variant 3** (`tools/concept/regiokaart3.py`, `docs/concept/regiokaart3_namen.png`): alle gyms, hoofdpad volgens het routeplan, spoor Uyuni–Oruro–La Paz, legenda met plekken zonder icoon. Variant 2 blijft de basis tot Jordi kiest.
- **Sprites:** alpaca ronde 5; Cuyby ronde 1 (A: kuif/rozet, B: Andesmuts); DJ Rotom ronde 1. Overzichten in `docs/concept/sprites/starters_fase1_ronde5.png` en `cuyby_djrotom_ronde1.png`.
- ROM: 18,32 MB vrij.

### [v0.0.9] - Hoenn-code opgeruimd (stap 7)
- 24 systemen opgeruimd (zie `docs/concept/PLAN_HOENN_ERUIT.md`, "Stand (23 okt)"): Pokémon Center wordt aan de layout herkend (healen, saven, uitwitten werken in elke nieuwe stad), Hoenn-specials en hun scripts weg (o.a. truck-intro, SS Tidal, kabelbaan, gympuzzels, braille, Mirage Tower, Regi-stippen, Faraway Island, post-game-rivaal), roamers zonder routes, Fly alleen naar StartTown, Pokédex-gebiedsscherm op kaarttype. Mechanieken zonder plek slapen tot de nieuwe regio (Forces, Enamorus, Burglar, draaihekken, Safari Zone, volgerberichten).
- Evoluties op een plek (Magnezone, Vikavolt, Leafeon, Glaceon, Crabominable) tijdelijk alleen met hun steen; Alolan Exeggutor tijdelijk op level-up met een Dragon-type in het team (open in POKEMON.md).
- Mom staat in het stock-huis (TwoStory) met haar standaardtekst, healen en PokéNav-registratie.
- Overgangslaag: 233 → 64 kaarten, 651 → 592 stubs; de rest hoort bij stap 8 (Frontier, Union Room, Contests, Secret Bases, Trainer Hill; inventaris met ROM-kosten in het plan). ROM: 18,38 MB vrij.

### [v0.0.10] - pokeemerald-expansion 1.14.4 → 1.17.1
- **Upstream-merge naar expansion 1.17.1** (TODO-stap 4). Nieuwe gevechtsmotor (cancelers, opgesplitste moveend, `battle_move_resolution.c`, volatiles in `gBattleMons[].volatiles`, statwijzigingen via een wachtrij; macro `queuestatchange` toegevoegd). Alle eigen moves/abilities/scripts omgezet of opnieuw geschreven (o.a. Kelp, Innard Punch, Overkill, Lure Light, Flash, Eye Spots, Super Splash, Totem Gaze/Burrow Maze, Weather Report, Pack Howl; Acid Rain en Pollen Haze als `EFFECT_WEATHER`). Spicy Spray en Eelevate gebruiken nu de upstream-versie (zelfde effect); Aura Guard blijft de onze.
- Zes regressies gerepareerd (Life Buoy, Wind Chime, Primeval Ward, Tusk Tumble, Venom Dust/Beaver Dam, Acid Rain/Pollen Haze-type). Eigen tests: 223 PASS, 0 FAIL (was 217/2 + 4 timeouts).
- Niet meegekomen: het nieuwe debug-geef-Pokémon-menu van upstream; kleurvarianten voor Frontier-tegenstanders.
- FRLG-code zit nu in upstream en kost ±0,4 MB (Kanto-regiokaart, Trainer Tower, Seagallop e.d.): kan weg bij stap 8/9. ROM: 17,86 MB vrij.
- Details en lessen: `docs/concept/STAND_TECHNIEK.md` (stap 4), `docs/lessen/AGENTS.md`.

### [v0.0.11] - Spriterondes starters en Cuyby-evolutie (Dragonfly Cave-lessen)
- Spritinglessen uit de Dragonfly Cave-gidsen toegepast; `docs/lessen/SPRITING.md` kreeg een verplichte checklist (§0: diagonale pose, ledematen tellen, geen rechte lijnen, ogen, silhouet, formaat, dynamische pose).
- **Nachtaap ronde 10: goedgekeurd (voor nu).** Feller violet, lichter gezicht, neutrale "uncanny schattige" blik, Nazca-spiraal los van het oor, pruim-pupillen.
- Olinguito ronde 10–11 (klauwen, ogen diagonaal, buikcirkel weg); ronde 12 loopt (mond, klauwen, kleinere poten, dynamischer pose).
- Alpaca ronde 10 afgekeurd (geen alpaca, te groot); ronde 11 from scratch loopt (één vachtkleur, handschoenen met Andes-breikleuren).
- Cuyby-evolutie ronde 2 (vacht i.p.v. gras, mooi shading/kleur); ronde 3 loopt (diagonaal, pluiziger, onverzorgd, referentiefoto's langhaarcavia).
- Les: verzonnen kleurvlakken mogen, als ze werken (`FAKEMON_DESIGN.md`).

### [v0.0.12] - Cuychu goedgekeurd, alpaca en olinguito verder
- **Cuychu** (evolutie van Cuyby, naam: cuy + ichu): sprite ronde 4 goedgekeurd. Keuring tegen 14 Gen 3-sprites (`cuyby_evo/ronde3/KEURING.md`); snuit kleiner, pony over de bles.
- Alpaca ronde 12 (kop omgebouwd, "Chernobyl") afgekeurd; ronde 13 = kop ronde 11 + kleuring/lijf ronde 12, vuisten weer op de grond. Bijna klaar; hint naar de evoluties nog te kiezen.
- Olinguito ronde 12–14 (mond, klauwen, 3/4-constructie, romp naar Mightyena); lijf bleef onnatuurlijk, ronde 15 tekent het over op het lijf van een echte Gen 3-viervoeter.

### [v0.0.13] - Alpaca goedgekeurd
- **Alpaca ronde 15 goedgekeurd:** kop ronde 11, kleuring/lijf ronde 12, vuisten op de grond, zwart oog met glans, vlechtkwastjes met rood knoopje en een aguayo-band in de halswol als hint naar fase 2 (kragen) en fase 3 (vlechten, manta). Neusstreep op verzoek weggehaald.
- Olinguito ronde 15 (lijf over Poochyena als skelet) voorlopig goed; onafhankelijke keuring volgt.
- Showcase-vel Cuyby + Cuychu (`docs/concept/sprites/showcase/`).

### [v0.0.14] - Alpaca klaar, olinguito ronde 16, vaste fakemon-werkwijze
- **Alpaca (fase 1) klaar** na onafhankelijke keuring: open randen dicht, achterpoten los, linkervoorpoot smaller; staartje omhoog gehouden (Jordi: leuker dan het lage, "dan maar minder immersie").
- **Olinguito ronde 16:** ronde kop, grotere ronde oren, masker met twee lobben en golvende rand, amandelogen met donker bovenlid, taps toelopende haakstaart. Palet blijft donker (Dark-type). Masker en oren: "uitstekende verbeteringen" (Jordi).
- **Vaste werkwijze per fakemon** (bovenaan `docs/lessen/FAKEMON_DESIGN.md`): ontwerp → silhouet op echt skelet → sprite + checklist → onafhankelijke keuring vóór Jordi → alleen benoemde reparaties; doel ≤ ±5 rondes.

### [v0.0.15] - Vormstudie en fakemon-checklist
- Studie van alle 1024 front-sprites (386 Gen 3 + 638 Gen 4–9) op vorm, pose en verhoudingen: `docs/lessen/vormstudie/` (STUDIE.md met 25 verbanden en 15 posetypes, contactvellen, metingen).
- `docs/lessen/FAKEMON_CHECKLIST.md`: 30 toetsbare punten (harde eisen/richtlijnen) + sjabloon "Pose kiezen" en mini-sjablonen per bouwtype; verplicht in `SPRITE_OPDRACHT.md`.
- `SPRITE_OPDRACHT.md` (vaste opdracht voor elke sprite-agent) en per Pokémon een `AFGEKEURD.md` (olinguito) tegen het herhalen van afgekeurde wijzigingen.
- Olinguito: rondes 17 en 19 afgekeurd; Galar-Linoone als leidraad; stap-voor-stap (kop → achterpoot → klauwen).

### [v0.0.16] - Checklist toegepast op de goedgekeurde sprites, kolibrie gestart
- Alle keuringspunten toegepast; Jordi koos: Cuyby ronde 4 (ronde 5 afgekeurd: voet in het lijf), Cuychu ronde 6 (pluk + diepere inkepingen + kussen weg), nachtaap ronde 12 met kleinere spiraal (950 px), alpaca ronde 17 met schuine hals en grotere kop.
- Olinguito: stap 1b (gezicht naar Galar-Linoone), ronde 20–21b (masker, hak, Sandslash-klauwen, dikke poten); ronde 22 loopt (poten zoals Linoone, diagonaal lopen).
- Kolibrie (testcase werkwijze met referenties): Ghost + Fairy/Flying, zielenbode (Guaraní mainumby, torpor van de Andes-hillstar); referentiefoto's, mythen met bronnen en drie concepten in `docs/concept/sprites/kolibrie/`.
- Nieuwe vaste regels: referentiemateriaal per fakemon, Jordi letterlijk citeren, diagonaal lopen (geen telgang).

### [v0.0.17] - Olinguito-ontwerp geschrapt
- Na ±30 rondes (incl. finale met onafhankelijke keuring) schrapt Jordi het olinguito-ontwerp en begint opnieuw met een eigen, andere aanpak. Rondes en keuringen blijven als naslag in `docs/concept/sprites/olinguito/`.
- Cuyby ronde 6: oranje/zwart gewisseld en zwart rond het rechteroog (consistent met Cuychu); wacht op akkoord.
- `docs/lessen/SPRITE_NORM.md` (één pagina norm voor sprite-agents), regel "zelfgenoemd zwak punt = fail", les "bouwtype bepaalt de moeite".

### [v0.0.18] - Kolibrie: ontwerp, silhouet en kleursprite
- Kolibrie (Ghost/Flying, eindvorm): modeltekeningen v1–v8 (`docs/concept/ontwerp/kolibrie/`) liepen vast; daarna silhouet op een skelet: Talonflame (v1–v4), daarna Jordi's foto's (v5–v6). **Silhouet v6 goedgekeurd** (pose van een drinkende kolibrie, jeguaka-kuif, drie slierten met zielvlammetjes).
- Kleursprite in 4 rondes met een sprite-agent en een onafhankelijke keurder (`docs/concept/sprites/kolibrie/ronde1–4`, `KEURING.md`). Fluweelpalet, vleugels doorschijnend zoals Venomoth. De slierten op het goedgekeurde silhouet lazen als poten (mug); de variant met een naar achteren slepende staart komt door de keuring. Eindversie: `docs/concept/sprites/kolibrie/eind/kolibrie.png` (wacht op Jordi: staart wijkt af van silhouet v6).
- Referenties van Jordi in `docs/concept/sprites/kolibrie/referenties/`; SPEC.md per onderdeel; lessen in FAKEMON_DESIGN.md.

### [v0.0.19] - Kolibrie: volume en oog
- Jordi over de eindversie: "erg mooi", maar "nog net iets te 2d qua shading" en "het oog is nog niet helemaal pokemon" (klein houden, "zoek naar pokemon met minimale ogen"). Staart naar achteren daarmee goedgekeurd.
- Ronde 5 (`docs/concept/sprites/kolibrie/ronde5/`): 102 px omgekleurd binnen hetzelfde silhouet: bolle kop (kapje + schaduw op wang/keel), schuin hooglicht op de borst, schaduwband onder de buik, gewelfde vleugelwortel, slierten met licht- en schaduwkant. Oog 2×3 als kraaloog naar Corviknight/Kilowattrel (zwart lid, glans, blauwgroene iris). Onafhankelijke keuring GOED.

### [v0.0.20] - Kolibrie: eindkeuring
- Nieuwe, onafhankelijke eindkeuring op alle richtlijnen (`docs/concept/sprites/kolibrie/ronde5/EINDKEURING.md`): alles PASS behalve open randen aan de bijna-witte kuiftoppen; 4 px omgekleurd naar de bleke omlijningstint (silhouet gelijk). Resultaat: `docs/concept/sprites/kolibrie/af/kolibrie.png`.
- Retrospectief kolibrie vs olinguito + aanbevelingen voor een sprite-editor: `docs/lessen/RETRO_KOLIBRIE.md`.

### [v0.0.21] - Kolibrie goedgekeurd
- Jordi keurt de kolibrie-frontsprite officieel goed (`docs/concept/sprites/kolibrie/af/kolibrie.png`). Twijfel over het zijaanzicht weggenomen: veel echte sprites zijn zijaanzicht (Yanma, Ninjask, Swellow, Taillow, Wingull, Skarmory, Latias en veel vissen); vergelijkingsvel `af/zijaanzicht_vergelijking.png`.
- Nog te doen: frame 2, rugsprite, icoon, shiny-palet, naam en data.
