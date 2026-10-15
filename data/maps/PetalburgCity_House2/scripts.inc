PetalburgCity_House2_MapScripts::
	.byte 0

PetalburgCity_House2_EventScript_Woman::
	msgbox PetalburgCity_House2_Text_NormanBecameGymLeader, MSGBOX_NPC
	end

@ Project Grounded: eenmalige item-giveaway (testrun Jordi)
PetalburgCity_House2_EventScript_SchoolKid::
	lock
	faceplayer
	msgbox PetalburgCity_House2_Text_BattledNormanOnce, MSGBOX_DEFAULT
	goto_if_set FLAG_RECEIVED_PETALBURG_HOUSE2_GIFT, PetalburgCity_House2_EventScript_SchoolKid_GiftDone
	msgbox PetalburgCity_House2_Text_TakeBrightPowder, MSGBOX_DEFAULT
	giveitem ITEM_BRIGHT_POWDER
	goto_if_eq VAR_RESULT, FALSE, Common_EventScript_ShowBagIsFull
	setflag FLAG_RECEIVED_PETALBURG_HOUSE2_GIFT
PetalburgCity_House2_EventScript_SchoolKid_GiftDone::
	release
	end

PetalburgCity_House2_Text_NormanBecameGymLeader:
	.string "NORMAN is our new GYM LEADER.\p"
	.string "He moved his whole family here from\n"
	.string "JOHTO.\p"
	.string "Nobody asked the family.$"

PetalburgCity_House2_Text_BattledNormanOnce:
	.string "I battled NORMAN once. Way too strong.\p"
	.string "He lives for POKéMON.\p"
	.string "His kid has to walk to the next town to\n"
	.string "see him.$"

PetalburgCity_House2_Text_TakeBrightPowder:
	.string "Here, take my BRIGHT POWDER.\p"
	.string "It makes the foe's attacks miss.\n"
	.string "NORMAN's POKéMON did not miss.\l"
	.string "Not once. Not even out of pity.$"
