Route111_MapScripts::
	map_script MAP_SCRIPT_ON_LOAD, Route111_OnLoad
	map_script MAP_SCRIPT_ON_TRANSITION, Route111_OnTransition
	map_script MAP_SCRIPT_ON_WARP_INTO_MAP_TABLE, Route111_OnWarp
	map_script MAP_SCRIPT_ON_FRAME_TABLE, Route111_OnFrame
	.byte 0

Route111_OnLoad:
	call_if_unset FLAG_REGI_DOORS_OPENED, Route111_EventScript_CloseDesertRuins
	call_if_eq VAR_MIRAGE_TOWER_STATE, 1, Route111_EventScript_ShowTemporaryMirageTower
	end

Route111_EventScript_CloseDesertRuins::
	setmetatile 29, 86, METATILE_General_RockWall_RockBase, TRUE
	setmetatile 29, 87, METATILE_General_RockWall_SandBase, TRUE
	return

@ Show Mirage Tower just prior to disintegration. Mirage Tower is otherwise handled by the map layout
Route111_EventScript_ShowTemporaryMirageTower::
	setmetatile 18, 53, METATILE_Mauville_MirageTower_Tile0, FALSE
	setmetatile 19, 53, METATILE_Mauville_MirageTower_Tile1, FALSE
	setmetatile 20, 53, METATILE_Mauville_MirageTower_Tile2, FALSE
	setmetatile 18, 54, METATILE_Mauville_MirageTower_Tile3, FALSE
	setmetatile 19, 54, METATILE_Mauville_MirageTower_Tile4, FALSE
	setmetatile 20, 54, METATILE_Mauville_MirageTower_Tile5, FALSE
	setmetatile 18, 55, METATILE_Mauville_MirageTower_Tile6, FALSE
	setmetatile 19, 55, METATILE_Mauville_MirageTower_Tile7, FALSE
	setmetatile 20, 55, METATILE_Mauville_MirageTower_Tile8, FALSE
	setmetatile 18, 56, METATILE_Mauville_MirageTower_Tile9, FALSE
	setmetatile 19, 56, METATILE_Mauville_MirageTower_TileA, FALSE
	setmetatile 20, 56, METATILE_Mauville_MirageTower_TileB, FALSE
	setmetatile 18, 57, METATILE_Mauville_MirageTower_TileC, FALSE
	setmetatile 19, 57, METATILE_Mauville_MirageTower_TileD, FALSE
	setmetatile 20, 57, METATILE_Mauville_MirageTower_TileE, FALSE
	setmetatile 18, 58, METATILE_Mauville_MirageTower_TileF, FALSE
	setmetatile 19, 58, METATILE_Mauville_MirageTower_Tile10, FALSE
	setmetatile 20, 58, METATILE_Mauville_MirageTower_Tile11, FALSE
	return

Route111_OnTransition:
	call Route111_EventScript_Legends2_GalarTransition
	setvar VAR_TRAINER_HILL_IS_ACTIVE, 0
	special SetMirageTowerVisibility
	call_if_unset FLAG_MIRAGE_TOWER_VISIBLE, Route111_EventScript_SetLayoutNoMirageTower
	call_if_eq VAR_MIRAGE_TOWER_STATE, 1, Route111_EventScript_SetFallingPlayerGfx
	call_if_eq VAR_MIRAGE_TOWER_STATE, 2, Route111_EventScript_SetMirageTowerGone
	call Route111_EventScript_CheckSetSandstorm
	call Route111_EventScript_UpdateHoopaRing
	call GabbyAndTy_EventScript_UpdateLocation
	setflag FLAG_TEMP_14 @ Project Grounded: Joey verschijnt alleen in de Gabby & Ty-scène
	goto_if_not_defeated TRAINER_VICKY, Route111_EventScript_SetWinstratesNotDefeated
	end

Route111_EventScript_SetFallingPlayerGfx::
	checkplayergender
	goto_if_eq VAR_RESULT, MALE, Route111_EventScript_SetFallingPlayerGfxMale
	goto_if_eq VAR_RESULT, FEMALE, Route111_EventScript_SetFallingPlayerGfxFemale
	return

Route111_EventScript_SetFallingPlayerGfxMale::
	setvar VAR_OBJ_GFX_ID_0, OBJ_EVENT_GFX_RIVAL_BRENDAN_NORMAL
	return

Route111_EventScript_SetFallingPlayerGfxFemale::
	setvar VAR_OBJ_GFX_ID_0, OBJ_EVENT_GFX_RIVAL_MAY_NORMAL
	return

Route111_EventScript_CheckSetSandstorm::
	getplayerxy VAR_TEMP_0, VAR_TEMP_1
	goto_if_lt VAR_TEMP_1, 34, Route111_EventScript_EndCheckSetSandstorm
	goto_if_gt VAR_TEMP_1, 107, Route111_EventScript_EndCheckSetSandstorm
	goto_if_gt VAR_TEMP_1, 72, Route111_EventScript_SetSandstorm
	goto_if_gt VAR_TEMP_0, 2000, Route111_EventScript_EndCheckSetSandstorm
	goto_if_lt VAR_TEMP_0, 8, Route111_EventScript_EndCheckSetSandstorm
Route111_EventScript_SetSandstorm::
	setweather WEATHER_SANDSTORM
Route111_EventScript_EndCheckSetSandstorm::
	return

Route111_EventScript_SetWinstratesNotDefeated::
	clearflag FLAG_HIDE_ROUTE_111_VICTOR_WINSTRATE
	setflag FLAG_HIDE_ROUTE_111_VICTORIA_WINSTRATE
	setflag FLAG_HIDE_ROUTE_111_VIVI_WINSTRATE
	setflag FLAG_HIDE_ROUTE_111_VICKY_WINSTRATE
	cleartrainerflag TRAINER_VICTOR
	cleartrainerflag TRAINER_VICTORIA
	cleartrainerflag TRAINER_VIVI
	end

