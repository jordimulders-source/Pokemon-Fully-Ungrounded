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
	.string "The voice in my head says I should fix\n"
	.string "that. It's very persuasive. It has a\l"
	.string "podcast.$"

PokemonTower_2F_Text_MayaDefeat:
	.string "The voice... stopped? Oh, thank\n"
	.string "goodness. It never let me pick the\l"
	.string "music.$"

PokemonTower_2F_Text_MayaPost:
	.string "Something up there is wearing people\n"
	.string "like coats. I was a coat. Zero stars.$"

PokemonTower_2F_Text_Channeler:
	.string "The upper floors are full of ghosts.\n"
	.string "Real ones, this time.\p"
	.string "The real ghosts are nicer than the fake\n"
	.string "ones. Fewer opinions.$"
