UltraSpace_Nihilego_MapScripts::
	.byte 0

UltraSpace_Nihilego_EventScript_UB::
	lock
	faceplayer
	playmoncry SPECIES_NIHILEGO, CRY_MODE_ENCOUNTER
	msgbox UltraSpace_Nihilego_Text_UB, MSGBOX_DEFAULT
	waitmoncry
	closemessage
	setwildbattle SPECIES_NIHILEGO, 88
	special BattleSetup_StartLegendaryBattle
	waitstate
	specialvar VAR_RESULT, GetBattleOutcome
	goto_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, UltraSpace_Nihilego_EventScript_UBCaught
	goto_if_eq VAR_RESULT, B_OUTCOME_WON, UltraSpace_Nihilego_EventScript_UBBack
	release
	end

UltraSpace_Nihilego_EventScript_UBBack::
	msgbox UltraSpace_Nihilego_Text_UBBack, MSGBOX_DEFAULT
	release
	end

UltraSpace_Nihilego_EventScript_UBCaught::
	setflag FLAG_ULTRA_NIHILEGO
	goto UltraSpace_EventScript_CaughtFade

UltraSpace_Nihilego_EventScript_Jelly::
	msgbox UltraSpace_Nihilego_Text_Jelly, MSGBOX_NPC
	end

UltraSpace_Nihilego_EventScript_Echo::
	msgbox UltraSpace_Nihilego_Text_Echo, MSGBOX_NPC
	end

@ ---------------------------------------------------------------- teksten (placeholders, Jordi herschrijft ze)
UltraSpace_Nihilego_Text_UB:
	.string "A translucent POKéMON drifts through\n"
	.string "the glass. It looks exactly like a\l"
	.string "thought you had once and regretted.$"

UltraSpace_Nihilego_Text_UBBack:
	.string "NIHILEGO wobbles back into the glass.\n"
	.string "It will be back. Thoughts always are.$"

UltraSpace_Nihilego_Text_Jelly:
	.string "It floats through the air as if the air\n"
	.string "were water. Nobody told it otherwise.$"

UltraSpace_Nihilego_Text_Echo:
	.string "A reflection of NIHILEGO. Or NIHILEGO\n"
	.string "is a reflection of this. The glass won't\l"
	.string "say.$"

