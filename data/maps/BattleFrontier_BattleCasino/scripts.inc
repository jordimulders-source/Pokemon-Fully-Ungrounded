@ Project Grounded: Battle Casino (Battle Frontier, oostkant). Inzetten op NPC-gevechten; de logica staat in
@ src/battle_casino.c. Stadium-modi lopen via de Stadium-arena (VAR_STADIUM_STATE = CASINO_STATE_ARENA) en
@ komen hier terug met CASINO_STATE_RESULT. Teksten zijn placeholders.
BattleFrontier_BattleCasino_MapScripts::
	map_script MAP_SCRIPT_ON_FRAME_TABLE, BattleFrontier_BattleCasino_OnFrame
	.byte 0

BattleFrontier_BattleCasino_OnFrame:
	map_script_2 VAR_STADIUM_STATE, CASINO_STATE_RESULT, BattleCasino_EventScript_ArenaResult
	.2byte 0

BattleCasino_EventScript_ArenaResult::
	lockall
	setvar VAR_STADIUM_STATE, 0
	goto BattleCasino_EventScript_Result

BattleCasino_EventScript_Croupier::
	lock
	faceplayer
	goto_if_set FLAG_CASINO_INTRO_SEEN, BattleCasino_EventScript_CroupierCard
	setflag FLAG_CASINO_INTRO_SEEN
	msgbox BattleCasino_Text_Intro, MSGBOX_DEFAULT
BattleCasino_EventScript_CroupierCard::
	special Casino_HasBp
	goto_if_eq VAR_RESULT, FALSE, BattleCasino_EventScript_NoBp
	fadescreen FADE_TO_BLACK
	special Casino_OpenCard
	waitstate
	goto_if_eq VAR_RESULT, CASINO_EXIT_ARENA, BattleCasino_EventScript_ToArena
	goto_if_eq VAR_RESULT, CASINO_EXIT_RESULT, BattleCasino_EventScript_Result
	msgbox BattleCasino_Text_NoBet, MSGBOX_DEFAULT
	release
	end

BattleCasino_EventScript_NoBp::
	msgbox BattleCasino_Text_NoBp, MSGBOX_DEFAULT
	release
	end

@ Stadium-modi: je loopt het stadion in en kijkt vanaf de rand (zie BattleFrontier_StadiumArena)
BattleCasino_EventScript_ToArena::
	setvar VAR_STADIUM_STATE, CASINO_STATE_ARENA
	warpsilent MAP_BATTLE_FRONTIER_STADIUM_ARENA, 9, 5
	waitstate
	end

BattleCasino_EventScript_Result::
	special Casino_Resolve
	goto_if_eq VAR_RESULT, 1, BattleCasino_EventScript_Won
	goto_if_eq VAR_RESULT, 2, BattleCasino_EventScript_Draw
	msgbox BattleCasino_Text_Lost, MSGBOX_DEFAULT
	goto BattleCasino_EventScript_Unlock
BattleCasino_EventScript_Won::
	playse SE_SHOP
	msgbox BattleCasino_Text_Won, MSGBOX_DEFAULT
	goto BattleCasino_EventScript_Unlock
BattleCasino_EventScript_Draw::
	msgbox BattleCasino_Text_Draw, MSGBOX_DEFAULT
BattleCasino_EventScript_Unlock::
	special Casino_CheckUnlock
	goto_if_eq VAR_RESULT, FALSE, BattleCasino_EventScript_End
	playfanfare MUS_LEVEL_UP
	msgbox BattleCasino_Text_Unlocked, MSGBOX_DEFAULT
	waitfanfare
BattleCasino_EventScript_End::
	releaseall
	end

@ In de arena (OnTransition/OnFrame van BattleFrontier_StadiumArena)
BattleCasino_EventScript_ArenaTransition::
	special Casino_SetArenaGfx
	copyvar VAR_TEMP_1, VAR_RESULT
	call_if_ne VAR_TEMP_1, STADIUM_DOUBLES, BattleFrontier_StadiumArena_EventScript_HideDoubles
	end

BattleCasino_EventScript_ArenaMatch::
	lockall
	setvar VAR_TEMP_0, 1
	applymovement LOCALID_PLAYER, BattleStadium_Movement_SetInvisible
	waitmovement 0
	delay 30
	playse SE_M_ENCORE2
	delay 30
	special Casino_StartArenaBattle
	waitstate
	setvar VAR_STADIUM_STATE, CASINO_STATE_RESULT
	warpsilent MAP_BATTLE_FRONTIER_BATTLE_CASINO, 12, 4
	waitstate
	end

