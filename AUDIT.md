# Audit Project Grounded

Gegenereerd met `python3 tools/grounded/audit.py --md AUDIT.md` (statisch, zonder emulator). FOUT = vrijwel zeker een bug, MELD = even naar kijken / ontwerpkeuze, INFO = ter informatie. Bevindingen op kaarten/teksten die sinds vanilla niet veranderd zijn, staan er niet in. Bewust negeren: de sleutel tussen [ ] in `IGNORE` in het script zetten.

| Categorie | FOUT | MELD | INFO | tellingen |
|---|---|---|---|---|
| Warps | 0 | 11 | 4 | dynamisch 47, alleen aankomstpunt 67, warps 1800 |
| Kaarten en objecten | 0 | 11 | 0 | genegeerd 2, bereikbaarheid 518, kaarten 704 |
| Scripts en teksten | 0 | 0 | 0 | map-scripts 4508, labelverwijzingen 29713, coord-scripts 218, lock-paden 3005, teksten 5279 |
| Flags en vars | 0 | 1 | 0 | FLAG_GROUNDED 406, flags 1953, vars 285 |
| Trainers | 0 | 24 | 81 | level-vergelijking 537, belangrijke gevechten 78, evolutie-meldingen 77, partijen 1200, pokemon 5404, trainer-id's 1190, vrije id's 9, ongebruikte constanten 4, alleen op ongebruikte kaarten 0 |
| Wilde encounters | 0 | 3 | 8 | tabellen 387 |
| Items en TM's | 0 | 5 | 0 | item-balls 395, verborgen items 318, TM's 60 |

## Warps

- **MELD** JaggedPass_RuinCaldera warpt naar JaggedPass_RuinChamber, maar daar wijst geen warp terug (eenrichting/gat/script?) `[warpback:JaggedPass_RuinCaldera:JaggedPass_RuinChamber]`
- **MELD** RocketHideout_B2F warpt naar FortreeJungle, maar daar wijst geen warp terug (eenrichting/gat/script?) `[warpback:RocketHideout_B2F:FortreeJungle]`
- **MELD** Route115 warpt naar TerraCave_Entrance, maar daar wijst geen warp terug (eenrichting/gat/script?) `[warpback:Route115:TerraCave_Entrance]`
- **MELD** SkyPillar_ReverseB1F warpt naar SkyPillar_Outside, maar daar wijst geen warp terug (eenrichting/gat/script?) `[warpback:SkyPillar_ReverseB1F:SkyPillar_Outside]`
- **MELD** SkyPillar_Top warpt naar HallOfOrigin_Stairway, maar daar wijst geen warp terug (eenrichting/gat/script?) `[warpback:SkyPillar_Top:HallOfOrigin_Stairway]`
- **MELD** SpearPillar warpt naar HallOfOrigin_Stairway, maar daar wijst geen warp terug (eenrichting/gat/script?) `[warpback:SpearPillar:HallOfOrigin_Stairway]`
- **MELD** Underwater_Route105 warpt naar Underwater_MarineCave, maar daar wijst geen warp terug (eenrichting/gat/script?) `[warpback:Underwater_Route105:Underwater_MarineCave]`
- **MELD** Underwater_Route125 warpt naar Underwater_MarineCave, maar daar wijst geen warp terug (eenrichting/gat/script?) `[warpback:Underwater_Route125:Underwater_MarineCave]`
- **MELD** Underwater_Route127 warpt naar Underwater_MarineCave, maar daar wijst geen warp terug (eenrichting/gat/script?) `[warpback:Underwater_Route127:Underwater_MarineCave]`
- **MELD** Underwater_Route129 warpt naar Underwater_MarineCave, maar daar wijst geen warp terug (eenrichting/gat/script?) `[warpback:Underwater_Route129:Underwater_MarineCave]`
- **MELD** YoshisIsland_Beach warp 0 (15,15): tegel zonder warpgedrag (MB_SAND) en niets warpt hierheen (dode warp) `[warp:YoshisIsland_Beach:0:dead]`
- **INFO** PokemonTower_1F warp 0 (10,19): tegel zonder warpgedrag (MB_NORMAL) en niets warpt hierheen (dode warp) `[warp:PokemonTower_1F:0:dead]`
- **INFO** PokemonTower_1F warp 2 (12,19): tegel zonder warpgedrag (MB_NORMAL) en niets warpt hierheen (dode warp) `[warp:PokemonTower_1F:2:dead]`
- **INFO** Route115 warp 2 (26,9): tegel zonder warpgedrag (MB_MOUNTAIN_TOP) en niets warpt hierheen (dode warp) `[warp:Route115:2:dead]`
- **INFO** Underwater_WhirlIsland warp 1 (10,8): tegel zonder warpgedrag (MB_DEEP_WATER) en niets warpt hierheen (dode warp) `[warp:Underwater_WhirlIsland:1:dead]`

