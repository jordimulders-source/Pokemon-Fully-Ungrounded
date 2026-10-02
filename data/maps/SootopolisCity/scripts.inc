SootopolisCity_MapScripts::
	map_script MAP_SCRIPT_ON_LOAD, SootopolisCity_OnLoad
	map_script MAP_SCRIPT_ON_TRANSITION, SootopolisCity_OnTransition
	map_script MAP_SCRIPT_ON_RESUME, SootopolisCity_OnResume
	map_script MAP_SCRIPT_ON_FRAME_TABLE, SootopolisCity_OnFrame
	map_script MAP_SCRIPT_ON_WARP_INTO_MAP_TABLE, SootopolisCity_OnWarp
	.byte 0

SootopolisCity_OnLoad:
	call_if_unset FLAG_SOOTOPOLIS_ARCHIE_MAXIE_LEAVE, SootopolisCity_EventScript_LockGymDoor
	goto_if_unset FLAG_KYOGRE_ESCAPED_SEAFLOOR_CAVERN, SootopolisCity_EventScript_LegendariesNotArrived
	call_if_unset FLAG_SOOTOPOLIS_ARCHIE_MAXIE_LEAVE, SootopolisCity_EventScript_LockHouseDoors
	end

SootopolisCity_EventScript_LegendariesNotArrived::
	end

SootopolisCity_EventScript_LockHouseDoors::
	setmetatile 9, 6, METATILE_Sootopolis_Door_Closed, TRUE
	setmetatile 9, 17, METATILE_Sootopolis_Door_Closed, TRUE
	setmetatile 9, 26, METATILE_Sootopolis_Door_Closed, TRUE
	setmetatile 44, 17, METATILE_Sootopolis_Door_Closed, TRUE
	setmetatile 8, 35, METATILE_Sootopolis_Door_Closed, TRUE
	setmetatile 53, 28, METATILE_Sootopolis_Door_Closed, TRUE
	setmetatile 45, 6, METATILE_Sootopolis_Door_Closed, TRUE
	setmetatile 48, 25, METATILE_Sootopolis_Door_Closed, TRUE
	setmetatile 51, 36, METATILE_Sootopolis_Door_Closed, TRUE
	return

SootopolisCity_EventScript_LockGymDoor::
	setmetatile 31, 32, METATILE_Sootopolis_GymDoor_Closed, TRUE
	return

SootopolisCity_OnTransition:
	setflag FLAG_VISITED_SOOTOPOLIS_CITY
	setflag FLAG_HIDE_SOOTOPOLIS_KECCLES
	setflag FLAG_HIDE_SOOTOPOLIS_TROPIUS
	call_if_eq VAR_SOOTOPOLIS_CITY_STATE, 1, SootopolisCity_EventScript_HideMapNamePopup
	call_if_eq VAR_SKY_PILLAR_STATE, 1, SootopolisCity_EventScript_HideMapNamePopup
	call SootopolisCity_EventScript_SetWeather
	call SootopolisCity_EventScript_SetLayout
	call_if_eq VAR_SOOTOPOLIS_CITY_STATE, 1, SootopolisCity_EventScript_SetBattleSpectators
	call_if_eq VAR_SOOTOPOLIS_CITY_STATE, 2, SootopolisCity_EventScript_SetBattleSpectators
	call_if_eq VAR_SOOTOPOLIS_CITY_STATE, 3, SootopolisCity_EventScript_SetBattleSpectators
	call_if_eq VAR_SOOTOPOLIS_CITY_STATE, 4, SootopolisCity_EventScript_SetBattleSpectators
	call_if_eq VAR_SOOTOPOLIS_CITY_STATE, 5, SootopolisCity_EventScript_SetBattleSpectators
	call_if_eq VAR_SOOTOPOLIS_CITY_STATE, 2, SootopolisCity_EventScript_CheckSetEnterCaveOfOriginObjPos
	call_if_eq VAR_SOOTOPOLIS_CITY_STATE, 3, SootopolisCity_EventScript_CheckSetEnterCaveOfOriginObjPos
	call_if_eq VAR_SOOTOPOLIS_CITY_STATE, 4, SootopolisCity_EventScript_SetExitCaveOfOriginObjPos
	call_if_eq VAR_SOOTOPOLIS_CITY_STATE, 5, SootopolisCity_EventScript_SetOutsideGymObjPos
	call_if_eq VAR_SOOTOPOLIS_CITY_STATE, 6, SootopolisCity_EventScript_SetExpertBlockCaveEntrance
	end

SootopolisCity_EventScript_HideMapNamePopup::
	setflag FLAG_HIDE_MAP_NAME_POPUP
	return

SootopolisCity_EventScript_SetBattleSpectators::
	setobjectxyperm LOCALID_KIRI, 13, 48
	setobjectxyperm LOCALID_SOOTOPOLIS_BOY_1, 46, 32
	setobjectxyperm LOCALID_SOOTOPOLIS_NINJA_BOY, 48, 41
	setobjectxyperm LOCALID_SOOTOPOLIS_WOMAN_1, 45, 43
	setobjectmovementtype LOCALID_KIRI, MOVEMENT_TYPE_FACE_UP
	setobjectmovementtype LOCALID_SOOTOPOLIS_BOY_1, MOVEMENT_TYPE_FACE_LEFT
	setobjectmovementtype LOCALID_SOOTOPOLIS_NINJA_BOY, MOVEMENT_TYPE_FACE_LEFT
	setobjectmovementtype LOCALID_SOOTOPOLIS_WOMAN_1, MOVEMENT_TYPE_FACE_LEFT
	return

SootopolisCity_EventScript_SetLayout::
	goto_if_eq VAR_SOOTOPOLIS_CITY_STATE, 0, SootopolisCity_EventScript_SetNormalLayout
	goto_if_ge VAR_SOOTOPOLIS_CITY_STATE, 6, SootopolisCity_EventScript_SetNormalLayout
	goto_if_eq VAR_SOOTOPOLIS_CITY_STATE, 1, SootopolisCity_EventScript_SetLegendariesLayout
	goto_if_eq VAR_SOOTOPOLIS_CITY_STATE, 2, SootopolisCity_EventScript_SetLegendariesLayout
	goto_if_eq VAR_SOOTOPOLIS_CITY_STATE, 3, SootopolisCity_EventScript_SetLegendariesLayout
	goto_if_eq VAR_SOOTOPOLIS_CITY_STATE, 4, SootopolisCity_EventScript_SetLegendariesLayout
	goto_if_le VAR_SKY_PILLAR_STATE, 1, SootopolisCity_EventScript_SetLegendariesLayout
	return

SootopolisCity_EventScript_SetNormalLayout::
	return

SootopolisCity_EventScript_SetLegendariesLayout::
	setmaplayoutindex LAYOUT_SOOTOPOLIS_CITY_LEGENDS_BATTLE
	return

SootopolisCity_EventScript_SetWeather::
	goto_if_eq VAR_SOOTOPOLIS_CITY_STATE, 0, SootopolisCity_EventScript_SetNormalWeather
	goto_if_ge VAR_SOOTOPOLIS_CITY_STATE, 6, SootopolisCity_EventScript_SetNormalWeather
	goto_if_eq VAR_SOOTOPOLIS_CITY_STATE, 1, SootopolisCity_EventScript_SetDownpour
	goto_if_eq VAR_SKY_PILLAR_STATE, 1, SootopolisCity_EventScript_SetDownpour
	goto_if_le VAR_SKY_PILLAR_STATE, 1, Common_EventScript_SetAbnormalWeather
	return

SootopolisCity_EventScript_SetNormalWeather::
	return

SootopolisCity_EventScript_SetDownpour::
	setweather WEATHER_DOWNPOUR
	return

SootopolisCity_EventScript_CheckSetEnterCaveOfOriginObjPos::
	goto_if_set FLAG_STEVEN_GUIDES_TO_CAVE_OF_ORIGIN, SootopolisCity_EventScript_SetEnterCaveOfOriginObjPos
	return

SootopolisCity_EventScript_SetEnterCaveOfOriginObjPos::
	setobjectxyperm LOCALID_SOOTOPOLIS_EXPERT, 30, 18
	setobjectxyperm LOCALID_SOOTOPOLIS_STEVEN, 32, 18
	return

SootopolisCity_EventScript_SetExitCaveOfOriginObjPos::
	setobjectxyperm LOCALID_SOOTOPOLIS_EXPERT, 30, 18
	setobjectxyperm LOCALID_SOOTOPOLIS_WALLACE, 31, 18
	setobjectxyperm LOCALID_SOOTOPOLIS_STEVEN, 32, 18
	end

SootopolisCity_EventScript_SetOutsideGymObjPos::
	setobjectxyperm LOCALID_SOOTOPOLIS_EXPERT, 31, 18
	setobjectxyperm LOCALID_SOOTOPOLIS_STEVEN, 29, 33
	setobjectxyperm LOCALID_SOOTOPOLIS_MAXIE, 33, 35
	setobjectxyperm LOCALID_SOOTOPOLIS_ARCHIE, 34, 35
	call_if_eq VAR_SOOTOPOLIS_WALLACE_STATE, 0, SootopolisCity_EventScript_SetWallaceMiddle
	call_if_eq VAR_SOOTOPOLIS_WALLACE_STATE, 1, SootopolisCity_EventScript_SetWallaceRight
	call_if_eq VAR_SOOTOPOLIS_WALLACE_STATE, 2, SootopolisCity_EventScript_SetWallaceLeft
	call_if_eq VAR_SOOTOPOLIS_KECCLES_STATE, 1, SootopolisCity_EventScript_SetKecclesSceneObjPos
	return

@ Project Grounded: Maxie en Archie tegenover de speler voor de scène met Keccles
SootopolisCity_EventScript_SetKecclesSceneObjPos::
	setobjectxyperm LOCALID_SOOTOPOLIS_MAXIE, 34, 34
	setobjectxyperm LOCALID_SOOTOPOLIS_ARCHIE, 34, 35
	setobjectmovementtype LOCALID_SOOTOPOLIS_MAXIE, MOVEMENT_TYPE_FACE_LEFT
	setobjectmovementtype LOCALID_SOOTOPOLIS_ARCHIE, MOVEMENT_TYPE_FACE_LEFT
	return

SootopolisCity_EventScript_SetWallaceMiddle::
	setobjectxyperm LOCALID_SOOTOPOLIS_WALLACE, 31, 33
	setobjectmovementtype LOCALID_SOOTOPOLIS_WALLACE, MOVEMENT_TYPE_FACE_DOWN
	return

SootopolisCity_EventScript_SetWallaceRight::
	setobjectxyperm LOCALID_SOOTOPOLIS_WALLACE, 32, 33
	setobjectmovementtype LOCALID_SOOTOPOLIS_WALLACE, MOVEMENT_TYPE_FACE_DOWN
	return

SootopolisCity_EventScript_SetWallaceLeft::
	setobjectxyperm LOCALID_SOOTOPOLIS_WALLACE, 30, 33
	setobjectmovementtype LOCALID_SOOTOPOLIS_WALLACE, MOVEMENT_TYPE_FACE_DOWN
	return

