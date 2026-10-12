RegidragoCave_MapScripts::
	map_script MAP_SCRIPT_ON_RESUME, RegidragoCave_OnResume
	map_script MAP_SCRIPT_ON_LOAD, RegidragoCave_OnLoad
	map_script MAP_SCRIPT_ON_TRANSITION, RegidragoCave_OnTransition
	.byte 0

@ Project Grounded: Regidrago (stippenpuzzel, zie src/regi_dots.c en tools/grounded/maptools/regi_caves.py)
RegidragoCave_OnResume:
	call_if_set FLAG_SYS_CTRL_OBJ_DELETE, RegidragoCave_EventScript_TryRemoveRegidrago
	end

RegidragoCave_EventScript_TryRemoveRegidrago::
	specialvar VAR_RESULT, GetBattleOutcome
	goto_if_ne VAR_RESULT, B_OUTCOME_CAUGHT, Common_EventScript_NopReturn
	removeobject VAR_LAST_TALKED
	return

RegidragoCave_OnTransition:
	setflag FLAG_HIDE_REGIDRAGO
	call_if_unset FLAG_DEFEATED_REGIDRAGO, RegidragoCave_EventScript_ShowRegidrago
	end

RegidragoCave_EventScript_ShowRegidrago::
	clearflag FLAG_HIDE_REGIDRAGO
	return

RegidragoCave_OnLoad:
	special RegiDots_OnLoad
	call_if_unset FLAG_SYS_REGIDRAGO_PUZZLE_COMPLETED, RegidragoCave_EventScript_HideRegiEntrance
	end

RegidragoCave_EventScript_HideRegiEntrance::
	setmetatile 7, 19, METATILE_Cave_EntranceCover, TRUE
	setmetatile 8, 19, METATILE_Cave_EntranceCover, TRUE
	setmetatile 9, 19, METATILE_Cave_EntranceCover, TRUE
	setmetatile 7, 20, METATILE_Cave_SealedChamberBraille_Mid, TRUE
	setmetatile 8, 20, METATILE_Cave_SealedChamberBraille_Mid, TRUE
	setmetatile 9, 20, METATILE_Cave_SealedChamberBraille_Mid, TRUE
	return

RegidragoCave_EventScript_Regidrago::
	lock
	faceplayer
	waitse
	playmoncry SPECIES_REGIDRAGO, CRY_MODE_ENCOUNTER
	delay 40
	waitmoncry
	setwildbattle SPECIES_REGIDRAGO, 73
	setflag FLAG_SYS_CTRL_OBJ_DELETE
	special StartRegiBattle
	waitstate
	clearflag FLAG_SYS_CTRL_OBJ_DELETE
	specialvar VAR_RESULT, GetBattleOutcome
	goto_if_eq VAR_RESULT, B_OUTCOME_WON, Common_EventScript_RegiCrumbled
	goto_if_eq VAR_RESULT, B_OUTCOME_RAN, RegidragoCave_EventScript_RanFromRegidrago
	goto_if_eq VAR_RESULT, B_OUTCOME_PLAYER_TELEPORTED, RegidragoCave_EventScript_RanFromRegidrago
	setflag FLAG_DEFEATED_REGIDRAGO
	call Common_EventScript_CheckRegigigasTemple
	release
	end

RegidragoCave_EventScript_RanFromRegidrago::
	setvar VAR_0x8004, SPECIES_REGIDRAGO
	goto Common_EventScript_LegendaryFlewAway
	end
