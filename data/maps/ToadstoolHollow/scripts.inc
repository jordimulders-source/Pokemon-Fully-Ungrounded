@ Project Grounded: Toadstool Hollow, verborgen paddenstoelenbos achter Petalburg Woods
@ (kaart: tools/grounded/maptools/mushroom_forest.py). Placeholderteksten; Jordi herschrijft ze via de Dialoogstudio.
@ Ingang: de doorloopbare boom in de oostrand van Petalburg Woods (x 46-47, y 10).

ToadstoolHollow_MapScripts::
	.byte 0

@ ---------------------------------------------------------------- trainers
ToadstoolHollow_EventScript_Oskar::
	trainerbattle_single TRAINER_HOLLOW_OSKAR, ToadstoolHollow_Text_OskarIntro, ToadstoolHollow_Text_OskarDefeat
	msgbox ToadstoolHollow_Text_OskarPostBattle, MSGBOX_AUTOCLOSE
	end

ToadstoolHollow_EventScript_Morelle::
	trainerbattle_single TRAINER_HOLLOW_MORELLE, ToadstoolHollow_Text_MorelleIntro, ToadstoolHollow_Text_MorelleDefeat
	msgbox ToadstoolHollow_Text_MorellePostBattle, MSGBOX_AUTOCLOSE
	end

ToadstoolHollow_EventScript_Gerrit::
	trainerbattle_single TRAINER_HOLLOW_GERRIT, ToadstoolHollow_Text_GerritIntro, ToadstoolHollow_Text_GerritDefeat
	msgbox ToadstoolHollow_Text_GerritPostBattle, MSGBOX_AUTOCLOSE
	end

@ ---------------------------------------------------------------- teksten
ToadstoolHollow_Text_OskarIntro:
	.string "I followed a PARAS in here\n"
	.string "three days ago.\p"
	.string "Now I'm pretty sure the PARAS\n"
	.string "is following ME.$"

ToadstoolHollow_Text_OskarDefeat:
	.string "The mushroom on its back just\n"
	.string "winked at me. Cool. Cool cool.$"

ToadstoolHollow_Text_OskarPostBattle:
	.string "Don't eat the glowing ones.\p"
	.string "Or do. Science needs a\n"
	.string "control group.$"

ToadstoolHollow_Text_MorelleIntro:
	.string "Shh. I'm foraging.\p"
	.string "One of these makes a lovely soup.\n"
	.string "The rest make a lovely funeral.$"

ToadstoolHollow_Text_MorelleDefeat:
	.string "Fine, I'll make tea instead.\n"
	.string "Tea never killed anyone. Probably.$"

ToadstoolHollow_Text_MorellePostBattle:
	.string "See that ring of mushrooms?\p"
	.string "Folklore says if you step inside,\n"
	.string "you dance until you die.\p"
	.string "Or you find something nice in\n"
	.string "the middle. Folklore is vague.$"

ToadstoolHollow_Text_GerritIntro:
	.string "Which way is out?\p"
	.string "No, don't tell me. The trees are\n"
	.string "listening, and they lie.$"

ToadstoolHollow_Text_GerritDefeat:
	.string "Three weeks I've been lost.\n"
	.string "PHANTUMP says that's nothing.$"

ToadstoolHollow_Text_GerritPostBattle:
	.string "PHANTUMP says he used to be\n"
	.string "a hiker too.\p"
	.string "I've decided not to ask\n"
	.string "any follow-up questions.$"