## Kaarten en objecten

- **MELD** gMapGroup_Dungeons: 128/128 kaarten `[groupfull:gMapGroup_Dungeons]`
- **MELD** AshfrostTown_House3: object 0 (MAN_1, AshfrostTown_House3_EventScript_Resident) staat op een muur/geblokkeerde tegel (4,4) [MB_NORMAL] `[wall:AshfrostTown_House3:0]`
- **MELD** BeaconIsle_Lighthouse_2F: object 0 (GIRL_3, BeaconIsle_Lighthouse_2F_EventScript_Keiko) staat op een muur/geblokkeerde tegel (2,7) [MB_NORMAL] `[wall:BeaconIsle_Lighthouse_2F:0]`
- **MELD** MeteorSpace: object 1 (DEOXYS, 0x0) staat op een muur/geblokkeerde tegel (22,0) [MB_NORMAL] `[wall:MeteorSpace:1]`
- **MELD** MtChimney: 32 objecten in totaal, tot 23 tegelijk in beeld rond (22, 12) (incl. objecten met flag; controleer dat ze niet allemaal tegelijk zichtbaar zijn) `[objview:MtChimney]`
- **MELD** MtPyre_Summit: object 8 (STEVEN, MtPyre_Summit_EventScript_Steven) staat op een muur/geblokkeerde tegel (21,8) [MB_NORMAL] `[wall:MtPyre_Summit:8]`
- **MELD** NothingIsland: object 0 (PLASMA_FRIGATE, 0x0) staat op een muur/geblokkeerde tegel (29,16) [MB_OCEAN_WATER] `[wall:NothingIsland:0]`
- **MELD** Route121: object 29 (ROCKET_GRUNT_M, 0x0) staat op een muur/geblokkeerde tegel (37,5) [MB_ANIMATED_DOOR] `[wall:Route121:29]`
- **MELD** Route123: 44 objecten in totaal, tot 16 tegelijk in beeld rond (17, 9) (incl. objecten met flag; controleer dat ze niet allemaal tegelijk zichtbaar zijn) `[objview:Route123]`
- **MELD** SlateportCity: 37 objecten in totaal, tot 16 tegelijk in beeld rond (24, 20) (incl. objecten met flag; controleer dat ze niet allemaal tegelijk zichtbaar zijn) `[objview:SlateportCity]`
- **MELD** YoshisIsland_Jungle: object 0 (POOCHY, YoshisIsland_Jungle_EventScript_Poochy) staat op een muur/geblokkeerde tegel (10,8) [MB_NORMAL] `[wall:YoshisIsland_Jungle:0]`

## Scripts en teksten

Niets open.

## Flags en vars

- **MELD** FLAG_UNUSED_RS_LEGENDARY_BATTLE_DONE heet "unused" maar wordt gebruikt in data/maps/CaveOfOrigin_1F/scripts.inc, data/maps/CaveOfOrigin_UnusedRubySapphireMap1/scripts.inc, data/maps/CaveOfOrigin_UnusedRubySapphireMap2/scripts.inc, data/maps/CaveOfOrigin_UnusedRubySapphireMap3/scripts.inc `[unusedused:FLAG_UNUSED_RS_LEGENDARY_BATTLE_DONE]`

