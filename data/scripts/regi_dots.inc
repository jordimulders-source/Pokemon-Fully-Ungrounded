@ Project Grounded: de Regi-stippenpuzzel (zie src/regi_dots.c) en de gedeelde Regi-scripts

@ coord-trigger op elke stip (VAR_TEMP_0 = 0)
Common_EventScript_RegiDotStep::
	special RegiDots_Step
	goto_if_eq VAR_RESULT, 1, Common_EventScript_RegiDotGood
	goto_if_eq VAR_RESULT, 2, Common_EventScript_RegiDotWrong
	goto_if_eq VAR_RESULT, 3, Common_EventScript_RegiDotsSolved
	releaseall
	end

Common_EventScript_RegiDotGood::
	playse SE_SELECT
	releaseall
	end

Common_EventScript_RegiDotWrong::
	playse SE_FAILURE
	releaseall
	end

Common_EventScript_RegiDotsSolved::
	lockall
	playse SE_SELECT
	delay 30
	setvar VAR_0x8004, 1  @ vertical pan
	setvar VAR_0x8005, 1  @ horizontal pan
	setvar VAR_0x8006, 8  @ num shakes
	setvar VAR_0x8007, 5  @ shake delay
	special ShakeCamera
	waitstate
	playse SE_BANG
	special RegiDots_OpenEntrance
	msgbox Common_Text_RegiDotsSolved, MSGBOX_DEFAULT
	releaseall
	end

@ de muur met het oogpatroon: speelt de volgorde voor op de vloerstippen
Common_EventScript_RegiDotsMural::
	lockall
	msgbox Common_Text_RegiDotsMural, MSGBOX_DEFAULT
	closemessage
	delay 20
	setvar VAR_0x8004, 0
Common_EventScript_RegiDotsMuralLoop::
	special RegiDots_ShowStep
	goto_if_eq VAR_RESULT, FALSE, Common_EventScript_RegiDotsMuralDone
	playse SE_BALL_TRAY_BALL
	delay 32
	addvar VAR_0x8004, 1
	goto Common_EventScript_RegiDotsMuralLoop

Common_EventScript_RegiDotsMuralDone::
	delay 20
	special RegiDots_Reset
	releaseall
	end

@ verslagen (niet gevangen): de Regi valt uit elkaar maar zet zichzelf weer in elkaar
Common_EventScript_RegiCrumbled::
	fadescreenswapbuffers FADE_TO_BLACK
	removeobject VAR_LAST_TALKED
	fadescreenswapbuffers FADE_FROM_BLACK
	msgbox Common_Text_RegiCrumbled, MSGBOX_DEFAULT
	release
	end

@ na het vangen van een Regi: zijn ze nu alle vijf binnen? Dan gaat de tempel in Ashfrost open.
Common_EventScript_CheckRegigigasTemple::
	goto_if_unset FLAG_DEFEATED_REGIROCK, Common_EventScript_NopReturn
	goto_if_unset FLAG_DEFEATED_REGICE, Common_EventScript_NopReturn
	goto_if_unset FLAG_DEFEATED_REGISTEEL, Common_EventScript_NopReturn
	goto_if_unset FLAG_DEFEATED_REGIELEKI, Common_EventScript_NopReturn
	goto_if_unset FLAG_DEFEATED_REGIDRAGO, Common_EventScript_NopReturn
	goto_if_set FLAG_REGIGIGAS_TEMPLE_OPEN, Common_EventScript_NopReturn
	setflag FLAG_REGIGIGAS_TEMPLE_OPEN
	delay 30
	setvar VAR_0x8004, 1
	setvar VAR_0x8005, 1
	setvar VAR_0x8006, 12
	setvar VAR_0x8007, 6
	special ShakeCamera
	waitstate
	msgbox Common_Text_RegigigasTempleOpen, MSGBOX_DEFAULT
	return

Common_Text_RegiDotsMural:
	.string "Dots like the eyes of an ancient\n"
	.string "POKéMON are carved into the wall.\p"
	.string "The dots on the floor answer them. They\n"
	.string "light up, one by one...$"

Common_Text_RegiDotsSolved:
	.string "Every dot is blazing.\p"
	.string "With a grinding sound, the stone wall\n"
	.string "slides open!$"

Common_Text_RegiCrumbled:
	.string "It fell apart into a heap of rubble...\p"
	.string "But its dots are still faintly glowing.\n"
	.string "Give it a minute. It's reassembling\l"
	.string "itself out of spite.$"

Common_Text_RegigigasTempleOpen:
	.string "A deep rumble rolls in from far to the\n"
	.string "north...\p"
	.string "Something in ASHFROST has been waiting\n"
	.string "for exactly this many REGIs.$"
