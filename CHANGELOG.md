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

### [v0.0.22] - Olinguito v2 goedgekeurd + vaste sprite-werkwijze
- Olinguito v2 (Dark-starter): hoek gekozen met het 3D-poppetje (B2: lijf 40°, kop 49°, kantel 8°, Linoone-perspectief); silhouet = de B2-render verkleind (massa), met de hand opgeschoond (klauwen aan elkaar, oor, kop, achterpoten, staart; ronde 5); kleur in 4 rondes met een maker-agent, eigen controle en een onafhankelijke keuring. Jordi: "het beste olinguito ontwerp wat ik tot nu toe heb gezien"; goedgekeurd: `docs/concept/sprites/olinguito_v2/af/olinguito.png`.
- Nieuwe vaste werkwijze voor alle sprites: `docs/lessen/SPRITE_WERKWIJZE.md` (Jordi: "de beste methode", "zodat alle nieuwe gesprekken vanaf nu het zo oppakken"); verwijzingen in CLAUDE.md en FAKEMON_DESIGN.md.

### [v0.0.23] - Olinguito v2 af na eindkeuring
- Verse eindkeuring (`docs/concept/sprites/olinguito_v2/af/EINDKEURING.md`): hoofdvraag PASS; reparaties: verre voorpoot roze voetje (2 px), losse spriet onder de klauw weg en drie haakjes van 1 px in curven glad (Jordi akkoord). 0 open randen. `docs/concept/sprites/olinguito_v2/af/olinguito.png` is af.

### [v0.0.24] - Coathief: start (stap 0)
- Evolutie van de olinguito (fase 2, coati) heet **Coathief** (Jordi). Map `docs/concept/sprites/coathief/` met `SPEC.md` en `referenties/` volgens `SPRITE_WERKWIJZE.md`; stap 1: referentiefoto's van Jordi in `referenties/`, besloten: *Nasua nasua*, bivakmuts-kop met zwarte neus, langer lijf, geringde staart, confrontatie-looppose; 3D-poppetje met hoekenraster (`ontwerp/hoeken.png`) wacht op Jordi.

### [v0.0.25] - Coathief: ontwerp gekozen, silhouet ronde 1
- Kop-test A/B/C op hoek B1: Jordi koos **C** (zwarte bivakmuts met echte coati-vlekken boven en onder het oog, zwarte neus); kleiner oog.
- Poppetje bijgesteld zodat de pose op 64 leest (kop omhoog, opgetilde voorpoot hoger, verre poten in een eigen kolom); silhouet = de render direct verkleind + handreparaties aan voorpoten/klauwen en een achtervoet (46 px, 0 buiten de zones): `docs/concept/sprites/coathief/silhouet/vel_ronde1.png` (1297 px).

### [v0.0.26] - Coathief af (frontsprite)
- Evolutie van de olinguito, **Coathief** (*Nasua nasua*, fase 2): frontsprite goedgekeurd, `docs/concept/sprites/coathief/af/coathief.png`. Zwarte bivakmuts-kop met coati-vlekken, zwarte neus en oren, klein roodbruin oog, warm roodbruin lijf (donkerder dan Linoone/Furret), geringde staart, klauwen aan beide voorpoten; driekwart naar de speler toe lopend met één poot opgetild.
- Werkwijze: 3D-poppetje (hoek B1, kop C), silhouet direct verkleind, kleur met één maker-agent, een onafhankelijke keuring, een evolutiekeuring en twee verse eindkeuringen. De voorpoten pas goed na een **overtrekvel met pixelraster** waarop Jordi cellen aftekende; vastgelegd in `docs/lessen/SPRITE_WERKWIJZE.md`, met gemeten tokenkosten.
- Nog te doen: frame 2, rug, icoon, shiny, data; A/B-test kleine kleurreparaties (SPEC).

### [v0.0.27] - Ideeënlijst 29 okt verwerkt
- Jordi's nieuwe lijst (Bartitsu-Mr. Rime, capoeira-Hitmontop met evolutie, BJJ, Arbok, zout-Sandaconda, kaaiman-Krookodile, harpij, Oricorio-samba/tango/cumbia, hoatzin-Archeops, poedelmot, Tiwanaku-Golett, açaí, pitahaya, plátano-Tropius, carambola, gaucho, guaraná, Galápagos-vormen, fruitvampier, Electric viscacha) uitgewerkt in `docs/concept/IDEEEN.md`, met types en dex-status uit de repo en overlap met eerdere plannen.
- Besloten in `POKEMON.md`: harpij komt er sowieso; capoeira-Hitmontop krijgt een evolutie; viscacha wordt Electric.

### [v0.0.28] - Lama (alpaca-evolutie): start (stap 0)
- Fase 2 van de Fighting-starter: map `docs/concept/sprites/lama/` met `SPEC.md` en `referenties/` volgens `SPRITE_WERKWIJZE.md` (Coathief als voorbeeld). Vastgelegd: wat uit fase 1 meegaat, Jordi's eerdere woorden over de lijn (wolkragen om de poten, vier poten, andere vechtsport dan capoeira), formaatdoel 1100–1550 px, verschil lama/alpaca. Stap 1 (vechtsport, pose + foto, kleur, naam) wacht op Jordi.

### [v0.0.29] - Nachtaap fase 2: voorbereiding
- Map `docs/concept/sprites/nachtaap_evo/` met `SPEC.md` (lijn, wat uit fase 1 meekomt, afgekeurd) en `referenties/` (fase 1 goedgekeurd, vel met skelet-kandidaten: Aipom, Monferno, Kadabra, Kirlia, Vigoroth, Grovyle, Medicham, Lombre, Grumpig, Primeape).
- Ontwerp-brainstorm met Jordi loopt (richtingen: nachtwaker, maangezicht, sterrenlezer, leerling-genezer, drager); nog niets besloten.

### [v0.0.30] - Lama: richting stap 1
- Jordi: geen BJJ (wordt een losse fakemon), de lama draagt traditionele Andes-kleding die per fase ontwikkelt, voorlopig MMA-handschoenen, kleur echt lama, fase 3 duidelijk anders en volwassener. Vastgelegd in `docs/concept/sprites/lama/SPEC.md` met een voorstel voor de kledinglijn.

### [v0.0.31] - Lama: foto's en poppetje
- Jordi's foto's in `docs/concept/sprites/lama/referenties/` (pose = foto 1, oorkwasten/aguayo, bonte vacht, MMA-handschoenen). Fase 2 is een tussenvorm (Marshtomp/Charmeleon-idee), vacht iets donkerder dan de alpaca.
- 3D-poppetje met de kledinglijn (`ontwerp/pop3d_lama.py`), vel `ontwerp/vel_ronde1.png`: drie verhoudingen en drie vachten. Open: keuze, en of fase 3 een guanaco wordt.

