RustboroCity_House2_MapScripts::
	.byte 0

@ Project Grounded: eenmalige item-giveaway (testrun Jordi)
RustboroCity_House2_EventScript_PokefanF::
	lock
	faceplayer
	msgbox RustboroCity_House2_Text_TrainerSchoolExcellent, MSGBOX_DEFAULT
	goto_if_set FLAG_RECEIVED_RUSTBORO_HOUSE2_GIFT, RustboroCity_House2_EventScript_PokefanF_GiftDone
	msgbox RustboroCity_House2_Text_TakeWideLens, MSGBOX_DEFAULT
	giveitem ITEM_WIDE_LENS
	goto_if_eq VAR_RESULT, FALSE, Common_EventScript_ShowBagIsFull
	setflag FLAG_RECEIVED_RUSTBORO_HOUSE2_GIFT
RustboroCity_House2_EventScript_PokefanF_GiftDone::
	release
	end

RustboroCity_House2_EventScript_LittleGirl::
	msgbox RustboroCity_House2_Text_RoxanneKnowsALot, MSGBOX_NPC
	end

RustboroCity_House2_Text_TrainerSchoolExcellent:
	.string "The TRAINER'S SCHOOL is excellent.\p"
	.string "If you study there, you could become a\n"
	.string "GYM LEADER.\p"
	.string "My son wants to be an influencer.$"

RustboroCity_House2_Text_RoxanneKnowsALot:
	.string "ROXANNE knows so much about POKéMON!\p"
	.string "She's a rock star!$"

RustboroCity_House2_Text_TakeWideLens:
	.string "He bought this WIDE LENS for his\n"
	.string "“content”. Then he got bored.\p"
	.string "It helps moves hit. Unlike his\n"
	.string "videos. Take it before he notices.$"
