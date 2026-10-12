AbandonedShip_Rooms_B1F_MapScripts::
	map_script MAP_SCRIPT_ON_RESUME, AbandonedShip_Rooms_B1F_OnResume
	.byte 0

AbandonedShip_Rooms_B1F_OnResume:
	setdivewarp MAP_ABANDONED_SHIP_UNDERWATER2, 17, 4
	end

AbandonedShip_Rooms_B1F_EventScript_FatMan::
	msgbox AbandonedShip_Rooms_B1F_Text_GettingQueasy, MSGBOX_NPC
	end

AbandonedShip_Rooms_B1F_Text_GettingQueasy:
	.string "Urrrrppp…\p"
	.string "I'm getting queasy just being aboard\n"
	.string "this ship…\p"
	.string "It's not even moving, but… I've barfed\n"
	.string "all over the place. For days now, it\l"
	.string "smells so rotten...BUUURRRRP$"


@ Project Grounded: eenmalige Muk in de prullenbak naast de zeezieke man.
AbandonedShip_Rooms_B1F_EventScript_TrashCan::
	goto_if_set FLAG_SHIP_MUK_ENCOUNTERED, EventScript_EmptyTrashCan
	lock
	msgbox AbandonedShip_Rooms_B1F_Text_TrashCanBubbles, MSGBOX_DEFAULT
	closemessage
	setflag FLAG_SHIP_MUK_ENCOUNTERED
	playmoncry SPECIES_MUK, CRY_MODE_ENCOUNTER
	delay 40
	waitmoncry
	setwildbattle SPECIES_MUK, 49
	dowildbattle
	release
	end

AbandonedShip_Rooms_B1F_Text_TrashCanBubbles:
	.string "The trash can is bubbling…$"
