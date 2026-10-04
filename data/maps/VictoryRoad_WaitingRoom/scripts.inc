@ Project Grounded: de wachtkamer van de Elite Four (Victory Road 1F, achter een Rock Smash-rots).
@ Ace Trainer-gauntlet: drie Cooltrainers in de rij, gevonden voorwerpen aan het eind.
VictoryRoad_WaitingRoom_MapScripts::
	.byte 0

VictoryRoad_WaitingRoom_EventScript_Brent::
	trainerbattle_single TRAINER_VR_BRENT, VictoryRoad_WaitingRoom_Text_BrentIntro, VictoryRoad_WaitingRoom_Text_BrentDefeat
	msgbox VictoryRoad_WaitingRoom_Text_BrentPostBattle, MSGBOX_AUTOCLOSE
	end

VictoryRoad_WaitingRoom_EventScript_Nadia::
	trainerbattle_single TRAINER_VR_NADIA, VictoryRoad_WaitingRoom_Text_NadiaIntro, VictoryRoad_WaitingRoom_Text_NadiaDefeat
	msgbox VictoryRoad_WaitingRoom_Text_NadiaPostBattle, MSGBOX_AUTOCLOSE
	end

VictoryRoad_WaitingRoom_EventScript_Oskar::
	trainerbattle_single TRAINER_VR_OSKAR, VictoryRoad_WaitingRoom_Text_OskarIntro, VictoryRoad_WaitingRoom_Text_OskarDefeat
	msgbox VictoryRoad_WaitingRoom_Text_OskarPostBattle, MSGBOX_AUTOCLOSE
	end

VictoryRoad_WaitingRoom_EventScript_TicketSign::
	msgbox VictoryRoad_WaitingRoom_Text_TicketSign, MSGBOX_SIGN
	end

VictoryRoad_WaitingRoom_EventScript_LostAndFound::
	msgbox VictoryRoad_WaitingRoom_Text_LostAndFound, MSGBOX_SIGN
	end

VictoryRoad_WaitingRoom_Text_TicketSign:
	.string "A ticket dispenser, carved into\n"
	.string "the rock.\p"
	.string "ELITE FOUR WAITING ROOM\n"
	.string "NOW SERVING: No. 12\p"
	.string "YOUR NUMBER: No. 4,813\n"
	.string "Estimated wait: 31 years.\p"
	.string "Your patience is our business\n"
	.string "model.$"

VictoryRoad_WaitingRoom_Text_LostAndFound:
	.string "LOST & FOUND\p"
	.string "Items left behind by trainers who\n"
	.string "stopped waiting. One way or another.\p"
	.string "Finders keepers. Please do not ask\n"
	.string "what happened to the owners.$"

VictoryRoad_WaitingRoom_Text_BrentIntro:
	.string "Hey. HEY. There's a LINE.\p"
	.string "I've been in this line since my\n"
	.string "MAMOSWINE was a SWINUB.\p"
	.string "You want to cut? Then you go\n"
	.string "through the line. Literally.$"

VictoryRoad_WaitingRoom_Text_BrentDefeat:
	.string "Fine. Cut. My ticket expired\n"
	.string "in 2014 anyway.$"

VictoryRoad_WaitingRoom_Text_BrentPostBattle:
	.string "They called number 13 once.\n"
	.string "Nobody answered.\p"
	.string "We don't talk about 13.$"

VictoryRoad_WaitingRoom_Text_NadiaIntro:
	.string "Number 4,812. That's me.\n"
	.string "You're BEHIND me. Legally.\p"
	.string "I brought snacks for the first\n"
	.string "decade. Now I bring POKéMON.$"

VictoryRoad_WaitingRoom_Text_NadiaDefeat:
	.string "Queue etiquette is dead.\n"
	.string "Like number 13.$"

VictoryRoad_WaitingRoom_Text_NadiaPostBattle:
	.string "My grandmother waited here too.\n"
	.string "She was number 9.\p"
	.string "She got called while she was in\n"
	.string "the bathroom. Never recovered.$"

VictoryRoad_WaitingRoom_Text_OskarIntro:
	.string "I'm at the front of the line.\n"
	.string "The VERY front.\p"
	.string "I've been “next” for eleven years.\n"
	.string "Nobody gets to be next-er than me.$"

VictoryRoad_WaitingRoom_Text_OskarDefeat:
	.string "So this is what getting called up\n"
	.string "feels like. It mostly hurts.$"

VictoryRoad_WaitingRoom_Text_OskarPostBattle:
	.string "Take the stuff from the lost and\n"
	.string "found. Those people won't need it.\p"
	.string "They got tired of waiting.\n"
	.string "Permanently.$"
