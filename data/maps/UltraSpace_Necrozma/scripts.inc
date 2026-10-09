UltraSpace_Necrozma_MapScripts::
	.byte 0

UltraSpace_Necrozma_EventScript_UB::
	lock
	faceplayer
	playmoncry SPECIES_NECROZMA, CRY_MODE_ENCOUNTER
	msgbox UltraSpace_Necrozma_Text_UB, MSGBOX_DEFAULT
	waitmoncry
	closemessage
	setwildbattle SPECIES_NECROZMA, 95
	special BattleSetup_StartLegendaryBattle
	waitstate
	specialvar VAR_RESULT, GetBattleOutcome
	goto_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, UltraSpace_Necrozma_EventScript_UBCaught
	goto_if_eq VAR_RESULT, B_OUTCOME_WON, UltraSpace_Necrozma_EventScript_UBBack
	release
	end

UltraSpace_Necrozma_EventScript_UBBack::
	msgbox UltraSpace_Necrozma_Text_UBBack, MSGBOX_DEFAULT
	release
	end

UltraSpace_Necrozma_EventScript_UBCaught::
	setflag FLAG_ULTRA_NECROZMA
	goto UltraSpace_EventScript_CaughtFade

@ ---------------------------------------------------------------- teksten (placeholders, Jordi herschrijft ze)
UltraSpace_Necrozma_Text_UB:
	.string "A POKéMON made of hungry darkness,\n"
	.string "sucking the light out of the prisms.\p"
	.string "It wants your light. You only have a\n"
	.string "flashlight app and a bad attitude.$"

UltraSpace_Necrozma_Text_UBBack:
	.string "NECROZMA folds back into the dark. The\n"
	.string "prisms dim. They're waiting for you.$"

