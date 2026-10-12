@ Project Grounded: MtCoronet_5F (tools/grounded/maptools/coronet.py)
MtCoronet_5F_MapScripts::
	.byte 0

MtCoronet_5F_EventScript_Dejavu::
	trainerbattle_single TRAINER_CORONET_DEJAVU, MtCoronet_5F_Text_DejavuIntro, MtCoronet_5F_Text_DejavuDefeat
	msgbox MtCoronet_5F_Text_DejavuPost, MSGBOX_AUTOCLOSE
	end

MtCoronet_5F_EventScript_Nebula::
	trainerbattle_single TRAINER_CORONET_NEBULA, MtCoronet_5F_Text_NebulaIntro, MtCoronet_5F_Text_NebulaDefeat
	msgbox MtCoronet_5F_Text_NebulaPost, MSGBOX_AUTOCLOSE
	end

@ ---------------------------------------------------------------- teksten (placeholders, Jordi herschrijft ze)
MtCoronet_5F_Text_DejavuIntro:
	.string "Have we done this before? We've done\n"
	.string "this before. I'm sure we've done this\l"
	.string "before.$"

MtCoronet_5F_Text_DejavuDefeat:
	.string "...We've definitely done this before. You\n"
	.string "won then too.$"

MtCoronet_5F_Text_DejavuPost:
	.string "Next time, I'm doing something\n"
	.string "different. I said that last time.$"

MtCoronet_5F_Text_NebulaIntro:
	.string "A nebula is where stars are born. I'm\n"
	.string "where trainers come to lose. Close\l"
	.string "enough!$"

MtCoronet_5F_Text_NebulaDefeat:
	.string "A star is born. It's you. I hate it.$"

MtCoronet_5F_Text_NebulaPost:
	.string "Above us is SPEAR PILLAR. Above that is\n"
	.string "space. PALKIA owns both. No visitors\l"
	.string "after midnight.$"
