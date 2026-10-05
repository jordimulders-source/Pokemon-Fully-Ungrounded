@ Project Grounded: reuzen-Wailord op zee (ZEE_PLAN.md). Elke kaart met een Wailord roept in OnTransition
@ Common_EventScript_GiantWailordSpawn aan met VAR_0x8004 = zijn plek (1 Route 124, 2 Route 128, 3 Route 129).

Common_EventScript_GiantWailordSpawn::
	specialvar VAR_RESULT, Grounded_GiantWailordSpot
	goto_if_eq VAR_RESULT, VAR_0x8004, Common_EventScript_GiantWailordShow
	setflag FLAG_HIDE_GIANT_WAILORD
	return

Common_EventScript_GiantWailordShow:
	clearflag FLAG_HIDE_GIANT_WAILORD
	return

Common_EventScript_GiantWailord::
	lock
	playmoncry SPECIES_WAILORD, CRY_MODE_NORMAL
	msgbox GiantWailord_Text_Chilling, MSGBOX_DEFAULT
	waitmoncry
	release
	end

GiantWailord_Text_Chilling:
	.string "A colossal WAILORD is floating here.\p"
	.string "It isn't blocking the route.\n"
	.string "The route is blocking it.\p"
	.string "…\p"
	.string "WAILORD gives you one slow,\n"
	.string "unbothered blink.\p"
	.string "It's chilling. It has no plans today.\n"
	.string "Or tomorrow. Or ever.$"
