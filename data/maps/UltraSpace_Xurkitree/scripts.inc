UltraSpace_Xurkitree_MapScripts::
	.byte 0

UltraSpace_Xurkitree_EventScript_UB::
	lock
	faceplayer
	playmoncry SPECIES_XURKITREE, CRY_MODE_ENCOUNTER
	msgbox UltraSpace_Xurkitree_Text_UB, MSGBOX_DEFAULT
	waitmoncry
	closemessage
	setwildbattle SPECIES_XURKITREE, 89
	special BattleSetup_StartLegendaryBattle
	waitstate
	specialvar VAR_RESULT, GetBattleOutcome
	goto_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, UltraSpace_Xurkitree_EventScript_UBCaught
	goto_if_eq VAR_RESULT, B_OUTCOME_WON, UltraSpace_Xurkitree_EventScript_UBBack
	release
	end

UltraSpace_Xurkitree_EventScript_UBBack::
	msgbox UltraSpace_Xurkitree_Text_UBBack, MSGBOX_DEFAULT
	release
	end

UltraSpace_Xurkitree_EventScript_UBCaught::
	setflag FLAG_ULTRA_XURKITREE
	goto UltraSpace_EventScript_CaughtFade

UltraSpace_Xurkitree_EventScript_Spark::
	msgbox UltraSpace_Xurkitree_Text_Spark, MSGBOX_NPC
	end

UltraSpace_Xurkitree_EventScript_Cable::
	msgbox UltraSpace_Xurkitree_Text_Cable, MSGBOX_NPC
	end

@ ---------------------------------------------------------------- teksten (placeholders, Jordi herschrijft ze)
UltraSpace_Xurkitree_Text_UB:
	.string "XURKITREE is plugged into nothing and\n"
	.string "still pulling 40,000 volts.\p"
	.string "Your hair is standing up. So is your\n"
	.string "BIKE, somewhere in your BAG.$"

UltraSpace_Xurkitree_Text_UBBack:
	.string "XURKITREE reboots. Have you tried\n"
	.string "turning it off and on again? It did.$"

UltraSpace_Xurkitree_Text_Spark:
	.string "It is chewing on a cable. The cable is\n"
	.string "chewing back.$"

UltraSpace_Xurkitree_Text_Cable:
	.string "A tangle of cables shaped like\n"
	.string "XURKITREE. Or a XURKITREE shaped like\l"
	.string "cables.$"

