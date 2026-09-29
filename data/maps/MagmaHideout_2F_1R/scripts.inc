MagmaHideout_2F_1R_MapScripts::
	.byte 0

MagmaHideout_2F_1R_EventScript_Grunt14::
	trainerbattle_single TRAINER_GRUNT_MAGMA_HIDEOUT_14, MagmaHideout_2F_1R_Text_Grunt14Intro, MagmaHideout_2F_1R_Text_Grunt14Defeat
	msgbox MagmaHideout_2F_1R_Text_Grunt14PostBattle, MSGBOX_AUTOCLOSE
	end

MagmaHideout_2F_1R_EventScript_Grunt3::
	trainerbattle_single TRAINER_GRUNT_MAGMA_HIDEOUT_3, MagmaHideout_2F_1R_Text_Grunt3Intro, MagmaHideout_2F_1R_Text_Grunt3Defeat
	msgbox MagmaHideout_2F_1R_Text_Grunt3PostBattle, MSGBOX_AUTOCLOSE
	end

MagmaHideout_2F_1R_EventScript_Grunt4::
	trainerbattle_single TRAINER_GRUNT_MAGMA_HIDEOUT_4, MagmaHideout_2F_1R_Text_Grunt4Intro, MagmaHideout_2F_1R_Text_Grunt4Defeat
	msgbox MagmaHideout_2F_1R_Text_Grunt4PostBattle, MSGBOX_AUTOCLOSE
	end

MagmaHideout_2F_1R_EventScript_Grunt5::
	trainerbattle_single TRAINER_GRUNT_MAGMA_HIDEOUT_5, MagmaHideout_2F_1R_Text_Grunt5Intro, MagmaHideout_2F_1R_Text_Grunt5Defeat
	msgbox MagmaHideout_2F_1R_Text_Grunt5PostBattle, MSGBOX_AUTOCLOSE
	end

MagmaHideout_2F_1R_Text_Grunt14Intro:
	.string "Only people who can handle a million\n"
	.string "SCOVILLE are allowed in here!$"

MagmaHideout_2F_1R_Text_Grunt14Defeat:
	.string "My pride… and my stomach…$"

MagmaHideout_2F_1R_Text_Grunt14PostBattle:
	.string "If you suffer from chills, eat a raw\n"
	.string "CAPSAKID.$"

MagmaHideout_2F_1R_Text_Grunt3Intro:
	.string "Hold it! Nobody passes without a taste\n"
	.string "test!$"

MagmaHideout_2F_1R_Text_Grunt3Defeat:
	.string "Your tongue is made of steel!$"

MagmaHideout_2F_1R_Text_Grunt3PostBattle:
	.string "Maybe I should've let you pass. And\n"
	.string "gone to the bathroom.$"

MagmaHideout_2F_1R_Text_Grunt4Intro:
	.string "An intruder! Quick, hide the sauce!$"

MagmaHideout_2F_1R_Text_Grunt4Defeat:
	.string "Graaah! I touched my eyes!$"

MagmaHideout_2F_1R_Text_Grunt4PostBattle:
	.string "Never touch your eyes after chopping\n"
	.string "peppers. Rule number one.$"

MagmaHideout_2F_1R_Text_Grunt5Intro:
	.string "Oh, an intruder! Want a sample?$"

MagmaHideout_2F_1R_Text_Grunt5Defeat:
	.string "Nobody ever wants a sample…$"

MagmaHideout_2F_1R_Text_Grunt5PostBattle:
	.string "Actually, I'm no expert at battling…$"

