MossdeepCity_House3_MapScripts::
	.byte 0

MossdeepCity_House3_EventScript_SuperRodFisherman::
	lock
	faceplayer
	goto_if_set FLAG_RECEIVED_SUPER_ROD, MossdeepCity_House3_EventScript_ReceivedSuperRod
	msgbox MossdeepCity_House3_Text_YouWantSuperRod, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, MossdeepCity_House3_EventScript_DeclineSuperRod
	msgbox MossdeepCity_House3_Text_SuperRodIsSuper, MSGBOX_DEFAULT
	giveitem ITEM_SUPER_ROD
	goto_if_eq VAR_RESULT, FALSE, Common_EventScript_ShowBagIsFull
	setflag FLAG_RECEIVED_SUPER_ROD
	msgbox MossdeepCity_House3_Text_TryDroppingRodInWater, MSGBOX_DEFAULT
	release
	end

MossdeepCity_House3_EventScript_ReceivedSuperRod::
	msgbox MossdeepCity_House3_Text_GoAfterSeafloorPokemon, MSGBOX_DEFAULT
	release
	end

MossdeepCity_House3_EventScript_DeclineSuperRod::
	msgbox MossdeepCity_House3_Text_DontYouLikeToFish, MSGBOX_DEFAULT
	release
	end

MossdeepCity_House3_Text_YouWantSuperRod:
	.string "Hey, TRAINER! A SUPER ROD is really\n"
	.string "super!\p"
	.string "It catches POKéMON off the seafloor!\p"
	.string "You want it. I can see it in your eyes.$"

MossdeepCity_House3_Text_SuperRodIsSuper:
	.string "You bet! A SUPER ROD is SUPER!\p"
	.string "The name says it all. We're not creative\n"
	.string "here.$"

MossdeepCity_House3_Text_TryDroppingRodInWater:
	.string "Any water? Drop your ROD in and see\n"
	.string "what bites!\p"
	.string "Even puddles. Trust me.$"

MossdeepCity_House3_Text_DontYouLikeToFish:
	.string "Hunh? You don't like fishing?\p"
	.string "What do you do with your weekends,\n"
	.string "then?$"

MossdeepCity_House3_Text_GoAfterSeafloorPokemon:
	.string "Go get the seafloor POKéMON with your\n"
	.string "SUPER ROD.$"

