SouthernIsland_Exterior_MapScripts::
	map_script MAP_SCRIPT_ON_TRANSITION, SouthernIsland_Exterior_OnTransition
	.byte 0

SouthernIsland_Exterior_OnTransition:
	setflag FLAG_LANDMARK_SOUTHERN_ISLAND
	end

SouthernIsland_Exterior_EventScript_Sailor::
	lock
	faceplayer
	msgbox EventTicket_Text_SouthernIslandSailBack, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, SouthernIsland_Exterior_EventScript_AsYouLike
	msgbox EventTicket_Text_SailHome, MSGBOX_DEFAULT
	closemessage
	applymovement VAR_LAST_TALKED, Common_Movement_WalkInPlaceFasterDown
	waitmovement 0
	delay 30
	hideobjectat LOCALID_SOUTHERN_ISLAND_SAILOR, MAP_SOUTHERN_ISLAND_EXTERIOR
	setvar VAR_0x8004, LOCALID_SOUTHERN_ISLAND_SS_TIDAL
	call Common_EventScript_FerryDepartIsland
	warp MAP_LILYCOVE_CITY_HARBOR, 8, 11
	waitstate
	release
	end

SouthernIsland_Exterior_EventScript_AsYouLike::
	msgbox EventTicket_Text_AsYouLike, MSGBOX_DEFAULT
	release
	end

Ferry_EventScript_DepartIslandSouth::
	applymovement LOCALID_PLAYER, Ferry_Movement_DepartIslandBoardSouth
	waitmovement 0
	return

Ferry_EventScript_DepartIslandWest::
	applymovement LOCALID_PLAYER, Ferry_Movement_DepartIslandBoardWest
	waitmovement 0
	return

Ferry_Movement_DepartIslandBoardSouth:
	walk_down
	step_end

Ferry_Movement_DepartIslandBoardWest:
	walk_left
	walk_in_place_faster_down
	step_end

SouthernIsland_Exterior_EventScript_Sign::
	msgbox SouthernIsland_Exterior_Text_Sign, MSGBOX_SIGN
	end

@ --- land_vulling (gegenereerd door tools/grounded/maptools/land_vulling.py) ---
SouthernIsland_Exterior_EventScript_LVLetters::
	msgbox SouthernIsland_Exterior_Text_LVLetters, MSGBOX_SIGN
	end

SouthernIsland_Exterior_Text_LVLetters:
	.string "A crate full of letters. The top\none reads:\p'Day 1. A red dragon lives here.\nI just know it. I'll wait.'\p'Day 90. Still waiting. Built a\nchair. The chair is my friend now.'\p'Day 2,190. The boat came. I went.\nKeep the stuff. Keep the chair.\lDon't keep the dream. It's heavy.'$"

SouthernIsland_Exterior_EventScript_LVPlush::
	msgbox SouthernIsland_Exterior_Text_LVPlush, MSGBOX_SIGN
	end

SouthernIsland_Exterior_Text_LVPlush:
	.string "A handmade LATIAS plush.\pOn closer inspection: a SWABLU\ndoll, painted red. Badly.\lWith love, but badly.$"
@ --- einde land_vulling ---
