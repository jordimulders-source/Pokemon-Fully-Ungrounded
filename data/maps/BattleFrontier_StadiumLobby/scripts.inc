@ Project Grounded: lobby van het Battle Stadium (toernooien à la Pokémon World Tournament).
@ De balies starten het toernooi (data/scripts/battle_stadium.inc). Teksten zijn placeholders.
BattleFrontier_StadiumLobby_MapScripts::
	.byte 0

BattleFrontier_StadiumLobby_EventScript_SinglesDesk::
	goto BattleStadium_EventScript_Singles

BattleFrontier_StadiumLobby_EventScript_DoublesDesk::
	goto BattleStadium_EventScript_Doubles

BattleFrontier_StadiumLobby_EventScript_Board::
	special Stadium_GetRecord
	msgbox BattleFrontier_StadiumLobby_Text_Board, MSGBOX_SIGN
	end

BattleFrontier_StadiumLobby_EventScript_Fan::
	msgbox BattleFrontier_StadiumLobby_Text_Fan, MSGBOX_NPC
	end

BattleFrontier_StadiumLobby_EventScript_Scout::
	msgbox BattleFrontier_StadiumLobby_Text_Scout, MSGBOX_NPC
	end

BattleFrontier_StadiumLobby_EventScript_Snacks::
	msgbox BattleFrontier_StadiumLobby_Text_Snacks, MSGBOX_NPC
	end

BattleFrontier_StadiumLobby_Text_Board:
	.string "BATTLE STADIUM - YOUR RECORD\p"
	.string "Singles trophies: {STR_VAR_1}\n"
	.string "Doubles trophies: {STR_VAR_2}\p"
	.string "Matches won: {STR_VAR_3}\n"
	.string "Someone drew a tiny trophy next to\l"
	.string "your name. It looks smug.$"

BattleFrontier_StadiumLobby_Text_Fan:
	.string "I bought a season ticket before they\n"
	.string "built the stadium. Before the island,\l"
	.string "actually. I just had a feeling.$"

BattleFrontier_StadiumLobby_Text_Scout:
	.string "I scout trainers for the big leagues.\p"
	.string "So far I've scouted the snack bar,\n"
	.string "the restrooms and a very nice bench.$"

BattleFrontier_StadiumLobby_Text_Snacks:
	.string "They don't sell snacks in here.\n"
	.string "I'm just holding this tray for morale.$"
