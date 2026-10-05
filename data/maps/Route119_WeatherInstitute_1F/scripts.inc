Route119_WeatherInstitute_1F_MapScripts::
	map_script MAP_SCRIPT_ON_TRANSITION, Route119_WeatherInstitute_1F_OnTransition
	.byte 0

Route119_WeatherInstitute_1F_OnTransition:
	call_if_eq VAR_WEATHER_INSTITUTE_STATE, 0, Route119_WeatherInstitute_1F_EventScript_SetLittleBoyPos
	setflag FLAG_HIDE_WEATHER_INSTITUTE_ARCHIE_MAXIE
	call_if_set FLAG_SYS_GAME_CLEAR, Route119_WeatherInstitute_1F_EventScript_ShowArchieMaxie
	end

Route119_WeatherInstitute_1F_EventScript_ShowArchieMaxie::
	clearflag FLAG_HIDE_WEATHER_INSTITUTE_ARCHIE_MAXIE
	return

@ Project Grounded: Archie en Maxie doen post-game hun werkstraf in het Weather Institute (ze hebben het weer gesloopt).
@ Eén dubbelgevecht per dag tegen allebei; na elke overwinning een sterkere ronde (VAR_WEATHER_SERVICE_TIER, max. ronde 4).
Route119_WeatherInstitute_1F_EventScript_ArchieMaxie::
	lock
	faceplayer
	goto_if_set FLAG_DAILY_WEATHER_SERVICE_BATTLE, Route119_WeatherInstitute_1F_EventScript_ServiceDone
	specialvar VAR_RESULT, GetMonsStateToDoubles
	goto_if_ne VAR_RESULT, PLAYER_HAS_TWO_USABLE_MONS, Route119_WeatherInstitute_1F_EventScript_ServiceNeedTwo
	call_if_eq VAR_WEATHER_SERVICE_TIER, 0, Route119_WeatherInstitute_1F_EventScript_ServiceIntroFirst
	call_if_ne VAR_WEATHER_SERVICE_TIER, 0, Route119_WeatherInstitute_1F_EventScript_ServiceIntroAgain
	closemessage
	switch VAR_WEATHER_SERVICE_TIER
	case 0, Route119_WeatherInstitute_1F_EventScript_ServiceBattle1
	case 1, Route119_WeatherInstitute_1F_EventScript_ServiceBattle2
	case 2, Route119_WeatherInstitute_1F_EventScript_ServiceBattle3
	goto Route119_WeatherInstitute_1F_EventScript_ServiceBattle4
	end

Route119_WeatherInstitute_1F_EventScript_ServiceIntroFirst::
	msgbox Route119_WeatherInstitute_1F_Text_ServiceIntroFirst, MSGBOX_DEFAULT
	return

Route119_WeatherInstitute_1F_EventScript_ServiceIntroAgain::
	msgbox Route119_WeatherInstitute_1F_Text_ServiceIntroAgain, MSGBOX_DEFAULT
	return

Route119_WeatherInstitute_1F_EventScript_ServiceBattle1::
	cleartrainerflag TRAINER_ARCHIE_SERVICE_1
	cleartrainerflag TRAINER_MAXIE_SERVICE_1
	trainerbattle_two_trainers TRAINER_ARCHIE_SERVICE_1, Route119_WeatherInstitute_1F_Text_ArchieServiceDefeat, TRAINER_MAXIE_SERVICE_1, Route119_WeatherInstitute_1F_Text_MaxieServiceDefeat
	goto Route119_WeatherInstitute_1F_EventScript_ServiceWon
	end

Route119_WeatherInstitute_1F_EventScript_ServiceBattle2::
	cleartrainerflag TRAINER_ARCHIE_SERVICE_2
	cleartrainerflag TRAINER_MAXIE_SERVICE_2
	trainerbattle_two_trainers TRAINER_ARCHIE_SERVICE_2, Route119_WeatherInstitute_1F_Text_ArchieServiceDefeat, TRAINER_MAXIE_SERVICE_2, Route119_WeatherInstitute_1F_Text_MaxieServiceDefeat
	goto Route119_WeatherInstitute_1F_EventScript_ServiceWon
	end

Route119_WeatherInstitute_1F_EventScript_ServiceBattle3::
	cleartrainerflag TRAINER_ARCHIE_SERVICE_3
	cleartrainerflag TRAINER_MAXIE_SERVICE_3
	trainerbattle_two_trainers TRAINER_ARCHIE_SERVICE_3, Route119_WeatherInstitute_1F_Text_ArchieServiceDefeat, TRAINER_MAXIE_SERVICE_3, Route119_WeatherInstitute_1F_Text_MaxieServiceDefeat
	goto Route119_WeatherInstitute_1F_EventScript_ServiceWon
	end

