EverGrandeCity_MapScripts::
	map_script MAP_SCRIPT_ON_TRANSITION, EverGrandeCity_OnTransition
	.byte 0

EverGrandeCity_OnTransition:
	call_if_set FLAG_SYS_WEATHER_CTRL, Common_EventScript_SetAbnormalWeather
	end

EverGrandeCity_EventScript_VictoryRoadSign::
	msgbox EverGrandeCity_Text_EnteringVictoryRoad, MSGBOX_SIGN
	end

EverGrandeCity_EventScript_CitySign::
	msgbox EverGrandeCity_Text_CitySign, MSGBOX_SIGN
	end

EverGrandeCity_EventScript_PokemonLeagueSign::
	msgbox EverGrandeCity_Text_EnteringPokemonLeague, MSGBOX_SIGN
	end

EverGrandeCity_EventScript_SetVisitedEverGrande::
	setflag FLAG_VISITED_EVER_GRANDE_CITY
	setvar VAR_TEMP_1, 1
	end

EverGrandeCity_Text_EnteringVictoryRoad:
	.string "ENTERING VICTORY ROAD\p"
	.string "Last chance to turn back.$"

EverGrandeCity_Text_EnteringPokemonLeague:
	.string "ENTERING POKéMON LEAGUE\p"
	.string "No refunds.$"

EverGrandeCity_Text_CitySign:
	.string "EVER GRANDE CITY\p"
	.string "“The paradise of flowers, the sea, and\n"
	.string "very tired TRAINERS.”$"

@ Project Grounded: Victory-gauntlet (post-game), uitdager V. Zie LibertyGarden/scripts.inc.
EverGrandeCity_EventScript_VictoryChallengerV::
	goto_if_unset FLAG_SYS_GAME_CLEAR, EverGrandeCity_EventScript_VictoryChallengerVNotYet
	trainerbattle_single TRAINER_VICTORY_V, EverGrandeCity_Text_VictoryVIntro, EverGrandeCity_Text_VictoryVDefeat, EverGrandeCity_EventScript_VictoryChallengerVStamp
	msgbox EverGrandeCity_Text_VictoryVPost, MSGBOX_AUTOCLOSE
	end

EverGrandeCity_EventScript_VictoryChallengerVNotYet::
	msgbox EverGrandeCity_Text_VictoryVNotYet, MSGBOX_NPC
	end

EverGrandeCity_EventScript_VictoryChallengerVStamp::
	call VictoryGauntlet_EventScript_GiveStamp
	release
	end

EverGrandeCity_Text_VictoryVNotYet:
	.string "V does not battle the uncrowned.\p"
	.string "Become CHAMPION. Then return.\p"
	.string "That is the way of V. It's also just the\n"
	.string "rules.$"

EverGrandeCity_Text_VictoryVIntro:
	.string "I am V.\p"
	.string "V for VICTORY. V for VENGEANCE. V for...\n"
	.string "very little imagination.\p"
	.string "Every POKéMON I own starts with a V.\n"
	.string "The rules were my idea.\p"
	.string "I am the last VICTORY CHALLENGER.\n"
	.string "Probably. The order is your choice,\l"
	.string "actually.$"

EverGrandeCity_Text_VictoryVDefeat:
	.string "V... for... VANQUISHED.\p"
	.string "I walked right into that one.$"

EverGrandeCity_Text_VictoryVPost:
	.string "I tried to catch a VICTINI once. It said\n"
	.string "no.\p"
	.string "VICTINI, I mean. Not the letter V. The\n"
	.string "letter V and I are fine.$"
