@ Project Grounded: Rocket-hideout B1F (labo/kazerne, teleportdoolhof). Kaart: tools/grounded/maptools/rocket_hideout.py
@ Placeholderteksten; Jordi herschrijft ze via de Dialoogstudio.
RocketHideout_B1F_MapScripts::
	.byte 0

RocketHideout_B1F_EventScript_Scientist::
	trainerbattle_single TRAINER_ROCKET_SCIENTIST, RocketHideout_B1F_Text_ScientistIntro, RocketHideout_B1F_Text_ScientistDefeat
	msgbox RocketHideout_B1F_Text_ScientistPostBattle, MSGBOX_AUTOCLOSE
	end

RocketHideout_B1F_EventScript_Thief::
	trainerbattle_single TRAINER_ROCKET_THIEF, RocketHideout_B1F_Text_ThiefIntro, RocketHideout_B1F_Text_ThiefDefeat
	msgbox RocketHideout_B1F_Text_ThiefPostBattle, MSGBOX_AUTOCLOSE
	end

RocketHideout_B1F_Text_ScientistIntro:
	.string "I networked every MAGNEMITE in this\n"
	.string "base into one supercomputer.\p"
	.string "It calculated that you will lose.\n"
	.string "It is also running DOOM.$"

RocketHideout_B1F_Text_ScientistDefeat:
	.string "The supercomputer would like to\n"
	.string "retract its previous statement.$"

RocketHideout_B1F_Text_ScientistPostBattle:
	.string "These teleport pads were cheaper\n"
	.string "than stairs. Like our dental plan:\l"
	.string "it also just teleports your teeth.$"

RocketHideout_B1F_Text_ThiefIntro:
	.string "Everything I own is stolen.\n"
	.string "The CHANSEY? From a NURSE JOY.\p"
	.string "The DELIBIRD? From Christmas.\p"
	.string "The FARFETCH'D stole its own leek,\n"
	.string "and then I stole the FARFETCH'D.$"

RocketHideout_B1F_Text_ThiefDefeat:
	.string "You can't rob a robber!\n"
	.string "…Oh. You just did.$"

RocketHideout_B1F_Text_ThiefPostBattle:
	.string "If you find a leek, it's mine.\n"
	.string "I mean the bird's. I mean mine.$"