Route119_WeatherInstitute_1F_EventScript_ServiceBattle4::
	cleartrainerflag TRAINER_ARCHIE_SERVICE_4
	cleartrainerflag TRAINER_MAXIE_SERVICE_4
	trainerbattle_two_trainers TRAINER_ARCHIE_SERVICE_4, Route119_WeatherInstitute_1F_Text_ArchieServiceDefeat, TRAINER_MAXIE_SERVICE_4, Route119_WeatherInstitute_1F_Text_MaxieServiceDefeat
	goto Route119_WeatherInstitute_1F_EventScript_ServiceWon
	end

Route119_WeatherInstitute_1F_EventScript_ServiceWon::
	setflag FLAG_DAILY_WEATHER_SERVICE_BATTLE
	call_if_lt VAR_WEATHER_SERVICE_TIER, 3, Route119_WeatherInstitute_1F_EventScript_ServiceTierUp
	msgbox Route119_WeatherInstitute_1F_Text_ServiceWon, MSGBOX_DEFAULT
	release
	end

Route119_WeatherInstitute_1F_EventScript_ServiceTierUp::
	addvar VAR_WEATHER_SERVICE_TIER, 1
	return

Route119_WeatherInstitute_1F_EventScript_ServiceDone::
	msgbox Route119_WeatherInstitute_1F_Text_ServiceDone, MSGBOX_DEFAULT
	release
	end

Route119_WeatherInstitute_1F_EventScript_ServiceNeedTwo::
	msgbox Route119_WeatherInstitute_1F_Text_ServiceNeedTwo, MSGBOX_DEFAULT
	release
	end

Route119_WeatherInstitute_1F_EventScript_SetLittleBoyPos::
	setobjectxyperm LOCALID_WEATHER_INSTITUTE_LITTLE_BOY, 0, 5
	setobjectmovementtype LOCALID_WEATHER_INSTITUTE_LITTLE_BOY, MOVEMENT_TYPE_FACE_RIGHT
	return

Route119_WeatherInstitute_1F_EventScript_LittleBoy::
	lock
	faceplayer
	special GetPlayerBigGuyGirlString
	goto_if_eq VAR_WEATHER_INSTITUTE_STATE, 0, Route119_WeatherInstitute_1F_EventScript_LittleBoyTeamAquaHere
	msgbox Route119_WeatherInstitute_1F_Text_WowYoureStrong, MSGBOX_DEFAULT
	release
	end

Route119_WeatherInstitute_1F_EventScript_LittleBoyTeamAquaHere::
	msgbox Route119_WeatherInstitute_1F_Text_EveryoneWentUpstairs, MSGBOX_DEFAULT
	release
	end

Route119_WeatherInstitute_1F_EventScript_InstituteWorker1::
	lock
	faceplayer
	goto_if_unset FLAG_SYS_GAME_CLEAR, Route119_WeatherInstitute_1F_EventScript_StudyingRain
	setvar VAR_0x8004, 0
	call_if_set FLAG_DEFEATED_KYOGRE, Route119_WeatherInstitute_1F_EventScript_LegendaryDefeated
	call_if_set FLAG_DEFEATED_GROUDON, Route119_WeatherInstitute_1F_EventScript_LegendaryDefeated
	goto_if_eq VAR_0x8004, 2, Route119_WeatherInstitute_1F_EventScript_StudyingRain  @ Both defeated
	msgbox Route119_WeatherInstitute_1F_Text_NoticingAbnormalWeather, MSGBOX_DEFAULT
	release
	end

Route119_WeatherInstitute_1F_EventScript_LegendaryDefeated::
	addvar VAR_0x8004, 1
	return

Route119_WeatherInstitute_1F_EventScript_StudyingRain::
	msgbox Route119_WeatherInstitute_1F_Text_ProfStudyingRain, MSGBOX_DEFAULT
	release
	end

Route119_WeatherInstitute_1F_EventScript_InstituteWorker2::
	msgbox Route119_WeatherInstitute_1F_Text_WhatWereAquasUpTo, MSGBOX_NPC
	end

Route119_WeatherInstitute_1F_EventScript_Bed::
	lockall
	msgbox Route119_WeatherInstitute_1F_Text_TakeRestInBed, MSGBOX_DEFAULT
	closemessage
	call Common_EventScript_OutOfCenterPartyHeal
	releaseall
	end

Route119_WeatherInstitute_1F_EventScript_Grunt1::
	trainerbattle_single TRAINER_GRUNT_WEATHER_INST_1, Route119_WeatherInstitute_1F_Text_Grunt1Intro, Route119_WeatherInstitute_1F_Text_Grunt1Defeat
	msgbox Route119_WeatherInstitute_1F_Text_Grunt1PostBattle, MSGBOX_AUTOCLOSE
	end

Route119_WeatherInstitute_1F_EventScript_Grunt4::
	trainerbattle_single TRAINER_GRUNT_WEATHER_INST_4, Route119_WeatherInstitute_1F_Text_Grunt4Intro, Route119_WeatherInstitute_1F_Text_Grunt4Defeat
	msgbox Route119_WeatherInstitute_1F_Text_Grunt4PostBattle, MSGBOX_AUTOCLOSE
	end

