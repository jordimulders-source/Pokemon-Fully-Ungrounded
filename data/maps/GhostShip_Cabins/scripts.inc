GhostShip_Cabins_MapScripts::
	.byte 0

GhostShip_Cabins_EventScript_Percy::
	trainerbattle_single TRAINER_GHOST_SAILOR_PERCY, GhostShip_Cabins_Text_PercyIntro, GhostShip_Cabins_Text_PercyDefeat
	msgbox GhostShip_Cabins_Text_PercyPostBattle, MSGBOX_AUTOCLOSE
	end

GhostShip_Cabins_EventScript_MapPiece::
	lock
	msgbox GhostShip_Cabins_Text_SoggyPaper, MSGBOX_DEFAULT
	removeobject VAR_LAST_TALKED
	setflag FLAG_GHOST_SHIP_PIECE_CABIN
	call GhostShip_EventScript_GotPiece
	release
	end

GhostShip_Cabins_EventScript_Widow::
	msgbox GhostShip_Cabins_Text_Widow, MSGBOX_NPC
	end

GhostShip_Cabins_EventScript_Husband::
	msgbox GhostShip_Cabins_Text_Husband, MSGBOX_NPC
	end

GhostShip_Cabins_Text_PercyIntro:
	.string "Do you MIND? This is my cabin. I've been\n"
	.string "haunting it since before haunting was\l"
	.string "cool.$"

GhostShip_Cabins_Text_PercyDefeat:
	.string "Fine. Haunt it yourself, then.$"

GhostShip_Cabins_Text_PercyPostBattle:
	.string "Cabin rules: no shoes, no knocking, no\n"
	.string "being alive. You're breaking two of\l"
	.string "them.$"

GhostShip_Cabins_Text_SoggyPaper:
	.string "A soggy scrap of paper is stuck under\n"
	.string "the bed. There's a coastline drawn on it.$"

GhostShip_Cabins_Text_Widow:
	.string "My husband went to sea and never came\n"
	.string "back.\p"
	.string "Then I went to sea too. Turns out he\n"
	.string "was in the cabin next door the whole\l"
	.string "time.\p"
	.string "We don't talk.$"

GhostShip_Cabins_Text_Husband:
	.string "My wife is in the cabin next door. We're\n"
	.string "on a break.\p"
	.string "Since 1902. It's going great.$"
