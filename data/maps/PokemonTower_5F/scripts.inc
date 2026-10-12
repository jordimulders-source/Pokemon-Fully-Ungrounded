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

PokemonTower_5F_EventScript_Agatha::
	lock
	faceplayer
	goto_if_set FLAG_SPACETIME_LAVENDER_DONE, PokemonTower_5F_EventScript_AgathaFreed
	playse SE_M_NIGHTMARE
	msgbox PokemonTower_5F_Text_AgathaIntro, MSGBOX_DEFAULT
	trainerbattle_single TRAINER_TOWER_AGATHA, PokemonTower_5F_Text_AgathaBattle, PokemonTower_5F_Text_AgathaDefeat, PokemonTower_5F_EventScript_AgathaDefeated
PokemonTower_5F_EventScript_AgathaFreed::
	msgbox PokemonTower_5F_Text_AgathaFreed, MSGBOX_DEFAULT
	release
	end

PokemonTower_5F_EventScript_AgathaDefeated::
	msgbox PokemonTower_5F_Text_AgathaLeaves, MSGBOX_DEFAULT
	closemessage
	playse SE_M_TELEPORT
	fadescreenspeed FADE_TO_WHITE, 4
	setflag FLAG_SPACETIME_LAVENDER_DONE
	setflag FLAG_HIDE_LAVENDER_GHOST_GENGAR
	setflag FLAG_HIDE_LAVENDER_GHOST_DUSKNOIR
	setflag FLAG_HIDE_LAVENDER_GHOST_BANETTE
	delay 30
	fadescreenspeed FADE_FROM_WHITE, 4
	msgbox PokemonTower_5F_Text_AgathaThanks, MSGBOX_DEFAULT
	msgbox PokemonTower_5F_Text_LavenderFreed, MSGBOX_DEFAULT
	release
	end

PokemonTower_5F_EventScript_Caretaker::
	lock
	faceplayer
	goto_if_unset FLAG_SPACETIME_LAVENDER_DONE, PokemonTower_5F_EventScript_CaretakerScared
	goto_if_set FLAG_RECEIVED_POKEMON_TOWER_LIFE_ORB, PokemonTower_5F_EventScript_CaretakerDone
	msgbox PokemonTower_5F_Text_CaretakerGift, MSGBOX_DEFAULT
	giveitem ITEM_LIFE_ORB
	goto_if_eq VAR_RESULT, FALSE, Common_EventScript_ShowBagIsFull
	setflag FLAG_RECEIVED_POKEMON_TOWER_LIFE_ORB
PokemonTower_5F_EventScript_CaretakerDone::
	msgbox PokemonTower_5F_Text_CaretakerDone, MSGBOX_DEFAULT
	release
	end

PokemonTower_5F_EventScript_CaretakerScared::
	msgbox PokemonTower_5F_Text_CaretakerScared, MSGBOX_DEFAULT
	release
	end

@ ---------------------------------------------------------------- teksten (placeholders, Jordi herschrijft ze)
PokemonTower_5F_Text_RuthIntro:
	.string "We are the CHOIR of the top floor. We\n"
	.string "sing for HER now.\p"
	.string "You may join. Briefly. Permanently.$"

PokemonTower_5F_Text_RuthDefeat:
	.string "That note was flat. And it was mine. I'm\n"
	.string "free!$"

PokemonTower_5F_Text_RuthPost:
	.string "We don't actually sing. The acoustics up\n"
	.string "here are terrible. SHE made us.$"

PokemonTower_5F_Text_TammyIntro:
	.string "A hundred and eight spirits live in my\n"
	.string "SPIRITOMB. A hundred and nine live in\l"
	.string "me. It gets crowded. They vote on\l"
	.string "everything.$"

PokemonTower_5F_Text_TammyDefeat:
	.string "The vote was unanimous. You win, and\n"
	.string "the hundred and ninth gets evicted.$"

PokemonTower_5F_Text_TammyPost:
	.string "Upstairs is AGATHA. Or something that\n"
	.string "used to be AGATHA. She brought the fog.$"

PokemonTower_5F_Text_KarinaIntro:
	.string "I lead the CHOIR. Or the thing behind my\n"
	.string "eyes does. It has terrible taste in\l"
	.string "hymns.$"

PokemonTower_5F_Text_KarinaDefeat:
	.string "...It's gone. My MAROWAK is staring at me\n"
	.string "like it knew all along.$"

PokemonTower_5F_Text_KarinaPost:
	.string "AGATHA is just ahead. The real one is\n"
	.string "still in there somewhere. Hit the other\l"
	.string "one first.$"

PokemonTower_5F_Text_AgathaIntro:
	.string "AGATHA stands perfectly still. Her eyes\n"
	.string "are the wrong color.\p"
	.string "“Oh, a visitor. How lovely. This old body\n"
	.string "has a lot of fight left in it. I'm\l"
	.string "borrowing it.”$"

PokemonTower_5F_Text_AgathaBattle:
	.string "“I made the fog. I made the CHANNELERS\n"
	.string "sing. I'll make you a GRAVE. A nice one.\l"
	.string "Near the window.”$"

PokemonTower_5F_Text_AgathaDefeat:
	.string "“Fine! FINE! There are other towns!\n"
	.string "Other dimensions!”$"

PokemonTower_5F_Text_AgathaLeaves:
	.string "Something black and screaming pours\n"
	.string "out of AGATHA and through the floor.\p"
	.string "The whole TOWER sighs.$"

PokemonTower_5F_Text_AgathaThanks:
	.string "AGATHA: ...Hm. Fifty years of training\n"
	.string "GHOSTS and one finally trains me.\p"
	.string "Thank you, child. Now go away before I\n"
	.string "get sentimental. It's bad for my image.$"

PokemonTower_5F_Text_LavenderFreed:
	.string "Far below, the fog over LAVENDER TOWN\n"
	.string "starts to lift.$"

PokemonTower_5F_Text_AgathaFreed:
	.string "AGATHA: The town is quiet again.\n"
	.string "Quiet-quiet, not haunted-quiet.\p"
	.string "If you see an old woman in a dimension\n"
	.string "that isn't this one, don't tell her about\l"
	.string "the possession. She'd never let me hear\l"
	.string "the end of it.$"

PokemonTower_5F_Text_CaretakerScared:
	.string "Psst. Don't look at her. That's AGATHA.\n"
	.string "Was AGATHA.\p"
	.string "She came up to deal with the ghosts and\n"
	.string "the ghosts dealt with her. Now she's the\l"
	.string "reason for the fog.$"

PokemonTower_5F_Text_CaretakerGift:
	.string "You climbed all the way up here? With\n"
	.string "the CHOIR and everything? And you got\l"
	.string "the thing out of AGATHA?\p"
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