Route111_EventScript_SetLayoutNoMirageTower::
	setmaplayoutindex LAYOUT_ROUTE111_NO_MIRAGE_TOWER
	return

Route111_EventScript_SetMirageTowerGone::
	setvar VAR_MIRAGE_TOWER_STATE, 3
	return

Route111_OnWarp:
	map_script_2 VAR_MIRAGE_TOWER_STATE, 1, Route111_EventScript_HidePlayerForMirageTower
	.2byte 0

Route111_EventScript_HidePlayerForMirageTower::
	hideobjectat LOCALID_PLAYER, MAP_LITTLEROOT_TOWN
	end

Route111_OnFrame:
	map_script_2 VAR_MIRAGE_TOWER_STATE, 1, Route111_EventScript_MirageTowerDisappear
	.2byte 0

Route111_EventScript_MirageTowerDisappear::
	lockall
	special StartMirageTowerShake
	waitstate
	delay 24
	playse SE_FALL
	addobject LOCALID_ROUTE111_PLAYER_FALLING
	special StartPlayerDescendMirageTower
	waitstate
	showobjectat LOCALID_PLAYER, MAP_LITTLEROOT_TOWN
	removeobject LOCALID_ROUTE111_PLAYER_FALLING
	delay 16
	turnobject LOCALID_PLAYER, DIR_NORTH
	delay 16
	special StartMirageTowerDisintegration
	waitstate
	special StartMirageTowerFossilFallAndSink
	waitstate
	setvar VAR_MIRAGE_TOWER_STATE, 2
	clearflag FLAG_HIDE_DESERT_UNDERPASS_FOSSIL
	goto_if_set FLAG_CHOSE_CLAW_FOSSIL, Route111_EventScript_RootFossilDisappeared
	msgbox Route111_Text_ClawFossilDisappeared, MSGBOX_DEFAULT
	releaseall
	end

Route111_EventScript_RootFossilDisappeared::
	msgbox Route111_Text_RootFossilDisappeared, MSGBOX_DEFAULT
	releaseall
	end

@ Unused
Route111_Movement_PlayerFall::
	lock_anim
	walk_fast_down
	walk_fast_down
	walk_fast_down
	walk_fast_down
	walk_fast_down
	walk_fast_down
	step_end

Route111_EventScript_Girl::
	lock
	faceplayer
	dotimebasedevents
	goto_if_set FLAG_DAILY_ROUTE_111_RECEIVED_BERRY, Route111_EventScript_ReceivedBerry
	msgbox Route111_Text_WateredPlantsEveryDayTakeBerry, MSGBOX_DEFAULT
	giveitem ITEM_RAZZ_BERRY
	goto_if_eq VAR_RESULT, FALSE, Common_EventScript_ShowBagIsFull
	setflag FLAG_DAILY_ROUTE_111_RECEIVED_BERRY
	special GetPlayerBigGuyGirlString
	msgbox Route111_Text_GoingToTryToMakeDifferentColorBerries, MSGBOX_DEFAULT
	release
	end

Route111_EventScript_ReceivedBerry::
	msgbox Route111_Text_WhatColorBerriesToLookForToday, MSGBOX_DEFAULT
	release
	end

@ Unused
Route111_EventScript_ViciousSandstormTriggerUp::
	lockall
	setvar VAR_0x8004, 0
	goto Route111_EventScript_ViciousSandstormTrigger
	end

Route111_EventScript_ViciousSandstormTriggerDown::
	lockall
	setvar VAR_0x8004, 1
	goto Route111_EventScript_ViciousSandstormTrigger
	end

Route111_EventScript_ViciousSandstormTriggerLeft::
	lockall
	setvar VAR_0x8004, 2
	goto Route111_EventScript_ViciousSandstormTrigger
	end

@ Unused
Route111_EventScript_ViciousSandstormTriggerRight::
	lockall
	setvar VAR_0x8004, 3
	goto Route111_EventScript_ViciousSandstormTrigger
	end

Route111_EventScript_ViciousSandstormTrigger::
	checkitem ITEM_GO_GOGGLES
	goto_if_eq VAR_RESULT, FALSE, Route111_EventScript_PreventRouteAccess
	setvar VAR_TEMP_3, 1
	releaseall
	end

Route111_EventScript_PreventRouteAccess::
	msgbox gText_SandstormIsVicious, MSGBOX_DEFAULT
	closemessage
	call_if_eq VAR_0x8004, 0, Route111_EventScript_PushUpFromRoute
	call_if_eq VAR_0x8004, 1, Route111_EventScript_PushDownFromRoute
	call_if_eq VAR_0x8004, 2, Route111_EventScript_PushLeftFromRoute
	call_if_eq VAR_0x8004, 3, Route111_EventScript_PushRightFromRoute
	releaseall
	end

Route111_EventScript_PushUpFromRoute::
	applymovement LOCALID_PLAYER, Route111_Movement_PushUpFromRoute
	waitmovement 0
	return

Route111_EventScript_PushDownFromRoute::
	applymovement LOCALID_PLAYER, Route111_Movement_PushDownFromRoute
	waitmovement 0
	return

Route111_EventScript_PushLeftFromRoute::
	applymovement LOCALID_PLAYER, Route111_Movement_PushLeftFromRoute
	waitmovement 0
	return

Route111_EventScript_PushRightFromRoute::
	applymovement LOCALID_PLAYER, Route111_Movement_PushRightFromRoute
	waitmovement 0
	return

Route111_Movement_PushUpFromRoute:
	walk_up
	step_end

Route111_Movement_PushDownFromRoute:
	walk_down
	step_end

Route111_Movement_PushLeftFromRoute:
	walk_left
	step_end

Route111_Movement_PushRightFromRoute:
	walk_right
	step_end

