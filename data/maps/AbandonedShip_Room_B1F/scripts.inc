AbandonedShip_Room_B1F_MapScripts::
	.byte 0


@ Project Grounded: Spiritomb verstopt in de prullenbak. Komt terug tot hij gevangen is.
AbandonedShip_Room_B1F_EventScript_TrashCan::
	goto_if_set FLAG_CAUGHT_SHIP_SPIRITOMB, EventScript_EmptyTrashCan
	lock
	msgbox AbandonedShip_Room_B1F_Text_TrashCanStirs, MSGBOX_DEFAULT
	closemessage
	playmoncry SPECIES_SPIRITOMB, CRY_MODE_ENCOUNTER
	delay 40
	waitmoncry
	setwildbattle SPECIES_SPIRITOMB, 45
	dowildbattle
	specialvar VAR_RESULT, GetBattleOutcome
	goto_if_ne VAR_RESULT, B_OUTCOME_CAUGHT, AbandonedShip_Room_B1F_EventScript_TrashCanEnd
	setflag FLAG_CAUGHT_SHIP_SPIRITOMB
AbandonedShip_Room_B1F_EventScript_TrashCanEnd::
	release
	end

AbandonedShip_Room_B1F_Text_TrashCanStirs:
	.string "Something inside the trash can\n"
	.string "is whispering…$"
