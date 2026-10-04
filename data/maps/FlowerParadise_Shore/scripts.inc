@ Project Grounded: Flower Paradise, het bloemeneiland van Shaymin (Bloom Ticket, veerboot vanuit Lilycove)
FlowerParadise_Shore_MapScripts::
	.byte 0

FlowerParadise_Shore_EventScript_Sailor::
	lock
	faceplayer
	msgbox FlowerParadise_Shore_Text_SailBack, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, FlowerParadise_Shore_EventScript_AsYouLike
	msgbox EventTicket_Text_SailHome, MSGBOX_DEFAULT
	closemessage
	applymovement VAR_LAST_TALKED, Common_Movement_WalkInPlaceFasterDown
	waitmovement 0
	delay 30
	hideobjectat LOCALID_FLOWER_PARADISE_SAILOR, MAP_FLOWER_PARADISE_SHORE
	setvar VAR_0x8004, LOCALID_FLOWER_PARADISE_SS_TIDAL
	call Common_EventScript_FerryDepartIsland
	warp MAP_LILYCOVE_CITY_HARBOR, 8, 11
	waitstate
	release
	end

FlowerParadise_Shore_EventScript_AsYouLike::
	msgbox EventTicket_Text_AsYouLike, MSGBOX_DEFAULT
	release
	end

FlowerParadise_Shore_EventScript_Sign::
	msgbox FlowerParadise_Shore_Text_Sign, MSGBOX_SIGN
	end

FlowerParadise_Shore_Text_SailBack:
	.string "Aye, mate. My nose has been running\n"
	.string "since we docked. It's trying to get back\l"
	.string "on the boat.\p"
	.string "Shall we sail back to LILYCOVE?$"

FlowerParadise_Shore_Text_Sign:
	.string "FLOWER PARADISE\p"
	.string "Please do not pick the GRACIDEA.\n"
	.string "Something in the meadow bites.\p"
	.string "It is very small. It knows SEED FLARE.$"
