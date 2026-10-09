@ Project Grounded: AreaZero_Depths (tools/grounded/maptools/area_zero.py)
AreaZero_Depths_MapScripts::
	.byte 0

AreaZero_Depths_EventScript_Log::
	msgbox AreaZero_Depths_Text_Log, MSGBOX_SIGN
	end

AreaZero_Depths_EventScript_ScreamTail::
	lock
	faceplayer
	playmoncry SPECIES_SCREAM_TAIL, CRY_MODE_ENCOUNTER
	msgbox AreaZero_Depths_Text_ScreamTail, MSGBOX_DEFAULT
	waitmoncry
	closemessage
	setwildbattle SPECIES_SCREAM_TAIL, 94
	special BattleSetup_StartLegendaryBattle
	waitstate
	specialvar VAR_RESULT, GetBattleOutcome
	goto_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, AreaZero_Depths_EventScript_ScreamTailCaught
	goto_if_eq VAR_RESULT, B_OUTCOME_WON, AreaZero_Depths_EventScript_ScreamTailBack
	release
	end

AreaZero_Depths_EventScript_ScreamTailBack::
	msgbox AreaZero_Depths_Text_ScreamTailBack, MSGBOX_DEFAULT
	release
	end

AreaZero_Depths_EventScript_ScreamTailCaught::
	removeobject LOCALID_AREA_ZERO_SCREAM_TAIL
	setflag FLAG_AREAZERO_SCREAM_TAIL
	release
	end

AreaZero_Depths_EventScript_IronHands::
	lock
	faceplayer
	playmoncry SPECIES_IRON_HANDS, CRY_MODE_ENCOUNTER
	msgbox AreaZero_Depths_Text_IronHands, MSGBOX_DEFAULT
	waitmoncry
	closemessage
	setwildbattle SPECIES_IRON_HANDS, 94
	special BattleSetup_StartLegendaryBattle
	waitstate
	specialvar VAR_RESULT, GetBattleOutcome
	goto_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, AreaZero_Depths_EventScript_IronHandsCaught
	goto_if_eq VAR_RESULT, B_OUTCOME_WON, AreaZero_Depths_EventScript_IronHandsBack
	release
	end

AreaZero_Depths_EventScript_IronHandsBack::
	msgbox AreaZero_Depths_Text_IronHandsBack, MSGBOX_DEFAULT
	release
	end

AreaZero_Depths_EventScript_IronHandsCaught::
	removeobject LOCALID_AREA_ZERO_IRON_HANDS
	setflag FLAG_AREAZERO_IRON_HANDS
	release
	end

@ ---------------------------------------------------------------- teksten (placeholders, Jordi herschrijft ze)
AreaZero_Depths_Text_Log:
	.string "RESEARCH LOG 02\n"
	.string "The deeper we go, the more the colours\l"
	.string "drift. The grass is now 'teal-adjacent'.\p"
	.string "The crystals hum. Our intern hums back.\n"
	.string "We have asked him to stop. He says he\l"
	.string "can't.$"

AreaZero_Depths_Text_ScreamTail:
	.string "A pink, fluffy thing with an enormous\n"
	.string "mouth stares at you.\p"
	.string "It screams. It isn't angry. That's just\n"
	.string "its resting face.$"

AreaZero_Depths_Text_ScreamTailBack:
	.string "SCREAM TAIL dissolves into crystal\n"
	.string "dust... and screams itself back\l"
	.string "together.\p"
	.string "Paradoxes don't really do 'gone'. Try\n"
	.string "catching it.$"

AreaZero_Depths_Text_IronHands:
	.string "A hulking machine flexes two gigantic\n"
	.string "hands.\p"
	.string "A label on its back reads: DO NOT\n"
	.string "HIGH-FIVE.$"

AreaZero_Depths_Text_IronHandsBack:
	.string "IRON HANDS powers down... and reboots\n"
	.string "with a cheerful chime.\p"
	.string "It wants a rematch. It always wants a\n"
	.string "rematch.$"
