MauvilleCity_House1_MapScripts::
	.byte 0

MauvilleCity_House1_EventScript_RockSmashDude::
	lock
	faceplayer
	goto_if_set FLAG_RECEIVED_HM_ROCK_SMASH, MauvilleCity_House1_EventScript_ReceivedRockSmash
	msgbox MauvilleCity_House1_Text_ImRockSmashDudeTakeThis, MSGBOX_DEFAULT
	giveitem ITEM_HM_ROCK_SMASH
	setflag FLAG_RECEIVED_HM_ROCK_SMASH
	setflag FLAG_HIDE_ROUTE_111_ROCK_SMASH_TIP_GUY
	msgbox MauvilleCity_House1_Text_ExplainRockSmash, MSGBOX_DEFAULT
	release
	end

MauvilleCity_House1_EventScript_ReceivedRockSmash::
	msgbox MauvilleCity_House1_Text_MonCanFlyOutOfSmashedRock, MSGBOX_DEFAULT
	release
	end

MauvilleCity_House1_Text_ImRockSmashDudeTakeThis:
	.string "Woohoo!\p"
	.string "People call me the ROCK SMASH GUY.\n"
	.string "Degrading.\p"
	.string "I deserve respect. Call me ROCK SMASH\n"
	.string "DUDE.\p"
	.string "Woohoo!\p"
	.string "Your POKéMON look strong. Here, take\n"
	.string "this HIDDEN MACHINE!$"

MauvilleCity_House1_Text_ExplainRockSmash:
	.string "ROCK SMASH. It smashes rocks.\p"
	.string "Outside of battle, rocks. In battle,\n"
	.string "POKéMON. Rocks, mostly.$"

MauvilleCity_House1_Text_MonCanFlyOutOfSmashedRock:
	.string "If you smash a rock, a POKéMON might fly\n"
	.string "out.\p"
	.string "Or an item. Or nothing. Rocks are a\n"
	.string "gamble.\p"
	.string "Woohoo!$"