SootopolisCity_EventScript_SetExpertBlockCaveEntrance::
	setobjectxyperm LOCALID_SOOTOPOLIS_EXPERT, 31, 18
	return

SootopolisCity_OnWarp:
	map_script_2 VAR_SOOTOPOLIS_CITY_STATE, 5, SootopolisCity_EventScript_PlayerFaceLegendaries
	.2byte 0

SootopolisCity_EventScript_PlayerFaceLegendaries::
	call_if_eq VAR_SKY_PILLAR_STATE, 1, SootopolisCity_EventScript_PlayerFaceLegendaries1
	call_if_eq VAR_SKY_PILLAR_STATE, 2, SootopolisCity_EventScript_PlayerFaceLegendaries2
	end

SootopolisCity_EventScript_PlayerFaceLegendaries1::
	turnobject LOCALID_PLAYER, DIR_NORTH
	return

SootopolisCity_EventScript_PlayerFaceLegendaries2::
	turnobject LOCALID_PLAYER, DIR_NORTH
	setvar VAR_SKY_PILLAR_STATE, 3
	return

SootopolisCity_OnResume:
	setdivewarp MAP_UNDERWATER_SOOTOPOLIS_CITY, 9, 6
	end

SootopolisCity_OnFrame:
	map_script_2 VAR_SOOTOPOLIS_CITY_STATE, 1, SootopolisCity_EventScript_StartLegendariesScene
	map_script_2 VAR_SOOTOPOLIS_KECCLES_STATE, 1, SootopolisCity_EventScript_KecclesScene
	map_script_2 VAR_SKY_PILLAR_STATE, 1, SootopolisCity_EventScript_StartRayquazaScene
	.2byte 0

@ If not at PokeCenter, assumed to have arrived via Dive
SootopolisCity_EventScript_StartLegendariesScene::
	lockall
	special StorePlayerCoordsInVars
	goto_if_ne VAR_0x8004, 43, SootopolisCity_EventScript_LegendariesSceneFromDive
	goto_if_ne VAR_0x8005, 32, SootopolisCity_EventScript_LegendariesSceneFromDive
	goto SootopolisCity_EventScript_LegendariesSceneFromPokeCenter
	end

SootopolisCity_EventScript_LegendariesSceneFromPokeCenter::
	delay 60
	special SpawnCameraObject
	applymovement LOCALID_CAMERA, SootopolisCity_Movement_PanToActionFromPokeCenter
	waitmovement 0
	special RemoveCameraObject
	delay 60
	fadescreenspeed FADE_TO_BLACK, 8
	setweather WEATHER_ABNORMAL
	doweather
	setvar VAR_0x8004, FALSE @ Just do Groudon/Kyogre fight scene
	special Script_DoRayquazaScene
	waitstate
	applymovement LOCALID_SOOTOPOLIS_KYOGRE, Common_Movement_WalkInPlaceFasterLeft
	applymovement LOCALID_SOOTOPOLIS_GROUDON, Common_Movement_WalkInPlaceFasterRight
	waitmovement 0
	delay 60
	waitse
	playmoncry SPECIES_KYOGRE, CRY_MODE_ENCOUNTER
	applymovement LOCALID_SOOTOPOLIS_KYOGRE, SootopolisCity_Movement_KyogreAttack
	applymovement LOCALID_SOOTOPOLIS_GROUDON, SootopolisCity_Movement_GroudonDefend
	waitmovement 0
	setvar VAR_0x8004, 1  @ vertical pan
	setvar VAR_0x8005, 1  @ horizontal pan
	setvar VAR_0x8006, 8  @ num shakes
	setvar VAR_0x8007, 5  @ shake delay
	special ShakeCamera
	waitstate
	applymovement LOCALID_SOOTOPOLIS_KYOGRE, SootopolisCity_Movement_KyogreMoveBack
	applymovement LOCALID_SOOTOPOLIS_GROUDON, SootopolisCity_Movement_GroudonMoveBack
	waitmovement 0
	waitse
	playmoncry SPECIES_GROUDON, CRY_MODE_ENCOUNTER
	applymovement LOCALID_SOOTOPOLIS_KYOGRE, SootopolisCity_Movement_KyogreDefend
	applymovement LOCALID_SOOTOPOLIS_GROUDON, SootopolisCity_Movement_GroudonAttack
	waitmovement 0
	setvar VAR_0x8004, 1  @ vertical pan
	setvar VAR_0x8005, 1  @ horizontal pan
	setvar VAR_0x8006, 8  @ num shakes
	setvar VAR_0x8007, 5  @ shake delay
	special ShakeCamera
	waitstate
	applymovement LOCALID_SOOTOPOLIS_KYOGRE, SootopolisCity_Movement_KyogreMoveBack
	applymovement LOCALID_SOOTOPOLIS_GROUDON, SootopolisCity_Movement_GroudonMoveBack
	waitmovement 0
	waitse
	playmoncry SPECIES_KYOGRE, CRY_MODE_ENCOUNTER
	applymovement LOCALID_SOOTOPOLIS_KYOGRE, SootopolisCity_Movement_KyogreAttack
	applymovement LOCALID_SOOTOPOLIS_GROUDON, SootopolisCity_Movement_GroudonDefend
	waitmovement 0
	setvar VAR_0x8004, 1  @ vertical pan
	setvar VAR_0x8005, 1  @ horizontal pan
	setvar VAR_0x8006, 8  @ num shakes
	setvar VAR_0x8007, 5  @ shake delay
	special ShakeCamera
	waitstate
	applymovement LOCALID_SOOTOPOLIS_KYOGRE, SootopolisCity_Movement_KyogreMoveBack
	applymovement LOCALID_SOOTOPOLIS_GROUDON, SootopolisCity_Movement_GroudonMoveBack
	waitmovement 0
	special SpawnCameraObject
	applymovement LOCALID_SOOTOPOLIS_KYOGRE, SootopolisCity_Movement_KyogreIdle
	applymovement LOCALID_SOOTOPOLIS_GROUDON, SootopolisCity_Movement_GroudonIdle
	applymovement LOCALID_CAMERA, SootopolisCity_Movement_PanBackToPokeCenter
	waitmovement 0
	special RemoveCameraObject
	setvar VAR_SOOTOPOLIS_CITY_STATE, 2
	clearflag FLAG_HIDE_MAP_NAME_POPUP
	releaseall
	end

SootopolisCity_Movement_PanToActionFromPokeCenter:
	walk_slow_diag_southwest
	walk_slow_diag_southwest
	walk_slow_diag_southwest
	walk_slow_diag_southwest
	walk_slow_diag_southwest
	walk_slow_diag_southwest
	walk_slow_diag_southwest
	walk_slow_diag_southwest
	walk_slow_diag_southwest
	walk_slow_diag_southwest
	walk_slow_diag_southwest
	walk_slow_diag_southwest
	step_end

SootopolisCity_Movement_PanBackToPokeCenter:
	walk_slow_diag_northeast
	walk_slow_diag_northeast
	walk_slow_diag_northeast
	walk_slow_diag_northeast
	walk_slow_diag_northeast
	walk_slow_diag_northeast
	walk_slow_diag_northeast
	walk_slow_diag_northeast
	walk_slow_diag_northeast
	walk_slow_diag_northeast
	walk_slow_diag_northeast
	walk_slow_diag_northeast
	step_end

SootopolisCity_EventScript_LegendariesSceneFromDive::
	delay 60
	special SpawnCameraObject
	applymovement LOCALID_CAMERA, SootopolisCity_Movement_PanToActionFromDive
	waitmovement 0
	special RemoveCameraObject
	delay 60
	fadescreenspeed FADE_TO_BLACK, 8
	setweather WEATHER_ABNORMAL
	doweather
	setvar VAR_0x8004, FALSE @ Just do Groudon/Kyogre fight scene
	special Script_DoRayquazaScene
	waitstate
	applymovement LOCALID_SOOTOPOLIS_KYOGRE, Common_Movement_WalkInPlaceFasterLeft
	applymovement LOCALID_SOOTOPOLIS_GROUDON, Common_Movement_WalkInPlaceFasterRight
	waitmovement 0
	delay 60
	waitse
	playmoncry SPECIES_KYOGRE, CRY_MODE_ENCOUNTER
	applymovement LOCALID_SOOTOPOLIS_KYOGRE, SootopolisCity_Movement_KyogreAttack
	applymovement LOCALID_SOOTOPOLIS_GROUDON, SootopolisCity_Movement_GroudonDefend
	waitmovement 0
	setvar VAR_0x8004, 1  @ vertical pan
	setvar VAR_0x8005, 1  @ horizontal pan
	setvar VAR_0x8006, 8  @ num shakes
	setvar VAR_0x8007, 5  @ shake delay
	special ShakeCamera
	waitstate
	applymovement LOCALID_SOOTOPOLIS_KYOGRE, SootopolisCity_Movement_KyogreMoveBack
	applymovement LOCALID_SOOTOPOLIS_GROUDON, SootopolisCity_Movement_GroudonMoveBack
	waitmovement 0
	waitse
	playmoncry SPECIES_GROUDON, CRY_MODE_ENCOUNTER
	applymovement LOCALID_SOOTOPOLIS_KYOGRE, SootopolisCity_Movement_KyogreDefend
	applymovement LOCALID_SOOTOPOLIS_GROUDON, SootopolisCity_Movement_GroudonAttack
	waitmovement 0
	setvar VAR_0x8004, 1  @ vertical pan
	setvar VAR_0x8005, 1  @ horizontal pan
	setvar VAR_0x8006, 8  @ num shakes
	setvar VAR_0x8007, 5  @ shake delay
	special ShakeCamera
	waitstate
	applymovement LOCALID_SOOTOPOLIS_KYOGRE, SootopolisCity_Movement_KyogreMoveBack
	applymovement LOCALID_SOOTOPOLIS_GROUDON, SootopolisCity_Movement_GroudonMoveBack
	waitmovement 0
	waitse
	playmoncry SPECIES_KYOGRE, CRY_MODE_ENCOUNTER
	applymovement LOCALID_SOOTOPOLIS_KYOGRE, SootopolisCity_Movement_KyogreAttack
	applymovement LOCALID_SOOTOPOLIS_GROUDON, SootopolisCity_Movement_GroudonDefend
	waitmovement 0
	setvar VAR_0x8004, 1  @ vertical pan
	setvar VAR_0x8005, 1  @ horizontal pan
	setvar VAR_0x8006, 8  @ num shakes
	setvar VAR_0x8007, 5  @ shake delay
	special ShakeCamera
	waitstate
	applymovement LOCALID_SOOTOPOLIS_KYOGRE, SootopolisCity_Movement_KyogreMoveBack
	applymovement LOCALID_SOOTOPOLIS_GROUDON, SootopolisCity_Movement_GroudonMoveBack
	waitmovement 0
	special SpawnCameraObject
	applymovement LOCALID_SOOTOPOLIS_KYOGRE, SootopolisCity_Movement_KyogreIdle
	applymovement LOCALID_SOOTOPOLIS_GROUDON, SootopolisCity_Movement_GroudonIdle
	applymovement LOCALID_CAMERA, SootopolisCity_Movement_PanBackToDive
	waitmovement 0
	special RemoveCameraObject
	setvar VAR_SOOTOPOLIS_CITY_STATE, 2
	clearflag FLAG_HIDE_MAP_NAME_POPUP
	releaseall
	end

