MegaForest_MapScripts::
	.byte 0

@ Project Grounded: Mega Forest (tools/grounded/maptools/mega_forest.py), post-game achter het Mini Forest.
@ Achterin rusten Zacian en Zamazenta (lv 70, MUS_RG_VS_LEGEND als placeholder). Met het roestige zwaard/schild
@ uit het Mini Forest als vastgehouden item nemen ze in een gevecht hun Crowned-vorm aan.
MegaForest_EventScript_Zacian::
	lock
	msgbox MegaForest_Text_Zacian, MSGBOX_DEFAULT
	playmoncry SPECIES_ZACIAN, CRY_MODE_ENCOUNTER
	waitmoncry
	setwildbattle SPECIES_ZACIAN, 70
	setflag FLAG_SYS_CTRL_OBJ_DELETE
	special BattleSetup_StartLegendaryBattle
	waitstate
	clearflag FLAG_SYS_CTRL_OBJ_DELETE
	specialvar VAR_RESULT, GetBattleOutcome
	goto_if_eq VAR_RESULT, B_OUTCOME_RAN, MegaForest_EventScript_LegendStays
	goto_if_eq VAR_RESULT, B_OUTCOME_PLAYER_TELEPORTED, MegaForest_EventScript_LegendStays
	removeobject LOCALID_MEGA_FOREST_ZACIAN
	setflag FLAG_HIDE_MEGA_FOREST_ZACIAN
	release
	end

MegaForest_EventScript_Zamazenta::
	lock
	msgbox MegaForest_Text_Zamazenta, MSGBOX_DEFAULT
	playmoncry SPECIES_ZAMAZENTA, CRY_MODE_ENCOUNTER
	waitmoncry
	setwildbattle SPECIES_ZAMAZENTA, 70
	setflag FLAG_SYS_CTRL_OBJ_DELETE
	special BattleSetup_StartLegendaryBattle
	waitstate
	clearflag FLAG_SYS_CTRL_OBJ_DELETE
	specialvar VAR_RESULT, GetBattleOutcome
	goto_if_eq VAR_RESULT, B_OUTCOME_RAN, MegaForest_EventScript_LegendStays
	goto_if_eq VAR_RESULT, B_OUTCOME_PLAYER_TELEPORTED, MegaForest_EventScript_LegendStays
	removeobject LOCALID_MEGA_FOREST_ZAMAZENTA
	setflag FLAG_HIDE_MEGA_FOREST_ZAMAZENTA
	release
	end

MegaForest_EventScript_LegendStays::
	release
	end

MegaForest_EventScript_Plaque::
	msgbox MegaForest_Text_Plaque, MSGBOX_SIGN
	end

MegaForest_EventScript_Percival::
	trainerbattle_single TRAINER_MEGA_FOREST_PERCIVAL, MegaForest_Text_PercivalIntro, MegaForest_Text_PercivalDefeat
	msgbox MegaForest_Text_PercivalPost, MSGBOX_AUTOCLOSE
	end

MegaForest_EventScript_Morgana::
	trainerbattle_single TRAINER_MEGA_FOREST_MORGANA, MegaForest_Text_MorganaIntro, MegaForest_Text_MorganaDefeat
	msgbox MegaForest_Text_MorganaPost, MSGBOX_AUTOCLOSE
	end

MegaForest_EventScript_Gwen::
	trainerbattle_single TRAINER_MEGA_FOREST_GWEN, MegaForest_Text_GwenIntro, MegaForest_Text_GwenDefeat
	msgbox MegaForest_Text_GwenPost, MSGBOX_AUTOCLOSE
	end

MegaForest_Text_Zacian:
	.string "A great wolf lies curled up among\n"
	.string "the flowers, one eye half open.\p"
	.string "It looks at you the way a dog looks\n"
	.string "at a stick. Expectant.$"

MegaForest_Text_Zamazenta:
	.string "A great wolf sits perfectly still,\n"
	.string "like a wall that learned to breathe.\p"
	.string "It has clearly decided that you are\n"
	.string "the intruder here. Fair.$"

MegaForest_Text_Plaque:
	.string "“HERE REST THE TWO HEROES OF\n"
	.string "LEGEND, WHO SAVED THE LAND.”\p"
	.string "Below, smaller: “PLEASE DO NOT PET\n"
	.string "THE HEROES. THEY WILL LET YOU.\l"
	.string "THAT IS THE PROBLEM.”$"

MegaForest_Text_PercivalIntro:
	.string "I came here to find a legendary\n"
	.string "sword. I found a stick.\p"
	.string "I named it Excalibur II. It is not\n"
	.string "taking the pressure well.$"

MegaForest_Text_PercivalDefeat:
	.string "Excalibur II has asked to be\n"
	.string "called “Steve” from now on.$"

MegaForest_Text_PercivalPost:
	.string "Seven years I've searched this\n"
	.string "forest. Turns out the sword was\l"
	.string "at the entrance. Leaning on a log.\p"
	.string "Don't tell anyone. Especially me.$"

MegaForest_Text_MorganaIntro:
	.string "The forest whispers to me.\n"
	.string "Ancient secrets. Prophecies.\p"
	.string "Mostly about my posture, though.$"

MegaForest_Text_MorganaDefeat:
	.string "The trees are laughing at me.\n"
	.string "In Galarian. Rudely.$"

MegaForest_Text_MorganaPost:
	.string "Further in, two wolves sleep.\p"
	.string "One dreams of a sword, the other\n"
	.string "of a shield. I dream of dental\l"
	.string "insurance. We all have our quests.$"

MegaForest_Text_GwenIntro:
	.string "I came here for a picnic!\n"
	.string "That was in March.\p"
	.string "The squirrels took my car keys.\n"
	.string "And the car.$"

MegaForest_Text_GwenDefeat:
	.string "That's fine. I've made peace\n"
	.string "with the forest. And the squirrels.\l"
	.string "Mostly the squirrels.$"

MegaForest_Text_GwenPost:
	.string "Want a sandwich? It's from March.\n"
	.string "It's evolved. It knows Recover.$"
