UltraSpace_Blacephalon_MapScripts::
	.byte 0

UltraSpace_Blacephalon_EventScript_UB::
	lock
	faceplayer
	playmoncry SPECIES_BLACEPHALON, CRY_MODE_ENCOUNTER
	msgbox UltraSpace_Blacephalon_Text_UB, MSGBOX_DEFAULT
	waitmoncry
	closemessage
	setwildbattle SPECIES_BLACEPHALON, 90
	special BattleSetup_StartLegendaryBattle
	waitstate
	specialvar VAR_RESULT, GetBattleOutcome
	goto_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, UltraSpace_Blacephalon_EventScript_UBCaught
	goto_if_eq VAR_RESULT, B_OUTCOME_WON, UltraSpace_Blacephalon_EventScript_UBBack
	release
	end

UltraSpace_Blacephalon_EventScript_UBBack::
	msgbox UltraSpace_Blacephalon_Text_UBBack, MSGBOX_DEFAULT
	release
	end

UltraSpace_Blacephalon_EventScript_UBCaught::
	setflag FLAG_ULTRA_BLACEPHALON
	goto UltraSpace_EventScript_CaughtFade

UltraSpace_Blacephalon_EventScript_Clown::
	msgbox UltraSpace_Blacephalon_Text_Clown, MSGBOX_NPC
	end

@ ---------------------------------------------------------------- teksten (placeholders, Jordi herschrijft ze)
UltraSpace_Blacephalon_Text_UB:
	.string "BLACEPHALON juggles its own head.\p"
	.string "It drops it, on purpose, and it explodes.\n"
	.string "The crowd goes wild. Your eyebrows go\l"
	.string "home.$"

UltraSpace_Blacephalon_Text_UBBack:
	.string "BLACEPHALON grows a new head and\n"
	.string "takes a bow. The crowd demands an\l"
	.string "encore.$"

UltraSpace_Blacephalon_Text_Clown:
	.string "A clown. Its makeup is real. Its smile is\n"
	.string "not. Welcome to the circus.$"

