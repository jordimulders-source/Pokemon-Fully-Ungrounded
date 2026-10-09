UltraSpace_Poipole_MapScripts::
	.byte 0

UltraSpace_Poipole_EventScript_Poipole::
	lock
	faceplayer
	playmoncry SPECIES_POIPOLE, CRY_MODE_NORMAL
	msgbox UltraSpace_Poipole_Text_PoipoleMon, MSGBOX_DEFAULT
	waitmoncry
	release
	end

UltraSpace_Poipole_EventScript_Alien0::
	lock
	faceplayer
	goto_if_set FLAG_ULTRA_POIPOLE, UltraSpace_Poipole_EventScript_AlienAfter
	msgbox UltraSpace_Poipole_Text_AlienGift, MSGBOX_DEFAULT
	setvar VAR_0x8004, SPECIES_POIPOLE
	setvar VAR_0x8005, 85
	setvar VAR_0x8006, ITEM_NONE
	call Grounded_EventScript_GiveGiftMon
	goto_if_eq VAR_RESULT, FALSE, UltraSpace_Poipole_EventScript_AlienNoRoom
	setflag FLAG_ULTRA_POIPOLE
	removeobject LOCALID_ULTRA_POIPOLE_MON
	msgbox UltraSpace_Poipole_Text_AlienBye, MSGBOX_DEFAULT
	release
	end

UltraSpace_Poipole_EventScript_AlienNoRoom::
	msgbox UltraSpace_Poipole_Text_AlienNoRoom, MSGBOX_DEFAULT
	release
	end

UltraSpace_Poipole_EventScript_AlienAfter::
	msgbox UltraSpace_Poipole_Text_AlienAfter, MSGBOX_DEFAULT
	release
	end

UltraSpace_Poipole_EventScript_Alien1::
	msgbox UltraSpace_Poipole_Text_Alien1, MSGBOX_NPC
	end

UltraSpace_Poipole_EventScript_Alien2::
	msgbox UltraSpace_Poipole_Text_Alien2, MSGBOX_NPC
	end

@ ---------------------------------------------------------------- teksten (placeholders, Jordi herschrijft ze)
UltraSpace_Poipole_Text_PoipoleMon:
	.string "POIPOLE: Beepu?\p"
	.string "It is wearing a tiny backpack. Someone\n"
	.string "loves this thing very much.$"

UltraSpace_Poipole_Text_AlienGift:
	.string "GREETINGS, FLESH-NOODLE.\p"
	.string "WE HAVE OBSERVED YOUR PLANET FOR\n"
	.string "SEVENTEEN (17) TELEVISION SEASONS.\p"
	.string "WE ARE DISAPPOINTED BY THE FINALE.\p"
	.string "TAKE THIS SMALL PURPLE ONE. IT EATS\n"
	.string "NOTHING AND SAYS “BEEPU”.\p"
	.string "WE CANNOT TAKE IT HOME. IT IS ALLERGIC\n"
	.string "TO HOME.$"

UltraSpace_Poipole_Text_AlienBye:
	.string "GOODBYE, FLESH-NOODLE. PLEASE RATE\n"
	.string "YOUR ABDUCTION FIVE STARS.$"

UltraSpace_Poipole_Text_AlienNoRoom:
	.string "YOUR POCKET-DIMENSIONS ARE FULL. WE\n"
	.string "WILL WAIT. WE ARE GOOD AT WAITING.\p"
	.string "WE HAVE BEEN WAITING SINCE THE\n"
	.string "DINOSAURS. THEY ALSO HAD NO ROOM.$"

UltraSpace_Poipole_Text_AlienAfter:
	.string "DOES THE PURPLE ONE STILL SAY\n"
	.string "“BEEPU”? GOOD. THAT MEANS IT IS\l"
	.string "WORKING.$"

UltraSpace_Poipole_Text_Alien1:
	.string "BLEEP. WE COME IN PEACE. WE LEAVE IN\n"
	.string "PIECES. LONG STORY.$"

UltraSpace_Poipole_Text_Alien2:
	.string "YOUR CRYSTALS ARE DELICIOUS. DO NOT\n"
	.string "LICK THE CRYSTALS.\p"
	.string "WE ARE ALLOWED. WE HAVE THE PAPERWORK.$"

