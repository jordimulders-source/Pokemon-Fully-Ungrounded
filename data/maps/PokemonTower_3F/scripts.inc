@ Project Grounded: PokemonTower_3F (tools/grounded/maptools/spacetime_cave.py)
PokemonTower_3F_MapScripts::
	.byte 0

PokemonTower_3F_EventScript_Patricia::
	trainerbattle_single TRAINER_TOWER_PATRICIA, PokemonTower_3F_Text_PatriciaIntro, PokemonTower_3F_Text_PatriciaDefeat
	msgbox PokemonTower_3F_Text_PatriciaPost, MSGBOX_AUTOCLOSE
	end

PokemonTower_3F_EventScript_Carly::
	trainerbattle_single TRAINER_TOWER_CARLY, PokemonTower_3F_Text_CarlyIntro, PokemonTower_3F_Text_CarlyDefeat
	msgbox PokemonTower_3F_Text_CarlyPost, MSGBOX_AUTOCLOSE
	end

PokemonTower_3F_EventScript_Hope::
	trainerbattle_single TRAINER_TOWER_HOPE, PokemonTower_3F_Text_HopeIntro, PokemonTower_3F_Text_HopeDefeat
	msgbox PokemonTower_3F_Text_HopePost, MSGBOX_AUTOCLOSE
	end

@ ---------------------------------------------------------------- teksten (placeholders, Jordi herschrijft ze)
PokemonTower_3F_Text_PatriciaIntro:
	.string "Kekeke... ke... sorry, I've had this cough\n"
	.string "since 1996.$"

PokemonTower_3F_Text_PatriciaDefeat:
	.string "Kek. That's the sound of me losing.$"

PokemonTower_3F_Text_PatriciaPost:
	.string "The spirits say you'll go far. They also\n"
	.string "said that about the last guy. He's in\l"
	.string "the third row.$"

PokemonTower_3F_Text_CarlyIntro:
	.string "Be gone... evil... spirit... oh, it's a kid.\n"
	.string "Same procedure.$"

PokemonTower_3F_Text_CarlyDefeat:
	.string "Fine! You may pass, evil kid.$"

PokemonTower_3F_Text_CarlyPost:
	.string "I wear this robe because it's warm. The\n"
	.string "chanting is optional.$"

PokemonTower_3F_Text_HopeIntro:
	.string "My name is HOPE. In this tower that's\n"
	.string "practically a joke.$"

PokemonTower_3F_Text_HopeDefeat:
	.string "And there it goes.$"

PokemonTower_3F_Text_HopePost:
	.string "Every grave here has a name on it.\n"
	.string "Except the ones that have two.$"
