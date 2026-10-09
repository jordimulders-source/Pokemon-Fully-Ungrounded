Route127_MapScripts::
	map_script MAP_SCRIPT_ON_TRANSITION, Route127_OnTransition
	map_script MAP_SCRIPT_ON_LOAD, Route127_OnLoad
	map_script MAP_SCRIPT_ON_FRAME_TABLE, Route127_OnFrame
	.byte 0

Route127_OnTransition:
	call_if_set FLAG_SYS_WEATHER_CTRL, Common_EventScript_SetAbnormalWeather
	call_if_eq VAR_SHOULD_END_ABNORMAL_WEATHER, 1, AbnormalWeather_EventScript_HideMapNamePopup
	call_if_eq VAR_ABNORMAL_WEATHER_LOCATION, ABNORMAL_WEATHER_ROUTE_127_NORTH, AbnormalWeather_StartKyogreWeather
	call_if_eq VAR_ABNORMAL_WEATHER_LOCATION, ABNORMAL_WEATHER_ROUTE_127_SOUTH, AbnormalWeather_StartKyogreWeather
	end

Route127_OnLoad:
	call_if_eq VAR_ABNORMAL_WEATHER_LOCATION, ABNORMAL_WEATHER_ROUTE_127_NORTH, AbnormalWeather_EventScript_PlaceTilesRoute127North
	call_if_eq VAR_ABNORMAL_WEATHER_LOCATION, ABNORMAL_WEATHER_ROUTE_127_SOUTH, AbnormalWeather_EventScript_PlaceTilesRoute127South
	end

Route127_OnFrame:
	map_script_2 VAR_SHOULD_END_ABNORMAL_WEATHER, 1, AbnormalWeather_EventScript_EndEventAndCleanup_1
	.2byte 0

Route127_EventScript_Camden::
	trainerbattle_single TRAINER_CAMDEN, Route127_Text_CamdenIntro, Route127_Text_CamdenDefeat
	msgbox Route127_Text_CamdenPostBattle, MSGBOX_AUTOCLOSE
	end

Route127_EventScript_Donny::
	trainerbattle_single TRAINER_DONNY, Route127_Text_DonnyIntro, Route127_Text_DonnyDefeat
	msgbox Route127_Text_DonnyPostBattle, MSGBOX_AUTOCLOSE
	end

Route127_EventScript_Jonah::
	trainerbattle_single TRAINER_JONAH, Route127_Text_JonahIntro, Route127_Text_JonahDefeat
	msgbox Route127_Text_JonahPostBattle, MSGBOX_AUTOCLOSE
	end

Route127_EventScript_Henry::
	trainerbattle_single TRAINER_HENRY, Route127_Text_HenryIntro, Route127_Text_HenryDefeat
	msgbox Route127_Text_HenryPostBattle, MSGBOX_AUTOCLOSE
	end

Route127_EventScript_Roger::
	trainerbattle_single TRAINER_ROGER, Route127_Text_RogerIntro, Route127_Text_RogerDefeat
	msgbox Route127_Text_RogerPostBattle, MSGBOX_AUTOCLOSE
	end

Route127_EventScript_Aidan::
	trainerbattle_single TRAINER_AIDAN, Route127_Text_AidanIntro, Route127_Text_AidanDefeat
	msgbox Route127_Text_AidanPostBattle, MSGBOX_AUTOCLOSE
	end

Route127_EventScript_Athena::
	trainerbattle_single TRAINER_ATHENA, Route127_Text_AthenaIntro, Route127_Text_AthenaDefeat
	msgbox Route127_Text_AthenaPostBattle, MSGBOX_AUTOCLOSE
	end

Route127_EventScript_Koji::
	trainerbattle_single TRAINER_KOJI_1, Route127_Text_KojiIntro, Route127_Text_KojiDefeat, Route127_EventScript_RegisterKoji
	specialvar VAR_RESULT, ShouldTryRematchBattle
	goto_if_eq VAR_RESULT, TRUE, Route127_EventScript_RematchKoji
	msgbox Route127_Text_KojiPostBattle, MSGBOX_DEFAULT
	release
	end

