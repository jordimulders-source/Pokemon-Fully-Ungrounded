@ Project Grounded: onderwatergrot onder de koele bron van de Scorched Slab (verborgen Big Nugget).
Underwater_ScorchedSlab_MapScripts::
	map_script MAP_SCRIPT_ON_RESUME, Underwater_ScorchedSlab_OnResume
	.byte 0

Underwater_ScorchedSlab_OnResume:
	setdivewarp MAP_SCORCHED_SLAB_SPRING, 14, 10
	end
