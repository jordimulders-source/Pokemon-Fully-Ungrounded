@ Project Grounded: MtCoronet_6F (tools/grounded/maptools/coronet.py)
MtCoronet_6F_MapScripts::
	.byte 0

MtCoronet_6F_EventScript_Chronos::
	trainerbattle_single TRAINER_CORONET_CHRONOS, MtCoronet_6F_Text_ChronosIntro, MtCoronet_6F_Text_ChronosDefeat
	msgbox MtCoronet_6F_Text_ChronosPost, MSGBOX_AUTOCLOSE
	end

MtCoronet_6F_EventScript_Spatia::
	trainerbattle_single TRAINER_CORONET_SPATIA, MtCoronet_6F_Text_SpatiaIntro, MtCoronet_6F_Text_SpatiaDefeat
	msgbox MtCoronet_6F_Text_SpatiaPost, MSGBOX_AUTOCLOSE
	end

@ ---------------------------------------------------------------- teksten (placeholders, Jordi herschrijft ze)
MtCoronet_6F_Text_ChronosIntro:
	.string "I am the last of DIALGA's projections.\n"
	.string "DIALGA has watched every possible\l"
	.string "version of this battle.\p"
	.string "In most of them you brought more\n"
	.string "Revives.$"

MtCoronet_6F_Text_ChronosDefeat:
	.string "Interesting. That was one of the rare\n"
	.string "timelines.$"

MtCoronet_6F_Text_ChronosPost:
	.string "Go on. DIALGA waits at the top. It\n"
	.string "already knows how this ends. It just\l"
	.string "likes to watch.$"

MtCoronet_6F_Text_SpatiaIntro:
	.string "I am the last of PALKIA's projections.\n"
	.string "Between you and SPEAR PILLAR lies\l"
	.string "exactly one trainer and an\l"
	.string "unreasonable amount of space.$"

MtCoronet_6F_Text_SpatiaDefeat:
	.string "The space between us has been...\n"
	.string "resolved.$"

MtCoronet_6F_Text_SpatiaPost:
	.string "The light at the top is SPEAR PILLAR.\n"
	.string "Don't touch the pearl unless you mean\l"
	.string "it. Same for the diamond. Same for most\l"
	.string "things.$"
