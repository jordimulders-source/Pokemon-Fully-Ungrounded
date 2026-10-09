Route135_RuinShrine_MapScripts::
	.byte 0

@ Project Grounded: verzegelde ChienPao (Beasts of Ruin, tools/grounded/maptools/ruin_beasts.py). Na de Hall of Fame
@ breken de zegels pas als alle vier de schrijnen bezocht zijn (RuinBeasts_EventScript_CheckSeals).
RuinBeasts_EventScript_CHIEN_PAO::
	lock
	setflag FLAG_RUIN_SEAL_CHIEN_PAO
	goto_if_unset FLAG_SYS_GAME_CLEAR, Route135_RuinShrine_EventScript_Sealed
	call RuinBeasts_EventScript_CheckSeals
	goto_if_eq VAR_RESULT, FALSE, Route135_RuinShrine_EventScript_Stays
	playmoncry SPECIES_CHIEN_PAO, CRY_MODE_ENCOUNTER
	waitmoncry
	setwildbattle SPECIES_CHIEN_PAO, 93
	setflag FLAG_SYS_CTRL_OBJ_DELETE
	special BattleSetup_StartLegendaryBattle
	waitstate
	clearflag FLAG_SYS_CTRL_OBJ_DELETE
	specialvar VAR_RESULT, GetBattleOutcome
	goto_if_eq VAR_RESULT, B_OUTCOME_RAN, Route135_RuinShrine_EventScript_Stays
	goto_if_eq VAR_RESULT, B_OUTCOME_PLAYER_TELEPORTED, Route135_RuinShrine_EventScript_Stays
	removeobject LOCALID_RUIN_CHIEN_PAO
	setflag FLAG_HIDE_RUIN_CHIEN_PAO
Route135_RuinShrine_EventScript_Stays::
	release
	end

Route135_RuinShrine_EventScript_Sealed::
	msgbox Route135_RuinShrine_Text_Sealed, MSGBOX_DEFAULT
	release
	end

Route135_RuinShrine_EventScript_Stake::
	msgbox Route135_RuinShrine_Text_Stake, MSGBOX_SIGN
	end

Route135_RuinShrine_Text_Sealed:
	.string "A white cat crouches in the ice, two\n"
	.string "blades of frost for teeth.\p"
	.string "Four stakes stand around it like guards\n"
	.string "that forgot what they were guarding.\p"
	.string "It doesn't move. Your breath freezes\n"
	.string "anyway.$"

Route135_RuinShrine_Text_Stake:
	.string "“HERE THE SWORD IS KEPT. WHO HELD IT\n"
	.string "WANTED MORE, AND MORE, UNTIL THE SNOW\l"
	.string "CAME FOR THEM.”\p"
	.string "Someone scratched a smiley face next\n"
	.string "to it. The smiley is frowning.$"
