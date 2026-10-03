MagmaHideout_2F_3R_MapScripts::
	.byte 0

@ ---------------------------------------------------------------- Project Grounded: Colress tussen de boormachines
MagmaHideout_2F_3R_EventScript_Colress::
	lock
	faceplayer
	msgbox MagmaHideout_2F_3R_Text_ColressIntro, MSGBOX_DEFAULT
	msgbox MagmaHideout_2F_3R_Text_ColressAsk, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, MagmaHideout_2F_3R_EventScript_ColressDeclined
	msgbox MagmaHideout_2F_3R_Text_ColressAccept, MSGBOX_DEFAULT
	trainerbattle_no_intro TRAINER_COLRESS_MAGMA, MagmaHideout_2F_3R_Text_ColressDefeat
	msgbox MagmaHideout_2F_3R_Text_ColressPostBattle, MSGBOX_DEFAULT
	closemessage
	fadescreen FADE_TO_BLACK
	removeobject LOCALID_MAGMA_HIDEOUT_COLRESS
	setflag FLAG_HIDE_MAGMA_HIDEOUT_COLRESS
	fadescreen FADE_FROM_BLACK
	release
	end

MagmaHideout_2F_3R_EventScript_ColressDeclined::
	msgbox MagmaHideout_2F_3R_Text_ColressDeclined, MSGBOX_DEFAULT
	release
	end

MagmaHideout_2F_3R_Text_ColressIntro:
	.string "COLRESS: Ah, you again! Look at these\n"
	.string "drills. Aren't they beautiful?\p"
	.string "I once worked with a group called TEAM\n"
	.string "PLASMA. Complete amateurs. Their\l"
	.string "master plan required a dragon, a castle,\l"
	.string "and a man in a cape who monologued for\l"
	.string "forty minutes.\p"
	.string "TEAM MAGMA is different. Their\n"
	.string "technique is in order. These drills have\l"
	.string "a maintenance schedule. It is\l"
	.string "laminated!\p"
	.string "Their only flaw is the goal. They want to\n"
	.string "make the land bigger by setting fire to\l"
	.string "the sea. The engineering is flawless.\l"
	.string "The idea is soup.\p"
	.string "Anyway. I have upgraded my team since\n"
	.string "MAUVILLE. Machine learning! My Pokémon\l"
	.string "now train themselves every turn.$"

MagmaHideout_2F_3R_Text_ColressAsk:
	.string "Shall we see whether your logic still\n"
	.string "beats my improved algorithms?$"

MagmaHideout_2F_3R_Text_ColressAccept:
	.string "Wonderful! Begin the experiment!$"

MagmaHideout_2F_3R_Text_ColressDeclined:
	.string "Hmm. A control group that refuses to be\n"
	.string "tested. I'll be here, admiring the\l"
	.string "laminated schedule.$"

MagmaHideout_2F_3R_Text_ColressDefeat:
	.string "Even with machine learning... The data is\n"
	.string "clear. You are the variable I cannot\l"
	.string "predict!$"

MagmaHideout_2F_3R_Text_ColressPostBattle:
	.string "Splendid. I must rewrite my entire\n"
	.string "model. Again.\p"
	.string "Go on, stop whatever these people are\n"
	.string "planning. I'll stay and take notes on\l"
	.string "the drills. For science. Not for TEAM\l"
	.string "MAGMA.$"
