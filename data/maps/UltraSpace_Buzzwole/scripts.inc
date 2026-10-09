UltraSpace_Buzzwole_MapScripts::
	.byte 0

UltraSpace_Buzzwole_EventScript_UB::
	lock
	faceplayer
	playmoncry SPECIES_BUZZWOLE, CRY_MODE_ENCOUNTER
	msgbox UltraSpace_Buzzwole_Text_UB, MSGBOX_DEFAULT
	waitmoncry
	closemessage
	setwildbattle SPECIES_BUZZWOLE, 88
	special BattleSetup_StartLegendaryBattle
	waitstate
	specialvar VAR_RESULT, GetBattleOutcome
	goto_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, UltraSpace_Buzzwole_EventScript_UBCaught
	goto_if_eq VAR_RESULT, B_OUTCOME_WON, UltraSpace_Buzzwole_EventScript_UBBack
	release
	end

UltraSpace_Buzzwole_EventScript_UBBack::
	msgbox UltraSpace_Buzzwole_Text_UBBack, MSGBOX_DEFAULT
	release
	end

UltraSpace_Buzzwole_EventScript_UBCaught::
	setflag FLAG_ULTRA_BUZZWOLE
	goto UltraSpace_EventScript_CaughtFade

UltraSpace_Buzzwole_EventScript_Lifter::
	msgbox UltraSpace_Buzzwole_Text_Lifter, MSGBOX_NPC
	end

@ ---------------------------------------------------------------- teksten (placeholders, Jordi herschrijft ze)
UltraSpace_Buzzwole_Text_UB:
	.string "BUZZWOLE flexes. The floor flexes back.\p"
	.string "It has never skipped leg day. It has\n"
	.string "never skipped any day.$"

UltraSpace_Buzzwole_Text_UBBack:
	.string "BUZZWOLE shakes it off and starts\n"
	.string "another set. You are now part of its\l"
	.string "warm-up.$"

UltraSpace_Buzzwole_Text_Lifter:
	.string "Counting reps. It lost count at 4,000\n"
	.string "and started over out of spite.$"