Route111_EventScript_SunTrigger::
	setweather WEATHER_SUNNY
	fadenewbgm MUS_ROUTE110
	doweather
	setvar VAR_TEMP_3, 0
	end

Route111_EventScript_SandstormTrigger::
	setweather WEATHER_SANDSTORM
	fadenewbgm MUS_DESERT
	doweather
	end

Route111_EventScript_Victor::
	lock
	faceplayer
	setflag FLAG_LANDMARK_WINSTRATE_FAMILY
	msgbox Route111_Text_BattleOurFamily, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, YES, Route111_EventScript_BattleWinstrates
	msgbox Route111_Text_IsThatSo, MSGBOX_DEFAULT
	release
	end

Route111_EventScript_BattleWinstrates::
	msgbox Route111_Text_VictorIntro, MSGBOX_DEFAULT
	trainerbattle_no_intro TRAINER_VICTOR, Route111_Text_VictorDefeat
	applymovement LOCALID_ROUTE111_VICTOR, Common_Movement_WalkInPlaceFasterUp
	waitmovement 0
	call Route111_EventScript_OpenWinstrateDoor
	msgbox Route111_Text_VictorPostBattle, MSGBOX_DEFAULT
	closemessage
	applymovement LOCALID_ROUTE111_VICTOR, Route111_Movement_WinstrateEnterHouse
	waitmovement 0
	removeobject LOCALID_ROUTE111_VICTOR
	call Route111_EventScript_CloseWinstrateDoor
	applymovement LOCALID_PLAYER, Route111_Movement_WaitForNextWinstrate
	waitmovement 0
	call Route111_EventScript_OpenWinstrateDoor
	addobject LOCALID_ROUTE111_VICTORIA
	applymovement LOCALID_ROUTE111_VICTORIA, Route111_Movement_WinstrateExitHouse
	waitmovement 0
	call Route111_EventScript_CloseWinstrateDoor
	msgbox Route111_Text_VictoriaIntro, MSGBOX_DEFAULT
	trainerbattle_no_intro TRAINER_VICTORIA, Route111_Text_VictoriaDefeat
	applymovement LOCALID_ROUTE111_VICTORIA, Common_Movement_WalkInPlaceFasterUp
	waitmovement 0
	call Route111_EventScript_OpenWinstrateDoor
	msgbox Route111_Text_VictoriaPostBattle, MSGBOX_DEFAULT
	closemessage
	applymovement LOCALID_ROUTE111_VICTORIA, Route111_Movement_WinstrateEnterHouse
	waitmovement 0
	removeobject LOCALID_ROUTE111_VICTORIA
	call Route111_EventScript_CloseWinstrateDoor
	applymovement LOCALID_PLAYER, Route111_Movement_WaitForNextWinstrate
	waitmovement 0
	call Route111_EventScript_OpenWinstrateDoor
	addobject LOCALID_ROUTE111_VIVI
	applymovement LOCALID_ROUTE111_VIVI, Route111_Movement_WinstrateExitHouse
	waitmovement 0
	call Route111_EventScript_CloseWinstrateDoor
	msgbox Route111_Text_ViviIntro, MSGBOX_DEFAULT
	trainerbattle_no_intro TRAINER_VIVI, Route111_Text_ViviDefeat
	applymovement LOCALID_ROUTE111_VIVI, Common_Movement_WalkInPlaceFasterUp
	waitmovement 0
	call Route111_EventScript_OpenWinstrateDoor
	msgbox Route111_Text_ViviPostBattle, MSGBOX_DEFAULT
	closemessage
	applymovement LOCALID_ROUTE111_VIVI, Route111_Movement_WinstrateEnterHouse
	waitmovement 0
	removeobject LOCALID_ROUTE111_VIVI
	call Route111_EventScript_CloseWinstrateDoor
	applymovement LOCALID_PLAYER, Route111_Movement_WaitForNextWinstrate
	waitmovement 0
	call Route111_EventScript_OpenWinstrateDoor
	addobject LOCALID_ROUTE111_VICKY
	applymovement LOCALID_ROUTE111_VICKY, Route111_Movement_WinstrateExitHouse
	waitmovement 0
	call Route111_EventScript_CloseWinstrateDoor
	msgbox Route111_Text_VickyIntro, MSGBOX_DEFAULT
	trainerbattle_no_intro TRAINER_VICKY, Route111_Text_VickyDefeat
	msgbox Route111_Text_VickyPostBattle, MSGBOX_DEFAULT
	closemessage
	applymovement LOCALID_ROUTE111_VICKY, Common_Movement_WalkInPlaceFasterUp
	waitmovement 0
	call Route111_EventScript_OpenWinstrateDoor
	applymovement LOCALID_ROUTE111_VICKY, Route111_Movement_WinstrateEnterHouse
	waitmovement 0
	removeobject LOCALID_ROUTE111_VICKY
	call Route111_EventScript_CloseWinstrateDoor
	release
	end

Route111_EventScript_OpenWinstrateDoor::
	opendoor 13, 113
	waitdooranim
	return

Route111_EventScript_CloseWinstrateDoor::
	closedoor 13, 113
	waitdooranim
	return

Route111_Movement_WinstrateEnterHouse:
	walk_in_place_faster_up
	walk_up
	step_end

Route111_Movement_WinstrateExitHouse:
	walk_down
	step_end

Route111_Movement_WaitForNextWinstrate:
	delay_16
	delay_16
	delay_16
	step_end

Route111_EventScript_RouteSignMauville::
	msgbox Route111_Text_RouteSignMauville, MSGBOX_SIGN
	end

Route111_EventScript_WinstrateHouseSign::
	msgbox Route111_Text_WinstrateHouseSign, MSGBOX_SIGN
	end

Route111_EventScript_RouteSign112::
	msgbox Route111_Text_RouteSign112, MSGBOX_SIGN
	end

