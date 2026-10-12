AlteringCave_MapScripts::
	map_script MAP_SCRIPT_ON_TRANSITION, AlteringCave_OnTransition
	.byte 0

AlteringCave_OnTransition:
	setflag FLAG_LANDMARK_ALTERING_CAVE
	call_if_unset FLAG_SYS_GAME_CLEAR, AlteringCave_EventScript_HideWormhole
	end

@ Project Grounded: Ultra Wormhole naar Ultra Space (post-game; tools/grounded/maptools/ultra_space.py)
AlteringCave_EventScript_HideWormhole::
	setflag FLAG_TEMP_1
	return

AlteringCave_EventScript_UltraWormhole::
	lock
	playse SE_M_TELEPORT
	waitse
	warp MAP_ULTRA_SPACE_HUB, 13, 17
	waitstate
	release
	end

