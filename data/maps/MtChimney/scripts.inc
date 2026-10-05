MtChimney_MapScripts::
	map_script MAP_SCRIPT_ON_RESUME, MtChimney_OnResume
	map_script MAP_SCRIPT_ON_TRANSITION, MtChimney_OnTransition
	map_script MAP_SCRIPT_ON_LOAD, MtChimney_OnLoad
	.byte 0

@ Project Grounded: vanaf badge 5 is er een verborgen grotingang aan de westkant (gang naar Entei)
MtChimney_OnLoad:
	goto_if_unset FLAG_BADGE05_GET, MtChimney_EventScript_EnteiCaveHidden
	setmetatile 8, 11, METATILE_Lavaridge_CaveEntrance_Top, TRUE
	setmetatile 8, 12, METATILE_Lavaridge_CaveEntrance_Bottom, FALSE
MtChimney_EventScript_EnteiCaveHidden:
	end

MtChimney_OnTransition:
	setvar VAR_JAGGED_PASS_ASH_WEATHER, 1
	@ Project Grounded: trap naar de top (noordoostkam). Tot badge 5 houdt de vulkanoloog je tegen;
	@ hij staat er pas als Team Magma weg is. VAR_TEMP_1 = 1: de trap is open.
	setflag FLAG_HIDE_MT_CHIMNEY_TRAIL_GUARD
	setvar VAR_TEMP_1, 0
	goto_if_set FLAG_BADGE05_GET, MtChimney_EventScript_TrailOpen
	goto_if_unset FLAG_HIDE_MT_CHIMNEY_TEAM_MAGMA, MtChimney_EventScript_TrailEnd
	clearflag FLAG_HIDE_MT_CHIMNEY_TRAIL_GUARD
	end
MtChimney_EventScript_TrailOpen:
	setvar VAR_TEMP_1, 1
MtChimney_EventScript_TrailEnd:
	end

MtChimney_EventScript_TrailClosed::
	lockall
	msgbox MtChimney_Text_TrailClosed, MSGBOX_DEFAULT
	closemessage
	applymovement OBJ_EVENT_ID_PLAYER, Common_Movement_WalkDown
	waitmovement 0
	releaseall
	end

MtChimney_EventScript_TrailGuard::
	msgbox MtChimney_Text_TrailGuard, MSGBOX_NPC
	end

MtChimney_Text_TrailClosed:
	.string "Whoa, whoa! The trail to the true\n"
	.string "summit is closed.\p"
	.string "Seismic activity. Also my insurance\n"
	.string "only covers people with five BADGES.$"

MtChimney_Text_TrailGuard:
	.string "I'm a volcanologist. I stand here so\n"
	.string "the mountain has someone to blame.\p"
	.string "Come back with five BADGES. The\n"
	.string "summit only eats experienced people.$"

MtChimney_OnResume:
	setstepcallback STEP_CB_ASH
	end

MtChimney_EventScript_Archie::
	lock
	faceplayer
	call_if_unset FLAG_EVIL_LEADER_PLEASE_STOP, MtChimney_EventScript_ArchieGoStopTeamMagma
	call_if_set FLAG_EVIL_LEADER_PLEASE_STOP, MtChimney_EventScript_ArchieBusyFighting
	closemessage
	applymovement LOCALID_MT_CHIMNEY_ARCHIE, Common_Movement_FaceOriginalDirection
	waitmovement 0
	setflag FLAG_EVIL_LEADER_PLEASE_STOP
	release
	end

MtChimney_EventScript_ArchieGoStopTeamMagma::
	msgbox MtChimney_Text_ArchieGoStopTeamMagma, MSGBOX_DEFAULT
	return

MtChimney_EventScript_ArchieBusyFighting::
	msgbox MtChimney_Text_ArchieIHaveMyHandsFull, MSGBOX_DEFAULT
	return

