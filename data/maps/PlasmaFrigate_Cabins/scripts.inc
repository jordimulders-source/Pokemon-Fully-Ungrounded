@ Project Grounded: Plasma Frigate, hutten (kopie van de S.S. Tidal-hutten). Kaart: tools/grounded/maptools/plasma_frigate.py
@ De onderste vier hutten hebben elk een terminal met de volgende kleurcode (VAR_PLASMA_FRIGATE 1->2->3->4->5).
@ Placeholderteksten; Jordi herschrijft ze via de Dialoogstudio.
PlasmaFrigate_Cabins_MapScripts::
	.byte 0

PlasmaFrigate_Cabins_EventScript_TerminalRed::
	lockall
	goto_if_ge VAR_PLASMA_FRIGATE, 2, PlasmaFrigate_Cabins_EventScript_RedRead
	msgbox PlasmaFrigate_Cabins_Text_TerminalRed, MSGBOX_DEFAULT
	setvar VAR_PLASMA_FRIGATE, 2
	playse SE_PC_LOGIN
	msgbox PlasmaFrigate_Cabins_Text_GotRed, MSGBOX_DEFAULT
	releaseall
	end

PlasmaFrigate_Cabins_EventScript_RedRead::
	msgbox PlasmaFrigate_Cabins_Text_RedRead, MSGBOX_DEFAULT
	releaseall
	end

PlasmaFrigate_Cabins_EventScript_TerminalBlue::
	lockall
	goto_if_ge VAR_PLASMA_FRIGATE, 3, PlasmaFrigate_Cabins_EventScript_BlueRead
	msgbox PlasmaFrigate_Cabins_Text_TerminalBlue, MSGBOX_DEFAULT
	setvar VAR_PLASMA_FRIGATE, 3
	playse SE_PC_LOGIN
	msgbox PlasmaFrigate_Cabins_Text_GotBlue, MSGBOX_DEFAULT
	releaseall
	end

PlasmaFrigate_Cabins_EventScript_BlueRead::
	msgbox PlasmaFrigate_Cabins_Text_BlueRead, MSGBOX_DEFAULT
	releaseall
	end

PlasmaFrigate_Cabins_EventScript_TerminalWhite::
	lockall
	goto_if_ge VAR_PLASMA_FRIGATE, 4, PlasmaFrigate_Cabins_EventScript_WhiteRead
	msgbox PlasmaFrigate_Cabins_Text_TerminalWhite, MSGBOX_DEFAULT
	setvar VAR_PLASMA_FRIGATE, 4
	playse SE_PC_LOGIN
	msgbox PlasmaFrigate_Cabins_Text_GotWhite, MSGBOX_DEFAULT
	releaseall
	end

PlasmaFrigate_Cabins_EventScript_WhiteRead::
	msgbox PlasmaFrigate_Cabins_Text_WhiteRead, MSGBOX_DEFAULT
	releaseall
	end

PlasmaFrigate_Cabins_EventScript_TerminalYellow::
	lockall
	goto_if_ge VAR_PLASMA_FRIGATE, 5, PlasmaFrigate_Cabins_EventScript_YellowRead
	msgbox PlasmaFrigate_Cabins_Text_TerminalYellow, MSGBOX_DEFAULT
	setvar VAR_PLASMA_FRIGATE, 5
	playse SE_PC_LOGIN
	msgbox PlasmaFrigate_Cabins_Text_GotYellow, MSGBOX_DEFAULT
	releaseall
	end

PlasmaFrigate_Cabins_EventScript_YellowRead::
	msgbox PlasmaFrigate_Cabins_Text_YellowRead, MSGBOX_DEFAULT
	releaseall
	end

PlasmaFrigate_Cabins_EventScript_Sleeper::
	msgbox PlasmaFrigate_Cabins_Text_Sleeper, MSGBOX_NPC
	end

PlasmaFrigate_Cabins_EventScript_Gossip::
	msgbox PlasmaFrigate_Cabins_Text_Gossip, MSGBOX_NPC
	end

PlasmaFrigate_Cabins_Text_TerminalRed:
	.string "Someone left a laptop under the\n"
	.string "pillow. The screen says:\p"
	.string "BURN DRIVE TEST LOG\n"
	.string "Day 1: Techno Blast is now Fire.\l"
	.string "Day 2: the lab is now also Fire.\p"
	.string "DOOR 2 PASSWORD: RED\n"
	.string "(please do not write this down)$"

PlasmaFrigate_Cabins_Text_GotRed:
	.string "You wrote it down.\n"
	.string "You now know the RED code.$"

PlasmaFrigate_Cabins_Text_RedRead:
	.string "BURN DRIVE TEST LOG\n"
	.string "Day 3: we bought a fire extinguisher.\l"
	.string "It was also on fire.$"

PlasmaFrigate_Cabins_Text_TerminalBlue:
	.string "A terminal on the table:\p"
	.string "DOUSE DRIVE TEST LOG\n"
	.string "Techno Blast is now Water.\l"
	.string "Genesect is not amused. Neither is\l"
	.string "the carpet.\p"
	.string "DOOR 3 PASSWORD: BLUE\n"
	.string "(it was going to be “WET”. Vetoed.)$"

PlasmaFrigate_Cabins_Text_GotBlue:
	.string "You now know the BLUE code.$"

PlasmaFrigate_Cabins_Text_BlueRead:
	.string "DOUSE DRIVE TEST LOG\n"
	.string "The carpet has filed a complaint.$"

PlasmaFrigate_Cabins_Text_TerminalWhite:
	.string "A frost-covered terminal:\p"
	.string "CHILL DRIVE TEST LOG\n"
	.string "Techno Blast is now Ice.\l"
	.string "ZINZOLIN cried. Happy tears.\l"
	.string "They froze. He's fine.\p"
	.string "DOOR 4 PASSWORD: WHITE$"

PlasmaFrigate_Cabins_Text_GotWhite:
	.string "You now know the WHITE code.$"

PlasmaFrigate_Cabins_Text_WhiteRead:
	.string "CHILL DRIVE TEST LOG\n"
	.string "Note: do not lick the Drive.\l"
	.string "Signed: everyone, from the infirmary.$"

PlasmaFrigate_Cabins_Text_TerminalYellow:
	.string "A terminal on the conference table:\p"
	.string "SHOCK DRIVE TEST LOG\n"
	.string "Techno Blast is now Electric.\l"
	.string "The ship's lights now flicker in\l"
	.string "time with the battle music.\p"
	.string "HOLD HATCH: RED, BLUE, WHITE,\n"
	.string "YELLOW. Guarded by the SHADOW TRIAD.\l"
	.string "Good luck finding them. Ha ha.$"

PlasmaFrigate_Cabins_Text_GotYellow:
	.string "You now know all four codes.\n"
	.string "The SHADOW TRIAD has a problem.$"

PlasmaFrigate_Cabins_Text_YellowRead:
	.string "MEETING AGENDA\n"
	.string "1. Genesect.\l"
	.string "2. Who keeps stealing the yogurts.\l"
	.string "3. Genesect again.$"

PlasmaFrigate_Cabins_Text_Sleeper:
	.string "Zzz… five more minutes…\n"
	.string "…I'll reform the world after lunch…$"

PlasmaFrigate_Cabins_Text_Gossip:
	.string "ZINZOLIN wanted the bug frozen.\n"
	.string "ROOD wanted the bug hugged.\p"
	.string "So now it's frozen AND hugged.\n"
	.string "That's called a compromise.$"
