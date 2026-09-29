Route111_WinstrateFamilysHouse_MapScripts::
	.byte 0

Route111_WinstrateFamilysHouse_EventScript_Victor::
	lock
	faceplayer
	setvar VAR_0x8008, LOCALID_WINSTRATE_HOUSE_VICTOR
	msgbox Route111_WinstrateFamilysHouse_Text_MySonIsStrongerThanYou, MSGBOX_DEFAULT
	goto Route111_WinstrateFamilysHouse_EventScript_FaceOriginalDirection
	end

Route111_WinstrateFamilysHouse_EventScript_Victoria::
	lock
	faceplayer
	setvar VAR_0x8008, LOCALID_WINSTRATE_HOUSE_VICTORIA
	goto_if_set FLAG_RECEIVED_MACHO_BRACE, Route111_WinstrateFamilysHouse_EventScript_ReceivedMachoBrace
	msgbox Route111_WinstrateFamilysHouse_Text_LikeYouToHaveMachoBrace, MSGBOX_DEFAULT
	giveitem ITEM_MACHO_BRACE
	goto_if_eq VAR_RESULT, FALSE, Common_EventScript_ShowBagIsFull
	setflag FLAG_RECEIVED_MACHO_BRACE
	goto Route111_WinstrateFamilysHouse_EventScript_FaceOriginalDirection
	end

Route111_WinstrateFamilysHouse_EventScript_ReceivedMachoBrace::
	msgbox Route111_WinstrateFamilysHouse_Text_PassionateAboutBattles, MSGBOX_DEFAULT
	goto Route111_WinstrateFamilysHouse_EventScript_FaceOriginalDirection
	end

Route111_WinstrateFamilysHouse_EventScript_Vivi::
	lock
	faceplayer
	setvar VAR_0x8008, LOCALID_WINSTRATE_HOUSE_VIVI
	msgbox Route111_WinstrateFamilysHouse_Text_StrongerFamilyMembers, MSGBOX_DEFAULT
	goto Route111_WinstrateFamilysHouse_EventScript_FaceOriginalDirection
	end

Route111_WinstrateFamilysHouse_EventScript_Vicky::
	lock
	faceplayer
	setvar VAR_0x8008, LOCALID_WINSTRATE_HOUSE_VICKY
	goto_if_set FLAG_TEMP_4, Route111_WinstrateFamilysHouse_EventScript_AlreadySpokenTo
	msgbox Route111_WinstrateFamilysHouse_Text_GrandsonStrong, MSGBOX_DEFAULT
	setflag FLAG_TEMP_4
	goto Route111_WinstrateFamilysHouse_EventScript_FaceOriginalDirection
	end

Route111_WinstrateFamilysHouse_EventScript_AlreadySpokenTo::
	msgbox Route111_WinstrateFamilysHouse_Text_GrandsonStrongShort, MSGBOX_DEFAULT
	goto Route111_WinstrateFamilysHouse_EventScript_FaceOriginalDirection
	end

Route111_WinstrateFamilysHouse_EventScript_FaceOriginalDirection::
	closemessage
	applymovement VAR_0x8008, Common_Movement_FaceOriginalDirection
	waitmovement 0
	release
	end

Route111_WinstrateFamilysHouse_Text_MySonIsStrongerThanYou:
	.string "You're the first TRAINER I've seen use\n"
	.string "POKéMON so masterfully.\p"
	.string "But my son is stronger than you.\p"
	.string "He took the POKéMON LEAGUE challenge!\p"
	.string "He hasn't called home since.$"

Route111_WinstrateFamilysHouse_Text_LikeYouToHaveMachoBrace:
	.string "We use this MACHO BRACE to strengthen\n"
	.string "our POKéMON. And VIVI.\p"
	.string "You beat all of us, so you can have it.\n"
	.string "There's a bit of drool on it. A lot,\l"
	.string "actually. It's mostly drool.$"

Route111_WinstrateFamilysHouse_Text_PassionateAboutBattles:
	.string "When it comes to battles, we're\n"
	.string "passionate.\p"
	.string "We battle at breakfast. For the last\n"
	.string "pancake.$"

Route111_WinstrateFamilysHouse_Text_StrongerFamilyMembers:
	.string "Mommy is stronger than Daddy. I'm\n"
	.string "stronger than Mommy. Grandma is\l"
	.string "stronger than me.\p"
	.string "Nobody is stronger than Grandma.\n"
	.string "Nobody.$"

Route111_WinstrateFamilysHouse_Text_GrandsonStrong:
	.string "You're strong. No doubt.\p"
	.string "But my grandson would make you cry.\p"
	.string "He's the strongest TRAINER our family\n"
	.string "knows.\p"
	.string "He must be fighting the CHAMPION by\n"
	.string "now.\p"
	.string "Or he's the CHAMPION already! He\n"
	.string "doesn't call, so who knows.$"

Route111_WinstrateFamilysHouse_Text_GrandsonStrongShort:
	.string "My grandson must be challenging the\n"
	.string "CHAMPION by now.\p"
	.string "Knowing him, he could BE the CHAMPION!\p"
	.string "He never calls, though.$"

