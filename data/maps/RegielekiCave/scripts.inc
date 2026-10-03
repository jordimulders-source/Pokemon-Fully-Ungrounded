RegielekiCave_MapScripts::
	map_script MAP_SCRIPT_ON_RESUME, RegielekiCave_OnResume
	map_script MAP_SCRIPT_ON_LOAD, RegielekiCave_OnLoad
	map_script MAP_SCRIPT_ON_TRANSITION, RegielekiCave_OnTransition
	.byte 0

@ Project Grounded: Regieleki (stippenpuzzel, zie src/regi_dots.c en tools/grounded/maptools/regi_caves.py)
RegielekiCave_OnResume:
	call_if_set FLAG_SYS_CTRL_OBJ_DELETE, RegielekiCave_EventScript_TryRemoveRegieleki
	end

RegielekiCave_EventScript_TryRemoveRegieleki::
	specialvar VAR_RESULT, GetBattleOutcome
	goto_if_ne VAR_RESULT, B_OUTCOME_CAUGHT, Common_EventScript_NopReturn
	removeobject VAR_LAST_TALKED
	return

RegielekiCave_OnTransition:
	setflag FLAG_HIDE_REGIELEKI
	call_if_unset FLAG_DEFEATED_REGIELEKI, RegielekiCave_EventScript_ShowRegieleki
	end

RegielekiCave_EventScript_ShowRegieleki::
	clearflag FLAG_HIDE_REGIELEKI
	return

RegielekiCave_OnLoad:
	special RegiDots_OnLoad
	call_if_unset FLAG_SYS_REGIELEKI_PUZZLE_COMPLETED, RegielekiCave_EventScript_HideRegiEntrance
	end

RegielekiCave_EventScript_HideRegiEntrance::
	setmetatile 7, 19, METATILE_Cave_EntranceCover, TRUE
	setmetatile 8, 19, METATILE_Cave_EntranceCover, TRUE
	setmetatile 9, 19, METATILE_Cave_EntranceCover, TRUE
	setmetatile 7, 20, METATILE_Cave_SealedChamberBraille_Mid, TRUE
	setmetatile 8, 20, METATILE_Cave_SealedChamberBraille_Mid, TRUE
	setmetatile 9, 20, METATILE_Cave_SealedChamberBraille_Mid, TRUE
	return

RegielekiCave_EventScript_Regieleki::
	lock
	faceplayer
	waitse
	playmoncry SPECIES_REGIELEKI, CRY_MODE_ENCOUNTER
	delay 40
	waitmoncry
	setwildbattle SPECIES_REGIELEKI, 50
	setflag FLAG_SYS_CTRL_OBJ_DELETE
	special StartRegiBattle
	waitstate
	clearflag FLAG_SYS_CTRL_OBJ_DELETE
	specialvar VAR_RESULT, GetBattleOutcome
	goto_if_eq VAR_RESULT, B_OUTCOME_WON, Common_EventScript_RegiCrumbled
	goto_if_eq VAR_RESULT, B_OUTCOME_RAN, RegielekiCave_EventScript_RanFromRegieleki
	goto_if_eq VAR_RESULT, B_OUTCOME_PLAYER_TELEPORTED, RegielekiCave_EventScript_RanFromRegieleki
	setflag FLAG_DEFEATED_REGIELEKI
	call Common_EventScript_CheckRegigigasTemple
	release
	end

RegielekiCave_EventScript_RanFromRegieleki::
	setvar VAR_0x8004, SPECIES_REGIELEKI
	goto Common_EventScript_LegendaryFlewAway
	end
