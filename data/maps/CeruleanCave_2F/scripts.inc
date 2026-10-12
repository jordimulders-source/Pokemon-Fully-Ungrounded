@ Project Grounded: CeruleanCave_2F (tools/grounded/maptools/spacetime_cave.py)
CeruleanCave_2F_MapScripts::
	.byte 0

CeruleanCave_2F_EventScript_Vera::
	trainerbattle_single TRAINER_CC_GRUNT_VERA, CeruleanCave_2F_Text_VeraIntro, CeruleanCave_2F_Text_VeraDefeat
	msgbox CeruleanCave_2F_Text_VeraPost, MSGBOX_AUTOCLOSE
	end

CeruleanCave_2F_EventScript_Duncan::
	trainerbattle_single TRAINER_CC_GRUNT_DUNCAN, CeruleanCave_2F_Text_DuncanIntro, CeruleanCave_2F_Text_DuncanDefeat
	msgbox CeruleanCave_2F_Text_DuncanPost, MSGBOX_AUTOCLOSE
	end

@ ---------------------------------------------------------------- teksten (placeholders, Jordi herschrijft ze)
CeruleanCave_2F_Text_VeraIntro:
	.string "Another tourist from the purple hole?\n"
	.string "We already have a tourist. We put him in\l"
	.string "the lake.$"

CeruleanCave_2F_Text_VeraDefeat:
	.string "Okay, okay! You can stay out of the\n"
	.string "lake.$"

CeruleanCave_2F_Text_VeraPost:
	.string "We've been searching this cave for\n"
	.string "weeks. Every tunnel looks the same. I\l"
	.string "think the cave does it on purpose.$"

CeruleanCave_2F_Text_DuncanIntro:
	.string "Shh! I'm listening for MEWTWO. It's\n"
	.string "psychic, so I'm trying very hard not to\l"
	.string "think.$"

CeruleanCave_2F_Text_DuncanDefeat:
	.string "I thought about losing. And then I lost.\n"
	.string "It works!$"

CeruleanCave_2F_Text_DuncanPost:
	.string "The BOSS is down below. He doesn't need\n"
	.string "us. He just likes an audience.$"
