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
BattleStadium_EventScript_NextRound::
	fadescreen FADE_TO_BLACK
	special Stadium_ShowNextMatch
	waitstate
	special Stadium_StartMatch
	waitstate
	special Stadium_AfterMatch
	copyvar VAR_TEMP_0, VAR_RESULT
	special Stadium_HasNewUnlocks
	goto_if_eq VAR_RESULT, FALSE, BattleStadium_EventScript_AfterUnlocks
	special Stadium_ShowUnlocks
	waitstate
BattleStadium_EventScript_AfterUnlocks::
	goto_if_eq VAR_TEMP_0, 1, BattleStadium_EventScript_NextRound
	goto_if_eq VAR_TEMP_0, 2, BattleStadium_EventScript_Champion
	special Stadium_EndTournament
	msgbox BattleStadium_Text_Lost, MSGBOX_DEFAULT
	releaseall
	end

BattleStadium_EventScript_Champion::
	fadescreen FADE_TO_BLACK
	special Stadium_ShowNextMatch
	waitstate
	special Stadium_EndTournament
	playfanfare MUS_OBTAIN_SYMBOL
	msgbox BattleStadium_Text_Champion, MSGBOX_DEFAULT
	waitfanfare
	releaseall
	end

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
