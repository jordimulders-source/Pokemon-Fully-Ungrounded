@ Project Grounded: de galerij bovenin de vuurtoren van Beacon Isle (kopie van het dak van het Lilycove-warenhuis).
@ Vuurtorenwachter WICK en zijn LANTURN, die al 40 jaar de lamp is. 's Nachts LANTURN aanspreken: haar licht vindt het
@ Lichteiland achter het rif (FLAG_BEACON_LIGHT_ISLE_FOUND). Kaart en scripts: beacon_isle.py.
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
	lock
	faceplayer
	specialvar VAR_RESULT, IsNightTime
	goto_if_eq VAR_RESULT, FALSE, BeaconIsle_Lighthouse_Top_EventScript_LanturnDay
	goto_if_set FLAG_BEACON_LIGHT_ISLE_FOUND, BeaconIsle_Lighthouse_Top_EventScript_LanturnKnown
	msgbox BeaconIsle_Lighthouse_Top_Text_LanturnNight, MSGBOX_DEFAULT
	closemessage
	playse SE_M_REFLECT
	setflag FLAG_BEACON_LIGHT_ISLE_FOUND
	msgbox BeaconIsle_Lighthouse_Top_Text_LanturnReveal, MSGBOX_DEFAULT
	release
	end

BeaconIsle_Lighthouse_Top_EventScript_LanturnDay::
	msgbox BeaconIsle_Lighthouse_Top_Text_LanturnDay, MSGBOX_DEFAULT
	release
	end

BeaconIsle_Lighthouse_Top_EventScript_LanturnKnown::
	msgbox BeaconIsle_Lighthouse_Top_Text_LanturnKnown, MSGBOX_DEFAULT
	release
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
	.string "The keeper before me, old TALLOW, broke\n"
	.string "the lamp. Then he rowed off to the\l"
	.string "little island behind the reef. Never\l"
	.string "came back.\p"
	.string "He still sends a postcard every\n"
	.string "Christmas. Blank. Smells of candles.$"

BeaconIsle_Lighthouse_Top_Text_LanturnDay:
	.string "LANTURN is glowing at roughly forty\n"
	.string "thousand lumens.\p"
	.string "It looks extremely proud of itself.\p"
	.string "By day, nobody notices. LANTURN is\n"
	.string "saving her best work for the night\l"
	.string "shift.$"

BeaconIsle_Lighthouse_Top_Text_LanturnNight:
	.string "LANTURN swings her light out over the\n"
	.string "sea, slowly, like she's looking for her\l"
	.string "keys.$"

BeaconIsle_Lighthouse_Top_Text_LanturnReveal:
	.string "...There! Behind the reef, a tiny island\n"
	.string "lights up. A gap in the rocks glows\l"
	.string "white.\p"
	.string "It was there all along. It just never\n"
	.string "got the light.\p"
	.string "The gap in the reef is marked now. Ships\n"
	.string "may follow it. Ships may also not.$"

BeaconIsle_Lighthouse_Top_Text_LanturnKnown:
	.string "LANTURN keeps her beam on the gap in\n"
	.string "the reef.\p"
	.string "She has never been more professional.$"

BeaconIsle_Lighthouse_Top_Text_View:
	.string "The whole sea, all the way to\n"
	.string "PACIFIDLOG.\p"
	.string "Somewhere out there, a ship is about to\n"
	.string "make a mistake.$"
