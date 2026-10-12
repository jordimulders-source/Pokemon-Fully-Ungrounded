@ Project Grounded: Yoshi's Island, Wario's fort (tools/grounded/maptools/yoshis_island.py)
YoshisIsland_WarioFort_MapScripts::
	.byte 0

YoshisIsland_WarioFort_EventScript_Guards::
	lock
	faceplayer
	goto YoshisIsland_WarioFort_EventScript_GuardsBattle

YoshisIsland_WarioFort_EventScript_GuardsWon::
	msgbox YoshisIsland_WarioFort_Text_GuardsWon, MSGBOX_DEFAULT
	closemessage
	fadescreenswapbuffers FADE_TO_BLACK
	removeobject LOCALID_YI_FORT_GUARD_A
	removeobject LOCALID_YI_FORT_GUARD_B
	setflag FLAG_YI_FORT_GUARDS
	fadescreenswapbuffers FADE_FROM_BLACK
	release
	end

YoshisIsland_WarioFort_EventScript_Wario::
	lock
	faceplayer
	goto YoshisIsland_WarioFort_EventScript_WarioBattle

YoshisIsland_WarioFort_EventScript_WarioWon::
	msgbox YoshisIsland_WarioFort_Text_WarioWon, MSGBOX_DEFAULT
	closemessage
	fadescreenswapbuffers FADE_TO_BLACK
	removeobject LOCALID_YI_WARIO
	setflag FLAG_YI_WARIO_DONE
	setflag FLAG_SPACETIME_YOSHI_DONE
	fadescreenswapbuffers FADE_FROM_BLACK
	applymovement LOCALID_YI_FORT_YOSHI, Common_Movement_FaceUp
	waitmovement 0
	msgbox YoshisIsland_WarioFort_Text_YoshiThanks, MSGBOX_DEFAULT
	closemessage
	fadescreenswapbuffers FADE_TO_BLACK
	removeobject LOCALID_YI_FORT_YOSHI
	setflag FLAG_YI_YOSHI_HOME
	clearflag FLAG_YI_YOSHI_AHEAD
	fadescreenswapbuffers FADE_FROM_BLACK
	msgbox YoshisIsland_WarioFort_Text_Done, MSGBOX_DEFAULT
	release
	end

YoshisIsland_WarioFort_EventScript_Yoshi::
	msgbox YoshisIsland_WarioFort_Text_Yoshi, MSGBOX_NPC
	end

YoshisIsland_WarioFort_EventScript_GuardsBattle::
	msgbox YoshisIsland_WarioFort_Text_GuardsIntro, MSGBOX_DEFAULT
	closemessage
YoshisIsland_WarioFort_EventScript_GuardsChoose::
	special SavePlayerParty
	fadescreen FADE_TO_BLACK
	special ChooseHalfPartyForBattle
	waitstate
	goto_if_ne VAR_RESULT, 0, YoshisIsland_WarioFort_EventScript_GuardsFight
	special LoadPlayerParty
	goto YoshisIsland_WarioFort_EventScript_GuardsChoose

YoshisIsland_WarioFort_EventScript_GuardsFight::
	multi_2_vs_2 TRAINER_YI_SHY_GUY_FORT_A, YoshisIsland_WarioFort_Text_GuardsDefeatA, TRAINER_YI_SHY_GUY_FORT_B, YoshisIsland_WarioFort_Text_GuardsDefeatB, PARTNER_YOSHI
	switch VAR_RESULT
	case 1, YoshisIsland_WarioFort_EventScript_GuardsWon
	fadescreen FADE_TO_BLACK
	special SetCB2WhiteOut
	waitstate

YoshisIsland_WarioFort_EventScript_WarioBattle::
	msgbox YoshisIsland_WarioFort_Text_WarioIntro, MSGBOX_DEFAULT
	closemessage
YoshisIsland_WarioFort_EventScript_WarioChoose::
	special SavePlayerParty
	fadescreen FADE_TO_BLACK
	special ChooseHalfPartyForBattle
	waitstate
	goto_if_ne VAR_RESULT, 0, YoshisIsland_WarioFort_EventScript_WarioFight
	special LoadPlayerParty
	goto YoshisIsland_WarioFort_EventScript_WarioChoose

