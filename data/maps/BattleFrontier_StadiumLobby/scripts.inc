@ Project Grounded: lobby van het Battle Stadium (toernooien à la Pokémon World Tournament).
@ Placeholders: de toernooi-engine wordt later aan deze scripts gehangen.
BattleFrontier_StadiumLobby_MapScripts::
	.byte 0

BattleFrontier_StadiumLobby_EventScript_SinglesDesk::
	msgbox BattleFrontier_StadiumLobby_Text_SinglesDesk, MSGBOX_NPC
	end

BattleFrontier_StadiumLobby_EventScript_DoublesDesk::
	msgbox BattleFrontier_StadiumLobby_Text_DoublesDesk, MSGBOX_NPC
	end

BattleFrontier_StadiumLobby_EventScript_Board::
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

BattleFrontier_StadiumLobby_Text_SinglesDesk:
	.string "Welcome to the BATTLE STADIUM!\n"
	.string "SINGLE BATTLE tournaments, right here.\p"
	.string "Registration opens soon. Our\n"
	.string "bracket printer is still warming up.$"

BattleFrontier_StadiumLobby_Text_DoublesDesk:
	.string "DOUBLE BATTLE tournaments!\n"
	.string "Twice the POKéMON, twice the paperwork.\p"
	.string "Please come back once the forms\n"
	.string "have been printed. In duplicate.$"

BattleFrontier_StadiumLobby_Text_Board:
	.string "TOURNAMENT BRACKET\p"
	.string "Round 1: TBA vs. TBA\n"
	.string "Round 2: Winner vs. also TBA\p"
	.string "Someone has drawn a tiny trophy\n"
	.string "in the corner. It looks smug.$"

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