## Trainers

- **MELD** TRAINER_ZINNIA_DELTA op MossdeepCity: ace lv 95, de andere trainers op die kaart rond lv 74 `[lvlfit:TRAINER_ZINNIA_DELTA]`
- **MELD** TRAINER_ANDREW op Route103: ace lv 75, de andere trainers op die kaart rond lv 14 `[lvlfit:TRAINER_ANDREW]`
- **MELD** TRAINER_RHETT op Route103: ace lv 27, de andere trainers op die kaart rond lv 14 `[lvlfit:TRAINER_RHETT]`
- **MELD** TRAINER_PETE op Route103: ace lv 42, de andere trainers op die kaart rond lv 14 `[lvlfit:TRAINER_PETE]`
- **MELD** TRAINER_ISABELLE op Route103: ace lv 42, de andere trainers op die kaart rond lv 14 `[lvlfit:TRAINER_ISABELLE]`
- **MELD** TRAINER_NED op Route106: ace lv 21, de andere trainers op die kaart rond lv 42 `[lvlfit:TRAINER_NED]`
- **MELD** TRAINER_EDWARD op Route110: ace lv 84, de andere trainers op die kaart rond lv 29 `[lvlfit:TRAINER_EDWARD]`
- **MELD** TRAINER_JACLYN op Route110: ace lv 52, de andere trainers op die kaart rond lv 29 `[lvlfit:TRAINER_JACLYN]`
- **MELD** TRAINER_NOLAN op Route114: ace lv 57, de andere trainers op die kaart rond lv 36 `[lvlfit:TRAINER_NOLAN]`
- **MELD** TRAINER_AARON op Route134: ace lv 83, de andere trainers op die kaart rond lv 69 `[lvlfit:TRAINER_AARON]`
- **MELD** TRAINER_COLTON op SSTidalRooms: ace lv 42, de andere trainers op die kaart rond lv 85 `[lvlfit:TRAINER_COLTON]`
- **MELD** TRAINER_STEVEN (Rival, MeteorFalls_StevensCave) heeft geen Mugshot: `[mugshot:TRAINER_STEVEN]`
- **MELD** TRAINER_MIMI (Rival, Route119) heeft geen Mugshot: `[mugshot:TRAINER_MIMI]`
- **MELD** TRAINER_ARCHIE_SERVICE_1 (Aqua Leader, Route119_WeatherInstitute_1F) heeft geen Mugshot: `[mugshot:TRAINER_ARCHIE_SERVICE_1]`
- **MELD** TRAINER_MAXIE_SERVICE_1 (Magma Leader, Route119_WeatherInstitute_1F) heeft geen Mugshot: `[mugshot:TRAINER_MAXIE_SERVICE_1]`
- **MELD** TRAINER_ARCHIE_SERVICE_2 (Aqua Leader, Route119_WeatherInstitute_1F) heeft geen Mugshot: `[mugshot:TRAINER_ARCHIE_SERVICE_2]`
- **MELD** TRAINER_MAXIE_SERVICE_2 (Magma Leader, Route119_WeatherInstitute_1F) heeft geen Mugshot: `[mugshot:TRAINER_MAXIE_SERVICE_2]`
- **MELD** TRAINER_ARCHIE_SERVICE_3 (Aqua Leader, Route119_WeatherInstitute_1F) heeft geen Mugshot: `[mugshot:TRAINER_ARCHIE_SERVICE_3]`
- **MELD** TRAINER_MAXIE_SERVICE_3 (Magma Leader, Route119_WeatherInstitute_1F) heeft geen Mugshot: `[mugshot:TRAINER_MAXIE_SERVICE_3]`
- **MELD** TRAINER_ARCHIE_SERVICE_4 (Aqua Leader, Route119_WeatherInstitute_1F) heeft geen Mugshot: `[mugshot:TRAINER_ARCHIE_SERVICE_4]`
- **MELD** TRAINER_MAXIE_SERVICE_4 (Magma Leader, Route119_WeatherInstitute_1F) heeft geen Mugshot: `[mugshot:TRAINER_MAXIE_SERVICE_4]`
- **MELD** TRAINER_RESORT_MISTY (Leader, ParadisoResort) heeft geen Mugshot: `[mugshot:TRAINER_RESORT_MISTY]`
- **MELD** TRAINER_RESORT_ERIKA (Leader, ParadisoResort) heeft geen Mugshot: `[mugshot:TRAINER_RESORT_ERIKA]`
- **MELD** TRAINER_RESORT_CYNTHIA (Champion, ParadisoResort_Lobby) heeft geen Mugshot: `[mugshot:TRAINER_RESORT_CYNTHIA]`
- **INFO** (81 stuks, eerste 60):
- **INFO** TRAINER_ANDREW: MAGIKARP op lv 70 is nog niet geëvolueerd (evolueert op 20) `[evo:TRAINER_ANDREW:0]`
- **INFO** TRAINER_ANDREW: MAGIKARP op lv 75 is nog niet geëvolueerd (evolueert op 20) `[evo:TRAINER_ANDREW:2]`
- **INFO** TRAINER_AUTUMN: SHROOMISH op lv 38 is nog niet geëvolueerd (evolueert op 23) `[evo:TRAINER_AUTUMN:0]`
- **INFO** TRAINER_BERNIE_1: PIDGEY op lv 36 is nog niet geëvolueerd (evolueert op 18) `[evo:TRAINER_BERNIE_1:1]`
- **INFO** TRAINER_BIRCH: WOOPER_PALDEA op lv 27 is nog niet geëvolueerd (evolueert op 20) `[evo:TRAINER_BIRCH:1]`
- **INFO** TRAINER_BRENDAN_ROUTE_110_MUDKIP: HOUNDOUR op lv 27 is nog niet geëvolueerd (evolueert op 24) `[evo:TRAINER_BRENDAN_ROUTE_110_MUDKIP:0]`
- **INFO** TRAINER_BROCK: GEODUDE op lv 32 is nog niet geëvolueerd (evolueert op 25) `[evo:TRAINER_BROCK:0]`
- **INFO** TRAINER_CHRIS: MAGIKARP op lv 29 is nog niet geëvolueerd (evolueert op 20) `[evo:TRAINER_CHRIS:0]`
- **INFO** TRAINER_COLRESS_MAUVILLE: ELGYEM op lv 34 is nog niet geëvolueerd (evolueert op 25) `[evo:TRAINER_COLRESS_MAUVILLE:0]`
- **INFO** TRAINER_COLRESS_MAUVILLE: KLINK op lv 34 is nog niet geëvolueerd (evolueert op 22) `[evo:TRAINER_COLRESS_MAUVILLE:1]`
- **INFO** TRAINER_COLRESS_MAUVILLE: MAGNEMITE op lv 34 is nog niet geëvolueerd (evolueert op 30) `[evo:TRAINER_COLRESS_MAUVILLE:2]`
- **INFO** TRAINER_COLTON: SKITTY op lv 36 is nog niet geëvolueerd (evolueert op 23) `[evo:TRAINER_COLTON:1]`
- **INFO** TRAINER_COLTON: SKITTY op lv 40 is nog niet geëvolueerd (evolueert op 23) `[evo:TRAINER_COLTON:2]`
- **INFO** TRAINER_COLTON: SKITTY op lv 30 is nog niet geëvolueerd (evolueert op 23) `[evo:TRAINER_COLTON:4]`
- **INFO** TRAINER_CORONET_AEON: DURALUDON op lv 95 is nog niet geëvolueerd (evolueert op 60) `[evo:TRAINER_CORONET_AEON:3]`
- **INFO** TRAINER_DALTON_1: WHISMUR op lv 31 is nog niet geëvolueerd (evolueert op 20) `[evo:TRAINER_DALTON_1:1]`
- **INFO** TRAINER_DALTON_1: JOLTIK op lv 31 is nog niet geëvolueerd (evolueert op 28) `[evo:TRAINER_DALTON_1:2]`
- **INFO** TRAINER_DAVE_PETALBURG: HAUNTER op lv 43 is nog niet geëvolueerd (evolueert op 37) `[evo:TRAINER_DAVE_PETALBURG:0]`
- **INFO** TRAINER_DAVE_ROUTE_111: GASTLY op lv 34 is nog niet geëvolueerd (evolueert op 25) `[evo:TRAINER_DAVE_ROUTE_111:0]`
- **INFO** TRAINER_DAVE_ROUTE_111: GIBLE op lv 34 is nog niet geëvolueerd (evolueert op 24) `[evo:TRAINER_DAVE_ROUTE_111:3]`
- **INFO** TRAINER_DEANDRE: ARON op lv 32 is nog niet geëvolueerd (evolueert op 24) `[evo:TRAINER_DEANDRE:1]`
- **INFO** TRAINER_DEANDRE: TRUMBEAK op lv 32 is nog niet geëvolueerd (evolueert op 28) `[evo:TRAINER_DEANDRE:2]`
- **INFO** TRAINER_DOJO_WATER_KEEPER: WIMPOD op lv 38 is nog niet geëvolueerd (evolueert op 30) `[evo:TRAINER_DOJO_WATER_KEEPER:1]`
- **INFO** TRAINER_EDWARD: ABRA op lv 21 is nog niet geëvolueerd (evolueert op 16) `[evo:TRAINER_EDWARD:0]`
- **INFO** TRAINER_EDWARD: ABRA op lv 28 is nog niet geëvolueerd (evolueert op 16) `[evo:TRAINER_EDWARD:1]`
- **INFO** TRAINER_EDWARD: ABRA op lv 35 is nog niet geëvolueerd (evolueert op 16) `[evo:TRAINER_EDWARD:2]`
- **INFO** TRAINER_EDWARD: ABRA op lv 56 is nog niet geëvolueerd (evolueert op 16) `[evo:TRAINER_EDWARD:3]`
- **INFO** TRAINER_EDWARD: ABRA op lv 84 is nog niet geëvolueerd (evolueert op 16) `[evo:TRAINER_EDWARD:4]`
- **INFO** TRAINER_GRUNT_MT_CHIMNEY_2: LITTEN op lv 36 is nog niet geëvolueerd (evolueert op 17) `[evo:TRAINER_GRUNT_MT_CHIMNEY_2:2]`
- **INFO** TRAINER_HARVEY: VIGOROTH op lv 44 is nog niet geëvolueerd (evolueert op 36) `[evo:TRAINER_HARVEY:0]`
- **INFO** TRAINER_HORATIO: VIGOROTH op lv 45 is nog niet geëvolueerd (evolueert op 36) `[evo:TRAINER_HORATIO:0]`
- **INFO** TRAINER_IVAN: GYARADOS op lv 4, maar MAGIKARP evolueert pas op 20 `[evo:TRAINER_IVAN:0]`
- **INFO** TRAINER_JACLYN: ABRA op lv 22 is nog niet geëvolueerd (evolueert op 16) `[evo:TRAINER_JACLYN:0]`
- **INFO** TRAINER_JOHNSON: ELECTABUZZ op lv 18, maar ELEKID evolueert pas op 30 `[evo:TRAINER_JOHNSON:2]`
- **INFO** TRAINER_JOHNSON: LUCARIO op lv 18, maar RIOLU evolueert pas op 30 `[evo:TRAINER_JOHNSON:5]`
- **INFO** TRAINER_KECCLES_1: CHARMANDER op lv 19 is nog niet geëvolueerd (evolueert op 16) `[evo:TRAINER_KECCLES_1:0]`
- **INFO** TRAINER_LAVA_TUBE_DAISY: DOLLIV op lv 40 is nog niet geëvolueerd (evolueert op 35) `[evo:TRAINER_LAVA_TUBE_DAISY:0]`
- **INFO** TRAINER_LOCAL_CELEBRITY: POOCHYENA op lv 34 is nog niet geëvolueerd (evolueert op 21) `[evo:TRAINER_LOCAL_CELEBRITY:0]`
- **INFO** TRAINER_LOLA_1: AZURILL op lv 23 is nog niet geëvolueerd (evolueert op 15) `[evo:TRAINER_LOLA_1:0]`
- **INFO** TRAINER_MAXIE_MT_CHIMNEY: FERROSEED op lv 38 is nog niet geëvolueerd (evolueert op 30) `[evo:TRAINER_MAXIE_MT_CHIMNEY:1]`
- **INFO** TRAINER_MEGA_FOREST_PERCIVAL: DURALUDON op lv 92 is nog niet geëvolueerd (evolueert op 60) `[evo:TRAINER_MEGA_FOREST_PERCIVAL:3]`
- **INFO** TRAINER_METEOR_DRAKE: SHELGON op lv 60 is nog niet geëvolueerd (evolueert op 50) `[evo:TRAINER_METEOR_DRAKE:0]`
- **INFO** TRAINER_MIGUEL_3: FLORAGATO op lv 40 is nog niet geëvolueerd (evolueert op 36) `[evo:TRAINER_MIGUEL_3:2]`
- **INFO** TRAINER_MIGUEL_3: TORRACAT op lv 40 is nog niet geëvolueerd (evolueert op 34) `[evo:TRAINER_MIGUEL_3:3]`
- **INFO** TRAINER_MIMI: MARILL op lv 50 is nog niet geëvolueerd (evolueert op 25) `[evo:TRAINER_MIMI:3]`
- **INFO** TRAINER_MITCH_ROUTE_110: TRAPINCH op lv 31 is nog niet geëvolueerd (evolueert op 25) `[evo:TRAINER_MITCH_ROUTE_110:0]`
- **INFO** TRAINER_MITCH_ROUTE_110: MAKUHITA op lv 31 is nog niet geëvolueerd (evolueert op 24) `[evo:TRAINER_MITCH_ROUTE_110:2]`
- **INFO** TRAINER_MITCH_ROUTE_121: METANG op lv 63 is nog niet geëvolueerd (evolueert op 45) `[evo:TRAINER_MITCH_ROUTE_121:1]`
- **INFO** TRAINER_MUSTARD: LUXIO op lv 40 is nog niet geëvolueerd (evolueert op 30) `[evo:TRAINER_MUSTARD:0]`
- **INFO** TRAINER_MUSTARD: JANGMO_O op lv 40 is nog niet geëvolueerd (evolueert op 35) `[evo:TRAINER_MUSTARD:2]`
- **INFO** TRAINER_PROF_OAK: BULBASAUR op lv 23 is nog niet geëvolueerd (evolueert op 16) `[evo:TRAINER_PROF_OAK:2]`
- **INFO** TRAINER_PROF_OAK: SQUIRTLE op lv 23 is nog niet geëvolueerd (evolueert op 16) `[evo:TRAINER_PROF_OAK:3]`
- **INFO** TRAINER_PROF_OAK: CHARMANDER op lv 23 is nog niet geëvolueerd (evolueert op 16) `[evo:TRAINER_PROF_OAK:4]`
- **INFO** TRAINER_RICK: KRICKETUNE op lv 12, maar KRICKETOT evolueert pas op 18 `[evo:TRAINER_RICK:4]`
- **INFO** TRAINER_RICKY_1: SENTRET op lv 26 is nog niet geëvolueerd (evolueert op 18) `[evo:TRAINER_RICKY_1:4]`
- **INFO** TRAINER_ROCKET_SCIENTIST: KLANG op lv 54 is nog niet geëvolueerd (evolueert op 47) `[evo:TRAINER_ROCKET_SCIENTIST:1]`
- **INFO** TRAINER_ROCKET_THIEF: CHANSEY op lv 54 is nog niet geëvolueerd (evolueert op 36) `[evo:TRAINER_ROCKET_THIEF:0]`
- **INFO** TRAINER_ROGER: MAGIKARP op lv 25 is nog niet geëvolueerd (evolueert op 20) `[evo:TRAINER_ROGER:1]`
- **INFO** TRAINER_RONALD: MAGIKARP op lv 70 is nog niet geëvolueerd (evolueert op 20) `[evo:TRAINER_RONALD:0]`
- **INFO** TRAINER_RUIN_MANIAC_SIMON: NOSEPASS op lv 47 is nog niet geëvolueerd (evolueert op 30) `[evo:TRAINER_RUIN_MANIAC_SIMON:1]`

