@ Project Grounded: Battle Stadium (Pokémon World Tournament, zie STADIUM_DESIGN.md). Teksten zijn placeholders.
@ Aanroepen vanuit de balies in de lobby (of het debugmenu): goto BattleStadium_EventScript_Singles / _Doubles.

BattleStadium_EventScript_Singles::
	lockall
	msgbox BattleStadium_Text_SinglesWelcome, MSGBOX_YESNO
	goto_if_ne VAR_RESULT, YES, BattleStadium_EventScript_Bye
	setvar VAR_0x8004, STADIUM_SINGLES
	goto BattleStadium_EventScript_ChooseTeam

BattleStadium_EventScript_Doubles::
	lockall
	msgbox BattleStadium_Text_DoublesWelcome, MSGBOX_YESNO
	goto_if_ne VAR_RESULT, YES, BattleStadium_EventScript_Bye
	msgbox BattleStadium_Text_ChooseCompanion, MSGBOX_DEFAULT
	fadescreen FADE_TO_BLACK
	special Stadium_ChooseCompanion
	waitstate
	goto_if_eq VAR_RESULT, FALSE, BattleStadium_EventScript_Bye
	setvar VAR_0x8004, STADIUM_DOUBLES
BattleStadium_EventScript_ChooseTeam::
	special Stadium_PrepareChooseParty
	msgbox BattleStadium_Text_ChooseTeam, MSGBOX_DEFAULT
	fadescreen FADE_TO_BLACK
	callnative RemoveFollowingPokemon
	special ChoosePartyForBattleFrontier
	waitstate
	goto_if_eq VAR_RESULT, FALSE, BattleStadium_EventScript_Bye
	special Stadium_StartTournament
BattleStadium_EventScript_ToArena::
	special Stadium_ShowNextMatch
	waitstate
	warpsilent MAP_BATTLE_FRONTIER_STADIUM_ARENA, 9, 5
	waitstate
	end

@ In de arena (OnFrame): opkomst, gevecht, uitslag
BattleStadium_EventScript_ArenaMatch::
	lockall
	setvar VAR_TEMP_0, 1
	applymovement LOCALID_PLAYER, BattleStadium_Movement_SetInvisible
	waitmovement 0
	special Stadium_GetMatchNames
	applymovement LOCALID_STADIUM_ANNOUNCER, Common_Movement_WalkInPlaceDown
	waitmovement 0
	msgbox BattleStadium_Text_Announce, MSGBOX_DEFAULT
	closemessage
	showobjectat LOCALID_STADIUM_PLAYER, MAP_BATTLE_FRONTIER_STADIUM_ARENA
	applymovement LOCALID_STADIUM_PLAYER, BattleStadium_Movement_PlayerEnter
	goto_if_ne VAR_TEMP_1, STADIUM_DOUBLES, BattleStadium_EventScript_ArenaCrowd
	clearflag FLAG_TEMP_2
	addobject LOCALID_STADIUM_PARTNER
	applymovement LOCALID_STADIUM_PARTNER, BattleStadium_Movement_PartnerEnter
BattleStadium_EventScript_ArenaCrowd::
	waitmovement 0
	playse SE_M_ENCORE2
	delay 30
	msgbox BattleStadium_Text_Versus, MSGBOX_DEFAULT
	closemessage
	applymovement LOCALID_STADIUM_PLAYER, BattleStadium_Movement_StepRight
	applymovement LOCALID_STADIUM_OPPONENT, BattleStadium_Movement_StepLeft
	waitmovement 0
	special Stadium_StartMatch
	waitstate
	applymovement LOCALID_PLAYER, BattleStadium_Movement_SetInvisible
	waitmovement 0
	special Stadium_AfterMatch
	copyvar VAR_TEMP_2, VAR_RESULT
	special Stadium_HasNewUnlocks
	goto_if_eq VAR_RESULT, FALSE, BattleStadium_EventScript_AfterUnlocks
	special Stadium_ShowUnlocks
	waitstate
