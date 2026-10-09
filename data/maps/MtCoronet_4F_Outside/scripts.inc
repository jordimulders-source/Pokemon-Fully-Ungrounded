@ Project Grounded: MtCoronet_4F_Outside (tools/grounded/maptools/coronet.py)
MtCoronet_4F_Outside_MapScripts::
	.byte 0

MtCoronet_4F_Outside_EventScript_Aeon::
	trainerbattle_single TRAINER_CORONET_AEON, MtCoronet_4F_Outside_Text_AeonIntro, MtCoronet_4F_Outside_Text_AeonDefeat
	msgbox MtCoronet_4F_Outside_Text_AeonPost, MSGBOX_AUTOCLOSE
	end

MtCoronet_4F_Outside_EventScript_Voida::
	trainerbattle_single TRAINER_CORONET_VOIDA, MtCoronet_4F_Outside_Text_VoidaIntro, MtCoronet_4F_Outside_Text_VoidaDefeat
	msgbox MtCoronet_4F_Outside_Text_VoidaPost, MSGBOX_AUTOCLOSE
	end

MtCoronet_4F_Outside_EventScript_Momentum::
	trainerbattle_single TRAINER_CORONET_MOMENTUM, MtCoronet_4F_Outside_Text_MomentumIntro, MtCoronet_4F_Outside_Text_MomentumDefeat
	msgbox MtCoronet_4F_Outside_Text_MomentumPost, MSGBOX_AUTOCLOSE
	end

MtCoronet_4F_Outside_EventScript_Orbit::
	trainerbattle_single TRAINER_CORONET_ORBIT, MtCoronet_4F_Outside_Text_OrbitIntro, MtCoronet_4F_Outside_Text_OrbitDefeat
	msgbox MtCoronet_4F_Outside_Text_OrbitPost, MSGBOX_AUTOCLOSE
	end

MtCoronet_4F_Outside_EventScript_Epoch::
	trainerbattle_single TRAINER_CORONET_EPOCH, MtCoronet_4F_Outside_Text_EpochIntro, MtCoronet_4F_Outside_Text_EpochDefeat
	msgbox MtCoronet_4F_Outside_Text_EpochPost, MSGBOX_AUTOCLOSE
	end

MtCoronet_4F_Outside_EventScript_Sign::
	msgbox MtCoronet_4F_Outside_Text_Sign, MSGBOX_SIGN
	end

@ ---------------------------------------------------------------- teksten (placeholders, Jordi herschrijft ze)
MtCoronet_4F_Outside_Text_AeonIntro:
	.string "I've waited here for an aeon. That's\n"
	.string "DIALGA's little joke.\p"
	.string "It has been eleven minutes.$"

MtCoronet_4F_Outside_Text_AeonDefeat:
	.string "Eleven minutes and one loss. A\n"
	.string "productive day.$"

MtCoronet_4F_Outside_Text_AeonPost:
	.string "Every time someone beats me, DIALGA\n"
	.string "rewinds me. I've lost this fight four\l"
	.string "hundred times.\p"
	.string "You're the first who said 'oops'.$"

MtCoronet_4F_Outside_Text_VoidaIntro:
	.string "The void between dimensions is cold,\n"
	.string "dark and full of my ex.\p"
	.string "PALKIA projected me out of it. I owe it\n"
	.string "one fight.$"

MtCoronet_4F_Outside_Text_VoidaDefeat:
	.string "Back to the void. At least it doesn't\n"
	.string "judge my GHOST types.$"

MtCoronet_4F_Outside_Text_VoidaPost:
	.string "If you hear whispering on this\n"
	.string "mountain, it's not me. It's the other me.\l"
	.string "Two dimensions over.$"

MtCoronet_4F_Outside_Text_MomentumIntro:
	.string "A body in motion stays in motion! That's\n"
	.string "physics! I'm a projection, so it's also\l"
	.string "my entire personality!$"

MtCoronet_4F_Outside_Text_MomentumDefeat:
	.string "An unstoppable force met an immovable\n"
	.string "object. The object was you.$"

MtCoronet_4F_Outside_Text_MomentumPost:
	.string "DIALGA says I'm 'temporally unstable'.\n"
	.string "My doctor said the same about my knees.$"

MtCoronet_4F_Outside_Text_OrbitIntro:
	.string "I orbit this cave entrance at a\n"
	.string "distance of exactly three tiles.\p"
	.string "Cross my orbit and gravity takes over.\n"
	.string "Gravity is me.$"

MtCoronet_4F_Outside_Text_OrbitDefeat:
	.string "My orbit decayed. That's the polite word\n"
	.string "for it.$"

MtCoronet_4F_Outside_Text_OrbitPost:
	.string "PALKIA folds space so the cave is\n"
	.string "bigger inside. That's why the rent is so\l"
	.string "high.$"

MtCoronet_4F_Outside_Text_EpochIntro:
	.string "Every fossil on my team was alive\n"
	.string "yesterday. Not your yesterday.\l"
	.string "DIALGA's.$"

MtCoronet_4F_Outside_Text_EpochDefeat:
	.string "Extinct again. They're used to it.$"

MtCoronet_4F_Outside_Text_EpochPost:
	.string "Time is just very slow archaeology.$"

MtCoronet_4F_Outside_Text_Sign:
	.string "MT. CORONET, 4F (exterior)\p"
	.string "The summit is up. Everything is up,\n"
	.string "eventually.\p"
	.string "Do not feed the projections.$"
