FieryPath_MapScripts::
	map_script MAP_SCRIPT_ON_TRANSITION, FieryPath_OnTransition
	map_script MAP_SCRIPT_ON_LOAD, FieryPath_OnLoad
	.byte 0

@ Project Grounded: na de Hall of Fame is er linksboven een grotopening naar het hol van Heatran
FieryPath_OnLoad:
	call_if_set FLAG_OGERPON_QUEST_STARTED, FieryPath_EventScript_OpenEmberHollow
	goto_if_unset FLAG_SYS_GAME_CLEAR, FieryPath_EventScript_HeatranCaveHidden
	setmetatile 8, 0, METATILE_Lavaridge_CaveEntrance_Top, TRUE
	setmetatile 8, 1, METATILE_Lavaridge_CaveEntrance_Bottom, FALSE
FieryPath_EventScript_HeatranCaveHidden:
	end

@ Project Grounded: Ogerpon-quest. Grotopening in de doodlopende zak linksonder (8,27) naar Munkidori (FieryPath_EmberHollow)
FieryPath_EventScript_OpenEmberHollow::
	setmetatile 8, 26, METATILE_Lavaridge_CaveEntrance_Top, TRUE
	setmetatile 8, 27, METATILE_Lavaridge_CaveEntrance_Bottom, FALSE
	return

FieryPath_OnTransition:
	call_if_unset FLAG_LANDMARK_FIERY_PATH, FieryPath_EventScript_MoveScottToFallarbor
	setflag FLAG_LANDMARK_FIERY_PATH
	end

FieryPath_EventScript_MoveScottToFallarbor::
	setflag FLAG_HIDE_VERDANTURF_TOWN_SCOTT
	clearflag FLAG_HIDE_FALLARBOR_TOWN_BATTLE_TENT_SCOTT
	return

