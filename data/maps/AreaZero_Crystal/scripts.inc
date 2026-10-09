@ Project Grounded: AreaZero_Crystal (tools/grounded/maptools/area_zero.py)
AreaZero_Crystal_MapScripts::
	map_script MAP_SCRIPT_ON_LOAD, AreaZero_Crystal_OnLoad
	.byte 0

AreaZero_Crystal_OnLoad:
	checktrainerflag TRAINER_AREA_ZERO_SECURITY_FUTURE
	goto_if FALSE, AreaZero_Crystal_EventScript_Sealed
	checktrainerflag TRAINER_AREA_ZERO_SECURITY_PAST
	goto_if FALSE, AreaZero_Crystal_EventScript_Sealed
	setmetatile 33, 23, 0x24E, FALSE
AreaZero_Crystal_EventScript_Sealed:
	end

AreaZero_Crystal_EventScript_Hole::
	checktrainerflag TRAINER_AREA_ZERO_SECURITY_FUTURE
	goto_if FALSE, AreaZero_Crystal_EventScript_HoleShut
	checktrainerflag TRAINER_AREA_ZERO_SECURITY_PAST
	goto_if FALSE, AreaZero_Crystal_EventScript_HoleShut
	end

AreaZero_Crystal_EventScript_HoleShut::
	msgbox AreaZero_Crystal_Text_HoleShut, MSGBOX_SIGN
	end

AreaZero_Crystal_EventScript_Log::
	msgbox AreaZero_Crystal_Text_Log, MSGBOX_SIGN
	end

AreaZero_Crystal_EventScript_SignPast::
	msgbox AreaZero_Crystal_Text_SignPast, MSGBOX_SIGN
	end

AreaZero_Crystal_EventScript_SignFuture::
	msgbox AreaZero_Crystal_Text_SignFuture, MSGBOX_SIGN
	end

@ ---------------------------------------------------------------- teksten (placeholders, Jordi herschrijft ze)
AreaZero_Crystal_Text_HoleShut:
	.string "Crystals have grown over a cave mouth.\p"
	.string "Behind them something enormous is\n"
	.string "asleep, and two security systems are\l"
	.string "very much awake. One in the past, one in\l"
	.string "the future. Naturally.$"

AreaZero_Crystal_Text_Log:
	.string "RESEARCH LOG 03\n"
	.string "We built a gate. It goes to the past AND\l"
	.string "the future. The paperwork goes to\l"
	.string "neither.\p"
	.string "If you see the PROFESSOR: the coffee\n"
	.string "machine in the future is fine. The one in\l"
	.string "the past is a rock.$"

AreaZero_Crystal_Text_SignPast:
	.string "ZERO GATE - CHANNEL A\n"
	.string "PAST\p"
	.string "Warranty void if you meet yourself.$"

AreaZero_Crystal_Text_SignFuture:
	.string "ZERO GATE - CHANNEL B\n"
	.string "FUTURE\p"
	.string "Please do not bring back souvenirs.\n"
	.string "They bring themselves back.$"
