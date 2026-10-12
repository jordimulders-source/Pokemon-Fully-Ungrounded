UltraSpace_Nihilego_MapScripts::
	.byte 0

UltraSpace_Nihilego_EventScript_UB::
	lock
	faceplayer
	playmoncry SPECIES_NIHILEGO, CRY_MODE_ENCOUNTER
	msgbox UltraSpace_Nihilego_Text_UB, MSGBOX_DEFAULT
	waitmoncry
	closemessage
	setwildbattle SPECIES_NIHILEGO, 88
	special BattleSetup_StartLegendaryBattle
	waitstate
	specialvar VAR_RESULT, GetBattleOutcome
	goto_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, UltraSpace_Nihilego_EventScript_UBCaught
	goto_if_eq VAR_RESULT, B_OUTCOME_WON, UltraSpace_Nihilego_EventScript_UBBack
	release
	end

UltraSpace_Nihilego_EventScript_UBBack::
	msgbox UltraSpace_Nihilego_Text_UBBack, MSGBOX_DEFAULT
	release
	end

UltraSpace_Nihilego_EventScript_UBCaught::
	setflag FLAG_ULTRA_NIHILEGO
	goto UltraSpace_EventScript_CaughtFade

UltraSpace_Nihilego_EventScript_Jelly::
	msgbox UltraSpace_Nihilego_Text_Jelly, MSGBOX_NPC
	end

UltraSpace_Nihilego_EventScript_Echo::
	msgbox UltraSpace_Nihilego_Text_Echo, MSGBOX_NPC
	end

@ ---------------------------------------------------------------- teksten (placeholders, Jordi herschrijft ze)
UltraSpace_Nihilego_Text_UB:
	.string "A translucent POKéMON drifts through\n"
	.string "the glass. It looks exactly like a\l"
	.string "thought you had once and regretted.$"

UltraSpace_Nihilego_Text_UBBack:
	.string "NIHILEGO wobbles back into the glass.\n"
	.string "It will be back. Thoughts always are.$"

UltraSpace_Nihilego_Text_Jelly:
	.string "It floats through the air as if the air\n"
	.string "were water. Nobody told it otherwise.$"

UltraSpace_Nihilego_Text_Echo:
	.string "A reflection of NIHILEGO. Or NIHILEGO\n"
	.string "is a reflection of this. The glass won't\l"
	.string "say.$"

