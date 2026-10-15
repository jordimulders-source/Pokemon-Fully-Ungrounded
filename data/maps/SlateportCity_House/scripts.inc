SlateportCity_House_MapScripts::
	.byte 0

@ Project Grounded: eenmalige item-giveaway (testrun Jordi)
SlateportCity_House_EventScript_PokefanM::
	lock
	faceplayer
	msgbox SlateportCity_House_Text_NatureToDoWithStatGains, MSGBOX_DEFAULT
	goto_if_set FLAG_RECEIVED_SLATEPORT_HOUSE_GIFT, SlateportCity_House_EventScript_PokefanM_GiftDone
	msgbox SlateportCity_House_Text_TakeMuscleBand, MSGBOX_DEFAULT
	giveitem ITEM_MUSCLE_BAND
	goto_if_eq VAR_RESULT, FALSE, Common_EventScript_ShowBagIsFull
	setflag FLAG_RECEIVED_SLATEPORT_HOUSE_GIFT
SlateportCity_House_EventScript_PokefanM_GiftDone::
	release
	end

SlateportCity_House_EventScript_Girl::
	msgbox SlateportCity_House_Text_MustBeGoingToBattleTent, MSGBOX_NPC
	end

SlateportCity_House_Text_NatureToDoWithStatGains:
	.string "My POKéMON has a HASTY nature.\p"
	.string "It has higher SPEED than my others.\p"
	.string "It also bites. Hastily.$"

SlateportCity_House_Text_MustBeGoingToBattleTent:
	.string "You're a TRAINER?\p"
	.string "Then you must be here for the BATTLE\n"
	.string "TENT.\p"
	.string "Or the free Wi-Fi. Like everyone else.$"

SlateportCity_House_Text_TakeMuscleBand:
	.string "Here, a MUSCLE BAND. Physical moves\n"
	.string "hit harder with it.\p"
	.string "Mine wore it once. Now it bites\n"
	.string "harder. Still hastily.$"
