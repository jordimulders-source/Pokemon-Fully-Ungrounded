AquaHideout_B2F_MapScripts::
	map_script MAP_SCRIPT_ON_TRANSITION, AquaHideout_B2F_OnTransition
	.byte 0

AquaHideout_B2F_OnTransition:
	call_if_set FLAG_TEAM_AQUA_ESCAPED_IN_SUBMARINE, AquaHideout_B2F_EventScript_PreventMattNoticing
	end

AquaHideout_B2F_EventScript_PreventMattNoticing::
	setvar VAR_TEMP_1, 1
	return

AquaHideout_B2F_EventScript_MattNoticePlayer::
	lockall
	setvar VAR_0x8008, LOCALID_AQUA_HIDEOUT_MATT
	playse SE_PIN
	applymovement VAR_0x8008, Common_Movement_ExclamationMark
	waitmovement 0
	applymovement VAR_0x8008, Common_Movement_FacePlayer
	waitmovement 0
	setvar VAR_TEMP_1, 1
	releaseall
	end

AquaHideout_B2F_EventScript_Matt::
	trainerbattle_single TRAINER_MATT, AquaHideout_B2F_Text_MattIntro, AquaHideout_B2F_Text_MattDefeat, AquaHideout_B2F_EventScript_SubmarineEscape
	msgbox AquaHideout_B2F_Text_MattPostBattle, MSGBOX_DEFAULT
	release
	end

AquaHideout_B2F_EventScript_SubmarineEscape::
	setvar VAR_0x8008, LOCALID_AQUA_HIDEOUT_MATT
	setvar VAR_0x8009, LOCALID_AQUA_HIDEOUT_SUBMARINE
	applymovement VAR_0x8008, Common_Movement_WalkInPlaceFasterLeft
	waitmovement 0
	delay 20
	applymovement VAR_0x8008, Common_Movement_FacePlayer
	waitmovement 0
	msgbox AquaHideout_B2F_Text_OurBossGotThroughHisPreparations, MSGBOX_DEFAULT
	closemessage
	applymovement VAR_0x8008, Common_Movement_WalkInPlaceFasterLeft
	applymovement VAR_0x8009, AquaHideout_B2F_Movement_SumbarineDepartLeft
	waitmovement 0
	removeobject VAR_0x8009
	delay 20
	applymovement VAR_0x8008, Common_Movement_FacePlayer
	waitmovement 0
	msgbox AquaHideout_B2F_Text_MattPostBattle, MSGBOX_DEFAULT
	setflag FLAG_TEAM_AQUA_ESCAPED_IN_SUBMARINE
	setflag FLAG_HIDE_LILYCOVE_CITY_AQUA_GRUNTS
	release
	end

AquaHideout_B2F_Movement_SumbarineDepartLeft:
	walk_left
	walk_left
	walk_left
	walk_left
	step_end

@ Unused
AquaHideout_B2F_Movement_SumbarineDepartRight:
	walk_right
	walk_right
	walk_right
	walk_right
	step_end

AquaHideout_B2F_EventScript_Grunt4::
	trainerbattle_single TRAINER_GRUNT_AQUA_HIDEOUT_4, AquaHideout_B2F_Text_Grunt4Intro, AquaHideout_B2F_Text_Grunt4Defeat, AquaHideout_B2F_EventScript_Grunt4Defeated
	msgbox AquaHideout_B2F_Text_Grunt4PostBattle, MSGBOX_AUTOCLOSE
	end

AquaHideout_B2F_EventScript_Grunt4Defeated::
	msgbox AquaHideout_B2F_Text_Grunt4PostBattle, MSGBOX_DEFAULT
	release
	end

AquaHideout_B2F_EventScript_Grunt6::
	trainerbattle_single TRAINER_GRUNT_AQUA_HIDEOUT_6, AquaHideout_B2F_Text_Grunt6Intro, AquaHideout_B2F_Text_Grunt6Defeat
	msgbox AquaHideout_B2F_Text_Grunt6PostBattle, MSGBOX_AUTOCLOSE
	end

AquaHideout_B2F_EventScript_Grunt8::
	trainerbattle_single TRAINER_GRUNT_AQUA_HIDEOUT_8, AquaHideout_B2F_Text_Grunt8Intro, AquaHideout_B2F_Text_Grunt8Defeat
	msgbox AquaHideout_B2F_Text_Grunt8PostBattle, MSGBOX_AUTOCLOSE
	end

AquaHideout_B2F_Text_MattIntro:
	.string "I am not a grunt, I am a dancing queen,\n"
	.string "only seventeen! And I will beat you!$"

AquaHideout_B2F_Text_MattDefeat:
	.string "Did I say queen?$"

AquaHideout_B2F_Text_OurBossGotThroughHisPreparations:
	.string "Your confusion helped our boss escape!\n"
	.string "Androgyny for the win!$"

AquaHideout_B2F_Text_MattPostBattle:
	.string "So I will definitely not tell you that\n"
	.string "our boss got out to LILYCOVE. In the\l"
	.string "meantime why won't you tell me about\l"
	.string "your previous endeavors? While our\l"
	.string "boss gets up to some heinous shit.$"

AquaHideout_B2F_Text_Grunt4Intro:
	.string "En garde!$"

AquaHideout_B2F_Text_Grunt4Defeat:
	.string "Putain!$"

AquaHideout_B2F_Text_Grunt4PostBattle:
	.string "Sacre bleu!$"

AquaHideout_B2F_Text_Grunt6Intro:
	.string "Yeah our warps aren't as lousy as Team\n"
	.string "Rocket's in Silph Co. This will take you a\l"
	.string "bit less time, for your convenience. Call\l"
	.string "it quality of life! Wait, we are supposed\l"
	.string "to hold you up aren't we?$"

AquaHideout_B2F_Text_Grunt6Defeat:
	.string "I should warp away!$"

AquaHideout_B2F_Text_Grunt6PostBattle:
	.string "That reminds me… I can't remember where\n"
	.string "I put the MASTER BALL.\p"
	.string "Damn, I was supposed to catch a wild\n"
	.string "Beldum with it.$"

AquaHideout_B2F_Text_Grunt8Intro:
	.string "When I joined TEAM AQUA, the first thing\n"
	.string "I had to learn was how these warp\l"
	.string "panels connected. Needless to say, as\l"
	.string "an ex-Rocket, that was easy!$"

AquaHideout_B2F_Text_Grunt8Defeat:
	.string "I was too occupied fantasizing about\n"
	.string "the warp panels…$"

AquaHideout_B2F_Text_Grunt8PostBattle:
	.string "At least these do not time warp, that\n"
	.string "would suck! Imagine doing over every\l"
	.string "single one of these grunt battles!$"
