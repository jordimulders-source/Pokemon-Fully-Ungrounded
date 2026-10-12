DesertUnderpass_RuinShrine_MapScripts::
	.byte 0

@ Project Grounded: verzegelde TingLu (Beasts of Ruin, tools/grounded/maptools/ruin_beasts.py). Na de Hall of Fame
@ breken de zegels pas als alle vier de schrijnen bezocht zijn (RuinBeasts_EventScript_CheckSeals).
RuinBeasts_EventScript_TING_LU::
	lock
	setflag FLAG_RUIN_SEAL_TING_LU
	goto_if_unset FLAG_SYS_GAME_CLEAR, DesertUnderpass_RuinShrine_EventScript_Sealed
	call RuinBeasts_EventScript_CheckSeals
	goto_if_eq VAR_RESULT, FALSE, DesertUnderpass_RuinShrine_EventScript_Stays
	playmoncry SPECIES_TING_LU, CRY_MODE_ENCOUNTER
	waitmoncry
	setwildbattle SPECIES_TING_LU, 93
	setflag FLAG_SYS_CTRL_OBJ_DELETE
	special BattleSetup_StartLegendaryBattle
	waitstate
	clearflag FLAG_SYS_CTRL_OBJ_DELETE
	specialvar VAR_RESULT, GetBattleOutcome
	goto_if_eq VAR_RESULT, B_OUTCOME_RAN, DesertUnderpass_RuinShrine_EventScript_Stays
	goto_if_eq VAR_RESULT, B_OUTCOME_PLAYER_TELEPORTED, DesertUnderpass_RuinShrine_EventScript_Stays
	removeobject LOCALID_RUIN_TING_LU
	setflag FLAG_HIDE_RUIN_TING_LU
DesertUnderpass_RuinShrine_EventScript_Stays::
	release
	end

DesertUnderpass_RuinShrine_EventScript_Sealed::
	msgbox DesertUnderpass_RuinShrine_Text_Sealed, MSGBOX_DEFAULT
	release
	end

DesertUnderpass_RuinShrine_EventScript_Stake::
	msgbox DesertUnderpass_RuinShrine_Text_Stake, MSGBOX_SIGN
	end

DesertUnderpass_RuinShrine_Text_Sealed:
	.string "A huge shape of earth and bronze sits\n"
	.string "with its head bowed, like it's carrying\l"
	.string "the whole desert.\p"
	.string "Four stakes are driven into the sand\n"
	.string "around it. The ground hums.\p"
	.string "It has been waiting a thousand years.\n"
	.string "It can wait a little longer.$"

DesertUnderpass_RuinShrine_Text_Stake:
	.string "“HERE THE VESSELS ARE KEPT. IT DRANK\n"
	.string "THE LAND DRY AND CALLED IT A HARVEST.”\p"
	.string "Someone scratched underneath: “tried\n"
	.string "to dig it out. do not dig it out.”$"