Route119_WeatherInstitute_1F_Text_Grunt1Intro:
	.string "The BOSS wants the research here.\p"
	.string "Rain is free water. We just add bubbles.$"

Route119_WeatherInstitute_1F_Text_Grunt1Defeat:
	.string "Blasted by a kid…\p"
	.string "And not even carbonated.$"

Route119_WeatherInstitute_1F_Text_Grunt1PostBattle:
	.string "Our BOSS knows everything.\p"
	.string "I just know SPA beats SOURCY.$"

Route119_WeatherInstitute_1F_Text_Grunt4Intro:
	.string "Huh? A kid?\p"
	.string "Want a PERRIER? No?\p"
	.string "Then battle!$"

Route119_WeatherInstitute_1F_Text_Grunt4Defeat:
	.string "I lost? My bubbles…$"

Route119_WeatherInstitute_1F_Text_Grunt4PostBattle:
	.string "I'll catch an earful for this.\p"
	.string "I'll drink my feelings. Sparkling.$"

Route119_WeatherInstitute_1F_Text_EveryoneWentUpstairs:
	.string "While I was asleep, everyone went\n"
	.string "upstairs!\p"
	.string "Was there cake?$"

Route119_WeatherInstitute_1F_Text_WowYoureStrong:
	.string "Wow, you're strong! SENPAI noticed me!$"

Route119_WeatherInstitute_1F_Text_ProfStudyingRain:
	.string "The PROFESSOR loves rain. Fact.\p"
	.string "Too much rain causes trouble. Also a\n"
	.string "fact.\p"
	.string "So he's studying how to use rain for\n"
	.string "good.\p"
	.string "TEAM AQUA wants to add bubbles to it.\n"
	.string "Not a fact yet.$"

Route119_WeatherInstitute_1F_Text_NoticingAbnormalWeather:
	.string "Upstairs we study HOENN's weather.\p"
	.string "Lately: sudden droughts and sudden\n"
	.string "floods.\p"
	.string "Something big is going on. Or it's\n"
	.string "climate change. Or both.$"

Route119_WeatherInstitute_1F_Text_WhatWereAquasUpTo:
	.string "Hello! You saved us!\p"
	.string "What were those AQUAS even doing here?\p"
	.string "They left 300 empty bottles.$"

Route119_WeatherInstitute_1F_Text_TakeRestInBed:
	.string "There's a bed… Let's take a rest.$"


Route119_WeatherInstitute_1F_Text_ServiceIntroFirst:
	.string "ARCHIE: Oh. It's you. Don't look at\n"
	.string "the mop. The mop is temporary.\p"
	.string "MAXIE: Community service. Six hundred\n"
	.string "hours. For “unscheduled climate\l"
	.string "events”, the judge called it.\p"
	.string "ARCHIE: I flooded a continent.\n"
	.string "He dried it. We're basically even.\p"
	.string "MAXIE: The judge disagreed.\p"
	.string "ARCHIE: Anyway, the institute lets us\n"
	.string "battle in our break. Builds character.\l"
	.string "Ours, not yours. Yours is fine.\p"
	.string "MAXIE: Two of us, two of yours.\n"
	.string "Please. I have mopped since dawn.$"

Route119_WeatherInstitute_1F_Text_ServiceIntroAgain:
	.string "ARCHIE: Break time! We trained!\n"
	.string "Between the mopping!\p"
	.string "MAXIE: We have also been reading\n"
	.string "the weather reports. For revenge.$"

Route119_WeatherInstitute_1F_Text_ArchieServiceDefeat:
	.string "ARCHIE: The sea is still bigger\n"
	.string "than you. Just so you know.$"

Route119_WeatherInstitute_1F_Text_MaxieServiceDefeat:
	.string "MAXIE: Statistically, this was\n"
	.string "the land's fault.$"

Route119_WeatherInstitute_1F_Text_ServiceWon:
	.string "ARCHIE: Same time tomorrow? We'll\n"
	.string "be here. Legally we have to be.\p"
	.string "MAXIE: We'll come back stronger.\n"
	.string "The court gave us a lot of free time.$"

Route119_WeatherInstitute_1F_Text_ServiceDone:
	.string "MAXIE: Break's over. The probation\n"
	.string "officer is watching. Come back\l"
	.string "tomorrow.\p"
	.string "ARCHIE: Bring sunscreen. Or an\n"
	.string "umbrella. We're not allowed to say.$"

Route119_WeatherInstitute_1F_Text_ServiceNeedTwo:
	.string "ARCHIE: Two against one? We're\n"
	.string "villains, not monsters.\p"
	.string "MAXIE: Come back with at least\n"
	.string "two POKéMON that can still stand.$"
