LilycoveCity_CoveLilyMotel_1F_MapScripts::
	.byte 0

LilycoveCity_CoveLilyMotel_1F_EventScript_MotelOwner::
	lockall
	goto_if_set FLAG_SYS_GAME_CLEAR, LilycoveCity_CoveLilyMotel_1F_EventScript_GameClear
	goto_if_set FLAG_BADGE07_GET, LilycoveCity_CoveLilyMotel_1F_EventScript_AquaHideoutBusted
	msgbox LilycoveCity_CoveLilyMotel_1F_Text_GuestsDoubledByMascot, MSGBOX_DEFAULT
	applymovement LOCALID_MOTEL_OWNER, Common_Movement_FacePlayer
	waitmovement 0
	msgbox LilycoveCity_CoveLilyMotel_1F_Text_NoGuestsWithTeamAqua, MSGBOX_DEFAULT
	closemessage
	applymovement LOCALID_MOTEL_OWNER, Common_Movement_FaceOriginalDirection
	waitmovement 0
	releaseall
	end

LilycoveCity_CoveLilyMotel_1F_EventScript_AquaHideoutBusted::
	msgbox LilycoveCity_CoveLilyMotel_1F_Text_MonFoundLostItem, MSGBOX_DEFAULT
	applymovement LOCALID_MOTEL_OWNER, Common_Movement_FacePlayer
	waitmovement 0
	msgbox LilycoveCity_CoveLilyMotel_1F_Text_HeardAquaHideoutBusted, MSGBOX_DEFAULT
	closemessage
	applymovement LOCALID_MOTEL_OWNER, Common_Movement_FaceOriginalDirection
	waitmovement 0
	releaseall
	end

LilycoveCity_CoveLilyMotel_1F_EventScript_GameClear::
	msgbox LilycoveCity_CoveLilyMotel_1F_Text_HouseSittingMonCaughtBurglar, MSGBOX_DEFAULT
	applymovement LOCALID_MOTEL_OWNER, Common_Movement_FacePlayer
	waitmovement 0
	msgbox LilycoveCity_CoveLilyMotel_1F_Text_BetterGetWorkingOnGuestsDinner, MSGBOX_DEFAULT
	closemessage
	applymovement LOCALID_MOTEL_OWNER, Common_Movement_FaceOriginalDirection
	waitmovement 0
	releaseall
	end

LilycoveCity_CoveLilyMotel_1F_EventScript_BlockingTV::
	lockall
	playse SE_PIN
	applymovement LOCALID_MOTEL_OWNER, Common_Movement_ExclamationMark
	waitmovement 0
	applymovement LOCALID_MOTEL_OWNER, Common_Movement_Delay48
	waitmovement 0
	applymovement LOCALID_PLAYER, Common_Movement_WalkInPlaceFasterDown
	waitmovement 0
	msgbox LilycoveCity_CoveLilyMotel_1F_Text_CantSeeTheTV, MSGBOX_DEFAULT
	closemessage
	applymovement LOCALID_PLAYER, LilycoveCity_CoveLilyMotel_1F_Movement_PlayerPushFromTV
	applymovement LOCALID_MOTEL_OWNER, LilycoveCity_CoveLilyMotel_1F_Movement_OwnerPushPlayer
	waitmovement 0
	applymovement LOCALID_MOTEL_OWNER, LilycoveCity_CoveLilyMotel_1F_Movement_OwnerReturn
	waitmovement 0
	release
	end

LilycoveCity_CoveLilyMotel_1F_Movement_PlayerPushFromTV:
	face_right
	lock_facing_direction
	walk_left
	unlock_facing_direction
	step_end

LilycoveCity_CoveLilyMotel_1F_Movement_OwnerPushPlayer:
	walk_up
	step_end

LilycoveCity_CoveLilyMotel_1F_Movement_OwnerReturn:
	face_down
	walk_down
	face_up
	step_end

LilycoveCity_CoveLilyMotel_1F_Text_GuestsDoubledByMascot:
	.string "They doubled their guests with a JYNX\n"
	.string "mascot?\p"
	.string "Maybe I need a mascot too.\p"
	.string "Or a working toilet. One of the two.$"

LilycoveCity_CoveLilyMotel_1F_Text_NoGuestsWithTeamAqua:
	.string "Oh, sorry! I was watching TV!\p"
	.string "Since TEAM AQUA came, no tourists.\p"
	.string "Just guys ordering sparkling water. At\n"
	.string "a motel.$"

