JaggedPass_RuinChamber_MapScripts::
	.byte 0

@ Project Grounded: kamer bovenin Jagged Pass, leidt naar het lavaveld van Chi-Yu (Beasts of Ruin)
JaggedPass_RuinChamber_EventScript_Stake::
	msgbox JaggedPass_RuinChamber_Text_Stake, MSGBOX_SIGN
	end

@ Gedeeld door de vier schrijnen. VAR_RESULT = TRUE als alle vier bezocht zijn (dan breekt de zegel),
@ anders een hint per schrijn die nog niet bezocht is.
@ Sinds v0.9.171 zijn de ingangen zelf verzegeld tot je de Sealbreaker hebt (oude echtpaar, Mt. Pyre); binnen vecht
@ het beest dus meteen. RuinBeasts_EventScript_NotAll en de hints blijven voor de Dialoogstudio staan.
RuinBeasts_EventScript_CheckSeals::
	setvar VAR_RESULT, TRUE
	return

RuinBeasts_EventScript_CheckSealsOld::
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

RuinBeasts_EventScript_SealChiYu::
	lock
	checkitem ITEM_SEALBREAKER
	goto_if_eq VAR_RESULT, FALSE, RuinBeasts_EventScript_SealLocked
	msgbox RuinBeasts_Text_SealBreaks, MSGBOX_DEFAULT
	closemessage
	playse SE_M_REFLECT
	waitse
	removeobject VAR_LAST_TALKED
	setflag FLAG_RUIN_SEAL_OPEN_CHI_YU
	release
	end

RuinBeasts_EventScript_SealTingLu::
	lock
	checkitem ITEM_SEALBREAKER
	goto_if_eq VAR_RESULT, FALSE, RuinBeasts_EventScript_SealLocked
	msgbox RuinBeasts_Text_SealBreaks, MSGBOX_DEFAULT
	closemessage
	playse SE_M_REFLECT
	waitse
	removeobject VAR_LAST_TALKED
	setflag FLAG_RUIN_SEAL_OPEN_TING_LU
	release
	end

RuinBeasts_EventScript_SealWoChien::
	lock
	checkitem ITEM_SEALBREAKER
	goto_if_eq VAR_RESULT, FALSE, RuinBeasts_EventScript_SealLocked
	msgbox RuinBeasts_Text_SealBreaks, MSGBOX_DEFAULT
	closemessage
	playse SE_M_REFLECT
	waitse
	removeobject VAR_LAST_TALKED
	setflag FLAG_RUIN_SEAL_OPEN_WO_CHIEN
	release
	end

RuinBeasts_EventScript_SealChienPao::
	lock
	checkitem ITEM_SEALBREAKER
	goto_if_eq VAR_RESULT, FALSE, RuinBeasts_EventScript_SealLocked
	msgbox RuinBeasts_Text_SealBreaks, MSGBOX_DEFAULT
	closemessage
	playse SE_M_REFLECT
	waitse
	removeobject VAR_LAST_TALKED
	setflag FLAG_RUIN_SEAL_OPEN_CHIEN_PAO
	release
	end

RuinBeasts_EventScript_SealLocked::
	msgbox RuinBeasts_Text_SealLocked, MSGBOX_DEFAULT
	goto_if_unset FLAG_SYS_GAME_CLEAR, RuinBeasts_EventScript_SealLockedEnd
	msgbox RuinBeasts_Text_SealLockedHint, MSGBOX_DEFAULT
RuinBeasts_EventScript_SealLockedEnd::
	release
	end

RuinBeasts_Text_SealLocked:
	.string "A stake is driven into the entrance,\n"
	.string "wrapped in a paper seal.\p"
	.string "Something on the other side is\n"
	.string "breathing very slowly. And patiently.$"

RuinBeasts_Text_SealLockedHint:
	.string "The seal smells faintly of incense.\n"
	.string "The same incense as on MT. PYRE…$"

RuinBeasts_Text_SealBreaks:
	.string "The SEALBREAKER grows warm.\p"
	.string "The paper seal curls up and turns\n"
	.string "to ash. The stake splits in two.\p"
	.string "Whatever was waiting in there\n"
	.string "has stopped waiting.$"