### [v0.0.32] - Nachtaap fase 2: richting gekozen
- Jordi kiest **nachtwaker met maangezicht**: gehurkte/hangende pose met de ogen recht in de camera, lijf groter t.o.v. de kop. Vier foto's in `docs/concept/sprites/nachtaap_evo/referenties/` + vel met sprites die ook zo kijken (Zorua, Sableye, Slakoth, Mew, Espeon, Persian, Eevee…). POKEMON.md en SPEC bijgewerkt.
- Pose-referenties met de rug boven de kop (Jordi: "een pose van een pokemon waar het rug een beetje boven het hoofd uitsteekt"; tak niet in beeld): `referenties/rug_boven_kop.png`.
- Pose = Lairon (Jordi). 3D-poppetje van de nachtaap in die pose, met foto 1/4 als inspiratie voor massa en gezicht: `docs/concept/sprites/nachtaap_evo/pop3d/` (rasters met lijf 30–50°, kop 55–90°, staart omlaag of omhoog). Wacht op Jordi's keuze van de hoek.
- Poppetje bijgewerkt naar Jordi's keuze A2 van het staart-omhoog-vel (lijf 40°, kop 80°; eerst ten onrechte kop 65° door dubbele labels) met de staart omhoog: voorpoten verder teruggetrokken, vacht donkerder dan fase 1, halve manen boven de ogen duidelijker, grotere spiraal (`pop3d/a2_staart_omhoog.png`). Ogen en neutrale mond volgen in de kleurstap.
- Lijfmotieven op het poppetje (Jordi: "we kunnen ook iets qua motief met het lichaam doen, want dat is nu wel erg effen"): effen, oranje borst, borst + halvemaan op de flank, borst + sterren, borst + maanfasen; met 1×-voorbeeld (`pop3d/motieven.png`).
- Halve maan nu als één sikkel op het voorhoofd met de punten omlaag (Jordi); middenstreep loopt eronder tussen de ogen door. Lijfpatronen die van bovenaf gecentreerd zijn (ontworpen in uitgerolde rugcoördinaten, lopen over beide flanken omlaag): Shipibo-kené en chakana (`pop3d/motieven2.png`, met bovenaanzicht).
- Kop volgens Jordi's krabbel (`referenties/jordi_krabbel_halvemaan.png`): het enige wit is één grote halve maan over de helft van de kop, over de ogen heen, punten omlaag; gezichtsschijf, zijstrepen en middenstreep weg. Borstvlak weg ("vind ik er niet mooi uitzien"). Lijfpatroon: kené (`pop3d/kop_halvemaan.png`).
- Halve maan groter: bedekt nu het grootste deel van de bovenkop, punten tot onder de ogen (Jordi: "de halve maan mag nog wat meer van het hoofd bedekken").
- Halve maan symmetrisch in beeld (Jordi: "niet mooi synchroon meer op het hoofd"): ontworpen in het vlak loodrecht op de kijkrichting, gecentreerd tussen de ogen, i.p.v. in het gezichtsvlak van de 80° gedraaide kop.
- Halve maan opnieuw als echte 3D-tekening op de kop (Jordi: "kijk even goed vanuit een 3d model"): spiegelsymmetrisch om het middenvlak van de kop, ontworpen in bolcoördinaten rond het gezicht (buitenboog door de kruin, binnenboog over de bovenkant van de ogen, punten naast de ogen omlaag). Gecontroleerd van voren, in de pose en van opzij (`pop3d/kop_halvemaan.png`).
- Halve maan 20% kleiner (Jordi: "nu is het niet heel goed duidelijk meer een halve maan"), geschaald rond het voorhoofd; leest weer als sikkel met violet eromheen.
- Bovenkant van de halve maan rond (Jordi: "de bovenkant is te puntig"): nu twee bolkappen (echte cirkels op de bol) i.p.v. cirkels in lengte/breedtegraad, die bij de kruin samenknepen tot een punt; maat gelijk gehouden aan de 20% kleinere versie.
- Middenstuk tussen de ogen bolt iets verder de halve maan in (Jordi: "nu mag het middenstuk tussen de ogen in nog een klein beetje meer inbollen"): een extra kleine bolkap tussen de ogen uit de maan gehaald.
- **Poppetje goedgekeurd** (Jordi: "ja, maak er maar een silhouet van"). Silhouet 64×64 = de render direct verkleind (1456 px, ≈1,5× fase 1; Lairon 1599), met handwerk in drie benoemde zones (diff 0 erbuiten): spiraal opnieuw als buis met open binnenkrul (liep dicht), vingertop-inkeping en de nabije hand los van de verre, kleine inham tussen kruin en rug. `docs/concept/sprites/nachtaap_evo/silhouet/` (`vel_silhouet.png`, `silhouet_1x.png`, scripts `silhouet.py`, `hand.py`, `vel.py`).
- Silhouet goedgekeurd en bevroren (Jordi: "er is een klein gat ontstaan tussen hoofd en lichaam in, verder prima"): de nek-inham is teruggedraaid; `silhouet/silhouet_bevroren_1x.png` (1459 px).
- Kleur ronde 1 (maker-agent, intern): `docs/concept/sprites/nachtaap_evo/kleur/ronde1/` (alpha-diff 0). Eigen keuring: lijf, staart, spiraal en kené goed (bevroren); terug voor de halve maan (te smal, las als wenkbrauwband met lichtlila voorhoofd), een bezorgde i.p.v. starende blik en de verre hand (las als plankje). Ronde 2 loopt.
- Kleur ronde 2 (intern): grote witte maan, kleinere rode ogen met gecentreerde pupil (starend, anders dan fase 1), volwassener snoet, verre hand als crème hand met vingers. Eigen keuring: alleen het violette middenstuk loopt nog als spitse wig de maan in (leest als fase 1-middenstreep); ronde 3 maakt het een kleine ronde bult.
- Kleur ronde 3 (intern, 7 px): middenstuk tussen de ogen is een kleine ronde bult, de maan bovenaan één doorlopende boog (dikte gelijk aan de onderlaag). Naar de onafhankelijke keurder.
- Kleur ronde 4: maan D2 overgenomen (Jordi's keuze; sikkel naar zijn referentie), alleen opgeschoond in de maanzone (11 px t.o.v. D2, vorm gelijk); buiten de zone diff 0 met ronde 3.
- Onafhankelijke keuring (`kleur/ronde4/KEURING.md`): TERUG. F1 rechter maanpunt valt weg, F2 kop leest als doos (rechte binnenlijnen), F3 verre oog is een kopie, F4 handen/voeten lezen als plankjes, F5 kené leest als krassen. Voor Jordi: leest eerder Ghost/Dark dan Psychic, silhouet leest als rat/opossum. Ronde 5 (F1–F4) loopt; F5 is een vraag aan Jordi.
- Kleur ronde 5 (F1–F4 van de keuring): rechter maanpunt wit, kop ronder (kruin, kin, rechterzijde), verre oog (links) met perspectief, handen met vingers/duim en achtervoet met tenen, nog steeds crème. Naar Jordi met de open vragen (kené, handrug, type-lezing). Vel `kleur/ronde5/vel_jordi.png`.
- Kleur ronde 6 (Jordi: "doe maar wat de keurder goed lijkt"): kené als rechthoekig getrapte meander langs de ruggengraat, violette hand- en voetrug met crème vingertoppen/tenen, violette oortjes met klein lila binnenvlak. Vel `kleur/ronde6/vel_jordi.png`.
- Ronde 6: meander afgekeurd (Jordi: "de lijnen zijn sowieso te dun, een patroon zou altijd dikker moeten"); poten wel beter → bevroren. Les in SPRITE_NORM: patronen ≥ 3 px. Ronde 7: kené als dikke banden naar het poppetje.
- Kleur ronde 7: kené als dikke banden naar het poppetje (rugband + 3 getrapte dwarsbanden, elk 3 px, lichtlila met schaduw- en lichtrand); rest = ronde 6. Vel `kleur/ronde7/vel_jordi.png`.
- Verse eindkeuring met patroonstudie (`kleur/ronde7/EINDKEURING.md`, `patroonstudie.png`): alles PASS behalve de kené (leest als ribbels: hooglichttint, bevel, 2 px, rechte verticalen, geen middenlijn). Patroonregels als les in SPRITE_NORM. Ronde 8: kené vlak en dik met middenlijn + getrapte zijbanden, plus variant met een eigen patroonkleur.
- Kleur ronde 8: kené volgens de patroonregels (vlak, middenlijn van 3 px op de ruggengraat, 3 getrapte zijbanden van 3 px, eindpunten op verschillende hoogtes), in lila; variant B met een eigen patroonkleur maanzilver (index 15 vrijgemaakt). Naar Jordi ter keuze (`kleur/ronde8/vel_jordi.png`).
- Jordi bij ronde 8: "b is wel mooier, maar klopt het patroon nog? is het niet teveel naar ons perspectief gevormd?" → gecontroleerd door de kené van het 3D-poppetje naar 64 px te projecteren (`silhouet/kene_projectie.py`): klopt, de maker had de zijbanden in beeld schuin naar voren getekend; in 3D lopen ze vanaf de ruggengraat vrijwel recht over de flank omlaag. Nieuwe dikke kené in 3D (`kene_dik`), geprojecteerd als `silhouet/kene_dik_64.npy`; vel `kleur/ronde8/kene_3d_check.png`. Ronde 9 volgt die loop in de kleuren van variant B.
- Kleur ronde 9: kené volgt de 3D-projectie (zijbanden recht over de flank omlaag, verdikt tot ≥ 3 px op 2 uiteinden na), kleuren van variant B. Vel `kleur/ronde9/vel_jordi.png`.
- Jordi vindt de strepen niet mooi; studie van Emboar, Dusknoir, Vivillon-vormen, Zangoose, Arbok, Relicanth (`referenties/patronen_gamefreak.png`) en motieven op het poppetje (`pop3d/lijfmotieven3.png`: effen, kené-banden, Nazca-spiraal op de flank, grote kené-ruit op de rug). Ogen: vergelijking met Espurr (`referenties/ogen_espurr_vs_ronde9.png`).
- Tweede patroonstudie (Jordi's voorbeelden: Spinarak, Growlithe, Dunsparce, Slakoth, Vigoroth, Loudred, Duskull, Groudon, Bronzor, Regigigas, Darmanitan; `referenties/patronen_gamefreak2.png`) en nieuwe motieven op het poppetje: tapse wiggen vanaf de ruggengraat in donker indigo of licht (`pop3d/lijfmotieven4.png`). Ogen (Espurr-richting, Jordi akkoord) in ronde 10 bij de maker.
- Kleur ronde 10: ogen in de richting van Espurr (Jordi akkoord): geen zwart kader of grote glans meer; vlak bovenlid in donker violet, ringen lichtrood → karmijn → donkere kern, lichtpunt van 1 px; rest = ronde 9.
- Jordi: "ogen zijn zeer sterk" (ronde 10 bevroren) en "tapse wiggen licht zie ik wel zitten": lijfpatroon wordt drie lichte tapse wiggen vanaf de ruggengraat (3D-projectie `silhouet/wiggen_64.npy`). Ronde 11 bij de maker.
- Kleur ronde 11: drie lichte tapse wiggen vanaf de ruggengraat (3D-projectie gevolgd, bovenaan 4–6 px, ≥ 3 px over 2/3, punt 1 px; maanzilver/lila, geen bevel); rest = ronde 10. Naar een verse eindkeurder.
- Verse eindkeuring ronde 11 (`kleur/ronde11/EINDKEURING.md`): TERUG voor 2 kleine punten (achterste wig slordig, zoals Jordi zag; kin/rechterflank als doosje). Ronde 12: die 14 px door Claude gerepareerd (alpha-diff 0, geen nieuwe open randen). Kandidaat-eindversie `kleur/ronde12/nachtaap.png`, vel `vel_jordi.png`.
- Jordi bij ronde 12: concept goedgekeurd ("puur een beetje afwerking"); geen storende rechte lijnen; lori-gelijkenis is prima. Ronde 13: ruimte tussen achterste wig, staart en rechtercontour; kleurafwerking voorpoten.
- Kleur ronde 13: achterste wig verplaatst/ingekort (2 px vacht naar staartwortel en rechtercontour), voorpoten rustiger afgewerkt (verre hand zonder dambord, zwarte onderrand aan de schaduwkant, vlekjes op de onderarm weg, doorlopende vingerlijnen). Vel `kleur/ronde13/vel_jordi.png`.
- Kleur ronde 14: achterste wig precies volgens Jordi's krabbel (schuine streep in lila; de 2 linkerpixels van ronde 12 blijven, na "en toch haal je nu aan de linkerkant 2 pixels teveel weg"). Vel `kleur/ronde14/vel_jordi.png`.

### [v0.0.33] - Dark-starter fase 3: ontwerp krabbenetende wasbeer (silhouet nog open)
- Eindvorm van de olinguito-lijn: **krabbenetende wasbeer** (*Procyon cancrivorus*), solitaire **vigilante** met een knipoog naar Sly Cooper (Robin Hood vervalt), puur Dark, niet rechtop/mensachtig. Vast: koevoetklauwen (2 klauwen = steel, bocht, gespleten punt), geringde haakstaart, masker over de neusrug, buidel op de rug als herkenbare dievenzak (deel van het lijf), houding zoals Gumshoos met Weavile-beenlengte, kop van silhouet ronde 9–11. Alles in `docs/concept/sprites/wasbeer/SPEC.md` en `AFGEKEURD.md`; referentiefoto's in `referenties/`.
- Werkwijze: 3D-poppetje (3 rondes) en eigen silhouetbouw (rondes 1–11, collage + scriptkleuring) mislukten; Jordi: "erbarmelijk slecht". Daarna een maker-agent volgens de werkwijze (ronde 12–14). Les vastgelegd en de werkwijze verplicht gemaakt in `CLAUDE.md` en `docs/lessen/SPRITE_WERKWIJZE.md` (Coathief als voorbeeld; Claude tekent niet zelf).
- Samengevoegd: Coathief-tak (frontsprite af, v0.0.24–26) en de ideeënlijst van 29 okt (v0.0.27).

### [v0.0.34] - Lama: fase 3 als poppetje, lijn op schaal
- Jordi: fase 2 = verhouding B, karamel; fase 3 blijft een lama. Fase 3 toegevoegd aan het poppetje (bombín, vlechten met tullma's, manta, pollera, bonte vacht, zwaardere bouw), twee varianten (MMA-handschoenen / windsels met vrije hoeven); vergelijking `docs/concept/sprites/lama/ontwerp/lijn_ronde1.png`.

### [v0.0.35] - Lama: fase 2 en 3 unieker
- Fase 2 slungelige tiener in dekking (wilde wol, lange dunne poten, voorpoot opgetild, kop laag), fase 3 zware geworteld kampioen (geschoren lijf, brede borst, kop hoog, wol alleen als kleding); vergelijking `docs/concept/sprites/lama/ontwerp/lijn_ronde2.png`.

### [v0.0.36] - Lama: ontwerp goedgekeurd, halsband als leitmotif
- Jordi "zeer tevreden"; fase 2 en 3 krijgen elk een aguayo-halsband (leitmotif van de alpaca), fase 3 = variant Y (windsels). Bron voor het silhouet van fase 2 klaar (`docs/concept/sprites/lama/fase2/silhouet/`); maker-agent start.

### [v0.0.37] - Werkwijze: ontwerpfase met poppetje vastgelegd
- Jordi: "ik vind dit echt geweldig werk [...] noteer dat deze manier van werken tot nu toe uitstekend werkt". De ontwerpfase van de lama (poppetje met kleding als praatplaat, keuzevel, hele lijn op schaal, onderscheid via bouw + pose) staat als vaste aanpak in `docs/lessen/SPRITE_WERKWIJZE.md` (stap 1); dubbele regel daar opgeruimd.

### [v0.0.38] - Dark-starter fase 3: nieuw 3D-ontwerp (wasbeer)
- Nieuw poppetje in de stijl van het lama-ontwerp: `docs/concept/sprites/wasbeer/ontwerp/pop3d_v2.py`, vel `ontwerp/vel_v2_ronde1.png` (3 poses x 3 hoeken, met 1x-voorbeeld, naast foto 10, Gumshoos en Weavile). Op 2 poten voorover, slank lijf zonder dikke achterkant, kop ±33%, koevoetklauwen, geringde haakstaart, buidel als zak op de rug. Wacht op Jordi's keuze van hoek en pose.

### [v0.0.39] - Wasbeer: 3D-ontwerp ronde 2 (rond P13)
- Jordi koos P13 als basis: klauwen kort met alleen een koevoet-uiteinde, stompere dunnere pootjes, iets dikker en menselijker lijf. Varianten in romphoek en lijfdikte: `docs/concept/sprites/wasbeer/ontwerp/vel_v2_ronde2.png`. Lichte buik als ovaal (geen rechthoekig vlak).

### [v0.0.40] - Wasbeer: 3D-ontwerp ronde 3 (benen)
- Jordi koos E (romp 26°, dikker lijf). Benen niet meer naast elkaar: het nabije been stapt naar achteren (ook op de tenen), onderbenen dunner zoals op de foto's: `docs/concept/sprites/wasbeer/ontwerp/vel_v2_ronde3.png`.

### [v0.0.41] - Lama fase 2: silhouet ronde 1b
- Maker-agent: silhouet uit het goedgekeurde poppetje, handreparaties aan poten, oren, snuit en wolomtrek (`docs/concept/sprites/lama/fase2/silhouet/vel_ronde1b.png`, 1188 px). Wacht op Jordi.

### [v0.0.42] - Lama fase 2: silhouet goedgekeurd
- Jordi keurde silhouet ronde 1b goed; de rechte hals blijft ("de rustige lama stand [...] vrij iconisch"). Kleurronde 1 gestart (maker-agent).

### [v0.0.43] - Wasbeer: silhouet v2 (direct van de render)
- Ontwerp E2 bevroren met een grotere rugzak. Silhouet direct van de render (`docs/concept/sprites/wasbeer/silhouet_v2/`), handwerk door een maker-agent alleen in zones (koevoetklauw, spleet zak/staart, randen), keuring door een onafhankelijke keurder; ronde 2 (`vel_ronde2.png`, 1446 px) ligt bij Jordi.

### [v0.0.44] - Lama fase 2: kleur ronde 1c
- Maker-agent kleurde met de hand op het bevroren silhouet (karamel, aguayo-halsband, aguayo-doek, rode MMA-handschoenen, oorkwasten); Claude-controle + onafhankelijke keuring (BIJNA, 6 reparaties verwerkt): `docs/concept/sprites/lama/fase2/kleur/ronde1c/vel.png`. Wacht op Jordi.

### [v0.0.45] - Wasbeer: klauw, sluippose en kleur
- Klauw vastgelegd als twee korte klauwen naast elkaar met een inkeping tussen de punten (Sneasel-achtig, driekwart), eerst los in 3D getekend (`docs/concept/sprites/wasbeer/ontwerp/klauw3d.png`).
- Pose S1a: sluipend, diep door de knieën, één been ver achter op de tenen. Silhouet direct van de render (1682 px) goedgekeurd; kleur ronde 2 na een Game Freak-studie en een keuring: `docs/concept/sprites/wasbeer/kleur_v2/vel_ronde2.png`.

### [v0.0.46] - Lama fase 2: ronde 2 (meer lama, fluffy, Pokémon-kleuren)
- Na Jordi's feedback (hoekige poten, rechte poot, vacht niet Pokémon-achtig, te weinig lama): diagnose naast de bron, nieuw silhouet (banaanoren, stompe snuit, wolhals, wolmouwen/-broek, zachte knieën; Jordi akkoord), warme heldere vachtramp, wol in klonten; Claude-controle, verse keuring (BIJNA), verse maker voor ronde 2c: `docs/concept/sprites/lama/fase2/kleur/ronde2c/vel.png`. Wacht op Jordi.

### [v0.0.47] - Wasbeer af (frontsprite)
- Eindvorm van de Dark-starter (krabbenetende wasbeer, fase 3 na olinguito en Coathief): frontsprite goedgekeurd, `docs/concept/sprites/wasbeer/af/wasbeer.png`. Sluipend op 2 poten, warm grijsbruin, masker in 2 lobben over ogen en neusrug, witte wenkbrauwboog en snuit, oog met pupil, ronde neus, twee klauwen naast elkaar met een inkeping, roodbruine buidel als dievenzak, geringde haakstaart.
- Werkwijze: nieuw 3D-ontwerp (pop3d_v2.py), silhouet direct van de render, kleur met de hand door een maker-agent na een Game Freak-studie, vier keuringen en een verse eindkeuring; Jordi's laatste punten (neus, staarthaak, klauwlijn) met kleine silhouetzones. Lessen in `docs/lessen/SPRITE_WERKWIJZE.md`.
- Nog te doen: frame 2, rug, icoon, shiny, naam en data.

### [v0.0.48] - Review sprite-werkwijze na de wasbeer
- `docs/lessen/SPRITE_WERKWIJZE.md`: review van de wasbeersessies (wat goed en slecht ging) en vijf regels: elk kenmerk uit een echte bron, klein onderdeel los in 3D of op een tekenvel, wat Jordi goed noemt blijft bevroren, grote keuzes vóór pixelreparaties, verse maker na ±250–300k context. Stap 1 en 2 bijgewerkt (poppetje in lama-stijl voor slanke dieren op 2 poten, poten nooit gelijk, dunne delen herstellen vóór de kleur).

### [v0.0.49] - Brainstorm Uyuni-Silicobra
- Brainstorm voor de eerste regional form (Silicobra uit de Salar de Uyuni, met een mogelijke nieuwe evolutie) toegevoegd aan `docs/concept/IDEEEN.md`. Nog niets besloten.

### [v0.0.50] - Nachtaap fase 2: frontsprite af
- Verse eindkeuring met vergelijking tegen echte sprites en de Dragonfly Cave-gids (`docs/concept/sprites/nachtaap_evo/kleur/ronde14/EINDKEURING.md`, 17 gidsregels): twee kleine FAILs in de crème tenen (bruine onderrand aan de schaduwkant → zwart, hark op de achtervoet), 8 px door Claude gerepareerd; alpha-diff 0 tegen het bevroren silhouet.
- **Af:** `docs/concept/sprites/nachtaap_evo/af/nachtaap_evo.png` (+ `normal.pal`, `vel.png`, `EINDKEURING.md`). Jordi: "Het concept ben ik gewoon tevreden mee". Nog te doen: frame 2, rugsprite, icoon, shiny, naam en data.
- Prompt voor een nieuw gesprek over nachtaap fase 3 (eindvorm): `docs/concept/sprites/PROMPT_NACHTAAP_FASE3.md`.

### [v0.0.51] - Uyuni-Silicobra: Ground + Ice-immuniteit
- Besloten (Jordi): de Uyuni-Silicobra blijft Ground en krijgt een nieuwe ability met een immuniteit voor Ice; de sprite wordt een aangepaste bestaande sprite (`POKEMON.md`, `SPRITE_WERKWIJZE.md`). Uitleg waarom Ground/Electric klopt + matchups in `IDEEEN.md`.

### [v0.0.52] - Kolibrie pre-evo: ontwerp en kleurrondes (onaf)
- Nieuwe map `docs/concept/sprites/kolibrie_pre/`: pre-evolutie van de kolibrie, puur Flying (wordt Ghost/Flying bij de evolutie), zittend jong met ingeklapte vleugels en open bedelbekje; foto's van Jordi in `referenties/`.
- Ontwerp: drie richtingen (A jong vogeltje gekozen), mild lila kleur zoals Fletchling vóór Fire, korte snavel bewust.
- 3D-poppetje uit bollen (79–88% overlap) en opgeblazen silhouet geprobeerd; gaven geen goed beeld. Silhouet met de hand (maker-agent) en kleurrondes r1–r10 met keuringen; goedgekeurd: kop r8 lager, Starly-oog, snavel r7b met lijn bij de mondhoek, palet.
- r10 afgekeurd (geen driekwart pose, lijnen); volgende stap een 3D-model op de goedgekeurde vorm, gedraaid naar 3/4, daarna het silhouet daaruit. Overdracht bovenaan `SPEC.md`.
- Lessen in `docs/lessen/SPRITE_WERKWIJZE.md` (poppetje passend op de foto, keurder nooit inperken).

### [v0.0.53] - Lama fase 2: terug naar de bron, nieuwe kop en pose
- Jordi: de kop was "meer een paard dan een lama", het oog moest droger, de hals kaarsrecht, de wol minder klonterig/korrelig, de pose niet "gebroken". Poppetje ronde 3 (lamakop met half gesloten bovenlid, kaarsrechte ruige hals) goedgekeurd; oogstudie (Camerupt, Farfetch'd, Numel, Slakoth-lijn); posestudie (24 Gen 3-viervoeters); poppetje ronde 5: lijf horizontaal, kop driekwart, alle poten op de grond, Jordi koos pose F. Bron voor silhouet ronde 5 klaar; overdracht in `docs/concept/sprites/lama/SPEC.md` (VOLGENDE STAP). Lessen in `docs/lessen/SPRITE_WERKWIJZE.md`.

### [v0.0.54] - Uyuni-Silicobra: nieuwe evolutie, kleurrichtingen
- Besloten (Jordi): de Uyuni-Silicobra krijgt een **nieuwe evolutie** (geen Uyuni-Sandaconda). Ability: Jordi denkt nog na.
- `docs/concept/sprites/silicobra_uyuni/` met SPEC.md en drie kleurrichtingen (paletwissel op de bestaande sprite): A Zoutkorst, B Spiegel, C Lithium.

### [v0.0.55] - Uyuni-Silicobra: ontwerpstudie regional forms
- Studie van 12 regional forms (wat ze veranderen) en een ontwerpvoorstel voor de Uyuni-Silicobra in `docs/concept/sprites/silicobra_uyuni/ONTWERP.md` (pekelzak, zeshoekige korst, zoutkegel; niet als Ice of Nacli lezen). De kleurrichtingen van v0.0.54 zijn vervallen tot het ontwerp vastligt.

### [v0.0.56] - Uyuni-Silicobra: schetsen ronde 1
- Vier ruwe ontwerpschetsen op de echte Silicobra-sprite (`docs/concept/sprites/silicobra_uyuni/schetsen_ronde1.png`): zoutkorst, pekelzak, zoutkegel-staart, korstschild. Besloten (Jordi): loom en traag, een wall.

### [v0.0.57] - Kolibrie pre-evo: 3D-model op de goedgekeurde vorm
- `docs/concept/sprites/kolibrie_pre/model3d/`: 3D-model dat het goedgekeurde profiel zelf opblaast (lijf 97,7% gelijk aan silhouet r2, kop 99,6% aan r8 lager), met r10-kleuren, Starly-oog en r7b-snavel; draaibaar naar driekwart.
- Vel `model3d/vel_hoeken.png` met 9 hoeken naast Taillow en Starly; wacht op Jordi's keuze.

### [v0.0.58] - Uyuni-Silicobra: keuzes + schetsen ronde 2 (zoutkegel)
- Besloten (Jordi): zoutkorst, pekelzak, half dichtgevallen oog en zoutkuif. Twijfel over de zoutkegel: vier varianten in `docs/concept/sprites/silicobra_uyuni/schetsen_ronde2.png`; voorstel om de kegel als overworld-gedrag te gebruiken in plaats van in de sprite.

### [v0.0.59] - Uyuni-Silicobra: ontwerp vastgelegd (variant A)
- Jordi koos variant A (zoutkorst, pekelzak, half dichtgevallen oog, zoutkuif; geen zoutkegel in de sprite). SPEC.md bijgewerkt; maker-agent gestart.

### [v0.0.60] - Lama fase 2: silhouet ronde 5c
- Verse maker tekende het silhouet op pose F (lijf horizontaal, kop driekwart, kaarsrechte hals, alle poten op de grond, 0 korrels). Claude stuurde ronde 5 terug (doos-romp, paaltjespoten); 5b met ronde wolmassa en tapse poten; verse keuring BIJNA (6 reparaties: oplopende rug, buikboog, hoeven achter, handschoenen met platte zool) verwerkt in 5c: `docs/concept/sprites/lama/fase2/silhouet_r5/vel_ronde5c.png`. Wacht op Jordi (rug oplopend/vlak, staartpluim, formaat).

### [v0.0.61] - Lama fase 2: silhouet 5b goedgekeurd
- Jordi koos ronde 5b ("5b ok want c heeft opeens geen staart meer"); 5c afgekeurd (staart verdwenen in de oplopende rug). Silhouet 5b bevroren als basis voor de kleur (oogvarianten, wol als één zachte massa).

### [v0.0.62] - Lama fase 2: silhouet ronde 5d
- Jordi: "als c nu gewoon een staart zou hebben, zou die het beste zijn" → ronde 5d: 5c met de staartpluim van 5b terug (rest pixel voor pixel 5c, 0 korrels). Wacht op Jordi. Les: één versie naar Jordi, geen meerdere imperfecte opties (`docs/lessen/SPRITE_OPDRACHT.md` §4).

### [v0.0.63] - Lama fase 2: silhouet ronde 5e (kop driekwart)
- Jordi twijfelde over de kophouding van 5d. Oren nu vanaf het achterhoofd naar achteren in een V zoals het poppetje, schedel iets langer; rest gelijk aan 5d. Wacht op Jordi.

### [v0.0.64] - Lama fase 2: silhouet ronde 5f (kop van het poppetje)
- Jordi: de kop van 5e was "anders" dan het goedgekeurde poppetje. De kop is nu overgetrokken van het poppetje (dekkingskaart uit dezelfde camera, max. 1 px afwijking), de achterrand van de hals loopt recht door; rest gelijk aan 5e. Les: een goedgekeurd poppetje is de specificatie en wordt overgetrokken, niet hertekend (`docs/lessen/SPRITE_OPDRACHT.md` §2). Wacht op Jordi.

### [v0.0.65] - Nachtaap fase 3: richting en pose
- Fase 3 = muriqui (Jordi): gezicht, lange armen en benen; rechtop/zwevend; kleurpatroon van de lijn blijft; sinistere ogen (kleiner); spiraalstaart met bladeren. Lore: kanaliseert planten en takken met psychische kracht.
- Pose naar Jordi's krabbel goedgekeurd: horizontaal zwevend, arm en been omhoog om een onzichtbare tak, healerhand met de palm naar de tegenstander (lijf 40° / kop 80°). 3D-poppetje `docs/concept/sprites/nachtaap_fase3/pop3d/muriqui3d.py`.
- Handen in 3D mislukt (alle varianten afgekeurd); volgende sessie: handen als pixelzones naar een echte sprite-hand (Gen 1-Drowzee). Overdracht onderaan `nachtaap_fase3/SPEC.md`.
- Lessen in `SPRITE_WERKWIJZE.md`: "Vóór elk vel naar Jordi" (harde regel), ellipsoïde-poppetje faalt bij dynamische poses en handen, referentie van Jordi = die afbeelding, kenmerken zelf tellen.

### [v0.0.66] - Uyuni-Silicobra: frontsprite ronde 2
- Maker-agent ronde 1 en 2 in `docs/concept/sprites/silicobra_uyuni/ronde1/` en `ronde2/`. Ronde 2: barstnet i.p.v. bakstenen, ronde pekelzak i.p.v. edelsteen, oogring terug met half lid, gekleurde buitenlijn (Jordi: "vooral de buitenste lijn is te zwart"). Wacht op Jordi.

### [v0.0.67] - Sprite-werkwijze afgedwongen (keurslot)
- Jordi: "het is elke keer opnieuw dat we instructies vastleggen die je elke keer opnieuw weer overslaat" → "doe allemaal".
- Keurslot: `.claude/settings.json` + `.claude/hooks/sprite_keurslot.py` (PreToolUse op SendUserFile): geen afbeelding uit `docs/concept/sprites/` naar Jordi zonder `<bestand>.keuring.md` met bron, 8×/1× en `Oordeel: PASS`.
- Keurvel: `tools/grounded/keurvel.py` (werk naast bronnen op 8× en 1×, licht/donker, close-ups, keuringssjabloon).
- `SPRITE_WERKWIJZE.md`: korte Checklist bovenaan (keurslot, keurvel, referentie per onderdeel, één afwijking = niet sturen, keurder per mijlpaal, ritme, gereedschap per onderdeel); de rest is naslag.

### [v0.0.68] - Uyuni-Silicobra: frontsprite ronde 3
- Pekelzak kleiner en los van de staart, kuif links loopt geleidelijk uit (39 px; de rest pixel voor pixel gelijk aan ronde 2). `docs/concept/sprites/silicobra_uyuni/ronde3/`.

### [v0.0.69] - Lama fase 2: silhouet ronde 6 (model overgetrokken)
- Jordi keurde 5f af (lijf en poten weken flink af van het model). Verse maker trok het hele silhouet over van het poppetje (max. 1 px afwijking, alleen korrels weg). Wacht op Jordi.

### [v0.0.70] - Uyuni-Silicobra: frontsprite ronde 4 (halsband)
- Ronde 3 afgekeurd (kuif brokkelt af, zak als aanhangsel); bespreking in `docs/concept/sprites/silicobra_uyuni/bespreking/`. Besloten (Jordi): de pekel wordt een **halsband**. Ronde 4 (vanaf ronde 2): slordige pixel weg, nek terug naar het originele silhouet met een volle turquoise band; kop, voet en krul pixel voor pixel ronde 2.

### [v0.0.71] - Lama fase 2: silhouet ronde 6 goedgekeurd, kleurronde 4 gestart
- Jordi keurde ronde 6 goed ("zolang de staart maar definieerbaar blijft"; schokken gladstrijken in het spritewerk). Kleurronde 4 gestart: verse maker na een Game Freak-studie, wol als één zachte massa, staart leesbaar, drie oogvarianten (Numel-basis, Slakoth-droogheid, zwaar lid).

### [v0.0.72] - Uyuni-Silicobra: frontsprite ronde 5
- A: halsband 1 px hoger onder de kin. B (test): A plus een scheidingslijn tussen kop en zoutkuif. `docs/concept/sprites/silicobra_uyuni/ronde5/`.

### [v0.0.73] - Uyuni-Silicobra: frontsprite ronde 6
- Vanaf 5A: de gezichtslijn van de originele Silicobra terug in een zachte grijs-okertint; halsband aan de bovenkant 1–2 px hoger, onderkant gelijk. `docs/concept/sprites/silicobra_uyuni/ronde6/`.

### [v0.0.74] - Uyuni-Silicobra: frontsprite goedgekeurd
- Jordi: "ronde 6 uitstekend en akkoord". Frontsprite (frame 1) bevroren in `docs/concept/sprites/silicobra_uyuni/af/silicobra_uyuni.png` (64×64, 15 kleuren, transparency=0). Lessen van de zes rondes in `docs/lessen/SPRITE_WERKWIJZE.md` (Regional forms). Stand van zaken in CLAUDE.md bijgewerkt.
- Nog te doen: frame 2 (mond open), rugsprite, icoon, shiny, naam en data; de nieuwe evolutie; de ability.

### [v0.0.75] - Naam evolutie: Saltaconda
- De nieuwe evolutie van de Uyuni-Silicobra heet **Saltaconda** (salt + anaconda, dé slang van Zuid-Amerika). Ontwerprichting en type nog open (`docs/concept/sprites/silicobra_uyuni/ONTWERP.md`).
- Gewijzigd (Jordi): de naam wordt **Salticonda** ("vind ik net wat lekkerder bekken").

### [v0.0.76] - Salticonda: richting + eerste schetsen
- Besloten (Jordi): Salticonda wordt **Ground/Electric**, een bulky wall (HP en Def), in de geest van Runerigus: een eigen vorm met inspiratie van Sandaconda (zoutheuvel met pekelringen, hints naar een accu). `docs/concept/sprites/salticonda/` met SPEC.md en vier ruwe schetsen op de Sandaconda-sprite.

### [v0.0.77] - Kolibrie pre-evo: echt 3D-model in Blender
- Numpy-model (opgeblazen profiel, ronde kop, ronder lijf, K1-R2b) geprobeerd en verlaten: van opzij gezien plat en van alle kanten vreemd.
- `docs/concept/sprites/kolibrie_pre/blender/`: model in Blender (bpy) als één huid (smooth union): bolletje-lijf met ingewerkte vleugels, kop zonder nek, kort staartje, langere naaldsnavel; vel met rondom-renders en 3/4-standen naast Fletchling, Starly en Taillow. Foto's 6 en 7 van Jordi beschreven in `referenties/`.
- Lessen in `docs/lessen/SPRITE_WERKWIJZE.md` (profielkop is geen 3/4, silhouet als omtrek over de render tonen, model niet ongevraagd wijzigen).

### [v0.0.78] - Salticonda: silhouetronde 1
- Drie silhouetvarianten op Ekans als skelet, met de anaconda-foto's van Jordi als bron voor de kop (`docs/concept/sprites/salticonda/silhouet1/`): A 4 windingen + kop bovenop, B laag en breed + kop vooraan, C Ekans-houding met staart omhoog.

### [v0.0.79] - Lama fase 2: kleur ronde 4b
- Verse keuring van ronde 4: NEE (wol vlak, staart bultje, doek als koffer, oog als streepje). Ronde 4b verwerkt de 9 reparaties: zachte wolmassa met licht linksboven en wolbogen, staartpluim, doek met plooi, één droog oog (lid B + iris C), verre poten gescheiden met kleur. Wacht op Jordi.

### [v0.0.80] - Lama fase 2: kleur ronde 4c
- Jordi vond 4b beter maar het lijf nog een "flakke plank" en het oog "un-pokemon like". Ronde 4c: lijf en hals als overlappende wolbollen (zoals Mareep/Flaaffy), oog met zwaar vlak bovenlid, donkere iris met lichtje en lama-wimpers. Wacht op Jordi.

### [v0.0.81] - Salticonda: silhouetronde 2
- Vanaf A: bulkier (±2150 px, voet ±55 px breed), één doorlopende kegelomtrek, kop van A bevroren (5 px omhoog). D = 4 windingen, E = 3 dikke windingen (`docs/concept/sprites/salticonda/silhouet2/`).

### [v0.0.82] - Lama fase 2: kleur ronde 4d (hals)
- Jordi keurde lijf en oog van 4c goed; de hals mocht "nog ietsje meer". Ronde 4d: drie overlappende wolbollen op de hals met zachte bogen in de omtrek, de rest gelijk aan 4c. Wacht op Jordi.

### [v0.0.83] - Lama fase 2: kleur ronde 4e (hals)
- Jordi vond de hals van 4d "teveel buis achtig". Ronde 4e: vanaf de hals van 4c één zachte wolmassa met een kraagje vóór boven de halsband, geen gestapelde bollen. Wacht op Jordi.

### [v0.0.84] - Lama fase 2: kleur ronde 4f (hals)
- Jordi: "klein beetje meer nog". Hals iets voller: bredere lichtmassa, diepere schaduwkant, een pluk achter en een vollere kraag vóór. Wacht op Jordi.

### [v0.0.85] - Lama fase 2: kleur ronde 4g (hals)
- Jordi: de pluk achter op de hals van 4f was een "gekke uitstulping"; hals bolliger met een bol links onderaan. Ronde 4g: uitstulping weg, drie ronde overlappende wolbollen met een borstbol vóór boven de halsband. Wacht op Jordi.

### [v0.0.86] - Lama fase 2: kleur ronde 4h (hals)
- Jordi: de nek vooral "aan de binnenkant wat meer fluffy kleuren", silhouet niet veranderen. Ronde 4h: wolstructuur van het lijf doorgezet in de hals (lichte wolvlekken, krulhaakjes), silhouet gelijk aan 4g. Wacht op Jordi.

### [v0.0.87] - Salticonda: kleurronde 1 (A en E)
- A en E ingekleurd met het palet van de Uyuni-Silicobra (silhouetten bevroren, alpha-diff 0): buisvormige windingen met licht van linksboven, turquoise pekelringen in de gleuven, zoutkorst met Y-naden, kop met half oog, anacondastreep en lichte snuit, gebandeerde staart met turquoise punt. `docs/concept/sprites/salticonda/kleur1/`.

### [v0.0.88] - Lama fase 2: frontsprite af
- Jordi keurde kleur ronde 4h goed; verse eindkeuring: af na 6 px (nagels, handschoen). Frontsprite fase 2 staat in `docs/concept/sprites/lama/fase2/af/lama.png`. Volgende: fase 3 (lama met bombín). Lessen in `docs/lessen/SPRITE_WERKWIJZE.md`.

### [v0.0.89] - Idee: koningstiran met Inca-kroon
- Nieuw idee van Jordi in `docs/concept/IDEEEN.md`: een Pokémon naar de tropical royal flycatcher (koningstiran) met een Inca-hoofdtooi (mascaypacha). Uitgewerkt door Claude: het echte dier, de Inca-koppeling, kuif dicht/open als sprite-animatie, geslachtsverschil, lijn- en type-opties. Nog niets besloten.
- Brainstorm erbij: verwante vogels (tirannen met verborgen kroon, rotshaan, parasolvogel, zonneral, bergcaracara, incastern, kuifkardinaal) en vier lijnvoorstellen.

### [v0.0.90] - Lama fase 3: poppetje ronde 3 (eigen pose)
- Fase 3 (3Y, cholita-luchadora) gestart volgens SPRITE_WERKWIJZE: nieuw poppetje `docs/concept/sprites/lama/ontwerp/fase3_r3.py` met de goedgekeurde lamakop en kaarsrechte hals van fase 2, bombín, pony, vlechten met tullma's, brede halsband met 7 pompons, manta, pollera en windsels.
- Jordi: "ik wil wel een iets andere pose dan fase 2" → vier pose-opties (A geworteld 32°, B uitval, C bijna frontaal, D zij met de kop naar je toe); advies A. Vel `ontwerp/vel_fase3_ronde3.png`, naar Jordi.

### [v0.0.91] - Lama fase 3: poppetje ronde 4 (pose C, worsteloutfit)
- Jordi koos pose C. Nieuw `docs/concept/sprites/lama/ontwerp/fase3_r4.py`: grotere bombín, dikke gevlochten vlechten over de schouders naar voren, gelijke windsels om beide voorpoten (gouden manchetten), intocht-cape met knoop, gouden kampioensriem, worstelrok; variant Y met singlet. Vel `vel_fase3_ronde4.png`, naar Jordi (advies X).

### [v0.0.92] - Lama fase 3: poppetje ronde 5 (franje, X of Y)
- Foto's 9 en 10 (cholitas luchadoras) in `docs/concept/sprites/lama/referenties/`. Besloten: beide geslachten krijgen hetzelfde ontwerp (zoals Gardevoir, Meowscarada, Primarina), maar geen volledige jurk.
- `fase3_r4.py`: franje-opties (manta-franje, franje + kant onder de rok, beide) voor X (bont) en Y (blauw worstelpak); vel `vel_fase3_ronde5.png`, naar Jordi.

### [v0.0.93] - Lama fase 3: ontwerp Y bevroren, bron silhouet
- Jordi koos Y (blauw worstelpak) zonder franje. Bron voor het silhouet in `docs/concept/sprites/lama/fase3/silhouet/` (`bron.py`, model 50 %: 1265 px, box 35×62) met controlevellen; op 64 px lopen de voorpoten in pose C samen, vraag aan Jordi.

### [v0.0.94] - Salticonda: ronde 2 (3/4, nieuwe kop, staart als zoutkegel)
- Nieuw 3/4-lijf met drie dikke windingen als ellipsen, doorbuigende pekelringen, een grotere anaconda-kop met Sandaconda-neusbult en ouder half oog; kopvariant A (koepel) en B (kroon van zoutplaten); staart als klein zoutkegeltje met pekelringen. `docs/concept/sprites/salticonda/kleur2/`.

### [v0.0.95] - Lama fase 3: silhouet ronde 1 (pose C2)
- Pose C2 (lijf 45°) gekozen. Maker trok het model over: `docs/concept/sprites/lama/fase3/silhouet/ronde1.txt` (1286 px, alles ≤ 1 px van het model, 0 korrels). Op 64 px: voorpoten één blok, formaat maar 9 % boven fase 2; vraag aan Jordi.

### [v0.0.96] - Lama fase 3: buffer (buffstudie + hals/kop-varianten)
- Gen 3-buffstudie (`docs/concept/sprites/lama/fase3/buffstudie/gen3_buff.png`) en varianten met kortere, dikkere hals en relatief kleinere kop (`fase3/silhouet/vel_buff.png`): V2 = 1,42× fase 2. Geforceerd perspectief in het poppetje werkte niet. Naar Jordi (advies V2).

### [v0.0.97] - Lama fase 3: breder zonder de verhoudingen te veranderen
- V1–V3 afgekeurd ("raar en komisch"). Nieuwe knop `breed` in `fase3_r4.py`: lijf, hals en poten alleen dikker, lengtes gelijk; vel `docs/concept/sprites/lama/fase3/silhouet/vel_breder.png` (W1–W3, tot 1,27× fase 2). Naar Jordi.

### [v0.0.98] - Lama fase 3: silhouet ronde 2 (W3)
- Jordi koos W3 ("de cholitas zijn best stompig ook qua bouw"). Maker trok het model opnieuw over: `docs/concept/sprites/lama/fase3/silhouet/ronde2.txt` (1512 px, 1,28× fase 2, alles ≤ 1 px van het model, 0 korrels). Naar Jordi.

### [v0.0.99] - Salticonda: nieuwe kop in 3/4 (kleur3 → 3c)
- Kleur2 afgekeurd (misvormde koppen, zijaanzicht). Lijf van kleur1-E bevroren; alleen de kop opnieuw, op de Silicobra-Uyuni-kop als skelet in dezelfde 3/4-hoek, iets groter, met Sandaconda-neusbult. Jordi over kleur3: "veel beter de goede kant op". 3b: zouttextuur op de kuif (goed), maar kuif kleiner (afgekeurd). 3c: kuif +19% t.o.v. kleur3 (kraag van zoutplaten naar achteren), neusgaten terug. `docs/concept/sprites/salticonda/kleur3*/`.
- Ability-richting (Jordi): één ability met immuniteit voor Ice én Water die hem oplaadt (zout smelt ijs, water + zout = pekel); details en naam later (`docs/concept/sprites/silicobra_uyuni/ONTWERP.md`).

### [v0.0.100] - Lama fase 3: kleur ronde 1/1b (intern) en kopstudie
- Kleurrondes 1 en 1b (`docs/concept/sprites/lama/fase3/kleur/`) intern: bombín en vlechten lazen op 1× niet, want ze waren in het model te klein (vlechten lagen in de dikke hals). Kopstudie `fase3/kopstudie/vel_kopstudie.png`: grotere bombín naar links, dikkere zichtbare vlechten, kop 1,0/1,12/1,2. Naar Jordi.

### [v0.0.101] - Lama fase 3: silhouet ronde 3 (sprite-overdrijving kop)
- Ontwerp blijft; alleen de spritebron krijgt kop 1,2×, grotere bombín naar links en zichtbare vlechten. Verse maker trok over: `docs/concept/sprites/lama/fase3/silhouet/ronde3.txt` (1488 px, alles ≤ 1 px van de bron, 0 korrels). Naar Jordi.

### [v0.0.102] - Salticonda: kleur3e en kleur3d
- Jordi: kleur3 heeft de beste kuif en neus; 3b/3c afgekeurd. kleur3e = kleur3 met alleen de zouttextuur van 3b op de kuif (vorm identiek). kleur3d = kleur3 met dezelfde kuif 1,1× hoger/breder (1,32× oppervlak), sprite 3 px omlaag, neus en lijf ongewijzigd.

### [v0.0.103] - Salticonda: kleur3f (kop past bij het lijf)
- Jordi koos 3e. 3f: schaduwkant van de kop even diep als op de windingen (zelfde tinten/stappen), slagschaduw op de bovenste winding onder kaak en halsband; 75 px, alleen tinten, silhouet/kuif/neus/oog ongewijzigd.

### [v0.0.104] - Salticonda: onafhankelijke keuring
- Keuring van kleur3f (`docs/concept/sprites/salticonda/keuring/KEURING.md`): geslaagde regionale vorm (herkenbaar idee, ander materiaal/functie, verklaard door de regio, evolutie vergroot het kenmerk), maar 4 kleine FAILs: rechte runs in de ringen, onderrand te licht, staart leest niet op 1×, raakt de bovenrand. Zes smaakvragen voor Jordi.

### [v0.0.105] - Lama fase 3: kleur rondes 2–3 (alleen sprite)
- Terug naar het goedgekeurde silhouet ronde 2 (spritebron/silhouet ronde 3 vervallen). Kleur ronde 2/2b/3 in `docs/concept/sprites/lama/fase3/kleur/`: kop in de sprite ±1,25× groter dan het silhouet, neutrale droge lamablik, grotere bombín, vlecht met krullen, poten afgewerkt. Ronde 3 naar Jordi.

### [v0.0.106] - Salticonda: kleur3g (reparaties keuring + Electric-hint)
- Ringen en halsband zakken in het midden door (runs ≤8 px), donkere onderrand, nieuwe staart (5 px dik, pekelband, eindigt als zoutkegeltje), sprite 2 px omlaag (2 rijen lucht boven), Electric-hint: warm lichtgele glans op de halsband (paletindex 15). 207 px; kop, kuif, neus, oog en korst gelijk aan 3f.

### [v0.0.107] - Salticonda: frontsprite goedgekeurd
- Jordi: 3g "bijna helemaal goed", met de staart van 3f. kleur3h = 3g + staart van 3f, vastgelegd als `docs/concept/sprites/salticonda/af/salticonda.png` (64×64, 16 kleuren, transparency=0). Stand van zaken in CLAUDE.md bijgewerkt.
- Nog te doen voor de lijn: frame 2, rugsprites, iconen, shinies, data; de ability (naam en effect).

### [v0.0.108] - Werkwijze: eerst de dex met alleen frontsprites
- Jordi: "Ik wil eerst gewoon een pokedex maken met alleen een 1e frontsprite". Vastgelegd in `docs/concept/SPRITE_PLAN.md` en de Stand van zaken: elke nieuwe soort eerst alleen frame 1; frame 2, rug, icoon en shiny later voor de hele dex in één ronde.

### [v0.0.109] - Lama fase 3: kop overgetrokken van het model (kleur ronde 4/4b)
- Kop-overtrekbron `docs/concept/sprites/lama/fase3/kleur/kopbron/` (model, kop uniform 1,25× om de oorpunten); de maker trok de kop cel voor cel over (ronde 4) en maakte daarna alleen het oog leesbaar (ronde 4b). Lijf, kleding en poten gelijk aan 2b. Naar Jordi.

### [v0.0.110] - Nachtaap fase 3: 2D-model (muriqui-kop en achtervoeten)
- Buiten Blender (Jordi): kop en achtervoeten overgeschilderd op de Blender-render (`docs/concept/sprites/nachtaap_fase3/model2d/overschilder.py`); pose, lijf, armen, healerhand en staart ongewijzigd.
- Muriqui-gezicht naar foto 4/5: donker schild met rechte wenkbrauwlijn, kleine lichtblauwe ogen dicht bij elkaar, lichte neusrug naar een brede snuit, rechte mond, donkere kin, korte maansikkel.
- Voeten: bovenste grijpt als haak om de onzichtbare tak (tenen als want, grote teen tegenover), onderste hangt slap met losse grote teen.
- Vertaalbaar naar de sprite (les lama): kop 1,3× en alle gezichtsdelen ≥ ±2 px op 64; controle `model_64.png`, vel `vel_model.png` (keurder: maten verwerkt).

### [v0.0.111] - Lama fase 3: kleur ronde 5 (A en B, luie blik)
- Oogstudie (Slakoth, Slaking, Camerupt) en nieuw oog: zichtbaar zwaar bovenlid, oogwit, kleine pupil, "nonchalant en unimpressed". Twee versies: A (kop 1,25×, hals blijft, lijf ±7 % kleiner) en B (lijf gelijk, kop 1,1×); vel `docs/concept/sprites/lama/fase3/kleur/vel_ronde5.png`. Naar Jordi.

### [v0.0.112] - Lama fase 3: A gekozen, kleur ronde 5A2
- Jordi koos A. Vlechten terug naar zwart zoals het model; oog lui in plaats van boos (licht lidvlak, lidlijn dalend naar buiten, meer oogwit). `docs/concept/sprites/lama/fase3/kleur/ronde5A2/`. Naar Jordi.

### [v0.0.113] - Lama fase 3: kleur ronde 5A3 (hoed, oog)
- Bombín 1,2× en lager, aansluitend op de vlechten; oog terug naar 5A met een lichter lidvlak. `docs/concept/sprites/lama/fase3/kleur/ronde5A3/`. Naar Jordi.

### [v0.0.114] - Lama fase 3: oog goedgekeurd, hoed 1 px lager (5A4)
- Jordi keurde het oog van 5A3 goed. Ronde 5A4: bombín 1 rij lager, vlecht begint onder de rand. `docs/concept/sprites/lama/fase3/kleur/ronde5A4/`. Naar Jordi.

### [v0.0.115] - Lama fase 3: kleur ronde 5A5 (bombín links, verre achterpoot)
- Bombín links in hoedtinten en 2 px korter; verre achterpoot met volume. `docs/concept/sprites/lama/fase3/kleur/ronde5A5/`. Naar Jordi.

### [v0.0.116] - Kolibrie pre-evo: frontsprite af
- Stand A van het Blender-model gekozen (één oog, snavel langer en open, kop iets omhoog); silhouet direct uit de render.
- Kleur in 10 rondes met maker-agents en drie onafhankelijke keuringen: Starly-oog (iris en Combusken/Latias geprobeerd, terug naar Starly), opgeschoond tot ≤3 tinten per kleurgroep, contrast als Taillow, belijning zonder wisselende zwart/donkerlila, ronde vleugelschaduw, kleine pootjes in perspectief, holle hals naar bolle buik (foto 8 van Jordi).
- Allerlaatste keuring: kleur en Dragonfly Cave PASS na 8 px. Af: `docs/concept/sprites/kolibrie_pre/af/kolibrie_pre.png`.
- Afspraak (Jordi): frame 2, rugsprite, icoon, shiny, naam en data komen later voor alle soorten samen; eerst designs met frontsprites (CLAUDE.md, SPRITE_WERKWIJZE.md).
- Spritelessen samengevat in één pagina `docs/lessen/SPRITE_KERN.md` (Jordi: "vat de lessen echt enorm samen"); CLAUDE.md en de oude spritebestanden verwijzen ernaar, de rest is naslag.
- `docs/lessen/SPRITE_WERKWIJZE.md` compact herschreven (stappentabel + commando's); oude versie in `docs/lessen/naslag/SPRITE_WERKWIJZE_oud.md`.
- `docs/lessen/SPRITE_WERKWIJZE.md` compact herschreven (stappentabel + commando's); oude versie in `docs/lessen/naslag/SPRITE_WERKWIJZE_oud.md`.
- Blender-model is geen vereiste (Jordi): foto of model, wat werkt (SPRITE_KERN, SPRITE_WERKWIJZE).

### [v0.0.117] - Lama fase 3: eindkeuring + reparaties (ronde 5A7)
- 1 px bombín (5A6); verse eindkeuring met extra aandacht voor de poten: af na 7 kleine reparaties (28 px), uitgevoerd in `docs/concept/sprites/lama/fase3/kleur/ronde5A7/`. Naar Jordi.

### [v0.0.118] - DJ Rotom: bron en silhouet 1
- DJ Rotom opnieuw begonnen volgens `docs/lessen/SPRITE_WERKWIJZE.md`, met Jordi's bron (Pokopia-render) in `docs/concept/sprites/dj_rotom/referenties/` en een `SPEC.md`.
- Silhouet 1 (64×64): de bron direct verkleind (60×45, ±1750 px, zo groot als Frost/Wash); alleen de bliksem-noot en de spits met de hand dikker gemaakt (32 px). Vel: `docs/concept/sprites/dj_rotom/silhouet1/vel_silhouet1.png`. Wacht op Jordi.

### [v0.0.119] - Lama fase 3 frontsprite af
- Jordi keurde ronde 5A7 goed: `docs/concept/sprites/lama/fase3/af/lama3.png` (+ `normal.pal`, `vel.png`). Buffe, stompige cholita-luchadora-lama in pose C2 met bombín, zwarte vlechten, blauw worstelpak, cape, kampioensriem, rok in drie ruches en aguayo-windsels; kop 1,25× van het model, droge nonchalante blik. Nog: frame 2, rug, icoon, shiny, naam/data.

### [v0.0.120] - DJ Rotom: silhouet 2 (sterker perspectief)
- Jordi: "misschien iets meer perspectief als in pronounced vormen?" en "ik vind de bron juist driekwart". Het 3/4 van de bron sterker gemaakt door de bron zelf te vervormen (`docs/concept/sprites/dj_rotom/silhouet2/perspectief.py`): de nabije rechterspeaker groter, de verre linkerspeaker kleiner, boven- en onderlijn kantelen mee en de kop blijft breed. Drie sterktes A/B/C in `silhouet2/vel_perspectief.png`; de bliksem wordt na de keuze weer met de hand dikker gemaakt.

### [v0.0.121] - DJ Rotom: silhouet bevroren
- Jordi: "prima! ga maar in kleuren. Bliksem noot mag idd dikker dan". Variant B (mijn advies) met de bliksem-noot met de hand dikker (15 px) is bevroren: `docs/concept/sprites/dj_rotom/silhouet_af/silhouet.png`. Stijlnorm voor de kleur: de Rotom-vormen die al in de game zitten (Jordi: "gebruik vooral de stijl van de rotom sprites die al in de game zitten he").

### [v0.0.122] - Nachtaap fase 3: model af, silhouet ronde 1
- Model in drie stappen met Jordi: beide poten in één stuk met de schaduw van de render, voeten als want (naar Jordi's foto); staart gekanteld; kop meer driekwart, gezicht 1,2×, grote maan; lichtblauwe gloed om de healerhand (vlakke banden + omlijning, zoals Reuniclus; studie `referenties/psychische_effecten.png`). Maan (nog groter) en rugpatroon (op de rug, mee met de pose) volgen in de sprite.
- Silhouet ronde 1 (`docs/concept/sprites/nachtaap_fase3/silhouet/`): model overgetrokken op de 50%-dekking, 1796 px, 0 korrels, alles ≤ 1 px van het model; spiraalspleten < 1 px gevuld (windingen als lijnen in de kleur). Onafhankelijke keurder: één reparatie (staartrand).

### [v0.0.123] - DJ Rotom: kleur1 + grotere kop (silhouet 3)
- Kleur1 (maker-agent): gloed, game-Rotom-oranje (de bronkleur lag er vrijwel op), speakers, ogen en bliksem goed; het gezicht was te smal (kopvoorkant ±13 px), met een te klein display. Teruggestuurd.
- Jordi: "ja dan moet het middenstuk misschien wat groter om de ogen enzo goed te kunnen uitbeelden". Silhouet 3: kop-kubus + spits in de bron vergroot (×1,15 / ×1,25 / ×1,35), bliksem houdt zijn maat, rechterspeaker blijft ervóór; daarna dezelfde perspectiefvervorming (B). Vel: `docs/concept/sprites/dj_rotom/silhouet3/vel_kop.png`.

### [v0.0.124] - DJ Rotom kleur2–4
- Kleur2: kop ×1,25 in de sprite (Jordi: "silhouet naar sprite is niet 1 op 1 te vertalen"), varianten A/B voor het display; onafhankelijke keuring (`kleur2/KEURING.md`) koos B, met 5 reparaties.
- Kleur3: reparaties (kop in 3/4, conussen met stofkap, hoek rechtsonder, snoer, schaduw).
- Kleur4: hogere bliksem (y10–25, twee knikken, witte achtste noot) en de ogen pixel voor pixel naar het Frost-sjabloon (Jordi: "het zijn nog geen typische rotom ogen"). Les in `SPRITE_OPDRACHT.md`.

### [v0.0.125] - DJ Rotom kleur5 (Rotom-consistentie)
- Jordi: "best goed al, laat een agent het met de andere rotom sprites vergelijken en kijken of er dingen zijn die consistent zijn die in deze sprite missen". Analyse: `docs/concept/sprites/dj_rotom/kleur4/CONSISTENTIE.md`.
- Kleur5 (`kleur5/dj_rotom.png`): zwarte binnenlijn aan de schaduwkant, vrije spits van 10 px (bliksem 3 px omhoog), twee losse tandjes, hooglicht als vlekjes (4,5%), oranje/wit/grijs op de exacte game-waarden. Open voor Jordi: gloed voller, navy of grijs, extra plasma, verticale plek; daarna shiny, frame 2, rug, icoon.

### [v0.0.126] - DJ Rotom frontsprite af
- Verse eindkeuring PASS (`docs/concept/sprites/dj_rotom/kleur5/EINDKEURING.md`): op 1× een vorm uit dezelfde game als de zes Rotoms. Aanbevelingen uitgevoerd: naden tussen kop en kasten zwart (zoals Frost/Mow), equalizertoppen eigen groen zodat ze in de shiny niet perzik worden (46 px).
- Af: `docs/concept/sprites/dj_rotom/af/dj_rotom.png` (frame 1). Volgende: shiny, frame 2, rug, icoon, data.
- Les in `SPRITE_WERKWIJZE.md`: consistentie-analyse tegen de bestaande vormen bij vormen van een bestaande soort.

### [v0.0.127] - DJ Rotom hoger in het vak, zweeft
- Jordi: "kan die nog hoger dan?" De frontsprite is 4 px omhoog geschoven (pixels ongewijzigd) en staat nu net zo in het vak als Frost (boven y3, onder y58).
- Jordi: "hij hoort te zweven". In deze build krijgt elke tegenstander een schaduw (Gen 4-stijl); met `enemyMonElevation` > 0 zweeft de sprite erboven. Bij het invoeren: elevation ±6 zoals Frost, schaduw breed genoeg voor de speakers (genoteerd in `dj_rotom/SPEC.md`).

### [v0.0.128] - Idee: roomkleurige specht (Electric/Flying)
- Jordi's idee (cream-colored woodpecker, "net Pikachu") met Claude's haakjes in `docs/concept/IDEEEN.md`: convergente evolutie in plaats van pikaclone, drie bronnen voor de elektriciteit (telegraaflijn van Rondon, piëzo-elektrisch hout, bliksembomen), evolutie naar een kastanjebruine vorm (*Celeus elegans*), naam via *pica-pau*.

### [v0.0.129] - Specht: mimicry en naam Picapau
- `docs/concept/IDEEEN.md`: Mülleriaanse mimicry als reden voor de Pikachu-gelijkenis; Picapau genoteerd als favoriete naam (Jordi).

### [v0.0.130] - Specht: convergente soort
- `docs/concept/IDEEEN.md`: Picapau is een convergente soort van Pikachu (zoals Wiglett/Toedscool), dan via kleur en tekening in plaats van vorm; mimicry als optionele reden.

### [v0.0.131] - Specht: convergent is een fan-term
- `docs/concept/IDEEEN.md`: na Bulbapedia-check: "convergent species" is een fan-term, officieel gaat het om toevallige gelijkenis; haakje via de World Pokémon Ecological Society; mimicry staat lager.

### [v0.0.132] - Specht: stroombronnen samen, Raichu-achtige evolutie
- `docs/concept/IDEEEN.md`: roffelen + droog hout + bliksembomen samen, met een dorp dat op Picapau draait; evolutie die (net als Toedscruel bij Tentacruel) minder op Raichu lijkt, met de spechtentong als bliksemstaart.

### [v0.0.133] - Parallelle takken samengevoegd, changelog hernummerd
- De acht takken die naast elkaar liepen (lama, wasbeer, nachtaap, kolibrie pre-evo, Uyuni-Silicobra/Salticonda, DJ Rotom, koningstiran, specht) zitten nu in `main`. Elke tak telde vanaf v0.0.23 zelf door, waardoor dezelfde nummers vaak voorkwamen; alle secties staan nu op volgorde van hun commitdatum met unieke nummers (v0.0.24–v0.0.132). Inhoud ongewijzigd.
- `docs/lessen/SPRITE_WERKWIJZE.md` is de compacte versie (met de keurslot-checklist bovenaan); de lessen die andere takken in de lange versie zetten, staan in `docs/lessen/naslag/SPRITE_WERKWIJZE_oud.md`.

### [v0.0.134] - Picapau: start spriteproces
- `docs/concept/sprites/picapau/`: SPEC (stap 0), Jordi's twee foto's en een vergelijkingsvel (Pikachu + vogel-sprites op 4×).

### [v0.0.135] - Picapau: 3D-model en stand B1
- `docs/concept/sprites/picapau/blender/picapau.py`: Blender-model (één huid, zoals de kolibrie-pre-evo): grote ronde kop, ronde rode wang, kuif met twee zwarte punten (Pikachu-oren) en rafelige achterkuif, vleugels dicht, beitelsnavel 40° omhoog, roodbruine steunstaart met knik, poten die uit het lijf groeien. Pose naar Jordi's foto's (schuin lijf). Jordi koos stand B1 (lijf 30°, kantel 8°); het silhouet uit die render wacht op zijn keuring. Een eerste silhouet geknipt uit een foto is afgekeurd ("slordig knipwerk").

### [v0.0.136] - Picapau: kleursprite ronde 5
- Kleur in 5 rondes (maker-agent) met een onafhankelijke keuring na ronde 3; versie B (23 px silhouetwijziging: snavelbasis, poten, buik) ligt bij Jordi: `docs/concept/sprites/picapau/kleur_r5/picapau.png`.

### [v0.0.137] - Picapau: sprite v2 (overgetrokken van het model)
- r5 afgekeurd ("volledig 2d ..."); model B1 bleef bevroren ("subliem"). Sprite v2 cel voor cel van de B1-render (`sprite_v2/bron/`: kleur + onderdelen per spritepixel), 6 rondes met Jordi's krabbel, verse keurder (r5 NIET GOED → 83 px reparaties → r6 GOED). Nieuw gereedschap: `tools/grounded/model_vs_sprite.py` (vergelijking model ↔ sprite per onderdeel vóór Jordi). Lessen in `docs/lessen/GRAPHICS.md`.

### [v0.0.138] - Picapau frontsprite af
- Jordi over r6/r7: staartpunt, buikvlek, donkerder geel, vleugelstip, kuif (suggestie keurder), snavel bleef ("snavel is prima"); "prima om een iets andere kleur te doen idd". Verse eindkeuring r7: GOED zonder reparaties. Eindversie: `docs/concept/sprites/picapau/af/picapau.png` (+ `normal.pal`). Smaakvragen (tenen, kuifstelen): Jordi "nee prima zo".

### [v0.0.139] - Les: changelog na main nummeren
- `docs/lessen/AGENTS.md`: vóór het pushen naar `main` eerst `main` mergen en de eigen changelogsecties achteraan nummeren (Jordi).

### [v0.0.140] - Hitmontop: evolutie in plaats van regional form
- Jordi: Hitmontops Japanse naam is al capoeira, dus geen regional form maar alleen een nieuwe capoeira-evolutie. Eerst puur ontwerp. Drie richtingen (mestre/bananeira, Besouro-kever/armada, malandro/negativa) in `docs/concept/IDEEEN.md`; POKEMON.md en DEX_NOMINATIES bijgewerkt (dubbele Hitmontop-regel in POKEMON.md weg).

### [v0.0.141] - Hitmontop-evolutie: pose gekozen
- Jordi koos de pose: eenarmige handstand met benen in een V-split (foto in `docs/concept/sprites/hitmontop_evo/referenties/`), beschreven in `SPEC.md` daar.

### [v0.0.142] - Hitmontop-evolutie: ontwerp vastgelegd
- Jordi's ontwerp letterlijk in `docs/concept/sprites/hitmontop_evo/SPEC.md`: kleine niet-functionele hoorn, bruine huid, lange aansluitende blauwe broek, langer lijf, afro-Braziliaans haar (Eddy Gordo), langere benen met kleinere blauwe klauwvoeten, koordjes aan broek en armen (muay thai), ronde handen. Fanart "Mestrimba" als inspiratie in `referenties/`.

### [v0.0.143] - Hitmontop-evolutie: Fighting/Ground
- Jordi koos Fighting/Ground ("omdat die telkens aan de grond zit"); Dark past niet. Uniek in de dex (Great Tusk staat uit). In SPEC.md en POKEMON.md.
