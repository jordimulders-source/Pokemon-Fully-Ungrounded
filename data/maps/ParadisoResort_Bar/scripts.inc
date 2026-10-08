@ Project Grounded: strandbar van het PARADISO RESORT (layout van het Seashore House). Lorelei vecht post-game.
ParadisoResort_Bar_MapScripts::
	.byte 0

ParadisoResort_Bar_EventScript_Bartender::
	msgbox ParadisoResort_Bar_Text_Bartender, MSGBOX_NPC
	end

ParadisoResort_Bar_EventScript_Lorelei::
	goto_if_unset FLAG_SYS_GAME_CLEAR, ParadisoResort_Bar_EventScript_LoreleiNotYet
	goto_if_defeated TRAINER_RESORT_LORELEI, ParadisoResort_Bar_EventScript_LoreleiPost
	lock
	faceplayer
	msgbox ParadisoResort_Bar_Text_LoreleiAsk, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, ParadisoResort_Bar_EventScript_LoreleiDecline
	trainerbattle_single TRAINER_RESORT_LORELEI, ParadisoResort_Bar_Text_LoreleiIntro, ParadisoResort_Bar_Text_LoreleiDefeat
ParadisoResort_Bar_EventScript_LoreleiPost::
	msgbox ParadisoResort_Bar_Text_LoreleiPost, MSGBOX_AUTOCLOSE
	end

ParadisoResort_Bar_EventScript_LoreleiDecline::
	msgbox ParadisoResort_Bar_Text_LoreleiDecline, MSGBOX_DEFAULT
	release
	end

ParadisoResort_Bar_EventScript_LoreleiNotYet::
	msgbox ParadisoResort_Bar_Text_LoreleiNotYet, MSGBOX_NPC
	end

ParadisoResort_Bar_EventScript_DrunkSailor::
	msgbox ParadisoResort_Bar_Text_DrunkSailor, MSGBOX_NPC
	end

ParadisoResort_Bar_EventScript_Tuber::
	msgbox ParadisoResort_Bar_Text_Tuber, MSGBOX_NPC
	end

@ ---------------------------------------------------------------- teksten (placeholders, Jordi herschrijft ze)
ParadisoResort_Bar_Text_Bartender:
	.string "Welcome to the beach bar!\n"
	.string "Everything is free. All-inclusive.\p"
	.string "That's why I look like this.\n"
	.string "I haven't slept since Tuesday.$"

ParadisoResort_Bar_Text_LoreleiNotYet:
	.string "LORELEI: The ice machine is broken.\p"
	.string "So I brought my own ice.\n"
	.string "Her name is LAPRAS.\p"
	.string "Come back when you're CHAMPION.\n"
	.string "My drink isn't cold enough yet.$"

ParadisoResort_Bar_Text_LoreleiIntro:
	.string "LORELEI: Thirty degrees in the shade\n"
	.string "and you want to battle the ELITE\l"
	.string "FOUR's ice queen?\p"
	.string "Bold. I'll put you on the rocks.$"

ParadisoResort_Bar_Text_LoreleiDefeat:
	.string "…You melted my ice.\n"
	.string "That one's going on your tab.$"

ParadisoResort_Bar_Text_LoreleiPost:
	.string "LORELEI: Everyone here drinks\n"
	.string "piña coladas.\p"
	.string "I order mine frozen solid and\n"
	.string "eat it with a fork.$"

ParadisoResort_Bar_Text_DrunkSailor:
	.string "I've sailed the seven seas!\n"
	.string "HOENN has a lot more than seven.\p"
	.string "I've been sailing since 1987.\n"
	.string "I just wanted to go home. Hic!$"

ParadisoResort_Bar_Text_Tuber:
	.string "The bartender gave me a juice box.\n"
	.string "It's all-inclusive!\p"
	.string "I've had thirty. I can hear\n"
	.string "colours.$"

ParadisoResort_Bar_Text_LoreleiAsk:
	.string "LORELEI: I'm on my third drink and my\n"
	.string "first day off in four generations.\p"
	.string "Are you here to battle me? Think before\n"
	.string "you answer.$"

ParadisoResort_Bar_Text_LoreleiDecline:
	.string "LORELEI: Wise. The ice in this glass is\n"
	.string "the only ice I want to deal with today.$"
