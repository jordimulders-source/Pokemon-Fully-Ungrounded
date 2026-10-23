# Plan: de Hoenn-wereld eruit (TODO-stap 6, met stap 5)

Opgesteld 22 okt, na het opruimen van de intro's. Doel: alleen het skelet blijft over, en na elke stap bouwt het
(`make -j4 2>&1 | grep -i error` leeg) en start een nieuw spel.

## Stand (23 okt): stap 7 gedaan, stap 8 wacht op Jordi
Uitgevoerd door de stap 7-agent, één commit per systeem (`git log --grep "Stap 7"`). De overgangslaag kromp van
233 kaarten / 21 layouts / 23 heal locations / 76 local ids / 651 stubs naar **64 / 16 / 0 / 35 / 592**, en alles wat
er nog in staat hoort bij stap 8 (zie de inventaris hieronder). ROM: vóór 18,55 MB vrij (`__rom_end` 0x08D71FE4), na
18,62 MB vrij (0x08D61CCC), dus ±65 KB erbij.

Per systeem (generiek mechaniek = blijft zonder Hoenn-kaart; Hoenn-plek = weg):
- **Pokémon Center herkennen** (`field_specials.c` `InPokemonCenter`/`UsedPokemonCenterWarp`, `save_location.c`): op
  de layout (`LAYOUT_POKEMON_CENTER_1F`/`2F`) i.p.v. een kaartlijst; nieuwe steden doen vanzelf mee. Saven in het
  Pokémon Center en opnieuw laden brengt je terug in het Pokémon Center (getest).
- **`field_specials.c` + `data/specials.inc`:** weg (functie + special + scriptaanroep): abnormaal weer (Kyogre/
  Groudon-routes, `abnormal_weather.inc`), SS Tidal (stappen, positie, patrijspoort), kabelbaan, Rusturf-tunnel (ook uit
  Rock Smash), warenhuis (verdiepingen, liftmenu), Meteor Space, Dewford-respawn, Mauville-/Petalburg-gympuzzels,
  loterijcomputer, Trick House-nugget, Abandoned Ship-sleutels, Black Glasses, weer Route 119/123, Pacifidlog-TM,
  Glass Workshop, Wally-Zigzagoon, vleugelgeluid; de oproepen van Wally/Scott/Roxanne/rivaal-Rayquaza in
  `field_control_avatar.c`; de truck-intro en patrijspoort (`field_special_scene.c` helemaal). Winkelbediende =
  `LOCALID_START_TOWN_MART_CLERK` (vanilla: altijd local id 1).
- **`region_map.c`:** Fly-bestemmingen alleen StartTown (`sMapHealLocations`); de Hoenn-steden blijven als grijze
  plaatshouder op de kaart (geen bestemming). Fly vanuit de regiokaart (R, na de 6e badge) getest.
- **`roamer.c`:** lege routetabel; een roamer verplaatst zich niet en staat nergens (geen deling door nul). Het
  gebiedsscherm slaat zo'n roamer over.
- **`item_use.c`:** Vs. Seeker-binnenlijst leeg (buiten werkt hij altijd), Sudowoodo water geven weg.
- **`overworld.c`:** muziekuitzonderingen (abnormaal weer, Sootopolis, Weather Institute, Space Center, Route 111/118),
  Route 130-kreten, omgekeerde Sky Pillar weg. (Let op: de oude check `warp->mapGroup == 0` gold nu voor de
  skeletgroep.)
- **`wild_encounter.c`:** Feebas-tegels Route 119, Altering Cave, Route 104-noord, Sootopolis-legendaries,
  Ditto-plek Route 115 weg; een wilde Floette krijgt nu overal een willekeurige bloemkleur (was alleen de Fairy Forest).
- **`pokedex_area_screen.c`:** glow of marker op kaarttype (buiten = glow, binnen/grot = marker) i.p.v. kaartgroep;
  Feebas-uitzondering weg. Getest (Lotad op de TestMap licht op bij StartTown).
- **`tv.c` / `tv.inc`:** spelershuis via de layout, geen Lati-nieuws/film meer, uitbraaktabel leeg (geen uitbraken),
  PokéNieuws Slateport/Lilycove uit, Gabby & Ty met vaste local ids (`LOCALID_GABBY_AND_TY_*` in `constants/tv.h`).
- **`follower_helper.c`:** kaartgebonden volgerberichten op `MAP_UNDEFINED` (plek in de nieuwe regio invullen).
- **Faraway Island-Mew** (`faraway_island.c`), **braillepuzzels** (`braille_puzzles.c`), **Mirage Tower**
  (`mirage_tower.c`), **Regi-stippen** (`regi_dots.c` + `.inc`), **Scorched Slab-zonnezaal**, **post-game-rivaal**
  (`rival_postgame.c` + `.party`): weg. Het veldeffect `FLDEFF_USE_TOMB_PUZZLE_EFFECT` blijft als lege plek.
- **Slapend zonder Hoenn-kaart** (mechaniek blijft, plekken invullen in de nieuwe regio): Forces of Nature
  (`forces.c`), Enamorus (`enamorus.c`), de Burglar (`burglar.c`, teksten per stad blijven), draaihekken
  (`rotating_gate.c`), donkere mist (`field_weather_effect.c`), Safari Zone (uitgang = StartTown als plaatshouder),
  visserstoernooi (`fishing_tournament.c`).
