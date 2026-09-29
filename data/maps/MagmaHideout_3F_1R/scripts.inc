MagmaHideout_3F_1R_MapScripts::
	.byte 0

MagmaHideout_3F_1R_EventScript_Grunt9::
	trainerbattle_single TRAINER_GRUNT_MAGMA_HIDEOUT_9, MagmaHideout_3F_1R_Text_Grunt9Intro, MagmaHideout_3F_1R_Text_Grunt9Defeat
	msgbox MagmaHideout_3F_1R_Text_Grunt9PostBattle, MSGBOX_AUTOCLOSE
	end

MagmaHideout_3F_1R_EventScript_Grunt16::
	trainerbattle_single TRAINER_GRUNT_MAGMA_HIDEOUT_16, MagmaHideout_3F_1R_Text_Grunt16Intro, MagmaHideout_3F_1R_Text_Grunt16Defeat
	msgbox MagmaHideout_3F_1R_Text_Grunt16PostBattle, MSGBOX_AUTOCLOSE
	end

MagmaHideout_3F_1R_Text_Grunt9Intro:
	.string "What did I do to deserve this post? My\n"
	.string "left ear is burning. So is everything\l"
	.string "else.$"

MagmaHideout_3F_1R_Text_Grunt9Defeat:
	.string "Heat exhaustion… or the wings.$"

MagmaHideout_3F_1R_Text_Grunt9PostBattle:
	.string "Why the hoods? To hide the tears.$"

MagmaHideout_3F_1R_Text_Grunt16Intro:
	.string "My SCOVILLAIN and I grow our own\n"
	.string "peppers. Organic. Also illegal in three\l"
	.string "regions.$"

MagmaHideout_3F_1R_Text_Grunt16Defeat:
	.string "SCOVILLAIN, go cry in the corner.$"

MagmaHideout_3F_1R_Text_Grunt16PostBattle:
	.string "TEAM AQUA drinks sparkling water with\n"
	.string "LEMON. Disgusting.$"

