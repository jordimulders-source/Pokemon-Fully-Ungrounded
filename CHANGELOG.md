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
