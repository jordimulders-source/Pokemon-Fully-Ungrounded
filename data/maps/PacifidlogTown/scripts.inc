PacifidlogTown_MapScripts::
	map_script MAP_SCRIPT_ON_TRANSITION, PacifidlogTown_OnTransition
	map_script MAP_SCRIPT_ON_RESUME, PacifidlogTown_OnResume
	.byte 0

PacifidlogTown_OnTransition:
	setvar VAR_0x8004, 3
	call Common_EventScript_SickBlikDevSpawn  @ SickBlik als developer (post-game, dagrotatie)
	setflag FLAG_VISITED_PACIFIDLOG_TOWN
	end

PacifidlogTown_OnResume:
	setstepcallback STEP_CB_PACIFIDLOG_BRIDGE
	end

PacifidlogTown_EventScript_NinjaBoy::
	msgbox PacifidlogTown_Text_NeatHousesOnWater, MSGBOX_NPC
	end

PacifidlogTown_EventScript_Girl::
	msgbox PacifidlogTown_Text_FastRunningCurrent, MSGBOX_NPC
	end

PacifidlogTown_EventScript_Fisherman::
	msgbox PacifidlogTown_Text_SkyPillarTooScary, MSGBOX_NPC
	end

PacifidlogTown_EventScript_TownSign::
	msgbox PacifidlogTown_Text_TownSign, MSGBOX_SIGN
	end

PacifidlogTown_Text_FastRunningCurrent:
	.string "The current here is fast.\p"
	.string "Faster than the internet.\p"
	.string "We don't have internet.$"

PacifidlogTown_Text_NeatHousesOnWater:
	.string "Houses on water! Just like the Land of\n"
	.string "Waves in NARUTO!\p"
	.string "I was born here. Still waiting for my\n"
	.string "ninja arc.$"

PacifidlogTown_Text_SkyPillarTooScary:
	.string "The SKY PILLAR? Don't care.\p"
	.string "We don't even have a supermarket.$"

PacifidlogTown_Text_TownSign:
	.string "PACIFIDLOG TOWN\p"
	.string "“Where the morning sun smiles upon the\n"
	.string "waters. And nothing else.”$"

