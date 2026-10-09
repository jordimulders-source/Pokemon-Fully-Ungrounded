@ Project Grounded: Swords of Justice (tools/grounded/maptools/swords_keldeo.py). Verborgen kamer achter een
@ Rock Smash-rots in Victory Road B2F; Terrakion (lv 70) staat er pas na de Hall of Fame.
VictoryRoad_SwordChamber_MapScripts::
	map_script MAP_SCRIPT_ON_TRANSITION, VictoryRoad_SwordChamber_OnTransition
	.byte 0

VictoryRoad_SwordChamber_OnTransition:
	call_if_unset FLAG_SYS_GAME_CLEAR, SwordsOfJustice_EventScript_HideSword
	call_if_set FLAG_DEFEATED_TERRAKION, SwordsOfJustice_EventScript_HideSword
	end

VictoryRoad_SwordChamber_EventScript_Terrakion::
	lock
	msgbox VictoryRoad_SwordChamber_Text_Terrakion, MSGBOX_DEFAULT
	closemessage
	playmoncry SPECIES_TERRAKION, CRY_MODE_ENCOUNTER
	waitmoncry
	setwildbattle SPECIES_TERRAKION, 70
	setflag FLAG_SYS_CTRL_OBJ_DELETE
	special BattleSetup_StartLegendaryBattle
	waitstate
	clearflag FLAG_SYS_CTRL_OBJ_DELETE
	specialvar VAR_RESULT, GetBattleOutcome
	goto_if_eq VAR_RESULT, B_OUTCOME_RAN, SwordsOfJustice_EventScript_SwordStays
	goto_if_eq VAR_RESULT, B_OUTCOME_PLAYER_TELEPORTED, SwordsOfJustice_EventScript_SwordStays
	removeobject LOCALID_VICTORY_ROAD_SWORD_CHAMBER_TERRAKION
	setflag FLAG_DEFEATED_TERRAKION
	goto SwordsOfJustice_EventScript_AfterSword
	end

VictoryRoad_SwordChamber_Text_Terrakion:
	.string "A huge stone bull paws at the floor.\n"
	.string "The floor files a complaint.\p"
	.string "Every trainer who ever walked past\n"
	.string "this wall on the way to the ELITE\l"
	.string "FOUR was being watched.\p"
	.string "Judged, too. Mostly on posture.$"