MtChimney_EventScript_Maxie::
	lockall
	playbgm MUS_ENCOUNTER_MAGMA, FALSE
	msgbox MtChimney_Text_MeteoriteWillActivateVolcano, MSGBOX_DEFAULT
	applymovement LOCALID_MT_CHIMNEY_MAXIE, Common_Movement_FacePlayer
	waitmovement 0
	playse SE_PIN
	applymovement LOCALID_MT_CHIMNEY_MAXIE, Common_Movement_ExclamationMark
	waitmovement 0
	applymovement LOCALID_MT_CHIMNEY_MAXIE, Common_Movement_Delay48
	waitmovement 0
	msgbox MtChimney_Text_MaxieIntro, MSGBOX_DEFAULT
	closemessage
	@ Project Grounded: Tabitha komt terug, Wally rent binnen en vecht met je mee (tag battle).
	applymovement LOCALID_MT_CHIMNEY_TABITHA, MtChimney_Movement_TabithaJoinMaxie
	waitmovement 0
	addobject LOCALID_MT_CHIMNEY_WALLY
	applymovement LOCALID_MT_CHIMNEY_WALLY, MtChimney_Movement_WallyRunIn
	waitmovement 0
	playse SE_PIN
	applymovement LOCALID_MT_CHIMNEY_WALLY, Common_Movement_ExclamationMark
	waitmovement 0
	msgbox MtChimney_Text_WallyWhoopWhoop, MSGBOX_DEFAULT
	closemessage
MtChimney_EventScript_ChooseMonsForWallyTag::
	special SavePlayerParty
	fadescreen FADE_TO_BLACK
	special ChooseHalfPartyForBattle
	waitstate
	goto_if_ne VAR_RESULT, 0, MtChimney_EventScript_DoWallyTagBattle
	special LoadPlayerParty
	goto MtChimney_EventScript_ChooseMonsForWallyTag

MtChimney_EventScript_DoWallyTagBattle::
	multi_2_vs_2 TRAINER_MAXIE_MT_CHIMNEY, MtChimney_Text_MaxieDefeat, TRAINER_TABITHA_MT_CHIMNEY_TAG, MtChimney_Text_TabithaDefeat, PARTNER_WALLY
	switch VAR_RESULT
	case 1, MtChimney_EventScript_DefeatedMaxieWithWally
	fadescreen FADE_TO_BLACK
	special SetCB2WhiteOut
	waitstate

MtChimney_EventScript_DefeatedMaxieWithWally::
	msgbox MtChimney_Text_MaxieYouHaventSeenLastOfMagma, MSGBOX_DEFAULT
	closemessage
	delay 30
	fadescreenswapbuffers FADE_TO_BLACK
	removeobject LOCALID_MT_CHIMNEY_MAXIE
	removeobject LOCALID_MT_CHIMNEY_MAGMA_GRUNT_1
	removeobject LOCALID_MT_CHIMNEY_TABITHA
	removeobject LOCALID_MT_CHIMNEY_MAGMA_GRUNT_2
	removeobject LOCALID_MT_CHIMNEY_WALLY
	setflag FLAG_HIDE_MT_CHIMNEY_WALLY
	setflag FLAG_HIDE_MT_CHIMNEY_TEAM_MAGMA
	fadescreenswapbuffers FADE_FROM_BLACK
	setobjectxyperm LOCALID_MT_CHIMNEY_ARCHIE, 10, 12
	addobject LOCALID_MT_CHIMNEY_ARCHIE
	call_if_eq VAR_FACING, DIR_EAST, MtChimney_EventScript_ArchieApproachPlayerEast
	call_if_eq VAR_FACING, DIR_NORTH, MtChimney_EventScript_ArchieApproachPlayerNorth
	applymovement LOCALID_PLAYER, Common_Movement_WalkInPlaceFasterLeft
	waitmovement 0
	msgbox MtChimney_Text_ArchieThankYou, MSGBOX_DEFAULT
	closemessage
	call_if_eq VAR_FACING, DIR_EAST, MtChimney_EventScript_ArchieExitEast
	call_if_eq VAR_FACING, DIR_NORTH, MtChimney_EventScript_ArchieExitNorth
	removeobject LOCALID_MT_CHIMNEY_ARCHIE
	setflag FLAG_HIDE_MT_CHIMNEY_TEAM_AQUA
	setflag FLAG_DEFEATED_EVIL_TEAM_MT_CHIMNEY
	clearflag FLAG_HIDE_FALLARBOR_HOUSE_PROF_COZMO
	setflag FLAG_HIDE_METEOR_FALLS_1F_1R_COZMO
	clearflag FLAG_HIDE_MT_CHIMNEY_LAVA_COOKIE_LADY
	releaseall
	end