Route127_EventScript_RegisterKoji::
	special PlayerFaceTrainerAfterBattle
	waitmovement 0
	msgbox Route127_Text_KojiRegister, MSGBOX_DEFAULT
	register_matchcall TRAINER_KOJI_1
	release
	end

Route127_EventScript_RematchKoji::
	trainerbattle_rematch TRAINER_KOJI_1, Route127_Text_KojiRematchIntro, Route127_Text_KojiRematchDefeat
	msgbox Route127_Text_KojiPostRematch, MSGBOX_AUTOCLOSE
	end

@ --- zee_vulling_1 (gegenereerd door tools/grounded/maptools/zee_vulling_1.py) ---
Route127_EventScript_ZVWailmer::
	lock
	faceplayer
	msgbox Route127_Text_ZVWailmer, MSGBOX_DEFAULT
	playmoncry SPECIES_WAILMER, CRY_MODE_NORMAL
	waitmoncry
	fadescreen FADE_TO_BLACK
	removeobject VAR_LAST_TALKED
	setflag FLAG_ROUTE_127_WAILMER_RESCUED
	fadescreen FADE_FROM_BLACK
	msgbox Route127_Text_ZVWailmerGone, MSGBOX_DEFAULT
	giveitem ITEM_SHELL_BELL
	release
	end

Route127_Text_ZVWailmer:
	.string "A WAILMER is stranded on the\nsand. It looks at you like you\lowe it money.\pYou push. And push. It rolls into\nthe sea with the grace of a\ldropped piano.$"

Route127_Text_ZVWailmerGone:
	.string "Far away, a spout of water.\nSomething shiny lands at your feet.\pA tip. From a whale.$"

Route127_EventScript_ZVMarisol::
	trainerbattle_single TRAINER_RANGER_MARISOL, Route127_Text_ZVMarisol_Intro, Route127_Text_ZVMarisol_Defeat
	msgbox Route127_Text_ZVMarisol_Post, MSGBOX_AUTOCLOSE
	end

Route127_Text_ZVMarisol_Intro:
	.string "Stand back! This WAILMER has been\nstranded for six hours.\pI've been observing it. Taking\nnotes. Very important notes.\lMostly drawings.$"

Route127_Text_ZVMarisol_Defeat:
	.string "You're right. Pushing it back\nwould also have been an option.$"

Route127_Text_ZVMarisol_Post:
	.string "Ranger protocol says observe, don't\ninterfere. Ranger protocol has\lnever met a sad whale.$"

Route127_EventScript_ZVTourist::
	msgbox Route127_Text_ZVTourist, MSGBOX_NPC
	end

Route127_Text_ZVTourist:
	.string "Excuse me, is this Kalos?\pMy map says the hotel is right\nhere. The map is of Kalos.\p...Is it upside down? Oh. Oh no.\nThen I swam the wrong way for\ltwo weeks.\pStill. Five stars. Great water.$"

Route127_EventScript_ZVTwins::
	trainerbattle_double TRAINER_TWINS_PIP_AND_PEP, Route127_Text_ZVTwins_Intro, Route127_Text_ZVTwins_Defeat, Route127_Text_ZVTwins_NotEnough
	msgbox Route127_Text_ZVTwins_Post, MSGBOX_AUTOCLOSE
	end

Route127_Text_ZVTwins_Intro:
	.string "PIP: We swam here on a floatie!\nPEP: The floatie popped!\pPIP: Now we live here!\nPEP: Mom doesn't know yet!$"

Route127_Text_ZVTwins_Defeat:
	.string "PIP: We lost!\nPEP: Like the floatie!$"

Route127_Text_ZVTwins_NotEnough:
	.string "PIP: Two against one is unfair.\nPEP: Come back with a friend!$"

Route127_Text_ZVTwins_Post:
	.string "PIP: If you see Mom, say we're\nat a sleepover.\pPEP: With a sandbank!$"
@ --- einde zee_vulling_1 ---