YoshisIsland_WarioFort_EventScript_WarioFight::
	multi_2_vs_1 TRAINER_YI_WARIO, YoshisIsland_WarioFort_Text_WarioDefeatA, PARTNER_YOSHI
	switch VAR_RESULT
	case 1, YoshisIsland_WarioFort_EventScript_WarioWon
	fadescreen FADE_TO_BLACK
	special SetCB2WhiteOut
	waitstate

YoshisIsland_WarioFort_EventScript_Throne::
	msgbox YoshisIsland_WarioFort_Text_Throne, MSGBOX_SIGN
	end

@ ---------------------------------------------------------------- teksten (placeholders, Jordi herschrijft ze)
YoshisIsland_WarioFort_Text_GuardsWon:
	.string "(The NINJA GUY vanishes in a puff of\n"
	.string "smoke. The BOUNCER GUY has to walk. It\l"
	.string "takes a while.)$"

YoshisIsland_WarioFort_Text_WarioWon:
	.string "WARIO: WAAAH! My gold! My fort! My mochi\n"
	.string "subscription!\p"
	.string "WARIO: Fine. FINE. I'll go back to my own\n"
	.string "dimension. The one with the microgames.\l"
	.string "You'd have lost those, by the way. Five\l"
	.string "seconds each. No POKéMON. Think about\l"
	.string "it.$"

YoshisIsland_WarioFort_Text_YoshiThanks:
	.string "YOSHI: Yoshi! Yoshi yoshi YOSHI!\p"
	.string "(YOSHI hugs you, hard, the way only a\n"
	.string "dinosaur raised on fruit can. The eggs\l"
	.string "are safe. The SHY GUYS are unemployed.\l"
	.string "He will see you on the beach.)$"

YoshisIsland_WarioFort_Text_Done:
	.string "(Spacetime hums. Somewhere far away, in\n"
	.string "a cave full of rifts, a folded wall\l"
	.string "unfolds a little. The ????? rift sounds\l"
	.string "less confused.)$"

YoshisIsland_WarioFort_Text_Yoshi:
	.string "YOSHI: Yoshi!\p"
	.string "(He is cracking his knuckles. He does\n"
	.string "not have knuckles. It is the thought\l"
	.string "that counts.)$"

YoshisIsland_WarioFort_Text_GuardsIntro:
	.string "(A NINJA GUY and a BOUNCER GUY guard\n"
	.string "the carpet. The BOUNCER GUY checks a\l"
	.string "list. You are not on it. Nobody is on it.\l"
	.string "It is a blank list. That's the joke. He\l"
	.string "doesn't get it either.)\p"
	.string "YOSHI: Yoshi!$"

YoshisIsland_WarioFort_Text_GuardsDefeatA:
	.string "(The NINJA GUY throws a smoke bomb. It\n"
	.string "is a dud. He leaves anyway, on foot, with\l"
	.string "dignity.)$"

YoshisIsland_WarioFort_Text_GuardsDefeatB:
	.string "(The BOUNCER GUY crosses you off the\n"
	.string "blank list.)$"

YoshisIsland_WarioFort_Text_WarioIntro:
	.string "WARIO: WAH HA HA! So YOU'RE the one\n"
	.string "beating up my employees! Do you know\l"
	.string "what SHY GUYS cost? Nothing! I pay\l"
	.string "them in mochi! It's GENIUS!\p"
	.string "WARIO: The fort, the gold, the eggs, the\n"
	.string "island: all WARIO's! And the purple mochi\l"
	.string "guy says the mochi make them do\l"
	.string "whatever I want. No refunds!\p"
	.string "YOSHI: YOSHI!!\p"
	.string "WARIO: Two against one? Fine! WARIO\n"
	.string "doesn't play fair anyway!$"

YoshisIsland_WarioFort_Text_WarioDefeatA:
	.string "WARIO: That was NOT in the contract!$"

YoshisIsland_WarioFort_Text_Throne:
	.string "(A golden throne with a big W on it. The\n"
	.string "cushion is shaped like a very specific\l"
	.string "behind.)$"