MtChimney_EventScript_ArchieApproachPlayerEast::
	applymovement LOCALID_MT_CHIMNEY_ARCHIE, MtChimney_Movement_ArchieApproachPlayerEast
	waitmovement 0
	return

MtChimney_EventScript_ArchieApproachPlayerNorth::
	applymovement LOCALID_MT_CHIMNEY_ARCHIE, MtChimney_Movement_ArchieApproachPlayerNorth
	waitmovement 0
	return

MtChimney_EventScript_ArchieExitEast::
	applymovement LOCALID_MT_CHIMNEY_ARCHIE, MtChimney_Movement_ArchieExitEast
	waitmovement 0
	return

MtChimney_EventScript_ArchieExitNorth::
	applymovement LOCALID_MT_CHIMNEY_ARCHIE, MtChimney_Movement_ArchieExitNorth
	waitmovement 0
	return

MtChimney_EventScript_LavaCookieLady::
	lock
	faceplayer
	showmoneybox 0, 0
	msgbox MtChimney_Text_LavaCookiesJust200, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, MtChimney_EventScript_DeclineLavaCookie
	checkmoney 200
	goto_if_eq VAR_RESULT, FALSE, MtChimney_EventScript_NotEnoughMoney
	msgbox MtChimney_Text_ThankYouDear, MSGBOX_DEFAULT
	checkitemspace ITEM_LAVA_COOKIE
	call_if_eq VAR_RESULT, TRUE, MtChimney_EventScript_RemoveMoney
.if OW_SHOW_ITEM_DESCRIPTIONS == OW_ITEM_DESCRIPTIONS_OFF
	giveitem ITEM_LAVA_COOKIE
	goto_if_eq VAR_RESULT, FALSE, MtChimney_EventScript_BagIsFull
	hidemoneybox
	release
	end

MtChimney_EventScript_BagIsFull::
	msgbox gText_TooBadBagIsFull, MSGBOX_DEFAULT
	hidemoneybox
	release
	end
.else
	hidemoneybox
	giveitem ITEM_LAVA_COOKIE
	goto_if_eq VAR_RESULT, FALSE, MtChimney_EventScript_BagIsFull
	release
	end

MtChimney_EventScript_BagIsFull::
	msgbox gText_TooBadBagIsFull, MSGBOX_DEFAULT
	release
	end
.endif @ OW_SHOW_ITEM_DESCRIPTIONS


MtChimney_EventScript_RemoveMoney::
	removemoney 200
	updatemoneybox
	return

MtChimney_EventScript_DeclineLavaCookie::
	msgbox MtChimney_Text_OhFineThen, MSGBOX_DEFAULT
	hidemoneybox
	release
	end

MtChimney_EventScript_NotEnoughMoney::
	msgbox MtChimney_Text_YouveNotGotTheMoney, MSGBOX_DEFAULT
	hidemoneybox
	release
	end

MtChimney_Movement_ArchieApproachPlayerEast:
	walk_up
	walk_up
	walk_up
	walk_up
	walk_up
	walk_up
	walk_right
	step_end

MtChimney_Movement_ArchieExitEast:
	walk_left
	walk_down
	walk_down
	walk_down
	walk_down
	walk_down
	walk_down
	walk_down
	step_end

MtChimney_Movement_ArchieApproachPlayerNorth:
	walk_up
	walk_up
	walk_up
	walk_up
	walk_up
	walk_right
	walk_right
	step_end

MtChimney_Movement_ArchieExitNorth:
	walk_left
	walk_left
	walk_down
	walk_down
	walk_down
	walk_down
	walk_down
	walk_down
	walk_down
	step_end

MtChimney_Movement_Unused1:
	walk_down
	walk_down
	walk_down
	walk_down
	walk_down
	walk_left
	walk_left
	walk_down
	walk_down
	walk_down
	walk_down
	walk_left
	walk_left
	walk_left
	walk_left
	walk_left
	walk_down
	step_end

MtChimney_Movement_Unused2:
	walk_down
	walk_down
	walk_down
	walk_down
	walk_left
	walk_left
	walk_left
	walk_down
	step_end

MtChimney_Movement_Unused3:
	walk_right
	walk_down
	walk_down
	walk_down
	walk_down
	walk_left
	walk_left
	walk_left
	walk_left
	walk_left
	walk_down
	walk_down
	walk_down
	walk_down
	step_end

