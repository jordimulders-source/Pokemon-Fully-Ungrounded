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
	.string "Kekeke... ke... sorry. That's not my\n"
	.string "laugh. I don't know whose laugh that is.$"

PokemonTower_3F_Text_PatriciaDefeat:
	.string "Kek. ...That one was mine. I think I'm\n"
	.string "back.$"

PokemonTower_3F_Text_PatriciaPost:
	.string "The spirits say you'll go far. They said\n"
	.string "that about the last guy. He's in the\l"
	.string "third row.$"

PokemonTower_3F_Text_CarlyIntro:
	.string "Be gone... living... thing... You're warm.\n"
	.string "Stop being warm. It's rude.$"

PokemonTower_3F_Text_CarlyDefeat:
	.string "Ugh. I'm cold again. Normal cold. Human\n"
	.string "cold.$"

PokemonTower_3F_Text_CarlyPost:
	.string "I wear this robe because it's warm. The\n"
	.string "chanting was the ghost's idea.$"

PokemonTower_3F_Text_HopeIntro:
	.string "My name is HOPE. The thing inside me\n"
	.string "finds that hilarious.$"

PokemonTower_3F_Text_HopeDefeat:
	.string "And there it goes. Out through the ears,\n"
	.string "I think.$"

PokemonTower_3F_Text_HopePost:
	.string "Every grave here has a name on it.\n"
	.string "Except the ones that have two.$"