BattleCasino_EventScript_Broke::
	msgbox BattleCasino_Text_Broke, MSGBOX_NPC
	end

BattleCasino_EventScript_Conspiracy::
	msgbox BattleCasino_Text_Conspiracy, MSGBOX_NPC
	end

BattleCasino_EventScript_Underdog::
	msgbox BattleCasino_Text_Underdog, MSGBOX_NPC
	end

BattleCasino_EventScript_OldMan::
	msgbox BattleCasino_Text_OldMan, MSGBOX_NPC
	end

BattleCasino_EventScript_Buffet::
	msgbox BattleCasino_Text_Buffet, MSGBOX_NPC
	end

BattleCasino_EventScript_Wurmple::
	msgbox BattleCasino_Text_Wurmple, MSGBOX_NPC
	end

BattleCasino_EventScript_Slots::
	msgbox BattleCasino_Text_Slots, MSGBOX_SIGN
	end

BattleCasino_EventScript_Roulette::
	msgbox BattleCasino_Text_Roulette, MSGBOX_SIGN
	end

BattleCasino_Text_Intro:
	.string "Welcome to the BATTLE CASINO!\p"
	.string "You bet BP on other people's battles.\n"
	.string "Like a sport, but with your savings.\p"
	.string "Watch the fight on our TV, or just ask\n"
	.string "for the result. The odds don't care.\p"
	.string "The more you bet, the more tables open:\n"
	.string "DOUBLES after 3 bets, the STADIUM\l"
	.string "after 6, STADIUM DOUBLES after 10,\l"
	.string "FACTORY RENTALS after 15 and\l"
	.string "SPIRE BOSSES after 20.\p"
	.string "No limits. No refunds. No feelings.$"

BattleCasino_Text_NoBet:
	.string "No bet? The house respects cowards.\n"
	.string "Cowards keep coming back.$"

BattleCasino_Text_NoBp:
	.string "You have no BP. I could lend you some,\n"
	.string "but I like you too much for that.$"

BattleCasino_Text_Won:
	.string "{STR_VAR_1} wins!\n"
	.string "You get {STR_VAR_2} BP. Balance: {STR_VAR_3} BP.\p"
	.string "Enjoy it. It's only borrowed.$"

BattleCasino_Text_Lost:
	.string "{STR_VAR_1} wins.\n"
	.string "Your {STR_VAR_2} BP now belong to the house.\p"
	.string "Balance: {STR_VAR_3} BP. Again?$"

BattleCasino_Text_Draw:
	.string "A draw! Nobody wins, so the house\n"
	.string "sulks and gives your {STR_VAR_2} BP back.$"

BattleCasino_Text_Unlocked:
	.string "Your losses have been noted. A new\n"
	.string "table is open: {STR_VAR_1}!$"

BattleCasino_Text_Broke:
	.string "I had four thousand BP this morning.\p"
	.string "Now I have a story. And the story\n"
	.string "isn't even that good.$"

BattleCasino_Text_Conspiracy:
	.string "The AI plays both sides. Both sides\n"
	.string "are the AI.\p"
	.string "So who is winning? ...The house.\n"
	.string "It's always the house.$"

BattleCasino_Text_Underdog:
	.string "I only bet on underdogs.\p"
	.string "Not for the odds. I just relate\n"
	.string "to them.$"

BattleCasino_Text_OldMan:
	.string "In my day we bet on MAGIKARP races.\p"
	.string "Nobody ever won. Nobody ever lost.\n"
	.string "We just sat there. Good times.$"

BattleCasino_Text_Buffet:
	.string "Free buffet for gamblers!\p"
	.string "The buffet is one ORAN BERRY.\n"
	.string "Please share.$"

BattleCasino_Text_Wurmple:
	.string "My husband bet our house on a\n"
	.string "WURMPLE.\p"
	.string "It evolved into the wrong one.\n"
	.string "We live in a CASCOON now.$"

BattleCasino_Text_Slots:
	.string "The slot machine has been retired.\n"
	.string "It now only accepts tears.$"

BattleCasino_Text_Roulette:
	.string "The roulette wheel was replaced by a\n"
	.string "TV. Progress.$"
