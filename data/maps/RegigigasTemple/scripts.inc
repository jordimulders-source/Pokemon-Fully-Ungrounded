RegigigasTemple_MapScripts::
	map_script MAP_SCRIPT_ON_RESUME, RegigigasTemple_OnResume
	map_script MAP_SCRIPT_ON_TRANSITION, RegigigasTemple_OnTransition
	.byte 0

@ Project Grounded: de Regigigas-tempel onder de iglo van Ashfrost (open als alle vijf Regi's gevangen zijn)
RegigigasTemple_OnResume:
	call_if_set FLAG_SYS_CTRL_OBJ_DELETE, RegigigasTemple_EventScript_TryRemoveRegigigas
	end

RegigigasTemple_EventScript_TryRemoveRegigigas::
	specialvar VAR_RESULT, GetBattleOutcome
	goto_if_ne VAR_RESULT, B_OUTCOME_CAUGHT, Common_EventScript_NopReturn
	removeobject VAR_LAST_TALKED
	return

RegigigasTemple_OnTransition:
	call_if_unset FLAG_REGIGIGAS_TEMPLE_OPEN, RegigigasTemple_EventScript_Seal
	setflag FLAG_HIDE_REGIGIGAS
	call_if_unset FLAG_DEFEATED_REGIGIGAS, RegigigasTemple_EventScript_ShowRegigigas
	end

@ zolang niet alle vijf Regi's gevangen zijn, staat er een ijsmuur voor Regigigas (regigigas_temple.py)
RegigigasTemple_EventScript_Seal::
	setmaplayoutindex LAYOUT_REGIGIGAS_TEMPLE_SEALED
	return

RegigigasTemple_EventScript_IceWall::
	goto_if_set FLAG_REGIGIGAS_TEMPLE_OPEN, RegigigasTemple_EventScript_IceWallGone
	msgbox RegigigasTemple_Text_IceWall, MSGBOX_SIGN
	end

RegigigasTemple_EventScript_IceWallGone::
	end

RegigigasTemple_EventScript_ShowRegigigas::
	clearflag FLAG_HIDE_REGIGIGAS
	return

RegigigasTemple_EventScript_Regigigas::
	lock
	faceplayer
	msgbox RegigigasTemple_Text_Regigigas, MSGBOX_DEFAULT
	closemessage
	waitse
	playmoncry SPECIES_REGIGIGAS, CRY_MODE_ENCOUNTER
	delay 40
	waitmoncry
	setwildbattle SPECIES_REGIGIGAS, 93
	setflag FLAG_SYS_CTRL_OBJ_DELETE
	special StartRegiBattle
	waitstate
	clearflag FLAG_SYS_CTRL_OBJ_DELETE
	specialvar VAR_RESULT, GetBattleOutcome
	goto_if_eq VAR_RESULT, B_OUTCOME_WON, Common_EventScript_RegiCrumbled
	goto_if_eq VAR_RESULT, B_OUTCOME_RAN, RegigigasTemple_EventScript_Ran
	goto_if_eq VAR_RESULT, B_OUTCOME_PLAYER_TELEPORTED, RegigigasTemple_EventScript_Ran
	setflag FLAG_DEFEATED_REGIGIGAS
	release
	end

RegigigasTemple_EventScript_Ran::
	setvar VAR_0x8004, SPECIES_REGIGIGAS
	goto Common_EventScript_LegendaryFlewAway
	end

RegigigasTemple_Text_Regigigas:
	.string "An enormous POKéMON sits frozen in\n"
	.string "place. Five sets of glowing dots flicker\l"
	.string "across its body...\p"
	.string "Rock, ice, steel, electricity and dragon.\n"
	.string "Everything it once made, it now wants\l"
	.string "back.$"

RegigigasTemple_Text_IceWall:
	.string "A wall of ice that will not melt. Five\n"
	.string "hollows are pressed into it, each the\l"
	.string "size of a giant's fist.\p"
	.string "“Rock from the sand. Ice from the sea.\n"
	.string "Steel from the rain.”\p"
	.string "“Lightning from under the road where\n"
	.string "the bicycles fly. Dragon from the speck\l"
	.string "of land east of the tower that touches\l"
	.string "the sky.”\p"
	.string "“Gather all five, and the one who made\n"
	.string "them will open its eyes.”$"
