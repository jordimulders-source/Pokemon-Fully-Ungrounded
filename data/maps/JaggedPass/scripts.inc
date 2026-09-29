JaggedPass_MapScripts::
	map_script MAP_SCRIPT_ON_RESUME, JaggedPass_OnResume
	map_script MAP_SCRIPT_ON_TRANSITION, JaggedPass_OnTransition
	map_script MAP_SCRIPT_ON_LOAD, JaggedPass_OnLoad
	.byte 0

JaggedPass_OnResume:
	setstepcallback STEP_CB_ASH
	call_if_eq VAR_JAGGED_PASS_STATE, 0, JaggedPass_EventScript_CheckHasMagmaEmblem
	end

JaggedPass_EventScript_CheckHasMagmaEmblem::
	checkitem ITEM_MAGMA_EMBLEM
	goto_if_eq VAR_RESULT, TRUE, JaggedPass_EventScript_SetReadyToOpenHideout
	return

JaggedPass_EventScript_SetReadyToOpenHideout::
	setvar VAR_JAGGED_PASS_STATE, 1
	return

JaggedPass_OnTransition:
	call_if_eq VAR_JAGGED_PASS_ASH_WEATHER, 1, JaggedPass_EventScript_SetWeatherAsh
	end

JaggedPass_EventScript_SetWeatherAsh::
	setweather WEATHER_VOLCANIC_ASH
	doweather
	return

JaggedPass_OnLoad:
	goto_if_le VAR_JAGGED_PASS_STATE, 1, JaggedPass_EventScript_ConcealHideoutEntrance
	end

JaggedPass_EventScript_ConcealHideoutEntrance::
	setmetatile 16, 17, METATILE_Lavaridge_RockWall, TRUE
	setmetatile 16, 18, METATILE_Lavaridge_RockWall, TRUE
	end

JaggedPass_EventScript_OpenMagmaHideout::
	lockall
	setvar VAR_0x8004, 1  @ vertical pan
	setvar VAR_0x8005, 1  @ horizontal pan
	setvar VAR_0x8006, 8  @ num shakes
	setvar VAR_0x8007, 5  @ shake delay
	special ShakeCamera
	waitstate
	msgbox JaggedPass_Text_BoulderShakingInResponseToEmblem, MSGBOX_DEFAULT
	closemessage
	setvar VAR_0x8004, 1   @ vertical pan
	setvar VAR_0x8005, 1   @ horizontal pan
	setvar VAR_0x8006, 16  @ num shakes
	setvar VAR_0x8007, 3   @ shake delay
	special ShakeCamera
	waitstate
	playse SE_EFFECTIVE
	setmetatile 16, 17, METATILE_Lavaridge_CaveEntrance_Top, TRUE
	setmetatile 16, 18, METATILE_Lavaridge_CaveEntrance_Bottom, FALSE
	special DrawWholeMapView
	delay 30
	setvar VAR_JAGGED_PASS_STATE, 2
	waitse
	releaseall
	end

JaggedPass_EventScript_MagmaHideoutGuard::
	lockall
	goto_if_set FLAG_BEAT_MAGMA_GRUNT_JAGGED_PASS, JaggedPass_EventScript_GuardDefeated
	waitse
	playse SE_PIN
	applymovement LOCALID_MAGMA_HIDEOUT_GUARD, Common_Movement_ExclamationMark
	waitmovement 0
	applymovement LOCALID_MAGMA_HIDEOUT_GUARD, Common_Movement_Delay48
	waitmovement 0
	applymovement LOCALID_MAGMA_HIDEOUT_GUARD, Common_Movement_FacePlayer
	waitmovement 0
	msgbox JaggedPass_Text_GruntIntro, MSGBOX_DEFAULT
	closemessage
	trainerbattle_no_intro TRAINER_GRUNT_JAGGED_PASS, JaggedPass_Text_GruntDefeat
	setflag FLAG_BEAT_MAGMA_GRUNT_JAGGED_PASS
	applymovement LOCALID_MAGMA_HIDEOUT_GUARD, Common_Movement_FaceOriginalDirection
	waitmovement 0
	releaseall
	end

