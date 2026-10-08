Route107_MapScripts::
	.byte 0

Route107_EventScript_Darrin::
	trainerbattle_single TRAINER_DARRIN, Route107_Text_DarrinIntro, Route107_Text_DarrinDefeated
	msgbox Route107_Text_DarrinPostBattle, MSGBOX_AUTOCLOSE
	end

Route107_EventScript_Tony::
	trainerbattle_single TRAINER_TONY_1, Route107_Text_TonyIntro, Route107_Text_TonyDefeated, Route107_EventScript_TonyRegisterMatchCallAfterBattle
	specialvar VAR_RESULT, ShouldTryRematchBattle
	goto_if_eq VAR_RESULT, TRUE, Route107_EventScript_TonyRematch
	msgbox Route107_Text_TonyPostBattle, MSGBOX_DEFAULT
	release
	end

Route107_EventScript_TonyRegisterMatchCallAfterBattle::
	special PlayerFaceTrainerAfterBattle
	waitmovement 0
	msgbox Route107_Text_TonyRegister, MSGBOX_DEFAULT
	register_matchcall TRAINER_TONY_1
	release
	end

Route107_EventScript_TonyRematch::
	trainerbattle_rematch TRAINER_TONY_1, Route107_Text_TonyRematchIntro, Route107_Text_TonyRematchDefeated
	msgbox Route107_Text_TonyRematchPostBattle, MSGBOX_AUTOCLOSE
	end

Route107_EventScript_Denise::
	trainerbattle_single TRAINER_DENISE, Route107_Text_DeniseIntro, Route107_Text_DeniseDefeated
	msgbox Route107_Text_DenisePostBattle, MSGBOX_AUTOCLOSE
	end

Route107_EventScript_Beth::
	trainerbattle_single TRAINER_BETH, Route107_Text_BethIntro, Route107_Text_BethDefeated
	msgbox Route107_Text_BethPostBattle, MSGBOX_AUTOCLOSE
	end

Route107_EventScript_Lisa::
	trainerbattle_double TRAINER_LISA_AND_RAY, Route107_Text_LisaIntro, Route107_Text_LisaDefeated, Route107_Text_LisaNotEnoughPokemon
	msgbox Route107_Text_LisaPostBattle, MSGBOX_AUTOCLOSE
	end

Route107_EventScript_Ray::
	trainerbattle_double TRAINER_LISA_AND_RAY, Route107_Text_RayIntro, Route107_Text_RayDefeated, Route107_Text_RayNotEnoughPokemon
	msgbox Route107_Text_RayPostBattle, MSGBOX_AUTOCLOSE
	end

Route107_EventScript_Camron::
	trainerbattle_single TRAINER_CAMRON, Route107_Text_CamronIntro, Route107_Text_CamronDefeated
	msgbox Route107_Text_CamronPostBattle, MSGBOX_AUTOCLOSE
	end

@ --- zee_vulling_1 (gegenereerd door tools/grounded/maptools/zee_vulling_1.py) ---
Route107_EventScript_ZVSushiChef::
	lock
	faceplayer
	goto_if_set FLAG_RECEIVED_ROUTE_107_LEFTOVERS, Route107_EventScript_ZVSushiChef_After
	msgbox Route107_Text_ZVSushiChef, MSGBOX_DEFAULT
	giveitem ITEM_LEFTOVERS
	goto_if_eq VAR_RESULT, FALSE, Common_EventScript_ShowBagIsFull
	setflag FLAG_RECEIVED_ROUTE_107_LEFTOVERS
	release
	end
Route107_EventScript_ZVSushiChef_After:
	msgbox Route107_Text_ZVSushiChefAfter, MSGBOX_DEFAULT
	release
	end

Route107_Text_ZVSushiChef:
	.string "Welcome to SUSHI 107. Omakase only.\nSeating: one sandbank.\pI used to serve raw fish. Then a\nWAILMER watched me through the\lwindow. For three days. Blinking.\pNow I serve rice. Just rice.\nHere, take the leftovers.\lLiterally. They're called that.$"

Route107_Text_ZVSushiChefAfter:
	.string "Today's special is rice.\nYesterday's special was also rice.\pTomorrow? Don't spoil it.$"

Route107_EventScript_ZVBoat::
	msgbox Route107_Text_ZVBoat, MSGBOX_SIGN
	end

Route107_Text_ZVBoat:
	.string "A boat named the S.S. NIGIRI.\nThe hull says: 'NOT A DELIVERY BOAT.'\lSomeone has added: 'UBER?'$"

Route107_EventScript_ZVRuin::
	msgbox Route107_Text_ZVRuin, MSGBOX_SIGN
	end

Route107_Text_ZVRuin:
	.string "It's a rock.\pSomeone has scratched into it:\n'ANCIENT RUIN. DO NOT TOUCH.\l-SIMON'$"

Route107_EventScript_ZVDuncan::
	trainerbattle_single TRAINER_SAILOR_DUNCAN, Route107_Text_ZVDuncan_Intro, Route107_Text_ZVDuncan_Defeat
	msgbox Route107_Text_ZVDuncan_Post, MSGBOX_AUTOCLOSE
	end

Route107_Text_ZVDuncan_Intro:
	.string "Oi! I've been waiting forty minutes\nfor one bowl of rice!\pI'm taking it out on you. That's\nhow customer service works!$"

Route107_Text_ZVDuncan_Defeat:
	.string "Fine. FINE. I'll leave a\ntwo-star review.$"

Route107_Text_ZVDuncan_Post:
	.string "The rice is actually very good.\nDon't tell him. He'll get ideas.$"

Route107_EventScript_ZVSimon::
	trainerbattle_single TRAINER_RUIN_MANIAC_SIMON, Route107_Text_ZVSimon_Intro, Route107_Text_ZVSimon_Defeat
	msgbox Route107_Text_ZVSimon_Post, MSGBOX_AUTOCLOSE
	end

Route107_Text_ZVSimon_Intro:
	.string "Careful! This rock is an ancient\nruin of the Hoenn sea people!\pProbably! I have no evidence,\nbut I DO have a grant!$"

Route107_Text_ZVSimon_Defeat:
	.string "My research funding...\nIt's slipping away like sand...$"

Route107_Text_ZVSimon_Post:
	.string "Carbon dating says this rock is\n'a rock'. The lab is clearly biased.$"
@ --- einde zee_vulling_1 ---
