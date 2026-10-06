@ Project Grounded: het spookschip S.S. AGAVE (zusterschip van de S.S. CACTUS / Abandoned Ship). Alleen 's nachts
@ te bereiken via het scheepswrakkenkerkhof (ShipwreckShoals). Zoektocht: de drie stukken van de schatkaart van
@ kapitein Grimsby (Morgan op het dek, de hut linksboven, de prullenbak van de kapitein).
GhostShip_Deck_MapScripts::
	.byte 0

GhostShip_Deck_EventScript_Silas::
	trainerbattle_single TRAINER_GHOST_SAILOR_SILAS, GhostShip_Deck_Text_SilasIntro, GhostShip_Deck_Text_SilasDefeat
	msgbox GhostShip_Deck_Text_SilasPostBattle, MSGBOX_AUTOCLOSE
	end

GhostShip_Deck_EventScript_Morgan::
	trainerbattle_single TRAINER_GHOST_SAILOR_MORGAN, GhostShip_Deck_Text_MorganIntro, GhostShip_Deck_Text_MorganDefeat, GhostShip_Deck_EventScript_MorganPiece
	goto_if_unset FLAG_GHOST_SHIP_PIECE_MORGAN, GhostShip_Deck_EventScript_MorganPiece
	msgbox GhostShip_Deck_Text_MorganPostBattle, MSGBOX_AUTOCLOSE
	end

GhostShip_Deck_EventScript_MorganPiece::
	lock
	faceplayer
	msgbox GhostShip_Deck_Text_MorganGivesPiece, MSGBOX_DEFAULT
	setflag FLAG_GHOST_SHIP_PIECE_MORGAN
	call GhostShip_EventScript_GotPiece
	release
	end

@ --- gedeeld door de kaarten van het spookschip ---
GhostShip_EventScript_CountPieces::
	setvar VAR_0x8004, 0
	call_if_set FLAG_GHOST_SHIP_PIECE_MORGAN, GhostShip_EventScript_AddPiece
	call_if_set FLAG_GHOST_SHIP_PIECE_CABIN, GhostShip_EventScript_AddPiece
	call_if_set FLAG_GHOST_SHIP_PIECE_BIN, GhostShip_EventScript_AddPiece
	buffernumberstring STR_VAR_1, VAR_0x8004
	return

GhostShip_EventScript_AddPiece:
	addvar VAR_0x8004, 1
	return

GhostShip_EventScript_GotPiece::
	call GhostShip_EventScript_CountPieces
	playfanfare MUS_OBTAIN_ITEM
	message GhostShip_Text_GotPiece
	waitmessage
	waitfanfare
	goto_if_eq VAR_0x8004, 3, GhostShip_EventScript_AllPieces
	msgbox GhostShip_Text_PieceMore, MSGBOX_DEFAULT
	return

GhostShip_EventScript_AllPieces:
	msgbox GhostShip_Text_PieceAll, MSGBOX_DEFAULT
	return

GhostShip_Text_GotPiece:
	.string "{PLAYER} found a piece of the\n"
	.string "TREASURE MAP! ({STR_VAR_1}/3)$"

GhostShip_Text_PieceMore:
	.string "Water stains, a skull doodle and half a\n"
	.string "coastline. The rest must be somewhere\l"
	.string "aboard.$"

GhostShip_Text_PieceAll:
	.string "The pieces fit together! It's a map of\n"
	.string "the SHIPWRECK SHOALS with a big X on\l"
	.string "it… and a doodle of a cat.\p"
	.string "The CAPTAIN should probably see this.$"

GhostShip_Deck_Text_SilasIntro:
	.string "LAND HO!\p"
	.string "…No, wait. That's a child. After two\n"
	.string "hundred years, everything looks like\l"
	.string "land.$"

GhostShip_Deck_Text_SilasDefeat:
	.string "I saw that loss coming from miles away.$"

GhostShip_Deck_Text_SilasPostBattle:
	.string "I've been on lookout duty since 1802.\n"
	.string "Nobody ever told me what I'm looking\l"
	.string "out for.$"

GhostShip_Deck_Text_MorganIntro:
	.string "Yarr. Dead for two hundred years and\n"
	.string "they STILL make me work nights.$"

GhostShip_Deck_Text_MorganDefeat:
	.string "I'd die of shame, but I'm all out of\n"
	.string "dying.$"

GhostShip_Deck_Text_MorganGivesPiece:
	.string "Fine, take this. A scrap of the\n"
	.string "CAPTAIN's map. I was using it as a\l"
	.string "napkin.\p"
	.string "For the soup. Don't ask about the soup.$"

GhostShip_Deck_Text_MorganPostBattle:
	.string "The CAPTAIN lost his map, you know. Tore\n"
	.string "it up in a rage, then forgot he did it.\l"
	.string "Classic GRIMSBY.$"