JaggedPass_EventScript_GuardDefeated::
	applymovement LOCALID_MAGMA_HIDEOUT_GUARD, Common_Movement_FacePlayer
	waitmovement 0
	msgbox JaggedPass_Text_GoWhereverYouWant, MSGBOX_DEFAULT
	closemessage
	applymovement LOCALID_MAGMA_HIDEOUT_GUARD, Common_Movement_FaceOriginalDirection
	waitmovement 0
	releaseall
	end

JaggedPass_EventScript_Eric::
	trainerbattle_single TRAINER_ERIC, JaggedPass_Text_EricIntro, JaggedPass_Text_EricDefeat
	msgbox JaggedPass_Text_EricPostBattle, MSGBOX_AUTOCLOSE
	end

JaggedPass_EventScript_Diana::
	trainerbattle_single TRAINER_DIANA_1, JaggedPass_Text_DianaIntro, JaggedPass_Text_DianaDefeat, JaggedPass_EventScript_RegisterDiana
	specialvar VAR_RESULT, ShouldTryRematchBattle
	goto_if_eq VAR_RESULT, TRUE, JaggedPass_EventScript_DianaRematch
	msgbox JaggedPass_Text_DianaPostBattle, MSGBOX_DEFAULT
	release
	end

JaggedPass_EventScript_RegisterDiana::
	special PlayerFaceTrainerAfterBattle
	msgbox JaggedPass_Text_DianaRegister, MSGBOX_DEFAULT
	register_matchcall TRAINER_DIANA_1
	release
	end

JaggedPass_EventScript_DianaRematch::
	trainerbattle_rematch TRAINER_DIANA_1, JaggedPass_Text_DianaRematchIntro, JaggedPass_Text_DianaRematchDefeat
	msgbox JaggedPass_Text_DianaPostRematch, MSGBOX_AUTOCLOSE
	end

JaggedPass_EventScript_Ethan::
	trainerbattle_single TRAINER_ETHAN_1, JaggedPass_Text_EthanIntro, JaggedPass_Text_EthanDefeat, JaggedPass_EventScript_RegisterEthan
	specialvar VAR_RESULT, ShouldTryRematchBattle
	goto_if_eq VAR_RESULT, TRUE, JaggedPass_EventScript_EthanRematch
	msgbox JaggedPass_Text_EthanPostBattle, MSGBOX_DEFAULT
	release
	end

JaggedPass_EventScript_RegisterEthan::
	special PlayerFaceTrainerAfterBattle
	msgbox JaggedPass_Text_EthanRegister, MSGBOX_DEFAULT
	register_matchcall TRAINER_ETHAN_1
	release
	end

JaggedPass_EventScript_EthanRematch::
	trainerbattle_rematch TRAINER_ETHAN_1, JaggedPass_Text_EthanRematchIntro, JaggedPass_Text_EthanRematchDefeat
	msgbox JaggedPass_Text_EthanPostRematch, MSGBOX_AUTOCLOSE
	end

JaggedPass_EventScript_Julio::
	trainerbattle_single TRAINER_JULIO, JaggedPass_Text_JulioIntro, JaggedPass_Text_JulioDefeat
	msgbox JaggedPass_Text_JulioPostBattle, MSGBOX_AUTOCLOSE
	end

JaggedPass_EventScript_Autumn::
	trainerbattle_single TRAINER_AUTUMN, JaggedPass_Text_AutumnIntro, JaggedPass_Text_AutumnDefeat
	msgbox JaggedPass_Text_AutumnPostBattle, MSGBOX_AUTOCLOSE
	end

JaggedPass_Text_EricIntro:
	.string "JAGGED PASS…\p"
	.string "This bumpiness… It rocks my soul!\p"
	.string "And my knees. Mostly my knees.$"

