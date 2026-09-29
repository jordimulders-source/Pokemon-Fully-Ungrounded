RustboroCity_PokemonSchool_MapScripts::
	.byte 0

RustboroCity_PokemonSchool_EventScript_Blackboard::
	lockall
	msgbox RustboroCity_PokemonSchool_Text_BlackboardListsStatusChanges, MSGBOX_DEFAULT
	goto RustboroCity_PokemonSchool_EventScript_ChooseBlackboardTopic
	end

RustboroCity_PokemonSchool_EventScript_ChooseBlackboardTopic::
	message RustboroCity_PokemonSchool_Text_ReadWhichTopic
	waitmessage
	multichoicegrid 8, 1, MULTI_STATUS_INFO, 3, FALSE
	switch VAR_RESULT
	case 0, RustboroCity_PokemonSchool_EventScript_Poison
	case 1, RustboroCity_PokemonSchool_EventScript_Paralysis
	case 2, RustboroCity_PokemonSchool_EventScript_Sleep
	case 3, RustboroCity_PokemonSchool_EventScript_Burn
	case 4, RustboroCity_PokemonSchool_EventScript_Freeze
	case 5, RustboroCity_PokemonSchool_EventScript_ExitTopicSelect
	case MULTI_B_PRESSED, RustboroCity_PokemonSchool_EventScript_ExitTopicSelect
	end

RustboroCity_PokemonSchool_EventScript_Poison::
	msgbox RustboroCity_PokemonSchool_Text_ExplainPoison, MSGBOX_DEFAULT
	goto RustboroCity_PokemonSchool_EventScript_ChooseBlackboardTopic
	end

RustboroCity_PokemonSchool_EventScript_Paralysis::
	msgbox RustboroCity_PokemonSchool_Text_ExplainParalysis, MSGBOX_DEFAULT
	goto RustboroCity_PokemonSchool_EventScript_ChooseBlackboardTopic
	end

RustboroCity_PokemonSchool_EventScript_Sleep::
	msgbox RustboroCity_PokemonSchool_Text_ExplainSleep, MSGBOX_DEFAULT
	goto RustboroCity_PokemonSchool_EventScript_ChooseBlackboardTopic
	end

RustboroCity_PokemonSchool_EventScript_Burn::
	msgbox RustboroCity_PokemonSchool_Text_ExplainBurn, MSGBOX_DEFAULT
	goto RustboroCity_PokemonSchool_EventScript_ChooseBlackboardTopic
	end

RustboroCity_PokemonSchool_EventScript_Freeze::
	msgbox RustboroCity_PokemonSchool_Text_ExplainFreeze, MSGBOX_DEFAULT
	goto RustboroCity_PokemonSchool_EventScript_ChooseBlackboardTopic
	end

RustboroCity_PokemonSchool_EventScript_ExitTopicSelect::
	releaseall
	end

RustboroCity_PokemonSchool_EventScript_GameboyKid1::
	msgbox RustboroCity_PokemonSchool_Text_TradingRightNow, MSGBOX_NPC
	end

RustboroCity_PokemonSchool_EventScript_GameboyKid2::
	msgbox RustboroCity_PokemonSchool_Text_AlwaysWantedSeedot, MSGBOX_NPC
	end

RustboroCity_PokemonSchool_EventScript_RichBoy::
	msgbox RustboroCity_PokemonSchool_Text_PokemontCantUseManMadeItems, MSGBOX_NPC
	end

RustboroCity_PokemonSchool_EventScript_Lass::
	msgbox RustboroCity_PokemonSchool_Text_ConfusedPokemonAttacksItself, MSGBOX_NPC
	end

RustboroCity_PokemonSchool_EventScript_SchoolKidM::
	msgbox RustboroCity_PokemonSchool_Text_PokemonHealItselfWithBerry, MSGBOX_NPC
	end

RustboroCity_PokemonSchool_EventScript_StudentNotebook::
	msgbox RustboroCity_PokemonSchool_Text_StudentsNotes, MSGBOX_SIGN
	end

RustboroCity_PokemonSchool_EventScript_Teacher::
	lock
	faceplayer
	goto_if_set FLAG_RECEIVED_QUICK_CLAW, RustboroCity_PokemonSchool_EventScript_GaveQuickClaw
	call_if_eq VAR_FACING, DIR_EAST, RustboroCity_PokemonSchool_EventScript_TeacherCheckOnStudentsEast
	call_if_eq VAR_FACING, DIR_WEST, RustboroCity_PokemonSchool_EventScript_TeacherCheckOnStudentsWest
	msgbox RustboroCity_PokemonSchool_Text_StudentsWhoDontStudyGetQuickClaw, MSGBOX_DEFAULT
	giveitem ITEM_QUICK_CLAW
	goto_if_eq VAR_RESULT, 0, Common_EventScript_ShowBagIsFull
	closemessage
	applymovement VAR_LAST_TALKED, Common_Movement_WalkInPlaceFasterDown
	waitmovement 0
	setflag FLAG_RECEIVED_QUICK_CLAW
	release
	end

