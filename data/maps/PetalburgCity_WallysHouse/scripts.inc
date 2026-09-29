PetalburgCity_WallysHouse_MapScripts::
	map_script MAP_SCRIPT_ON_FRAME_TABLE, PetalburgCity_WallysHouse_OnFrame
	map_script MAP_SCRIPT_ON_WARP_INTO_MAP_TABLE, PetalburgCity_WallysHouse_OnWarp
	.byte 0

PetalburgCity_WallysHouse_OnWarp:
	map_script_2 VAR_PETALBURG_CITY_STATE, 4, PetalburgCity_WallysHouse_EventScript_PlayerWallysDadFaceEachOther
	.2byte 0

PetalburgCity_WallysHouse_EventScript_PlayerWallysDadFaceEachOther::
	turnobject LOCALID_PLAYER, DIR_EAST
	turnobject LOCALID_WALLYS_HOUSE_WALLYS_DAD, DIR_WEST
	end

PetalburgCity_WallysHouse_OnFrame:
	map_script_2 VAR_PETALBURG_CITY_STATE, 4, PetalburgCity_WallysHouse_EventScript_GiveHMSurf
	.2byte 0

PetalburgCity_WallysHouse_EventScript_GiveHMSurf::
	lockall
	msgbox PetalburgCity_WallysHouse_Text_PleaseExcuseUs, MSGBOX_DEFAULT
	giveitem ITEM_HM_SURF
	setflag FLAG_RECEIVED_HM_SURF
	msgbox PetalburgCity_WallysHouse_Text_SurfGoAllSortsOfPlaces, MSGBOX_DEFAULT
	setvar VAR_PETALBURG_CITY_STATE, 5
	releaseall
	end

PetalburgCity_WallysHouse_EventScript_WallysDad::
	lock
	faceplayer
	goto_if_set FLAG_DEFEATED_WALLY_VICTORY_ROAD, PetalburgCity_WallysHouse_EventScript_DefeatedWallyInVictoryRoad
	goto_if_set FLAG_RECEIVED_HM_SURF, PetalburgCity_WallysHouse_EventScript_ReceievedHMSurf
	goto_if_set FLAG_THANKED_FOR_PLAYING_WITH_WALLY, PetalburgCity_WallysHouse_EventScript_PlayedWithWally
	msgbox PetalburgCity_WallysHouse_Text_ThanksForPlayingWithWally, MSGBOX_DEFAULT
	setflag FLAG_THANKED_FOR_PLAYING_WITH_WALLY
	release
	end

PetalburgCity_WallysHouse_EventScript_ReceievedHMSurf::
	msgbox PetalburgCity_WallysHouse_Text_WallyIsComingHomeSoon, MSGBOX_DEFAULT
	release
	end

PetalburgCity_WallysHouse_EventScript_DefeatedWallyInVictoryRoad::
	msgbox PetalburgCity_WallysHouse_Text_YouMetWallyInEverGrandeCity, MSGBOX_DEFAULT
	release
	end

PetalburgCity_WallysHouse_EventScript_PlayedWithWally::
	msgbox PetalburgCity_WallysHouse_Text_WonderHowWallyIsDoing, MSGBOX_DEFAULT
	release
	end

PetalburgCity_WallysHouse_EventScript_WallysMom::
	lock
	faceplayer
	goto_if_set FLAG_RECEIVED_HM_SURF, PetalburgCity_WallysHouse_EventScript_ReceivedHMSurf
	msgbox PetalburgCity_WallysHouse_Text_WallyWasReallyHappy, MSGBOX_DEFAULT
	release
	end

PetalburgCity_WallysHouse_EventScript_ReceivedHMSurf::
	msgbox PetalburgCity_WallysHouse_Text_WallyLeftWithoutTelling, MSGBOX_DEFAULT
	release
	end

PetalburgCity_WallysHouse_Text_ThanksForPlayingWithWally:
	.string "You're… Ah, you must be {PLAYER}{KUN}, right?\p"
	.string "Thank you for playing with WALLY. That\n"
	.string "was very brave of you.\p"
	.string "He's been frail and sickly since he was a\n"
	.string "baby. And he doesn't talk very well. The\l"
	.string "speech therapist gave up.\p"
	.string "We've sent him to my relatives in\n"
	.string "VERDANTURF TOWN. The air is cleaner\l"
	.string "there.\p"
	.string "Where's WALLY? He already left. By\n"
	.string "himself! Can you believe it?$"

PetalburgCity_WallysHouse_Text_WonderHowWallyIsDoing:
	.string "I wonder how our WALLY is doing? I hope\n"
	.string "he remembered to breathe.$"

PetalburgCity_WallysHouse_Text_PleaseExcuseUs:
	.string "{PLAYER}{KUN}! Sorry for dragging you here.\p"
	.string "Our WALLY's become very healthy in\n"
	.string "VERDANTURF. He's still not the sharpest\l"
	.string "tool in the shed. But that's okay!\p"
	.string "You helped him catch a POKéMON. He\n"
	.string "talked about it for three weeks. We\l"
	.string "understood about half.\p"
	.string "This isn't a bribe or anything, but I'd\n"
	.string "really like you to have this.$"

PetalburgCity_WallysHouse_Text_SurfGoAllSortsOfPlaces:
	.string "If your POKéMON can SURF, you can go all\n"
	.string "sorts of places. WALLY can't. He'd drown\l"
	.string "in a puddle.$"

PetalburgCity_WallysHouse_Text_WallyIsComingHomeSoon:
	.string "WALLY's coming home soon! He walked ten\n"
	.string "steps outside last week. TEN! We threw\l"
	.string "a party.$"

PetalburgCity_WallysHouse_Text_YouMetWallyInEverGrandeCity:
	.string "You met WALLY in EVER GRANDE CITY?\n"
	.string "{PLAYER}{KUN}, don't be silly. WALLY gets lost\l"
	.string "in our garden.$"

PetalburgCity_WallysHouse_Text_WallyWasReallyHappy:
	.string "WALLY was so happy when he caught a\n"
	.string "POKéMON.\p"
	.string "He said: “POKéMON mine, WALLY happy,\n"
	.string "yes!” It's the longest sentence he's\l"
	.string "ever made.$"

PetalburgCity_WallysHouse_Text_WallyLeftWithoutTelling:
	.string "Keep this a secret from my husband…\p"
	.string "Our WALLY left VERDANTURF TOWN without\n"
	.string "telling anyone.\p"
	.string "He can barely order a sandwich, but he's\n"
	.string "surprisingly strong-willed.\p"
	.string "I'm sure he'll come back safe and sound.\n"
	.string "Probably. Maybe.$"

