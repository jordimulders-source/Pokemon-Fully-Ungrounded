UltraSpace_Guzzlord_MapScripts::
	map_script MAP_SCRIPT_ON_RESUME, UltraSpace_Guzzlord_OnResume
	.byte 0

UltraSpace_Guzzlord_OnResume:
	setstepcallback STEP_CB_ULTRA_WORLDS
	end

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

UltraSpace_Guzzlord_EventScript_Trubbish::
	msgbox UltraSpace_Guzzlord_Text_Trubbish, MSGBOX_NPC
	end

UltraSpace_Guzzlord_EventScript_Garbodor::
	msgbox UltraSpace_Guzzlord_Text_Garbodor, MSGBOX_NPC
	end

UltraSpace_Guzzlord_EventScript_Murkrow::
	msgbox UltraSpace_Guzzlord_Text_Murkrow, MSGBOX_NPC
	end

UltraSpace_Guzzlord_EventScript_Munchlax::
	msgbox UltraSpace_Guzzlord_Text_Munchlax, MSGBOX_NPC
	end

UltraSpace_Guzzlord_EventScript_Sign::
	msgbox UltraSpace_Guzzlord_Text_Sign, MSGBOX_SIGN
	end

@ ---------------------------------------------------------------- teksten (placeholders, Jordi herschrijft ze)
UltraSpace_Guzzlord_Text_UB:
	.string "GUZZLORD is eating the horizon.\p"
	.string "It has been eating it for a while. The\n"
	.string "horizon is getting nervous.$"

UltraSpace_Guzzlord_Text_UBBack:
	.string "GUZZLORD burps and keeps eating. You\n"
	.string "were a snack. Barely.$"

UltraSpace_Guzzlord_Text_Trubbish:
	.string "TRUBBISH is going through the ruins of\n"
	.string "the DEPARTMENT STORE.\p"
	.string "It found a coupon. It expired the day\n"
	.string "the world ended.$"

UltraSpace_Guzzlord_Text_Garbodor:
	.string "GARBODOR is sitting where a house used\n"
	.string "to be. It has never felt more at home.$"

UltraSpace_Guzzlord_Text_Murkrow:
	.string "MURKROW is perched on what is left of a\n"
	.string "streetlight, waiting for the sequel.$"

UltraSpace_Guzzlord_Text_Munchlax:
	.string "MUNCHLAX is staring at GUZZLORD with\n"
	.string "professional admiration.$"

UltraSpace_Guzzlord_Text_Sign:
	.string "LILYCOVE CITY Where the land ends and\n"
	.string "the sea begins.\p"
	.string "Someone has crossed it out and written:\n"
	.string "“WHERE THE LAND ENDS.”$"

