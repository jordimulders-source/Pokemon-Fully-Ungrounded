FortreeCity_Mart_MapScripts::
	.byte 0

FortreeCity_Mart_EventScript_Clerk::
	lock
	faceplayer
	message gText_HowMayIServeYou
	waitmessage
	badgemart FortreeCity_Mart_Pokemart
	msgbox gText_PleaseComeAgain, MSGBOX_DEFAULT
	release
	end

	.align 2
FortreeCity_Mart_Pokemart:
	.2byte ITEM_SIX_PACK
	pokemartlistend

FortreeCity_Mart_EventScript_Woman::
	msgbox FortreeCity_Mart_Text_SuperRepelBetter, MSGBOX_NPC
	end

FortreeCity_Mart_EventScript_Girl::
	msgbox FortreeCity_Mart_Text_StockUpOnItems, MSGBOX_NPC
	end

FortreeCity_Mart_EventScript_Boy::
	msgbox FortreeCity_Mart_Text_RareCandyMakesMonGrow, MSGBOX_NPC
	end

FortreeCity_Mart_Text_SuperRepelBetter:
	.string "SUPER REPEL lasts longer than REPEL.\p"
	.string "Longer than my last relationship.$"

FortreeCity_Mart_Text_StockUpOnItems:
	.string "I always buy more than I need.\p"
	.string "You never know.\p"
	.string "(She has 400 POTIONS.)$"

FortreeCity_Mart_Text_RareCandyMakesMonGrow:
	.string "A RARE CANDY: one level up.\p"
	.string "I eat them too. Nothing happens.$"

