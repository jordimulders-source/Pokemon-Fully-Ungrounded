Route105_MapScripts::
	map_script MAP_SCRIPT_ON_LOAD, Route105_OnLoad
	map_script MAP_SCRIPT_ON_TRANSITION, Route105_OnTransition
	map_script MAP_SCRIPT_ON_FRAME_TABLE, Route105_OnFrame
	.byte 0

Route105_OnLoad:
	call_if_unset FLAG_REGI_DOORS_OPENED, Route105_CloseRegiEntrance
	call_if_eq VAR_ABNORMAL_WEATHER_LOCATION, ABNORMAL_WEATHER_ROUTE_105_NORTH, AbnormalWeather_EventScript_PlaceTilesRoute105North
	call_if_eq VAR_ABNORMAL_WEATHER_LOCATION, ABNORMAL_WEATHER_ROUTE_105_SOUTH, AbnormalWeather_EventScript_PlaceTilesRoute105South
	end

Route105_CloseRegiEntrance::
	setmetatile 9, 19, METATILE_General_RockWall_RockBase, TRUE
	setmetatile 9, 20, METATILE_General_RockWall_SandBase, TRUE
	return

Route105_OnTransition:
	call_if_eq VAR_SHOULD_END_ABNORMAL_WEATHER, 1, AbnormalWeather_EventScript_HideMapNamePopup
	call_if_eq VAR_ABNORMAL_WEATHER_LOCATION, ABNORMAL_WEATHER_ROUTE_105_NORTH, AbnormalWeather_StartKyogreWeather
	call_if_eq VAR_ABNORMAL_WEATHER_LOCATION, ABNORMAL_WEATHER_ROUTE_105_SOUTH, AbnormalWeather_StartKyogreWeather
	end

Route105_OnFrame:
	map_script_2 VAR_SHOULD_END_ABNORMAL_WEATHER, 1, AbnormalWeather_EventScript_EndEventAndCleanup_1
	.2byte 0

Route105_EventScript_Foster::
	trainerbattle_single TRAINER_FOSTER, Route105_Text_FosterIntro, Route105_Text_FosterDefeated
	msgbox Route105_Text_FosterPostBattle, MSGBOX_AUTOCLOSE
	end

Route105_EventScript_Luis::
	trainerbattle_single TRAINER_LUIS, Route105_Text_LuisIntro, Route105_Text_LuisDefeated
	msgbox Route105_Text_LuisPostBattle, MSGBOX_AUTOCLOSE
	end

Route105_EventScript_Dominik::
	trainerbattle_single TRAINER_DOMINIK, Route105_Text_DominikIntro, Route105_Text_DominikDefeated
	msgbox Route105_Text_DominikPostBattle, MSGBOX_AUTOCLOSE
	end

Route105_EventScript_Beverly::
	trainerbattle_single TRAINER_BEVERLY, Route105_Text_BeverlyIntro, Route105_Text_BeverlyDefeated
	msgbox Route105_Text_PostBattle, MSGBOX_AUTOCLOSE
	end

Route105_EventScript_Imani::
	trainerbattle_single TRAINER_IMANI, Route105_Text_ImaniIntro, Route105_Text_ImaniDefeated
	msgbox Route105_Text_ImaniPostBattle, MSGBOX_AUTOCLOSE
	end

Route105_EventScript_Josue::
	trainerbattle_single TRAINER_JOSUE, Route105_Text_JosueIntro, Route105_Text_JosueDefeated
	msgbox Route105_Text_JosuePostBattle, MSGBOX_AUTOCLOSE
	end

Route105_EventScript_Andres::
	trainerbattle_single TRAINER_ANDRES_1, Route105_Text_AndresIntro, Route105_Text_AndresDefeated, Route105_EventScript_AndresRegisterMatchCallAfterBattle
	specialvar VAR_RESULT, ShouldTryRematchBattle
	goto_if_eq VAR_RESULT, TRUE, Route105_EventScript_AndresRematch
	msgbox Route105_Text_AndresPostBattle, MSGBOX_DEFAULT
	release
	end

