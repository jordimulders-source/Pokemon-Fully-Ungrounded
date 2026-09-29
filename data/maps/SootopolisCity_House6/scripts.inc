SootopolisCity_House6_MapScripts::
	.byte 0

SootopolisCity_House6_EventScript_Woman::
	lock
	faceplayer
	goto_if_set FLAG_RECEIVED_WAILMER_DOLL, SootopolisCity_House6_EventScript_ReceivedWailmerDoll
	msgbox SootopolisCity_House6_Text_FirstGuestInWhileTakeDoll, MSGBOX_YESNO
	call_if_eq VAR_RESULT, NO, SootopolisCity_House6_EventScript_DeclineWailmerDoll
	msgbox SootopolisCity_House6_Text_TakeGoodCareOfIt, MSGBOX_DEFAULT
	givedecoration DECOR_WAILMER_DOLL
	goto_if_eq VAR_RESULT, FALSE, SootopolisCity_House6_EventScript_NoRoomForWailmerDoll
	setflag FLAG_RECEIVED_WAILMER_DOLL
	release
	end

SootopolisCity_House6_EventScript_DeclineWailmerDoll::
	msgbox SootopolisCity_House6_Text_DontWantThisDoll, MSGBOX_DEFAULT
	release
	end

SootopolisCity_House6_EventScript_ReceivedWailmerDoll::
	msgbox SootopolisCity_House6_Text_LovePlushDolls, MSGBOX_DEFAULT
	release
	end

SootopolisCity_House6_EventScript_NoRoomForWailmerDoll::
	bufferdecorationname STR_VAR_2, DECOR_WAILMER_DOLL
	msgbox gText_NoRoomLeftForAnother, MSGBOX_DEFAULT
	msgbox SootopolisCity_House6_Text_IllHoldItForYou, MSGBOX_DEFAULT
	release
	end

SootopolisCity_House6_Text_FirstGuestInWhileTakeDoll:
	.string "Hello! You're our first guest in years!\p"
	.string "You've made my day. Take this big\n"
	.string "WAILMER DOLL.\p"
	.string "It was taking up the whole bed.$"

SootopolisCity_House6_Text_TakeGoodCareOfIt:
	.string "Take good care of it! It snores.$"

SootopolisCity_House6_Text_IllHoldItForYou:
	.string "Oh, you want it, but not right now? Okay,\n"
	.string "I'll hold on to it.\p"
	.string "It can have the bed a little longer.$"

SootopolisCity_House6_Text_DontWantThisDoll:
	.string "Are you sure? You don't want this DOLL?\n"
	.string "It's huge!$"

SootopolisCity_House6_Text_LovePlushDolls:
	.string "I love plush DOLLS! I have no space left\n"
	.string "in my bed.$"

