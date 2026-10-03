FieryPath_HeatranLair_MapScripts::
	.byte 0

@ Project Grounded: Heatran in de lavagrot onder Fiery Path (post-game, ingang linksboven in Fiery Path)
FieryPath_HeatranLair_EventScript_Heatran::
	lock
	faceplayer
	playmoncry SPECIES_HEATRAN, CRY_MODE_ENCOUNTER
	waitmoncry
	setwildbattle SPECIES_HEATRAN, 70
	setflag FLAG_SYS_CTRL_OBJ_DELETE
	special BattleSetup_StartLegendaryBattle
	waitstate
	clearflag FLAG_SYS_CTRL_OBJ_DELETE
	specialvar VAR_RESULT, GetBattleOutcome
	goto_if_eq VAR_RESULT, B_OUTCOME_RAN, FieryPath_HeatranLair_EventScript_HeatranStays
	goto_if_eq VAR_RESULT, B_OUTCOME_PLAYER_TELEPORTED, FieryPath_HeatranLair_EventScript_HeatranStays
	removeobject LOCALID_HEATRAN_LAIR_HEATRAN
	setflag FLAG_HIDE_FIERY_PATH_HEATRAN
FieryPath_HeatranLair_EventScript_HeatranStays::
	release
	end
