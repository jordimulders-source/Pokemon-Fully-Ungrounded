@ Project Grounded: Virizion-kamer (tools/grounded/maptools/swords_glade.py). Open plek achter de groene tunnel aan
@ het einde van het oostelijke zijpad van Mangrove Mire; Virizion (lv 70) staat er pas na de Hall of Fame.
MangroveMire_VirizionGlade_MapScripts::
	map_script MAP_SCRIPT_ON_TRANSITION, MangroveMire_VirizionGlade_OnTransition
	.byte 0

MangroveMire_VirizionGlade_OnTransition:
	call_if_unset FLAG_SYS_GAME_CLEAR, SwordsOfJustice_EventScript_HideSword
	call_if_set FLAG_DEFEATED_VIRIZION, SwordsOfJustice_EventScript_HideSword
	end

MangroveMire_VirizionGlade_EventScript_Virizion::
	lock
	msgbox MangroveMire_Text_Virizion, MSGBOX_DEFAULT
	closemessage
	playmoncry SPECIES_VIRIZION, CRY_MODE_ENCOUNTER
	waitmoncry
	setwildbattle SPECIES_VIRIZION, 70
	setflag FLAG_SYS_CTRL_OBJ_DELETE
	special BattleSetup_StartLegendaryBattle
	waitstate
	clearflag FLAG_SYS_CTRL_OBJ_DELETE
	specialvar VAR_RESULT, GetBattleOutcome
	goto_if_eq VAR_RESULT, B_OUTCOME_RAN, SwordsOfJustice_EventScript_SwordStays
	goto_if_eq VAR_RESULT, B_OUTCOME_PLAYER_TELEPORTED, SwordsOfJustice_EventScript_SwordStays
	removeobject LOCALID_VIRIZION_GLADE_VIRIZION
	setflag FLAG_DEFEATED_VIRIZION
	goto SwordsOfJustice_EventScript_AfterSword
	end

MangroveMire_VirizionGlade_EventScript_CutTree::
	msgbox MangroveMire_Text_CutTree, MSGBOX_SIGN
	end
