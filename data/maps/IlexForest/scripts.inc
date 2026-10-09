@ Project Grounded: IlexForest (tools/grounded/maptools/national_park.py)
IlexForest_MapScripts::
	map_script MAP_SCRIPT_ON_TRANSITION, IlexForest_OnTransition
	.byte 0

IlexForest_OnTransition:
	setflag FLAG_TEMP_1
	end

IlexForest_EventScript_Shrine::
	lock
	goto_if_set FLAG_NATIONAL_PARK_CELEBI_DONE, IlexForest_EventScript_ShrineDone
	goto_if_unset FLAG_NATIONAL_PARK_REVEALED, IlexForest_EventScript_ShrineQuiet
	goto_if_not_defeated TRAINER_NP_SHADOW_ASH, IlexForest_EventScript_ShrineQuiet
	goto_if_not_defeated TRAINER_NP_SHADOW_EMBER, IlexForest_EventScript_ShrineQuiet
	msgbox IlexForest_Text_ShrineCall, MSGBOX_DEFAULT
	closemessage
	playse SE_M_HEAL_BELL
	clearflag FLAG_TEMP_1
	addobject LOCALID_ILEX_FOREST_CELEBI
	delay 20
	goto IlexForest_EventScript_CelebiBattle

IlexForest_EventScript_Celebi::
	lock
IlexForest_EventScript_CelebiBattle::
	playmoncry SPECIES_CELEBI, CRY_MODE_ENCOUNTER
	msgbox IlexForest_Text_Celebi, MSGBOX_DEFAULT
	waitmoncry
	closemessage
	setwildbattle SPECIES_CELEBI, 93
	special BattleSetup_StartLegendaryBattle
	waitstate
	specialvar VAR_RESULT, GetBattleOutcome
	goto_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, IlexForest_EventScript_CelebiCaught
	goto_if_eq VAR_RESULT, B_OUTCOME_WON, IlexForest_EventScript_CelebiReset
	release
	end

IlexForest_EventScript_CelebiReset::
	playse SE_M_TELEPORT
	fadescreenspeed FADE_TO_WHITE, 4
	fadescreenspeed FADE_FROM_WHITE, 4
	msgbox IlexForest_Text_CelebiReset, MSGBOX_DEFAULT
	release
	end

IlexForest_EventScript_CelebiCaught::
	removeobject LOCALID_ILEX_FOREST_CELEBI
	setflag FLAG_NATIONAL_PARK_CELEBI_DONE
	msgbox IlexForest_Text_CelebiCaught, MSGBOX_DEFAULT
	release
	end

IlexForest_EventScript_ShrineQuiet::
	msgbox IlexForest_Text_ShrineQuiet, MSGBOX_DEFAULT
	release
	end

IlexForest_EventScript_ShrineDone::
	msgbox IlexForest_Text_ShrineDone, MSGBOX_DEFAULT
	release
	end

IlexForest_EventScript_Sign::
	msgbox IlexForest_Text_Sign, MSGBOX_SIGN
	end

@ ---------------------------------------------------------------- teksten (placeholders, Jordi herschrijft ze)
IlexForest_Text_ShrineCall:
	.string "A small stone CELEBI on a mossy\n"
	.string "pedestal. CALYREX said to call it. You\l"
	.string "feel silly. You call it anyway. The\l"
	.string "forest goes quiet. Then: a chime.$"

IlexForest_Text_Celebi:
	.string "CELEBI looks at you as if it has seen\n"
	.string "this moment before. Several times. It\l"
	.string "did not like how most of them ended.$"

IlexForest_Text_CelebiReset:
	.string "The world folds back on itself.\n"
	.string "Somewhere far away, CALYREX sighs and\l"
	.string "rewinds time by a few minutes. CELEBI is\l"
	.string "still here. Try again. Gently. With a ball.$"

IlexForest_Text_CelebiCaught:
	.string "CELEBI is yours. The forest exhales. Go\n"
	.string "back to the NATIONAL PARK: CALYREX is\l"
	.string "waiting.$"

IlexForest_Text_ShrineQuiet:
	.string "A small stone CELEBI on a mossy\n"
	.string "pedestal. Someone left a sandwich as an\l"
	.string "offering. It looks suspiciously\l"
	.string "familiar.$"

IlexForest_Text_ShrineDone:
	.string "The shrine is empty now. The sandwich is\n"
	.string "gone too. Nobody saw who took it.$"

IlexForest_Text_Sign:
	.string "ILEX FOREST\n"
	.string "The forest is said to be protected by a\l"
	.string "time-travelling spirit.\l"
	.string "Please do not walk in circles. It is rude.$"