Route111_EventScript_RouteSign113::
	msgbox Route111_Text_RouteSign113, MSGBOX_SIGN
	end

Route111_EventScript_OldLadysRestStopSign::
	msgbox Route111_Text_OldLadysRestStopSign, MSGBOX_SIGN
	end

Route111_EventScript_TrainerTipsSpAtkSpDef::
	msgbox Route111_Text_TrainerTipsSpAtkSpDef, MSGBOX_SIGN
	end

Route111_EventScript_Man1::
	msgbox Route111_Text_ToughToKeepWinningUpTheRanks, MSGBOX_NPC
	end

Route111_EventScript_Man2::
	msgbox Route111_Text_WinstrateFamilyDestroyedMe, MSGBOX_NPC
	end

Route111_EventScript_Hiker::
	lock
	faceplayer
	goto_if_eq VAR_MIRAGE_TOWER_STATE, 3, Route111_EventScript_HikerMirageTowerGone
	goto_if_eq VAR_MIRAGE_TOWER_STATE, 2, Route111_EventScript_HikerMirageTowerDisintegrated
	goto_if_set FLAG_MIRAGE_TOWER_VISIBLE, Route111_EventScript_HikerMirageTowerVisible
	msgbox Route111_Text_ShouldBeMirageTowerAroundHere, MSGBOX_DEFAULT
	release
	end

Route111_EventScript_HikerMirageTowerGone::
	msgbox Route111_Text_MirageTowerHasntBeenSeenSince, MSGBOX_DEFAULT
	release
	end

Route111_EventScript_HikerMirageTowerDisintegrated::
	msgbox Route111_Text_ThatWasShockingSandRainedDown, MSGBOX_DEFAULT
	release
	end

Route111_EventScript_HikerMirageTowerVisible::
	msgbox Route111_Text_MirageTowerClearlyVisible, MSGBOX_DEFAULT
	release
	end

Route111_EventScript_RockSmashTipFatMan::
	lockall
	applymovement LOCALID_ROUTE111_ROCK_SMASH_MAN, Common_Movement_FacePlayer
	waitmovement 0
	call_if_ge VAR_HEATRAN_CUTSCENE_STATE, 1, Route111_EventScript_RockSmashManAfterHeatran
	call_if_eq VAR_HEATRAN_CUTSCENE_STATE, 0, Route111_EventScript_RockSmashManTip
	closemessage
	applymovement LOCALID_ROUTE111_ROCK_SMASH_MAN, Common_Movement_FaceOriginalDirection
	waitmovement 0
	@ Project Grounded (Jordi): na zijn dialoog komt Heatran de stenen wegbeuken (vanaf de 3e badge, eenmalig)
	goto_if_unset FLAG_BADGE03_GET, Route111_EventScript_RockSmashManEnd
	goto_if_eq VAR_HEATRAN_CUTSCENE_STATE, 0, Route111_EventScript_HeatranScene
Route111_EventScript_RockSmashManEnd::
	releaseall
	end

Route111_EventScript_RockSmashManTip::
	msgbox Route111_Text_MauvilleUncleToldMeToTakeRockSmash, MSGBOX_DEFAULT
	return

Route111_EventScript_RockSmashManAfterHeatran::
	msgbox Route111_Text_RockSmashManAfterHeatran, MSGBOX_DEFAULT
	return

Route111_Text_RockSmashManAfterHeatran:
	.string "Unbelievable. UNBELIEVABLE!\p"
	.string "I gave you that HM for NOTHING!\n"
	.string "Do you know what I had to do for it?\p"
	.string "…What do you mean, I never gave you\n"
	.string "anything? I gave you EMOTIONAL\l"
	.string "SUPPORT. That's worth more than a HM.$"

Route111_EventScript_Drew::
	trainerbattle_single TRAINER_DREW, Route111_Text_DrewIntro, Route111_Text_DrewDefeat
	msgbox Route111_Text_DrewPostBattle, MSGBOX_AUTOCLOSE
	end

Route111_EventScript_Heidi::
	trainerbattle_single TRAINER_HEIDI, Route111_Text_HeidiIntro, Route111_Text_HeidiDefeat
	msgbox Route111_Text_HeidiPostBattle, MSGBOX_AUTOCLOSE
	end

Route111_EventScript_Beau::
	trainerbattle_single TRAINER_BEAU, Route111_Text_BeauIntro, Route111_Text_BeauDefeat
	msgbox Route111_Text_BeauPostBattle, MSGBOX_AUTOCLOSE
	end

Route111_EventScript_Becky::
	trainerbattle_single TRAINER_BECKY, Route111_Text_BeckyIntro, Route111_Text_BeckyDefeat
	msgbox Route111_Text_BeckyPostBattle, MSGBOX_AUTOCLOSE
	end

Route111_EventScript_Dusty::
	trainerbattle_single TRAINER_DUSTY_1, Route111_Text_DustyIntro, Route111_Text_DustyDefeat, Route111_EventScript_RegisterDusty
	specialvar VAR_RESULT, ShouldTryRematchBattle
	goto_if_eq VAR_RESULT, TRUE, Route111_EventScript_RematchDusty
	msgbox Route111_Text_DustyPostBattle, MSGBOX_DEFAULT
	release
	end

Route111_EventScript_RegisterDusty::
	special PlayerFaceTrainerAfterBattle
	waitmovement 0
	msgbox Route111_Text_DustyRegister, MSGBOX_DEFAULT
	register_matchcall TRAINER_DUSTY_1
	release
	end

Route111_EventScript_RematchDusty::
	trainerbattle_rematch TRAINER_DUSTY_1, Route111_Text_DustyRematchIntro, Route111_Text_DustyRematchDefeat
	msgbox Route111_Text_DustyPostRematch, MSGBOX_AUTOCLOSE
	end

