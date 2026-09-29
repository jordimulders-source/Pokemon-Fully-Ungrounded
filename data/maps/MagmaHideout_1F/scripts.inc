MagmaHideout_1F_MapScripts::
	map_script MAP_SCRIPT_ON_TRANSITION, MagmaHideout_1F_OnTransition
	.byte 0

MagmaHideout_1F_OnTransition:
	setvar VAR_JAGGED_PASS_ASH_WEATHER, 0
	end

MagmaHideout_1F_EventScript_Grunt1::
	trainerbattle_single TRAINER_GRUNT_MAGMA_HIDEOUT_1, MagmaHideout_1F_Text_Grunt1Intro, MagmaHideout_1F_Text_Grunt1Defeat
	msgbox MagmaHideout_1F_Text_Grunt1PostBattle, MSGBOX_AUTOCLOSE
	end

MagmaHideout_1F_EventScript_Grunt2::
	trainerbattle_single TRAINER_GRUNT_MAGMA_HIDEOUT_2, MagmaHideout_1F_Text_Grunt2Intro, MagmaHideout_1F_Text_Grunt2Defeat
	msgbox MagmaHideout_1F_Text_Grunt2PostBattle, MSGBOX_AUTOCLOSE
	end

MagmaHideout_1F_Text_Grunt1Intro:
	.string "Roll call rule: whoever eats the most DA\n"
	.string "BOMB gets the best guard post. I came\l"
	.string "last.$"

MagmaHideout_1F_Text_Grunt1Defeat:
	.string "One drop and I cried.$"

MagmaHideout_1F_Text_Grunt1PostBattle:
	.string "I'll start with mild salsa…$"

MagmaHideout_1F_Text_Grunt2Intro:
	.string "Our leader told us to dig into MT.\n"
	.string "CHIMNEY. Perfect soil for peppers.$"

MagmaHideout_1F_Text_Grunt2Defeat:
	.string "Arrgh! I need milk!$"

MagmaHideout_1F_Text_Grunt2PostBattle:
	.string "I won't tell you the recipe. You'll taste\n"
	.string "it soon enough.$"

