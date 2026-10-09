# Audit Project Grounded

Gegenereerd met `python3 tools/grounded/audit.py --md AUDIT.md` (statisch, zonder emulator). FOUT = vrijwel zeker een bug, MELD = even naar kijken / ontwerpkeuze, INFO = ter informatie. Bevindingen op kaarten/teksten die sinds vanilla niet veranderd zijn, staan er niet in. Bewust negeren: de sleutel tussen [ ] in `IGNORE` in het script zetten.

| Categorie | FOUT | MELD | INFO | tellingen |
|---|---|---|---|---|
| Warps | 0 | 11 | 4 | dynamisch 47, alleen aankomstpunt 67, warps 1800 |
| Kaarten en objecten | 0 | 11 | 0 | genegeerd 2, bereikbaarheid 518, kaarten 704 |
| Scripts en teksten | 0 | 0 | 0 | map-scripts 4508, labelverwijzingen 29713, coord-scripts 218, lock-paden 3005, teksten 5279 |
| Flags en vars | 0 | 1 | 0 | FLAG_GROUNDED 406, flags 1953, vars 285 |
| Trainers | 0 | 0 | 4 | partijen 1200, pokemon 5404, trainer-id's 1190, vrije id's 9, ongebruikte constanten 4, alleen op ongebruikte kaarten 0 |
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

- **INFO** TRAINER_BRENDAN_PLACEHOLDER (id 853) wordt nergens gebruikt (kan vrij) `[unusedtrainer:TRAINER_BRENDAN_PLACEHOLDER]`
- **INFO** TRAINER_LEAF (id 852) wordt nergens gebruikt (kan vrij) `[unusedtrainer:TRAINER_LEAF]`
- **INFO** TRAINER_MAY_PLACEHOLDER (id 854) wordt nergens gebruikt (kan vrij) `[unusedtrainer:TRAINER_MAY_PLACEHOLDER]`
- **INFO** TRAINER_RED (id 851) wordt nergens gebruikt (kan vrij) `[unusedtrainer:TRAINER_RED]`

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
