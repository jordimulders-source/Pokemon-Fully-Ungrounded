AshfrostTown_Lodge_2F_MapScripts::
	.byte 0

@ Project Grounded: gang van de Ashfrost Lodge (ashfrost_lodge.py)
AshfrostTown_Lodge_2F_EventScript_Maid::
	msgbox AshfrostTown_Lodge_2F_Text_Maid, MSGBOX_NPC
	end

AshfrostTown_Lodge_2F_EventScript_Room1Sign::
	msgbox AshfrostTown_Lodge_2F_Text_Room1Sign, MSGBOX_SIGN
	end

AshfrostTown_Lodge_2F_EventScript_Room2Sign::
	msgbox AshfrostTown_Lodge_2F_Text_Room2Sign, MSGBOX_SIGN
	end

AshfrostTown_Lodge_2F_EventScript_Room3Sign::
	msgbox AshfrostTown_Lodge_2F_Text_Room3Sign, MSGBOX_SIGN
	end

AshfrostTown_Lodge_2F_EventScript_Room4Sign::
	msgbox AshfrostTown_Lodge_2F_Text_Room4Sign, MSGBOX_SIGN
	end

AshfrostTown_Lodge_2F_Text_Maid:
	.string "Housekeeping! I fold the towels into\n"
	.string "little SWABLU.\p"
	.string "By morning they've frozen solid. The\n"
	.string "MART downstairs sells them as ICE\l"
	.string "STONES.\p"
	.string "Please don't tell anyone. It's my\n"
	.string "pension.$"

AshfrostTown_Lodge_2F_Text_Room1Sign:
	.string "ROOM 1\n"
	.string "“DO NOT DISTURB.”\p"
	.string "The sign is frozen to the door. So is the\n"
	.string "door.$"

AshfrostTown_Lodge_2F_Text_Room2Sign:
	.string "ROOM 2\n"
	.string "VACANT. Has been vacant since the\l"
	.string "grand opening.$"

AshfrostTown_Lodge_2F_Text_Room3Sign:
	.string "ROOM 3\n"
	.string "OCCUPIED.\p"
	.string "According to the guest book, nobody\n"
	.string "has ever checked in.$"

AshfrostTown_Lodge_2F_Text_Room4Sign:
	.string "ROOM 4\n"
	.string "LONG-TERM GUEST.\l"
	.string "Please knock. Then run.$"
