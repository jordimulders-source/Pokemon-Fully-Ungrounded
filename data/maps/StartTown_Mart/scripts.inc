StartTown_Mart_MapScripts::
	.byte 0

StartTown_Mart_EventScript_Clerk::
	lock
	faceplayer
	message gText_HowMayIServeYou
	waitmessage
	goto_if_set FLAG_ADVENTURE_STARTED, StartTown_Mart_ExpandedItems
	pokemart StartTown_Mart_Pokemart_Basic
	msgbox gText_PleaseComeAgain, MSGBOX_DEFAULT
	release
	end

	.align 2
StartTown_Mart_Pokemart_Basic:
	.2byte ITEM_POTION
	.2byte ITEM_ANTIDOTE
	.2byte ITEM_PARALYZE_HEAL
	.2byte ITEM_AWAKENING
	pokemartlistend

StartTown_Mart_ExpandedItems::
	badgemart StartTown_Mart_Pokemart_Expanded
	msgbox gText_PleaseComeAgain, MSGBOX_DEFAULT
	release
	end

	.align 2
StartTown_Mart_Pokemart_Expanded:
	pokemartlistend

StartTown_Mart_EventScript_Woman::
	lock
	faceplayer
	goto_if_set FLAG_ADVENTURE_STARTED, StartTown_Mart_EventScript_PokeBallsInStock
	msgbox StartTown_Mart_Text_PokeBallsAreSoldOut, MSGBOX_DEFAULT
	release
	end

StartTown_Mart_EventScript_PokeBallsInStock::
	msgbox StartTown_Mart_Text_ImGoingToBuyPokeBalls, MSGBOX_DEFAULT
	release
	end

StartTown_Mart_EventScript_Boy::
	msgbox StartTown_Mart_Text_RestoreHPWithPotion, MSGBOX_NPC
	end

StartTown_Mart_Text_PokeBallsAreSoldOut:
	.string "I always used to think of\n"
	.string "MART SMEETS when I saw MART.\p"
	.string "Senk joe.$"

StartTown_Mart_Text_ImGoingToBuyPokeBalls:
	.string "I'm going to buy a bunch of BALLS!\p"
	.string "MeatBALLS, GolfBALLS, BeachBALLS,\n"
	.string "SpeedBALLS, CueBALLS, GoofBALLS,\l"
	.string "BALLS BALLS BALLS BALLS\l"
	.string "BAAAAAAAAAAAAAAAAAAAAALLS!$"

StartTown_Mart_Text_RestoreHPWithPotion:
	.string "If a POKéMON gets hurt and loses\n"
	.string "its HP, it might lose its faith…\p"
	.string "In the hypercapitalist fake system\n"
	.string "that this world is held together by.\p"
	.string "It's up to you if you want\n"
	.string "this or not.$"
