Route133_MapScripts::
	.byte 0

Route133_EventScript_Franklin::
	trainerbattle_single TRAINER_FRANKLIN, Route133_Text_FranklinIntro, Route133_Text_FranklinDefeat
	msgbox Route133_Text_FranklinPostBattle, MSGBOX_AUTOCLOSE
	end

Route133_EventScript_Debra::
	trainerbattle_single TRAINER_DEBRA, Route133_Text_DebraIntro, Route133_Text_DebraDefeat
	msgbox Route133_Text_DebraPostBattle, MSGBOX_AUTOCLOSE
	end

Route133_EventScript_Linda::
	trainerbattle_single TRAINER_LINDA, Route133_Text_LindaIntro, Route133_Text_LindaDefeat
	msgbox Route133_Text_LindaPostBattle, MSGBOX_AUTOCLOSE
	end

Route133_EventScript_Warren::
	trainerbattle_single TRAINER_WARREN, Route133_Text_WarrenIntro, Route133_Text_WarrenDefeat
	msgbox Route133_Text_WarrenPostBattle, MSGBOX_AUTOCLOSE
	end

Route133_EventScript_Beck::
	trainerbattle_single TRAINER_BECK, Route133_Text_BeckIntro, Route133_Text_BeckDefeat
	msgbox Route133_Text_BeckPostBattle, MSGBOX_AUTOCLOSE
	end

Route133_EventScript_Mollie::
	trainerbattle_single TRAINER_MOLLIE, Route133_Text_MollieIntro, Route133_Text_MollieDefeat
	msgbox Route133_Text_MolliePostBattle, MSGBOX_AUTOCLOSE
	end

Route133_EventScript_Conor::
	trainerbattle_single TRAINER_CONOR, Route133_Text_ConorIntro, Route133_Text_ConorDefeat
	msgbox Route133_Text_ConorPostBattle, MSGBOX_AUTOCLOSE
	end

@ --- zee_vulling_2 (gegenereerd door tools/grounded/maptools/zee_vulling_2.py) ---
Route133_EventScript_ZV2Brayden::
	trainerbattle_single TRAINER_BRAYDEN, Route133_Text_ZV2Brayden_Intro, Route133_Text_ZV2Brayden_Defeat
	msgbox Route133_Text_ZV2Brayden_Post, MSGBOX_AUTOCLOSE
	end

Route133_Text_ZV2Brayden_Intro:
	.string "Hey guys, BRAYDEN here! We're\nLIVE from a literal sandbank!\pToday's challenge: battle a random\nkid! Smash that LIKE button!\pThe LIKE button is my POKeMON's\nface. Smash it. Respectfully.$"

Route133_Text_ZV2Brayden_Defeat:
	.string "...Cut that. CUT THAT.\nWe're doing a 'lessons learned'\lvideo now.$"

Route133_Text_ZV2Brayden_Post:
	.string "My sponsor sent me those glasses.\nI threw them over there.\pThey only let you pick one move.\nMy brand is about OPTIONS.$"

Route133_EventScript_ZV2Cameraman::
	msgbox Route133_Text_ZV2Cameraman, MSGBOX_NPC
	end

Route133_Text_ZV2Cameraman:
	.string "I'm not his cameraman. I'm his\ndad. He pays me in exposure.\pWe've been on this sandbank for\nfour hours. The view count is 3.\lTwo of them are me.$"
@ --- einde zee_vulling_2 ---

@ --- zee_vulling_3 (gegenereerd door tools/grounded/maptools/zee_vulling_3.py) ---
Route133_EventScript_ZV3Meteorologist::
	lock
	faceplayer
	goto_if_set FLAG_RECEIVED_ROUTE_133_ICY_ROCK, Route133_EventScript_ZV3Meteorologist_After
	msgbox Route133_Text_ZV3Meteo, MSGBOX_DEFAULT
	giveitem ITEM_ICY_ROCK
	goto_if_eq VAR_RESULT, FALSE, Common_EventScript_ShowBagIsFull
	setflag FLAG_RECEIVED_ROUTE_133_ICY_ROCK
	release
	end
Route133_EventScript_ZV3Meteorologist_After:
	random 4
	goto_if_eq VAR_RESULT, 0, Route133_EventScript_ZV3Meteorologist_F0
	goto_if_eq VAR_RESULT, 1, Route133_EventScript_ZV3Meteorologist_F1
	goto_if_eq VAR_RESULT, 2, Route133_EventScript_ZV3Meteorologist_F2
	msgbox Route133_Text_ZV3Forecast3, MSGBOX_DEFAULT
	release
	end
Route133_EventScript_ZV3Meteorologist_F0:
	msgbox Route133_Text_ZV3Forecast0, MSGBOX_DEFAULT
	release
	end
Route133_EventScript_ZV3Meteorologist_F1:
	msgbox Route133_Text_ZV3Forecast1, MSGBOX_DEFAULT
	release
	end
Route133_EventScript_ZV3Meteorologist_F2:
	msgbox Route133_Text_ZV3Forecast2, MSGBOX_DEFAULT
	release
	end

Route133_Text_ZV3Meteo:
	.string "Welcome to the CASTFORM WEATHER\nOBSERVATION POST. Staff: me.\lEquipment: CASTFORM.\pWhen it's sunny, CASTFORM looks\nsunny. When it rains, it looks\lrainy. Science.\pMy grant ran out, so the ice\ncooler goes. Take this rock.\lIt's the cold part.$"

Route133_Text_ZV3Forecast0:
	.string "Today's forecast: CASTFORM looks\nnormal. So: weather. Probably.$"

Route133_Text_ZV3Forecast1:
	.string "CASTFORM sneezed. That's either\nrain or allergies. I'm writing\l'rain'. Nobody checks.$"

Route133_Text_ZV3Forecast2:
	.string "Forecast: 90% chance of KYOGRE.\nJust kidding. 40%.$"

Route133_Text_ZV3Forecast3:
	.string "I've predicted the weather here\nfor six years. I've been right\lonce. It was a guess.$"

Route133_EventScript_ZV3Castform::
	lock
	faceplayer
	playmoncry SPECIES_CASTFORM, CRY_MODE_NORMAL
	msgbox Route133_Text_ZV3Castform, MSGBOX_DEFAULT
	waitmoncry
	release
	end

Route133_Text_ZV3Castform:
	.string "CASTFORM: Pyuu!\pIt's wearing a tiny label:\n'PROPERTY OF THE WEATHER INSTITUTE.\lIF FOUND, IT'S PROBABLY RAINING.'$"

Route133_EventScript_ZV3Post::
	msgbox Route133_Text_ZV3Post, MSGBOX_SIGN
	end

Route133_Text_ZV3Post:
	.string "CASTFORM WEATHER OBSERVATION POST\pToday: see CASTFORM.\nTomorrow: see CASTFORM tomorrow.$"
@ --- einde zee_vulling_3 ---