@ --- zee_vulling_3 (gegenereerd door tools/grounded/maptools/zee_vulling_3.py) ---
Route127_EventScript_ZV3Mine0::
	lock
	faceplayer
	playmoncry SPECIES_VOLTORB, CRY_MODE_ENCOUNTER
	msgbox Route127_Text_ZV3Mine, MSGBOX_DEFAULT
	waitmoncry
	setwildbattle SPECIES_VOLTORB, 69
	dowildbattle
	removeobject VAR_LAST_TALKED
	release
	end

Route127_EventScript_ZV3Mine1::
	lock
	faceplayer
	playmoncry SPECIES_ELECTRODE, CRY_MODE_ENCOUNTER
	msgbox Route127_Text_ZV3Mine, MSGBOX_DEFAULT
	waitmoncry
	setwildbattle SPECIES_ELECTRODE, 70
	dowildbattle
	removeobject VAR_LAST_TALKED
	release
	end

Route127_EventScript_ZV3Mine2::
	lock
	faceplayer
	playmoncry SPECIES_VOLTORB, CRY_MODE_ENCOUNTER
	msgbox Route127_Text_ZV3Mine, MSGBOX_DEFAULT
	waitmoncry
	setwildbattle SPECIES_VOLTORB, 69
	dowildbattle
	removeobject VAR_LAST_TALKED
	release
	end

Route127_EventScript_ZV3Mine3::
	lock
	faceplayer
	playmoncry SPECIES_ELECTRODE, CRY_MODE_ENCOUNTER
	msgbox Route127_Text_ZV3Mine, MSGBOX_DEFAULT
	waitmoncry
	setwildbattle SPECIES_ELECTRODE, 70
	dowildbattle
	removeobject VAR_LAST_TALKED
	release
	end

Route127_EventScript_ZV3Mine4::
	lock
	faceplayer
	playmoncry SPECIES_VOLTORB_HISUI, CRY_MODE_ENCOUNTER
	msgbox Route127_Text_ZV3MineAntique, MSGBOX_DEFAULT
	waitmoncry
	setwildbattle SPECIES_VOLTORB_HISUI, 69
	dowildbattle
	removeobject VAR_LAST_TALKED
	release
	end

Route127_EventScript_ZV3Mine5::
	lock
	faceplayer
	playmoncry SPECIES_ELECTRODE, CRY_MODE_ENCOUNTER
	msgbox Route127_Text_ZV3Mine, MSGBOX_DEFAULT
	waitmoncry
	setwildbattle SPECIES_ELECTRODE, 70
	dowildbattle
	removeobject VAR_LAST_TALKED
	release
	end

Route127_Text_ZV3Mine:
	.string "Something round is bobbing in the\nwater. It's ticking.\pIt's a SEA MINE!\n...No. It's a POKeMON pretending.\lIt's very committed to the bit.$"

Route127_Text_ZV3MineAntique:
	.string "This mine is made of wood and has\na fuse. An antique.\pIt looks at you like you are\nthe newfangled one.$"

Route127_EventScript_ZV3Warning::
	msgbox Route127_Text_ZV3Warning, MSGBOX_SIGN
	end

Route127_Text_ZV3Warning:
	.string "DANGER: MINEFIELD.\nDO NOT TOUCH, PET OR CATCH.\pSomeone has scratched underneath:\n'they respawn btw'$"
@ --- einde zee_vulling_3 ---

@ --- zee_vulling_4 (gegenereerd door tools/grounded/maptools/zee_vulling_4.py) ---
Route127_EventScript_ZV4Oceanographer::
	msgbox Route127_Text_ZV4Oceanographer, MSGBOX_NPC
	end

Route127_Text_ZV4Oceanographer:
	.string "I measure the depth of the trench\nwest of here. With a rope.\pThe rope ran out. I tied on a\nsecond rope. That ran out too.\pOfficial result: two ropes deep.\nIf you DIVE at the head of the\ltrench, look for a hole. Bring\lrope.$"
@ --- einde zee_vulling_4 ---
