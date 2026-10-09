JaggedPass_RuinChamber_MapScripts::
	.byte 0

@ Project Grounded: kamer bovenin Jagged Pass, leidt naar het lavaveld van Chi-Yu (Beasts of Ruin)
JaggedPass_RuinChamber_EventScript_Stake::
	msgbox JaggedPass_RuinChamber_Text_Stake, MSGBOX_SIGN
	end

@ Gedeeld door de vier schrijnen. VAR_RESULT = TRUE als alle vier bezocht zijn (dan breekt de zegel),
@ anders een hint per schrijn die nog niet bezocht is.
RuinBeasts_EventScript_CheckSeals::
	goto_if_unset FLAG_RUIN_SEAL_CHI_YU, RuinBeasts_EventScript_NotAll
	goto_if_unset FLAG_RUIN_SEAL_TING_LU, RuinBeasts_EventScript_NotAll
	goto_if_unset FLAG_RUIN_SEAL_WO_CHIEN, RuinBeasts_EventScript_NotAll
	goto_if_unset FLAG_RUIN_SEAL_CHIEN_PAO, RuinBeasts_EventScript_NotAll
	msgbox RuinBeasts_Text_SealsBreak, MSGBOX_DEFAULT
	closemessage
	setvar VAR_RESULT, TRUE
	return

RuinBeasts_EventScript_NotAll::
	msgbox RuinBeasts_Text_SealRattles, MSGBOX_DEFAULT
	call_if_unset FLAG_RUIN_SEAL_CHI_YU, RuinBeasts_EventScript_HintChiYu
	call_if_unset FLAG_RUIN_SEAL_TING_LU, RuinBeasts_EventScript_HintTingLu
	call_if_unset FLAG_RUIN_SEAL_WO_CHIEN, RuinBeasts_EventScript_HintWoChien
	call_if_unset FLAG_RUIN_SEAL_CHIEN_PAO, RuinBeasts_EventScript_HintChienPao
	setvar VAR_RESULT, FALSE
	return

RuinBeasts_EventScript_HintChiYu::
	msgbox RuinBeasts_Text_HintChiYu, MSGBOX_DEFAULT
	return

RuinBeasts_EventScript_HintTingLu::
	msgbox RuinBeasts_Text_HintTingLu, MSGBOX_DEFAULT
	return

RuinBeasts_EventScript_HintWoChien::
	msgbox RuinBeasts_Text_HintWoChien, MSGBOX_DEFAULT
	return

RuinBeasts_EventScript_HintChienPao::
	msgbox RuinBeasts_Text_HintChienPao, MSGBOX_DEFAULT
	return

JaggedPass_RuinChamber_Text_Stake:
	.string "Words are carved into the stake:\p"
	.string "“FOUR TREASURES OF RUIN. TABLETS.\n"
	.string "SWORD. VESSELS. BEADS.\p"
	.string "THOSE WHO TOUCHED THEM GREW ENVIOUS,\n"
	.string "CRUEL, GREEDY, AND VERY BAD AT PARTIES.\p"
	.string "THE STAKES HOLD THE FOUR. THE FOUR\n"
	.string "HOLD EACH OTHER. PULL ONE, AND NOTHING\l"
	.string "HAPPENS.”\p"
	.string "The heat comes from further in.$"

RuinBeasts_Text_SealsBreak:
	.string "The stakes crack. Far away, three other\n"
	.string "stakes crack with them.\p"
	.string "Somewhere a historian screams into a\n"
	.string "pillow.$"

RuinBeasts_Text_SealRattles:
	.string "The stakes rattle. The seal knows a\n"
	.string "CHAMPION when it sees one.\p"
	.string "But this seal is one of four, and the\n"
	.string "others still hold. It hums of places you\l"
	.string "haven't been...$"

RuinBeasts_Text_HintChiYu:
	.string "...a heat at the top of JAGGED PASS...$"

RuinBeasts_Text_HintTingLu:
	.string "...a weight deep beneath the desert\n"
	.string "sand...$"

RuinBeasts_Text_HintWoChien:
	.string "...a rot under the roots of the woods\n"
	.string "near PETALBURG...$"

RuinBeasts_Text_HintChienPao:
	.string "...a cold behind a cliff of snow, far to\n"
	.string "the north...$"
