@ Project Grounded: AreaZero_TeraCave (tools/grounded/maptools/area_zero.py)
AreaZero_TeraCave_MapScripts::
	map_script MAP_SCRIPT_ON_TRANSITION, AreaZero_TeraCave_OnTransition
	.byte 0

AreaZero_TeraCave_OnTransition:
	setflag FLAG_TEMP_1
	goto_if_set FLAG_SPACETIME_AREAZERO_DONE, AreaZero_TeraCave_EventScript_TransEnd
	checktrainerflag TRAINER_AREA_ZERO_ALARM
	goto_if FALSE, AreaZero_TeraCave_EventScript_TransEnd
	clearflag FLAG_TEMP_1
AreaZero_TeraCave_EventScript_TransEnd:
	end

AreaZero_TeraCave_EventScript_Alarm::
	lock
	goto_if_defeated TRAINER_AREA_ZERO_ALARM, AreaZero_TeraCave_EventScript_AlarmOff
	msgbox AreaZero_TeraCave_Text_AlarmIntro, MSGBOX_DEFAULT
	trainerbattle_no_intro TRAINER_AREA_ZERO_ALARM, AreaZero_TeraCave_Text_AlarmDefeat
	playse SE_THUNDERSTORM_STOP
	msgbox AreaZero_TeraCave_Text_Freed, MSGBOX_DEFAULT
	clearflag FLAG_TEMP_1
	addobject LOCALID_AREA_ZERO_TERAPAGOS
	playmoncry SPECIES_TERAPAGOS, CRY_MODE_NORMAL
	waitmoncry
	release
	end

AreaZero_TeraCave_EventScript_AlarmOff::
	msgbox AreaZero_TeraCave_Text_AlarmOff, MSGBOX_DEFAULT
	release
	end

AreaZero_TeraCave_EventScript_Terapagos::
	lock
	faceplayer
	playmoncry SPECIES_TERAPAGOS, CRY_MODE_ENCOUNTER
	msgbox AreaZero_TeraCave_Text_Terapagos, MSGBOX_DEFAULT
	waitmoncry
	closemessage
	setwildbattle SPECIES_TERAPAGOS, 100
	special BattleSetup_StartLegendaryBattle
	waitstate
	specialvar VAR_RESULT, GetBattleOutcome
	goto_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, AreaZero_TeraCave_EventScript_TerapagosCaught
	goto_if_eq VAR_RESULT, B_OUTCOME_WON, AreaZero_TeraCave_EventScript_TerapagosBack
	release
	end

AreaZero_TeraCave_EventScript_TerapagosBack::
	msgbox AreaZero_TeraCave_Text_TerapagosBack, MSGBOX_DEFAULT
	release
	end

AreaZero_TeraCave_EventScript_TerapagosCaught::
	removeobject LOCALID_AREA_ZERO_TERAPAGOS
	setflag FLAG_SPACETIME_AREAZERO_DONE
	msgbox AreaZero_TeraCave_Text_Done, MSGBOX_DEFAULT
	release
	end


@ ---------------------------------------------------------------- teksten (placeholders, Jordi herschrijft ze)
AreaZero_TeraCave_Text_AlarmIntro:
	.string "ALARM SYSTEM. THE LAST ONE. THE LOUD\n"
	.string "ONE.\p"
	.string "YOU HAVE DISABLED TWO SECURITY\n"
	.string "SYSTEMS. THAT WAS VERY RUDE.\p"
	.string "ENGAGING TERASTAL PROTOCOL. EVERY.\n"
	.string "SINGLE. ONE.$"

AreaZero_TeraCave_Text_AlarmDefeat:
	.string "ALARM... SNOOZED.$"

AreaZero_TeraCave_Text_Freed:
	.string "The alarm whines down to silence.\p"
	.string "The great crystal at the back of the\n"
	.string "cave cracks, and something small and\l"
	.string "shell-shaped blinks at the light for\l"
	.string "the first time in a very long time.$"

AreaZero_TeraCave_Text_AlarmOff:
	.string "ALARM SYSTEM: OFFLINE.\n"
	.string "Somebody has drawn a frowny face on\l"
	.string "the screen. From the inside.$"

AreaZero_TeraCave_Text_Terapagos:
	.string "TERAPAGOS looks at you, then at the\n"
	.string "dead alarm, then back at you.\p"
	.string "It seems grateful. It also seems like a\n"
	.string "nuclear reactor shaped like a turtle.$"

AreaZero_TeraCave_Text_TerapagosBack:
	.string "TERAPAGOS retreats into its shell and\n"
	.string "quietly re-crystallises. It's fine. It\l"
	.string "has done this for a few thousand years.$"

AreaZero_TeraCave_Text_Done:
	.string "TERAPAGOS is yours.\p"
	.string "AREA ZERO falls quiet: past, future and\n"
	.string "present, all minding their own business\l"
	.string "for once.$"
