AbandonedShip_Corridors_1F_MapScripts::
	.byte 0

AbandonedShip_Corridors_1F_EventScript_Youngster::
	msgbox AbandonedShip_Corridors_1F_Text_IsntItFunHere, MSGBOX_NPC
	end

AbandonedShip_Corridors_1F_EventScript_Charlie::
	trainerbattle_single TRAINER_CHARLIE, AbandonedShip_Corridors_1F_Text_CharlieIntro, AbandonedShip_Corridors_1F_Text_CharlieDefeat
	msgbox AbandonedShip_Corridors_1F_Text_CharliePostBattle, MSGBOX_AUTOCLOSE
	end

AbandonedShip_Corridors_1F_Text_CharlieIntro:
	.string "What's so funny about having my inner\n"
	.string "tube aboard the ship? At least I'm not\l"
	.string "tubing in the river while drunk out of\l"
	.string "my mind...$"

AbandonedShip_Corridors_1F_Text_CharlieDefeat:
	.string "Whoa, you overwhelmed me! Let's tube\n"
	.string "out of here!$"

AbandonedShip_Corridors_1F_Text_CharliePostBattle:
	.string "It's not easy throwing POKé BALLS while\n"
	.string "hanging on to an inner tube and being\l"
	.string "drunk!$"

AbandonedShip_Corridors_1F_Text_IsntItFunHere:
	.string "Isn't it fun here? I get excited just\n"
	.string "being here! The risk of broken material\l"
	.string "opening wounds and infecting you were\l"
	.string "you stand. Life is short, better be\l"
	.string "idiotic from time to time!$"
