Route124_MapScripts::
	map_script MAP_SCRIPT_ON_TRANSITION, Route124_OnTransition
	.byte 0

Route124_OnTransition:
	setvar VAR_0x8004, 1
	call Common_EventScript_GiantWailordSpawn
	call_if_set FLAG_SYS_WEATHER_CTRL, Common_EventScript_SetAbnormalWeather
	end

Route124_EventScript_HuntersHouseSign::
	msgbox Route124_Text_HuntersHouse, MSGBOX_SIGN
	end

Route124_EventScript_Spencer::
	trainerbattle_single TRAINER_SPENCER, Route124_Text_SpencerIntro, Route124_Text_SpencerDefeat
	msgbox Route124_Text_SpencerPostBattle, MSGBOX_AUTOCLOSE
	end

Route124_EventScript_Roland::
	trainerbattle_single TRAINER_ROLAND, Route124_Text_RolandIntro, Route124_Text_RolandDefeat
	msgbox Route124_Text_RolandPostBattle, MSGBOX_AUTOCLOSE
	end

Route124_EventScript_Jenny::
	trainerbattle_single TRAINER_JENNY_1, Route124_Text_JennyIntro, Route124_Text_JennyDefeat, Route124_EventScript_RegisterJenny
	specialvar VAR_RESULT, ShouldTryRematchBattle
	goto_if_eq VAR_RESULT, TRUE, Route124_EventScript_RematchJenny
	msgbox Route124_Text_JennyPostBattle, MSGBOX_DEFAULT
	release
	end

Route124_EventScript_RegisterJenny::
	special PlayerFaceTrainerAfterBattle
	waitmovement 0
	msgbox Route124_Text_JennyRegister, MSGBOX_DEFAULT
	register_matchcall TRAINER_JENNY_1
	release
	end

Route124_EventScript_RematchJenny::
	trainerbattle_rematch TRAINER_JENNY_1, Route124_Text_JennyRematchIntro, Route124_Text_JennyRematchDefeat
	msgbox Route124_Text_JennyPostRematch, MSGBOX_AUTOCLOSE
	end

Route124_EventScript_Grace::
	trainerbattle_single TRAINER_GRACE, Route124_Text_GraceIntro, Route124_Text_GraceDefeat
	msgbox Route124_Text_GracePostBattle, MSGBOX_AUTOCLOSE
	end

Route124_EventScript_Chad::
	trainerbattle_single TRAINER_CHAD, Route124_Text_ChadIntro, Route124_Text_ChadDefeat
	msgbox Route124_Text_ChadPostBattle, MSGBOX_AUTOCLOSE
	end

Route124_EventScript_Lila::
	trainerbattle_double TRAINER_LILA_AND_ROY_1, Route124_Text_LilaIntro, Route124_Text_LilaDefeat, Route124_Text_LilaNotEnoughMons, Route124_EventScript_RegisterLila
	specialvar VAR_RESULT, ShouldTryRematchBattle
	goto_if_eq VAR_RESULT, TRUE, Route124_EventScript_RematchLila
	msgbox Route124_Text_LilaPostBattle, MSGBOX_DEFAULT
	release
	end

Route124_EventScript_RegisterLila::
	msgbox Route124_Text_LilaRoyRegister, MSGBOX_DEFAULT
	register_matchcall TRAINER_LILA_AND_ROY_1
	release
	end

Route124_EventScript_RematchLila::
	trainerbattle_rematch_double TRAINER_LILA_AND_ROY_1, Route124_Text_LilaRematchIntro, Route124_Text_LilaRematchDefeat, Route124_Text_LilaRematchNotEnoughMons
	msgbox Route124_Text_LilaPostRematch, MSGBOX_AUTOCLOSE
	end

Route124_EventScript_Roy::
	trainerbattle_double TRAINER_LILA_AND_ROY_1, Route124_Text_RoyIntro, Route124_Text_RoyDefeat, Route124_Text_RoyNotEnoughMons, Route124_EventScript_RegisterRoy
	specialvar VAR_RESULT, ShouldTryRematchBattle
	goto_if_eq VAR_RESULT, TRUE, Route124_EventScript_RematchRoy
	msgbox Route124_Text_RoyPostBattle, MSGBOX_DEFAULT
	release
	end

Route124_EventScript_RegisterRoy::
	msgbox Route124_Text_LilaRoyRegister, MSGBOX_DEFAULT
	register_matchcall TRAINER_LILA_AND_ROY_1
	release
	end

Route124_EventScript_RematchRoy::
	trainerbattle_rematch_double TRAINER_LILA_AND_ROY_1, Route124_Text_RoyRematchIntro, Route124_Text_RoyRematchDefeat, Route124_Text_RoyRematchNotEnoughMons
	msgbox Route124_Text_RoyPostRematch, MSGBOX_AUTOCLOSE
	end

