@ Project Grounded: Whirl Island (Lugia). Alleen bereikbaar door te duiken (Dive = badge 7): onder Route 124 een
@ zwemgat naar Underwater_WhirlIsland, bovenkomen in de lagune binnen een ring van draaikolken. Het diepe water
@ in de lagune (20,33) is ook de weg terug. De grot (15,27) leidt naar Lugia (WhirlIsland_Cave).
@ Kaart: tools/grounded/maptools/sea_temple_lugia.py
WhirlIsland_MapScripts::
	map_script MAP_SCRIPT_ON_RESUME, WhirlIsland_OnResume
	.byte 0

WhirlIsland_OnResume:
	setdivewarp MAP_UNDERWATER_WHIRL_ISLAND, 9, 6
	end

WhirlIsland_EventScript_Bottle::
	msgbox WhirlIsland_Text_Bottle, MSGBOX_SIGN
	end

WhirlIsland_Text_Bottle:
	.string "There's a message in a bottle stuck\n"
	.string "in the shallows.\p"
	.string "“Day 40. Still circling. The\n"
	.string "whirlpools let you in, but they never\l"
	.string "let you out.\p"
	.string "Day 41. Just remembered I can DIVE.\n"
	.string "Bye.”$"
