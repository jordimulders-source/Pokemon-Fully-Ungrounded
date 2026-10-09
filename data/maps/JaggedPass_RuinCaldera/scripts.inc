JaggedPass_RuinCaldera_MapScripts::
	.byte 0

@ Project Grounded: verzegelde ChiYu (Beasts of Ruin, tools/grounded/maptools/ruin_beasts.py). Na de Hall of Fame
@ breken de zegels pas als alle vier de schrijnen bezocht zijn (RuinBeasts_EventScript_CheckSeals).
RuinBeasts_EventScript_CHI_YU::
	lock
	setflag FLAG_RUIN_SEAL_CHI_YU
	goto_if_unset FLAG_SYS_GAME_CLEAR, JaggedPass_RuinCaldera_EventScript_Sealed
	call RuinBeasts_EventScript_CheckSeals
	goto_if_eq VAR_RESULT, FALSE, JaggedPass_RuinCaldera_EventScript_Stays
	playmoncry SPECIES_CHI_YU, CRY_MODE_ENCOUNTER
	waitmoncry
	setwildbattle SPECIES_CHI_YU, 70
	setflag FLAG_SYS_CTRL_OBJ_DELETE
	special BattleSetup_StartLegendaryBattle
	waitstate
	clearflag FLAG_SYS_CTRL_OBJ_DELETE
	specialvar VAR_RESULT, GetBattleOutcome
	goto_if_eq VAR_RESULT, B_OUTCOME_RAN, JaggedPass_RuinCaldera_EventScript_Stays
	goto_if_eq VAR_RESULT, B_OUTCOME_PLAYER_TELEPORTED, JaggedPass_RuinCaldera_EventScript_Stays
	removeobject LOCALID_RUIN_CHI_YU
	setflag FLAG_HIDE_RUIN_CHI_YU
JaggedPass_RuinCaldera_EventScript_Stays::
	release
	end

JaggedPass_RuinCaldera_EventScript_Sealed::
	msgbox JaggedPass_RuinCaldera_Text_Sealed, MSGBOX_DEFAULT
	release
	end

JaggedPass_RuinCaldera_EventScript_Stake::
	msgbox JaggedPass_RuinCaldera_Text_Stake, MSGBOX_SIGN
	end

JaggedPass_RuinCaldera_Text_Sealed:
	.string "A fish made of fire hangs in the air,\n"
	.string "perfectly still. The heat doesn't\l"
	.string "flicker. It waits.\p"
	.string "Four stakes pin its shadow to the\n"
	.string "ground. The air smells of melted jade\l"
	.string "beads.\p"
	.string "It does not look at you. You are not\n"
	.string "important enough. Yet.$"

JaggedPass_RuinCaldera_Text_Stake:
	.string "“HERE THE BEADS ARE KEPT. THEY WANTED\n"
	.string "EVERYTHING TO BURN, SO THEY BURN\l"
	.string "FOREVER.”\p"
	.string "Underneath, scratched in later: “bring\n"
	.string "marshmallows. do not bring the\l"
	.string "marshmallows back.”$"
