SeafloorCavern_Room3_MapScripts::
	.byte 0

SeafloorCavern_Room3_EventScript_Shelly::
	trainerbattle_single TRAINER_SHELLY_SEAFLOOR_CAVERN, SeafloorCavern_Room3_Text_ShellyIntro, SeafloorCavern_Room3_Text_ShellyDefeat
	msgbox SeafloorCavern_Room3_Text_ShellyPostBattle, MSGBOX_AUTOCLOSE
	end

SeafloorCavern_Room3_EventScript_Grunt5::
	trainerbattle_single TRAINER_GRUNT_SEAFLOOR_CAVERN_5, SeafloorCavern_Room3_Text_Grunt5Intro, SeafloorCavern_Room3_Text_Grunt5Defeat
	msgbox SeafloorCavern_Room3_Text_Grunt5PostBattle, MSGBOX_AUTOCLOSE
	end

SeafloorCavern_Room3_Text_ShellyIntro:
	.string "Ahahahaha!\p"
	.string "No submarine? Impressive!\p"
	.string "The BOSS is about to wake KYOGRE.\p"
	.string "Imagine an ocean of sparkling water!$"

SeafloorCavern_Room3_Text_ShellyDefeat:
	.string "Ahahahaha!\p"
	.string "Ouch!$"

SeafloorCavern_Room3_Text_ShellyPostBattle:
	.string "So strong. What a waste.\p"
	.string "You'd look great holding a SPA ROOD.$"

SeafloorCavern_Room3_Text_Grunt5Intro:
	.string "For our dream we need the power of\n"
	.string "POKéMON.\p"
	.string "And a lot of CO2.$"

SeafloorCavern_Room3_Text_Grunt5Defeat:
	.string "Gwah! Fizzled out!$"

SeafloorCavern_Room3_Text_Grunt5PostBattle:
	.string "We don't question the leader.\p"
	.string "Even the part about carbonating the\n"
	.string "sea.$"