Route111_EventScript_Travis::
	trainerbattle_single TRAINER_TRAVIS, Route111_Text_TravisIntro, Route111_Text_TravisDefeat
	msgbox Route111_Text_TravisPostBattle, MSGBOX_AUTOCLOSE
	end

Route111_EventScript_Irene::
	trainerbattle_single TRAINER_IRENE, Route111_Text_IreneIntro, Route111_Text_IreneDefeat
	msgbox Route111_Text_IrenePostBattle, MSGBOX_AUTOCLOSE
	end

Route111_EventScript_Daisuke::
	trainerbattle_single TRAINER_DAISUKE, Route111_Text_DaisukeIntro, Route111_Text_DaisukeDefeat
	msgbox Route111_Text_DaisukePostBattle, MSGBOX_AUTOCLOSE
	end

Route111_EventScript_Charles::
	trainerbattle_single TRAINER_CHARLES_1, Route111_Text_WiltonIntro, Route111_Text_WiltonDefeat, Route111_EventScript_RegisterCharles
	specialvar VAR_RESULT, ShouldTryRematchBattle
	goto_if_eq VAR_RESULT, TRUE, Route111_EventScript_RematchCharles
	msgbox Route111_Text_WiltonPostBattle, MSGBOX_DEFAULT
	release
	end

Route111_EventScript_RegisterCharles::
	special PlayerFaceTrainerAfterBattle
	waitmovement 0
	msgbox Route111_Text_WiltonRegister, MSGBOX_DEFAULT
	register_matchcall TRAINER_CHARLES_1
	release
	end

Route111_EventScript_RematchCharles::
	trainerbattle_rematch TRAINER_CHARLES_1, Route111_Text_WiltonRematchIntro, Route111_Text_WiltonRematchDefeat
	msgbox Route111_Text_WiltonPostRematch, MSGBOX_AUTOCLOSE
	end

Route111_EventScript_Brooke::
	trainerbattle_single TRAINER_BROOKE_1, Route111_Text_BrookeIntro, Route111_Text_BrookeDefeat, Route111_EventScript_RegisterBrooke
	specialvar VAR_RESULT, ShouldTryRematchBattle
	goto_if_eq VAR_RESULT, TRUE, Route111_EventScript_RematchBrooke
	msgbox Route111_Text_BrookePostBattle, MSGBOX_DEFAULT
	release
	end

Route111_EventScript_RegisterBrooke::
	special PlayerFaceTrainerAfterBattle
	waitmovement 0
	msgbox Route111_Text_BrookeRegister, MSGBOX_DEFAULT
	register_matchcall TRAINER_BROOKE_1
	release
	end

Route111_EventScript_RematchBrooke::
	trainerbattle_rematch TRAINER_BROOKE_1, Route111_Text_BrookeRematchIntro, Route111_Text_BrookeRematchDefeat
	msgbox Route111_Text_BrookePostRematch, MSGBOX_AUTOCLOSE
	end

Route111_EventScript_Hayden::
	trainerbattle_single TRAINER_HAYDEN, Route111_Text_HaydenIntro, Route111_Text_HaydenDefeat
	msgbox Route111_Text_HaydenPostBattle, MSGBOX_AUTOCLOSE
	end

Route111_EventScript_Bianca::
	trainerbattle_single TRAINER_BIANCA, Route111_Text_BiancaIntro, Route111_Text_BiancaDefeat
	msgbox Route111_Text_BiancaPostBattle, MSGBOX_AUTOCLOSE
	end

Route111_EventScript_Tyron::
	trainerbattle_single TRAINER_TYRON, Route111_Text_TyronIntro, Route111_Text_TyronDefeat
	msgbox Route111_Text_TyronPostBattle, MSGBOX_AUTOCLOSE
	end

Route111_EventScript_Celina::
	trainerbattle_single TRAINER_CELINA, Route111_Text_CelinaIntro, Route111_Text_CelinaDefeat
	msgbox Route111_Text_CelinaPostBattle, MSGBOX_AUTOCLOSE
	end

Route111_EventScript_Celia::
	trainerbattle_single TRAINER_CELIA, Route111_Text_CeliaIntro, Route111_Text_CeliaDefeat
	msgbox Route111_Text_CeliaPostBattle, MSGBOX_AUTOCLOSE
	end

Route111_EventScript_Bryan::
	trainerbattle_single TRAINER_BRYAN, Route111_Text_BryanIntro, Route111_Text_BryanDefeat
	msgbox Route111_Text_BryanPostBattle, MSGBOX_AUTOCLOSE
	end

Route111_EventScript_Branden::
	trainerbattle_single TRAINER_BRANDEN, Route111_Text_BrandenIntro, Route111_Text_BrandenDefeat
	msgbox Route111_Text_BrandenPostBattle, MSGBOX_AUTOCLOSE
	end

Route111_EventScript_TrainerHillSign::
	msgbox Route111_Text_TrainerHillSign, MSGBOX_SIGN
	end

Route111_Text_BattleOurFamily:
	.string "Hello! A traveler?\p"
	.string "How about taking on our family of four?\n"
	.string "One battle each!\p"
	.string "We're the WINSTRATES. Our hearts beat\n"
	.string "as one. Visitors must battle.$"

Route111_Text_IsThatSo:
	.string "Is that so? Drop in if you change your\n"
	.string "mind!\p"
	.string "We'll be watching. Always.$"

Route111_Text_VictorIntro:
	.string "That's the spirit! My daughter trains\n"
	.string "six hours a day. She's five.$"

Route111_Text_VictorDefeat:
	.string "Aiyah! Don't tell my wife.$"

Route111_Text_VictorPostBattle:
	.string "HONEY! A strong one! Lock the door!$"

Route111_Text_VictoriaIntro:
	.string "You beat my husband? He's useless, but\n"
	.string "still.$"

Route111_Text_VictoriaDefeat:
	.string "You're stronger than my marriage!$"

