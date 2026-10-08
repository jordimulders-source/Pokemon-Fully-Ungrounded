AshfrostTown_Lodge_Rooms_MapScripts::
	.byte 0

@ Project Grounded: de vier kamers van de Ashfrost Lodge (ashfrost_lodge.py)
AshfrostTown_Lodge_Rooms_EventScript_Guest::
	msgbox AshfrostTown_Lodge_Rooms_Text_Guest, MSGBOX_NPC
	end

AshfrostTown_Lodge_Rooms_EventScript_Room2Bed::
	msgbox AshfrostTown_Lodge_Rooms_Text_Room2Bed, MSGBOX_SIGN
	end

AshfrostTown_Lodge_Rooms_EventScript_Ghost::
	msgbox AshfrostTown_Lodge_Rooms_Text_Ghost, MSGBOX_NPC
	end

AshfrostTown_Lodge_Rooms_EventScript_Beartic::
	lock
	playmoncry SPECIES_BEARTIC, CRY_MODE_NORMAL
	msgbox AshfrostTown_Lodge_Rooms_Text_Beartic, MSGBOX_DEFAULT
	waitmoncry
	release
	end

AshfrostTown_Lodge_Rooms_Text_Guest:
	.string "I checked out in 1998.\p"
	.string "The door froze shut that same night, so\n"
	.string "technically I'm still checking out.\p"
	.string "The OWNER says I'm not a guest. I'm a\n"
	.string "“situation.”$"

AshfrostTown_Lodge_Rooms_Text_Room2Bed:
	.string "This bed is made with military precision.\p"
	.string "The sheets are frozen into that shape.\n"
	.string "Nobody has ever been able to get in.$"

AshfrostTown_Lodge_Rooms_Text_Ghost:
	.string "Don't mind me. I'm the ghost of ROOM 3.\p"
	.string "Ghosts don't count as guests, so the\n"
	.string "OWNER can keep saying there's only one.\p"
	.string "I'm not dead, by the way. I just don't\n"
	.string "want to pay.$"

AshfrostTown_Lodge_Rooms_Text_Beartic:
	.string "A BEARTIC is asleep in the bed.\p"
	.string "A note on the nightstand: “Paid in full\n"
	.string "for the winter. In salmon. Do NOT wake.”\p"
	.string "Its snoring rattles the windows.$"
