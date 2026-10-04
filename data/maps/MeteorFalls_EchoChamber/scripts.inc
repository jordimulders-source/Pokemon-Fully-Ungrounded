@ Project Grounded: de echokamer (kaart: tools/grounded/maptools/meteor_falls_ext.py).
@ Roep in het donker; de echo verraadt het gat onder de brokkelrots in de gangen (doodlopend, midden).

MeteorFalls_EchoChamber_MapScripts::
	.byte 0

MeteorFalls_EchoChamber_EventScript_Shout::
	lock
	msgbox MeteorFalls_EchoChamber_Text_Shout, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, MeteorFalls_EchoChamber_EventScript_NoShout
	msgbox MeteorFalls_EchoChamber_Text_Echo, MSGBOX_DEFAULT
	release
	end

MeteorFalls_EchoChamber_EventScript_NoShout::
	msgbox MeteorFalls_EchoChamber_Text_NoShout, MSGBOX_DEFAULT
	release
	end

MeteorFalls_EchoChamber_Text_Shout:
	.string "The wall here curves like a giant ear.\n"
	.string "Shout into the dark?$"

MeteorFalls_EchoChamber_Text_NoShout:
	.string "You stay quiet. Somewhere in the dark,\n"
	.string "something is disappointed in you.$"

MeteorFalls_EchoChamber_Text_Echo:
	.string "{PLAYER}: HELLO?\p"
	.string "…hello… …llo… …lo…\p"
	.string "…the rock… in the middle… where the\n"
	.string "tunnels end… sits on nothing…\p"
	.string "…smash it… fall… fall… all…\p"
	.string "…also your fly is open… open… pen…$"
