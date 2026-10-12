PacifidlogTown_MapScripts::
	map_script MAP_SCRIPT_ON_TRANSITION, PacifidlogTown_OnTransition
	map_script MAP_SCRIPT_ON_RESUME, PacifidlogTown_OnResume
	.byte 0

PacifidlogTown_OnTransition:
	setvar VAR_0x8004, 3
	call Common_EventScript_SickBlikDevSpawn  @ SickBlik als developer (post-game, dagrotatie)
	call PacifidlogTown_EventScript_SetupRival
	setflag FLAG_VISITED_PACIFIDLOG_TOWN
	end

@ Project Grounded: rivaal na de Hall of Fame (gevecht 7). Zichtbaar (FLAG_TEMP_1) tot FLAG_RIVAL_PG_PACIFIDLOG_DONE.
@ Team: TRAINER_RIVAL_POSTGAME_* (src/rival_postgame.c kiest BRENDAN/MAY en fase).
PacifidlogTown_EventScript_SetupRival::
	setflag FLAG_TEMP_1
	goto_if_unset FLAG_SYS_GAME_CLEAR, Common_EventScript_NopReturn
	goto_if_set FLAG_RIVAL_PG_PACIFIDLOG_DONE, Common_EventScript_NopReturn
	clearflag FLAG_TEMP_1
	setvar VAR_OBJ_GFX_ID_0, OBJ_EVENT_GFX_RIVAL_BRENDAN_NORMAL
	checkplayergender
	goto_if_ne VAR_RESULT, MALE, Common_EventScript_NopReturn
	setvar VAR_OBJ_GFX_ID_0, OBJ_EVENT_GFX_RIVAL_MAY_NORMAL
	return

PacifidlogTown_EventScript_Rival::
	lock
	faceplayer
	call PacifidlogTown_EventScript_RivalMusic
	msgbox PacifidlogTown_Text_RivalPGIntro, MSGBOX_DEFAULT
	switch VAR_STARTER_MON
	case 0, PacifidlogTown_EventScript_RivalTreecko
	case 1, PacifidlogTown_EventScript_RivalTorchic
	case 2, PacifidlogTown_EventScript_RivalMudkip
	end

PacifidlogTown_EventScript_RivalMusic::
	checkplayergender
	goto_if_eq VAR_RESULT, MALE, PacifidlogTown_EventScript_RivalMusicMay
	playbgm MUS_ENCOUNTER_BRENDAN, TRUE
	return

PacifidlogTown_EventScript_RivalMusicMay::
	playbgm MUS_ENCOUNTER_MAY, TRUE
	return

PacifidlogTown_EventScript_RivalTreecko::
	trainerbattle_no_intro TRAINER_RIVAL_POSTGAME_TREECKO, PacifidlogTown_Text_RivalPGDefeat
	goto PacifidlogTown_EventScript_RivalAfter
	end

PacifidlogTown_EventScript_RivalTorchic::
	trainerbattle_no_intro TRAINER_RIVAL_POSTGAME_TORCHIC, PacifidlogTown_Text_RivalPGDefeat
	goto PacifidlogTown_EventScript_RivalAfter
	end

PacifidlogTown_EventScript_RivalMudkip::
	trainerbattle_no_intro TRAINER_RIVAL_POSTGAME_MUDKIP, PacifidlogTown_Text_RivalPGDefeat
	goto PacifidlogTown_EventScript_RivalAfter
	end

PacifidlogTown_EventScript_RivalAfter::
	msgbox PacifidlogTown_Text_RivalPGPostBattle, MSGBOX_DEFAULT
	closemessage
	fadescreen FADE_TO_BLACK
	removeobject LOCALID_PACIFIDLOG_RIVAL
	setflag FLAG_TEMP_1
	setflag FLAG_RIVAL_PG_PACIFIDLOG_DONE
	savebgm MUS_DUMMY
	fadedefaultbgm
	fadescreen FADE_FROM_BLACK
	release
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


PacifidlogTown_Text_RivalPGIntro:
	.string "{RIVAL}: {PLAYER}! Or should I say,\n"
	.string "CHAMPION {PLAYER}. It tastes like\l"
	.string "sand when I say it.\p"
	.string "I came to PACIFIDLOG to think.\n"
	.string "The whole town floats. Just like\l"
	.string "my career.\p"
	.string "Dad says I need a backup plan.\n"
	.string "I said beating you IS my backup\l"
	.string "plan. He sighed for a full minute.\p"
	.string "So. Battle number seven.\n"
	.string "Nobody's counting. I'm counting.$"

PacifidlogTown_Text_RivalPGDefeat:
	.string "Seven losses. That's a whole week.\n"
	.string "You took a week from me.$"

PacifidlogTown_Text_RivalPGPostBattle:
	.string "{RIVAL}: Okay. New plan.\p"
	.string "I'm going to the BATTLE FRONTIER.\n"
	.string "Professionals. Facilities.\l"
	.string "Vending machines.\p"
	.string "If I can't beat you there, with all\n"
	.string "that infrastructure behind me,\l"
	.string "I'll do the sensible thing.\p"
	.string "I'll retire. At thirteen.\p"
	.string "Meet me at the BATTLE TOWER.\n"
	.string "Bring a tissue. For you. Probably.$"