Route111_Text_VictoriaPostBattle:
	.string "VIVI! Stop crying and get your POKéMON!$"

Route111_Text_ViviIntro:
	.string "You're stronger than Mommy? Daddy says\n"
	.string "I can't have dinner if I lose.$"

Route111_Text_ViviDefeat:
	.string "…No dinner tonight.$"

Route111_Text_ViviPostBattle:
	.string "…Snivel… Grandma, kill them.$"

Route111_Text_VickyIntro:
	.string "How dare you make my granddaughter\n"
	.string "cry! That's MY job!$"

Route111_Text_VickyDefeat:
	.string "Kwah! You're strong… I'll make her train\n"
	.string "harder.$"

Route111_Text_VickyPostBattle:
	.string "Stay for dinner. VIVI isn't having any.$"

Route111_Text_ToughToKeepWinningUpTheRanks:
	.string "I'm a LIFE COACH now! Here's my advice:\n"
	.string "drink water, wake up at 5, believe in\l"
	.string "yourself.\p"
	.string "That'll be 200 POKéDOLLARS. …No, I don't\n"
	.string "have clients yet. Or a job.$"

Route111_Text_WinstrateFamilyDestroyedMe:
	.string "I challenged the WINSTRATES. Four\n"
	.string "battles in a row…\p"
	.string "They destroyed me.\p"
	.string "Then they made me stay for dinner.$"

Route111_Text_RouteSignMauville:
	.string "ROUTE 111\n"
	.string "{DOWN_ARROW} MAUVILLE CITY\p"
	.string "You just came from there. Why are you\n"
	.string "reading this?$"

Route111_Text_WinstrateHouseSign:
	.string "“Our family's hearts beat as one!”\n"
	.string "THE WINSTRATE'S HOUSE\p"
	.string "Visitors must battle.$"

Route111_Text_RouteSign112:
	.string "ROUTE 111\n"
	.string "{LEFT_ARROW} ROUTE 112\p"
	.string "The arrow is correct. Probably.$"

Route111_Text_RouteSign113:
	.string "ROUTE 111\n"
	.string "{LEFT_ARROW} ROUTE 113\p"
	.string "Also left. Everything is left. Don't ask.$"

Route111_Text_OldLadysRestStopSign:
	.string "OLD LADY'S REST STOP\n"
	.string "“Come in and rest your tired bones. She\l"
	.string "insists.”$"

Route111_Text_TrainerTipsSpAtkSpDef:
	.string "TRAINER TIPS\p"
	.string "SP. ATK means “SPECIAL ATTACK.” SP. DEF\n"
	.string "means “SPECIAL DEFENSE.”\p"
	.string "Don't act like this is new information.\n"
	.string "BULBAPEDIA.$"

Route111_Text_ShouldBeMirageTowerAroundHere:
	.string "There's supposed to be a tower of sand\n"
	.string "around here.\p"
	.string "Sometimes you see it, sometimes you\n"
	.string "don't.\p"
	.string "So I call it the MIRAGE TOWER. Or\n"
	.string "heatstroke.$"

Route111_Text_MirageTowerClearlyVisible:
	.string "I see it! The tower of sand!\p"
	.string "It looks so fragile… It could crumble\n"
	.string "any second…\p"
	.string "I want to go in, but I'm scared. You go.$"

Route111_Text_ThatWasShockingSandRainedDown:
	.string "Whoa… That was shocking.\p"
	.string "Sand rained down in chunks.\p"
	.string "What was inside? Sandy ghosts? Tell me\n"
	.string "there were sandy ghosts.$"

Route111_Text_MirageTowerHasntBeenSeenSince:
	.string "The tower of sand hasn't been seen\n"
	.string "since.\p"
	.string "Maybe it really was a mirage…\p"
	.string "Or it's buried. Like my hopes.$"

Route111_Text_ClawFossilDisappeared:
	.string "The CLAW FOSSIL disappeared into the\n"
	.string "sand…\p"
	.string "The desert keeps what it wants.$"

Route111_Text_RootFossilDisappeared:
	.string "The ROOT FOSSIL disappeared into the\n"
	.string "sand…\p"
	.string "The desert keeps what it wants.$"

Route111_Text_MauvilleUncleToldMeToTakeRockSmash:
	.string "Oh, no!\p"
	.string "My uncle in MAUVILLE told me to bring\n"
	.string "ROCK SMASH!\p"
	.string "He lives across from the bike shop. The\n"
	.string "ROCK SMASH DUDE. Woohoo.$"

Route111_Text_TrainerHillSign:
	.string "{RIGHT_ARROW} TRAINER HILL ENTRANCE\p"
	.string "“Scale the heights, you hot-blooded\n"
	.string "TRAINERS!”\p"
	.string "Your knees won't.$"


@ Project Grounded: na Wattson beukt Heatran de stenen boven Mauville weg, loopt langs, ruikt aan je en gaat naar het noorden.
Route111_EventScript_HeatranCutscene::
	goto_if_unset FLAG_BADGE03_GET, Route111_EventScript_HeatranNotYet
	@ Staat de Rock Smash-man er nog, dan komt Heatran pas na zijn dialoog (zie RockSmashTipFatMan)
	goto_if_unset FLAG_HIDE_ROUTE_111_ROCK_SMASH_TIP_GUY, Route111_EventScript_HeatranNotYet
	lockall
	goto Route111_EventScript_HeatranScene

