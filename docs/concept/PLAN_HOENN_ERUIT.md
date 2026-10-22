# Plan: de Hoenn-wereld eruit (TODO-stap 6, met stap 5)

Opgesteld 22 okt, na het opruimen van de intro's. Nog niet uitgevoerd. Doel: alleen het skelet blijft over, en na elke
stap bouwt het (`make -j4 2>&1 | grep -i error` leeg) en start een nieuw spel.

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