MtChimney_Movement_Unused4:
	walk_fast_down
	walk_fast_down
	walk_fast_down
	walk_fast_down
	walk_fast_down
	walk_fast_down
	walk_fast_down
	walk_fast_down
	walk_fast_down
	walk_left
	walk_left
	walk_down
	walk_down
	walk_down
	walk_left
	walk_left
	walk_down
	walk_down
	walk_left
	walk_left
	walk_left
	walk_left
	walk_left
	walk_down
	step_end

MtChimney_Movement_Unused5:
	delay_16
	delay_16
	delay_16
	walk_down
	walk_down
	walk_down
	walk_left
	walk_left
	walk_left
	walk_down
	step_end

MtChimney_Movement_Unused6:
	delay_16
	walk_left
	walk_down
	walk_down
	walk_down
	walk_down
	walk_left
	walk_left
	walk_left
	walk_left
	walk_left
	walk_down
	walk_down
	walk_down
	walk_down
	step_end

MtChimney_Movement_Unused7:
	delay_16
	walk_left
	walk_left
	walk_down
	walk_down
	walk_down
	walk_left
	walk_left
	walk_down
	walk_down
	walk_left
	walk_left
	walk_left
	walk_left
	walk_left
	walk_down
	step_end

MtChimney_Movement_Unused8:
	delay_16
	walk_down
	walk_left
	walk_left
	walk_left
	walk_left
	walk_in_place_faster_down
	step_end

MtChimney_Movement_Unused9:
	walk_down
	walk_down
	walk_down
	walk_down
	walk_left
	walk_left
	walk_left
	walk_left
	walk_left
	walk_down
	walk_down
	walk_down
	walk_down
	step_end

MtChimney_Movement_Unused10:
	walk_down
	step_end

MtChimney_Movement_Unused11:
	walk_down
	walk_down
	walk_down
	walk_down
	walk_down
	walk_down
	walk_down
	step_end

MtChimney_Movement_Unused12:
	delay_16
	delay_16
	walk_in_place_faster_left
	delay_16
	walk_down
	walk_down
	walk_down
	walk_down
	walk_down
	step_end

MtChimney_Movement_Unused13:
	delay_16
	delay_16
	delay_16
	delay_16
	delay_16
	delay_16
	walk_in_place_faster_left
	delay_16
	walk_down
	walk_down
	step_end

MtChimney_Movement_Unused14:
	lock_facing_direction
	walk_fast_left
	unlock_facing_direction
	face_right
	step_end

MtChimney_Movement_Unused15:
	walk_left
	walk_in_place_faster_right
	delay_16
	step_end

MtChimney_EventScript_BusyAquaGrunt1::
	msgbox MtChimney_Text_MagmaOutnumbersUs, MSGBOX_SIGN
	end

MtChimney_EventScript_BusyAquaGrunt2::
	msgbox MtChimney_Text_LessHabitatForWaterPokemon, MSGBOX_SIGN
	end

MtChimney_EventScript_BusyAquaGrunt3::
	msgbox MtChimney_Text_MagmasNameSimilar, MSGBOX_SIGN
	end

MtChimney_EventScript_Tabitha::
	trainerbattle_single TRAINER_TABITHA_MT_CHIMNEY, MtChimney_Text_TabithaIntro, MtChimney_Text_TabithaDefeat
	msgbox MtChimney_Text_TabithaPostBattle, MSGBOX_AUTOCLOSE
	end

MtChimney_EventScript_Grunt2::
	trainerbattle_single TRAINER_GRUNT_MT_CHIMNEY_2, MtChimney_Text_Grunt2Intro, MtChimney_Text_Grunt2Defeat
	msgbox MtChimney_Text_Grunt2PostBattle, MSGBOX_AUTOCLOSE
	end

MtChimney_EventScript_BusyMagmaGrunt1::
	msgbox MtChimney_Text_TeamAquaAlwaysMessingWithPlans, MSGBOX_SIGN
	end

MtChimney_EventScript_BusyMagmaGrunt2::
	msgbox MtChimney_Text_MeteoritesPackAmazingPower, MSGBOX_SIGN
	end

MtChimney_EventScript_BusyMagmaGrunt3::
	msgbox MtChimney_Text_YouBetterNotMessWithUs, MSGBOX_SIGN
	end

MtChimney_EventScript_BusyMagmaGrunt4::
	msgbox MtChimney_Text_AquasNameSimilar, MSGBOX_SIGN
	end

