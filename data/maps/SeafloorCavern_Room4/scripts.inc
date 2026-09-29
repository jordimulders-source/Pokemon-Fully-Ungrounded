SeafloorCavern_Room4_MapScripts::
	.byte 0

SeafloorCavern_Room4_EventScript_Grunt3::
	trainerbattle_single TRAINER_GRUNT_SEAFLOOR_CAVERN_3, SeafloorCavern_Room4_Text_Grunt3Intro, SeafloorCavern_Room4_Text_Grunt3Defeat
	msgbox SeafloorCavern_Room4_Text_Grunt3PostBattle, MSGBOX_AUTOCLOSE
	end

SeafloorCavern_Room4_EventScript_Grunt4::
	trainerbattle_single TRAINER_GRUNT_SEAFLOOR_CAVERN_4, SeafloorCavern_Room4_Text_Grunt4Intro, SeafloorCavern_Room4_Text_Grunt4Defeat
	msgbox SeafloorCavern_Room4_Text_Grunt4PostBattle, MSGBOX_AUTOCLOSE
	end

SeafloorCavern_Room4_Text_Grunt3Intro:
	.string "Who are you? Where'd you come from?\p"
	.string "The water cooler?$"

SeafloorCavern_Room4_Text_Grunt3Defeat:
	.string "Lost my fizz…$"

SeafloorCavern_Room4_Text_Grunt3PostBattle:
	.string "I can't find the way out!\p"
	.string "I'm not scared! Just… dehydrated.$"

SeafloorCavern_Room4_Text_Grunt4Intro:
	.string "Who are you? Where are you going?\p"
	.string "The bar's closed.$"

SeafloorCavern_Room4_Text_Grunt4Defeat:
	.string "I failed. Like a flat soda.$"

SeafloorCavern_Room4_Text_Grunt4PostBattle:
	.string "My partner forgot the map in the\n"
	.string "submarine.\p"
	.string "But he brought 40 bottles of PERRIER.$"