SootopolisCity_Movement_PanToActionFromDive:
	walk_slow_diag_northeast
	walk_slow_diag_northeast
	walk_up
	walk_up
	walk_up
	walk_up
	walk_up
	walk_up
	walk_up
	step_end

SootopolisCity_Movement_PanBackToDive:
	walk_down
	walk_down
	walk_down
	walk_down
	walk_down
	walk_down
	walk_down
	walk_slow_diag_southwest
	walk_slow_diag_southwest
	step_end

SootopolisCity_Movement_KyogreAttack:
	walk_in_place_slow_left
	walk_in_place_slow_left
	walk_in_place_slow_left
	delay_16
	delay_16
	delay_16
	init_affine_anim
	walk_left_affine
	clear_affine_anim
	step_end

SootopolisCity_Movement_KyogreDefend:
	delay_16
	delay_16
	delay_16
	delay_16
	delay_16
	delay_16
	delay_16
	delay_16
	delay_16
	init_affine_anim
	walk_left_affine
	clear_affine_anim
	step_end

SootopolisCity_Movement_KyogreMoveBack:
	lock_facing_direction
	walk_right
	delay_16
	delay_16
	delay_16
	unlock_facing_direction
	step_end

SootopolisCity_Movement_KyogreIdle:
	walk_in_place_slow_left
	walk_in_place_slow_left
	walk_in_place_slow_left
	walk_in_place_slow_left
	walk_in_place_slow_left
	walk_in_place_slow_left
	step_end

SootopolisCity_Movement_GroudonAttack:
	walk_in_place_slow_right
	walk_in_place_slow_right
	walk_in_place_slow_right
	delay_16
	delay_16
	delay_16
	walk_fast_right
	step_end

SootopolisCity_Movement_GroudonDefend:
	delay_16
	delay_16
	delay_16
	delay_16
	delay_16
	delay_16
	delay_16
	delay_16
	delay_16
	walk_fast_right
	step_end

SootopolisCity_Movement_GroudonMoveBack:
	lock_facing_direction
	walk_left
	delay_16
	delay_16
	delay_16
	unlock_facing_direction
	step_end

SootopolisCity_Movement_GroudonIdle:
	walk_in_place_slow_right
	walk_in_place_slow_right
	walk_in_place_slow_right
	walk_in_place_slow_right
	walk_in_place_slow_right
	walk_in_place_slow_right
	step_end

@ If not at PokeCenter, assumed to have arrived via Dive
SootopolisCity_EventScript_StartRayquazaScene::
	lockall
	special StorePlayerCoordsInVars
	goto_if_ne VAR_0x8004, 43, SootopolisCity_EventScript_RayquazaSceneFromDive
	goto_if_ne VAR_0x8005, 32, SootopolisCity_EventScript_RayquazaSceneFromDive
	goto SootopolisCity_EventScript_RayquazaSceneFromPokeCenter
	end

SootopolisCity_EventScript_RayquazaSceneFromPokeCenter::
	delay 60
	special SpawnCameraObject
	applymovement LOCALID_CAMERA, SootopolisCity_Movement_PanToActionFromPokeCenter
	waitmovement 0
	special RemoveCameraObject
	delay 60
	fadescreenspeed FADE_TO_BLACK, 8
	call SootopolisCity_EventScript_SetRoughWater
	removeobject LOCALID_SOOTOPOLIS_GROUDON
	removeobject LOCALID_SOOTOPOLIS_KYOGRE
	addobject LOCALID_SOOTOPOLIS_RAYQUAZA
	hideobjectat LOCALID_SOOTOPOLIS_RAYQUAZA, MAP_SOOTOPOLIS_CITY
	setvar VAR_0x8004, TRUE
	special Script_DoRayquazaScene
	waitstate
	playse SE_THUNDER
	special SpawnCameraObject
	applymovement LOCALID_CAMERA, SootopolisCity_Movement_PanUp
	waitmovement 0
	waitse
	playmoncry SPECIES_RAYQUAZA, CRY_MODE_ENCOUNTER
	setvar VAR_0x8004, 1  @ vertical pan
	setvar VAR_0x8005, 1  @ horizontal pan
	setvar VAR_0x8006, 8  @ num shakes
	setvar VAR_0x8007, 3  @ shake delay
	special ShakeCamera
	waitstate
	waitse
	playmoncry SPECIES_RAYQUAZA, CRY_MODE_ENCOUNTER
	setvar VAR_0x8004, 1  @ vertical pan
	setvar VAR_0x8005, 2  @ horizontal pan
	setvar VAR_0x8006, 8  @ num shakes
	setvar VAR_0x8007, 5  @ shake delay
	special ShakeCamera
	waitstate
	waitmoncry
	setweather WEATHER_NONE
	doweather
	applymovement LOCALID_SOOTOPOLIS_RAYQUAZA, SootopolisCity_Movement_RayquazaFlyOff
	waitmovement 0
	removeobject LOCALID_SOOTOPOLIS_RAYQUAZA
	special WaitWeather
	waitstate
	clearflag FLAG_SYS_WEATHER_CTRL
	setvar VAR_SKY_PILLAR_STATE, 3
	clearflag FLAG_LEGENDARIES_IN_SOOTOPOLIS
	fadenewbgm MUS_SOOTOPOLIS
	delay 120
	clearflag FLAG_HIDE_MAP_NAME_POPUP
	setvar VAR_SOOTOPOLIS_KECCLES_STATE, 1  @ Project Grounded: Archie, Maxie en Keccles
	warpwhitefade MAP_SOOTOPOLIS_CITY, 31, 35
	waitstate
	end

SootopolisCity_EventScript_RayquazaSceneFromDive::
	delay 60
	special SpawnCameraObject
	applymovement LOCALID_CAMERA, SootopolisCity_Movement_PanToActionFromDive
	waitmovement 0
	special RemoveCameraObject
	delay 60
	fadescreenspeed FADE_TO_BLACK, 8
	call SootopolisCity_EventScript_SetRoughWater
	removeobject LOCALID_SOOTOPOLIS_GROUDON
	removeobject LOCALID_SOOTOPOLIS_KYOGRE
	addobject LOCALID_SOOTOPOLIS_RAYQUAZA
	setvar VAR_0x8004, TRUE
	special Script_DoRayquazaScene
	waitstate
	special SpawnCameraObject
	applymovement LOCALID_CAMERA, SootopolisCity_Movement_PanUp
	applymovement LOCALID_PLAYER, SootopolisCity_Movement_PlayerApproachLegendaries
	waitmovement 0
	waitse
	playmoncry SPECIES_RAYQUAZA, CRY_MODE_ENCOUNTER
	setvar VAR_0x8004, 1  @ vertical pan
	setvar VAR_0x8005, 1  @ horizontal pan
	setvar VAR_0x8006, 8  @ num shakes
	setvar VAR_0x8007, 3  @ shake delay
	special ShakeCamera
	waitstate
	waitse
	playmoncry SPECIES_RAYQUAZA, CRY_MODE_ENCOUNTER
	setvar VAR_0x8004, 1  @ vertical pan
	setvar VAR_0x8005, 2  @ horizontal pan
	setvar VAR_0x8006, 8  @ num shakes
	setvar VAR_0x8007, 5  @ shake delay
	special ShakeCamera
	waitstate
	waitmoncry
	setweather WEATHER_NONE
	doweather
	applymovement LOCALID_SOOTOPOLIS_RAYQUAZA, SootopolisCity_Movement_RayquazaFlyOff
	waitmovement 0
	removeobject LOCALID_SOOTOPOLIS_RAYQUAZA
	special WaitWeather
	waitstate
	clearflag FLAG_SYS_WEATHER_CTRL
	setvar VAR_SKY_PILLAR_STATE, 2
	clearflag FLAG_LEGENDARIES_IN_SOOTOPOLIS
	fadenewbgm MUS_SURF
	delay 120
	clearflag FLAG_HIDE_MAP_NAME_POPUP
	setvar VAR_SOOTOPOLIS_KECCLES_STATE, 1  @ Project Grounded: Archie, Maxie en Keccles
	warpwhitefade MAP_SOOTOPOLIS_CITY, 31, 35
	waitstate
	end

SootopolisCity_EventScript_SetRoughWater::
	setmetatile 27, 43, METATILE_Sootopolis_RoughWater, FALSE
	setmetatile 28, 43, METATILE_Sootopolis_RoughWater, FALSE
	setmetatile 29, 43, METATILE_Sootopolis_RoughWater, FALSE
	setmetatile 30, 43, METATILE_Sootopolis_RoughWater, FALSE
	setmetatile 27, 44, METATILE_Sootopolis_RoughWater, FALSE
	setmetatile 28, 44, METATILE_Sootopolis_RoughWater, FALSE
	setmetatile 29, 44, METATILE_Sootopolis_RoughWater, FALSE
	setmetatile 30, 44, METATILE_Sootopolis_RoughWater, FALSE
	setmetatile 27, 45, METATILE_Sootopolis_RoughWater, FALSE
	setmetatile 28, 45, METATILE_Sootopolis_RoughWater, FALSE
	setmetatile 29, 45, METATILE_Sootopolis_RoughWater, FALSE
	setmetatile 30, 45, METATILE_Sootopolis_RoughWater, FALSE
	setmetatile 32, 43, METATILE_Sootopolis_RoughWater, FALSE
	setmetatile 33, 43, METATILE_Sootopolis_RoughWater, FALSE
	setmetatile 34, 43, METATILE_Sootopolis_RoughWater, FALSE
	setmetatile 35, 43, METATILE_Sootopolis_RoughWater, FALSE
	setmetatile 32, 44, METATILE_Sootopolis_RoughWater, FALSE
	setmetatile 33, 44, METATILE_Sootopolis_RoughWater, FALSE
	setmetatile 34, 44, METATILE_Sootopolis_RoughWater, FALSE
	setmetatile 35, 44, METATILE_Sootopolis_RoughWater, FALSE
	setmetatile 32, 45, METATILE_Sootopolis_RoughWater, FALSE
	setmetatile 33, 45, METATILE_Sootopolis_RoughWater, FALSE
	setmetatile 34, 45, METATILE_Sootopolis_RoughWater, FALSE
	setmetatile 35, 45, METATILE_Sootopolis_RoughWater, FALSE
	return

SootopolisCity_Movement_RayquazaFlyOff:
	walk_fast_up
	walk_faster_up
	walk_faster_up
	walk_faster_up
	walk_faster_up
	walk_faster_up
	walk_faster_up
	step_end

