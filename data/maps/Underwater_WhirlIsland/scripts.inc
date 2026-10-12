@ Project Grounded: onderzeese grot onder Whirl Island (kopie van Underwater_SootopolisCity). Ingang = zwemgat in de
@ noordwand van de westelijke kom van Underwater Route 124 (13,25). Bovenkomen = de lagune van Whirl Island.
Underwater_WhirlIsland_MapScripts::
	map_script MAP_SCRIPT_ON_RESUME, Underwater_WhirlIsland_OnResume
	.byte 0

Underwater_WhirlIsland_OnResume:
	setdivewarp MAP_WHIRL_ISLAND, 20, 33
	end
