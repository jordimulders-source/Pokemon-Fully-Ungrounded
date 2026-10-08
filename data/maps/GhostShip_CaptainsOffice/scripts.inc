@ Kapitein Grimsby: geef hem de drie stukken van zijn schatkaart, versla hem (vakbondsregels) en hij vertelt waar
@ de schat ligt (ShipwreckShoals, voet van de eenzame mast op de zuidelijke zandbank).
GhostShip_CaptainsOffice_MapScripts::
	.byte 0

GhostShip_CaptainsOffice_EventScript_Captain::
	lock
	faceplayer
	goto_if_set FLAG_GHOST_SHIP_MAP_RETURNED, GhostShip_CaptainsOffice_EventScript_CaptainAfter
	call GhostShip_EventScript_CountPieces
	goto_if_eq VAR_0x8004, 3, GhostShip_CaptainsOffice_EventScript_CaptainHasMap
	msgbox GhostShip_CaptainsOffice_Text_LostMap, MSGBOX_DEFAULT
	release
	end

GhostShip_CaptainsOffice_EventScript_CaptainHasMap::
	msgbox GhostShip_CaptainsOffice_Text_YouFoundIt, MSGBOX_DEFAULT
	trainerbattle_single TRAINER_GRIMSBY, GhostShip_CaptainsOffice_Text_GrimsbyIntro, GhostShip_CaptainsOffice_Text_GrimsbyDefeat, GhostShip_CaptainsOffice_EventScript_CaptainBearings
	goto GhostShip_CaptainsOffice_EventScript_CaptainBearings

GhostShip_CaptainsOffice_EventScript_CaptainBearings::
	msgbox GhostShip_CaptainsOffice_Text_Bearings, MSGBOX_DEFAULT
	setflag FLAG_GHOST_SHIP_MAP_RETURNED
	release
	end

GhostShip_CaptainsOffice_EventScript_CaptainAfter::
	goto_if_set FLAG_SHIPWRECK_TREASURE_FOUND, GhostShip_CaptainsOffice_EventScript_CaptainTreasureFound
	msgbox GhostShip_CaptainsOffice_Text_Reminder, MSGBOX_DEFAULT
	release
	end

GhostShip_CaptainsOffice_EventScript_CaptainTreasureFound::
	msgbox GhostShip_CaptainsOffice_Text_TreasureFound, MSGBOX_DEFAULT
	release
	end

GhostShip_CaptainsOffice_EventScript_Bin::
	lockall
	goto_if_set FLAG_GHOST_SHIP_PIECE_BIN, GhostShip_CaptainsOffice_EventScript_BinEmpty
	msgbox GhostShip_CaptainsOffice_Text_Bin, MSGBOX_DEFAULT
	setflag FLAG_GHOST_SHIP_PIECE_BIN
	call GhostShip_EventScript_GotPiece
	releaseall
	end

GhostShip_CaptainsOffice_EventScript_BinEmpty::
	msgbox GhostShip_CaptainsOffice_Text_BinEmpty, MSGBOX_DEFAULT
	releaseall
	end

GhostShip_CaptainsOffice_Text_LostMap:
	.string "Ahoy. I am CAPTAIN GRIMSBY of the S.S.\n"
	.string "AGAVE. Sister ship of the S.S. CACTUS.\l"
	.string "Our parents had a theme.\p"
	.string "I've lost my treasure map. Torn into\n"
	.string "three pieces, like my marriage and my\l"
	.string "will to live. Well. To unlive.\p"
	.string "Bring me the pieces. You have {STR_VAR_1}\n"
	.string "of 3. I have nothing but time.$"

GhostShip_CaptainsOffice_Text_YouFoundIt:
	.string "The map! All three pieces!\p"
	.string "I'd thank you, but a ghost captain may\n"
	.string "not accept a favor without a duel first.\p"
	.string "It's in the union contract. Page 600. I\n"
	.string "wrote it myself.$"

GhostShip_CaptainsOffice_Text_GrimsbyIntro:
	.string "En garde! Or whatever sailors say. I was\n"
	.string "mostly in charge of the yelling.$"

GhostShip_CaptainsOffice_Text_GrimsbyDefeat:
	.string "Beaten by a landlubber. My crew will\n"
	.string "never let me hear the end of it. And\l"
	.string "they never end.$"

GhostShip_CaptainsOffice_Text_Bearings:
	.string "A deal is a deal. Look at the map: the\n"
	.string "lonely mast on the southern sandbar of\l"
	.string "the shoals.\p"
	.string "Dig at its foot. I'd go myself, but I'm\n"
	.string "legally dead and the sand gets\l"
	.string "everywhere.$"

GhostShip_CaptainsOffice_Text_Reminder:
	.string "The lonely mast, south. Its FOOT. Not\n"
	.string "its knee. Masts don't have knees. You\l"
	.string "knew that.$"

GhostShip_CaptainsOffice_Text_TreasureFound:
	.string "You found it? Good. Spend it on\n"
	.string "something nice. Like a second sock.$"

GhostShip_CaptainsOffice_Text_Bin:
	.string "The CAPTAIN's wastebasket. Inside:\n"
	.string "three apple cores, a will and…\p"
	.string "…a piece of the TREASURE MAP!\p"
	.string "He searched the whole ship except his\n"
	.string "own bin.$"

GhostShip_CaptainsOffice_Text_BinEmpty:
	.string "The CAPTAIN's wastebasket. Three apple\n"
	.string "cores and a will. The will leaves\l"
	.string "everything to the apple cores.$"