SootopolisCity_Movement_PanUp:
	walk_up
	walk_up
	walk_up
	walk_up
	step_end

SootopolisCity_Movement_PlayerApproachLegendaries:
	walk_up
	walk_up
	walk_up
	walk_up
	step_end

@ Unused
SootopolisCity_Movement_PlayerApproachLegendariesDown:
	walk_down
	walk_down
	walk_down
	walk_down
	step_end

@ Unused
SootopolisCity_Movement_UnusedPanUp:
	walk_slow_diag_northeast
	walk_slow_diag_northeast
	walk_slow_diag_northeast
	walk_slow_diag_northeast
	walk_slow_diag_northeast
	walk_slow_diag_northeast
	walk_slow_diag_northeast
	walk_slow_diag_northeast
	walk_right
	walk_right
	walk_right
	walk_right
	step_end

@ Unused
SootopolisCity_Movement_UnusedPanBack:
	walk_down
	walk_down
	walk_down
	walk_down
	walk_down
	walk_down
	walk_down
	walk_down
	walk_down
	walk_down
	walk_down
	walk_slow_diag_southwest
	walk_slow_diag_southwest
	step_end

SootopolisCity_EventScript_CaveOfOriginExpert::
	lock
	faceplayer
	goto_if_ge VAR_SOOTOPOLIS_CITY_STATE, 6, SootopolisCity_EventScript_ExpertPostLegendaries
	goto_if_eq VAR_SOOTOPOLIS_CITY_STATE, 5, SootopolisCity_EventScript_ExpertLegendaries
	goto_if_ge VAR_SOOTOPOLIS_CITY_STATE, 2, SootopolisCity_EventScript_ExpertLeadToCave
	msgbox SootopolisCity_Text_CaveOfOriginPleaseLeave, MSGBOX_DEFAULT
	release
	end

SootopolisCity_EventScript_ExpertLeadToCave::
	msgbox SootopolisCity_Text_LeadSuperiorTrainerToCave, MSGBOX_DEFAULT
	release
	end

SootopolisCity_EventScript_ExpertPostLegendaries::
	msgbox SootopolisCity_Text_CaveOfOriginSleepsToo, MSGBOX_DEFAULT
	release
	end

SootopolisCity_EventScript_ExpertLegendaries::
	msgbox SootopolisCity_Text_AwakenedPokemonClash, MSGBOX_DEFAULT
	release
	end

SootopolisCity_EventScript_Kiri::
	lock
	faceplayer
	goto_if_le VAR_SOOTOPOLIS_CITY_STATE, 1, SootopolisCity_EventScript_KiriGiveBerry
	goto_if_ge VAR_SOOTOPOLIS_CITY_STATE, 6, SootopolisCity_EventScript_KiriGiveBerry
	goto_if_eq VAR_SOOTOPOLIS_CITY_STATE, 5, SootopolisCity_EventScript_KiriRayquaza
	msgbox SootopolisCity_Text_BigPokemonFighting, MSGBOX_DEFAULT
	closemessage
	applymovement LOCALID_KIRI, Common_Movement_FaceOriginalDirection
	waitmovement 0
	release
	end

SootopolisCity_EventScript_KiriRayquaza::
	msgbox SootopolisCity_Text_PrettyMonCameFromSky, MSGBOX_DEFAULT
	closemessage
	release
	end

@ Gives 2 berries daily. First ranges from FIRST_KIRI_BERRY to LAST_KIRI_BERRY, second is always Figy or Iapapa
SootopolisCity_EventScript_KiriGiveBerry::
	dotimebasedevents
	special GetPlayerBigGuyGirlString
	goto_if_set FLAG_DAILY_SOOTOPOLIS_RECEIVED_BERRY, SootopolisCity_EventScript_KiriReceivedBerry
	msgbox SootopolisCity_Text_NameIsKiriHaveOneOfThese, MSGBOX_DEFAULT
	random NUM_KIRI_BERRIES
	addvar VAR_RESULT, NUM_KIRI_BERRIES_SKIPPED
	addvar VAR_RESULT, FIRST_BERRY_INDEX
	giveitem VAR_RESULT
	goto_if_eq VAR_RESULT, FALSE, Common_EventScript_ShowBagIsFull
	setflag FLAG_DAILY_SOOTOPOLIS_RECEIVED_BERRY
	msgbox SootopolisCity_Text_GiveYouThisBerryToo, MSGBOX_DEFAULT
	random 2
	goto_if_eq VAR_RESULT, 0, SootopolisCity_EventScript_GiveFigyBerry
	goto_if_eq VAR_RESULT, 1, SootopolisCity_EventScript_GiveIapapaBerry
	end

SootopolisCity_EventScript_GiveFigyBerry::
	giveitem ITEM_FIGY_BERRY
	goto_if_eq VAR_RESULT, FALSE, Common_EventScript_ShowBagIsFull
	msgbox SootopolisCity_Text_WhatKindOfWishInYourName, MSGBOX_DEFAULT
	release
	end

SootopolisCity_EventScript_GiveIapapaBerry::
	giveitem ITEM_IAPAPA_BERRY
	goto_if_eq VAR_RESULT, FALSE, Common_EventScript_ShowBagIsFull
	msgbox SootopolisCity_Text_WhatKindOfWishInYourName, MSGBOX_DEFAULT
	release
	end

SootopolisCity_EventScript_KiriReceivedBerry::
	msgbox SootopolisCity_Text_LikeSeasonBornIn, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, YES, SootopolisCity_EventScript_KiriLikeSeasonBornIn
	msgbox SootopolisCity_Text_OhDoesntMatter, MSGBOX_DEFAULT
	release
	end

SootopolisCity_EventScript_KiriLikeSeasonBornIn::
	msgbox SootopolisCity_Text_ThenILoveAutumn, MSGBOX_DEFAULT
	release
	end

SootopolisCity_EventScript_Woman2::
	lockall
	applymovement LOCALID_SOOTOPOLIS_WOMAN_2, Common_Movement_FacePlayer
	waitmovement 0
	goto_if_eq VAR_SOOTOPOLIS_CITY_STATE, 5, SootopolisCity_EventScript_Woman2Rayquaza
	msgbox SootopolisCity_Text_WeatherWentWild, MSGBOX_DEFAULT
	closemessage
	applymovement LOCALID_SOOTOPOLIS_WOMAN_2, Common_Movement_FaceOriginalDirection
	waitmovement 0
	releaseall
	end

SootopolisCity_EventScript_Woman2Rayquaza::
	msgbox SootopolisCity_Text_YouBroughtFlyingMon, MSGBOX_DEFAULT
	releaseall
	end

SootopolisCity_EventScript_Man::
	lock
	faceplayer
	goto_if_ge VAR_SOOTOPOLIS_CITY_STATE, 6, SootopolisCity_EventScript_ManPostLegendaries
	msgbox SootopolisCity_Text_NoOrdinaryTourist, MSGBOX_DEFAULT
	release
	end

SootopolisCity_EventScript_ManPostLegendaries::
	msgbox SootopolisCity_Text_CityRegainedCalm, MSGBOX_DEFAULT
	release
	end

SootopolisCity_EventScript_Woman1::
	lock
	faceplayer
	goto_if_ge VAR_SOOTOPOLIS_CITY_STATE, 6, SootopolisCity_EventScript_Woman1PostLegendaries
	goto_if_eq VAR_SOOTOPOLIS_CITY_STATE, 5, SootopolisCity_EventScript_Woman1Rayquaza
	goto_if_ge VAR_SOOTOPOLIS_CITY_STATE, 2, SootopolisCity_EventScript_Woman1Legendaries
	msgbox SootopolisCity_Text_SootopolisSkyBeautiful, MSGBOX_DEFAULT
	release
	end

SootopolisCity_EventScript_Woman1Legendaries::
	msgbox SootopolisCity_Text_GiganticPokemonFight, MSGBOX_DEFAULT
	closemessage
	applymovement LOCALID_SOOTOPOLIS_WOMAN_1, Common_Movement_FaceOriginalDirection
	waitmovement 0
	release
	end

SootopolisCity_EventScript_Woman1PostLegendaries::
	msgbox SootopolisCity_Text_NightSkyFavoriteScenery, MSGBOX_DEFAULT
	release
	end

SootopolisCity_EventScript_Woman1Rayquaza::
	msgbox SootopolisCity_Text_FearedWorstWhenPokemonFlewDown, MSGBOX_DEFAULT
	release
	end

SootopolisCity_EventScript_NinjaBoy::
	lockall
	applymovement LOCALID_SOOTOPOLIS_NINJA_BOY, Common_Movement_FacePlayer
	waitmovement 0
	goto_if_eq VAR_SOOTOPOLIS_CITY_STATE, 5, SootopolisCity_EventScript_NinjaBoyRayquaza
	goto_if_ge VAR_SOOTOPOLIS_CITY_STATE, 6, SootopolisCity_EventScript_NinjaBoyNormal
	goto_if_le VAR_SOOTOPOLIS_CITY_STATE, 1, SootopolisCity_EventScript_NinjaBoyNormal
	msgbox SootopolisCity_Text_ThisIsWicked, MSGBOX_DEFAULT
	closemessage
	applymovement LOCALID_SOOTOPOLIS_NINJA_BOY, Common_Movement_FaceOriginalDirection
	waitmovement 0
	release
	end

SootopolisCity_EventScript_NinjaBoyNormal::
	msgbox SootopolisCity_Text_WonderWhatWorldIsLike, MSGBOX_DEFAULT
	release
	end

SootopolisCity_EventScript_NinjaBoyRayquaza::
	msgbox SootopolisCity_Text_ThatWasWicked, MSGBOX_DEFAULT
	release
	end

SootopolisCity_EventScript_Boy1::
	lockall
	applymovement LOCALID_SOOTOPOLIS_BOY_1, Common_Movement_FacePlayer
	waitmovement 0
	goto_if_eq VAR_SOOTOPOLIS_CITY_STATE, 5, SootopolisCity_EventScript_Boy1Rayquaza
	goto_if_set FLAG_SYS_GAME_CLEAR, SootopolisCity_EventScript_Boy1GameClear
	goto_if_ge VAR_SOOTOPOLIS_CITY_STATE, 6, SootopolisCity_EventScript_Boy1Normal
	goto_if_le VAR_SOOTOPOLIS_CITY_STATE, 1, SootopolisCity_EventScript_Boy1Normal
	msgbox SootopolisCity_Text_GiantPokemonSuddenlyAppeared, MSGBOX_DEFAULT
	closemessage
	applymovement LOCALID_SOOTOPOLIS_BOY_1, Common_Movement_FaceOriginalDirection
	waitmovement 0
	release
	end

SootopolisCity_EventScript_Boy1Rayquaza::
	msgbox SootopolisCity_Text_WhatIsThatGreenPokemon, MSGBOX_DEFAULT
	release
	end

SootopolisCity_EventScript_Boy1GameClear::
	msgbox SootopolisCity_Text_WhereDidLegendariesGo, MSGBOX_DEFAULT
	release
	end