Route111_EventScript_HeatranScene::
	setvar VAR_HEATRAN_CUTSCENE_STATE, 1
	playse SE_M_STRENGTH
	setvar VAR_0x8004, 2  @ vertical pan
	setvar VAR_0x8005, 1  @ horizontal pan
	setvar VAR_0x8006, 10 @ num shakes
	setvar VAR_0x8007, 4  @ shake delay
	special ShakeCamera
	waitstate
	msgbox Route111_Text_HeatranRumble, MSGBOX_DEFAULT
	closemessage
	applymovement OBJ_EVENT_ID_PLAYER, Common_Movement_FaceUp
	waitmovement 0
	@ Project Grounded (Jordi 17 okt): pas als je zelf bij de stenen staat; Heatran beukt ze in beeld weg
	clearflag FLAG_HIDE_ROUTE111_HEATRAN
	addobject LOCALID_ROUTE111_HEATRAN
	applymovement LOCALID_ROUTE111_HEATRAN, Route111_Movement_HeatranToRocks
	waitmovement 0
	playmoncry SPECIES_HEATRAN, CRY_MODE_ENCOUNTER
	waitmoncry
	playse SE_M_ROCK_THROW
	applymovement LOCALID_ROUTE111_HEATRAN_ROCK_2, Movement_SmashRock
	applymovement LOCALID_ROUTE111_HEATRAN_ROCK_1, Movement_SmashRock
	applymovement LOCALID_ROUTE111_ROCK_SMASH_MAN, Common_Movement_ExclamationMark
	waitmovement 0
	removeobject LOCALID_ROUTE111_HEATRAN_ROCK_1
	removeobject LOCALID_ROUTE111_HEATRAN_ROCK_2
	setflag FLAG_HIDE_ROUTE111_HEATRAN_ROCKS
	applymovement LOCALID_ROUTE111_HEATRAN, Route111_Movement_HeatranWalkDown
	waitmovement 0
	playmoncry SPECIES_HEATRAN, CRY_MODE_ENCOUNTER
	waitmoncry
	applymovement OBJ_EVENT_ID_PLAYER, Route111_Movement_PlayerStartled
	waitmovement 0
	msgbox Route111_Text_HeatranSniffs, MSGBOX_DEFAULT
	closemessage
	applymovement LOCALID_ROUTE111_HEATRAN, Route111_Movement_HeatranWalkAway
	waitmovement 0
	removeobject LOCALID_ROUTE111_HEATRAN
	setflag FLAG_HIDE_ROUTE111_HEATRAN
	msgbox Route111_Text_HeatranGone, MSGBOX_DEFAULT
	goto_if_set FLAG_HIDE_ROUTE_111_ROCK_SMASH_TIP_GUY, Route111_EventScript_HeatranSceneEnd
	applymovement LOCALID_ROUTE111_ROCK_SMASH_MAN, Common_Movement_FacePlayer
	waitmovement 0
	msgbox Route111_Text_RockSmashManAfterHeatran, MSGBOX_DEFAULT
	closemessage
	applymovement LOCALID_ROUTE111_ROCK_SMASH_MAN, Common_Movement_FaceOriginalDirection
	waitmovement 0
Route111_EventScript_HeatranSceneEnd::
	releaseall
	end

Route111_EventScript_HeatranNotYet::
	end

Route111_Movement_HeatranToRocks:
	walk_slow_down
	walk_slow_down
	walk_slow_down
	face_down
	step_end

Route111_Movement_HeatranWalkDown:
	walk_down
	walk_left
	walk_down
	walk_down
	delay_16
	step_end

Route111_Movement_PlayerStartled:
	emote_exclamation_mark
	lock_facing_direction
	walk_slow_down
	unlock_facing_direction
	step_end

Route111_Movement_HeatranWalkAway:
	delay_16
	face_up
	delay_16
	walk_up
	walk_up
	walk_up
	walk_up
	walk_up
	walk_up
	walk_up
	step_end

Route111_Text_HeatranRumble:
	.string "The ground is shaking…\n"
	.string "Something big is coming down the route!$"

Route111_Text_HeatranSniffs:
	.string "The POKéMON sniffs at you.\p"
	.string "Its breath smells like a volcano\n"
	.string "that skipped breakfast.\p"
	.string "It seems to have lost interest.$"

Route111_Text_HeatranGone:
	.string "It lumbered off to the north…\p"
	.string "The rocks that blocked the route\n"
	.string "are gone. Melted, probably.$"

@ extra_fights { (tools/grounded/maptools/extra_fights.py)
Route111_EventScript_EF_DaveRoute111::
	trainerbattle_single TRAINER_DAVE_ROUTE_111, Route111_Text_EF_DaveRoute111Intro, Route111_Text_EF_DaveRoute111Defeat, Route111_EventScript_EF_DaveRoute111Defeated
	msgbox Route111_Text_EF_DaveRoute111PostBattle, MSGBOX_AUTOCLOSE
	end

Route111_EventScript_EF_DaveRoute111Defeated::
	msgbox Route111_Text_EF_DaveRoute111PostBattle, MSGBOX_DEFAULT
	closemessage
	fadescreen FADE_TO_BLACK
	removeobject LOCALID_EF_DAVE_ROUTE_111
	fadescreen FADE_FROM_BLACK
	release
	end

Route111_Text_EF_DaveRoute111Intro:
	.string "DAVE: Hey, kleine speler.\p"
	.string "Have you heard about the\n"
	.string "Dublin Rules?\p"
	.string "Cheating is a subjective thing.\p"
	.string "If this girl is related to you,\n"
	.string "like it's your mom or sister,\l"
	.string "it's cheating,\p"
	.string "otherwise it could've been\n"
	.string "non-consensual or accidental.\p"
	.string "Nobody knows!\p"
	.string "Well, let's fight!\n"
	.string "Too much info!$"

Route111_Text_EF_DaveRoute111Defeat:
	.string "{PLAYER}, more....$"

Route111_Text_EF_DaveRoute111PostBattle:
	.string "DAVE: Dublin Rule number two:\n"
	.string "never explain the Dublin Rules.\p"
	.string "I've now broken both.\n"
	.string "Great session. Bye!$"

Route111_EventScript_EF_ShyGuyDesert::
	trainerbattle_single TRAINER_SHY_GUY_DESERT, Route111_Text_EF_ShyGuyDesertIntro, Route111_Text_EF_ShyGuyDesertDefeat
	msgbox Route111_Text_EF_ShyGuyDesertPostBattle, MSGBOX_AUTOCLOSE
	end

Route111_Text_EF_ShyGuyDesertIntro:
	.string "…………\p"
	.string "(A SHY GUY was hiding in the sand.\n"
	.string "He is mortified that you found him.)$"

Route111_Text_EF_ShyGuyDesertDefeat:
	.string "…!\p"
	.string "(He wants to be buried again.\n"
	.string "Preferably forever.)$"

Route111_Text_EF_ShyGuyDesertPostBattle:
	.string "…\p"
	.string "(He is pretending to be a cactus.\n"
	.string "It is not going well.)$"

@ }