MtChimney_EventScript_BusyMagmaGrunt5::
	msgbox MtChimney_Text_DouseThemInFire, MSGBOX_SIGN
	end

MtChimney_EventScript_BusyMagmaGrunt6::
	msgbox MtChimney_Text_KeepMakingMoreLand, MSGBOX_SIGN
	end

MtChimney_EventScript_MagmaPoochyena::
	msgbox MtChimney_Text_Bufoh, MSGBOX_SIGN
	end

MtChimney_EventScript_AquaPoochyena::
	msgbox MtChimney_Text_Bushaa, MSGBOX_SIGN
	end

MtChimney_EventScript_MeteoriteMachine::
	lockall
	goto_if_unset FLAG_DEFEATED_EVIL_TEAM_MT_CHIMNEY, MtChimney_EventScript_MachineOn
	goto_if_set FLAG_RECEIVED_METEORITE, MtChimney_EventScript_MachineOff
	msgbox MtChimney_Text_RemoveTheMeteorite, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, MtChimney_EventScript_LeaveMeteoriteAlone
	msgbox MtChimney_Text_PlayerRemovedMeteorite, MSGBOX_DEFAULT
	giveitem ITEM_METEORITE
	goto_if_eq VAR_RESULT, FALSE, Common_EventScript_ShowBagIsFull
	setflag FLAG_RECEIVED_METEORITE
	releaseall
	end

MtChimney_EventScript_LeaveMeteoriteAlone::
	msgbox MtChimney_Text_PlayerLeftMeteorite, MSGBOX_DEFAULT
	releaseall
	end

MtChimney_EventScript_MachineOff::
	msgbox MtChimney_Text_MachineMakesNoResponse, MSGBOX_DEFAULT
	releaseall
	end

MtChimney_EventScript_MachineOn::
	msgbox MtChimney_Text_MetoriteFittedOnMachine, MSGBOX_DEFAULT
	releaseall
	end

MtChimney_EventScript_RouteSign::
	msgbox MtChimney_Text_RouteSign, MSGBOX_SIGN
	end

MtChimney_EventScript_Shelby::
	trainerbattle_single TRAINER_SHELBY_1, MtChimney_Text_ShelbyIntro, MtChimney_Text_ShelbyDefeat, MtChimney_EventScript_DefeatedShelby
	specialvar VAR_RESULT, ShouldTryRematchBattle
	goto_if_eq VAR_RESULT, TRUE, MtChimney_EventScript_RematchShelby
	msgbox MtChimney_Text_ShelbyPostBattle, MSGBOX_DEFAULT
	release
	end

MtChimney_EventScript_DefeatedShelby::
	special PlayerFaceTrainerAfterBattle
	waitmovement 0
	msgbox MtChimney_Text_ShelbyRegister, MSGBOX_DEFAULT
	register_matchcall TRAINER_SHELBY_1
	release
	end

MtChimney_EventScript_RematchShelby::
	trainerbattle_rematch TRAINER_SHELBY_1, MtChimney_Text_ShelbyRematchIntro, MtChimney_Text_ShelbyRematchDefeat
	msgbox MtChimney_Text_ShelbyPostRematch, MSGBOX_AUTOCLOSE
	end

MtChimney_EventScript_Melissa::
	trainerbattle_single TRAINER_MELISSA, MtChimney_Text_MelissaIntro, MtChimney_Text_MelissaDefeat
	msgbox MtChimney_Text_MelissaPostBattle, MSGBOX_AUTOCLOSE
	end

MtChimney_EventScript_Sheila::
	trainerbattle_single TRAINER_SHEILA, MtChimney_Text_SheilaIntro, MtChimney_Text_SheilaDefeat
	msgbox MtChimney_Text_SheilaPostBattle, MSGBOX_AUTOCLOSE
	end

MtChimney_EventScript_Shirley::
	trainerbattle_single TRAINER_SHIRLEY, MtChimney_Text_ShirleyIntro, MtChimney_Text_ShirleyDefeat
	msgbox MtChimney_Text_ShirleyPostBattle, MSGBOX_AUTOCLOSE
	end

