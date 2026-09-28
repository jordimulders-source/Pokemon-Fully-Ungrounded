AbandonedShip_Corridors_B1F_MapScripts::
	map_script MAP_SCRIPT_ON_RESUME, AbandonedShip_Corridors_B1F_OnResume
	map_script MAP_SCRIPT_ON_LOAD, AbandonedShip_Corridors_B1F_OnLoad
	.byte 0

AbandonedShip_Corridors_B1F_OnResume:
	setdivewarp MAP_ABANDONED_SHIP_UNDERWATER1, 5, 4
	end

AbandonedShip_Corridors_B1F_OnLoad:
	call_if_unset FLAG_USED_STORAGE_KEY, AbandonedShip_Corridors_B1F_EventScript_LockStorageRoom
	call_if_set FLAG_USED_STORAGE_KEY, AbandonedShip_Corridors_B1F_EventScript_UnlockStorageRoom
	end

AbandonedShip_Corridors_B1F_EventScript_LockStorageRoom::
	setmetatile 11, 4, METATILE_InsideShip_IntactDoor_Bottom_Locked, TRUE
	return

AbandonedShip_Corridors_B1F_EventScript_UnlockStorageRoom::
	setmetatile 11, 4, METATILE_InsideShip_IntactDoor_Bottom_Unlocked, TRUE
	return

AbandonedShip_Corridors_B1F_EventScript_TuberM::
	msgbox AbandonedShip_Corridors_B1F_Text_YayItsAShip, MSGBOX_NPC
	end

AbandonedShip_Corridors_B1F_EventScript_StorageRoomDoor::
	lockall
	goto_if_set FLAG_USED_STORAGE_KEY, AbandonedShip_Corridors_B1F_EventScript_DoorIsUnlocked
	checkitem ITEM_STORAGE_KEY
	goto_if_eq VAR_RESULT, FALSE, AbandonedShip_Corridors_B1F_EventScript_DoorIsLocked
	msgbox AbandonedShip_Corridors_B1F_Text_InsertedStorageKey, MSGBOX_DEFAULT
	playse SE_PIN
	removeitem ITEM_STORAGE_KEY
	setflag FLAG_USED_STORAGE_KEY
	call AbandonedShip_Corridors_B1F_EventScript_UnlockStorageRoom
	special DrawWholeMapView
	releaseall
	end

AbandonedShip_Corridors_B1F_EventScript_DoorIsLocked::
	msgbox AbandonedShip_Corridors_B1F_Text_DoorIsLocked, MSGBOX_DEFAULT
	releaseall
	end

AbandonedShip_Corridors_B1F_EventScript_DoorIsUnlocked::
	msgbox AbandonedShip_Text_TheDoorIsOpen, MSGBOX_DEFAULT
	releaseall
	end

AbandonedShip_Corridors_B1F_EventScript_Duncan::
	trainerbattle_single TRAINER_DUNCAN, AbandonedShip_Corridors_B1F_Text_DuncanIntro, AbandonedShip_Corridors_B1F_Text_DuncanDefeat
	msgbox AbandonedShip_Corridors_B1F_Text_DuncanPostBattle, MSGBOX_AUTOCLOSE
	end

AbandonedShip_Corridors_B1F_Text_DuncanIntro:
	.string "SAILING, SAILING, JUMPING OFF THE\n"
	.string "RAILING.$"

AbandonedShip_Corridors_B1F_Text_DuncanDefeat:
	.string "DRINKING, DRINKING, UNTIL THE SHIP IS\n"
	.string "SINKING.$"

AbandonedShip_Corridors_B1F_Text_DuncanPostBattle:
	.string "SO IF WE ALL COME TOGETHER.$"

AbandonedShip_Corridors_B1F_Text_YayItsAShip:
	.string "OH SHIT, I'M ON A FUCKING BOAT. WITH\n"
	.string "T-PAIN. I'M ON A BOAT MOTHERFUCKER\l"
	.string "TAKE A LOOK AT ME! NEVER THOUGHT I'D BE\l"
	.string "ON A BOAT, IT'S A BIG BLUE WATERY ROAD.\l"
	.string "POSEIDOOOOOON, LOOK AT MEEEEE!$"

AbandonedShip_Corridors_B1F_Text_DoorIsLocked:
	.string "The door is locked.\p"
	.string "“STORAGE” is painted on the door, with\n"
	.string "a suspicious lipstick like painting.$"

AbandonedShip_Corridors_B1F_Text_InsertedStorageKey:
	.string "{PLAYER} inserted and turned the\n"
	.string "STORAGE KEY.\p"
	.string "The inserted KEY stuck fast and broke\n"
	.string "the hell off, but the door opened.$"

AbandonedShip_Text_TheDoorIsOpen:
	.string "The door is open. But are you really\n"
	.string "sure you wanna go in?$"

