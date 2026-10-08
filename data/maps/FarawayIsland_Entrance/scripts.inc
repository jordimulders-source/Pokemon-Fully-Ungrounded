FarawayIsland_Entrance_MapScripts::
	map_script MAP_SCRIPT_ON_TRANSITION, FarawayIsland_Entrance_OnTransition
	.byte 0

FarawayIsland_Entrance_OnTransition:
	setflag FLAG_ARRIVED_ON_FARAWAY_ISLAND
	end

FarawayIsland_Entrance_EventScript_SetCloudsWeather::
	setweather WEATHER_SUNNY_CLOUDS
	doweather
	end

FarawayIsland_Entrance_EventScript_ClearWeather::
	setweather WEATHER_NONE
	doweather
	end

FarawayIsland_Entrance_EventScript_Sailor::
	lock
	faceplayer
	msgbox FarawayIsland_Entrance_Text_SailorReturn, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, FarawayIsland_Entrance_EventScript_AsYouLike
	msgbox EventTicket_Text_SailHome, MSGBOX_DEFAULT
	closemessage
	applymovement VAR_LAST_TALKED, Common_Movement_WalkInPlaceFasterDown
	waitmovement 0
	delay 30
	hideobjectat LOCALID_FARAWAY_ISLAND_SAILOR, MAP_FARAWAY_ISLAND_ENTRANCE
	setvar VAR_0x8004, LOCALID_FARAWAY_ISLAND_SS_TIDAL
	call Common_EventScript_FerryDepartIsland
	warp MAP_LILYCOVE_CITY_HARBOR, 8, 11
	waitstate
	release
	end

FarawayIsland_Entrance_EventScript_AsYouLike::
	msgbox EventTicket_Text_AsYouLike, MSGBOX_DEFAULT
	release
	end

FarawayIsland_Entrance_EventScript_Sign::
	msgbox FarawayIsland_Entrance_Text_Sign, MSGBOX_SIGN
	end

@ --- land_vulling (gegenereerd door tools/grounded/maptools/land_vulling.py) ---
FarawayIsland_Entrance_EventScript_LVLetters::
	msgbox FarawayIsland_Entrance_Text_LVLetters, MSGBOX_SIGN
	end

FarawayIsland_Entrance_Text_LVLetters:
	.string "A damp crate. Research notes,\nsigned 'DR. P. LUMB'.\p'Week 1. Saw a small pink cat.\nPossibly the ancestor of all\lPOKeMON. Possibly a cat.'\p'Week 12. It knows my name.\nI never told it my name.'\p'Week 30. It turned into my sister.\nI am an only child.'\p'Week 31. Going home. If my sister\ncalls, don't pick up.'$"
@ --- einde land_vulling ---