MtChimney_EventScript_Grunt1::
	trainerbattle_single TRAINER_GRUNT_MT_CHIMNEY_1, MtChimney_Text_Grunt1Intro, MtChimney_Text_Grunt1Defeat
	msgbox MtChimney_Text_Grunt1PostBattle, MSGBOX_AUTOCLOSE
	end

MtChimney_EventScript_Sawyer::
	trainerbattle_single TRAINER_SAWYER_1, MtChimney_Text_SawyerIntro, MtChimney_Text_SawyerDefeat, MtChimney_EventScript_SawyerDefeated
	specialvar VAR_RESULT, ShouldTryRematchBattle
	goto_if_eq VAR_RESULT, TRUE, MtChimney_EventScript_SawyerRematch
	msgbox MtChimney_Text_SawyerPostBattle, MSGBOX_DEFAULT
	release
	end

MtChimney_EventScript_SawyerDefeated::
	special PlayerFaceTrainerAfterBattle
	waitmovement 0
	msgbox MtChimney_Text_SawyerRegister, MSGBOX_DEFAULT
	register_matchcall TRAINER_SAWYER_1
	release
	end

MtChimney_EventScript_SawyerRematch::
	trainerbattle_rematch TRAINER_SAWYER_1, MtChimney_Text_SawyerRematchIntro, MtChimney_Text_SawyerRematchDefeat
	msgbox MtChimney_Text_SawyerPostRematch, MSGBOX_AUTOCLOSE
	end

MtChimney_Text_MeteoriteWillActivateVolcano:
	.string "The METEORITE's power…\p"
	.string "Amplified by this machine, MT. CHIMNEY\n"
	.string "heats up…\p"
	.string "The perfect pepper greenhouse.\n"
	.string "Fufufu…$"

MtChimney_Text_MaxieIntro:
	.string "MAXIE: Hm? Who are you?\p"
	.string "… … … … … …\p"
	.string "ARCHIE mentioned a child. The one who\n"
	.string "drinks tap water.\p"
	.string "Listen. Long ago, all life came from the\n"
	.string "land.\p"
	.string "And from the land come peppers.\p"
	.string "MAGMA HOT SAUCE will be on every table\n"
	.string "in HOENN.\p"
	.string "For that, I need what sleeps in this\n"
	.string "mountain…\p"
	.string "Oops. I've said too much.\p"
	.string "No matter! Taste the consequences!$"

MtChimney_Text_MaxieDefeat:
	.string "What?!\p"
	.string "I, MAXIE, was caught off guard?!$"

MtChimney_Text_MaxieYouHaventSeenLastOfMagma:
	.string "MAXIE: Enough. I'll back off this time.\p"
	.string "But MAGMA isn't done.\p"
	.string "Even without the METEORITE, if we get\n"
	.string "that ORB…\p"
	.string "Fufufu… Extra hot.$"

MtChimney_Text_TabithaIntro:
	.string "Hehehe! You're too late!\p"
	.string "I already brought the METEORITE to the\n"
	.string "BOSS!\p"
	.string "I always deliver.$"

MtChimney_Text_TabithaDefeat:
	.string "Hehehe…\p"
	.string "Even if I lose, the BOSS gets it done. He\n"
	.string "always does.$"

MtChimney_Text_TabithaPostBattle:
	.string "BOSS, hurry! Give it the METEORITE!\p"
	.string "I'll hold your coat. Hehehe…$"

MtChimney_Text_Grunt2Intro:
	.string "Most people in HOENN are so pale they\n"
	.string "sweat from black pepper. We're here to\l"
	.string "help.$"

MtChimney_Text_Grunt2Defeat:
	.string "Hunh? You're not even sweating?$"

MtChimney_Text_Grunt2PostBattle:
	.string "Our BOSS says, “It will make everyone\n"
	.string "happy.” Then why is everyone crying?$"

MtChimney_Text_Grunt1Intro:
	.string "More land means more chili fields! More\n"
	.string "chili fields means more hot sauce!$"

MtChimney_Text_Grunt1Defeat:
	.string "My chili fields…$"

MtChimney_Text_Grunt1PostBattle:
	.string "A kid like you should stick to ketchup.$"

MtChimney_Text_TeamAquaAlwaysMessingWithPlans:
	.string "That annoying TEAM AQUA… Always\n"
	.string "ruining our plans!\p"
	.string "And our sauce. They water it down!$"

MtChimney_Text_MeteoritesPackAmazingPower:
	.string "METEORITES pack amazing power!\p"
	.string "Like a ghost pepper from space!$"

