MtPyre_1F_MapScripts::
	.byte 0

MtPyre_1F_EventScript_CleanseTagWoman::
	lock
	faceplayer
	goto_if_set FLAG_RECEIVED_CLEANSE_TAG, MtPyre_1F_EventScript_ReceivedCleanseTag
	msgbox MtPyre_1F_Text_TakeThisForYourOwnGood, MSGBOX_DEFAULT
	giveitem ITEM_CLEANSE_TAG
	goto_if_eq VAR_RESULT, FALSE, Common_EventScript_ShowBagIsFull
	setflag FLAG_RECEIVED_CLEANSE_TAG
	release
	end

MtPyre_1F_EventScript_ReceivedCleanseTag::
	msgbox MtPyre_1F_Text_ExplainCleanseTag, MSGBOX_DEFAULT
	release
	end

MtPyre_1F_EventScript_PokefanF::
	msgbox MtPyre_1F_Text_ComeToPayRespects, MSGBOX_NPC
	end

MtPyre_1F_EventScript_Man::
	msgbox MtPyre_1F_Text_RestingPlaceOfZigzagoon, MSGBOX_NPC
	end

MtPyre_1F_Text_TakeThisForYourOwnGood:
	.string "All sorts of beings wander MT. PYRE…\p"
	.string "Anything can happen. Take this. For\n"
	.string "your own good.$"

MtPyre_1F_Text_ExplainCleanseTag:
	.string "Let a POKéMON hold that CLEANSE TAG.\p"
	.string "It keeps wild POKéMON away.\p"
	.string "Ghosts too. Mostly.$"

MtPyre_1F_Text_ComeToPayRespects:
	.string "Did you come to honor the spirits of\n"
	.string "departed POKéMON?\p"
	.string "You must love your POKéMON.\p"
	.string "Or you're lost. Either is fine.$"

MtPyre_1F_Text_RestingPlaceOfZigzagoon:
	.string "This is the final resting place of my\n"
	.string "RATICATE.\p"
	.string "It fell in battle against some kid from\n"
	.string "PALLET TOWN.\p"
	.string "… … … … … …\p"
	.string "Smell ya later, buddy.$"

@ extra_fights { (tools/grounded/maptools/extra_fights.py)
MtPyre_1F_EventScript_EF_WallyMtPyre::
	trainerbattle_single TRAINER_WALLY_MT_PYRE, MtPyre_1F_Text_EF_WallyMtPyreIntro, MtPyre_1F_Text_EF_WallyMtPyreDefeat, MtPyre_1F_EventScript_EF_WallyMtPyreDefeated
	msgbox MtPyre_1F_Text_EF_WallyMtPyrePostBattle, MSGBOX_AUTOCLOSE
	end

MtPyre_1F_EventScript_EF_WallyMtPyreDefeated::
	msgbox MtPyre_1F_Text_EF_WallyMtPyrePostBattle, MSGBOX_DEFAULT
	closemessage
	fadescreen FADE_TO_BLACK
	removeobject LOCALID_EF_WALLY_MT_PYRE
	fadescreen FADE_FROM_BLACK
	release
	end

MtPyre_1F_Text_EF_WallyMtPyreIntro:
	.string "WALLY: {PLAYER}! Mountain of grave!\p"
	.string "Scare no much, horror watching\n"
	.string "when young many.\p"
	.string "Ghost now is friend team.\n"
	.string "Boo! You scare? I no scare.$"

MtPyre_1F_Text_EF_WallyMtPyreDefeat:
	.string "Aaah! Now real scare…$"

MtPyre_1F_Text_EF_WallyMtPyrePostBattle:
	.string "WALLY: Horror rule number one:\n"
	.string "never split up.\p"
	.string "…I split up from you now.\n"
	.string "Not scare. Is cardio.$"

@ }
