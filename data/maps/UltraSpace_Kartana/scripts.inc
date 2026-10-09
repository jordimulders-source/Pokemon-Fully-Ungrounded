UltraSpace_Kartana_MapScripts::
	.byte 0

UltraSpace_Kartana_EventScript_UB::
	lock
	faceplayer
	playmoncry SPECIES_KARTANA, CRY_MODE_ENCOUNTER
	msgbox UltraSpace_Kartana_Text_UB, MSGBOX_DEFAULT
	waitmoncry
	closemessage
	setwildbattle SPECIES_KARTANA, 89
	special BattleSetup_StartLegendaryBattle
	waitstate
	specialvar VAR_RESULT, GetBattleOutcome
	goto_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, UltraSpace_Kartana_EventScript_UBCaught
	goto_if_eq VAR_RESULT, B_OUTCOME_WON, UltraSpace_Kartana_EventScript_UBBack
	release
	end

UltraSpace_Kartana_EventScript_UBBack::
	msgbox UltraSpace_Kartana_Text_UBBack, MSGBOX_DEFAULT
	release
	end

UltraSpace_Kartana_EventScript_UBCaught::
	setflag FLAG_ULTRA_KARTANA
	goto UltraSpace_EventScript_CaughtFade

UltraSpace_Kartana_EventScript_Fold::
	msgbox UltraSpace_Kartana_Text_Fold, MSGBOX_NPC
	end

@ ---------------------------------------------------------------- teksten (placeholders, Jordi herschrijft ze)
UltraSpace_Kartana_Text_UB:
	.string "A POKéMON made of paper, folded into a\n"
	.string "sword, folded into a POKéMON.\p"
	.string "It could cut you. Mostly it just gives\n"
	.string "you papercuts and an attitude.$"

UltraSpace_Kartana_Text_UBBack:
	.string "KARTANA refolds itself. Origami is\n"
	.string "mostly about not giving up.$"

UltraSpace_Kartana_Text_Fold:
	.string "A folded paper KARTANA. It is not alive.\n"
	.string "Probably. Do not unfold it.$"

