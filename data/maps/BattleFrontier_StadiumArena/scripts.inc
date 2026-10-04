@ Project Grounded: arena van het Battle Stadium (kopie van de Battle Dome-zaal). Het echte spelersobject is de
@ camera en onzichtbaar; LOCALID_STADIUM_PLAYER (VAR_1) loopt naar binnen, LOCALID_STADIUM_OPPONENT (VAR_0) staat
@ rechts. In doubles ook LOCALID_STADIUM_PARTNER (VAR_3) en LOCALID_STADIUM_OPPONENT2 (VAR_2).
@ Het verloop staat in data/scripts/battle_stadium.inc.
BattleFrontier_StadiumArena_MapScripts::
	map_script MAP_SCRIPT_ON_TRANSITION, BattleFrontier_StadiumArena_OnTransition
	map_script MAP_SCRIPT_ON_FRAME_TABLE, BattleFrontier_StadiumArena_OnFrame
	.byte 0

BattleFrontier_StadiumArena_OnTransition:
	setflag FLAG_TEMP_HIDE_FOLLOWER
	setflag FLAG_TEMP_2
	special Stadium_SetArenaGfx
	copyvar VAR_TEMP_1, VAR_RESULT
	call_if_ne VAR_TEMP_1, STADIUM_DOUBLES, BattleFrontier_StadiumArena_EventScript_HideOpponent2
	end

BattleFrontier_StadiumArena_EventScript_HideOpponent2::
	setflag FLAG_TEMP_1
	return

BattleFrontier_StadiumArena_OnFrame:
	map_script_2 VAR_TEMP_0, 0, BattleStadium_EventScript_ArenaMatch
	.2byte 0
