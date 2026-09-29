GraniteCave_1F_MapScripts::
	.byte 0

GraniteCave_1F_EventScript_Hiker::
	lock
	faceplayer
	goto_if_set FLAG_RECEIVED_HM_FLASH, GraniteCave_1F_EventScript_ReceivedFlash
	msgbox GraniteCave_1F_Text_GetsDarkAheadHereYouGo, MSGBOX_DEFAULT
	giveitem ITEM_HM_FLASH
	setflag FLAG_RECEIVED_HM_FLASH
	msgbox GraniteCave_1F_Text_ExplainFlash, MSGBOX_DEFAULT
	release
	end

GraniteCave_1F_EventScript_ReceivedFlash::
	msgbox GraniteCave_1F_Text_ExplainFlash, MSGBOX_DEFAULT
	release
	end

GraniteCave_1F_Text_GetsDarkAheadHereYouGo:
	.string "Hey. It gets awfully dark ahead.\p"
	.string "That STEVEN guy came by earlier. He had\n"
	.string "FLASH.\p"
	.string "And a guitar. He played the whole way in.\p"
	.string "HIKERS help each other out. Here.$"

GraniteCave_1F_Text_ExplainFlash:
	.string "FLASH. It lights up dark caves. You need\n"
	.string "DEWFORD's GYM BADGE to use it outside\l"
	.string "battle.\p"
	.string "It also lowers accuracy. Mostly, it's\n"
	.string "light.$"

