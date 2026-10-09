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

@ ultra_worlds_a { gegenereerd door tools/grounded/maptools/ultra_worlds_a.py; niet met de hand bewerken
UltraSpace_Celesteela_EventScript_Statue::
	msgbox UltraSpace_Celesteela_Text_Statue, MSGBOX_SIGN
	end
@ } ultra_worlds_a

UltraSpace_Celesteela_Text_Statue:
	.string "A stone CELESTEELA.\p"
	.string "The plaque says: “FIRST TO LAUNCH.” It\n"
	.string "has not launched.$"
