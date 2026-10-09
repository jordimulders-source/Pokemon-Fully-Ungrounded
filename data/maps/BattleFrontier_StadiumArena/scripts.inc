@ Project Grounded: arena van het Battle Stadium (kopie van de Battle Dome-zaal). Het echte spelersobject is de
@ camera en onzichtbaar; LOCALID_STADIUM_PLAYER (VAR_1) staat links klaar, LOCALID_STADIUM_OPPONENT (VAR_0)
@ rechts (geen opkomst: Jordi wil het kort). In doubles ook LOCALID_STADIUM_PARTNER (VAR_3) en LOCALID_STADIUM_OPPONENT2 (VAR_2).
@ Het verloop staat in data/scripts/battle_stadium.inc. Battle Casino (Stadium-modi): VAR_STADIUM_STATE = CASINO_STATE_ARENA,
@ zie data/maps/BattleFrontier_BattleCasino/scripts.inc.
BattleFrontier_StadiumArena_MapScripts::
	map_script MAP_SCRIPT_ON_TRANSITION, BattleFrontier_StadiumArena_OnTransition
	map_script MAP_SCRIPT_ON_FRAME_TABLE, BattleFrontier_StadiumArena_OnFrame
	.byte 0

BattleFrontier_StadiumArena_OnTransition:
	setflag FLAG_TEMP_HIDE_FOLLOWER
	goto_if_eq VAR_STADIUM_STATE, CASINO_STATE_ARENA, BattleCasino_EventScript_ArenaTransition
	special Stadium_SetArenaGfx
	copyvar VAR_TEMP_1, VAR_RESULT
	call_if_ne VAR_TEMP_1, STADIUM_DOUBLES, BattleFrontier_StadiumArena_EventScript_HideDoubles
	end

BattleFrontier_StadiumArena_EventScript_HideDoubles::
	setflag FLAG_TEMP_1
	setflag FLAG_TEMP_2
	return

BattleFrontier_StadiumArena_OnFrame:
	map_script_2 VAR_STADIUM_STATE, CASINO_STATE_ARENA, BattleCasino_EventScript_ArenaMatch
	map_script_2 VAR_TEMP_0, 0, BattleStadium_EventScript_ArenaMatch
	.2byte 0
