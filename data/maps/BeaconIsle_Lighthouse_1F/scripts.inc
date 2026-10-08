@ Project Grounded: vuurtoren op Beacon Isle, begane grond (kopie van de Space Center 1F: tafels = zeekaarten).
@ Kaart en scripts: tools/grounded/maptools/beacon_dragon.py. Teksten zijn placeholders.
BeaconIsle_Lighthouse_1F_MapScripts::
	.byte 0

BeaconIsle_Lighthouse_1F_EventScript_Dylan::
	trainerbattle_single TRAINER_BEACON_DYLAN, BeaconIsle_Lighthouse_1F_Text_DylanIntro, BeaconIsle_Lighthouse_1F_Text_DylanDefeat
	msgbox BeaconIsle_Lighthouse_1F_Text_DylanPost, MSGBOX_AUTOCLOSE
	end

BeaconIsle_Lighthouse_1F_EventScript_Logbook::
	msgbox BeaconIsle_Lighthouse_1F_Text_Logbook, MSGBOX_SIGN
	end

BeaconIsle_Lighthouse_1F_EventScript_Charts::
	msgbox BeaconIsle_Lighthouse_1F_Text_Charts, MSGBOX_SIGN
	end

BeaconIsle_Lighthouse_1F_EventScript_Window::
	msgbox BeaconIsle_Lighthouse_1F_Text_Window, MSGBOX_SIGN
	end

@ ---------------------------------------------------------------- teksten (placeholders, Jordi herschrijft ze)
BeaconIsle_Lighthouse_1F_Text_DylanIntro:
	.string "I'm the foghorn of this lighthouse.\n"
	.string "Unpaid. Self-appointed.\p"
	.string "HONNNNK! Let's battle!$"

BeaconIsle_Lighthouse_1F_Text_DylanDefeat:
	.string "That was my last note.$"

BeaconIsle_Lighthouse_1F_Text_DylanPost:
	.string "The keeper says I'm “not a foghorn” and\n"
	.string "“not allowed in.”\p"
	.string "And yet here I am. In.$"

BeaconIsle_Lighthouse_1F_Text_Logbook:
	.string "KEEPER'S LOG.\n"
	.string "Day 1: Lamp broken.\l"
	.string "Day 2: Lamp still broken.\p"
	.string "Day 3: Found a LANTURN.\n"
	.string "Days 4 to 14,600: LANTURN.$"

BeaconIsle_Lighthouse_1F_Text_Charts:
	.string "Sea charts. Someone circled every rock\n"
	.string "around the island and wrote “NOT\l"
	.string "AGAIN.”$"

BeaconIsle_Lighthouse_1F_Text_Window:
	.string "You can see the ocean. The ocean can\n"
	.string "see you. Neither of you blinks.$"