- **Losse verwijzingen:** Ever Grande-vrijlaatregel (pc), Lavaridge-stoom (Misty Terrain), Meteor Space/Route 113
  (gevechtsachtergrond), Altering Cave-items, Lavaridge-respawn na vergif, Hall of Fame-vervolg (nu het Pokémon Center
  van StartTown), opvangvrouw (`VAR_LAST_TALKED`), Mom na uitwitten (respawn_npc).
- **Evoluties:** de plaatsgebonden evoluties zijn weg; Magnezone/Vikavolt (Thunder Stone), Leafeon (Leaf Stone),
  Glaceon/Crabominable (Ice Stone) werkten al met een steen; Alolan Exeggutor nu tijdelijk level-up met een Dragon-type
  in het team. Genoteerd in `POKEMON.md` ("Evolutieplek in de nieuwe regio").
- **Scripts:** `players_house.inc` is nu alleen Mom (standaardtekst "The A-Team will be on soon!", PokéNav-registratie,
  healen), de slaapkamer-PC, de wandklok en de Running Shoes-handleiding; Mom staat in `Stock_TwoStory_1F`, PC en klok
  in `Stock_TwoStory_2F` (ook in `skelet_maps.py`). Mr. Briney (ook de aanroep in PC 1F), veerboot en Rusturf weg uit
  `event_scripts.s`. Teksten die nog nodig waren, kwamen terug in hun eigen bestand (Kecleon/Devon Scope, munten,
  Birch-registratie, regiokaart). Weg (ongebruikt, Hoenn): `cave_of_origin.inc`, `elite_four.inc`,
  `set_gym_trainers.inc`, `rival_graphics.inc`, `giant_wailord.inc`, `sickblik_dev.inc`, `legends2.inc`, en de
  teksten braille, Shoal Cave, eventtickets, bessen, loterij. Steven Multi uit het debugmenu.
- **Niet aangeraakt:** `battle_partners.party` (Steven = vanilla en gebruikt door `battle_tower.c`/debug, Wally slapend,
  Joey hoort bij Gabby & Ty, Keccles blijft; een partner zonder team breekt trainerproc), de Match Call-koppen
  (inert zolang hun registratieflags niet gezet worden; Mom en Birch zijn weer te registreren).

Getest (emulator, nieuw spel, Mewtwo lv 100 + alle badges): start in StartTown (9, 12), healen bij de verpleegster,
Mart (koopmenu), wild gevecht op de TestMap, Keccles (gewonnen), saven in het Pokémon Center + reset + Continue (terug
in het Pokémon Center), Fly vanuit de regiokaart naar StartTown, Pokédex-gebiedsscherm (Lotad), Mom (healt), slaapkamer-
PC (menu, uitzetten). `audit.py`: 0 fouten in warps/kaarten/scripts/flags/wild/items; 59 bij trainers (zie hieronder).

**Nog open (geen stap 8):**
- Het debugmenu **Battle test** verwijst in 55 van de 57 ingangen naar trainers zonder team (sinds stap 6), ook de
  klasse-intro-tests; `audit.py` meldt ze als `noparty`. Nieuwe testtrainers per klasse nodig (bijv. in
  `debug_trainers.party`).
- Ongebruikte Hoenn-specials buiten de compat-laag (geen kaartverwijzing, wel ROM): o.a. `StartWallyTutorialBattle`,
  `StartGroudonKyogreBattle`, `Script_DoRayquazaScene`, `DoOrbEffect`, `IsMirageIslandPresent`, `UpdateShoalTideFlag`,
  `InitBirchState`, Lilycove-SS Tidal-menu (`script_menu.c`). Lijst: `specials.py`-aanpak (specials zonder scriptaanroep).
- `TRAINER_SICKBLIK_DEV` en Gabby & Ty 2–6 staan nog in `trainers.party` voor scripts die slapen of weg zijn.

## Stap 8: inventaris (wacht op Jordi)
Code die alleen nog via de compat-header bouwt. Grootte = ROM van de objectbestanden (`.text`/`.rodata`/`.data`) uit
`pokeemerald.map`; scripts, teksten en graphics in `event_scripts.o`/`graphics.o` komen er nog bij.

