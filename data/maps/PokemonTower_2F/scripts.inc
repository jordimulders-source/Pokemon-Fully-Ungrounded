@ Project Grounded: PokemonTower_2F (tools/grounded/maptools/spacetime_cave.py)
PokemonTower_2F_MapScripts::
	.byte 0

PokemonTower_2F_EventScript_Maya::
	trainerbattle_single TRAINER_TOWER_MAYA, PokemonTower_2F_Text_MayaIntro, PokemonTower_2F_Text_MayaDefeat
	msgbox PokemonTower_2F_Text_MayaPost, MSGBOX_AUTOCLOSE
	end

PokemonTower_2F_EventScript_Channeler::
	msgbox PokemonTower_2F_Text_Channeler, MSGBOX_NPC
	end

@ ---------------------------------------------------------------- teksten (placeholders, Jordi herschrijft ze)
PokemonTower_2F_Text_MayaIntro:
	.string "Hey! You're not dead! How refreshing.\p"
	.string "I'll fix that. Spiritually.$"

PokemonTower_2F_Text_MayaDefeat:
	.string "Okay, okay, you're very alive. I get it.$"

PokemonTower_2F_Text_MayaPost:
	.string "I used to channel the dead. Now I\n"
	.string "mostly channel my frustration.$"

PokemonTower_2F_Text_Channeler:
	.string "The upper floors are full of ghosts.\n"
	.string "Real ones, this time.\p"
	.string "The real ghosts are nicer than the fake\n"
	.string "ones. Fewer opinions.$"
