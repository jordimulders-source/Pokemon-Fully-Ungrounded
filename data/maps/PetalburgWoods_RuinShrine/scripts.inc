PetalburgWoods_RuinShrine_MapScripts::
	.byte 0

@ Project Grounded: verzegelde WoChien (Beasts of Ruin, tools/grounded/maptools/ruin_beasts.py). Na de Hall of Fame
@ breken de zegels pas als alle vier de schrijnen bezocht zijn (RuinBeasts_EventScript_CheckSeals).
RuinBeasts_EventScript_WO_CHIEN::
	lock
	setflag FLAG_RUIN_SEAL_WO_CHIEN
	goto_if_unset FLAG_SYS_GAME_CLEAR, PetalburgWoods_RuinShrine_EventScript_Sealed
	call RuinBeasts_EventScript_CheckSeals
	goto_if_eq VAR_RESULT, FALSE, PetalburgWoods_RuinShrine_EventScript_Stays
	playmoncry SPECIES_WO_CHIEN, CRY_MODE_ENCOUNTER
	waitmoncry
	setwildbattle SPECIES_WO_CHIEN, 70
	setflag FLAG_SYS_CTRL_OBJ_DELETE
	special BattleSetup_StartLegendaryBattle
	waitstate
	clearflag FLAG_SYS_CTRL_OBJ_DELETE
	specialvar VAR_RESULT, GetBattleOutcome
	goto_if_eq VAR_RESULT, B_OUTCOME_RAN, PetalburgWoods_RuinShrine_EventScript_Stays
	goto_if_eq VAR_RESULT, B_OUTCOME_PLAYER_TELEPORTED, PetalburgWoods_RuinShrine_EventScript_Stays
	removeobject LOCALID_RUIN_WO_CHIEN
	setflag FLAG_HIDE_RUIN_WO_CHIEN
PetalburgWoods_RuinShrine_EventScript_Stays::
	release
	end

PetalburgWoods_RuinShrine_EventScript_Sealed::
	msgbox PetalburgWoods_RuinShrine_Text_Sealed, MSGBOX_DEFAULT
	release
	end

PetalburgWoods_RuinShrine_EventScript_Stake::
	msgbox PetalburgWoods_RuinShrine_Text_Stake, MSGBOX_SIGN
	end

PetalburgWoods_RuinShrine_Text_Sealed:
	.string "A small snail of rotting leaves sits\n"
	.string "under the wooden tablets.\p"
	.string "The moss around it is grey and dead.\n"
	.string "Four stakes hold it in place.\p"
	.string "It's tiny. That is somehow the most\n"
	.string "frightening part.$"

PetalburgWoods_RuinShrine_Text_Stake:
	.string "“HERE THE TABLETS ARE KEPT. A KING'S\n"
	.string "GRUDGE, WRITTEN ON WOOD. THE FOREST\l"
	.string "READ IT AND DIED.”\p"
	.string "Below it, in fresh pen: “the BUG\n"
	.string "CATCHERS do not come here. ask them\l"
	.string "why. they cry.”$"