| Systeem | ROM | Bestanden (KB) | Wat er nog in de compat-laag zit |
| --- | --- | --- | --- |
| Battle Frontier (Tower, Dome, Palace, Arena, Factory, Pike, Pyramid, Tents, pas, lounge, ruilhoek, Apprentice, opgenomen gevechten) | ±273 KB | battle_tower 113, battle_dome 30, battle_factory_screen 26, apprentice 20, frontier_util 16, battle_pyramid 13, frontier_pass 12, overige < 10 | Frontier-kaarten/layouts (pas, Pyramid, Pike, Tower-lift/-gang, Tent), lounge-NPC's in `field_specials.c` (71 stubs), Nature Girl in `pokemon.c`, ruilhoek, ±340 partner-/Apprentice-teksten via `##`, Pyramid in `overworld.c`/`wild_encounter.c`/`start_menu.c`/`party_menu.c`/`map_name_popup.c`/`field_poison.inc`, Tower-lobby in `save_location.c`/`link.c`/`tv.c`/`field_door.c` |
| Trainer Hill | ±20 KB | trainer_hill 20 | kaarten, `field_specials.c`, `trainer_hill.inc`, `field_poison.inc` |
| Secret Bases (incl. decoraties) | ±38 KB | decoration 26, secret_base 11 | 27 kaartnamen in `secret_base.c` (let op: `SaveBlock1.secretBases` blijft) |
| Contests (wedstrijd, schilderijen, Pokéblocks, Berry Blender, Lilycove Lady) | ±140 KB | contest 42, berry_blender 19, contest_painting 16, contest_util 14, contest_ai 11, overige < 10 | `contest_hall.inc` (55), `contest_util.c`, `berry_blender.inc`, `lilycove_lady.inc` |
| Union Room / Cable Club / draadloos (incl. Berry Crush, Dodrio, Pokémon Jump, Mystery Gift, e-Reader) | ±213 KB | union_room 33, dodrio_berry_picking 33, pokemon_jump 21, berry_crush 16, link_rfu_2 14, union_room_chat 12, librfu_rfu 11, link 10 | `union_room.c`, `union_room_player_avatar.c`, `cable_club.inc`, Trade Center in `menu_helpers.c` |

Gedeeld met de rest (niet zonder meer weg): `trade.o` (71 KB, ook ruilen in de game), `easy_chat.o` (47 KB, mail,
vragenlijst, trendy phrases), `record_mixing.o` (6 KB, ook TV/Lilycove Lady). Save-data (`SaveBlock2.frontier`,
`SaveBlock1.secretBases`, contest- en Lilycove Lady-velden) blijft staan, ook als de code weggaat.

## Stand (22 okt, avond): stap 1–6 gedaan
Uitgevoerd door de Hoenn-agent, één commit per stap. Wat er nu is:
- **Skeletkaarten** (`gMapGroup_FullyUngrounded`, enige kaartgroep, groep 0): `StartTown` (kopie van Oldale, noord-
  en zuiduitgang dicht), `StartTown_PokemonCenter_1F/2F` en `StartTown_Mart` (de Oldale-kaarten, alleen hernoemd; de
  warps van 2F naar Union Room/Trade Center zijn weg), zeven stock-kaarten op zes interieurs (`Stock_House1/2` vanuit
  StartTown, `Stock_HouseWithBed`, `Stock_SmallHouse`, `Stock_TwoStory_1F/2F` (spelershuis met trap), `Stock_Lab`
  vanuit de TestMap) en `TestMap` (Route 102 + een pleintje met vier huizen; 12 unieke landsoorten, water en vissen
  van Route 102, twee bessenbomen, Keccles (`TRAINER_KECCLES_1`, steeds opnieuw te bevechten), een PC op het bord
  linksboven). StartTown en TestMap zijn verbonden (west/oost). Bouwscript: `tools/grounded/maptools/skelet_maps.py`
  (bronnen uit git-commit `a64c32e28d`, dus ook nu nog te draaien); bewaarlijst: `skelet_keep.py`.
- **Mapsec:** `MAPSEC_START_TOWN` is het oude vakje van Yoshi's Island (er past geen mapsec meer bij: 255 + NONE in
  een u8). Op de Hoenn-regiokaart staat hij op de plek van Littleroot; StartTown zet `FLAG_VISITED_LITTLEROOT_TOWN`
  zodat het Littleroot-icoon vliegbaar is; `GetMapsecType` geeft voor StartTown altijd "vliegbaar".
- **Nieuw spel** (`src/new_game.c`): StartTown (9, 12), respawn `HEAL_LOCATION_START_TOWN` (Pokémon Center). Het
  Littleroot-/truckverloop (vars, hide-flags) is weg. `make_intro_state.py` drukt A tot de overworld en meldt de kaart.
- **Debugmenu:** Zone warp toont eerst "Fully Ungrounded" (`debug_zone_warps.py`, labels "PC" i.p.v. "PokemonCenter").
- **Weg (stap 5, `hoenn_eruit.py`):** 648 kaarten en hun 598 includes, 542 layoutmappen (12 layouts blijven, zie
  `skelet_keep.KEEP_LAYOUTS`), 22 heal locations, alle wilde tabellen behalve de TestMap (Pyramid/Pike blijven),
  158 `FLAG_HIDE_*`-regels in `new_game.inc`. `berry_tree_locations.py` en `debug_zone_warps.py` draaien mee.