SootopolisCity_EventScript_Boy1Normal::
	msgbox SootopolisCity_Text_PhysicallyFitLivingHere, MSGBOX_DEFAULT
	release
	end

SootopolisCity_EventScript_GymSign::
	msgbox SootopolisCity_Text_GymSign, MSGBOX_SIGN
	end

SootopolisCity_EventScript_CitySign::
	msgbox SootopolisCity_Text_CitySign, MSGBOX_SIGN
	end

EventScript_ClosedSootopolisDoor::
	msgbox SootopolisCity_Text_DoorIsClosed, MSGBOX_SIGN
	end

SootopolisCity_EventScript_Steven::
	lockall
	applymovement LOCALID_SOOTOPOLIS_STEVEN, Common_Movement_FacePlayer
	waitmovement 0
	call_if_unset FLAG_STEVEN_GUIDES_TO_CAVE_OF_ORIGIN, SootopolisCity_EventScript_StevenLeadPlayerCaveOfOrigin
	goto_if_eq VAR_SOOTOPOLIS_CITY_STATE, 2, SootopolisCity_EventScript_StevenHelpWallace
	goto_if_eq VAR_SOOTOPOLIS_CITY_STATE, 3, SootopolisCity_EventScript_StevenHelpedWallace
	goto_if_eq VAR_SOOTOPOLIS_CITY_STATE, 4, SootopolisCity_EventScript_StevenHelpedWallace
	goto_if_set FLAG_SOOTOPOLIS_ARCHIE_MAXIE_LEAVE, SootopolisCity_EventScript_StevenMaxieArchieLeft
	msgbox SootopolisCity_Text_SoThatsRayquaza, MSGBOX_DEFAULT
	releaseall
	end

SootopolisCity_EventScript_StevenHelpWallace::
	msgbox SootopolisCity_Text_KnowWhatsNeededToHelpHim, MSGBOX_DEFAULT
	releaseall
	end

SootopolisCity_EventScript_StevenMaxieArchieLeft::
	msgbox SootopolisCity_Text_MaxieArchieLeft, MSGBOX_DEFAULT
	releaseall
	end

SootopolisCity_EventScript_StevenHelpedWallace::
	msgbox SootopolisCity_Text_NeverBeenToSkyPillar, MSGBOX_DEFAULT
	releaseall
	end

SootopolisCity_EventScript_StevenLeadPlayerCaveOfOrigin::
	msgbox SootopolisCity_Text_InvolvedWithCrisisComeWithMe, MSGBOX_DEFAULT
	closemessage
	call_if_eq VAR_FACING, DIR_WEST, SootopolisCity_EventScript_StartWalkToCaveOfOriginWest
	call_if_eq VAR_FACING, DIR_NORTH, SootopolisCity_EventScript_StartWalkToCaveOfOriginNorth
	msgbox SootopolisCity_Text_DoesThisMakeYourFearPokemon, MSGBOX_DEFAULT
	closemessage
	applymovement LOCALID_SOOTOPOLIS_STEVEN, SootopolisCity_Movement_StevenWalkToCaveOfOrigin
	applymovement LOCALID_PLAYER, SootopolisCity_Movement_PlayerWalkToCaveOfOrigin
	waitmovement 0
	delay 120
	applymovement LOCALID_SOOTOPOLIS_EXPERT, SootopolisCity_Movement_ExpertMoveAside
	waitmovement 0
	applymovement LOCALID_SOOTOPOLIS_STEVEN, SootopolisCity_Movement_StevenArriveCaveEntrance
	applymovement LOCALID_PLAYER, SootopolisCity_Movement_PlayerArriveCaveEntrance
	waitmovement 0
	msgbox SootopolisCity_Text_HereWereAreHelpWallace, MSGBOX_DEFAULT
	closemessage
	setflag FLAG_STEVEN_GUIDES_TO_CAVE_OF_ORIGIN
	applymovement LOCALID_PLAYER, SootopolisCity_Movement_PlayerEnterCaveOfOrigin
	waitmovement 0
	warp MAP_CAVE_OF_ORIGIN_ENTRANCE, 9, 20
	waitstate
	end

SootopolisCity_EventScript_StartWalkToCaveOfOriginWest::
	applymovement LOCALID_SOOTOPOLIS_STEVEN, SootopolisCity_Movement_StevenStartWalkToCaveOfOrigin
	applymovement LOCALID_PLAYER, SootopolisCity_Movement_PlayerStartWalkToCaveOfOriginWest
	waitmovement 0
	return

SootopolisCity_EventScript_StartWalkToCaveOfOriginNorth::
	applymovement LOCALID_SOOTOPOLIS_STEVEN, SootopolisCity_Movement_StevenStartWalkToCaveOfOrigin
	applymovement LOCALID_PLAYER, SootopolisCity_Movement_PlayerStartWalkToCaveOfOriginNorth
	waitmovement 0
	return

SootopolisCity_Movement_StevenStartWalkToCaveOfOrigin:
	walk_up
	walk_up
	walk_up
	walk_right
	walk_up
	walk_up
	walk_up
	walk_up
	walk_up
	walk_up
	walk_up
	walk_up
	walk_up
	walk_up
	walk_up
	walk_left
	walk_up
	walk_up
	walk_up
	walk_up
	walk_left
	walk_left
	walk_left
	walk_left
	walk_up
	walk_up
	walk_up
	walk_up
	walk_up
	walk_up
	walk_up
	walk_up
	walk_up
	walk_up
	walk_up
	walk_in_place_faster_down
	step_end

SootopolisCity_Movement_PlayerStartWalkToCaveOfOriginWest:
	walk_left
	walk_up
	walk_up
	walk_up
	walk_right
	walk_up
	walk_up
	walk_up
	walk_up
	walk_up
	walk_up
	walk_up
	walk_up
	walk_up
	walk_up
	walk_up
	walk_left
	walk_up
	walk_up
	walk_up
	walk_up
	walk_left
	walk_left
	walk_left
	walk_left
	walk_up
	walk_up
	walk_up
	walk_up
	walk_up
	walk_up
	walk_up
	walk_up
	walk_up
	walk_up
	step_end

SootopolisCity_Movement_PlayerStartWalkToCaveOfOriginNorth:
	walk_up
	walk_up
	walk_up
	walk_up
	walk_right
	walk_up
	walk_up
	walk_up
	walk_up
	walk_up
	walk_up
	walk_up
	walk_up
	walk_up
	walk_up
	walk_up
	walk_left
	walk_up
	walk_up
	walk_up
	walk_up
	walk_left
	walk_left
	walk_left
	walk_left
	walk_up
	walk_up
	walk_up
	walk_up
	walk_up
	walk_up
	walk_up
	walk_up
	walk_up
	walk_up
	step_end

SootopolisCity_Movement_StevenWalkToCaveOfOrigin:
	walk_up
	walk_up
	walk_right
	walk_right
	walk_right
	walk_right
	walk_down
	walk_down
	walk_right
	walk_right
	walk_right
	walk_right
	walk_right
	walk_up
	walk_right
	walk_right
	walk_right
	walk_right
	walk_down
	walk_down
	walk_down
	walk_right
	walk_right
	walk_right
	walk_right
	walk_right
	walk_down
	walk_down
	walk_down
	walk_down
	walk_left
	walk_left
	walk_left
	walk_left
	walk_left
	walk_left
	walk_left
	walk_left
	walk_down
	walk_down
	walk_down
	walk_down
	walk_down
	walk_down
	walk_down
	walk_down
	walk_right
	walk_right
	walk_right
	walk_right
	delay_4
	walk_in_place_faster_left
	delay_16
	delay_16
	walk_right
	walk_up
	walk_up
	step_end

SootopolisCity_Movement_PlayerWalkToCaveOfOrigin:
	walk_up
	walk_up
	walk_up
	walk_right
	walk_right
	walk_right
	walk_right
	walk_down
	walk_down
	walk_right
	walk_right
	walk_right
	walk_right
	walk_right
	walk_up
	walk_right
	walk_right
	walk_right
	walk_right
	walk_down
	walk_down
	walk_down
	walk_right
	walk_right
	walk_right
	walk_right
	walk_right
	walk_down
	walk_down
	walk_down
	walk_down
	walk_left
	walk_left
	walk_left
	walk_left
	walk_left
	walk_left
	walk_left
	walk_left
	walk_down
	walk_down
	walk_down
	walk_down
	walk_down
	walk_down
	walk_down
	walk_down
	walk_right
	walk_right
	walk_right
	step_end

SootopolisCity_Movement_ExpertMoveAside:
	walk_slow_left
	walk_in_place_faster_right
	step_end

SootopolisCity_Movement_StevenArriveCaveEntrance:
	walk_down
	walk_down
	walk_left
	delay_8
	walk_right
	walk_up
	walk_up
	walk_up
	walk_right
	walk_in_place_faster_left
	step_end

SootopolisCity_Movement_PlayerArriveCaveEntrance:
	delay_16
	delay_16
	delay_16
	delay_8
	walk_right
	walk_right
	walk_up
	walk_up
	walk_up
	walk_in_place_faster_right
	step_end

SootopolisCity_Movement_PlayerEnterCaveOfOrigin:
	walk_up
	walk_up
	step_end

SootopolisCity_EventScript_Boy2::
	lockall
	applymovement LOCALID_SOOTOPOLIS_BOY_2, Common_Movement_FacePlayer
	waitmovement 0
	goto_if_eq VAR_SOOTOPOLIS_CITY_STATE, 5, SootopolisCity_EventScript_Boy2Rayquaza
	msgbox SootopolisCity_Text_TwoPokemonArentAngry, MSGBOX_DEFAULT
	closemessage
	applymovement LOCALID_SOOTOPOLIS_BOY_2, Common_Movement_FaceOriginalDirection
	waitmovement 0
	releaseall
	end

SootopolisCity_EventScript_Boy2Rayquaza::
	msgbox SootopolisCity_Text_FlyingMonStoppedRampage, MSGBOX_DEFAULT
	closemessage
	releaseall
	end

SootopolisCity_EventScript_BlackBelt::
	lockall
	goto_if_eq VAR_SOOTOPOLIS_CITY_STATE, 5, SootopolisCity_EventScript_BlackBeltRayquaza
	msgbox SootopolisCity_Text_GoRedAndBlueMon, MSGBOX_DEFAULT
	closemessage
	applymovement LOCALID_SOOTOPOLIS_BLACK_BELT, Common_Movement_FacePlayer
	waitmovement 0
	msgbox SootopolisCity_Text_DoYouKnowMonNames, MSGBOX_DEFAULT
	closemessage
	applymovement LOCALID_SOOTOPOLIS_BLACK_BELT, Common_Movement_FaceOriginalDirection
	waitmovement 0
	releaseall
	end

SootopolisCity_EventScript_BlackBeltRayquaza::
	applymovement LOCALID_SOOTOPOLIS_BLACK_BELT, Common_Movement_FacePlayer
	waitmovement 0
	msgbox SootopolisCity_Text_GreenOneSettlesThings, MSGBOX_DEFAULT
	releaseall
	end

