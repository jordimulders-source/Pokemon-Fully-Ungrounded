Route135_House_MapScripts::
	.byte 0

Route135_House_EventScript_OldMan::
	msgbox Route135_House_Text_OldMan, MSGBOX_NPC
	end

Route135_House_EventScript_OldWoman::
	msgbox Route135_House_Text_OldWoman, MSGBOX_NPC
	end

Route135_House_Text_OldMan:
	.string "News? We stopped following the news\n"
	.string "twenty years ago.\p"
	.string "Who's the CHAMPION these days?\n"
	.string "Things were better back then anyway.$"

Route135_House_Text_OldWoman:
	.string "We don't own a TV. Or a radio.\n"
	.string "Or anything with a plug.\p"
	.string "The big companies won't get\n"
	.string "a single POKé DOLLAR from us!$"
