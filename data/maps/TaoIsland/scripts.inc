@ Project Grounded: het Tao-eiland (was Dragonspine Isle), rechts van Route 129.
@ Kaart en scripts: tools/grounded/maptools/tao_island.py. Toren -> RESHIRAM en ZEKROM, Dragon's Den -> KYUREM en
@ GHETSIS. Teksten zijn placeholders.
TaoIsland_MapScripts::
	.byte 0

TaoIsland_EventScript_Vernon::
	trainerbattle_single TRAINER_TAO_VERNON, TaoIsland_Text_VernonIntro, TaoIsland_Text_VernonDefeat
	msgbox TaoIsland_Text_VernonPost, MSGBOX_AUTOCLOSE
	end

TaoIsland_EventScript_Saela::
	trainerbattle_single TRAINER_TAO_SAELA, TaoIsland_Text_SaelaIntro, TaoIsland_Text_SaelaDefeat
	msgbox TaoIsland_Text_SaelaPost, MSGBOX_AUTOCLOSE
	end

TaoIsland_EventScript_Adjuster::
	msgbox TaoIsland_Text_Adjuster, MSGBOX_NPC
	end

TaoIsland_EventScript_Sign::
	msgbox TaoIsland_Text_Sign, MSGBOX_SIGN
	end

@ ---------------------------------------------------------------- teksten (placeholders, Jordi herschrijft ze)
TaoIsland_Text_VernonIntro:
	.string "Welcome to TAO ISLAND! Formerly\n"
	.string "DRAGONSPINE ISLE. We rebranded.\p"
	.string "The dragons didn't notice. They still\n"
	.string "bite in the old font.$"

TaoIsland_Text_VernonDefeat:
	.string "Bitten. Again.$"

TaoIsland_Text_VernonPost:
	.string "I've been bitten 412 times. I keep\n"
	.string "count. It keeps me humble.\p"
	.string "That tower is three thousand years old.\n"
	.string "The “No Swimming” sign is older.$"

TaoIsland_Text_SaelaIntro:
	.string "I came here to train with dragons.\n"
	.string "Mostly I've been training my running.$"

TaoIsland_Text_SaelaDefeat:
	.string "Running away it is.$"

TaoIsland_Text_SaelaPost:
	.string "Two dragons sleep at the top of that\n"
	.string "tower. One white, one black. Brothers.\p"
	.string "They haven't spoken in three hundred\n"
	.string "years. Honestly? Relatable.$"

TaoIsland_Text_Adjuster:
	.string "I'm the island's insurance adjuster.\p"
	.string "Claims this week: fourteen scorched\n"
	.string "tents, three eaten canoes and one man\l"
	.string "who “just wanted to pet it.”\p"
	.string "All denied. Dragons count as an act of\n"
	.string "God. The tower counts as two acts of\l"
	.string "God. Double denied.$"

TaoIsland_Text_Sign:
	.string "TAO TOWER\n"
	.string "Built: yes. Visitors: at own risk.\l"
	.string "Legendary dragons: do not poke.$"
