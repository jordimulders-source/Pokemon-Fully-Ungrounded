UltraSpace_Pheromosa_MapScripts::
	.byte 0

UltraSpace_Pheromosa_EventScript_UB::
	lock
	faceplayer
	playmoncry SPECIES_PHEROMOSA, CRY_MODE_ENCOUNTER
	msgbox UltraSpace_Pheromosa_Text_UB, MSGBOX_DEFAULT
	waitmoncry
	closemessage
	setwildbattle SPECIES_PHEROMOSA, 88
	special BattleSetup_StartLegendaryBattle
	waitstate
	specialvar VAR_RESULT, GetBattleOutcome
	goto_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, UltraSpace_Pheromosa_EventScript_UBCaught
	goto_if_eq VAR_RESULT, B_OUTCOME_WON, UltraSpace_Pheromosa_EventScript_UBBack
	release
	end

UltraSpace_Pheromosa_EventScript_UBBack::
	msgbox UltraSpace_Pheromosa_Text_UBBack, MSGBOX_DEFAULT
	release
	end

UltraSpace_Pheromosa_EventScript_UBCaught::
	setflag FLAG_ULTRA_PHEROMOSA
	goto UltraSpace_EventScript_CaughtFade

@ ---------------------------------------------------------------- teksten (placeholders, Jordi herschrijft ze)
UltraSpace_Pheromosa_Text_UB:
	.string "PHEROMOSA strikes a pose at the end of\n"
	.string "the catwalk.\p"
	.string "It refuses to look at you. You are not\n"
	.string "in its tax bracket.$"

UltraSpace_Pheromosa_Text_UBBack:
	.string "PHEROMOSA walks back to the start of\n"
	.string "the catwalk. Again. Forever. Fashion is\l"
	.string "pain.$"

@ ultra_worlds_a { gegenereerd door tools/grounded/maptools/ultra_worlds_a.py; niet met de hand bewerken
UltraSpace_Pheromosa_EventScript_Weather::
	msgbox UltraSpace_Pheromosa_Text_Weather, MSGBOX_NPC
	end

UltraSpace_Pheromosa_EventScript_Treaty::
	msgbox UltraSpace_Pheromosa_Text_Treaty, MSGBOX_SIGN
	end
@ } ultra_worlds_a

UltraSpace_Pheromosa_Text_Treaty:
	.string "THE ELEMENTAL TREATY\p"
	.string "Article 1: Nothing affects anything.\n"
	.string "Article 2: See article 1.\p"
	.string "Article 3: Fire may sit in water if it\n"
	.string "wants to. Water is fine with it.$"

UltraSpace_Pheromosa_Text_Weather:
	.string "It tried to change the weather. The\n"
	.string "weather did not care.\p"
	.string "Nothing here cares. It is very relaxing,\n"
	.string "in a horrifying way.$"
