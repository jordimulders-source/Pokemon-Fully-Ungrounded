MagmaHideout_3F_2R_MapScripts::
	.byte 0

MagmaHideout_3F_2R_EventScript_Grunt10::
	trainerbattle_single TRAINER_GRUNT_MAGMA_HIDEOUT_10, MagmaHideout_3F_2R_Text_Grunt10Intro, MagmaHideout_3F_2R_Text_Grunt10Defeat
	msgbox MagmaHideout_3F_2R_Text_Grunt10PostBattle, MSGBOX_AUTOCLOSE
	end

MagmaHideout_3F_2R_Text_Grunt10Intro:
	.string "I get everything our leader says. But a\n"
	.string "sauce that melts the whole region?\l"
	.string "Isn't that a bit much?$"

MagmaHideout_3F_2R_Text_Grunt10Defeat:
	.string "Yeah, we're doing something wrong.$"

MagmaHideout_3F_2R_Text_Grunt10PostBattle:
	.string "Losing cleared my mind. And my sinuses.$"