@ Project Grounded: Hoopa-quest. Na de Hall of Fame hangt een ring van Hoopa in de zandstorm; erdoor kom je in de
@ Mirage Bazaar (data/maps/MirageBazaar/scripts.inc). De ring blijft ook na de quest hangen.
Route111_EventScript_UpdateHoopaRing::
	setflag FLAG_HIDE_ROUTE111_HOOPA_RING
	goto_if_unset FLAG_SYS_GAME_CLEAR, Route111_EventScript_HoopaRingEnd
	clearflag FLAG_HIDE_ROUTE111_HOOPA_RING
Route111_EventScript_HoopaRingEnd::
	return

Route111_EventScript_HoopaRing::
	lockall
	goto_if_set FLAG_HOOPA_BAZAAR_VISITED, Route111_EventScript_HoopaRingAgain
	msgbox Route111_Text_HoopaRing, MSGBOX_DEFAULT
	closemessage
Route111_EventScript_HoopaRingAgain::
	playse SE_WARP_IN
	warp MAP_MIRAGE_BAZAAR, 14, 20
	waitstate
	releaseall
	end

Route111_Text_HoopaRing:
	.string "A golden ring hangs in the\n"
	.string "sandstorm. It's not attached to\l"
	.string "anything.\p"
	.string "Through it: market stalls, lanterns,\n"
	.string "and someone yelling “NO REFUNDS.”\p"
	.string "You step through. Of course you do.$"

@ --- legends2 (gegenereerd door tools/grounded/maptools/legends2.py) ---
Route111_EventScript_Legends2_GalarTransition:
	setflag FLAG_HIDE_LEGENDS_GALAR_ZAPDOS
	goto_if_set FLAG_CAUGHT_GALAR_ZAPDOS, Route111_EventScript_Legends2_GalarTransitionEnd
	call Legends2_EventScript_GalarReady
	goto_if_eq VAR_RESULT, FALSE, Route111_EventScript_Legends2_GalarTransitionEnd
	clearflag FLAG_HIDE_LEGENDS_GALAR_ZAPDOS
Route111_EventScript_Legends2_GalarTransitionEnd:
	return

Route111_EventScript_GalarZapdos::
	lock
	faceplayer
	playmoncry SPECIES_ZAPDOS_GALAR, CRY_MODE_ENCOUNTER
	msgbox Route111_Text_GalarZapdos, MSGBOX_DEFAULT
	waitmoncry
	closemessage
Route111_EventScript_GalarZapdos_Battle::
	setwildbattle SPECIES_ZAPDOS_GALAR, 88
	setflag FLAG_SYS_CTRL_OBJ_DELETE
	special BattleSetup_StartLegendaryBattle
	waitstate
	clearflag FLAG_SYS_CTRL_OBJ_DELETE
	specialvar VAR_RESULT, GetBattleOutcome
	goto_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, Route111_EventScript_GalarZapdos_Caught
	goto_if_eq VAR_RESULT, B_OUTCOME_RAN, Route111_EventScript_GalarZapdos_Stays
	goto_if_eq VAR_RESULT, B_OUTCOME_PLAYER_TELEPORTED, Route111_EventScript_GalarZapdos_Stays
	removeobject LOCALID_LEGENDS_GALAR_ZAPDOS
	setflag FLAG_HIDE_LEGENDS_GALAR_ZAPDOS
	msgbox Route111_Text_GalarZapdosFled, MSGBOX_DEFAULT
Route111_EventScript_GalarZapdos_Stays::
	release
	end

Route111_EventScript_GalarZapdos_Caught::
	removeobject LOCALID_LEGENDS_GALAR_ZAPDOS
	setflag FLAG_HIDE_LEGENDS_GALAR_ZAPDOS
	setflag FLAG_CAUGHT_GALAR_ZAPDOS
	release
	end

Route111_Text_GalarZapdos:
	.string "Gya-gya!\p"
	.string "(An orange ZAPDOS that cannot fly, will\n"
	.string "not fly, and is doing laps. It's been\l"
	.string "doing laps since the LEAGUE. It is on\l"
	.string "lap four thousand.)$"

Route111_Text_GalarZapdosFled:
	.string "ZAPDOS sprinted off into the\n"
	.string "sandstorm.\p"
	.string "You can hear it doing laps out there.\n"
	.string "It'll be back. It never actually leaves\l"
	.string "the track.$"
@ --- einde legends2 ---

@ Project Grounded: NPC verderop dan Dave (Route 111), die zich als BLUE verkleedt.
Route111_EventScript_DaveBlueGossip::
	msgbox Route111_Text_DaveBlueGossip, MSGBOX_NPC
	end

Route111_Text_DaveBlueGossip:
	.string "Did you see that guy back there? Spiky\n"
	.string "hair, purple shirt, attitude?\p"
	.string "He's cosplaying as BLUE. From KANTO.\n"
	.string "He thinks nobody notices.\p"
	.string "Everybody notices.\p"
	.string "Smell him later, I guess.$"
