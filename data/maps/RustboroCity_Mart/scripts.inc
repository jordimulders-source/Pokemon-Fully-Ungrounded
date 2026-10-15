RustboroCity_Mart_MapScripts::
	.byte 0

RustboroCity_Mart_EventScript_Clerk::
	lock
	faceplayer
	message gText_HowMayIServeYou
	waitmessage
	goto_if_unset FLAG_MET_DEVON_EMPLOYEE, RustboroCity_Mart_EventScript_PokemartBasic
	goto_if_set FLAG_MET_DEVON_EMPLOYEE, RustboroCity_Mart_EventScript_PokemartExpanded
	end

RustboroCity_Mart_EventScript_PokemartBasic::
	badgemart RustboroCity_Mart_Pokemart_Basic
	msgbox gText_PleaseComeAgain, MSGBOX_DEFAULT
	release
	end

	.align 2
RustboroCity_Mart_Pokemart_Basic:
	.2byte ITEM_X_SPEED
	.2byte ITEM_X_ATTACK
	.2byte ITEM_X_DEFENSE
	pokemartlistend

RustboroCity_Mart_EventScript_PokemartExpanded::
	badgemart RustboroCity_Mart_Pokemart_Expanded
	msgbox gText_PleaseComeAgain, MSGBOX_DEFAULT
	release
	end

	.align 2
RustboroCity_Mart_Pokemart_Expanded:
	.2byte ITEM_TIMER_BALL
	.2byte ITEM_REPEAT_BALL
	.2byte ITEM_X_SPEED
	.2byte ITEM_X_ATTACK
	.2byte ITEM_X_DEFENSE
	pokemartlistend

RustboroCity_Mart_EventScript_PokefanF::
	msgbox RustboroCity_Mart_Text_BuyingHealsInCaseOfShroomish, MSGBOX_NPC
	end

RustboroCity_Mart_EventScript_Boy::
	msgbox RustboroCity_Mart_Text_ShouldBuySuperPotionsInstead, MSGBOX_NPC
	end

RustboroCity_Mart_EventScript_BugCatcher::
	msgbox RustboroCity_Mart_Text_GettingEscapeRopeJustInCase, MSGBOX_NPC
	end

RustboroCity_Mart_Text_BuyingHealsInCaseOfShroomish:
	.string "PARLYZ HEALS and ANTIDOTES.\p"
	.string "For SHROOMISH in PETALBURG WOODS.\p"
	.string "Those things are evil.$"

RustboroCity_Mart_Text_ShouldBuySuperPotionsInstead:
	.string "My POKéMON evolved.\p"
	.string "Now I need SUPER POTIONS.\p"
	.string "Evolution is expensive.$"

RustboroCity_Mart_Text_GettingEscapeRopeJustInCase:
	.string "An ESCAPE ROPE. In case I get lost.\p"
	.string "Or in case of a bad date.$"