SootopolisCity_EventScript_Girl::
	lockall
	applymovement LOCALID_SOOTOPOLIS_GIRL, Common_Movement_FacePlayer
	waitmovement 0
	goto_if_eq VAR_SOOTOPOLIS_CITY_STATE, 5, SootopolisCity_EventScript_GirlRayquaza
	msgbox SootopolisCity_Text_SootopolisWillBeWrecked, MSGBOX_DEFAULT
	closemessage
	applymovement LOCALID_SOOTOPOLIS_GIRL, Common_Movement_FaceOriginalDirection
	waitmovement 0
	releaseall
	end

SootopolisCity_EventScript_GirlRayquaza::
	msgbox SootopolisCity_Text_SootopolisDidntGetWrecked, MSGBOX_DEFAULT
	closemessage
	releaseall
	end

SootopolisCity_EventScript_Maniac::
	lockall
	applymovement LOCALID_SOOTOPOLIS_MANIAC, Common_Movement_FacePlayer
	waitmovement 0
	goto_if_eq VAR_SOOTOPOLIS_CITY_STATE, 5, SootopolisCity_EventScript_ManiacRayquaza
	msgbox SootopolisCity_Text_SeeingLegendWithOwnEyes, MSGBOX_DEFAULT
	closemessage
	applymovement LOCALID_SOOTOPOLIS_MANIAC, Common_Movement_FaceOriginalDirection
	waitmovement 0
	releaseall
	end

SootopolisCity_EventScript_ManiacRayquaza::
	msgbox SootopolisCity_Text_SawLegendWithOwnEyes, MSGBOX_DEFAULT
	releaseall
	end

SootopolisCity_EventScript_Wallace::
	lock
	faceplayer
	goto_if_eq VAR_SOOTOPOLIS_CITY_STATE, 4, SootopolisCity_EventScript_GoToSkyPillar
	goto_if_set FLAG_RECEIVED_HM_WATERFALL, SootopolisCity_EventScript_GoToGym
	goto_if_set FLAG_SOOTOPOLIS_ARCHIE_MAXIE_LEAVE, SootopolisCity_EventScript_GiveWaterfall
	msgbox SootopolisCity_Text_AquaMagmaDidntMeanHarm, MSGBOX_DEFAULT
	release
	end

SootopolisCity_EventScript_GiveWaterfall::
	msgbox SootopolisCity_Text_ThankYouForHelpAcceptThis, MSGBOX_DEFAULT
	giveitem ITEM_HM_WATERFALL
	setflag FLAG_RECEIVED_HM_WATERFALL
	msgbox SootopolisCity_Text_ExplainWaterfallGoToGym, MSGBOX_DEFAULT
	closemessage
	call_if_eq VAR_FACING, DIR_NORTH, SootopolisCity_EventScript_WallaceMoveFromGym
	call_if_eq VAR_FACING, DIR_EAST, SootopolisCity_EventScript_WallaceMoveFromGym
	call_if_eq VAR_FACING, DIR_WEST, SootopolisCity_EventScript_WallaceMoveFromGymWest
	release
	end

SootopolisCity_EventScript_WallaceMoveFromGym::
	applymovement LOCALID_SOOTOPOLIS_WALLACE, SootopolisCity_Movement_WallaceMoveFromGym
	waitmovement 0
	copyobjectxytoperm LOCALID_SOOTOPOLIS_WALLACE
	setvar VAR_SOOTOPOLIS_WALLACE_STATE, 1
	return

SootopolisCity_EventScript_WallaceMoveFromGymWest::
	applymovement LOCALID_SOOTOPOLIS_WALLACE, SootopolisCity_Movement_WallaceMoveFromGymWest
	waitmovement 0
	copyobjectxytoperm LOCALID_SOOTOPOLIS_WALLACE
	setvar VAR_SOOTOPOLIS_WALLACE_STATE, 2
	return

SootopolisCity_EventScript_GoToSkyPillar::
	msgbox SootopolisCity_Text_HaventYouScaledSkyPillar, MSGBOX_DEFAULT
	release
	end

SootopolisCity_EventScript_GoToGym::
	msgbox SootopolisCity_Text_DazzledByMentor, MSGBOX_DEFAULT
	release
	end

SootopolisCity_Movement_WallaceMoveFromGym:
	walk_right
	walk_in_place_faster_down
	step_end

SootopolisCity_Movement_WallaceMoveFromGymWest:
	walk_left
	walk_in_place_faster_down
	step_end

SootopolisCity_EventScript_Maxie::
	lockall
	goto_if_eq VAR_SOOTOPOLIS_CITY_STATE, 5, SootopolisCity_EventScript_MaxieRayquaza
	msgbox SootopolisCity_Text_GroudonPleaseStop, MSGBOX_DEFAULT
	closemessage
	releaseall
	end

SootopolisCity_EventScript_MaxieRayquaza::
	msgbox SootopolisCity_Text_AfterAllOurScheming, MSGBOX_DEFAULT
	setflag FLAG_MET_MAXIE_SOOTOPOLIS
	goto_if_set FLAG_MET_ARCHIE_SOOTOPOLIS, SootopolisCity_EventScript_MaxieArchieLeave
	releaseall
	end

SootopolisCity_EventScript_Archie::
	lockall
	goto_if_eq VAR_SOOTOPOLIS_CITY_STATE, 5, SootopolisCity_EventScript_ArchieRayquaza
	msgbox SootopolisCity_Text_KyogreCalmDown, MSGBOX_DEFAULT
	closemessage
	releaseall
	end

SootopolisCity_EventScript_ArchieRayquaza::
	msgbox SootopolisCity_Text_TryingMeaninglessToPokemon, MSGBOX_DEFAULT
	setflag FLAG_MET_ARCHIE_SOOTOPOLIS
	goto_if_set FLAG_MET_MAXIE_SOOTOPOLIS, SootopolisCity_EventScript_MaxieArchieLeave
	releaseall
	end

SootopolisCity_EventScript_MaxieArchieLeave::
	setflag FLAG_HIDE_SOOTOPOLIS_CITY_MAXIE
	setflag FLAG_HIDE_SOOTOPOLIS_CITY_ARCHIE
	setflag FLAG_SOOTOPOLIS_ARCHIE_MAXIE_LEAVE
	clearflag FLAG_HIDE_MT_PYRE_SUMMIT_MAXIE
	clearflag FLAG_HIDE_MT_PYRE_SUMMIT_ARCHIE
	setvar VAR_MT_PYRE_STATE, 2
	warpsilent MAP_SOOTOPOLIS_CITY, 31, 34
	waitstate
	releaseall
	end

@ Unused
SootopolisCity_Movement_Levitate::
	levitate
	step_end

@ Unused
SootopolisCity_Movement_DestroyTask::
	destroy_extra_task
	step_end

SootopolisCity_Text_GymSign:
	.string "SOOTOPOLIS CITY POKéMON GYM\n"
	.string "LEADER: WALLACE\p"
	.string "“Sommelier, proprietor and connoisseur\n"
	.string "of fine vintages.\p"
	.string "”Full-bodied. Notes of oak, black\n"
	.string "cherry and a mildly enlarged liver.\p"
	.string "“Never drinks before noon. It is always\n"
	.string "noon somewhere.”$"

SootopolisCity_Text_CitySign:
	.string "SOOTOPOLIS CITY\p"
	.string "“The mystical city where history\n"
	.string "slumbers. Do not wake.”$"

SootopolisCity_Text_DoorIsClosed:
	.string "The door is closed. The gods are\n"
	.string "napping.$"

SootopolisCity_Text_PhysicallyFitLivingHere:
	.string "Diving in the sea. Stairs, stairs and\n"
	.string "more stairs…\p"
	.string "Live here and you get calves like Greek\n"
	.string "statues.$"

SootopolisCity_Text_GiantPokemonSuddenlyAppeared:
	.string "Giant POKéMON appeared in the middle of\n"
	.string "the city!\p"
	.string "Why are they fighting?!\p"
	.string "They're like the gods of the old\n"
	.string "stories!$"

SootopolisCity_Text_WhatIsThatGreenPokemon:
	.string "What? What? What? What is that green\n"
	.string "POKéMON?! A new god?!$"

SootopolisCity_Text_WhereDidLegendariesGo:
	.string "GROUDON and KYOGRE… Where did they go?\p"
	.string "Will they ruin someone else's weather\n"
	.string "now?$"

SootopolisCity_Text_TwoPokemonArentAngry:
	.string "I don't think they're angry.\p"
	.string "They just can't control their power.\p"
	.string "Like my uncle at weddings.$"

SootopolisCity_Text_FlyingMonStoppedRampage:
	.string "That flying POKéMON came down from the\n"
	.string "sky and told them to knock it off…$"

SootopolisCity_Text_WonderWhatWorldIsLike:
	.string "I've never been outside this city.\p"
	.string "What's the world like beyond this round\n"
	.string "sky? Do they have stairs?$"

SootopolisCity_Text_ThisIsWicked:
	.string "Two kaiju fighting! This is SO anime!$"

SootopolisCity_Text_ThatWasWicked:
	.string "Wow! That was wicked! Again! Again!$"

SootopolisCity_Text_GoRedAndBlueMon:
	.string "Go, red POKéMON! Don't back off, blue\n"
	.string "POKéMON!\p"
	.string "¥200 on red!$"

SootopolisCity_Text_DoYouKnowMonNames:
	.string "… … … … … …\p"
	.string "Do you know the names of those\n"
	.string "POKéMON?\p"
	.string "I want to know who to root for.$"

SootopolisCity_Text_GreenOneSettlesThings:
	.string "I bet on the red one. My brother bet on\n"
	.string "the blue one.\p"
	.string "Then the green one shows up and wins.\n"
	.string "Nobody bet on the green one!\p"
	.string "The bookie is the only winner here.$"

SootopolisCity_Text_SeeingLegendWithOwnEyes:
	.string "An ancient legend says land and sea\n"
	.string "were shaped by a battle of POKéMON!\p"
	.string "Like ZEUS versus POSEIDON!\p"
	.string "I'm seeing it with my own eyes! I need to\n"
	.string "write an epic poem!$"

SootopolisCity_Text_SawLegendWithOwnEyes:
	.string "The legend says a colossal battle\n"
	.string "between POKéMON shaped land and sea.\p"
	.string "Well, I saw it happen with my own eyes!\p"
	.string "Nobody's going to believe me. I didn't\n"
	.string "even film it.$"

SootopolisCity_Text_BigPokemonFighting:
	.string "Two huge POKéMON are fighting!\p"
	.string "Someone make them stop!\p"
	.string "WALLACE! Put down the wine and do\n"
	.string "something!$"

SootopolisCity_Text_PrettyMonCameFromSky:
	.string "A pretty POKéMON came down from the\n"
	.string "sky… Like ZEUS, but a noodle.$"

SootopolisCity_Text_SootopolisWillBeWrecked:
	.string "Oh, no! SOOTOPOLIS will get wrecked!\p"
	.string "We just renovated the temple!$"

