@ Project Grounded: AbandonedShip_NightCabins (gegenereerd door tools/grounded/maptools/abandoned_ship_night.py; niet met de hand bewerken, teksten via de Dialoogstudio)
AbandonedShip_NightCabins_MapScripts::
	.byte 0

AbandonedShip_NightCabins_EventScript_Sailor::
	lock
	faceplayer
	msgbox AbandonedShip_NightCabins_Text_Sailor, MSGBOX_DEFAULT
	closemessage
	playse SE_M_NIGHTMARE
	fadescreen FADE_TO_BLACK
	removeobject VAR_LAST_TALKED
	setflag FLAG_HIDE_NIGHT_CABINS_SAILOR
	fadescreen FADE_FROM_BLACK
	msgbox AbandonedShip_NightCabins_Text_SailorGone, MSGBOX_DEFAULT
	release
	end

AbandonedShip_NightCabins_EventScript_Lampent::
	lock
	faceplayer
	playmoncry SPECIES_LAMPENT, CRY_MODE_NORMAL
	msgbox AbandonedShip_NightCabins_Text_Lampent, MSGBOX_DEFAULT
	waitmoncry
	release
	end

AbandonedShip_NightCabins_EventScript_Tuber::
	msgbox AbandonedShip_NightCabins_Text_Tuber, MSGBOX_NPC
	end

AbandonedShip_NightCabins_EventScript_Log::
	msgbox AbandonedShip_NightCabins_Text_Log, MSGBOX_SIGN
	end

AbandonedShip_NightCabins_EventScript_Trash::
	msgbox AbandonedShip_NightCabins_Text_Trash, MSGBOX_SIGN
	end

@ ---------------------------------------------------------------- teksten (placeholders, Jordi herschrijft ze)
AbandonedShip_NightCabins_Text_Sailor:
	.string "Evening, mate. Night watch? Me too.\n"
	.string "Been on night watch since the ship went\l"
	.string "down. Since the ship went DOWN TO THE\l"
	.string "DOCKS, I mean. For supplies.\p"
	.string "Ship's fine. Tight as a drum. The water\n"
	.string "in the corridor is decorative.\p"
	.string "Well, back to work. Don't tell the\n"
	.string "captain you saw me. Don't tell anyone\l"
	.string "you saw me. Technically, you can't have.$"

AbandonedShip_NightCabins_Text_SailorGone:
	.string "...The SAILOR is gone.\p"
	.string "His chair is still spinning. Slowly.\n"
	.string "Against the clock.$"

AbandonedShip_NightCabins_Text_Lampent:
	.string "LAMPENT is keeping watch over the\n"
	.string "cabin.\p"
	.string "It is also, very politely, sipping at\n"
	.string "your life force. It has a quota.\p"
	.string "It's a small quota. Please hold still.$"

AbandonedShip_NightCabins_Text_Tuber:
	.string "Do you want to play hide-and-seek? I'm\n"
	.string "really good at it.\p"
	.string "Nobody's found me in ages.\p"
	.string "My mom said she'd come looking right\n"
	.string "after dinner.$"

AbandonedShip_NightCabins_Text_Log:
	.string "SHIP'S LOG, NIGHT 14,610\p"
	.string "Weather: underwater.\n"
	.string "Morale: low.\l"
	.string "Pulse: none.\p"
	.string "The passenger in cabin 3 keeps asking\n"
	.string "when we dock. I have run out of polite\l"
	.string "ways to say “never”.$"

AbandonedShip_NightCabins_Text_Trash:
	.string "There's a note in the bin.\p"
	.string "“If found, please return my body to\n"
	.string "cabin 2.”\p"
	.string "This is cabin 2. You decide the note was\n"
	.string "not addressed to you.$"