RustboroCity_PokemonSchool_EventScript_TeacherCheckOnStudentsEast::
	applymovement VAR_LAST_TALKED, RustboroCity_PokemonSchool_Movement_TeacherCheckOnStudentsEast
	waitmovement 0
	return

RustboroCity_PokemonSchool_EventScript_TeacherCheckOnStudentsWest::
	applymovement VAR_LAST_TALKED, RustboroCity_PokemonSchool_Movement_TeacherCheckOnStudentsWest
	waitmovement 0
	return

RustboroCity_PokemonSchool_EventScript_GaveQuickClaw::
	msgbox RustboroCity_PokemonSchool_Text_ExplainQuickClaw, MSGBOX_DEFAULT
	closemessage
	applymovement VAR_LAST_TALKED, Common_Movement_WalkInPlaceFasterDown
	waitmovement 0
	release
	end

RustboroCity_PokemonSchool_Movement_TeacherCheckOnStudentsWest:
	walk_left
	walk_down
	walk_down
	walk_right
	walk_in_place_faster_down
	delay_16
	delay_16
	delay_16
	walk_down
	walk_in_place_faster_left
	delay_16
	delay_16
	walk_right
	delay_16
	delay_16
	delay_8
	walk_up
	walk_left
	walk_left
	walk_up
	walk_up
	walk_right
	step_end

RustboroCity_PokemonSchool_Movement_TeacherCheckOnStudentsEast:
	walk_right
	walk_right
	walk_down
	walk_down
	walk_left
	walk_left
	walk_in_place_faster_down
	delay_16
	delay_16
	delay_16
	walk_down
	walk_in_place_faster_left
	delay_16
	delay_16
	walk_right
	delay_16
	delay_16
	delay_8
	walk_up
	walk_right
	walk_up
	walk_up
	walk_left
	walk_left
	step_end

RustboroCity_PokemonSchool_EventScript_Scott::
	lock
	faceplayer
	goto_if_set FLAG_MET_SCOTT_AFTER_OBTAINING_STONE_BADGE, RustboroCity_PokemonSchool_EventScript_ScottWatchStudents
	goto_if_set FLAG_MET_SCOTT_RUSTBORO, RustboroCity_PokemonSchool_EventScript_ScottSpokeAlready
	goto_if_set FLAG_BADGE01_GET, RustboroCity_PokemonSchool_EventScript_ScottGreetHasBadge
	msgbox RustboroCity_PokemonSchool_Text_ScottMetAlreadyCut, MSGBOX_DEFAULT
	addvar VAR_SCOTT_STATE, 1
	setflag FLAG_MET_SCOTT_RUSTBORO
	release
	end

RustboroCity_PokemonSchool_EventScript_ScottSpokeAlready::
	goto_if_set FLAG_BADGE01_GET, RustboroCity_PokemonSchool_EventScript_ScottNoticeBadge
	msgbox RustboroCity_PokemonSchool_Text_StudentTalentLevelUnknown, MSGBOX_DEFAULT
	release
	end

RustboroCity_PokemonSchool_EventScript_ScottGreetHasBadge::
	msgbox RustboroCity_PokemonSchool_Text_ScottMetAlreadyStoneBadge, MSGBOX_DEFAULT
	goto RustboroCity_PokemonSchool_EventScript_MetScottAfterBadge
	end

RustboroCity_PokemonSchool_EventScript_ScottNoticeBadge::
	msgbox RustboroCity_PokemonSchool_Text_ScottStoneBadge, MSGBOX_DEFAULT
	goto RustboroCity_PokemonSchool_EventScript_MetScottAfterBadge
	end

RustboroCity_PokemonSchool_EventScript_MetScottAfterBadge::
	addvar VAR_SCOTT_STATE, 1
	setflag FLAG_MET_SCOTT_AFTER_OBTAINING_STONE_BADGE
	release
	end

RustboroCity_PokemonSchool_EventScript_ScottWatchStudents::
	msgbox RustboroCity_PokemonSchool_Text_StudentTalentLevelUnknown, MSGBOX_DEFAULT
	release
	end

RustboroCity_PokemonSchool_Text_BlackboardListsStatusChanges:
	.string "The blackboard lists status conditions\n"
	.string "in battle.\p"
	.string "Someone drew a PIKACHU in the corner.\n"
	.string "It's pale. Its ears are down.$"

RustboroCity_PokemonSchool_Text_ReadWhichTopic:
	.string "Which topic do you want to read?$"

