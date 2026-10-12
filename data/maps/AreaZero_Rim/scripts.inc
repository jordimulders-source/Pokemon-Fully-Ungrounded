@ Project Grounded: AreaZero_Rim (tools/grounded/maptools/area_zero.py)
AreaZero_Rim_MapScripts::
	map_script MAP_SCRIPT_ON_TRANSITION, AreaZero_Rim_OnTransition
	map_script MAP_SCRIPT_ON_FRAME_TABLE, AreaZero_Rim_OnFrame
	.byte 0

AreaZero_Rim_OnTransition:
	call_if_unset FLAG_AREAZERO_INTRO, AreaZero_Rim_EventScript_SetIntro
	end

AreaZero_Rim_EventScript_SetIntro::
	setvar VAR_TEMP_1, 1
	return

AreaZero_Rim_OnFrame:
	map_script_2 VAR_TEMP_1, 1, AreaZero_Rim_EventScript_Intro
	.2byte 0

AreaZero_Rim_EventScript_Intro::
	lockall
	setvar VAR_TEMP_1, 0
	delay 16
	msgbox AreaZero_Rim_Text_Intro, MSGBOX_DEFAULT
	setflag FLAG_AREAZERO_INTRO
	releaseall
	end

AreaZero_Rim_EventScript_Station::
	msgbox AreaZero_Rim_Text_Station, MSGBOX_SIGN
	end

AreaZero_Rim_EventScript_Log::
	msgbox AreaZero_Rim_Text_Log, MSGBOX_SIGN
	end

@ ---------------------------------------------------------------- teksten (placeholders, Jordi herschrijft ze)
AreaZero_Rim_Text_Intro:
	.string "The rift spits you out on a ledge above\n"
	.string "an enormous crater.\p"
	.string "Somewhere far below, something is\n"
	.string "humming in a key that doesn't exist yet.\l"
	.string "Or anymore. Hard to say down here.$"

AreaZero_Rim_Text_Station:
	.string "RESEARCH STATION No. 1\n"
	.string "Status: unmanned since (DATE\l"
	.string "CORRUPTED).\p"
	.string "A sticky note on the door: 'Elevator\n"
	.string "broken. Also time. Take the ladders.'$"

AreaZero_Rim_Text_Log:
	.string "RESEARCH LOG 01\n"
	.string "Day 3: the POKéMON up here are normal.\l"
	.string "Suspiciously normal.\p"
	.string "A FARIGIRAF looked at me like it knew my\n"
	.string "PIN.\l"
	.string "Day 4: it did know my PIN.$"
