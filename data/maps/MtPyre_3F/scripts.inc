MtPyre_3F_MapScripts::
	.byte 0

MtPyre_3F_EventScript_William::
	trainerbattle_single TRAINER_WILLIAM, MtPyre_3F_Text_WilliamIntro, MtPyre_3F_Text_WilliamDefeat
	msgbox MtPyre_3F_Text_WilliamPostBattle, MSGBOX_AUTOCLOSE
	end

MtPyre_3F_EventScript_Kayla::
	trainerbattle_single TRAINER_KAYLA, MtPyre_3F_Text_KaylaIntro, MtPyre_3F_Text_KaylaDefeat
	msgbox MtPyre_3F_Text_KaylaPostBattle, MSGBOX_AUTOCLOSE
	end

MtPyre_3F_EventScript_Gabrielle::
	trainerbattle_single TRAINER_GABRIELLE_1, MtPyre_3F_Text_GabrielleIntro, MtPyre_3F_Text_GabrielleDefeat, MtPyre_3F_EventScript_RegisterGabrielle
	specialvar VAR_RESULT, ShouldTryRematchBattle
	goto_if_eq VAR_RESULT, TRUE, MtPyre_3F_EventScript_RematchGabrielle
	msgbox MtPyre_3F_Text_GabriellePostBattle, MSGBOX_DEFAULT
	release
	end

MtPyre_3F_EventScript_RegisterGabrielle::
	special PlayerFaceTrainerAfterBattle
	waitmovement 0
	msgbox MtPyre_3F_Text_GabrielleRegister, MSGBOX_DEFAULT
	register_matchcall TRAINER_GABRIELLE_1
	release
	end

MtPyre_3F_EventScript_RematchGabrielle::
	trainerbattle_rematch TRAINER_GABRIELLE_1, MtPyre_3F_Text_GabrielleRematchIntro, MtPyre_3F_Text_GabrielleRematchDefeat
	msgbox MtPyre_3F_Text_GabriellePostRematch, MSGBOX_AUTOCLOSE
	end

MtPyre_3F_Text_WilliamIntro:
	.string "My astral body is on floor 6. My physical\n"
	.string "body is stuck here with you.$"

MtPyre_3F_Text_WilliamDefeat:
	.string "Bad karma… I drown in it.$"

MtPyre_3F_Text_WilliamPostBattle:
	.string "My astral body will be back soon. It's\n"
	.string "getting coffee.$"

MtPyre_3F_Text_KaylaIntro:
	.string "Ahahaha! I channel the COSMOS! The\n"
	.string "COSMOS says… you're mid.$"

MtPyre_3F_Text_KaylaDefeat:
	.string "The COSMOS lied to me…$"

MtPyre_3F_Text_KaylaPostBattle:
	.string "The COSMOS says I need more training.\p"
	.string "The COSMOS also says I'm mid. Rude.$"

MtPyre_3F_Text_GabrielleIntro:
	.string "Why have you come here?\p"
	.string "To cry? Everyone cries here.$"

MtPyre_3F_Text_GabrielleDefeat:
	.string "That was amazing! You're special.$"

MtPyre_3F_Text_GabriellePostBattle:
	.string "POKéMON no longer with us. POKéMON with\n"
	.string "you now.\p"
	.string "POKéMON you'll meet in the future…\p"
	.string "Cherish them all. Even the MAGIKARP.$"

MtPyre_3F_Text_GabrielleRegister:
	.string "I'd like to see your POKéMON grow…\p"
	.string "Let's register each other.$"

MtPyre_3F_Text_GabrielleRematchIntro:
	.string "Oh, it's you…\p"
	.string "Come to show me your grown POKéMON?$"

MtPyre_3F_Text_GabrielleRematchDefeat:
	.string "How amazing! You're special.$"

MtPyre_3F_Text_GabriellePostRematch:
	.string "Past, present, future POKéMON…\p"
	.string "You cherish them all. I can tell.\p"
	.string "Even the ones in the PC. Especially\n"
	.string "those.$"

