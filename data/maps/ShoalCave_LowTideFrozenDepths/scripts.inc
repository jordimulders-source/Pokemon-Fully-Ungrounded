@ Project Grounded: de ijzige onderlaag van Shoal Cave (bij eb). Layout: kopie van ColdstepCave_IceRoom2.
@ Kaart en scripts: tools/grounded/maptools/dungeon_extra.py.
ShoalCave_LowTideFrozenDepths_MapScripts::
	map_script MAP_SCRIPT_ON_TRANSITION, ShoalCave_LowTideFrozenDepths_Legends2_OnTransition
	.byte 0

ShoalCave_LowTideFrozenDepths_EventScript_Hole::
	msgbox ShoalCave_LowTideFrozenDepths_Text_Hole, MSGBOX_SIGN
	end

ShoalCave_LowTideFrozenDepths_EventScript_Tally::
	msgbox ShoalCave_LowTideFrozenDepths_Text_Tally, MSGBOX_SIGN
	end

@ ---------------------------------------------------------------- teksten (placeholders, Jordi herschrijft ze)
ShoalCave_LowTideFrozenDepths_Text_Hole:
	.string "A big CETODDLE-shaped hole in the ice\n"
	.string "wall.\p"
	.string "The CETODDLE that made it is nowhere to\n"
	.string "be seen. The hole looks very proud of\l"
	.string "itself.$"

ShoalCave_LowTideFrozenDepths_Text_Tally:
	.string "Tally marks scratched into the ice.\n"
	.string "Hundreds of them.\p"
	.string "At the very end:\n"
	.string "“DAY 412. THE TIDE CAME BACK. I DID\l"
	.string "NOT.”$"

@ --- legends2 (gegenereerd door tools/grounded/maptools/legends2.py) ---
ShoalCave_LowTideFrozenDepths_EventScript_Legends2_Transition:
	setflag FLAG_HIDE_LEGENDS_ARTICUNO
	goto_if_unset FLAG_SYS_GAME_CLEAR, ShoalCave_LowTideFrozenDepths_EventScript_Legends2_TransitionEnd
	goto_if_set FLAG_CAUGHT_KANTO_ARTICUNO, ShoalCave_LowTideFrozenDepths_EventScript_Legends2_TransitionEnd
	clearflag FLAG_HIDE_LEGENDS_ARTICUNO
ShoalCave_LowTideFrozenDepths_EventScript_Legends2_TransitionEnd:
	return

ShoalCave_LowTideFrozenDepths_EventScript_Articuno::
	lock
	faceplayer
	playmoncry SPECIES_ARTICUNO, CRY_MODE_ENCOUNTER
	msgbox ShoalCave_LowTideFrozenDepths_Text_Articuno, MSGBOX_DEFAULT
	waitmoncry
	closemessage
ShoalCave_LowTideFrozenDepths_EventScript_Articuno_Battle::
	setwildbattle SPECIES_ARTICUNO, 85
	setflag FLAG_SYS_CTRL_OBJ_DELETE
	special BattleSetup_StartLegendaryBattle
	waitstate
	clearflag FLAG_SYS_CTRL_OBJ_DELETE
	specialvar VAR_RESULT, GetBattleOutcome
	goto_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, ShoalCave_LowTideFrozenDepths_EventScript_Articuno_Caught
	goto_if_eq VAR_RESULT, B_OUTCOME_RAN, ShoalCave_LowTideFrozenDepths_EventScript_Articuno_Stays
	goto_if_eq VAR_RESULT, B_OUTCOME_PLAYER_TELEPORTED, ShoalCave_LowTideFrozenDepths_EventScript_Articuno_Stays
	removeobject LOCALID_LEGENDS_ARTICUNO
	setflag FLAG_HIDE_LEGENDS_ARTICUNO
	msgbox ShoalCave_LowTideFrozenDepths_Text_ArticunoFled, MSGBOX_DEFAULT
ShoalCave_LowTideFrozenDepths_EventScript_Articuno_Stays::
	release
	end

ShoalCave_LowTideFrozenDepths_EventScript_Articuno_Caught::
	removeobject LOCALID_LEGENDS_ARTICUNO
	setflag FLAG_HIDE_LEGENDS_ARTICUNO
	setflag FLAG_CAUGHT_KANTO_ARTICUNO
	call Legends2_EventScript_CheckGalarArrive
	release
	end

ShoalCave_LowTideFrozenDepths_Text_Articuno:
	.string "Kyaaah!\p"
	.string "(It has been sitting here so long the\n"
	.string "ice thinks it's furniture.)$"

ShoalCave_LowTideFrozenDepths_Text_ArticunoFled:
	.string "ARTICUNO shattered into a cloud of\n"
	.string "snow and was gone.\p"
	.string "It'll reassemble. It always does. Mostly\n"
	.string "out of spite.$"
@ --- einde legends2 ---

ShoalCave_LowTideFrozenDepths_Legends2_OnTransition:
	call ShoalCave_LowTideFrozenDepths_EventScript_Legends2_Transition
	end
