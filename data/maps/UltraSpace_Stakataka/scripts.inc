UltraSpace_Stakataka_MapScripts::
	.byte 0

UltraSpace_Stakataka_EventScript_UB::
	lock
	faceplayer
	playmoncry SPECIES_STAKATAKA, CRY_MODE_ENCOUNTER
	msgbox UltraSpace_Stakataka_Text_UB, MSGBOX_DEFAULT
	waitmoncry
	closemessage
	setwildbattle SPECIES_STAKATAKA, 90
	special BattleSetup_StartLegendaryBattle
	waitstate
	specialvar VAR_RESULT, GetBattleOutcome
	goto_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, UltraSpace_Stakataka_EventScript_UBCaught
	goto_if_eq VAR_RESULT, B_OUTCOME_WON, UltraSpace_Stakataka_EventScript_UBBack
	release
	end

UltraSpace_Stakataka_EventScript_UBBack::
	msgbox UltraSpace_Stakataka_Text_UBBack, MSGBOX_DEFAULT
	release
	end

UltraSpace_Stakataka_EventScript_UBCaught::
	setflag FLAG_ULTRA_STAKATAKA
	goto UltraSpace_EventScript_CaughtFade

UltraSpace_Stakataka_EventScript_Wall::
	msgbox UltraSpace_Stakataka_Text_Wall, MSGBOX_NPC
	end

@ ---------------------------------------------------------------- teksten (placeholders, Jordi herschrijft ze)
UltraSpace_Stakataka_Text_UB:
	.string "The wall is looking at you.\p"
	.string "One brick in particular is looking at you\n"
	.string "really hard.$"

UltraSpace_Stakataka_Text_UBBack:
	.string "The bricks reshuffle. The wall is still\n"
	.string "looking at you. Harder now.$"

UltraSpace_Stakataka_Text_Wall:
	.string "The wall looks at you. You look at the\n"
	.string "wall. Nobody blinks. Bricks can't blink.$"

