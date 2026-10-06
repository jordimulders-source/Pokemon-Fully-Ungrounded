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
