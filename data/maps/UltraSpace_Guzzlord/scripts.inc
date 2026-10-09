UltraSpace_Guzzlord_MapScripts::
	.byte 0

UltraSpace_Guzzlord_EventScript_UB::
	lock
	faceplayer
	playmoncry SPECIES_GUZZLORD, CRY_MODE_ENCOUNTER
	msgbox UltraSpace_Guzzlord_Text_UB, MSGBOX_DEFAULT
	waitmoncry
	closemessage
	setwildbattle SPECIES_GUZZLORD, 90
	special BattleSetup_StartLegendaryBattle
	waitstate
	specialvar VAR_RESULT, GetBattleOutcome
	goto_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, UltraSpace_Guzzlord_EventScript_UBCaught
	goto_if_eq VAR_RESULT, B_OUTCOME_WON, UltraSpace_Guzzlord_EventScript_UBBack
	release
	end

UltraSpace_Guzzlord_EventScript_UBBack::
	msgbox UltraSpace_Guzzlord_Text_UBBack, MSGBOX_DEFAULT
	release
	end

UltraSpace_Guzzlord_EventScript_UBCaught::
	setflag FLAG_ULTRA_GUZZLORD
	goto UltraSpace_EventScript_CaughtFade

UltraSpace_Guzzlord_EventScript_Trash::
	msgbox UltraSpace_Guzzlord_Text_Trash, MSGBOX_NPC
	end

UltraSpace_Guzzlord_EventScript_Junk::
	msgbox UltraSpace_Guzzlord_Text_Junk, MSGBOX_NPC
	end

@ ---------------------------------------------------------------- teksten (placeholders, Jordi herschrijft ze)
UltraSpace_Guzzlord_Text_UB:
	.string "GUZZLORD is eating the horizon.\p"
	.string "It has been eating it for a while. The\n"
	.string "horizon is getting nervous.$"

UltraSpace_Guzzlord_Text_UBBack:
	.string "GUZZLORD burps and keeps eating. You\n"
	.string "were a snack. Barely.$"

UltraSpace_Guzzlord_Text_Trash:
	.string "It lives here. It likes it here. Please\n"
	.string "stop looking at it like that.$"

UltraSpace_Guzzlord_Text_Junk:
	.string "A pile of things GUZZLORD didn't finish.\n"
	.string "There is a sock. There is always a sock.$"

