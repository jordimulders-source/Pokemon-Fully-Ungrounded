SlateportCity_House_MapScripts::
	.byte 0

SlateportCity_House_EventScript_PokefanM::
	msgbox SlateportCity_House_Text_NatureToDoWithStatGains, MSGBOX_NPC
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

