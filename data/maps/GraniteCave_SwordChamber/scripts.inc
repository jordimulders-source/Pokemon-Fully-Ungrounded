@ Project Grounded: Swords of Justice (tools/grounded/maptools/swords_keldeo.py). Verborgen kamer achter een
@ Rock Smash-rots in Granite Cave B2F; Cobalion (lv 70) staat er pas na de Hall of Fame.
GraniteCave_SwordChamber_MapScripts::
	map_script MAP_SCRIPT_ON_TRANSITION, GraniteCave_SwordChamber_OnTransition
	.byte 0

GraniteCave_SwordChamber_OnTransition:
	call_if_unset FLAG_SYS_GAME_CLEAR, SwordsOfJustice_EventScript_HideSword
	call_if_set FLAG_DEFEATED_COBALION, SwordsOfJustice_EventScript_HideSword
	end

GraniteCave_SwordChamber_EventScript_Cobalion::
	lock
	msgbox GraniteCave_SwordChamber_Text_Cobalion, MSGBOX_DEFAULT
	closemessage
	playmoncry SPECIES_COBALION, CRY_MODE_ENCOUNTER
	waitmoncry
	setwildbattle SPECIES_COBALION, 70
	setflag FLAG_SYS_CTRL_OBJ_DELETE
	special BattleSetup_StartLegendaryBattle
	waitstate
	clearflag FLAG_SYS_CTRL_OBJ_DELETE
	specialvar VAR_RESULT, GetBattleOutcome
	goto_if_eq VAR_RESULT, B_OUTCOME_RAN, SwordsOfJustice_EventScript_SwordStays
	goto_if_eq VAR_RESULT, B_OUTCOME_PLAYER_TELEPORTED, SwordsOfJustice_EventScript_SwordStays
	removeobject LOCALID_GRANITE_CAVE_SWORD_CHAMBER_COBALION
	setflag FLAG_DEFEATED_COBALION
	goto SwordsOfJustice_EventScript_AfterSword
	end

GraniteCave_SwordChamber_Text_Cobalion:
	.string "A steel-blue stag stands perfectly\n"
	.string "still, like a statue of a statue.\p"
	.string "It looks at you the way a headmaster\n"
	.string "looks at a forged signature.\p"
	.string "It has clearly seen how you name\n"
	.string "your PC boxes. It is not impressed.$"