Route124_EventScript_Declan::
	trainerbattle_single TRAINER_DECLAN, Route124_Text_DeclanIntro, Route124_Text_DeclanDefeat
	msgbox Route124_Text_DeclanPostBattle, MSGBOX_AUTOCLOSE
	end

Route124_EventScript_Isabella::
	trainerbattle_single TRAINER_ISABELLA, Route124_Text_IsabellaIntro, Route124_Text_IsabellaDefeat
	msgbox Route124_Text_IsabellaPostBattle, MSGBOX_AUTOCLOSE
	end

Route124_Text_HuntersHouse:
	.string "HUNTER'S HOUSE\p"
	.string "Shards only. Relax.$"

@ --- zee_vulling_2 (gegenereerd door tools/grounded/maptools/zee_vulling_2.py) ---
Route124_EventScript_ZV2Weatherman::
	lock
	faceplayer
	goto_if_set FLAG_RECEIVED_ROUTE_124_SMOOTH_ROCK, Route124_EventScript_ZV2Weatherman_After
	msgbox Route124_Text_ZV2Weatherman, MSGBOX_DEFAULT
	giveitem ITEM_SMOOTH_ROCK
	goto_if_eq VAR_RESULT, FALSE, Common_EventScript_ShowBagIsFull
	setflag FLAG_RECEIVED_ROUTE_124_SMOOTH_ROCK
	release
	end
Route124_EventScript_ZV2Weatherman_After:
	msgbox Route124_Text_ZV2WeathermanAfter, MSGBOX_DEFAULT
	release
	end

Route124_Text_ZV2Weatherman:
	.string "Welcome to HOENN WEATHER STATION\nnumber 2. Number 1 blew away.\pMy equipment: one CASTFORM.\nIf it's round, nice weather.\lIf it's on fire, also nice weather.\pIf it's gone, run.\pHere, a souvenir. It's a rock.\nVery smooth. Science!$"

Route124_Text_ZV2WeathermanAfter:
	.string "Today's forecast: weather.\nI'm right 100% of the time.$"

Route124_EventScript_ZV2Castform::
	lock
	faceplayer
	playmoncry SPECIES_CASTFORM, CRY_MODE_NORMAL
	msgbox Route124_Text_ZV2Castform, MSGBOX_DEFAULT
	waitmoncry
	release
	end

Route124_Text_ZV2Castform:
	.string "The CASTFORM is round.\nThe forecast is good.\pIt looks very proud of this.$"

Route124_EventScript_ZV2Elliot::
	trainerbattle_single TRAINER_BUG_MANIAC_ELLIOT, Route124_Text_ZV2Elliot_Intro, Route124_Text_ZV2Elliot_Defeat
	msgbox Route124_Text_ZV2Elliot_Post, MSGBOX_AUTOCLOSE
	end

Route124_Text_ZV2Elliot_Intro:
	.string "Shh! The VOLBEAT and ILLUMISE\ndance here at night.\pI've been watching them for a\nweek. I think they're watching\lme back. Battle!$"

Route124_Text_ZV2Elliot_Defeat:
	.string "My bugs are fine. They're just\nlying down. Dramatically.$"

Route124_Text_ZV2Elliot_Post:
	.string "The weatherman says there's a\nstorm coming. He says that every\lday. One day he'll be right.$"

Route124_EventScript_ZV2Abe::
	trainerbattle_single TRAINER_CAPTAIN_ABE, Route124_Text_ZV2Abe_Intro, Route124_Text_ZV2Abe_Defeat
	msgbox Route124_Text_ZV2Abe_Post, MSGBOX_AUTOCLOSE
	end

Route124_Text_ZV2Abe_Intro:
	.string "Call me ABE. Somewhere in these\nwaters swims a WAILORD the size\lof a town. White as a cloud.\pIt took my boat. My hat. My\nsandwich. Today I take it back!$"

Route124_Text_ZV2Abe_Defeat:
	.string "Argh! You fight like that WAILORD.\nHeavy. Wet. Unbothered.$"

Route124_Text_ZV2Abe_Post:
	.string "Some days the giant WAILORD is\nhere, some days it isn't.\pWhen it is, it's asleep. I've\nnever had the heart to wake it.$"

Route124_EventScript_ZV2AbeBoat::
	msgbox Route124_Text_ZV2AbeBoat, MSGBOX_SIGN
	end

Route124_Text_ZV2AbeBoat:
	.string "ABE's boat. Named the 'SEQUEL'.\pThe first boat is inside a WAILORD.$"
@ --- einde zee_vulling_2 ---
