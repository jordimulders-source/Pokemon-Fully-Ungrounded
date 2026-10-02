Underwater_Route136_MapScripts::
	map_script MAP_SCRIPT_ON_DIVE_WARP, Underwater_Route136_OnDive
	.byte 0

@ Boven komen: op de lichte plek onderaan (12,44) in de Suicune-grot, anders terug in het kristalmeer
Underwater_Route136_OnDive:
	getplayerxy VAR_0x8004, VAR_0x8005
	goto_if_ne VAR_0x8004, 12, Underwater_Route136_EventScript_SurfaceGrotto
	goto_if_ne VAR_0x8005, 44, Underwater_Route136_EventScript_SurfaceGrotto
	setdivewarp MAP_ROUTE136_SUICUNE_CAVE, 10, 17
	end

Underwater_Route136_EventScript_SurfaceGrotto::
	setdivewarp MAP_ROUTE136_GROTTO, 9, 21
	end
