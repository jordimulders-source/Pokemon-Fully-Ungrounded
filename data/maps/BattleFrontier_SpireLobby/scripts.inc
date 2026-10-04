@ Project Grounded: lobby van The Spire (roguelike-faciliteit). Teksten zijn placeholders.
BattleFrontier_SpireLobby_MapScripts::
	.byte 0

BattleFrontier_SpireLobby_EventScript_Attendant::
	lockall
	faceplayer
	special Spire_IsRunActive
	goto_if_eq VAR_RESULT, TRUE, BattleFrontier_SpireLobby_EventScript_Continue
	msgbox BattleFrontier_SpireLobby_Text_Attendant, MSGBOX_DEFAULT
	msgbox BattleFrontier_SpireLobby_Text_StartClimb, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, BattleFrontier_SpireLobby_EventScript_NotToday
BattleFrontier_SpireLobby_EventScript_Enter::
	special Spire_Enter
	waitstate
	releaseall
	end

BattleFrontier_SpireLobby_EventScript_Continue::
	msgbox BattleFrontier_SpireLobby_Text_Continue, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, YES, BattleFrontier_SpireLobby_EventScript_Enter
	msgbox BattleFrontier_SpireLobby_Text_GiveUp, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, BattleFrontier_SpireLobby_EventScript_NotToday
	special Spire_GiveUpFromField
	waitstate
	releaseall
	end

BattleFrontier_SpireLobby_EventScript_NotToday::
	msgbox BattleFrontier_SpireLobby_Text_NotToday, MSGBOX_DEFAULT
	releaseall
	end

BattleFrontier_SpireLobby_EventScript_Veteran::
	msgbox BattleFrontier_SpireLobby_Text_Veteran, MSGBOX_NPC
	end

BattleFrontier_SpireLobby_EventScript_RulesBoard::
	msgbox BattleFrontier_SpireLobby_Text_RulesBoard, MSGBOX_SIGN
	end

BattleFrontier_SpireLobby_Text_Attendant:
	.string "Welcome to THE SPIRE.\p"
	.string "It goes up. Nobody knows how far.\n"
	.string "Our surveyor is still climbing.\p"
	.string "You get borrowed POKéMON, a map\n"
	.string "that lies a little, and a very\l"
	.string "long way down.\p"
	.string "Leave whenever you like.\n"
	.string "The Spire will keep your spot.\l"
	.string "It is very patient. Up you go!$"

BattleFrontier_SpireLobby_Text_StartClimb:
	.string "Shall I open the stairs?$"

BattleFrontier_SpireLobby_Text_Continue:
	.string "Your climb is still waiting for you.\n"
	.string "Shall we pick up where you left off?$"

BattleFrontier_SpireLobby_Text_GiveUp:
	.string "Then shall I end this run?\n"
	.string "You keep the BP you earned.$"

BattleFrontier_SpireLobby_Text_NotToday:
	.string "Of course. The Spire is not going\n"
	.string "anywhere. Mostly upwards.$"

BattleFrontier_SpireLobby_Text_Veteran:
	.string "I made it to floor three once.\n"
	.string "A SKITTY took everything from me.\p"
	.string "They say there's a heart on top.\n"
	.string "Still beating. Still hungry.\p"
	.string "I say there's a gift shop.\n"
	.string "Nobody ever comes back to check.$"

BattleFrontier_SpireLobby_Text_RulesBoard:
	.string "THE SPIRE - HOUSE RULES\p"
	.string "1. Rental POKéMON only.\n"
	.string "2. What you find, you keep.\l"
	.string "   Until you lose.\p"
	.string "3. Please stop asking about the\n"
	.string "   elevator.$"