LilycoveCity_CoveLilyMotel_1F_Text_CantSeeTheTV:
	.string "Hey, down in front! I can't see the TV!$"

LilycoveCity_CoveLilyMotel_1F_Text_MonFoundLostItem:
	.string "Amazing! A POKéMON found someone's\n"
	.string "lost item?\p"
	.string "If we had a POKéMON like that…\p"
	.string "We could find the TV remote.$"

LilycoveCity_CoveLilyMotel_1F_Text_HeardAquaHideoutBusted:
	.string "Oh, sorry! I was watching TV!\p"
	.string "Someone busted the TEAM AQUA HIDEOUT.\p"
	.string "So we got a big booking. A company\n"
	.string "called… GAME something…$"

LilycoveCity_CoveLilyMotel_1F_Text_HouseSittingMonCaughtBurglar:
	.string "Amazing! A house-sitting POKéMON\n"
	.string "caught a burglar?\p"
	.string "With a POKéMON guard, our guests would\n"
	.string "be safer.\p"
	.string "Right now we have a very old ZIGZAGOON.$"

LilycoveCity_CoveLilyMotel_1F_Text_BetterGetWorkingOnGuestsDinner:
	.string "Oh, sorry! I was watching TV.\p"
	.string "A big group checked in. GAME FREAK, they\n"
	.string "said.\p"
	.string "They make games. They asked for 30\n"
	.string "years of the same formula. For dinner.$"


@ Project Grounded: SickBlik chillt in het motel (Jordi, 9 okt)
LilycoveCity_CoveLilyMotel_1F_EventScript_SickBlik::
	lock
	faceplayer
	goto_if_defeated TRAINER_SICKBLIK_MOTEL, LilycoveCity_CoveLilyMotel_1F_EventScript_SickBlikAfter
	msgbox LilycoveCity_CoveLilyMotel_1F_Text_SickBlikIntro, MSGBOX_DEFAULT
	msgbox LilycoveCity_CoveLilyMotel_1F_Text_SickBlikAsk, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, LilycoveCity_CoveLilyMotel_1F_EventScript_SickBlikNo
	trainerbattle_no_intro TRAINER_SICKBLIK_MOTEL, LilycoveCity_CoveLilyMotel_1F_Text_SickBlikDefeat
	msgbox LilycoveCity_CoveLilyMotel_1F_Text_SickBlikAfter, MSGBOX_DEFAULT
	release
	end

LilycoveCity_CoveLilyMotel_1F_EventScript_SickBlikNo:
	msgbox LilycoveCity_CoveLilyMotel_1F_Text_SickBlikNo, MSGBOX_DEFAULT
	release
	end

LilycoveCity_CoveLilyMotel_1F_EventScript_SickBlikAfter:
	msgbox LilycoveCity_CoveLilyMotel_1F_Text_SickBlikAfter, MSGBOX_DEFAULT
	release
	end

LilycoveCity_CoveLilyMotel_1F_Text_SickBlikIntro:
	.string "SICKBLIK: I am travelling the globe!\p"
	.string "Well, the globe is kinda relative,\n"
	.string "since it's just a map. Either way.\p"
	.string "This hotel is way worse than its\n"
	.string "rating described. The shower\l"
	.string "doesn't even work well.\p"
	.string "At least the guests are funny.\n"
	.string "There was this guy talking to his\l"
	.string "EVOLUTION STONE. He doesn't even\l"
	.string "have a POKéMON!$"

LilycoveCity_CoveLilyMotel_1F_Text_SickBlikAsk:
	.string "Well, do you want to battle the\n"
	.string "literal enhancer of this world?\p"
	.string "I mean, creator is too much honor.$"

LilycoveCity_CoveLilyMotel_1F_Text_SickBlikNo:
	.string "Fair. I'll be here. The shower\n"
	.string "isn't going anywhere either.$"

LilycoveCity_CoveLilyMotel_1F_Text_SickBlikDefeat:
	.string "Okay, okay. Writing that down\n"
	.string "as a balancing issue.$"

LilycoveCity_CoveLilyMotel_1F_Text_SickBlikAfter:
	.string "SICKBLIK: Now if you'll excuse me,\n"
	.string "I have a one-star review to write.$"
