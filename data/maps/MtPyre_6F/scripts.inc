MtPyre_6F_MapScripts::
	.byte 0

MtPyre_6F_EventScript_Valerie::
	trainerbattle_single TRAINER_VALERIE_1, MtPyre_6F_Text_ValerieIntro, MtPyre_6F_Text_ValerieDefeat, MtPyre_6F_EventScript_RegisterValerie
	specialvar VAR_RESULT, ShouldTryRematchBattle
	goto_if_eq VAR_RESULT, TRUE, MtPyre_6F_EventScript_RematchValerie
	msgbox MtPyre_6F_Text_ValeriePostBattle, MSGBOX_DEFAULT
	release
	end

MtPyre_6F_EventScript_RegisterValerie::
	special PlayerFaceTrainerAfterBattle
	waitmovement 0
	msgbox MtPyre_6F_Text_ValerieRegister, MSGBOX_DEFAULT
	register_matchcall TRAINER_VALERIE_1
	release
	end

MtPyre_6F_EventScript_RematchValerie::
	trainerbattle_rematch TRAINER_VALERIE_1, MtPyre_6F_Text_ValerieRematchIntro, MtPyre_6F_Text_ValerieRematchDefeat
	msgbox MtPyre_6F_Text_ValeriePostRematch, MSGBOX_AUTOCLOSE
	end

MtPyre_6F_EventScript_Cedric::
	trainerbattle_single TRAINER_CEDRIC, MtPyre_6F_Text_CedricIntro, MtPyre_6F_Text_CedricDefeat
	msgbox MtPyre_6F_Text_CedricPostBattle, MSGBOX_AUTOCLOSE
	end

MtPyre_6F_Text_ValerieIntro:
	.string "When I'm here… A curious power flows\n"
	.string "into me…\p"
	.string "Or it's the incense. Hard to say.$"

MtPyre_6F_Text_ValerieDefeat:
	.string "The power is ebbing away… Or the\n"
	.string "incense ran out.$"

MtPyre_6F_Text_ValeriePostBattle:
	.string "Perhaps the power comes from the\n"
	.string "spirits of POKéMON sleeping here…\p"
	.string "They snore, you know.$"

MtPyre_6F_Text_ValerieRegister:
	.string "Fufufu… I lost, but I have a little\n"
	.string "ability…\p"
	.string "Without touching your POKéNAV… Hiyah!\p"
	.string "…Registered. Don't ask how.$"

MtPyre_6F_Text_ValerieRematchIntro:
	.string "Behind you… What is it…$"

MtPyre_6F_Text_ValerieRematchDefeat:
	.string "Something faded away… Probably my\n"
	.string "dignity.$"

MtPyre_6F_Text_ValeriePostRematch:
	.string "The POKéMON at rest here… Sometimes,\n"
	.string "they play…\p"
	.string "Hide and seek. They always win.$"

MtPyre_6F_Text_CedricIntro:
	.string "Lost? Fear not. I channel the spirits of\n"
	.string "this mountain. They say turn left.$"

MtPyre_6F_Text_CedricDefeat:
	.string "The spirits said left. The spirits were\n"
	.string "wrong.$"

MtPyre_6F_Text_CedricPostBattle:
	.string "My feelings are 60% accurate. On a good\n"
	.string "day.$"

