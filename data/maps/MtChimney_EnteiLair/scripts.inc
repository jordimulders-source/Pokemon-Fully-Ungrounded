MtChimney_EnteiLair_MapScripts::
	.byte 0

@ Project Grounded: Entei in de verborgen lavagrot onder Mt. Chimney
MtChimney_EnteiLair_EventScript_Entei::
	lock
	faceplayer
	playmoncry SPECIES_ENTEI, CRY_MODE_ENCOUNTER
	waitmoncry
	setwildbattle SPECIES_ENTEI, 62
	setflag FLAG_SYS_CTRL_OBJ_DELETE
	special BattleSetup_StartLegendaryBattle
	waitstate
	clearflag FLAG_SYS_CTRL_OBJ_DELETE
	specialvar VAR_RESULT, GetBattleOutcome
	goto_if_eq VAR_RESULT, B_OUTCOME_RAN, MtChimney_EnteiLair_EventScript_EnteiStays
	goto_if_eq VAR_RESULT, B_OUTCOME_PLAYER_TELEPORTED, MtChimney_EnteiLair_EventScript_EnteiStays
	removeobject LOCALID_MT_CHIMNEY_ENTEI
	setflag FLAG_HIDE_MT_CHIMNEY_ENTEI
MtChimney_EnteiLair_EventScript_EnteiStays::
	release
	end