BattleStadium_EventScript_AfterUnlocks::
	goto_if_eq VAR_TEMP_2, 1, BattleStadium_EventScript_ToArena
	goto_if_eq VAR_TEMP_2, 2, BattleStadium_EventScript_Champion
	setvar VAR_STADIUM_STATE, 3
	goto BattleStadium_EventScript_BackToLobby

BattleStadium_EventScript_Champion::
	special Stadium_ShowNextMatch
	waitstate
	setvar VAR_STADIUM_STATE, 2
BattleStadium_EventScript_BackToLobby::
	goto_if_eq VAR_TEMP_1, STADIUM_DOUBLES, BattleStadium_EventScript_BackToLobbyDoubles
	warpsilent MAP_BATTLE_FRONTIER_STADIUM_LOBBY, 5, 11
	waitstate
	end
BattleStadium_EventScript_BackToLobbyDoubles::
	warpsilent MAP_BATTLE_FRONTIER_STADIUM_LOBBY, 17, 11
	waitstate
	end

@ In de lobby (OnFrame): het toernooi afronden (team terug, BP)
BattleStadium_EventScript_LobbyResult::
	lockall
	special Stadium_EndTournament
	goto_if_eq VAR_STADIUM_STATE, 2, BattleStadium_EventScript_LobbyChampion
	setvar VAR_STADIUM_STATE, 0
	msgbox BattleStadium_Text_Lost, MSGBOX_DEFAULT
	releaseall
	end
BattleStadium_EventScript_LobbyChampion::
	setvar VAR_STADIUM_STATE, 0
	playfanfare MUS_OBTAIN_SYMBOL
	msgbox BattleStadium_Text_Champion, MSGBOX_DEFAULT
	waitfanfare
	releaseall
	end

BattleStadium_Movement_SetInvisible:
	set_invisible
	step_end

BattleStadium_Movement_PlayerEnter:
	set_visible
	delay_16
	walk_up
	walk_up
	walk_up
	walk_right
	step_end

BattleStadium_Movement_PartnerEnter:
	delay_16
	delay_16
	walk_up
	walk_up
	walk_up
	walk_up
	walk_right
	face_right
	step_end

BattleStadium_Movement_StepRight:
	walk_right
	step_end

BattleStadium_Movement_StepLeft:
	walk_left
	step_end

BattleStadium_EventScript_Bye::
	msgbox BattleStadium_Text_Bye, MSGBOX_DEFAULT
	releaseall
	end

BattleStadium_Text_SinglesWelcome:
	.string "Welcome to the BATTLE STADIUM!\p"
	.string "SINGLES: four POKéMON, thirty-two\n"
	.string "trainers, one trophy. Everyone is\l"
	.string "level 50, including your ego.\p"
	.string "Shall I sign you up?$"

BattleStadium_Text_DoublesWelcome:
	.string "Welcome to the DOUBLES desk!\p"
	.string "You bring three POKéMON, your\n"
	.string "partner brings three. Sixteen\l"
	.string "teams, one trophy. Level 50.\p"
	.string "Shall I sign you up?$"

BattleStadium_Text_ChooseCompanion:
	.string "First, choose your partner.$"

BattleStadium_Text_ChooseTeam:
	.string "Now choose your POKéMON.\n"
	.string "They will all fight at level 50.$"

BattleStadium_Text_Announce:
	.string "Ladies and gentlemen, welcome to the\n"
	.string "{STR_VAR_3} of the BATTLE STADIUM!\p"
	.string "Entering the arena…\n"
	.string "{STR_VAR_1}!$"

BattleStadium_Text_Versus:
	.string "{STR_VAR_1}\n"
	.string "versus {STR_VAR_2}!\p"
	.string "Let the battle begin!$"

BattleStadium_Text_Lost:
	.string "That's the end of your run.\n"
	.string "The crowd was entertained!\p"
	.string "You earned {STR_VAR_1} BP.$"

BattleStadium_Text_Champion:
	.string "We have a CHAMPION!\n"
	.string "The trophy is yours! Briefly.\p"
	.string "You earned {STR_VAR_1} BP.$"

BattleStadium_Text_Bye:
	.string "Come back when you're ready.\n"
	.string "The bracket waits for no one,\l"
	.string "but it will wait for you.$"