RustboroCity_PokemonSchool_Text_ExplainPoison:
	.string "Poison makes a POKéMON lose HP\n"
	.string "steadily.\p"
	.string "It lasts after battle.\p"
	.string "It keeps losing HP while you walk.\p"
	.string "Cure it with an ANTIDOTE.$"

RustboroCity_PokemonSchool_Text_ExplainParalysis:
	.string "Paralysis lowers SPEED.\p"
	.string "Sometimes the POKéMON can't move at\n"
	.string "all.\p"
	.string "It lasts after battle. Cure it with a\n"
	.string "PARLYZ HEAL.$"

RustboroCity_PokemonSchool_Text_ExplainSleep:
	.string "A sleeping POKéMON can't attack.\p"
	.string "It may wake up by itself. If the battle\n"
	.string "ends first, it stays asleep.\p"
	.string "Wake it with an AWAKENING. Or a bucket\n"
	.string "of water.$"

RustboroCity_PokemonSchool_Text_ExplainBurn:
	.string "A burn lowers ATTACK and drains HP.\p"
	.string "It lasts after battle. Cure it with a\n"
	.string "BURN HEAL.$"

RustboroCity_PokemonSchool_Text_ExplainFreeze:
	.string "A frozen POKéMON is completely\n"
	.string "helpless.\p"
	.string "It stays frozen after battle. Thaw it\n"
	.string "with an ICE HEAL.$"

RustboroCity_PokemonSchool_Text_StudentsWhoDontStudyGetQuickClaw:
	.string "Students who don't study get a taste\n"
	.string "of my QUICK CLAW.\p"
	.string "You think I'm just a teacher? No. I AM\n"
	.string "THE ONE WHO KNOCKS!$"

RustboroCity_PokemonSchool_Text_ExplainQuickClaw:
	.string "A POKéMON holding a QUICK CLAW\n"
	.string "sometimes moves first.\p"
	.string "There are many held items.\p"
	.string "Enough to study for years. Nobody will.$"

RustboroCity_PokemonSchool_Text_TradingRightNow:
	.string "Football's coming home this year. I can\n"
	.string "feel it.$"

RustboroCity_PokemonSchool_Text_AlwaysWantedSeedot:
	.string "HAHAHAHA! It's never coming home.$"

RustboroCity_PokemonSchool_Text_PokemontCantUseManMadeItems:
	.string "Schade DEUTSCHLAND, alles ist vorbei!$"

RustboroCity_PokemonSchool_Text_ConfusedPokemonAttacksItself:
	.string "Did you see the SKITTY that fell off\n"
	.string "the table? 40 million views.\p"
	.string "School doesn't teach you that.$"

RustboroCity_PokemonSchool_Text_PokemonHealItselfWithBerry:
	.string "Why learn about BERRIES?\p"
	.string "A guy on TikTok says school is a scam.\p"
	.string "He's 14. He owns a Lamborghini.$"

RustboroCity_PokemonSchool_Text_StudentsNotes:
	.string "It's a student's notebook…\p"
	.string "Catch POKéMON with POKé BALLS.\p"
	.string "Up to six POKéMON per TRAINER.\p"
	.string "A TRAINER catches, raises and battles\n"
	.string "POKéMON.\p"
	.string "A TRAINER's mission: beat the GYM\n"
	.string "LEADERS.\p"
	.string "Then, in the margin: “school is a scam”$"

RustboroCity_PokemonSchool_Text_ScottMetAlreadyCut:
	.string "Ahem. Hello, I'm PROF. BIRCH. I study…\n"
	.string "POKéMON. Their… habits.\p"
	.string "…Right. BIRCH would've talked about\n"
	.string "poop by now. Fine. I'm SCOTT.\p"
	.string "I watch TRAINERS. All of them. I know\n"
	.string "where they sleep.\p"
	.string "Teach a POKéMON CUT. Someone in this\n"
	.string "town has it. I've been in his house.$"

RustboroCity_PokemonSchool_Text_StudentTalentLevelUnknown:
	.string "SCOTT: I have a folder on every\n"
	.string "student. Height, weight, favorite\l"
	.string "snack. BIRCH would've studied their\l"
	.string "droppings.$"

RustboroCity_PokemonSchool_Text_ScottStoneBadge:
	.string "SCOTT: I watched the whole battle. You\n"
	.string "blinked 212 times.$"

RustboroCity_PokemonSchool_Text_ScottMetAlreadyStoneBadge:
	.string "Ahem. Hello, I'm PROF. BIRCH. I study…\n"
	.string "POKéMON. Their… habits.\p"
	.string "…Right. BIRCH would've talked about\n"
	.string "poop by now. Fine. I'm SCOTT.\p"
	.string "I watch TRAINERS. All of them. I know\n"
	.string "where they sleep.\p"
	.string "A STONE BADGE. I know. I watched you\n"
	.string "get it. Through the vent.$"