SootopolisCity_Text_SootopolisDidntGetWrecked:
	.string "SOOTOPOLIS CITY didn't get wrecked!\n"
	.string "Praise the noodle!$"

SootopolisCity_Text_NoOrdinaryTourist:
	.string "Nothing beats a pita souvlaki after a\n"
	.string "long day of volcano living.$"

SootopolisCity_Text_CityRegainedCalm:
	.string "The city is calm again… Time for a nap.$"

SootopolisCity_Text_CaveOfOriginPleaseLeave:
	.string "Who might you be?\p"
	.string "This is the CAVE OF ORIGIN.\p"
	.string "The spirits of POKéMON resting at MT.\n"
	.string "PYRE are said to be revived here.\p"
	.string "Please leave. No tourists.$"

SootopolisCity_Text_LeadSuperiorTrainerToCave:
	.string "A person with a strong will and great\n"
	.string "talent…\p"
	.string "A TRAINER who knows many kinds of\n"
	.string "POKéMON…\p"
	.string "If such a person showed up, WALLACE\n"
	.string "told me to lead them into this CAVE.$"

SootopolisCity_Text_AwakenedPokemonClash:
	.string "Oh, my…\p"
	.string "The clash between two awakened\n"
	.string "POKéMON was ended by a third one…\p"
	.string "Like a parent breaking up a fight\n"
	.string "between siblings.$"

SootopolisCity_Text_CaveOfOriginSleepsToo:
	.string "This is the CAVE OF ORIGIN…\p"
	.string "The crisis is over. The cave sleeps\n"
	.string "again. Shh.$"

SootopolisCity_Text_SootopolisSkyBeautiful:
	.string "It's GYROS. YEE-ros. Not JAI-ros. Say it\n"
	.string "right or leave my city.$"

SootopolisCity_Text_GiganticPokemonFight:
	.string "When two POKéMON that huge fight like\n"
	.string "that, there's not much we can do.\p"
	.string "Except pray. And buy flood insurance.$"

SootopolisCity_Text_FearedWorstWhenPokemonFlewDown:
	.string "When that third POKéMON flew down, I\n"
	.string "thought: “Great, now there's three of\l"
	.string "them.”$"

SootopolisCity_Text_NightSkyFavoriteScenery:
	.string "A circle of night sky, framed by a\n"
	.string "volcano crater…\p"
	.string "The stars flicker as if they're alive…\n"
	.string "My favorite view.\p"
	.string "Also the only view. We live in a hole.$"

SootopolisCity_Text_WeatherWentWild:
	.string "It was sunny this morning…\p"
	.string "Then sheets of rain, thunder,\n"
	.string "lightning…\p"
	.string "The gods are angry. Or the POKéMON.\n"
	.string "Same thing here.$"

SootopolisCity_Text_YouBroughtFlyingMon:
	.string "Oh?\p"
	.string "You brought that flying POKéMON here?\p"
	.string "Well, aren't you something! Want to be a\n"
	.string "god? We have a vacancy.$"

SootopolisCity_Text_GroudonPleaseStop:
	.string "MAXIE: G… GROUDON… Please! Stop!\p"
	.string "I get it now! You're too hot! Even for\n"
	.string "me!\p"
	.string "If you keep going, all of HOENN will\n"
	.string "burn!$"

SootopolisCity_Text_AfterAllOurScheming:
	.string "MAXIE: So there was a third one…\p"
	.string "All our scheming, and one POKéMON fixes\n"
	.string "everything, just like that…\p"
	.string "Fu… Fuhahaha…\p"
	.string "Maybe I'll just sell salsa.$"

SootopolisCity_Text_KyogreCalmDown:
	.string "ARCHIE: KYOGRE! Look! The RED ORB! Calm\n"
	.string "down!\p"
	.string "… … … … … …\p"
	.string "It's not responding! It doesn't even\n"
	.string "like bubbles!$"

SootopolisCity_Text_TryingMeaninglessToPokemon:
	.string "ARCHIE: KYOGRE and GROUDON flew off.\p"
	.string "The weather is back to normal…\p"
	.string "Haha… Hahaha…\p"
	.string "Maybe I'll just sell tap water.$"

SootopolisCity_Text_InvolvedWithCrisisComeWithMe:
	.string "STEVEN: GROUDON… KYOGRE… Two ancient\n"
	.string "titans smashing each other! Greatest\l"
	.string "metal show on earth!\p"
	.string "…Also a crisis. {PLAYER}{KUN}, if you're here,\n"
	.string "you're in.\p"
	.string "There's someone I want you to meet.\n"
	.string "Come with me.$"

SootopolisCity_Text_DoesThisMakeYourFearPokemon:
	.string "STEVEN: Does this make you think\n"
	.string "POKéMON are scary? It's not true.\l"
	.string "POKéMON are more…\p"
	.string "…Why am I asking? You already know.\n"
	.string "METAL.$"

SootopolisCity_Text_HereWereAreHelpWallace:
	.string "STEVEN: Here we are! Inside is WALLACE.\n"
	.string "More of a wine guy than a metal guy.\p"
	.string "I think you have what's needed to help\n"
	.string "him…$"

SootopolisCity_Text_KnowWhatsNeededToHelpHim:
	.string "STEVEN: Go on in. He's probably drunk.$"

SootopolisCity_Text_NeverBeenToSkyPillar:
	.string "STEVEN: The SKY PILLAR… Never been\n"
	.string "there. Sounds like a good spot for a\l"
	.string "music video.$"

SootopolisCity_Text_SoThatsRayquaza:
	.string "STEVEN: So that's RAYQUAZA… It scared\n"
	.string "off both of them with one ROAR. Most\l"
	.string "METAL thing I've ever seen.$"

SootopolisCity_Text_MaxieArchieLeft:
	.string "STEVEN: MAXIE and ARCHIE are gone.\n"
	.string "Last I saw, they were sharing one\l"
	.string "bus ticket. And one sandwich.$"

SootopolisCity_Text_HaventYouScaledSkyPillar:
	.string "WALLACE: Oh? {PLAYER}{KUN}?\p"
	.string "You haven't climbed the SKY PILLAR\n"
	.string "yet?\p"
	.string "I'm sure you can make it to the top. Go!\n"
	.string "I'll keep the wine chilled.$"

SootopolisCity_Text_AquaMagmaDidntMeanHarm:
	.string "WALLACE: {PLAYER}{KUN}…\p"
	.string "The leaders of MAGMA and AQUA… I don't\n"
	.string "think they meant harm. They just\l"
	.string "wanted to sell things.\p"
	.string "It wouldn't hurt to hear their side.\n"
	.string "Over a drink, perhaps.$"

SootopolisCity_Text_ThankYouForHelpAcceptThis:
	.string "WALLACE: {PLAYER}{KUN}… My eyes didn't\n"
	.string "deceive me.\p"
	.string "Thanks to you, SOOTOPOLIS… No, all of\n"
	.string "HOENN was saved.\p"
	.string "On behalf of the people, I thank you.\p"
	.string "A gift from me. Please accept it. It\n"
	.string "pairs well with victory.$"

SootopolisCity_Text_ExplainWaterfallGoToGym:
	.string "WATERFALL. You go up waterfalls. You\n"
	.string "need the RAIN BADGE.\p"
	.string "It's a waterfall. Up.$"

SootopolisCity_Text_DazzledByMentor:
	.string "WALLACE: Come to my GYM whenever you\n"
	.string "like. I've uncorked something special\l"
	.string "for you.$"

@ ---------------------------------------------------------------- Project Grounded
@ Na Rayquaza: Archie en Maxie hebben geen spijt, ze zijn woedend. Keccles vliegt in op zijn Tropius
@ en vecht met je mee (multi battle). Daarna dropen ze af, zonder eer en zonder les.
SootopolisCity_EventScript_KecclesScene::
	lockall
	special StorePlayerCoordsInVars
	goto_if_ne VAR_0x8004, 31, SootopolisCity_EventScript_KecclesSceneReposition
	goto_if_ne VAR_0x8005, 35, SootopolisCity_EventScript_KecclesSceneReposition
	turnobject LOCALID_PLAYER, DIR_EAST
	turnobject LOCALID_SOOTOPOLIS_MAXIE, DIR_WEST
	turnobject LOCALID_SOOTOPOLIS_ARCHIE, DIR_WEST
	delay 30
	playbgm MUS_ENCOUNTER_MAGMA, FALSE
	applymovement LOCALID_SOOTOPOLIS_MAXIE, SootopolisCity_Movement_StompLeft
	applymovement LOCALID_SOOTOPOLIS_ARCHIE, SootopolisCity_Movement_StompLeft
	waitmovement 0
	msgbox SootopolisCity_Text_MaxieFurious, MSGBOX_DEFAULT
	msgbox SootopolisCity_Text_ArchieFurious, MSGBOX_DEFAULT
	msgbox SootopolisCity_Text_MaxieBlamesPlayer, MSGBOX_DEFAULT
	msgbox SootopolisCity_Text_ArchieBlamesPlayer, MSGBOX_DEFAULT
	closemessage
	@ Keccles komt aanvliegen op zijn Tropius
	clearflag FLAG_HIDE_SOOTOPOLIS_TROPIUS
	addobject LOCALID_SOOTOPOLIS_TROPIUS
	playse SE_M_FLY
	applymovement LOCALID_SOOTOPOLIS_TROPIUS, SootopolisCity_Movement_TropiusFlyIn
	waitmovement 0
	waitse
	clearflag FLAG_HIDE_SOOTOPOLIS_KECCLES
	addobject LOCALID_SOOTOPOLIS_KECCLES
	applymovement LOCALID_SOOTOPOLIS_KECCLES, SootopolisCity_Movement_KecclesHopOff
	waitmovement 0
	playse SE_BALL_OPEN
	removeobject LOCALID_SOOTOPOLIS_TROPIUS
	applymovement LOCALID_SOOTOPOLIS_KECCLES, SootopolisCity_Movement_KecclesJoinPlayer
	applymovement LOCALID_PLAYER, Common_Movement_WalkInPlaceFasterUp
	waitmovement 0
	msgbox SootopolisCity_Text_KecclesArrives, MSGBOX_DEFAULT
	closemessage
	applymovement LOCALID_SOOTOPOLIS_KECCLES, Common_Movement_WalkInPlaceFasterRight
	applymovement LOCALID_PLAYER, Common_Movement_WalkInPlaceFasterRight
	waitmovement 0
	msgbox SootopolisCity_Text_KecclesChanneledReptile, MSGBOX_DEFAULT
	playse SE_PIN
	applymovement LOCALID_SOOTOPOLIS_MAXIE, Common_Movement_ExclamationMark
	applymovement LOCALID_SOOTOPOLIS_ARCHIE, Common_Movement_ExclamationMark
	waitmovement 0
	msgbox SootopolisCity_Text_MaxieInsultsKeccles, MSGBOX_DEFAULT
	msgbox SootopolisCity_Text_ArchieInsultsKeccles, MSGBOX_DEFAULT
	msgbox SootopolisCity_Text_ArchieInsultsPlayer, MSGBOX_DEFAULT
	msgbox SootopolisCity_Text_MaxieInsultsPlayer, MSGBOX_DEFAULT
	msgbox SootopolisCity_Text_KecclesLetsBattle, MSGBOX_DEFAULT
	closemessage
