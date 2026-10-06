@ Project Grounded: het scheepswrakkenkerkhof onder Route 131 (tools/grounded/maptools/shipwreck_shoals.py).
@ 's Nachts (echte klok) ligt het spookschip S.S. AGAVE op de ondiepte in het midden; overdag is het weg.
ShipwreckShoals_MapScripts::
	map_script MAP_SCRIPT_ON_LOAD, ShipwreckShoals_OnLoad
	.byte 0

ShipwreckShoals_OnLoad:
	specialvar VAR_RESULT, IsNightTime
	goto_if_eq VAR_RESULT, FALSE, ShipwreckShoals_EventScript_NoShip
	call ShipwreckShoals_EventScript_PlaceGhostShip
ShipwreckShoals_EventScript_NoShip:
	end

@ --- schip (gegenereerd) ---
ShipwreckShoals_EventScript_PlaceGhostShip::  @ gegenereerd door shipwreck_shoals.py
	setmetatile 19, 33, 0x200, FALSE
	setmetatile 20, 33, 0x201, FALSE
	setmetatile 21, 33, 0x202, FALSE
	setmetatile 22, 33, 0x203, FALSE
	setmetatile 18, 34, 0x204, TRUE
	setmetatile 19, 34, 0x205, TRUE
	setmetatile 20, 34, 0x206, TRUE
	setmetatile 21, 34, 0x207, TRUE
	setmetatile 22, 34, 0x208, TRUE
	setmetatile 23, 34, 0x209, TRUE
	setmetatile 18, 35, 0x20A, TRUE
	setmetatile 19, 35, 0x20B, TRUE
	setmetatile 20, 35, 0x20C, TRUE
	setmetatile 21, 35, 0x20D, TRUE
	setmetatile 22, 35, 0x20E, TRUE
	setmetatile 23, 35, 0x20F, TRUE
	setmetatile 19, 36, 0x210, FALSE
	setmetatile 20, 36, 0x211, FALSE
	setmetatile 21, 36, 0x212, FALSE
	return
@ --- einde schip ---

ShipwreckShoals_EventScript_Fisherman::
	lock
	faceplayer
	specialvar VAR_RESULT, IsNightTime
	goto_if_eq VAR_RESULT, TRUE, ShipwreckShoals_EventScript_FishermanNight
	goto_if_set FLAG_SHIPWRECK_TREASURE_FOUND, ShipwreckShoals_EventScript_FishermanTreasure
	msgbox ShipwreckShoals_Text_FishermanDay, MSGBOX_DEFAULT
	release
	end

ShipwreckShoals_EventScript_FishermanNight::
	msgbox ShipwreckShoals_Text_FishermanNight, MSGBOX_DEFAULT
	release
	end

ShipwreckShoals_EventScript_FishermanTreasure::
	msgbox ShipwreckShoals_Text_FishermanTreasure, MSGBOX_DEFAULT
	release
	end

@ De schat van kapitein Grimsby: aan de voet van de eenzame mast op de zuidelijke zandbank.
ShipwreckShoals_EventScript_TreasureSpot::
	lockall
	goto_if_set FLAG_SHIPWRECK_TREASURE_FOUND, ShipwreckShoals_EventScript_TreasureGone
	goto_if_unset FLAG_GHOST_SHIP_MAP_RETURNED, ShipwreckShoals_EventScript_JustSand
	msgbox ShipwreckShoals_Text_Dig, MSGBOX_DEFAULT
	playse SE_M_DIG
	waitse
	msgbox ShipwreckShoals_Text_Chest, MSGBOX_DEFAULT
	checkitemspace ITEM_CHOICE_BAND
	goto_if_eq VAR_RESULT, FALSE, ShipwreckShoals_EventScript_TreasureBagFull
	checkitemspace ITEM_PEARL_STRING, 2
	goto_if_eq VAR_RESULT, FALSE, ShipwreckShoals_EventScript_TreasureBagFull
	setflag FLAG_SHIPWRECK_TREASURE_FOUND
	giveitem ITEM_CHOICE_BAND
	giveitem ITEM_PEARL_STRING, 2
	msgbox ShipwreckShoals_Text_Sock, MSGBOX_DEFAULT
	releaseall
	end

ShipwreckShoals_EventScript_TreasureBagFull::
	msgbox ShipwreckShoals_Text_TreasureBagFull, MSGBOX_DEFAULT
	releaseall
	end

ShipwreckShoals_EventScript_JustSand::
	msgbox ShipwreckShoals_Text_JustSand, MSGBOX_DEFAULT
	releaseall
	end

ShipwreckShoals_EventScript_TreasureGone::
	msgbox ShipwreckShoals_Text_TreasureGone, MSGBOX_DEFAULT
	releaseall
	end

ShipwreckShoals_Text_FishermanDay:
	.string "Welcome to the SHIPWRECK SHOALS.\n"
	.string "Every ship that ever sank ends up\l"
	.string "here. It's like a retirement home,\l"
	.string "but with more barnacles.\p"
	.string "They say a ship sails into this fog\n"
	.string "at night. A ship with a full crew.\p"
	.string "A full crew of dead people. Union\n"
	.string "rules. Death doesn't end a contract.$"

ShipwreckShoals_Text_FishermanNight:
	.string "Don't look at it. The ship.\n"
	.string "In the middle of the shoals.\p"
	.string "…You looked at it.\p"
	.string "Well, now it knows your name.\n"
	.string "Ships are terrible gossips.$"

ShipwreckShoals_Text_FishermanTreasure:
	.string "You found the captain's treasure?\n"
	.string "I've been fishing on that sandbar\l"
	.string "for thirty years.\p"
	.string "Thirty years. On top of it.\n"
	.string "I'm going to need a minute.$"

ShipwreckShoals_Text_Dig:
	.string "The foot of the lonely mast.\n"
	.string "Exactly where the map says.\p"
	.string "{PLAYER} digs into the wet sand…$"

ShipwreckShoals_Text_Chest:
	.string "There's a chest! It says\n"
	.string "“PROPERTY OF CAPT. GRIMSBY.\l"
	.string "IF FOUND, I AM PROBABLY DEAD.”$"

ShipwreckShoals_Text_Sock:
	.string "At the bottom: one (1) sock and\n"
	.string "a note.\p"
	.string "“I kept the other sock. It is on my\n"
	.string "foot. Forever. -GRIMSBY”$"

ShipwreckShoals_Text_TreasureBagFull:
	.string "The chest is full, but so is your\n"
	.string "BAG. The sand politely covers it\l"
	.string "up again. Come back with room.$"

ShipwreckShoals_Text_JustSand:
	.string "Wet sand at the foot of an old mast.\n"
	.string "Suspiciously ordinary sand.\p"
	.string "Nobody ever buries anything under\n"
	.string "ordinary sand. Right?$"

ShipwreckShoals_Text_TreasureGone:
	.string "A hole in the sand, an empty chest\n"
	.string "and one very lonely sock.$"