@ ultra_worlds_a { gegenereerd door tools/grounded/maptools/ultra_worlds_a.py; niet met de hand bewerken
UltraSpace_Nihilego_EventScript_Mirage0::
	lockall
	playse SE_M_HAZE
	setmetatile 4, 18, 9, FALSE
	setmetatile 4, 19, 3, FALSE
	setmetatile 5, 15, 0, FALSE
	setmetatile 5, 16, 7, FALSE
	setmetatile 5, 17, 11, FALSE
	setmetatile 5, 18, 515, FALSE
	setmetatile 5, 19, 0, FALSE
	setmetatile 5, 20, 7, FALSE
	setmetatile 6, 15, 1, FALSE
	setmetatile 6, 16, 4, FALSE
	setmetatile 6, 17, 514, FALSE
	setmetatile 6, 18, 6, FALSE
	setmetatile 6, 19, 1, FALSE
	setmetatile 6, 20, 4, FALSE
	setmetatile 7, 16, 5, FALSE
	setmetatile 7, 17, 10, FALSE
	setmetatile 7, 18, 2, FALSE
	setmetatile 7, 19, 512, FALSE
	setmetatile 7, 20, 5, FALSE
	setmetatile 7, 21, 10, FALSE
	setmetatile 8, 15, 3, FALSE
	setmetatile 8, 16, 513, FALSE
	setmetatile 8, 17, 8, FALSE
	setmetatile 8, 18, 9, FALSE
	setmetatile 8, 19, 3, FALSE
	setmetatile 8, 20, 513, FALSE
	setmetatile 8, 21, 8, FALSE
	setmetatile 9, 15, 0, FALSE
	setmetatile 9, 16, 7, FALSE
	setmetatile 9, 17, 11, FALSE
	setmetatile 9, 18, 515, FALSE
	setmetatile 9, 19, 0, FALSE
	setmetatile 9, 20, 7, FALSE
	setmetatile 9, 21, 11, FALSE
	setmetatile 10, 18, 6, FALSE
	setmetatile 10, 19, 1, FALSE
	setmetatile 10, 20, 4, FALSE
	special DrawWholeMapView
	waitse
	setvar VAR_TEMP_1, 1
	releaseall
	end

UltraSpace_Nihilego_EventScript_Mirage1::
	lockall
	playse SE_M_HAZE
	setmetatile 30, 19, 1, FALSE
	setmetatile 30, 20, 4, FALSE
	setmetatile 30, 21, 514, FALSE
	setmetatile 30, 22, 6, FALSE
	setmetatile 31, 17, 10, FALSE
	setmetatile 31, 18, 2, FALSE
	setmetatile 31, 19, 512, FALSE
	setmetatile 31, 20, 5, FALSE
	setmetatile 31, 21, 10, FALSE
	setmetatile 31, 22, 2, FALSE
	setmetatile 31, 23, 512, FALSE
	setmetatile 32, 17, 8, FALSE
	setmetatile 32, 18, 9, FALSE
	setmetatile 32, 19, 3, FALSE
	setmetatile 32, 20, 513, FALSE
	setmetatile 32, 21, 8, FALSE
	setmetatile 32, 22, 9, FALSE
	setmetatile 32, 23, 3, FALSE
	setmetatile 33, 17, 11, FALSE
	setmetatile 33, 18, 515, FALSE
	setmetatile 33, 19, 0, FALSE
	setmetatile 33, 20, 7, FALSE
	setmetatile 33, 21, 11, FALSE
	setmetatile 33, 22, 515, FALSE
	setmetatile 33, 23, 0, FALSE
	setmetatile 34, 18, 6, FALSE
	setmetatile 34, 19, 1, FALSE
	setmetatile 34, 20, 4, FALSE
	setmetatile 34, 21, 514, FALSE
	setmetatile 34, 22, 6, FALSE
	setmetatile 34, 23, 1, FALSE
	setmetatile 35, 17, 10, FALSE
	setmetatile 35, 18, 2, FALSE
	setmetatile 35, 19, 512, FALSE
	setmetatile 35, 20, 5, FALSE
	setmetatile 35, 21, 10, FALSE
	setmetatile 35, 22, 2, FALSE
	setmetatile 35, 23, 512, FALSE
	setmetatile 36, 19, 3, FALSE
	setmetatile 36, 20, 513, FALSE
	setmetatile 36, 21, 8, FALSE
	setmetatile 36, 22, 9, FALSE
	special DrawWholeMapView
	waitse
	setvar VAR_TEMP_2, 1
	releaseall
	end

UltraSpace_Nihilego_EventScript_Mirage2::
	lockall
	playse SE_M_HAZE
	setmetatile 29, 12, 7, FALSE
	setmetatile 29, 13, 11, FALSE
	setmetatile 29, 15, 0, FALSE
	setmetatile 29, 16, 7, FALSE
	setmetatile 29, 17, 11, FALSE
	setmetatile 30, 12, 4, FALSE
	setmetatile 30, 13, 514, FALSE
	setmetatile 30, 14, 6, FALSE
	setmetatile 30, 15, 1, FALSE
	setmetatile 30, 16, 4, FALSE
	setmetatile 30, 17, 514, FALSE
	setmetatile 31, 12, 5, FALSE
	setmetatile 31, 13, 10, FALSE
	setmetatile 31, 14, 2, FALSE
	setmetatile 31, 15, 512, FALSE
	setmetatile 31, 16, 5, FALSE
	setmetatile 31, 17, 10, FALSE
	setmetatile 32, 12, 513, FALSE
	setmetatile 32, 13, 8, FALSE
	setmetatile 32, 14, 9, FALSE
	setmetatile 32, 15, 3, FALSE
	setmetatile 32, 16, 513, FALSE
	setmetatile 32, 17, 8, FALSE
	setmetatile 33, 12, 7, FALSE
	setmetatile 33, 13, 11, FALSE
	setmetatile 33, 14, 515, FALSE
	setmetatile 33, 15, 0, FALSE
	setmetatile 33, 16, 7, FALSE
	setmetatile 33, 17, 11, FALSE
	setmetatile 34, 15, 1, FALSE
	setmetatile 34, 16, 4, FALSE
	special DrawWholeMapView
	waitse
	setvar VAR_TEMP_3, 1
	releaseall
	end
@ } ultra_worlds_a
