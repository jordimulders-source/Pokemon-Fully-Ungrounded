@ Project Grounded: de galerij bovenin de vuurtoren van Beacon Isle (kopie van het dak van het Lilycove-warenhuis).
@ Vuurtorenwachter WICK en zijn LANTURN, die al 40 jaar de lamp is. Kaart en scripts: beacon_dragon.py.
BeaconIsle_Lighthouse_Top_MapScripts::
	.byte 0

BeaconIsle_Lighthouse_Top_EventScript_Wick::
	trainerbattle_single TRAINER_WICK, BeaconIsle_Lighthouse_Top_Text_WickIntro, BeaconIsle_Lighthouse_Top_Text_WickDefeat, BeaconIsle_Lighthouse_Top_EventScript_WickDefeated
	msgbox BeaconIsle_Lighthouse_Top_Text_WickPost, MSGBOX_AUTOCLOSE
	end

BeaconIsle_Lighthouse_Top_EventScript_WickDefeated::
	msgbox BeaconIsle_Lighthouse_Top_Text_WickGift, MSGBOX_DEFAULT
	giveitem ITEM_ZOOM_LENS
	msgbox BeaconIsle_Lighthouse_Top_Text_WickPost, MSGBOX_DEFAULT
	release
	end

BeaconIsle_Lighthouse_Top_EventScript_Lanturn::
	msgbox BeaconIsle_Lighthouse_Top_Text_Lanturn, MSGBOX_DEFAULT
	end

BeaconIsle_Lighthouse_Top_EventScript_View::
	msgbox BeaconIsle_Lighthouse_Top_Text_View, MSGBOX_SIGN
	end

@ ---------------------------------------------------------------- teksten (placeholders, Jordi herschrijft ze)
BeaconIsle_Lighthouse_Top_Text_WickGift:
	.string "Here. The old lens of the lighthouse.\p"
	.string "Turns out it was a camera lens all along.\n"
	.string "No wonder the light never reached the\l"
	.string "ships.$"

BeaconIsle_Lighthouse_Top_Text_WickIntro:
	.string "Up all those stairs just to look at a\n"
	.string "fish? Well. She is quite a fish.\p"
	.string "Forty years I've kept this light. The\n"
	.string "lamp broke in the first week. Since\l"
	.string "then: LANTURN.\p"
	.string "She works nights. I pay her in pilchards.\n"
	.string "Want to see what she can do?$"

BeaconIsle_Lighthouse_Top_Text_WickDefeat:
	.string "...She's still shining. That's what\n"
	.string "counts.$"

BeaconIsle_Lighthouse_Top_Text_WickPost:
	.string "Some ships still crash. But they crash\n"
	.string "in a lovely, steady glow.\p"
	.string "A man on ROUTE 134 wants to build his\n"
	.string "own lighthouse. He asked me what one\l"
	.string "looks like.\p"
	.string "I said “a fish.” He wrote it down.$"

BeaconIsle_Lighthouse_Top_Text_Lanturn:
	.string "LANTURN is glowing at roughly forty\n"
	.string "thousand lumens.\p"
	.string "It looks extremely proud of itself.$"

BeaconIsle_Lighthouse_Top_Text_View:
	.string "The whole sea, all the way to\n"
	.string "PACIFIDLOG.\p"
	.string "Somewhere out there, a ship is about to\n"
	.string "make a mistake.$"