JaggedPass_Text_EricDefeat:
	.string "Losing left me bitter! Like the ash!$"

JaggedPass_Text_EricPostBattle:
	.string "I lost at POKéMON…\p"
	.string "But I love mountains more than you.\p"
	.string "I married one. Emotionally.$"

JaggedPass_Text_DianaIntro:
	.string "This is not a picnic spot.\p"
	.string "I brought a picnic anyway. It's covered\n"
	.string "in ash.$"

JaggedPass_Text_DianaDefeat:
	.string "Ohhh, no! The ground is too bumpy… My\n"
	.string "sandwich fell.$"

JaggedPass_Text_DianaPostBattle:
	.string "Some people ride their bikes up this\n"
	.string "pass.\p"
	.string "Those people are psychopaths.$"

JaggedPass_Text_DianaRegister:
	.string "Come back sometime!\p"
	.string "I'll have a new sandwich. Probably also\n"
	.string "ashy.$"

JaggedPass_Text_DianaRematchIntro:
	.string "Picnics are fun anywhere! Even on a\n"
	.string "volcano!$"

JaggedPass_Text_DianaRematchDefeat:
	.string "I only lost because the ground is\n"
	.string "bumpy!$"

JaggedPass_Text_DianaPostRematch:
	.string "I'll forget about losing and eat my ash\n"
	.string "sandwich.$"

JaggedPass_Text_EthanIntro:
	.string "JAGGED PASS is hard to walk on.\p"
	.string "Great for training. Terrible for ankles.$"

JaggedPass_Text_EthanDefeat:
	.string "We lost while still looking for solid\n"
	.string "ground…$"

JaggedPass_Text_EthanPostBattle:
	.string "With an ACRO BIKE I could jump these\n"
	.string "ledges.\p"
	.string "I'd also die. But stylishly.$"

JaggedPass_Text_EthanRegister:
	.string "Once I'm used to the bumps, I'll win!\p"
	.string "Register me, please.$"

JaggedPass_Text_EthanRematchIntro:
	.string "I'm used to the bumps now. I sing while I\n"
	.string "climb.\p"
	.string "Badly. But loudly.$"

JaggedPass_Text_EthanRematchDefeat:
	.string "Still not easy on this ground…$"

JaggedPass_Text_EthanPostRematch:
	.string "I really should get that ACRO BIKE from\n"
	.string "RYDEL.\p"
	.string "He gives them away, right? Right?$"

JaggedPass_Text_GruntIntro:
	.string "Wah! What are you doing here? I'm, uh…\n"
	.string "harvesting. For the sauce.$"

JaggedPass_Text_GruntDefeat:
	.string "My mouth is on fire. Not in the good way.$"

JaggedPass_Text_GoWhereverYouWant:
	.string "Okay, okay! You're strong!\p"
	.string "Go wherever you want!\p"
	.string "I'll stay here. With the chili.$"

JaggedPass_Text_BoulderShakingInResponseToEmblem:
	.string "This boulder is shaking at the MAGMA\n"
	.string "EMBLEM!\p"
	.string "It smells like hot sauce.$"

JaggedPass_Text_JulioIntro:
	.string "They see me rollin'… They hatin'…$"

JaggedPass_Text_JulioDefeat:
	.string "…They caught me ridin' dirty.$"

JaggedPass_Text_JulioPostBattle:
	.string "My bike bounced so much, my rear end's\n"
	.string "sore.\p"
	.string "They see me limpin'…$"

JaggedPass_Text_AutumnIntro:
	.string "I climb this hill every day!\p"
	.string "My thighs could crack walnuts!$"

JaggedPass_Text_AutumnDefeat:
	.string "Hmm… What went wrong? Leg day wasn't\n"
	.string "enough?$"

JaggedPass_Text_AutumnPostBattle:
	.string "See that odd rock up the hill?\p"
	.string "I think someone lives behind it. Weird.$"