Route105_EventScript_AndresRegisterMatchCallAfterBattle::
	special PlayerFaceTrainerAfterBattle
	waitmovement 0
	msgbox Route105_Text_AndresRegister, MSGBOX_DEFAULT
	register_matchcall TRAINER_ANDRES_1
	release
	end

Route105_EventScript_AndresRematch::
	trainerbattle_rematch TRAINER_ANDRES_1, Route105_Text_AndresRematchIntro, Route105_Text_AndresRematchDefeated
	msgbox Route105_Text_AndresRematchPostBattle, MSGBOX_AUTOCLOSE
	end

Route104_Text_DadPokenavCall:
	.string "… … … … … … Beep!\p"
	.string "DAD: Oh, {PLAYER}?\p"
	.string "… … … Where are you? It sounds windy.\p"
	.string "MR. STONE told me about your POKéNAV,\n"
	.string "so I called.\p"
	.string "You sound fine. Good.\p"
	.string "Take care.\p"
	.string "… … … … … … Click!\p"
	.string "…That was the longest conversation\n"
	.string "we've had in years.$"

Route104_Text_RegisteredDadInPokenav:
	.string "Registered DAD NORMAN in the POKéNAV.\p"
	.string "He won't call. But he's there.$"

@ --- zee_vulling_2 (gegenereerd door tools/grounded/maptools/zee_vulling_2.py) ---
Route105_EventScript_ZV2Castaway::
	lock
	faceplayer
	goto_if_set FLAG_RECEIVED_ROUTE_105_FOCUS_SASH, Route105_EventScript_ZV2Castaway_After
	msgbox Route105_Text_ZV2Castaway, MSGBOX_DEFAULT
	giveitem ITEM_FOCUS_SASH
	goto_if_eq VAR_RESULT, FALSE, Common_EventScript_ShowBagIsFull
	setflag FLAG_RECEIVED_ROUTE_105_FOCUS_SASH
	release
	end
Route105_EventScript_ZV2Castaway_After:
	msgbox Route105_Text_ZV2CastawayAfter, MSGBOX_DEFAULT
	release
	end

Route105_Text_ZV2Castaway:
	.string "Rescue? No thanks.\pI've lived on this sandbank for\nthree years. DEWFORD is right\lthere. I can see the gym.\pI could swim back any time.\nI choose not to. Taxes, you know.\pHere, take this. I don't need it.\nI can't focus on anything except\lthe horizon.$"

Route105_Text_ZV2CastawayAfter:
	.string "WILSON and I are doing great.\nHe's a very good listener.\lSometimes he explodes. We all do.$"

Route105_EventScript_ZV2Wilson::
	lock
	faceplayer
	playmoncry SPECIES_VOLTORB, CRY_MODE_NORMAL
	msgbox Route105_Text_ZV2Wilson, MSGBOX_DEFAULT
	waitmoncry
	release
	end

Route105_Text_ZV2Wilson:
	.string "A VOLTORB with a face painted on it.\p...No, wait. That's just its face.\nIt looks at you like it's waiting\lfor an apology.$"

Route105_EventScript_ZV2Kenta::
	trainerbattle_single TRAINER_BLACK_BELT_KENTA, Route105_Text_ZV2Kenta_Intro, Route105_Text_ZV2Kenta_Defeat
	msgbox Route105_Text_ZV2Kenta_Post, MSGBOX_AUTOCLOSE
	end

Route105_Text_ZV2Kenta_Intro:
	.string "Every morning I punch the tide\na thousand times.\pThe tide has never lost.\nNeither have I. We're both stubborn.$"

Route105_Text_ZV2Kenta_Defeat:
	.string "The tide is laughing at me.\nI can hear it. Shhhh. Shhhh.$"

Route105_Text_ZV2Kenta_Post:
	.string "The castaway says I'm his only\nfriend. Then he talks to the\lVOLTORB for six hours.$"
@ --- einde zee_vulling_2 ---
