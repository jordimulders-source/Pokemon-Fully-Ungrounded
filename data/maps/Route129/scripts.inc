Route129_MapScripts::
	map_script MAP_SCRIPT_ON_TRANSITION, Route129_OnTransition
	map_script MAP_SCRIPT_ON_LOAD, Route129_OnLoad
	map_script MAP_SCRIPT_ON_FRAME_TABLE, Route129_OnFrame
	.byte 0

Route129_OnLoad:
	call_if_eq VAR_ABNORMAL_WEATHER_LOCATION, ABNORMAL_WEATHER_ROUTE_129_WEST, AbnormalWeather_EventScript_PlaceTilesRoute129West
	call_if_eq VAR_ABNORMAL_WEATHER_LOCATION, ABNORMAL_WEATHER_ROUTE_129_EAST, AbnormalWeather_EventScript_PlaceTilesRoute129East
	end

Route129_OnTransition:
	setvar VAR_0x8004, 3
	call Common_EventScript_GiantWailordSpawn
	call_if_eq VAR_SHOULD_END_ABNORMAL_WEATHER, 1, AbnormalWeather_EventScript_HideMapNamePopup
	call_if_ge VAR_SOOTOPOLIS_CITY_STATE, 4, Route129_EventScript_CheckSetAbnormalWeather
	call_if_eq VAR_ABNORMAL_WEATHER_LOCATION, ABNORMAL_WEATHER_ROUTE_129_WEST, AbnormalWeather_StartKyogreWeather
	call_if_eq VAR_ABNORMAL_WEATHER_LOCATION, ABNORMAL_WEATHER_ROUTE_129_EAST, AbnormalWeather_StartKyogreWeather
	end

Route129_EventScript_CheckSetAbnormalWeather::
	call_if_set FLAG_SYS_WEATHER_CTRL, Common_EventScript_SetAbnormalWeather
	return

Route129_OnFrame:
	map_script_2 VAR_SHOULD_END_ABNORMAL_WEATHER, 1, AbnormalWeather_EventScript_EndEventAndCleanup_1
	.2byte 0

Route129_EventScript_Chase::
	trainerbattle_single TRAINER_CHASE, Route129_Text_ChaseIntro, Route129_Text_ChaseDefeat
	msgbox Route129_Text_ChasePostBattle, MSGBOX_AUTOCLOSE
	end

Route129_EventScript_Allison::
	trainerbattle_single TRAINER_ALLISON, Route129_Text_AllisonIntro, Route129_Text_AllisonDefeat
	msgbox Route129_Text_AllisonPostBattle, MSGBOX_AUTOCLOSE
	end

Route129_EventScript_Juan::
	trainerbattle_single TRAINER_JUAN, Route129_Text_ReedIntro, Route129_Text_ReedDefeat
	msgbox Route129_Text_ReedPostBattle, MSGBOX_AUTOCLOSE
	end

Route129_EventScript_Tisha::
	trainerbattle_single TRAINER_TISHA, Route129_Text_TishaIntro, Route129_Text_TishaDefeat
	msgbox Route129_Text_TishaPostBattle, MSGBOX_AUTOCLOSE
	end

Route129_EventScript_Clarence::
	trainerbattle_single TRAINER_CLARENCE, Route129_Text_ClarenceIntro, Route129_Text_ClarenceDefeat
	msgbox Route129_Text_ClarencePostBattle, MSGBOX_AUTOCLOSE
	end


@ Project Grounded: Juans eiland (waterpodium, leerling, fans, Walrein)
Route129_EventScript_JuanStudent::
	msgbox Route129_Text_JuanStudent, MSGBOX_NPC
	end

Route129_EventScript_JuanFan::
	msgbox Route129_Text_JuanFan, MSGBOX_NPC
	end

Route129_EventScript_JuanCritic::
	msgbox Route129_Text_JuanCritic, MSGBOX_NPC
	end

Route129_EventScript_JuanWalrein::
	lock
	playmoncry SPECIES_WALREIN, CRY_MODE_NORMAL
	msgbox Route129_Text_JuanWalrein, MSGBOX_DEFAULT
	waitmoncry
	release
	end

Route129_EventScript_SandWriting::
	msgbox Route129_Text_SandWriting, MSGBOX_SIGN
	end

Route129_Text_JuanStudent:
	.string "Master JUAN says I'm not swimming.\n"
	.string "I'm “a living fountain.”\p"
	.string "I've been a living fountain for six\n"
	.string "hours. I can't feel my legs.\p"
	.string "Very elegant, though.$"

Route129_Text_JuanFan:
	.string "JUAN used to lead the SOOTOPOLIS\n"
	.string "GYM. He taught WALLACE everything.\p"
	.string "Then WALLACE took the GYM.\p"
	.string "Now JUAN has his own island.\n"
	.string "Honestly? Better view.$"

Route129_Text_JuanCritic:
	.string "I review JUAN's water shows.\p"
	.string "Three stars. The water was wet.\n"
	.string "The drama was wetter.\p"
	.string "I come back every day. Not for the\n"
	.string "show. My boat sank in 2003.$"

Route129_Text_JuanWalrein:
	.string "WALREIN is sunbathing.\n"
	.string "It refuses to be part of the show.$"

Route129_Text_SandWriting:
	.string "Words are drawn in the sand:\p"
	.string "JUAN'S OPEN-AIR WATER ACADEMY\n"
	.string "Lessons: free. Dignity: extra.\p"
	.string "Looking for the SOOTOPOLIS GYM?\n"
	.string "Ask WALLACE. (Sore subject.)$"
