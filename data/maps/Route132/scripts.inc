Route132_MapScripts::
	map_script MAP_SCRIPT_ON_TRANSITION, Route132_OnTransition
	.byte 0

@ Project Grounded: eb en vloed. Even uur = eb (wad ten noorden van het zandeiland valt droog), oneven uur = vloed.
@ Alleen bij binnenkomst; de layout blijft tot je de kaart verlaat (ook na laden van een save).
Route132_OnTransition:
	special Grounded_UpdateTide
	call_if_unset FLAG_TIDE_HIGH, Route132_EventScript_SetLowTide
	end

Route132_EventScript_SetLowTide::
	setmaplayoutindex LAYOUT_ROUTE132_LOW_TIDE
	return

Route132_EventScript_Gilbert::
	trainerbattle_single TRAINER_GILBERT, Route132_Text_GilbertIntro, Route132_Text_GilbertDefeat
	msgbox Route132_Text_GilbertPostBattle, MSGBOX_AUTOCLOSE
	end

Route132_EventScript_Dana::
	trainerbattle_single TRAINER_DANA, Route132_Text_DanaIntro, Route132_Text_DanaDefeat
	msgbox Route132_Text_DanaPostBattle, MSGBOX_AUTOCLOSE
	end

Route132_EventScript_Ronald::
	trainerbattle_single TRAINER_RONALD, Route132_Text_RonaldIntro, Route132_Text_RonaldDefeat
	msgbox Route132_Text_RonaldPostBattle, MSGBOX_AUTOCLOSE
	end

Route132_EventScript_Kiyo::
	trainerbattle_single TRAINER_KIYO, Route132_Text_KiyoIntro, Route132_Text_KiyoDefeat
	msgbox Route132_Text_KiyoPostBattle, MSGBOX_AUTOCLOSE
	end

Route132_EventScript_Paxton::
	trainerbattle_single TRAINER_PAXTON, Route132_Text_PaxtonIntro, Route132_Text_PaxtonDefeat
	msgbox Route132_Text_PaxtonPostBattle, MSGBOX_AUTOCLOSE
	end

Route132_EventScript_Darcy::
	trainerbattle_single TRAINER_DARCY, Route132_Text_DarcyIntro, Route132_Text_DarcyDefeat
	msgbox Route132_Text_DarcyPostBattle, MSGBOX_AUTOCLOSE
	end

Route132_EventScript_Jonathan::
	trainerbattle_single TRAINER_JONATHAN, Route132_Text_JonathanIntro, Route132_Text_JonathanDefeat
	msgbox Route132_Text_JonathanPostBattle, MSGBOX_AUTOCLOSE
	end

Route132_EventScript_Makayla::
	trainerbattle_single TRAINER_MAKAYLA, Route132_Text_MakaylaIntro, Route132_Text_MakaylaDefeat
	msgbox Route132_Text_MakaylaPostBattle, MSGBOX_AUTOCLOSE
	end


@ Project Grounded: strandjutter op het wad (alleen bij eb), geeft elke dag een vondst
Route132_EventScript_Beachcomber::
	lock
	faceplayer
	goto_if_set FLAG_DAILY_BEACHCOMBER_FIND, Route132_EventScript_BeachcomberTide
	msgbox Route132_Text_BeachcomberIntro, MSGBOX_DEFAULT
	random 8
	switch VAR_RESULT
	case 0, Route132_EventScript_BeachcomberPearl
	case 1, Route132_EventScript_BeachcomberBigPearl
	case 2, Route132_EventScript_BeachcomberStardust
	case 3, Route132_EventScript_BeachcomberShoalSalt
	case 4, Route132_EventScript_BeachcomberShoalShell
	case 5, Route132_EventScript_BeachcomberNetBall
	case 6, Route132_EventScript_BeachcomberStarPiece
	setvar VAR_0x8008, ITEM_HEART_SCALE
	goto Route132_EventScript_BeachcomberGive

Route132_EventScript_BeachcomberPearl::
	setvar VAR_0x8008, ITEM_PEARL
	goto Route132_EventScript_BeachcomberGive

Route132_EventScript_BeachcomberBigPearl::
	setvar VAR_0x8008, ITEM_BIG_PEARL
	goto Route132_EventScript_BeachcomberGive

Route132_EventScript_BeachcomberStardust::
	setvar VAR_0x8008, ITEM_STARDUST
	goto Route132_EventScript_BeachcomberGive

Route132_EventScript_BeachcomberShoalSalt::
	setvar VAR_0x8008, ITEM_SHOAL_SALT
	goto Route132_EventScript_BeachcomberGive

Route132_EventScript_BeachcomberShoalShell::
	setvar VAR_0x8008, ITEM_SHOAL_SHELL
	goto Route132_EventScript_BeachcomberGive

Route132_EventScript_BeachcomberNetBall::
	setvar VAR_0x8008, ITEM_NET_BALL
	goto Route132_EventScript_BeachcomberGive

Route132_EventScript_BeachcomberStarPiece::
	setvar VAR_0x8008, ITEM_STAR_PIECE
	goto Route132_EventScript_BeachcomberGive

Route132_EventScript_BeachcomberGive::
	giveitem VAR_0x8008
	goto_if_eq VAR_RESULT, FALSE, Route132_EventScript_BeachcomberBagFull
	setflag FLAG_DAILY_BEACHCOMBER_FIND
	goto Route132_EventScript_BeachcomberTide

Route132_EventScript_BeachcomberBagFull::
	msgbox Route132_Text_BeachcomberBagFull, MSGBOX_DEFAULT
	release
	end

Route132_EventScript_BeachcomberTide::
	special Grounded_TideMinutesLeft
	buffernumberstring STR_VAR_1, VAR_RESULT
	msgbox Route132_Text_BeachcomberTide, MSGBOX_DEFAULT
	release
	end

Route132_EventScript_TideCarving::
	msgbox Route132_Text_TideCarving, MSGBOX_SIGN
	end

Route132_Text_BeachcomberIntro:
	.string "Low tide! The sea pulls back and\n"
	.string "leaves its pockets on the floor.\p"
	.string "I'm a beachcomber. It's like being\n"
	.string "a burglar, but the victim is the\l"
	.string "ocean, and it can't press charges.\p"
	.string "Here, today's find. Don't ask what\n"
	.string "it was stuck to.$"

Route132_Text_BeachcomberBagFull:
	.string "Your BAG is full? Then the ocean\n"
	.string "keeps it. The ocean always wins.$"

Route132_Text_BeachcomberTide:
	.string "The tide turns every hour, on the\n"
	.string "hour. Even hours: low. Odd: high.\p"
	.string "Next turn in {STR_VAR_1} minutes. But this\n"
	.string "sea is lazy. It only checks the\l"
	.string "clock when you leave and come back.\p"
	.string "Like a cat. Or a landlord.\p"
	.string "Come back tomorrow. The sea always\n"
	.string "coughs up more. Mostly regret.$"

Route132_Text_TideCarving:
	.string "Someone carved a tide table into\n"
	.string "the rock.\p"
	.string "EVEN HOURS: low tide. Walk north.\n"
	.string "ODD HOURS: high tide. Swim north.\p"
	.string "ALWAYS: do not lick the rocks.\n"
	.string "(We know it was you, GERALD.)$"
