@ Project Grounded: LavenderTown (tools/grounded/maptools/spacetime_cave.py)
LavenderTown_MapScripts::
	.byte 0

LavenderTown_EventScript_LittleGirl::
	msgbox LavenderTown_Text_LittleGirl, MSGBOX_NPC
	end

LavenderTown_EventScript_Worker::
	msgbox LavenderTown_Text_Worker, MSGBOX_NPC
	end

LavenderTown_EventScript_Boy::
	msgbox LavenderTown_Text_Boy, MSGBOX_NPC
	end

LavenderTown_EventScript_TownSign::
	msgbox LavenderTown_Text_TownSign, MSGBOX_SIGN
	end

LavenderTown_EventScript_TowerSign::
	msgbox LavenderTown_Text_TowerSign, MSGBOX_SIGN
	end

LavenderTown_EventScript_HouseSign::
	msgbox LavenderTown_Text_HouseSign, MSGBOX_SIGN
	end

LavenderTown_EventScript_Notice::
	msgbox LavenderTown_Text_Notice, MSGBOX_SIGN
	end

@ ---------------------------------------------------------------- teksten (placeholders, Jordi herschrijft ze)
LavenderTown_Text_LittleGirl:
	.string "Do you believe in ghosts?\p"
	.string "My mom says they're just POKéMON. My\n"
	.string "dad says they're just POKéMON with\l"
	.string "unfinished business.\p"
	.string "My dad has a lot of unfinished business.$"

LavenderTown_Text_Worker:
	.string "We were going to renovate the TOWER.\n"
	.string "Then the rift opened and Kanto just...\l"
	.string "stopped updating.\p"
	.string "I've been on lunch break for\n"
	.string "twenty-five years.$"

LavenderTown_Text_Boy:
	.string "You came out of the purple hole! Cool!\p"
	.string "The last person who came out of it was a\n"
	.string "grumpy kid with spiky hair. He said\l"
	.string "'smell ya later' and went back in.$"

LavenderTown_Text_TownSign:
	.string "LAVENDER TOWN\n"
	.string "The Noble Purple Town\p"
	.string "(Population: fluctuating. Please count\n"
	.string "yourself twice to be sure.)$"

LavenderTown_Text_TowerSign:
	.string "POKéMON TOWER\n"
	.string "Becalm the spirits of POKéMON\p"
	.string "No running. No flash photography. No\n"
	.string "asking the CHANNELERS if they're okay.$"

LavenderTown_Text_HouseSign:
	.string "VOLUNTEER POKéMON HOUSE\p"
	.string "All POKéMON welcome. Ghosts by\n"
	.string "appointment.$"

LavenderTown_Text_Notice:
	.string "NOTICE\p"
	.string "Silph Scopes are no longer required. The\n"
	.string "ghosts have unionized and now identify\l"
	.string "themselves voluntarily.$"
