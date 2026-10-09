@ Project Grounded: PokemonTower_1F (tools/grounded/maptools/spacetime_cave.py)
PokemonTower_1F_MapScripts::
	.byte 0

PokemonTower_1F_EventScript_Receptionist::
	msgbox PokemonTower_1F_Text_Receptionist, MSGBOX_NPC
	end

PokemonTower_1F_EventScript_Mourner::
	msgbox PokemonTower_1F_Text_Mourner, MSGBOX_NPC
	end

PokemonTower_1F_EventScript_OldMan::
	msgbox PokemonTower_1F_Text_OldMan, MSGBOX_NPC
	end

@ ---------------------------------------------------------------- teksten (placeholders, Jordi herschrijft ze)
PokemonTower_1F_Text_Receptionist:
	.string "Welcome to POKéMON TOWER. Visiting\n"
	.string "hours are from dusk till dusk.\p"
	.string "Wild ghosts haunt the upper floors.\n"
	.string "They're harmless. Mostly. Legally\l"
	.string "speaking, entirely.$"

PokemonTower_1F_Text_Mourner:
	.string "I come here every day to visit my\n"
	.string "CLEFAIRY.\p"
	.string "She isn't buried here. She just likes it\n"
	.string "here. She's around the back, judging the\l"
	.string "décor.$"

PokemonTower_1F_Text_OldMan:
	.string "I've been coming here since this was all\n"
	.string "FRLG.\p"
	.string "The floor used to be green. Can you\n"
	.string "imagine? A green floor. In a graveyard.$"
