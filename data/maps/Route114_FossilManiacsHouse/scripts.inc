Route114_FossilManiacsHouse_MapScripts::
	map_script MAP_SCRIPT_ON_TRANSITION, Route114_FossilManiacsHouse_OnTransition
	.byte 0

Route114_FossilManiacsHouse_OnTransition:
	setflag FLAG_LANDMARK_FOSSIL_MANIACS_HOUSE
	end

Route114_FossilManiacsHouse_EventScript_FossilManiacsBrother::
	lock
	faceplayer
	goto_if_set FLAG_RECEIVED_TM_DIG, Route114_FossilManiacsHouse_EventScript_ReceivedDig
	msgbox Route114_FossilManiacsHouse_Text_HaveThisToDigLikeMyBrother, MSGBOX_DEFAULT
	giveitem ITEM_TM_DIG
	goto_if_eq VAR_RESULT, FALSE, Common_EventScript_ShowBagIsFull
	setflag FLAG_RECEIVED_TM_DIG
	release
	end

Route114_FossilManiacsHouse_EventScript_ReceivedDig::
	msgbox Route114_FossilManiacsHouse_Text_DigReturnsYouToEntrance, MSGBOX_DEFAULT
	release
	end

Route114_FossilManiacsHouse_EventScript_RockDisplay::
	msgbox Route114_FossilManiacsHouse_Text_RocksFillDisplayCase, MSGBOX_SIGN
	end

Route114_FossilManiacsHouse_EventScript_Bookshelf::
	msgbox Route114_FossilManiacsHouse_Text_CrammedWithBooks, MSGBOX_SIGN
	end

Route114_FossilManiacsHouse_Text_HaveThisToDigLikeMyBrother:
	.string "My big brother is the FOSSIL MANIAC…\p"
	.string "He's a genius. Nobody knows. He loves\n"
	.string "FOSSILS…\p"
	.string "He dug this hole by himself…\p"
	.string "Take this, so you can DIG like my\n"
	.string "brother…$"

Route114_FossilManiacsHouse_Text_DigReturnsYouToEntrance:
	.string "DIG. You dig. Then you hit.\p"
	.string "In a cave, it takes you back to the\n"
	.string "entrance. Riveting.$"

Route114_FossilManiacsHouse_Text_RocksFillDisplayCase:
	.string "Rocks in strange shapes fill the\n"
	.string "display case…\p"
	.string "Each one labeled. In three languages.$"

Route114_FossilManiacsHouse_Text_CrammedWithBooks:
	.string "THE COMPOSITION OF STRATA… HOW RAIN\n"
	.string "SHAPES THE LAND…\p"
	.string "STONES, SOIL AND ROCK…\p"
	.string "All read. All annotated. This guy is a\n"
	.string "genius.$"

