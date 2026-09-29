Route111_OldLadysRestStop_MapScripts::
	map_script MAP_SCRIPT_ON_TRANSITION, Route111_OldLadysRestStop_OnTransition
	.byte 0

Route111_OldLadysRestStop_OnTransition:
	setflag FLAG_LANDMARK_OLD_LADY_REST_SHOP
	end

Route111_OldLadysRestStop_EventScript_OldLady::
	lock
	faceplayer
	msgbox Route111_OldLadysRestStop_Text_RestUpHere, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, YES, Route111_OldLadysRestStop_EventScript_Rest
	goto_if_eq VAR_RESULT, NO, Route111_OldLadysRestStop_EventScript_DeclineRest
	end

Route111_OldLadysRestStop_EventScript_Rest::
	msgbox Route111_OldLadysRestStop_Text_TakeYourTimeRestUp, MSGBOX_DEFAULT
	closemessage
	call Common_EventScript_OutOfCenterPartyHeal
	msgbox Route111_OldLadysRestStop_Text_StillTiredTakeAnotherRest, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, YES, Route111_OldLadysRestStop_EventScript_Rest
	goto_if_eq VAR_RESULT, NO, Route111_OldLadysRestStop_EventScript_DeclineRest
	end

Route111_OldLadysRestStop_EventScript_DeclineRest::
	msgbox Route111_OldLadysRestStop_Text_DontNeedToBeShy, MSGBOX_DEFAULT
	release
	end

Route111_OldLadysRestStop_Text_RestUpHere:
	.string "Oh, dear, dear. Your POKéMON look\n"
	.string "exhausted!\p"
	.string "Rest here. You should do that. I insist.\p"
	.string "I insist very much.$"

Route111_OldLadysRestStop_Text_TakeYourTimeRestUp:
	.string "That's right. Take your time. Rest up.\p"
	.string "Stay forever, if you like.$"

Route111_OldLadysRestStop_Text_StillTiredTakeAnotherRest:
	.string "Oh, dear, dear. Still tired?\p"
	.string "Rest again. You should. You really\n"
	.string "should. Don't leave.$"

Route111_OldLadysRestStop_Text_DontNeedToBeShy:
	.string "Is that so? No need to be shy.\p"
	.string "The door is always open. It doesn't lock\n"
	.string "from the inside.$"

