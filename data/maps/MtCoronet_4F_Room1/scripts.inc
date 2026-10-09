@ Project Grounded: MtCoronet_4F_Room1 (tools/grounded/maptools/coronet.py)
MtCoronet_4F_Room1_MapScripts::
	.byte 0

MtCoronet_4F_Room1_EventScript_Tick::
	trainerbattle_single TRAINER_CORONET_TICK, MtCoronet_4F_Room1_Text_TickIntro, MtCoronet_4F_Room1_Text_TickDefeat
	msgbox MtCoronet_4F_Room1_Text_TickPost, MSGBOX_AUTOCLOSE
	end

MtCoronet_4F_Room1_EventScript_Parallax::
	trainerbattle_single TRAINER_CORONET_PARALLAX, MtCoronet_4F_Room1_Text_ParallaxIntro, MtCoronet_4F_Room1_Text_ParallaxDefeat
	msgbox MtCoronet_4F_Room1_Text_ParallaxPost, MSGBOX_AUTOCLOSE
	end

@ ---------------------------------------------------------------- teksten (placeholders, Jordi herschrijft ze)
MtCoronet_4F_Room1_Text_TickIntro:
	.string "I am a projection of DIALGA.\n"
	.string "Technically I'm a trainer who hasn't\l"
	.string "been born yet.\p"
	.string "Don't worry about it. I don't.$"

MtCoronet_4F_Room1_Text_TickDefeat:
	.string "Ah. So that's how this ends. I always\n"
	.string "wondered.$"

MtCoronet_4F_Room1_Text_TickPost:
	.string "Time is a flat circle. Mostly it's just\n"
	.string "flat. Like my team, apparently.$"

MtCoronet_4F_Room1_Text_ParallaxIntro:
	.string "Hi! I'm a projection of PALKIA. From\n"
	.string "over there, I look closer than I am.\p"
	.string "From over here too, actually. Space is\n"
	.string "weird.$"

MtCoronet_4F_Room1_Text_ParallaxDefeat:
	.string "Objects in defeat are smaller than they\n"
	.string "appear.$"

MtCoronet_4F_Room1_Text_ParallaxPost:
	.string "PALKIA projects us so nobody walks up\n"
	.string "to Spear Pillar unannounced. We're the\l"
	.string "doorbell.$"