- **Overgangslaag (stap 4/5, `map_compat.py`):** `include/constants/map_compat.h` (via `constants/maps.h`, als enum
  zodat de `map`-macro in scripts hem ziet) met 233 kaarten (groep 0x40 + oude groep), 21 layouts, 23 heal locations
  en 76 local ids, plus `data/scripts/map_compat_stubs.inc` met 651 stubs voor labels uit verdwenen kaartscripts die
  C-code of algemene scripts nog noemen (ook via `##` in macro's, zoals de Battle Tower-partnerteksten).
- **Trainers (stap 6, `tools/grounded/trainers_eruit.py`):** 1036 teams weg. Over: `TRAINER_NONE`, Keccles (alle vier)
  en wat algemene scripts nog bevechten: Gabby & Ty 2–6 (`gabby_and_ty.inc`), Phillip (`trainer_hill.inc`),
  Burglar 1–9 (`burglar.inc`; de inbreker kan op elke kaart met badges verschijnen, dus niet leeg laten),
  SickBlik dev (`sickblik_dev.inc`, debug). `opponents.h` ongewijzigd. `gRematchTable` is een plaatshouder (alle
  ingangen `TRAINER_NONE` op `MAP_UNDEFINED`; `REMATCH_*` blijft voor de save-indeling), `sMatchCallTrainers`
  één plaatshouder, `gym_leader_rematch.c` één voorbeeldregel (Roxanne) en één algemene weigertekst.
- **Ook gedaan:** `pokedex_area_screen.c` kijkt voor "routes" naar de skeletgroep (anders wees hij naar groep 0x40,
  buiten `gMapGroups`).
- **Getest** (emulator, nieuw spel): StartTown, healen bij de verpleegster, Mart (koopmenu), alle stock-huizen in en
  uit, trap 1F↔2F, lopen StartTown → TestMap, wild gevecht (Nickit lv 7), Keccles-gevecht, debug Zone warp, debug
  Fly naar StartTown (landt voor het Pokémon Center). Niet getest: Fly via de Town Map (QoL na de 6e badge).
- **ROM:** vóór 9,36 MB vrij (`__rom_end` 0x096A41C8), na 11,47 MB vrij (0x09488034): 2,11 MB erbij.
- Oude saves en savestates zijn ongeldig (andere kaartgroepnummers): nieuw spel.

## Wat er over was voor stap 7–9 (gevonden tijdens stap 1–6; stap 7 is gedaan, zie boven)
- **Compat-gebruikers** (aantal namen uit `map_compat.h` per bestand): `field_specials.c` 154, `region_map.c` 129,
  `roamer.c` 70, `contest_hall.inc` 55, `tv.c` 45, `item_use.c` 40, `save_location.c` 39, `overworld.c` 36,
  `frontier_pass.c` 31, `secret_base.c` 27, `trainer_hill.c` 20, `wild_encounter.c` 19, `battle_pike.inc` 19,
  `field_special_scene.c` 15, `union_room.c` 12, `follower_helper.c` 10, `gabby_and_ty.inc` 10, `forces.c` 9,
  `union_room_player_avatar.c`/`braille_puzzles.c`/`pokemon_storage_system.c`/`abnormal_weather.inc` 8,
  `faraway_island.c`/`burglar.c`/`battle_pyramid.c`/`contest_util.c`/`mirage_tower.c` 7, `berry_blender.inc`/
  `players_house.inc` 6, `field_player_avatar.c`/`regi_dots.c`/`pokedex_area_screen.c`/`cable_club.inc` 5, en 1–4 in
  `battle_pike.c`, `rotating_gate.c`, `heal_location.c`, `enamorus.c`, `battle_setup.c`, `lilycove_lady.inc`,
  `battle_util.c`, `event_scripts.s`, `battle_tent.c`, `field_weather_effect.c`, `menu_helpers.c`,
  `battle_factory.c`, `post_battle_event_funcs.c`, `field_door.c`, `party_menu.c`, `trainer_hill.inc`,
  `apprentice.inc`, `safari_zone.inc`, `map_name_popup.c`, `pokemon.c`, `field_poison.inc`, `day_care.inc`, en de
  evoluties in `gen_1_families.h` (2) en `gen_7_families.h` (1). Opnieuw tellen: namen uit `map_compat.h` grep'en.
- **Stub-gebruikers** (`map_compat_stubs.inc`): `battle_pyramid.c` 129, `field_specials.c` 77,
  `battle_frontier_exchange_corner.h` 30, `players_house.inc` 30, `pokemon.c` 25 (de Nature Girl-teksten van
  Lounge 5 in de naturetabel), `field_control_avatar.c` 13 (PC in het spelershuis, Sootopolis-deur, Regi-ingang, …),
  `battle_pike.inc` 7, `battle_main.c` 5, `start_menu.c` 3 (Pyramid), `event_scripts.s` 3, `trainer_hill.inc` 3,
  `kecleon.inc` 3, en 1–2 in `field_player_avatar.c`, `fldeff_cut.c`, `player_pc.c`, `roulette.inc`, `tv.inc`,
  `field_poison.inc`, `item_use.c`, `link.c`, `fishing_tournament.c`, `dewford_trend.c`, `cable_club.c`,
  `debug.inc` (Steven Multi), `prof_birch.inc`, `contest_hall.inc`, `enamorus.inc`.
- **Risico's tot stap 7:** code die een compat-waarde als index gebruikt leest buiten de tabel
  (`Overworld_GetMapHeaderByGroupAndId`, `gMapLayouts[...]`, `gHealLocations[...]`). Alleen bereikbaar via dode
  scripts/systemen (Frontier, Pyramid, roamers, secret bases, Mirage Tower, …), maar wel eerst opruimen als iets
  vreemd crasht. Het Fly-scherm tekent nog alle Hoenn-stadsiconen (grijs).
- **Niet aangeraakt, hoort bij stap 7/8:** `battle_partners.party` (Steven, Wally, Joey; Keccles blijft),
  `rival_postgame.party` + `rival_postgame.c`, `debug_trainers.party`, de Match Call-koppen in
  `pokenav_match_call_data.c` (Mr. Stone, Birch, May/Brendan, Wally, Norman, Mom, Steven, Scott, gymleiders, E4: inert
  zolang hun registratieflags niet gezet worden), `data/text/match_call*.inc`, de PC-1F-aanroep
  `Common_EventScript_UpdateBrineyLocation` (precies overgenomen van Oldale), de Union Room/Wireless Club-
  medewerkers op 2F (zonder warp), `data/scripts/*.inc` met Hoenn-inhoud (zie de lijsten hierboven), de
  Grounded-mapsecs en -flags.
- **Tools die niet meer werken** (bouwen Hoenn-kaarten na): de meeste scripts in `tools/grounded/maptools/` (route135,
  route136, meteor_falls_ext, …), `land_vulling.py`/`landlib.py`-gebruikers, `audit.py` en de sweep-recepten nakijken.
  Werken wel: `skelet_maps.py`, `hoenn_eruit.py`, `map_compat.py`, `testrom.py`, `emu.py`, `render_map.py`,
  `make_intro_state.py`, `debug_zone_warps.py`, `berry_tree_locations.py`. CLAUDE.md-recepten met Hoenn-kaarten
  (`warp MAP_ROUTE136_GROTTO`, Stadium-, Spire-tests) gelden niet meer: gebruik `warp MAP_TEST_MAP, x, y`.
- **Dialoogstudio:** verwijst nu naar verdwenen labels; alleen op verzoek opnieuw exporteren.

## Wat blijft
- **Tilesets en assets:** alle tilesets (`data/tilesets/`, `src/data/tilesets/`), trainerfoto's, overworld-sprites,
  Pokémon-graphics, de bronbestanden in `graphics/grounded/` (ook die van Yoshi's Island). Een tileset zonder kaart
  kost ROM (de headers in `src/data/tilesets/headers.h` worden altijd gelinkt). Daarom laten staan en pas bij de 1.0
  meten.
- **Layouts als bouwstenen** (in `layouts.json` laten staan, ook zonder kaart):
  - Pokémon Center: `PokemonCenter_1F`, `PokemonCenter_2F` (plus de varianten van Lavaridge/Ever Grande als je die wilt
    houden);
  - Mart: `Mart`;
  - huizen: `House1`–`House4`, `HouseWithBed`, `Brendans/MaysHouse_1F/2F` (spelershuis), en een paar grotere
    interieurs als voorbeeld van andere maten (bijv. `RustboroCity_House*`, `LilycoveCity_House*`,
    `PacifidlogTown_House*`). Begin met een korte lijst in een script (`tools/grounded/maptools/skelet_keep.py`) zodat
    wat blijft één keer vastligt.
  - Let op: een layout zonder kaart is alleen in een kaart te gebruiken via een nieuwe `map.json` die ernaar verwijst.
    Laat elke layout die we houden in elk geval door één kaart gebruiken (zie de stock-kaarten hieronder), anders ziet
    niemand of hij nog werkt.
- **Kaarten** (nieuwe groep `gMapGroup_FullyUngrounded`, achteraan `group_order` en als laatste sleutel in
  `map_groups.json`; max. 128 kaarten per groep):
  - `StartTown` (plaatshouder, La Paz-achtig; mag eerst een kopie van Littleroot-grond zijn) met spelershuis,
    Pokémon Center, Mart;
  - `StartTown_PokemonCenter_1F/2F` en `StartTown_Mart`: kopie van de kaarten van Oldale (map.json + scripts.inc +
    teksten), alleen hernoemd. Scripts precies zo houden (nurse via `Common_EventScript_PkmnCenterNurse`,
    `CableClub_OnResume`, `setrespawn`, `badgemart`/`pokemart`);
  - `StockHouses`: per bewaarde huislayout één kaart (`Stock_House1` …) met een deur terug naar StartTown, zodat ze
    in de debugwarp zitten en getest worden;
  - `TestMap`: gras met wilde Pokémon, water, een trainer (Keccles), een PC en een paar warps naar de stock-kaarten.
    Alles wat we later testen gebeurt hier.
- **Code:** alle QoL, debugmenu (`DEBUG_OVERWORLD_MENU`/`DEBUG_BATTLE_MENU`), klasse-intro's, Keccles (trainer
  `TRAINER_KECCLES_*`, thema, transitie, sprites, Kecleon-rol).

## Wat weg moet
| Wat | Waar | Aantal (22 okt) |
| --- | --- | --- |
| Kaarten | `data/maps/*`, `map_groups.json` (35 groepen) | ±700 |
| Layouts die niet in de lijst staan | `data/layouts/*`, `layouts.json` | 553 → ±25 |
| Map-scripts | `data/event_scripts.s` (`.include "data/maps/*/scripts.inc"`) | 598 includes |
| Algemene scripts met Hoenn-verwijzingen | `data/scripts/*.inc` (73 bestanden) | eerst per bestand beoordelen |
| Trainers + teams | `src/data/trainers.party`, `include/constants/opponents.h` | 1057 teams |
| Wilde encounters | `src/data/wild_encounters.json` | per kaart |
| Heal locations | `src/data/heal_locations.json` | 23 → 1–2 |
| `MAP_*` in C-code | src/ + include/ | 1526 verwijzingen, 45 bestanden |

De grootste C-bestanden met `MAP_*`: `src/data/debug_zone_warps.h` (648, gegenereerd), `field_specials.c` (141),
`battle_setup.c` (82, rematchtabel), `roamer.c` (82), `frontier_pass.c` (59), `item_use.c` (40, Itemfinder-/
Repel-lijsten), `save_location.c` (39, lijst van PC-kaarten), `pokemon_sprite_visualizer.c` + header (48),
`overworld.c` (32, muziek/zee-routes, Sootopolis/Weather Institute/Space Center), `secret_base.c` (27), `tv.c` (21),
`union_room.c`, `wild_encounter.c` (Feebas Route 119, Altering Cave, Route 104/115, Sootopolis), `follower_helper.c`,
`forces.c`, `braille_puzzles.c`, `battle_environment.h`, `pokemon_storage_system.c`, `burglar.c`, `trainer_hill.c`,
`faraway_island.c`, `mirage_tower.c`, `pokedex_area_screen.c`, `regi_dots.c`, `enamorus.c`, `new_game.c`,
`rotating_gate.c`, en evoluties met `IF_IN_MAP` (Leafeon `MAP_PETALBURG_WOODS`, Glaceon/Crabominable
`MAP_SHOAL_CAVE_LOW_TIDE_ICE_ROOM`).

## De truc: een overgangsheader
Kaarten weghalen laat honderden `MAP_*`-constanten verdwijnen; alles in één keer oplossen bouwt dagen niet. Daarom:
1. Een script (`tools/grounded/maptools/map_compat.py`) zoekt alle `MAP_*` die in `src/`, `include/` en `data/`
   gebruikt worden maar niet meer in `map_groups.json` staan, en schrijft `include/constants/map_compat.h`:
   `#define MAP_ROUTE119 (0x7E00 | 3)`, enz. Elke oude kaart krijgt een **eigen** waarde in een niet-bestaande groep
   (0x7E). Niet alles op `MAP_UNDEFINED` zetten: `switch`es met `case MAP_NUM(MAP_LILYCOVE_CITY): case
   MAP_NUM(MAP_MOSSDEEP_CITY):` (overworld.c) geven dan dubbele `case`-waarden.
2. `constants/map_groups.h` (gegenereerd) laat de compat-header aan het eind invoegen (in `include/constants/maps.h` of
   via een `#include` onderaan het gegenereerde bestand: kijk in `tools/mapjson` waar het bestand gemaakt wordt; liever
   in een niet-gegenereerd bestand dat overal al ingevoegd wordt, zoals `include/constants/maps.h`).
3. Code die op zo'n kaart test, is daarna gewoon nooit waar. Daarna bestand voor bestand opruimen en de header
   krimpen; aan het eind is hij leeg en gaat hij weg.

Hetzelfde voor trainers: **`opponents.h` in deze fase niet hernummeren**. De trainer-id's bepalen de trainerflags
(`TRAINER_FLAGS_START + id`); `MAX_TRAINERS_COUNT` (1200) blijft. Haal alleen de teams uit `trainers.party`
(`gTrainers` is met aangewezen initialisatie gevuld: een ontbrekend id wordt een leeg team). De constanten zelf kosten
niets; opruimen kan later in één keer, met de Keccles-id's gespaard.

Flags en vars blijven ook staan (`flags.h`, `vars.h`): ze kosten niets, en verschuiven zou de save-indeling raken.
Wel `FLAG_HIDE_*`-regels uit `data/scripts/new_game.inc` (158 stuks) die naar verdwenen kaarten verwijzen weghalen
(onschadelijk, maar ruis).

## Volgorde (na elke stap bouwen en een nieuw spel starten)
1. **Nieuwe groep en kaarten erbij** (er gaat nog niets weg): `gMapGroup_FullyUngrounded` met StartTown, PC 1F/2F,
   Mart, stock-huizen, TestMap. Heal location `HEAL_LOCATION_START_TOWN` in `heal_locations.json` (`respawn_map` =
   het PC). Mapsec: tijdelijk een nieuwe `MAPSEC_START_TOWN` in `region_map_sections.json` + beide popup-tabellen in
   `src/map_name_popup.c` (op de Hoenn-kaart een vakje dat al bestaat; de echte regiokaart komt later).
   `.include` van elk nieuw `scripts.inc` in `data/event_scripts.s` (anders linkerfout `*_MapScripts`).
2. **Nieuw spel daarheen:** `src/new_game.c` (`SetWarpDestination(... MAP_LITTLEROOT_TOWN ...)`, regels ±132/134)
   naar StartTown; respawn/`SetLastHealLocationWarp`. `data/scripts/new_game.inc` nalopen (zet het
   Littleroot-/truck-verloop flags of vars die nu nergens meer betekenis hebben?). Controleer korte intro, Mom
   (healen, PokéNav-registratie) als het spelershuis meekomt, en de titel ("Pokémon Fully Ungrounded", TODO-stap 5).
3. **Debugmenu:** `python3 tools/grounded/debug_zone_warps.py` draaien na elke kaartwijziging (genereert
   `src/data/debug_zone_warps.h`). Controleer de debug-scripts in `data/scripts/debug.inc` op `warp MAP_*`.
4. **Compat-header aanzetten** (zie hierboven), nog zonder iets weg te halen: bouwt identiek.
5. **Hoenn-kaarten en layouts weg** in één script (`tools/grounded/maptools/hoenn_eruit.py`): alle groepen behalve de
   nieuwe uit `map_groups.json` (tekstueel bewerken, niet met `json.dump`), de mappen uit `data/maps/`, de
   `.include`s uit `data/event_scripts.s`, layouts die niet in de bewaarlijst staan uit `layouts.json` +
   `data/layouts/`, kaarten uit `heal_locations.json` en `wild_encounters.json`. `build/emerald/data/maps.o` en de
   gegenereerde `data/maps/*.inc` verwijderen (make volgt ze niet altijd). Daarna `map_compat.py` en bouwen.
   Valkuilen hier:
   - `data/scripts/*.inc` met `warp`/`setwarp`/`setdynamicwarp`/`setescapewarp MAP_*` (bijv. Fly-/Dig-/teleport-,
     S.S. Tidal, kabelbaan, Battle Frontier, Trick House, Contest): via de compat-header bouwen ze; na de stap
     bestand voor bestand weghalen wat bij Hoenn hoort.
   - Tekstlabels in `data/text/*.inc` en `data/maps/*/text.inc` die vanuit C of algemene scripts gebruikt worden
     (Dialoogstudio-sleutels): de linker meldt ze, dan per geval oplossen.
   - Verbindingen (`connections`) en warps in de nieuwe kaarten mogen niet naar oude kaarten wijzen.
   - Kaartgroepnummers veranderen: oude saves en savestates zijn ongeldig (nieuw spel; Jordi waarschuwen).
6. **Trainers weg:** teams uit `trainers.party` behalve Keccles (en wat de TestMap gebruikt); `gRematchTable` in
   `battle_setup.c` (`REMATCH_TABLE_ENTRIES` uit `include/constants/rematches.h`, ook gebruikt door `vs_seeker.c`,
   Match Call en `src/gym_leader_rematch.c`) leeg maken of tot één plaatshouder terugbrengen; Match Call-gegevens
   (`src/data/... match_call`, PokéNav) leegmaken behalve Mom/Prof. als die blijven; Battle Frontier-trainers
   (`battle_frontier_trainers.h`, facility-teams) apart, samen met de Frontier-code.
7. **C-code per systeem opruimen** (compat-header krimpt), elk een eigen commit:
   - `field_specials.c` + `data/specials.inc`: Hoenn-specials (Sootopolis, Mirage Tower, Weather Institute, Glass
     Workshop, Lilycove Department Store, …) weg; ook de aanroepen in scripts.
   - `roamer.c`: routetabel leeg (Latios/Latias zwerven niet meer) of naar de nieuwe regio.
   - `wild_encounter.c`: Feebas-tegels Route 119, Altering Cave-varianten, Route 104/115-uitzonderingen,
     Sootopolis-Kyogre/Groudon-weer.
   - `pokedex_area_screen.c`: `MAP_GROUP_TOWNS_AND_ROUTES`/`DUNGEONS`/`SPECIAL_AREA` wijzen naar `MAP_PETALBURG_CITY`
     e.d.; naar de nieuwe groep. Feebas-uitzondering (`MAP_ROUTE119`) en roamer-markers weg. Het gebiedsscherm tekent
     op de Hoenn-regiokaart: werkt tot de nieuwe kaart er is, maar laat dan niets zien.
   - `overworld.c`: zee-routes/duikmuziek, Sootopolis-, Weather Institute-, Space Center-, Route 111-, Mauville- en
     Route 130-gevallen.
   - `item_use.c` (lijsten waar Itemfinder/fietsen/… niet mag), `save_location.c` (lijst van PC-kaarten: de nieuwe
     PC's erin, anders onthoudt het spel niet dat je in een PC saveerde), `battle_environment.h`,
     `follower_helper.c`, `union_room.c`, `pokemon_storage_system.c`, `field_door.c`, `field_weather_effect.c`,
     `rotating_gate.c`, `braille_puzzles.c`, `mirage_tower.c`, `faraway_island.c`, `tv.c`, `menu_helpers.c`,
     `party_menu.c`, `battle_util.c`, `battle_bg.c`, `dexnav.c`.
   - Eigen Ungrounded-systemen met kaartverwijzingen: `forces.c`, `burglar.c`, `enamorus.c`, `regi_dots.c`, de
     Grounded-specials (Kubfu, Wailord, …). Per systeem kijken of het een generiek mechaniek is (blijft, zonder
     kaart) of aan een Hoenn-plek hangt (weg).
   - Evoluties met `IF_IN_MAP` (Leafeon, Glaceon, Crabominable) en mapsec-evoluties (Magnezone/Vikavolt via
     `MAPSEC_CHARGESTONE_CAVE`): tijdelijk naar de TestMap of een item-evolutie; in de nieuwe regio een eigen plek.
   - `pokemon_sprite_visualizer.c` + `include/constants/pokemon_sprite_visualizer.h`: kaartlijst voor de
     achtergronden; naar de TestMap.
   - `region_map.c` (`sMapHealLocations` per MAPSEC, Fly): alleen StartTown; de Hoenn-regiokaart (graphics,
     `region_map_layout.h`) blijft als plaatshouder tot de nieuwe regiokaart er is. Fly vanuit de kaart (QoL) moet
     blijven werken: test het.
8. **Battle Frontier, Battle Tents, Trick House, Trainer Hill, Secret Bases, Contests:** kaarten gaan in stap 5 al
   weg; de code (`battle_tower.c`, `frontier_util.c`, `battle_pyramid.c`, `battle_pike.c`, `battle_factory.c`,
   `battle_dome.c`, `battle_palace`/`arena`, `trainer_hill.c`, `secret_base.c`, `contest*.c`, `frontier_pass.c`)
   blijft dan dood maar compileerbaar door de compat-header. Echt weghalen hoort bij TODO-stap 8 (eerst aan Jordi
   voorleggen welke vanilla-systemen weg mogen); let op save-data (`SaveBlock2.frontier`, secret bases in
   `SaveBlock1`): velden niet weghalen of verschuiven, alleen ongebruikt laten.
9. **Laatste controle:** compat-header leeg en weg, `python3 tools/grounded/audit.py`, een sweep zoals bij de 1.0
   (alle kaarten laden, alle warps), ROM-ruimte meten, en `ow_species_keep.py` draait vanzelf mee (minder
   Pokémon-overworlds in de ROM is verwacht).

## Andere valkuilen
- **`map_groups.json`/`layouts.json`** tekstueel bewerken (volgorde en notatie bewaren), daarna `json.load` als
  controle. Een lege groep kan niet; een groep die verdwijnt, ook uit `group_order`.
- **Heal locations:** `heal_locations.json` levert `HEAL_LOCATION_*`; `region_map.c`, scripts (`setrespawn`) en de
  Fly-QoL verwijzen ernaar. `respawn_npc` (`LOCALID_PLAYERS_HOUSE_1F_MOM`) moet in de nieuwe respawn-kaart bestaan.
- **Wilde encounters:** `wild_encounters.json` kent twee notaties (zie CLAUDE.md); de laatste header is de
  `MAP_UNDEFINED`-sentinel die `pokedex_area_screen.c` en `wild_encounter.c` verwachten. TestMap: 12 unieke soorten.
- **Berry trees:** `berry_tree` objecten met eigen ids (`src/data/berry_trees`/`tools/grounded/berry_tree_locations.py`)
  verdwijnen met de kaarten; de bessenlijst in de save blijft. De QoL (Wailmer Pail toont rijpe bessen, planten in één
  handeling) op de TestMap testen.
- **Objecten/flags in `map.json`** verwijzen naar `FLAG_HIDE_*`/`TRAINER_FLAGS_START+...`: met de kaarten weg, geen
  probleem; in nieuwe kaarten max. 16 objecten tegelijk.
- **`data/maps/*/text.inc`** met labels die de Dialoogstudio gebruikt: na de stap `tools/dialogen/export.py` alleen op
  verzoek opnieuw (zie CLAUDE.md); de studio verwijst dan naar verdwenen labels.
- **Grounded-tools** in `tools/grounded/maptools/` die Hoenn-kaarten bouwen (route135/136, meteor_falls_ext,
  area_zero, …) worden onbruikbaar; meenemen in de opruiming (bibliotheken als `landlib.py`, `snowlib.py`,
  `render_map.py`, `testrom.py`, `emu.py`, `make_intro_state.py` blijven). `make_intro_state.py` speelt de intro met
  vaste frames en toetsen: na de nieuwe start controleren (en bijwerken), anders werkt geen enkele emulatortest meer.
- **Debugmenu-scripts en testtools** (`testrom.py`, CLAUDE.md-recepten) gebruiken `MAP_*` van Hoenn
  (`warp MAP_ROUTE136_GROTTO`); na de stap de TestMap als standaard nemen.
- **Gegenereerde bestanden** (`include/constants/map_groups.h`, `data/maps/headers.inc`, `connections.inc`,
  `events.inc`, `data/layouts/layouts.inc`, `src/data/heal_locations.h`, `src/data/wild_encounters.h`) niet met de
  hand bewerken; bij vreemde fouten `build/emerald/data/maps.o` en de gegenereerde bestanden weggooien.

## Schatting
Stap 1–4: één sessie. Stap 5: één sessie (vooral linkerfouten). Stap 6–7: twee tot drie sessies (veel kleine
beslissingen; geschikt voor 2–3 agents met elk eigen bestanden). Stap 8 wacht op Jordi.