SootopolisCity_EventScript_ChooseMonsForKecclesTag::
	special SavePlayerParty
	fadescreen FADE_TO_BLACK
	special ChooseHalfPartyForBattle
	waitstate
	goto_if_ne VAR_RESULT, 0, SootopolisCity_EventScript_DoKecclesTagBattle
	special LoadPlayerParty
	goto SootopolisCity_EventScript_ChooseMonsForKecclesTag

SootopolisCity_EventScript_DoKecclesTagBattle::
	multi_2_vs_2 TRAINER_MAXIE_SOOTOPOLIS, SootopolisCity_Text_MaxieDefeat, TRAINER_ARCHIE_SOOTOPOLIS, SootopolisCity_Text_ArchieDefeat, PARTNER_KECCLES
	switch VAR_RESULT
	case 1, SootopolisCity_EventScript_DefeatedArchieMaxieWithKeccles
	fadescreen FADE_TO_BLACK
	special SetCB2WhiteOut
	waitstate

SootopolisCity_EventScript_DefeatedArchieMaxieWithKeccles::
	msgbox SootopolisCity_Text_MaxiePathetic, MSGBOX_DEFAULT
	msgbox SootopolisCity_Text_ArchiePathetic, MSGBOX_DEFAULT
	closemessage
	applymovement LOCALID_SOOTOPOLIS_MAXIE, SootopolisCity_Movement_MaxieSlinkOff
	applymovement LOCALID_SOOTOPOLIS_ARCHIE, SootopolisCity_Movement_ArchieSlinkOff
	waitmovement 0
	msgbox SootopolisCity_Text_TheySlunkAway, MSGBOX_DEFAULT
	closemessage
	fadescreenswapbuffers FADE_TO_BLACK
	removeobject LOCALID_SOOTOPOLIS_MAXIE
	removeobject LOCALID_SOOTOPOLIS_ARCHIE
	fadescreenswapbuffers FADE_FROM_BLACK
	setflag FLAG_HIDE_SOOTOPOLIS_CITY_MAXIE
	setflag FLAG_HIDE_SOOTOPOLIS_CITY_ARCHIE
	setflag FLAG_SOOTOPOLIS_ARCHIE_MAXIE_LEAVE
	setflag FLAG_MET_MAXIE_SOOTOPOLIS
	setflag FLAG_MET_ARCHIE_SOOTOPOLIS
	@ geen berouwscène op Mt. Pyre: ze brengen de bollen niet terug
	delay 30
	applymovement LOCALID_SOOTOPOLIS_KECCLES, Common_Movement_WalkInPlaceFasterDown
	applymovement LOCALID_PLAYER, Common_Movement_WalkInPlaceFasterUp
	waitmovement 0
	msgbox SootopolisCity_Text_KecclesThanks, MSGBOX_DEFAULT
	closemessage
	@ Keccles vliegt weer weg op zijn Tropius
	playse SE_BALL_OPEN
	setobjectxyperm LOCALID_SOOTOPOLIS_TROPIUS, 32, 33
	clearflag FLAG_HIDE_SOOTOPOLIS_TROPIUS
	addobject LOCALID_SOOTOPOLIS_TROPIUS
	delay 20
	applymovement LOCALID_SOOTOPOLIS_KECCLES, SootopolisCity_Movement_KecclesHopOn
	waitmovement 0
	removeobject LOCALID_SOOTOPOLIS_KECCLES
	playse SE_M_FLY
	applymovement LOCALID_SOOTOPOLIS_TROPIUS, SootopolisCity_Movement_TropiusFlyAway
	waitmovement 0
	removeobject LOCALID_SOOTOPOLIS_TROPIUS
	setflag FLAG_HIDE_SOOTOPOLIS_KECCLES
	setflag FLAG_HIDE_SOOTOPOLIS_TROPIUS
	setvar VAR_SOOTOPOLIS_KECCLES_STATE, 2
	fadedefaultbgm
	releaseall
	end

@ Na een verloren gevecht (of na Rayquaza van elders): eerst netjes op de plek zetten
SootopolisCity_EventScript_KecclesSceneReposition::
	warpsilent MAP_SOOTOPOLIS_CITY, 31, 35
	waitstate
	releaseall
	end

SootopolisCity_Movement_StompLeft:
	walk_in_place_faster_left
	walk_in_place_faster_left
	step_end

SootopolisCity_Movement_TropiusFlyIn:
	walk_faster_down
	walk_faster_down
	walk_faster_down
	walk_faster_down
	walk_faster_down
	walk_faster_down
	walk_in_place_faster_down
	step_end

SootopolisCity_Movement_KecclesHopOff:
	jump_in_place_down
	step_end

SootopolisCity_Movement_KecclesJoinPlayer:
	walk_left
	walk_in_place_faster_down
	step_end

SootopolisCity_Movement_KecclesHopOn:
	walk_right
	jump_in_place_up
	step_end

SootopolisCity_Movement_TropiusFlyAway:
	walk_faster_up
	walk_faster_up
	walk_faster_up
	walk_faster_up
	walk_faster_up
	walk_faster_up
	walk_faster_up
	walk_faster_up
	step_end

SootopolisCity_Movement_MaxieSlinkOff:
	face_right
	delay_16
	walk_slow_up
	step_end

SootopolisCity_Movement_ArchieSlinkOff:
	face_right
	delay_16
	walk_slow_down
	step_end

SootopolisCity_Text_TheySlunkAway:
	.string "MAXIE and ARCHIE shuffle off,\n"
	.string "arguing about who pays for the bus.$"

SootopolisCity_Text_MaxieFurious:
	.string "MAXIE: …Do you know what that\n"
	.string "dragon just did?\p"
	.string "It calmed GROUDON. Calmed it!\n"
	.string "Like a scented candle!\p"
	.string "There goes my volcano-roasted salsa\n"
	.string "empire. Fifteen years of planning.\l"
	.string "The jars were already printed!$"

SootopolisCity_Text_ArchieFurious:
	.string "ARCHIE: Jars?! I had a FLEET of\n"
	.string "bottling ships waiting offshore!\p"
	.string "PRIMORDIAL SEA WATER, premium!\n"
	.string "Now it's just… sea. Regular sea.\l"
	.string "You can't sell regular sea!$"

SootopolisCity_Text_MaxieBlamesPlayer:
	.string "MAXIE: And who climbed that pillar\n"
	.string "and rang the big green doorbell?\p"
	.string "YOU. {PLAYER}. The intern of\n"
	.string "the apocalypse.$"

SootopolisCity_Text_ArchieBlamesPlayer:
	.string "ARCHIE: Nobody asked you to call\n"
	.string "a sky noodle!\p"
	.string "We're going to sue you. And then\n"
	.string "we're going to beat you up.\l"
	.string "Not necessarily in that order!$"

SootopolisCity_Text_KecclesArrives:
	.string "KECCLES: Hello, {PLAYER}.\n"
	.string "Sorry I'm late. I was flying\l"
	.string "in camouflage. Over the sea.\p"
	.string "I matched the water so well\n"
	.string "I nearly lost myself.$"

SootopolisCity_Text_KecclesChanneledReptile:
	.string "KECCLES: Gentlemen. Allow me\n"
	.string "to confess something.\p"
	.string "I sat on my rock and watched\n"
	.string "the rain drown the fields and the\l"
	.string "sun scorch the reefs.\p"
	.string "And I asked myself: what is a\n"
	.string "chameleon, if not a creature that\l"
	.string "becomes whatever surrounds it?\p"
	.string "But I could not become this.\n"
	.string "The suffering of the POKéMON\l"
	.string "was too loud.\p"
	.string "So I meditated. Three days.\n"
	.string "No food. Some snacks.\p"
	.string "And I channeled the ultimate\n"
	.string "green reptile.\p"
	.string "You are welcome, Hoenn.$"

SootopolisCity_Text_MaxieInsultsKeccles:
	.string "MAXIE: YOU summoned RAYQUAZA?\n"
	.string "You're a lizard that forgot\l"
	.string "which colour it was supposed to be!$"

SootopolisCity_Text_ArchieInsultsKeccles:
	.string "ARCHIE: A discount handbag\n"
	.string "with a philosophy degree!\p"
	.string "I've seen more spine in\n"
	.string "a jellyfish buffet!$"

SootopolisCity_Text_ArchieInsultsPlayer:
	.string "ARCHIE: And YOU, {PLAYER}!\n"
	.string "You've got the charisma of a\l"
	.string "wet REPEL and the haircut to\l"
	.string "match!$"

SootopolisCity_Text_MaxieInsultsPlayer:
	.string "MAXIE: A walking participation\n"
	.string "trophy. A loading screen\l"
	.string "with legs.\p"
	.string "ARCHIE! Truce. Just this once.\n"
	.string "Let's flatten these two!$"

SootopolisCity_Text_KecclesLetsBattle:
	.string "KECCLES: Anger is just fear\n"
	.string "wearing a bigger coat.\p"
	.string "{PLAYER}, shall we take their\n"
	.string "coats off?$"

SootopolisCity_Text_MaxieDefeat:
	.string "MAXIE: This is the worst business\n"
	.string "quarter of my life.$"

SootopolisCity_Text_ArchieDefeat:
	.string "ARCHIE: My ships… my bottles…\n"
	.string "my sea…$"

SootopolisCity_Text_MaxiePathetic:
	.string "MAXIE: This isn't over. It's…\n"
	.string "paused. Strategically.\p"
	.string "I'm going to go home and lie\n"
	.string "face down on the carpet.$"

SootopolisCity_Text_ArchiePathetic:
	.string "ARCHIE: Yeah, well… you smell!\n"
	.string "Both of you!\p"
	.string "MAXIE, can you lend me bus fare?\n"
	.string "My ships got repossessed.$"

SootopolisCity_Text_KecclesThanks:
	.string "KECCLES: Thank you, {PLAYER}.\n"
	.string "Truly.\p"
	.string "I set out to find the meaning of\n"
	.string "life. I have not found it.\l"
	.string "I suspect I never will.\p"
	.string "But I have found two smaller\n"
	.string "things: health and happiness.\l"
	.string "Those will be my goals now.\p"
	.string "The POKéMON LEAGUE? No. That\n"
	.string "mountain is yours to climb.\p"
	.string "I only want to keep growing\n"
	.string "stronger. Quietly. In disguise.\p"
	.string "Although… I hear rumours of a\n"
	.string "place across the sea. A frontier\l"
	.string "built for battle.\p"
	.string "Rules that bend, formats that\n"
	.string "twist… A strategist could really\l"
	.string "go wild there.\p"
	.string "Perhaps we will meet again,\n"
	.string "{PLAYER}. You may not see me.\l"
	.string "But I will be there.$"