MtChimney_Text_YouBetterNotMessWithUs:
	.string "Don't mess with us!\p"
	.string "We're awakening that thing for\n"
	.string "everyone's benefit!\p"
	.string "Everyone who likes spicy food.$"

MtChimney_Text_AquasNameSimilar:
	.string "We're TEAM MAGMA!\p"
	.string "They're TEAM AQUA!\p"
	.string "We sound like two flavors of the same\n"
	.string "drink!$"

MtChimney_Text_DouseThemInFire:
	.string "Yeah! Douse them in sauce! Extra hot!$"

MtChimney_Text_KeepMakingMoreLand:
	.string "More land! More peppers! More sauce!$"

MtChimney_Text_Bufoh:
	.string "Bufoh!\p"
	.string "(It's panting. The hot sauce got it.)$"

MtChimney_Text_ArchieGoStopTeamMagma:
	.string "ARCHIE: Grr, {PLAYER}! Of course you're\n"
	.string "here.\p"
	.string "Look what MAGMA is doing!\p"
	.string "They're pumping the METEORITE into the\n"
	.string "volcano!\p"
	.string "If it erupts, the whole mountain\n"
	.string "becomes a chili pan!$"

MtChimney_Text_ArchieIHaveMyHandsFull:
	.string "ARCHIE: Grrr…\p"
	.string "I want to stop MAXIE, but I'm fighting\n"
	.string "three goons at once!$"

MtChimney_Text_ArchieThankYou:
	.string "ARCHIE: {PLAYER}! Thank you!\p"
	.string "MAGMA's plan is foiled!\p"
	.string "But… whose side are you on?\p"
	.string "Doesn't matter. Free SPA? No?\p"
	.string "We'll meet again!$"

MtChimney_Text_MagmaOutnumbersUs:
	.string "Darn… MAGMA outnumbers us!\p"
	.string "They have free samples. That's how they\n"
	.string "recruit.$"

MtChimney_Text_LessHabitatForWaterPokemon:
	.string "More land means less water!\p"
	.string "Less water means fewer bubbles!$"

MtChimney_Text_MagmasNameSimilar:
	.string "We're TEAM AQUA!\p"
	.string "They're TEAM MAGMA!\p"
	.string "Who came up with this? Same marketing\n"
	.string "agency?$"

MtChimney_Text_Bushaa:
	.string "Bushaa!\p"
	.string "(It burps. Sparkling water.)$"

MtChimney_Text_LavaCookiesJust200:
	.string "LAVA COOKIES! MT. CHIMNEY's specialty!\p"
	.string "Just ¥200. Only a little ash in them.$"

MtChimney_Text_ThankYouDear:
	.string "Thank you, dear!\p"
	.string "Don't chew too hard. Some bits are\n"
	.string "volcanic.$"

MtChimney_Text_YouveNotGotTheMoney:
	.string "Oh, dear. No money, no cookies.\p"
	.string "That's capitalism, sweetie.$"

MtChimney_Text_OhFineThen:
	.string "Oh, fine then.\p"
	.string "Your loss. Literally.$"

MtChimney_Text_MetoriteFittedOnMachine:
	.string "A METEORITE is fitted into a mysterious\n"
	.string "machine…\p"
	.string "It's charging up the METEORITE.\p"
	.string "There's a pepper plant taped to the\n"
	.string "side.$"

MtChimney_Text_RemoveTheMeteorite:
	.string "A METEORITE is fitted into a mysterious\n"
	.string "machine…\p"
	.string "Remove the METEORITE?$"

MtChimney_Text_PlayerRemovedMeteorite:
	.string "{PLAYER} removed the METEORITE from\n"
	.string "the machine.\p"
	.string "It's warm. And smells like chili.$"

MtChimney_Text_PlayerLeftMeteorite:
	.string "{PLAYER} left the METEORITE where it\n"
	.string "was.$"

MtChimney_Text_MachineMakesNoResponse:
	.string "The mysterious machine does nothing at\n"
	.string "all.\p"
	.string "Like most of DEVON's stuff.$"

MtChimney_Text_RouteSign:
	.string "{DOWN_ARROW} JAGGED PATH\n"
	.string "LAVARIDGE TOWN AHEAD\p"
	.string "Wear shoes. Seriously.$"

