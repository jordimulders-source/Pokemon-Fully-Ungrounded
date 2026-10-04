NewMauville_ServerVault_MapScripts::
	.byte 0

@ Project Grounded: Genesect in de serverkluis achter de Raikou-grot (post-game, deur via de terminal in de Raikou-grot)
NewMauville_ServerVault_EventScript_Genesect::
	lock
	faceplayer
	msgbox NewMauville_ServerVault_Text_TargetAcquired, MSGBOX_DEFAULT
	closemessage
	playmoncry SPECIES_GENESECT, CRY_MODE_ENCOUNTER
	waitmoncry
	setwildbattle SPECIES_GENESECT, 70
	setflag FLAG_SYS_CTRL_OBJ_DELETE
	special BattleSetup_StartLegendaryBattle
	waitstate
	clearflag FLAG_SYS_CTRL_OBJ_DELETE
	specialvar VAR_RESULT, GetBattleOutcome
	goto_if_eq VAR_RESULT, B_OUTCOME_RAN, NewMauville_ServerVault_EventScript_GenesectStays
	goto_if_eq VAR_RESULT, B_OUTCOME_PLAYER_TELEPORTED, NewMauville_ServerVault_EventScript_GenesectStays
	removeobject LOCALID_SERVER_VAULT_GENESECT
	setflag FLAG_HIDE_NEW_MAUVILLE_GENESECT
NewMauville_ServerVault_EventScript_GenesectStays::
	release
	end

NewMauville_ServerVault_EventScript_Server1::
	msgbox NewMauville_ServerVault_Text_Server1, MSGBOX_SIGN
	end

NewMauville_ServerVault_EventScript_Server2::
	msgbox NewMauville_ServerVault_Text_Server2, MSGBOX_SIGN
	end

NewMauville_ServerVault_Text_TargetAcquired:
	.string "Every screen in the room turns red.\p"
	.string "TARGET ACQUIRED.\n"
	.string "TARGET: YOU.\p"
	.string "HASTA LA VISTA, BABY.$"

NewMauville_ServerVault_Text_Server1:
	.string "A server rack, humming happily.\p"
	.string "Someone taped a note to it:\n"
	.string "“DO NOT FEED THE BUG. IT ATE THE\l"
	.string "INTERN.”$"

NewMauville_ServerVault_Text_Server2:
	.string "A file is open on the screen:\n"
	.string "GENESECT-FINAL-v2-REAL.EXE\p"
	.string "Last modified: 300 million years ago.\n"
	.string "Still not backed up.$"
