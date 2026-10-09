UltraSpace_Blacephalon_MapScripts::
	map_script MAP_SCRIPT_ON_RESUME, UltraSpace_Blacephalon_OnResume
	.byte 0

UltraSpace_Blacephalon_OnResume:
	setstepcallback STEP_CB_ULTRA_WORLDS
	end

UltraSpace_Blacephalon_EventScript_UB::
	lock
	faceplayer
	playmoncry SPECIES_BLACEPHALON, CRY_MODE_ENCOUNTER
	msgbox UltraSpace_Blacephalon_Text_UB, MSGBOX_DEFAULT
	waitmoncry
	closemessage
	setwildbattle SPECIES_BLACEPHALON, 90
	special BattleSetup_StartLegendaryBattle
	waitstate
	specialvar VAR_RESULT, GetBattleOutcome
	goto_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, UltraSpace_Blacephalon_EventScript_UBCaught
	goto_if_eq VAR_RESULT, B_OUTCOME_WON, UltraSpace_Blacephalon_EventScript_UBBack
	release
	end

UltraSpace_Blacephalon_EventScript_UBBack::
	msgbox UltraSpace_Blacephalon_Text_UBBack, MSGBOX_DEFAULT
	release
	end

UltraSpace_Blacephalon_EventScript_UBCaught::
	setflag FLAG_ULTRA_BLACEPHALON
	goto UltraSpace_EventScript_CaughtFade

UltraSpace_Blacephalon_EventScript_MrMime::
	msgbox UltraSpace_Blacephalon_Text_MrMime, MSGBOX_NPC
	end

UltraSpace_Blacephalon_EventScript_Hypno::
	msgbox UltraSpace_Blacephalon_Text_Hypno, MSGBOX_NPC
	end

UltraSpace_Blacephalon_EventScript_Spoink::
	msgbox UltraSpace_Blacephalon_Text_Spoink, MSGBOX_NPC
	end

UltraSpace_Blacephalon_EventScript_MimeJr::
	msgbox UltraSpace_Blacephalon_Text_MimeJr, MSGBOX_NPC
	end

UltraSpace_Blacephalon_EventScript_Grimmsnarl::
	msgbox UltraSpace_Blacephalon_Text_Grimmsnarl, MSGBOX_NPC
	end

UltraSpace_Blacephalon_EventScript_Spinda::
	msgbox UltraSpace_Blacephalon_Text_Spinda, MSGBOX_NPC
	end

UltraSpace_Blacephalon_EventScript_ShyGuy::
	msgbox UltraSpace_Blacephalon_Text_ShyGuy, MSGBOX_NPC
	end

UltraSpace_Blacephalon_EventScript_Tickets::
	msgbox UltraSpace_Blacephalon_Text_Tickets, MSGBOX_SIGN
	end

UltraSpace_Blacephalon_EventScript_Popcorn::
	msgbox UltraSpace_Blacephalon_Text_Popcorn, MSGBOX_SIGN
	end

UltraSpace_Blacephalon_EventScript_Cannon::
	msgbox UltraSpace_Blacephalon_Text_Cannon, MSGBOX_SIGN
	end

@ ---------------------------------------------------------------- teksten (placeholders, Jordi herschrijft ze)
UltraSpace_Blacephalon_Text_UB:
	.string "BLACEPHALON juggles its own head.\p"
	.string "It drops it, on purpose, and it explodes.\n"
	.string "The crowd goes wild. Your eyebrows go\l"
	.string "home.$"

UltraSpace_Blacephalon_Text_UBBack:
	.string "BLACEPHALON grows a new head and\n"
	.string "takes a bow. The crowd demands an\l"
	.string "encore.$"

UltraSpace_Blacephalon_Text_MrMime:
	.string "MR. MIME is trapped in an invisible box.\p"
	.string "He built the box himself. He is very\n"
	.string "proud of the box.$"

UltraSpace_Blacephalon_Text_Hypno:
	.string "HYPNO: LADIES AND GENTLEMEN, POKéMON\n"
	.string "OF ALL AGES… look into the pendulum…\p"
	.string "You WILL buy popcorn. You WILL laugh at\n"
	.string "the clowns. You WILL NOT ask for a\l"
	.string "refund.$"

UltraSpace_Blacephalon_Text_Spoink:
	.string "SPOINK has been bouncing since the\n"
	.string "show started. The show started in 1998.$"

UltraSpace_Blacephalon_Text_MimeJr:
	.string "MIME JR. is miming that it is having fun.\n"
	.string "Convincingly. Mostly.$"

UltraSpace_Blacephalon_Text_Grimmsnarl:
	.string "GRIMMSNARL is the strongman. It is\n"
	.string "lifting a barbell made of two smaller\l"
	.string "GRIMMSNARL.$"

UltraSpace_Blacephalon_Text_Spinda:
	.string "SPINDA is doing the tightrope act.\n"
	.string "There is no rope. That is the act.$"

UltraSpace_Blacephalon_Text_ShyGuy:
	.string "The clown refuses to take off his mask.\p"
	.string "Nobody has ever seen him without it.\n"
	.string "Including him.$"

UltraSpace_Blacephalon_Text_Tickets:
	.string "ADMISSION: ONE (1) HEAD.\p"
	.string "BLACEPHALON BRINGS ITS OWN.$"

UltraSpace_Blacephalon_Text_Popcorn:
	.string "The popcorn is free. The popcorn is also\n"
	.string "slightly on fire. Those are related.$"

UltraSpace_Blacephalon_Text_Cannon:
	.string "THE HUMAN CANNONBALL (position\n"
	.string "available)\p"
	.string "Previous applicant: BLACEPHALON's\n"
	.string "head.$"

