MagmaHideout_2F_2R_MapScripts::
	.byte 0

MagmaHideout_2F_2R_EventScript_Grunt15::
	trainerbattle_single TRAINER_GRUNT_MAGMA_HIDEOUT_15, MagmaHideout_2F_2R_Text_Grunt15Intro, MagmaHideout_2F_2R_Text_Grunt15Defeat
	msgbox MagmaHideout_2F_2R_Text_Grunt15PostBattle, MSGBOX_AUTOCLOSE
	end

MagmaHideout_2F_2R_EventScript_Grunt6::
	trainerbattle_single TRAINER_GRUNT_MAGMA_HIDEOUT_6, MagmaHideout_2F_2R_Text_Grunt6Intro, MagmaHideout_2F_2R_Text_Grunt6Defeat
	msgbox MagmaHideout_2F_2R_Text_Grunt6PostBattle, MSGBOX_AUTOCLOSE
	end

MagmaHideout_2F_2R_EventScript_Grunt7::
	trainerbattle_single TRAINER_GRUNT_MAGMA_HIDEOUT_7, MagmaHideout_2F_2R_Text_Grunt7Intro, MagmaHideout_2F_2R_Text_Grunt7Defeat
	msgbox MagmaHideout_2F_2R_Text_Grunt7PostBattle, MSGBOX_AUTOCLOSE
	end

MagmaHideout_2F_2R_EventScript_Grunt8::
	trainerbattle_single TRAINER_GRUNT_MAGMA_HIDEOUT_8, MagmaHideout_2F_2R_Text_Grunt8Intro, MagmaHideout_2F_2R_Text_Grunt8Defeat
	msgbox MagmaHideout_2F_2R_Text_Grunt8PostBattle, MSGBOX_AUTOCLOSE
	end

MagmaHideout_2F_2R_Text_Grunt15Intro:
	.string "No bone to pick with you. Just peppers.$"

MagmaHideout_2F_2R_Text_Grunt15Defeat:
	.string "I may have lost, but my sauce won't.$"

MagmaHideout_2F_2R_Text_Grunt15PostBattle:
	.string "We got the BLUE ORB! GROUDON will be the\n"
	.string "ultimate heat source for the sauce.$"

MagmaHideout_2F_2R_Text_Grunt6Intro:
	.string "I can't stand heat. Maybe I should've\n"
	.string "joined TEAM AQUA and sipped fizzy water\l"
	.string "all day.$"

MagmaHideout_2F_2R_Text_Grunt6Defeat:
	.string "Yeah… I order everything mild.$"

MagmaHideout_2F_2R_Text_Grunt6PostBattle:
	.string "Don't tell anyone, but I put yogurt on\n"
	.string "everything.$"

MagmaHideout_2F_2R_Text_Grunt7Intro:
	.string "Hear those tremors? That's not the\n"
	.string "volcano. That's the guy who ate a whole\l"
	.string "SCOVILLAIN.$"

MagmaHideout_2F_2R_Text_Grunt7Defeat:
	.string "You're a fiery battler. Just like DA\n"
	.string "BOMB!$"

MagmaHideout_2F_2R_Text_Grunt7PostBattle:
	.string "Laugh now. Our sauce will melt HOENN.$"

MagmaHideout_2F_2R_Text_Grunt8Intro:
	.string "Someone lost his MAGMA EMBLEM… Wait, do\n"
	.string "you even like spicy food?$"

MagmaHideout_2F_2R_Text_Grunt8Defeat:
	.string "You beat me AND you like spicy food?$"

MagmaHideout_2F_2R_Text_Grunt8PostBattle:
	.string "I've got a feeling our sauce will end up\n"
	.string "too mild…$"