Vrije trainer-id's (9): 601-602, 734, 883, 970, 972, 974, 976, 1198

## Wilde encounters

- **MELD** gArtisanCave_B1F land (lv tot 80, post-game): dubbele soorten SMEARGLE `[wild:gArtisanCave_B1F:land_mons:dup]`
- **MELD** gArtisanCave_1F land (lv tot 80, post-game): dubbele soorten SMEARGLE `[wild:gArtisanCave_1F:land_mons:dup]`
- **MELD** gAlteringCave1 land (lv tot 91, post-game): dubbele soorten ROARING_MOON `[wild:gAlteringCave1:land_mons:dup]`
- **INFO** gAlteringCave2 land (lv tot 18): dubbele soorten MAREEP `[wild:gAlteringCave2:land_mons:dup]`
- **INFO** gAlteringCave3 land (lv tot 44): dubbele soorten PINECO `[wild:gAlteringCave3:land_mons:dup]`
- **INFO** gAlteringCave4 land (lv tot 32): dubbele soorten HOUNDOUR `[wild:gAlteringCave4:land_mons:dup]`
- **INFO** gAlteringCave5 land (lv tot 23): dubbele soorten TEDDIURSA `[wild:gAlteringCave5:land_mons:dup]`
- **INFO** gAlteringCave6 land (lv tot 42): dubbele soorten AIPOM `[wild:gAlteringCave6:land_mons:dup]`
- **INFO** gAlteringCave7 land (lv tot 42): dubbele soorten SHUCKLE `[wild:gAlteringCave7:land_mons:dup]`
- **INFO** gAlteringCave8 land (lv tot 42): dubbele soorten STANTLER `[wild:gAlteringCave8:land_mons:dup]`
- **INFO** gAlteringCave9 land (lv tot 42): dubbele soorten SMEARGLE `[wild:gAlteringCave9:land_mons:dup]`

## Items en TM's

- **MELD** ITEM_TM_DARK_PULSE komt op meer plekken voor: C: src/trainer_hill.c (nieuw); ligt: MtPyre_Exterior (nieuw) `[tm:ITEM_TM_DARK_PULSE]`
- **MELD** ITEM_TM_FIRE_BLAST komt op meer plekken voor: ligt: JaggedPass_LavaTube (nieuw); winkel: LilycoveCity_DepartmentStore_4F `[tm:ITEM_TM_FIRE_BLAST]`
- **MELD** ITEM_TM_NASTY_PLOT komt op meer plekken voor: C: src/trainer_hill.c (nieuw); script: SlateportCity_BattleTentLobby (nieuw) `[tm:ITEM_TM_NASTY_PLOT]`
- **MELD** ITEM_TM_STORED_POWER komt op meer plekken voor: C: src/trainer_hill.c (nieuw); script: Route114 (nieuw) `[tm:ITEM_TM_STORED_POWER]`
- **MELD** ITEM_TM_U_TURN komt op meer plekken voor: ligt: FortreeJungle (nieuw); winkel: LilycoveCity_DepartmentStore_4F (nieuw) `[tm:ITEM_TM_U_TURN]`