MtChimney_Text_ShelbyIntro:
	.string "I soaked in the hot springs.\p"
	.string "My bones feel 60 again! I'm 82!$"

MtChimney_Text_ShelbyDefeat:
	.string "Oh, my goodness. Aren't you something!$"

MtChimney_Text_ShelbyPostBattle:
	.string "I lost. Can I still call myself an\n"
	.string "EXPERT?\p"
	.string "I'll call myself a SENIOR. That comes\n"
	.string "with discounts.$"

MtChimney_Text_ShelbyRegister:
	.string "That was fun, like battling my\n"
	.string "grandchild.\p"
	.string "My grandchild never visits. You will,\n"
	.string "right?$"

MtChimney_Text_ShelbyRematchIntro:
	.string "Mesh your heart with your POKéMON and\n"
	.string "you'll achieve great things.\p"
	.string "Mesh your back with the hot springs and\n"
	.string "you'll feel great too.$"

MtChimney_Text_ShelbyRematchDefeat:
	.string "Oh, my goodness. Aren't you something!$"

MtChimney_Text_ShelbyPostRematch:
	.string "Your heart and your POKéMON's are one.\p"
	.string "My heart and my hip are not.$"

MtChimney_Text_MelissaIntro:
	.string "I've got the fire in me, baby!\p"
	.string "It might be the chili from TEAM MAGMA.$"

MtChimney_Text_MelissaDefeat:
	.string "Ooh, scorching-hot match!$"

MtChimney_Text_MelissaPostBattle:
	.string "MT. CHIMNEY warms me up, baby!\p"
	.string "My makeup is melting, though.$"

MtChimney_Text_SheilaIntro:
	.string "I finally made it to MT. CHIMNEY!\p"
	.string "The view is… grey. Everything is grey.$"

MtChimney_Text_SheilaDefeat:
	.string "You battle like an eruption!$"

MtChimney_Text_SheilaPostBattle:
	.string "I came for sightseeing and battles.\p"
	.string "And LAVA COOKIES. The cookies are the\n"
	.string "real reason.$"

MtChimney_Text_ShirleyIntro:
	.string "Since bathing in the hot springs, I feel\n"
	.string "amazing!\p"
	.string "My skin is glowing! Or burning. Hard to\n"
	.string "tell.$"

MtChimney_Text_ShirleyDefeat:
	.string "Yowch! I'm getting a chill!$"

MtChimney_Text_ShirleyPostBattle:
	.string "I need another dip in the hot springs.\p"
	.string "Want to join me?\p"
	.string "Just kidding. Hotel rules.$"

MtChimney_Text_SawyerIntro:
	.string "Fine mountain! Plenty of hot people\n"
	.string "around!\p"
	.string "I mean the temperature. I'm a hiker, not\n"
	.string "a creep.$"

MtChimney_Text_SawyerDefeat:
	.string "Oh, you're a real firebrand!$"

MtChimney_Text_SawyerPostBattle:
	.string "I need a dip in the LAVARIDGE HOT\n"
	.string "SPRINGS.\p"
	.string "The locals say I smell like a hiker.$"

MtChimney_Text_SawyerRegister:
	.string "I like firebrands like you! Let's\n"
	.string "register.$"

MtChimney_Text_SawyerRematchIntro:
	.string "Still surrounded by hot people.\n"
	.string "Temperature-wise!$"

MtChimney_Text_SawyerRematchDefeat:
	.string "Still a firebrand, huh!$"

MtChimney_Text_SawyerPostRematch:
	.string "It's really hot here. I'm wearing three\n"
	.string "sweaters.\p"
	.string "Hiker habit.$"

MtChimney_Movement_TabithaJoinMaxie:
	walk_fast_left
	walk_fast_left
	walk_fast_up
	walk_fast_up
	walk_fast_up
	walk_fast_up
	walk_fast_right
	walk_fast_right
	face_up
	step_end

MtChimney_Movement_WallyRunIn:
	walk_fast_up
	walk_fast_up
	walk_fast_up
	walk_fast_up
	walk_fast_up
	walk_fast_up
	walk_fast_right
	face_up
	step_end

MtChimney_Text_WallyWhoopWhoop:
	.string "WALLY: Whoopwhoop, hot {PLAYER}\n"
	.string "fight with, want learn.\p"
	.string "Come ons!$"
