@ Project Grounded: PokemonTower_4F (tools/grounded/maptools/spacetime_cave.py)
PokemonTower_4F_MapScripts::
	.byte 0

PokemonTower_4F_EventScript_Laurel::
	trainerbattle_single TRAINER_TOWER_LAUREL, PokemonTower_4F_Text_LaurelIntro, PokemonTower_4F_Text_LaurelDefeat
	msgbox PokemonTower_4F_Text_LaurelPost, MSGBOX_AUTOCLOSE
	end

PokemonTower_4F_EventScript_Jody::
	trainerbattle_single TRAINER_TOWER_JODY, PokemonTower_4F_Text_JodyIntro, PokemonTower_4F_Text_JodyDefeat
	msgbox PokemonTower_4F_Text_JodyPost, MSGBOX_AUTOCLOSE
	end

PokemonTower_4F_EventScript_Paula::
	trainerbattle_single TRAINER_TOWER_PAULA, PokemonTower_4F_Text_PaulaIntro, PokemonTower_4F_Text_PaulaDefeat
	msgbox PokemonTower_4F_Text_PaulaPost, MSGBOX_AUTOCLOSE
	end

@ ---------------------------------------------------------------- teksten (placeholders, Jordi herschrijft ze)
PokemonTower_4F_Text_LaurelIntro:
	.string "GHOST! Oh. No. That's my reflection.\n"
	.string "Long night.$"

PokemonTower_4F_Text_LaurelDefeat:
	.string "I need a nap. In a coffin, ideally.$"

PokemonTower_4F_Text_LaurelPost:
	.string "The tower used to be quiet. Then that\n"
	.string "hole in spacetime opened and now we get\l"
	.string "tourists.$"

PokemonTower_4F_Text_JodyIntro:
	.string "I can see five spirits behind you. One\n"
	.string "of them is rolling its eyes.$"

PokemonTower_4F_Text_JodyDefeat:
	.string "The eye-roller says 'told you so'.$"

PokemonTower_4F_Text_JodyPost:
	.string "My HOUNDSTONE is a good boy. Was a good\n"
	.string "boy. Remains, technically, a good boy.$"

PokemonTower_4F_Text_PaulaIntro:
	.string "Shhh. You'll wake them. And they are SO\n"
	.string "cranky in the morning.$"

PokemonTower_4F_Text_PaulaDefeat:
	.string "...They're awake. Thanks.$"

PokemonTower_4F_Text_PaulaPost:
	.string "Please walk softly. Some of them are\n"
	.string "light sleepers. All of them are heavy\l"
	.string "grudge-holders.$"
