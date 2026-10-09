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

UltraSpace_Pheromosa_EventScript_Judge::
	msgbox UltraSpace_Pheromosa_Text_Judge, MSGBOX_NPC
	end

UltraSpace_Pheromosa_EventScript_Crowd::
	msgbox UltraSpace_Pheromosa_Text_Crowd, MSGBOX_NPC
	end

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

UltraSpace_Pheromosa_Text_Judge:
	.string "The judge holds up a scorecard. It says\n"
	.string "“ew”.$"

UltraSpace_Pheromosa_Text_Crowd:
	.string "The audience claps politely, then stops\n"
	.string "when it realizes it has no idea why.$"

