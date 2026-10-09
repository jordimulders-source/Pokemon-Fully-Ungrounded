@ Project Grounded: PokemonTower_5F (tools/grounded/maptools/spacetime_cave.py)
PokemonTower_5F_MapScripts::
	.byte 0

PokemonTower_5F_EventScript_Ruth::
	trainerbattle_single TRAINER_TOWER_RUTH, PokemonTower_5F_Text_RuthIntro, PokemonTower_5F_Text_RuthDefeat
	msgbox PokemonTower_5F_Text_RuthPost, MSGBOX_AUTOCLOSE
	end

PokemonTower_5F_EventScript_Tammy::
	trainerbattle_single TRAINER_TOWER_TAMMY, PokemonTower_5F_Text_TammyIntro, PokemonTower_5F_Text_TammyDefeat
	msgbox PokemonTower_5F_Text_TammyPost, MSGBOX_AUTOCLOSE
	end

PokemonTower_5F_EventScript_Karina::
	trainerbattle_single TRAINER_TOWER_KARINA, PokemonTower_5F_Text_KarinaIntro, PokemonTower_5F_Text_KarinaDefeat
	msgbox PokemonTower_5F_Text_KarinaPost, MSGBOX_AUTOCLOSE
	end

PokemonTower_5F_EventScript_Caretaker::
	lock
	faceplayer
	goto_if_set FLAG_RECEIVED_POKEMON_TOWER_LIFE_ORB, PokemonTower_5F_EventScript_CaretakerDone
	msgbox PokemonTower_5F_Text_CaretakerGift, MSGBOX_DEFAULT
	giveitem ITEM_LIFE_ORB
	goto_if_eq VAR_RESULT, FALSE, Common_EventScript_ShowBagIsFull
	setflag FLAG_RECEIVED_POKEMON_TOWER_LIFE_ORB
PokemonTower_5F_EventScript_CaretakerDone::
	msgbox PokemonTower_5F_Text_CaretakerDone, MSGBOX_DEFAULT
	release
	end

@ ---------------------------------------------------------------- teksten (placeholders, Jordi herschrijft ze)
PokemonTower_5F_Text_RuthIntro:
	.string "We are the CHOIR of the top floor. We\n"
	.string "sing for the departed.\p"
	.string "You may join. Briefly. Permanently.$"

PokemonTower_5F_Text_RuthDefeat:
	.string "That note was flat. Like my team.$"

PokemonTower_5F_Text_RuthPost:
	.string "We don't actually sing. The acoustics up\n"
	.string "here are terrible.$"

PokemonTower_5F_Text_TammyIntro:
	.string "A hundred and eight spirits live in my\n"
	.string "SPIRITOMB. It gets crowded. They vote\l"
	.string "on everything.$"

PokemonTower_5F_Text_TammyDefeat:
	.string "The vote was unanimous. You win.$"

PokemonTower_5F_Text_TammyPost:
	.string "Upstairs is the caretaker. He's nice.\n"
	.string "Tips well. Mostly in items.$"

PokemonTower_5F_Text_KarinaIntro:
	.string "I lead the CHOIR. The MAROWAK in my\n"
	.string "party has been waiting a very long time\l"
	.string "for someone to finally fight it fair.$"

PokemonTower_5F_Text_KarinaDefeat:
	.string "...It's at peace. Or it's sulking. Hard to\n"
	.string "tell with skulls.$"

PokemonTower_5F_Text_KarinaPost:
	.string "Go on. The caretaker is waiting. He has\n"
	.string "been waiting since before the rift.$"

PokemonTower_5F_Text_CaretakerGift:
	.string "You climbed all the way up here? With\n"
	.string "the CHOIR and everything?\p"
	.string "I'm the caretaker. MR. FUJI left me in\n"
	.string "charge when he went to find himself.\l"
	.string "Twenty-five years ago.\p"
	.string "Here. Someone left this on a grave. It\n"
	.string "glows. I think it's a LIFE ORB, or a very\l"
	.string "determined nightlight.$"

PokemonTower_5F_Text_CaretakerDone:
	.string "Every soul up here had a trainer once.\p"
	.string "Take good care of yours. The paperwork\n"
	.string "for ghosts is unbelievable.$"
