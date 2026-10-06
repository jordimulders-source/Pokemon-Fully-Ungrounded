Route131_MapScripts::
	map_script MAP_SCRIPT_ON_TRANSITION, Route131_OnTransition
	.byte 0

Route131_OnTransition:
	call_if_ge VAR_SOOTOPOLIS_CITY_STATE, 4, Route131_EventScript_CheckSetAbnormalWeather
	call Route131_EventScript_SetLayout
	end

Route131_EventScript_SetLayout::
	setmaplayoutindex LAYOUT_ROUTE131_SKY_PILLAR
	return

Route131_EventScript_CheckSetAbnormalWeather::
	call_if_set FLAG_SYS_WEATHER_CTRL, Common_EventScript_SetAbnormalWeather
	return

Route131_EventScript_Richard::
	trainerbattle_single TRAINER_RICHARD, Route131_Text_RichardIntro, Route131_Text_RichardDefeat
	msgbox Route131_Text_RichardPostBattle, MSGBOX_AUTOCLOSE
	end

Route131_EventScript_Herman::
	trainerbattle_single TRAINER_HERMAN, Route131_Text_HermanIntro, Route131_Text_HermanDefeat
	msgbox Route131_Text_HermanPostBattle, MSGBOX_AUTOCLOSE
	end

Route131_EventScript_Susie::
	trainerbattle_single TRAINER_SUSIE, Route131_Text_SusieIntro, Route131_Text_SusieDefeat
	msgbox Route131_Text_SusiePostBattle, MSGBOX_AUTOCLOSE
	end

Route131_EventScript_Kara::
	trainerbattle_single TRAINER_KARA, Route131_Text_KaraIntro, Route131_Text_KaraDefeat
	msgbox Route131_Text_KaraPostBattle, MSGBOX_AUTOCLOSE
	end

Route131_EventScript_Reli::
	trainerbattle_double TRAINER_RELI_AND_IAN, Route131_Text_ReliIntro, Route131_Text_ReliDefeat, Route131_Text_ReliNotEnoughMons
	msgbox Route131_Text_ReliPostBattle, MSGBOX_AUTOCLOSE
	end

Route131_EventScript_Ian::
	trainerbattle_double TRAINER_RELI_AND_IAN, Route131_Text_IanIntro, Route131_Text_IanDefeat, Route131_Text_IanNotEnoughMons
	msgbox Route131_Text_IanPostBattle, MSGBOX_AUTOCLOSE
	end

Route131_EventScript_Talia::
	trainerbattle_single TRAINER_TALIA, Route131_Text_TaliaIntro, Route131_Text_TaliaDefeat
	msgbox Route131_Text_TaliaPostBattle, MSGBOX_AUTOCLOSE
	end

Route131_EventScript_Kevin::
	trainerbattle_single TRAINER_KEVIN, Route131_Text_KevinIntro, Route131_Text_KevinDefeat
	msgbox Route131_Text_KevinPostBattle, MSGBOX_AUTOCLOSE
	end

@ --- zee_vulling_2 (gegenereerd door tools/grounded/maptools/zee_vulling_2.py) ---
Route131_EventScript_ZV2Cousin::
	lock
	faceplayer
	msgbox Route131_Text_ZV2Cousin, MSGBOX_DEFAULT
	fadescreen FADE_TO_BLACK
	playfanfare MUS_HEAL
	waitfanfare
	special HealPlayerParty
	fadescreen FADE_FROM_BLACK
	msgbox Route131_Text_ZV2CousinDone, MSGBOX_DEFAULT
	release
	end

Route131_Text_ZV2Cousin:
	.string "I'm not a NURSE. I'm a nurse's\ncousin. Very different.\pNo license, no POKeMON CENTER,\nno machine. Just vibes.\pHold still.$"

Route131_Text_ZV2CousinDone:
	.string "There. All better.\nDon't ask what I did.\lLegally I can't tell you.$"

Route131_EventScript_ZV2Bernard::
	trainerbattle_single TRAINER_HIKER_BERNARD, Route131_Text_ZV2Bernard_Intro, Route131_Text_ZV2Bernard_Defeat
	msgbox Route131_Text_ZV2Bernard_Post, MSGBOX_AUTOCLOSE
	end

Route131_Text_ZV2Bernard_Intro:
	.string "I followed the tallest mountain\nI could see.\pIt was SKY PILLAR. It's a tower.\nI don't do towers. I do rocks.$"

Route131_Text_ZV2Bernard_Defeat:
	.string "Rocks: 0. Towers: 1. You: 1.\nI hate this scoreboard.$"

Route131_Text_ZV2Bernard_Post:
	.string "The nurse lady fixed my knee.\nIt's my other knee now. Somehow.$"
@ --- einde zee_vulling_2 ---
