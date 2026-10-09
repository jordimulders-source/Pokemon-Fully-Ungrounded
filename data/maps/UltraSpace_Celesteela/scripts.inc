UltraSpace_Celesteela_MapScripts::
	.byte 0

UltraSpace_Celesteela_EventScript_UB::
	lock
	faceplayer
	playmoncry SPECIES_CELESTEELA, CRY_MODE_ENCOUNTER
	msgbox UltraSpace_Celesteela_Text_UB, MSGBOX_DEFAULT
	waitmoncry
	closemessage
	setwildbattle SPECIES_CELESTEELA, 90
	special BattleSetup_StartLegendaryBattle
	waitstate
	specialvar VAR_RESULT, GetBattleOutcome
	goto_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, UltraSpace_Celesteela_EventScript_UBCaught
	goto_if_eq VAR_RESULT, B_OUTCOME_WON, UltraSpace_Celesteela_EventScript_UBBack
	release
	end

UltraSpace_Celesteela_EventScript_UBBack::
	msgbox UltraSpace_Celesteela_Text_UBBack, MSGBOX_DEFAULT
	release
	end

UltraSpace_Celesteela_EventScript_UBCaught::
	setflag FLAG_ULTRA_CELESTEELA
	goto UltraSpace_EventScript_CaughtFade

UltraSpace_Celesteela_EventScript_Rocket::
	msgbox UltraSpace_Celesteela_Text_Rocket, MSGBOX_NPC
	end

UltraSpace_Celesteela_EventScript_Smoke::
	msgbox UltraSpace_Celesteela_Text_Smoke, MSGBOX_NPC
	end

@ ---------------------------------------------------------------- teksten (placeholders, Jordi herschrijft ze)
UltraSpace_Celesteela_Text_UB:
	.string "CELESTEELA is counting down.\p"
	.string "3… 2… 1…\p"
	.string "It reconsiders. It counts down again.\n"
	.string "This has been going on for a century.$"

UltraSpace_Celesteela_Text_UBBack:
	.string "CELESTEELA aborts the launch and\n"
	.string "resets the countdown. 100… 99…$"

UltraSpace_Celesteela_Text_Rocket:
	.string "3… 2… 1… nothing. This one has been\n"
	.string "“about to launch” since the last ice\l"
	.string "age.$"

UltraSpace_Celesteela_Text_Smoke:
	.string "It insists it is exhaust. It is clearly\n"
	.string "just a KOFFING.$"

