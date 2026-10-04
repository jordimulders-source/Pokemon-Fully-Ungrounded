@ Project Grounded: lavabuis onder Jagged Pass (tools/grounded/maptools/chimney_ext.py).
@ Ingang A: klif vlak onder Mt. Chimney (Rock Smash-rots), uitgang B: plateau halverwege Jagged Pass.
@ Drie magmapoelen, drie trainers; de nis met TM Fire Blast en Heat Rock zit achter een Strength-blok.
JaggedPass_LavaTube_MapScripts::
	.byte 0

JaggedPass_LavaTube_EventScript_Hank::
	trainerbattle_single TRAINER_LAVA_TUBE_HANK, JaggedPass_LavaTube_Text_HankIntro, JaggedPass_LavaTube_Text_HankDefeat
	msgbox JaggedPass_LavaTube_Text_HankPostBattle, MSGBOX_AUTOCLOSE
	end

JaggedPass_LavaTube_EventScript_Ignace::
	trainerbattle_single TRAINER_LAVA_TUBE_IGNACE, JaggedPass_LavaTube_Text_IgnaceIntro, JaggedPass_LavaTube_Text_IgnaceDefeat
	msgbox JaggedPass_LavaTube_Text_IgnacePostBattle, MSGBOX_AUTOCLOSE
	end

JaggedPass_LavaTube_EventScript_Daisy::
	trainerbattle_single TRAINER_LAVA_TUBE_DAISY, JaggedPass_LavaTube_Text_DaisyIntro, JaggedPass_LavaTube_Text_DaisyDefeat
	msgbox JaggedPass_LavaTube_Text_DaisyPostBattle, MSGBOX_AUTOCLOSE
	end

JaggedPass_LavaTube_EventScript_Pillar::
	msgbox JaggedPass_LavaTube_Text_Pillar, MSGBOX_SIGN
	end

JaggedPass_LavaTube_Text_HankIntro:
	.string "This tunnel was dug by lava.\n"
	.string "I respect that. No permits,\l"
	.string "no union. Just vibes and\p"
	.string "1,200 degrees.$"

JaggedPass_LavaTube_Text_HankDefeat:
	.string "My boots melted three tunnels ago.\n"
	.string "I've been walking on pride.$"

JaggedPass_LavaTube_Text_HankPostBattle:
	.string "Fun fact: a lava tube is a volcano's\n"
	.string "intestine.\p"
	.string "You're standing in it. Enjoy.$"

JaggedPass_LavaTube_Text_IgnaceIntro:
	.string "I came down here to feel something.\n"
	.string "Mostly I feel second-degree burns.$"

JaggedPass_LavaTube_Text_IgnaceDefeat:
	.string "Extinguished. Like my dreams,\n"
	.string "and my eyebrows.$"

JaggedPass_LavaTube_Text_IgnacePostBattle:
	.string "Kindlers don't fear fire.\n"
	.string "We fear the electricity bill.$"

JaggedPass_LavaTube_Text_DaisyIntro:
	.string "Oh thank god, a human!\n"
	.string "I took a “shortcut” to the picnic.\p"
	.string "That was… what day is it?\n"
	.string "Battle me so I feel normal again!$"

JaggedPass_LavaTube_Text_DaisyDefeat:
	.string "My sandwiches turned into charcoal.\n"
	.string "I ate them anyway.$"

JaggedPass_LavaTube_Text_DaisyPostBattle:
	.string "If you see my picnic blanket, it's\n"
	.string "the one that's on fire. Tell it I'm\l"
	.string "sorry.$"

JaggedPass_LavaTube_Text_Pillar:
	.string "Someone scratched into the rock:\p"
	.string "“DAY 4. THE FLOOR IS LAVA.\n"
	.string "THIS IS NO LONGER A GAME.”$"
