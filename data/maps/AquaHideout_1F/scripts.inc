AquaHideout_1F_MapScripts::
	.byte 0

@ The below two entrance guards give hints about what to do to progress the story
AquaHideout_1F_EventScript_HideoutEntranceGrunt1::
	lock
	faceplayer
	goto_if_set FLAG_GROUDON_AWAKENED_MAGMA_HIDEOUT, AquaHideout_1F_EventScript_SlateportHint1
	goto_if_set FLAG_RECEIVED_RED_OR_BLUE_ORB, AquaHideout_1F_EventScript_MagmaHideoutHint1
	msgbox AquaHideout_1F_Text_OurBossIsSnatchingSomething, MSGBOX_DEFAULT
	release
	end

AquaHideout_1F_EventScript_MagmaHideoutHint1::
	msgbox AquaHideout_1F_Text_WhereMightMagmaHideoutBe, MSGBOX_DEFAULT
	release
	end

AquaHideout_1F_EventScript_SlateportHint1::
	msgbox AquaHideout_1F_Text_BossWentToJackASubmarine, MSGBOX_DEFAULT
	release
	end

AquaHideout_1F_EventScript_HideoutEntranceGrunt2::
	lock
	faceplayer
	goto_if_set FLAG_GROUDON_AWAKENED_MAGMA_HIDEOUT, AquaHideout_1F_EventScript_SlateportHint2
	goto_if_set FLAG_RECEIVED_RED_OR_BLUE_ORB, AquaHideout_1F_EventScript_MagmaHideoutHint2
	msgbox AquaHideout_1F_Text_BossIsOnRoute122, MSGBOX_DEFAULT
	release
	end

AquaHideout_1F_EventScript_MagmaHideoutHint2::
	msgbox AquaHideout_1F_Text_TeamMagmaAtMtChimney, MSGBOX_DEFAULT
	release
	end

AquaHideout_1F_EventScript_SlateportHint2::
	msgbox AquaHideout_1F_Text_BossIsInSlateportCity, MSGBOX_DEFAULT
	release
	end

AquaHideout_1F_EventScript_Grunt1::
	trainerbattle_single TRAINER_GRUNT_AQUA_HIDEOUT_1, AquaHideout_1F_Text_Grunt1Intro, AquaHideout_1F_Text_Grunt1Defeat, AquaHideout_1F_EventScript_Grunt1Defeated
	msgbox AquaHideout_1F_Text_Grunt1PostBattle, MSGBOX_AUTOCLOSE
	end

AquaHideout_1F_EventScript_Grunt1Defeated::
	msgbox AquaHideout_1F_Text_Grunt1PostBattle, MSGBOX_DEFAULT
	release
	end

AquaHideout_1F_Text_OurBossIsSnatchingSomething:
	.string "What? What? What are you doing here?\p"
	.string "Our capo? Or the big boss? I ain't no\n"
	.string "snitch! I won't tell you where they are.$"

AquaHideout_1F_Text_WhereMightMagmaHideoutBe:
	.string "TEAM MAGMA? Those stupid activists.\n"
	.string "Let them burn in their own hell,\l"
	.string "literally. If I knew where their hideout\l"
	.string "is, I would splash the whole place, with\l"
	.string "a hose. That'll teach them!$"

AquaHideout_1F_Text_BossWentToJackASubmarine:
	.string "Where's the boss? Something about a\n"
	.string "Yellow Submarine? He wants one, but no\l"
	.string "idea where they sell these, or have\l"
	.string "them.$"

AquaHideout_1F_Text_BossIsOnRoute122:
	.string "Big Boss is at Mt. Pyre. No idea what\n"
	.string "he's doing with all the spiritual\l"
	.string "bullshit over there, maybe he is into\l"
	.string "astrology? Why am I telling you this?$"

AquaHideout_1F_Text_TeamMagmaAtMtChimney:
	.string "GROUDON and KYOGRE have awesome music.\n"
	.string "I would go undercover at TEAM MAGMA, so\l"
	.string "I could hear it twice.$"

AquaHideout_1F_Text_BossIsInSlateportCity:
	.string "SLATEPORT has a PORT, with boats. Yeah,\n"
	.string "surprising, really?$"

AquaHideout_1F_Text_Grunt1Intro:
	.string "Ayiyiyi! Suspicious character spotted!\n"
	.string "Please do not touch me!$"

AquaHideout_1F_Text_Grunt1Defeat:
	.string "I'm scared!!!!$"

AquaHideout_1F_Text_Grunt1PostBattle:
	.string "HAHAHA, you thought I was scared, but I\n"
	.string "wasn't. Also I am actually your grandma\l"
	.string "as well! Hahahaha, Now that's a twist. My\l"
	.string "colleagues have already finished their\l"
	.string "sinister plans now too.$"

