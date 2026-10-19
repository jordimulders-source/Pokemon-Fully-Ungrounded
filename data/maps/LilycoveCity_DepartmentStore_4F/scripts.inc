LilycoveCity_DepartmentStore_4F_MapScripts::
	.byte 0

LilycoveCity_DepartmentStore_4F_EventScript_Gentleman::
	msgbox LilycoveCity_DepartmentStore_4F_Text_AttackOrDefenseTM, MSGBOX_NPC
	end

LilycoveCity_DepartmentStore_4F_EventScript_Woman::
	goto_if_set FLAG_RECEIVED_TM_SUPER_SPLASH, LilycoveCity_DepartmentStore_4F_EventScript_WomanTM100
	msgbox LilycoveCity_DepartmentStore_4F_Text_FiftyDifferentTMs, MSGBOX_NPC
	end

@ Project Grounded: zodra je TM100 (Super Splash) hebt, weet ze dat er een honderdste bestaat.
LilycoveCity_DepartmentStore_4F_EventScript_WomanTM100::
	msgbox LilycoveCity_DepartmentStore_4F_Text_HundredTMs, MSGBOX_NPC
	end

LilycoveCity_DepartmentStore_4F_EventScript_Youngster::
	msgbox LilycoveCity_DepartmentStore_4F_Text_PokemonOnlyHaveFourMoves, MSGBOX_NPC
	end

@ Project Grounded: Hyper Beam is niet meer te koop; deze fan deelt hem uit.
LilycoveCity_DepartmentStore_4F_EventScript_HyperFan::
	lock
	faceplayer
	goto_if_set FLAG_RECEIVED_TM_HYPER_BEAM, LilycoveCity_DepartmentStore_4F_EventScript_HyperFanAfter
	msgbox LilycoveCity_DepartmentStore_4F_Text_HyperFan, MSGBOX_DEFAULT
	giveitem ITEM_TM_HYPER_BEAM
	goto_if_eq VAR_RESULT, FALSE, Common_EventScript_BagIsFull
	setflag FLAG_RECEIVED_TM_HYPER_BEAM
	msgbox LilycoveCity_DepartmentStore_4F_Text_HyperFanExplain, MSGBOX_DEFAULT
	release
	end

LilycoveCity_DepartmentStore_4F_EventScript_HyperFanAfter::
	msgbox LilycoveCity_DepartmentStore_4F_Text_HyperFanAfter, MSGBOX_DEFAULT
	release
	end

LilycoveCity_DepartmentStore_4F_EventScript_ClerkLeft::
	lock
	faceplayer
	message gText_HowMayIServeYou
	waitmessage
	pokemart LilycoveCity_DepartmentStore_4F_Pokemart_AttackTMs
	msgbox gText_PleaseComeAgain, MSGBOX_DEFAULT
	release
	end

	.align 2
LilycoveCity_DepartmentStore_4F_Pokemart_AttackTMs:
	.2byte ITEM_TM_FIRE_BLAST
	.2byte ITEM_TM_THUNDER
	.2byte ITEM_TM_BLIZZARD
	.2byte ITEM_TM_POWER_GEM
	pokemartlistend

LilycoveCity_DepartmentStore_4F_EventScript_ClerkRight::
	lock
	faceplayer
	message gText_HowMayIServeYou
	waitmessage
	pokemart LilycoveCity_DepartmentStore_4F_Pokemart_DefenseTMs
	msgbox gText_PleaseComeAgain, MSGBOX_DEFAULT
	release
	end

	.align 2
LilycoveCity_DepartmentStore_4F_Pokemart_DefenseTMs:
	.2byte ITEM_TM_PROTECT
	.2byte ITEM_TM_U_TURN
	.2byte ITEM_TM_REFLECT
	.2byte ITEM_TM_LIGHT_SCREEN
	.2byte ITEM_TM_SUBSTITUTE @ Project Grounded: TM78
	.2byte ITEM_TM_BATON_PASS @ Project Grounded: TM79
	pokemartlistend

LilycoveCity_DepartmentStore_4F_Text_AttackOrDefenseTM:
	.string "HERO in Smash is bad enough. Random\n"
	.string "crits, random instakills. Fine.\p"
	.string "But INCINEROAR? That wrestling cat\n"
	.string "taunts, takes the hit and REVENGES me\l"
	.string "off the stage. My blood boils.$"

LilycoveCity_DepartmentStore_4F_Text_FiftyDifferentTMs:
	.string "There are 99 kinds of TMs.\p"
	.string "I have 98.\p"
	.string "I can't sleep.$"

LilycoveCity_DepartmentStore_4F_Text_HundredTMs:
	.string "Is that… TM100?\p"
	.string "There are A HUNDRED kinds now?\n"
	.string "Since WHEN?\p"
	.string "I have 98. Two missing.\p"
	.string "I'm never sleeping again.$"

LilycoveCity_DepartmentStore_4F_Text_PokemonOnlyHaveFourMoves:
	.string "A POKéMON can learn four moves.\n"
	.string "INCINEROAR only needs two: Fake Out\l"
	.string "and Parting Shot.$"


LilycoveCity_DepartmentStore_4F_Text_HyperFan:
	.string "HYPER BEAM!\p"
	.string "THE MOST POWERFUL MOVE\n"
	.string "IN POKéMON!\p"
	.string "NOT EVEN SUPER!\n"
	.string "BUT HYPER!!\p"
	.string "They stopped SELLING it here.\n"
	.string "Cowards. Take mine.$"

LilycoveCity_DepartmentStore_4F_Text_HyperFanExplain:
	.string "After you fire it, your POKéMON\n"
	.string "has to recharge for a turn.\p"
	.string "That's not a weakness. That's it\n"
	.string "catching its breath after being\l"
	.string "THAT AWESOME.$"

LilycoveCity_DepartmentStore_4F_Text_HyperFanAfter:
	.string "Did you use it yet? DID YOU?\p"
	.string "Don't tell me if it missed.\n"
	.string "I don't want to know.$"
