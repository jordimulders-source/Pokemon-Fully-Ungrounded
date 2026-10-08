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

@ --- zee_vulling_3 (gegenereerd door tools/grounded/maptools/zee_vulling_3.py) ---
Route131_EventScript_ZV3Diver::
	lock
	faceplayer
	msgbox Route131_Text_ZV3Diver, MSGBOX_DEFAULT
	checkitem ITEM_HEART_SCALE, 2
	goto_if_eq VAR_RESULT, FALSE, Route131_EventScript_ZV3Diver_NoScales
	msgbox Route131_Text_ZV3DiverAsk, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, Route131_EventScript_ZV3Diver_No
	removeitem ITEM_HEART_SCALE, 2
	msgbox Route131_Text_ZV3DiverDeal, MSGBOX_DEFAULT
	random 10
	goto_if_lt VAR_RESULT, 4, Route131_EventScript_ZV3Diver_Star
	goto_if_lt VAR_RESULT, 7, Route131_EventScript_ZV3Diver_Pearl
	goto_if_lt VAR_RESULT, 9, Route131_EventScript_ZV3Diver_Nugget
	giveitem ITEM_COMET_SHARD
	goto Route131_EventScript_ZV3Diver_Given
Route131_EventScript_ZV3Diver_Star:
	giveitem ITEM_STAR_PIECE
	goto Route131_EventScript_ZV3Diver_Given
Route131_EventScript_ZV3Diver_Pearl:
	giveitem ITEM_BIG_PEARL
	goto Route131_EventScript_ZV3Diver_Given
Route131_EventScript_ZV3Diver_Nugget:
	giveitem ITEM_NUGGET
Route131_EventScript_ZV3Diver_Given:
	goto_if_eq VAR_RESULT, FALSE, Route131_EventScript_ZV3Diver_Full
	msgbox Route131_Text_ZV3DiverDone, MSGBOX_DEFAULT
	release
	end
Route131_EventScript_ZV3Diver_Full:
	additem ITEM_HEART_SCALE, 2
	msgbox Route131_Text_ZV3DiverFull, MSGBOX_DEFAULT
	release
	end
Route131_EventScript_ZV3Diver_NoScales:
	msgbox Route131_Text_ZV3DiverNoScales, MSGBOX_DEFAULT
	release
	end
Route131_EventScript_ZV3Diver_No:
	msgbox Route131_Text_ZV3DiverNo, MSGBOX_DEFAULT
	release
	end

Route131_Text_ZV3Diver:
	.string "I'm a salvage diver. I dive for\ntreasure in the wrecks down there.\pMostly I find HEART SCALES.\nThen I lose them. I'm a collector\lwith no pockets.$"

Route131_Text_ZV3DiverAsk:
	.string "Tell you what: give me two\nHEART SCALES and I'll give you\lsomething from my last dive.\pI don't know what it is either.\nDeal?$"

Route131_Text_ZV3DiverDeal:
	.string "Pleasure doing business.\nLet me see what's in the bag...$"

Route131_Text_ZV3DiverDone:
	.string "Huh. Better than last time.\nLast time it was a hand.$"

Route131_Text_ZV3DiverFull:
	.string "Your bag is full? Then keep your\nscales. I'm a diver, not a monster.$"

Route131_Text_ZV3DiverNoScales:
	.string "You don't have two HEART SCALES?\nGo look. The sea is full of them.\lThat's where mine went.$"

Route131_Text_ZV3DiverNo:
	.string "Your loss. Literally. I'll just\ndrop them back in the sea.$"

Route131_EventScript_ZV3Rusty::
	trainerbattle_single TRAINER_SAILOR_RUSTY, Route131_Text_ZV3Rusty_Intro, Route131_Text_ZV3Rusty_Defeat
	msgbox Route131_Text_ZV3Rusty_Post, MSGBOX_AUTOCLOSE
	end

Route131_Text_ZV3Rusty_Intro:
	.string "I'm the captain of our salvage\noperation. The boat sank.\pNow I captain this sandbank.\nIt also sinks. Twice a day.$"

Route131_Text_ZV3Rusty_Defeat:
	.string "Abandon sandbank!\n...Never mind. Tide's out.$"

Route131_Text_ZV3Rusty_Post:
	.string "My diver gives away everything he\nfinds. I only keep the paperwork.\lThe paperwork is also wet.$"
@ --- einde zee_vulling_3 ---
