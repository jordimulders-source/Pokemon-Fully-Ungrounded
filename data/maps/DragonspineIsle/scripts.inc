@ Project Grounded: Dragonspine Isle, het drakeneiland rechts van Route 129 (ZEE_PLAN.md idee 6).
@ Kaart en scripts: tools/grounded/maptools/beacon_dragon.py. In de bergwand de Dragon's Den (drakenwachter GERALD,
@ achter een waterval). Teksten zijn placeholders.
DragonspineIsle_MapScripts::
	.byte 0

DragonspineIsle_EventScript_Vernon::
	trainerbattle_single TRAINER_DRAGONSPINE_VERNON, DragonspineIsle_Text_VernonIntro, DragonspineIsle_Text_VernonDefeat
	msgbox DragonspineIsle_Text_VernonPost, MSGBOX_AUTOCLOSE
	end

DragonspineIsle_EventScript_Saela::
	trainerbattle_single TRAINER_DRAGONSPINE_SAELA, DragonspineIsle_Text_SaelaIntro, DragonspineIsle_Text_SaelaDefeat
	msgbox DragonspineIsle_Text_SaelaPost, MSGBOX_AUTOCLOSE
	end

DragonspineIsle_EventScript_Adjuster::
	msgbox DragonspineIsle_Text_Adjuster, MSGBOX_NPC
	end

@ ---------------------------------------------------------------- teksten (placeholders, Jordi herschrijft ze)
DragonspineIsle_Text_VernonIntro:
	.string "Welcome to DRAGONSPINE ISLE! The\n"
	.string "dragons here are wild, free and\l"
	.string "incredibly bitey.$"

DragonspineIsle_Text_VernonDefeat:
	.string "Bitten. Again.$"

DragonspineIsle_Text_VernonPost:
	.string "I've been bitten 412 times. I keep\n"
	.string "count. It keeps me humble.$"

DragonspineIsle_Text_SaelaIntro:
	.string "I came here to train with dragons.\n"
	.string "Mostly I've been training my running.$"

DragonspineIsle_Text_SaelaDefeat:
	.string "Running away it is.$"

DragonspineIsle_Text_SaelaPost:
	.string "The cave? The warden lives in there.\n"
	.string "GERALD.\p"
	.string "He has a clipboard. Even the dragons\n"
	.string "are afraid of the clipboard.$"

DragonspineIsle_Text_Adjuster:
	.string "I'm the island's insurance adjuster.\p"
	.string "Claims this week: fourteen scorched\n"
	.string "tents, three eaten canoes and one man\l"
	.string "who “just wanted to pet it.”\p"
	.string "All denied. Dragons count as an act of\n"
	.string "God.$"
