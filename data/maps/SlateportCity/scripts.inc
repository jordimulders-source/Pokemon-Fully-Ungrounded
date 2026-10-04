SlateportCity_MapScripts::
	map_script MAP_SCRIPT_ON_TRANSITION, SlateportCity_OnTransition
	map_script MAP_SCRIPT_ON_FRAME_TABLE, SlateportCity_OnFrame
	.byte 0

SlateportCity_OnTransition:
	call SlateportCity_EventScript_SetScottDisguise
	setvar VAR_SLATEPORT_MUSEUM_1F_STATE, 0
	call SlateportCity_EventScript_EnterSlateport
	call_if_eq VAR_SLATEPORT_CITY_STATE, 1, SlateportCity_EventScript_MovePeopleForSternInterview
	call_if_eq VAR_SLATEPORT_OUTSIDE_MUSEUM_STATE, 1, SlateportCity_EventScript_SetReadyForScottScene
	end

SlateportCity_EventScript_EnterSlateport::
	setflag FLAG_VISITED_SLATEPORT_CITY
	setvar VAR_CONTEST_HALL_STATE, 0
	setflag FLAG_HIDE_SLATEPORT_CITY_CONTEST_REPORTER
	return

SlateportCity_EventScript_MovePeopleForSternInterview::
	setobjectxyperm LOCALID_SLATEPORT_CAPT_STERN, 28, 13
	setobjectxyperm LOCALID_SLATEPORT_OLD_WOMAN, 25, 13
	setobjectxyperm LOCALID_SLATEPORT_RICH_BOY, 25, 14
	setobjectxyperm LOCALID_SLATEPORT_COOK, 27, 16
	setobjectxyperm LOCALID_SLATEPORT_GIRL, 28, 16
	setobjectxyperm LOCALID_SLATEPORT_FAT_MAN, 29, 16
	setobjectxyperm LOCALID_SLATEPORT_MAN_1, 31, 14
	setobjectmovementtype LOCALID_SLATEPORT_CAPT_STERN, MOVEMENT_TYPE_FACE_DOWN
	setobjectmovementtype LOCALID_SLATEPORT_OLD_WOMAN, MOVEMENT_TYPE_FACE_DOWN_AND_RIGHT
	setobjectmovementtype LOCALID_SLATEPORT_RICH_BOY, MOVEMENT_TYPE_FACE_UP_AND_RIGHT
	setobjectmovementtype LOCALID_SLATEPORT_COOK, MOVEMENT_TYPE_FACE_UP
	setobjectmovementtype LOCALID_SLATEPORT_GIRL, MOVEMENT_TYPE_FACE_UP
	setobjectmovementtype LOCALID_SLATEPORT_FAT_MAN, MOVEMENT_TYPE_FACE_UP
	setobjectmovementtype LOCALID_SLATEPORT_MAN_1, MOVEMENT_TYPE_FACE_LEFT
	return

SlateportCity_EventScript_SetReadyForScottScene::
	setflag FLAG_HIDE_MAP_NAME_POPUP
	getplayerxy VAR_0x8004, VAR_0x8005
	goto_if_eq VAR_0x8004, 30, SlateportCity_EventScript_MoveScottLeft
	setobjectxyperm LOCALID_SLATEPORT_SCOTT, 23, 27
	setobjectmovementtype LOCALID_SLATEPORT_SCOTT, MOVEMENT_TYPE_FACE_RIGHT
	return

SlateportCity_EventScript_MoveScottLeft::
	setobjectxyperm LOCALID_SLATEPORT_SCOTT, 22, 27
	setobjectmovementtype LOCALID_SLATEPORT_SCOTT, MOVEMENT_TYPE_FACE_RIGHT
	return

SlateportCity_OnFrame:
	map_script_2 VAR_SLATEPORT_OUTSIDE_MUSEUM_STATE, 1, SlateportCity_EventScript_ScottScene
	.2byte 0

SlateportCity_EventScript_ScottScene::
	lockall
	addobject LOCALID_SLATEPORT_SCOTT
	applymovement LOCALID_PLAYER, SlateportCity_Movement_PlayerFaceScott
	applymovement LOCALID_SLATEPORT_SCOTT, SlateportCity_Movement_ScottApproachPlayer
	waitmovement 0
	msgbox SlateportCity_Text_YouDroveTeamAquaAway, MSGBOX_DEFAULT
	closemessage
	applymovement LOCALID_SLATEPORT_SCOTT, Common_Movement_WalkInPlaceFasterLeft
	waitmovement 0
	delay 60
	msgbox SlateportCity_Text_MaybeThisTrainer, MSGBOX_DEFAULT
	applymovement LOCALID_SLATEPORT_SCOTT, Common_Movement_WalkInPlaceFasterRight
	waitmovement 0
	msgbox SlateportCity_Text_LetsRegisterEachOther, MSGBOX_DEFAULT
	closemessage
	delay 30
	playfanfare MUS_REGISTER_MATCH_CALL
	msgbox SlateportCity_Text_RegisteredScott, MSGBOX_DEFAULT
	waitfanfare
	closemessage
	delay 30
	setflag FLAG_ENABLE_SCOTT_MATCH_CALL
	msgbox SlateportCity_Text_KeepEyeOnTrainersBeSeeingYou, MSGBOX_DEFAULT
	closemessage
	applymovement LOCALID_SLATEPORT_SCOTT, SlateportCity_Movement_ScottExit
	waitmovement 0
	removeobject LOCALID_SLATEPORT_SCOTT
	setobjectxyperm LOCALID_SLATEPORT_SCOTT, 10, 12
	setobjectmovementtype LOCALID_SLATEPORT_SCOTT, MOVEMENT_TYPE_FACE_DOWN
	clearflag FLAG_HIDE_MAP_NAME_POPUP
	setvar VAR_SLATEPORT_OUTSIDE_MUSEUM_STATE, 2
	addvar VAR_SCOTT_STATE, 1
	releaseall
	end

SlateportCity_Movement_PlayerFaceScott:
	delay_16
	delay_8
	walk_in_place_faster_left
	step_end

SlateportCity_Movement_ScottApproachPlayer:
	walk_right
	walk_right
	walk_right
	walk_right
	walk_right
	walk_right
	walk_right
	step_end

SlateportCity_Movement_ScottExit:
	walk_left
	walk_left
	walk_left
	walk_left
	walk_left
	walk_left
	walk_left
	walk_left
	step_end

SlateportCity_EventScript_EnergyGuru::
	lock
	faceplayer
	message SlateportCity_Text_EnergyGuruSellWhatYouNeed
	waitmessage
	pokemart SlateportCity_Pokemart_EnergyGuru
	msgbox gText_PleaseComeAgain, MSGBOX_DEFAULT
	release
	end

	.align 2
SlateportCity_Pokemart_EnergyGuru:
	.2byte ITEM_PROTEIN
	.2byte ITEM_IRON
	.2byte ITEM_CARBOS
	.2byte ITEM_ZINC
	.2byte ITEM_CALCIUM
	.2byte ITEM_HP_UP
	pokemartlistend

SlateportCity_EventScript_EffortRibbonWoman::
	lock
	faceplayer
	bufferleadmonspeciesname STR_VAR_1
	msgbox SlateportCity_Text_OhYourPokemon, MSGBOX_DEFAULT
	specialvar VAR_RESULT, LeadMonHasEffortRibbon
	call_if_eq VAR_RESULT, TRUE, SlateportCity_EventScript_MonHasEffortRibbon
	specialvar VAR_RESULT, Special_AreLeadMonEVsMaxedOut
	call_if_eq VAR_RESULT, FALSE, SlateportCity_EventScript_MonEVsNotMaxed
	msgbox SlateportCity_Text_PleaseGiveItThisEffortRibbon, MSGBOX_DEFAULT
	playfanfare MUS_OBTAIN_ITEM
	message SlateportCity_Text_ReceivedEffortRibbon
	waitfanfare
	msgbox SlateportCity_Text_PutEffortRibbonOnMon, MSGBOX_DEFAULT
	special GiveLeadMonEffortRibbon
	release
	end

SlateportCity_EventScript_MonEVsNotMaxed::
	msgbox SlateportCity_Text_GoForItLittleHarder, MSGBOX_DEFAULT
	release
	end

SlateportCity_EventScript_MonHasEffortRibbon::
	msgbox SlateportCity_Text_EffortRibbonLooksGoodOnIt, MSGBOX_DEFAULT
	release
	end

SlateportCity_EventScript_Cook::
	lock
	faceplayer
	call_if_eq VAR_SLATEPORT_CITY_STATE, 1, SlateportCity_EventScript_CookSternInterview
	msgbox SlateportCity_Text_SeaweedFullOfLife, MSGBOX_DEFAULT
	release
	end

SlateportCity_EventScript_CookSternInterview::
	msgbox SlateportCity_Text_CaptainComeBackWithBigFish, MSGBOX_DEFAULT
	release
	end

SlateportCity_EventScript_OldWoman::
	lock
	faceplayer
	call_if_eq VAR_SLATEPORT_CITY_STATE, 1, SlateportCity_EventScript_OldWomanSternInterview
	msgbox SlateportCity_Text_HowTownIsBornAndGrows, MSGBOX_DEFAULT
	release
	end

SlateportCity_EventScript_OldWomanSternInterview::
	msgbox SlateportCity_Text_CaptSternBeingInterviewed, MSGBOX_DEFAULT
	release
	end

SlateportCity_EventScript_Girl::
	lock
	faceplayer
	call_if_eq VAR_SLATEPORT_CITY_STATE, 1, SlateportCity_EventScript_GirlSternInterview
	goto_if_set FLAG_RECEIVED_SECRET_POWER, SlateportCity_EventScript_GirlSecretBase
	msgbox SlateportCity_Text_SlateportWonderfulPlace, MSGBOX_DEFAULT
	release
	end

SlateportCity_EventScript_GirlSternInterview::
	msgbox SlateportCity_Text_InterviewerSoCool, MSGBOX_DEFAULT
	release
	end

SlateportCity_EventScript_GirlSecretBase::
	msgbox SlateportCity_Text_BuyBricksSoDecorWontGetDirty, MSGBOX_DEFAULT
	release
	end

SlateportCity_EventScript_RichBoy::
	lock
	faceplayer
	call_if_eq VAR_SLATEPORT_CITY_STATE, 1, SlateportCity_EventScript_RichBoySternInterview
	msgbox SlateportCity_Text_GoingToCompeteInBattleTent, MSGBOX_DEFAULT
	release
	end

SlateportCity_EventScript_RichBoySternInterview::
	msgbox SlateportCity_Text_SternSaysDiscoveredSomething, MSGBOX_DEFAULT
	release
	end

SlateportCity_EventScript_FatMan::
	goto_if_eq VAR_SLATEPORT_CITY_STATE, 1, SlateportCity_EventScript_FatManSternInterview
	msgbox SlateportCity_Text_BushedHikingFromMauville, MSGBOX_NPC
	end

SlateportCity_EventScript_FatManSternInterview::
	msgbox SlateportCity_Text_AmIOnTV, MSGBOX_SIGN
	end

SlateportCity_EventScript_Man1::
	lock
	faceplayer
	call_if_eq VAR_SLATEPORT_CITY_STATE, 1, SlateportCity_EventScript_Man1SternInterview
	msgbox SlateportCity_Text_EveryoneCallsHimCaptStern, MSGBOX_DEFAULT
	release
	end

SlateportCity_EventScript_Man1SternInterview::
	msgbox SlateportCity_Text_CaptainsACelebrity, MSGBOX_DEFAULT
	release
	end

SlateportCity_EventScript_Woman1::
	lock
	faceplayer
	goto_if_set FLAG_DOCK_REJECTED_DEVON_GOODS, SlateportCity_EventScript_Woman1AquaGone
	msgbox SlateportCity_Text_WhatsLongLineOverThere, MSGBOX_DEFAULT
	release
	end

SlateportCity_EventScript_Woman1AquaGone::
	msgbox SlateportCity_Text_VisitedMuseumOften, MSGBOX_DEFAULT
	release
	end

SlateportCity_EventScript_BattleTentSign::
	msgbox SlateportCity_Text_BattleTentSign, MSGBOX_SIGN
	end

SlateportCity_EventScript_SternsShipyardSign::
	lockall
	goto_if_set FLAG_SYS_GAME_CLEAR, SlateportCity_EventScript_SternsShipyardFerryComplete
	goto_if_set FLAG_BADGE07_GET, SlateportCity_EventScript_SternsShipyardNearsCompletion
	msgbox SlateportCity_Text_SternsShipyardWantedSign, MSGBOX_DEFAULT
	releaseall
	end

SlateportCity_EventScript_SternsShipyardNearsCompletion::
	msgbox SlateportCity_Text_SternsShipyardNearsCompletion, MSGBOX_DEFAULT
	releaseall
	end

SlateportCity_EventScript_SternsShipyardFerryComplete::
	msgbox SlateportCity_Text_SternsShipyardFerryComplete, MSGBOX_DEFAULT
	releaseall
	end

SlateportCity_EventScript_PokemonFanClubSign::
	msgbox SlateportCity_Text_PokemonFanClubSign, MSGBOX_SIGN
	end

SlateportCity_EventScript_OceanicMuseumSign::
	msgbox SlateportCity_Text_OceanicMuseumSign, MSGBOX_SIGN
	end

SlateportCity_EventScript_CitySign::
	msgbox SlateportCity_Text_CitySign, MSGBOX_SIGN
	end

SlateportCity_EventScript_MarketSign::
	msgbox SlateportCity_Text_MarketSign, MSGBOX_SIGN
	end

SlateportCity_EventScript_HarborSign::
	lockall
	goto_if_set FLAG_SYS_GAME_CLEAR, SlateportCity_EventScript_HarborSignFerryComplete
	msgbox SlateportCity_Text_HarborFerryUnderConstruction, MSGBOX_DEFAULT
	releaseall
	end

SlateportCity_EventScript_HarborSignFerryComplete::
	msgbox SlateportCity_Text_HarborSign, MSGBOX_DEFAULT
	releaseall
	end

SlateportCity_EventScript_NameRatersHouseSign::
	msgbox SlateportCity_Text_NameRatersHouseSign, MSGBOX_SIGN
	end

SlateportCity_EventScript_Maniac::
	lock
	faceplayer
	call_if_eq VAR_SLATEPORT_CITY_STATE, 1, SlateportCity_EventScript_ManiacSternInterview
	msgbox SlateportCity_Text_GetNameRaterToHelpYou, MSGBOX_DEFAULT
	release
	end

@ Unclear if the text here was meant to be different, but its not
SlateportCity_EventScript_ManiacSternInterview::
	msgbox SlateportCity_Text_GetNameRaterToHelpYou, MSGBOX_DEFAULT
	release
	end

SlateportCity_EventScript_Woman2::
	msgbox SlateportCity_Text_CantChangeTradeMonName, MSGBOX_NPC
	end

SlateportCity_EventScript_Sailor1::
	msgbox SlateportCity_Text_SeaIsSoWet, MSGBOX_NPC
	end

SlateportCity_EventScript_Sailor2::
	msgbox SlateportCity_Text_SinkOldBoats, MSGBOX_NPC
	end

SlateportCity_EventScript_PokefanF::
	msgbox SlateportCity_Text_BuyTooMuch, MSGBOX_NPC
	end

SlateportCity_EventScript_Man2::
	msgbox SlateportCity_Text_BattleTentBuiltRecently, MSGBOX_NPC
	end

SlateportCity_EventScript_AquaGrunt1::
	lock
	faceplayer
	msgbox SlateportCity_Text_QuitPushing, MSGBOX_DEFAULT
	closemessage
	applymovement LOCALID_SLATEPORT_GRUNT_1, Common_Movement_FaceOriginalDirection
	waitmovement 0
	release
	end

SlateportCity_EventScript_AquaGrunt2::
	lock
	faceplayer
	msgbox SlateportCity_Text_AquaHasPolicy, MSGBOX_DEFAULT
	closemessage
	applymovement LOCALID_SLATEPORT_GRUNT_2, Common_Movement_FaceOriginalDirection
	waitmovement 0
	release
	end

SlateportCity_EventScript_AquaGrunt3::
	lock
	faceplayer
	msgbox SlateportCity_Text_BossIsBrilliant, MSGBOX_DEFAULT
	closemessage
	applymovement LOCALID_SLATEPORT_GRUNT_3, Common_Movement_FaceOriginalDirection
	waitmovement 0
	release
	end

SlateportCity_EventScript_AquaGrunt4::
	lock
	faceplayer
	msgbox SlateportCity_Text_WhatsNewSchemeIWonder, MSGBOX_DEFAULT
	closemessage
	applymovement LOCALID_SLATEPORT_GRUNT_4, Common_Movement_FaceOriginalDirection
	waitmovement 0
	release
	end

SlateportCity_EventScript_AquaGrunt5::
	lock
	faceplayer
	msgbox SlateportCity_Text_ShouldTakeItAll, MSGBOX_DEFAULT
	closemessage
	applymovement LOCALID_SLATEPORT_GRUNT_5, Common_Movement_FaceOriginalDirection
	waitmovement 0
	release
	end

SlateportCity_EventScript_AquaGrunt6::
	lock
	faceplayer
	msgbox SlateportCity_Text_DontButtIn, MSGBOX_DEFAULT
	closemessage
	applymovement LOCALID_SLATEPORT_GRUNT_6, Common_Movement_FaceOriginalDirection
	waitmovement 0
	release
	end

SlateportCity_EventScript_AquaGrunt7::
	lock
	faceplayer
	msgbox SlateportCity_Text_RemindsMeOfLongLineForGames, MSGBOX_DEFAULT
	closemessage
	applymovement LOCALID_SLATEPORT_GRUNT_7, Common_Movement_FaceOriginalDirection
	waitmovement 0
	release
	end

SlateportCity_EventScript_AquaGrunt8::
	lock
	faceplayer
	msgbox SlateportCity_Text_WhyAreWeLiningUp, MSGBOX_DEFAULT
	closemessage
	applymovement LOCALID_SLATEPORT_GRUNT_8, Common_Movement_FaceOriginalDirection
	waitmovement 0
	release
	end

SlateportCity_EventScript_AquaGrunt9::
	lock
	faceplayer
	playse SE_PIN
	applymovement LOCALID_SLATEPORT_GRUNT_9, Common_Movement_ExclamationMark
	waitmovement 0
	applymovement LOCALID_SLATEPORT_GRUNT_9, Common_Movement_Delay48
	waitmovement 0
	msgbox SlateportCity_Text_WhatDoYouWant, MSGBOX_DEFAULT
	closemessage
	applymovement LOCALID_SLATEPORT_GRUNT_9, Common_Movement_FaceOriginalDirection
	waitmovement 0
	applymovement LOCALID_SLATEPORT_GRUNT_9, SlateportCity_Movement_DelayAquaGrunt
	waitmovement 0
	applymovement LOCALID_SLATEPORT_GRUNT_9, Common_Movement_FacePlayer
	waitmovement 0
	msgbox SlateportCity_Text_IllReadSignForYou, MSGBOX_DEFAULT
	closemessage
	applymovement LOCALID_SLATEPORT_GRUNT_9, Common_Movement_FaceOriginalDirection
	waitmovement 0
	applymovement LOCALID_SLATEPORT_GRUNT_9, SlateportCity_Movement_DelayAquaGrunt
	waitmovement 0
	msgbox SlateportCity_Text_SaysSomethingLikeSeaIsEndless, MSGBOX_DEFAULT
	closemessage
	applymovement LOCALID_SLATEPORT_GRUNT_9, Common_Movement_FacePlayer
	waitmovement 0
	applymovement LOCALID_SLATEPORT_GRUNT_9, SlateportCity_Movement_DelayAquaGrunt
	waitmovement 0
	applymovement LOCALID_SLATEPORT_GRUNT_9, Common_Movement_FaceOriginalDirection
	waitmovement 0
	release
	end

SlateportCity_Movement_DelayAquaGrunt:
	delay_16
	delay_16
	step_end

SlateportCity_EventScript_AquaGrunt10::
	msgbox SlateportCity_Text_ShouldveBroughtMyGameBoy, MSGBOX_SIGN
	end

SlateportCity_EventScript_AquaGrunt11::
	lock
	faceplayer
	msgbox SlateportCity_Text_HotSpringsAfterOperation, MSGBOX_DEFAULT
	closemessage
	applymovement LOCALID_SLATEPORT_GRUNT_11, Common_Movement_FaceOriginalDirection
	waitmovement 0
	release
	end

SlateportCity_EventScript_DollClerk::
	lock
	faceplayer
	message gText_HowMayIServeYou
	waitmessage
	pokemartdecoration SlateportCity_PokemartDecor_Dolls
	msgbox gText_PleaseComeAgain, MSGBOX_DEFAULT
	release
	end

	.align 2
SlateportCity_PokemartDecor_Dolls:
	.2byte DECOR_AZURILL_DOLL
	.2byte DECOR_MARILL_DOLL
	.2byte DECOR_SKITTY_DOLL
	pokemartlistend

SlateportCity_EventScript_ComeBackWithSecretPower::
	msgbox gText_ComeBackWithSecretPower, MSGBOX_DEFAULT
	release
	end

SlateportCity_EventScript_DecorClerk::
	lock
	faceplayer
	goto_if_unset FLAG_RECEIVED_SECRET_POWER, SlateportCity_EventScript_ComeBackWithSecretPower
	message gText_HowMayIServeYou
	waitmessage
	pokemartdecoration SlateportCity_PokemartDecor
	msgbox gText_PleaseComeAgain, MSGBOX_DEFAULT
	release
	end

	.align 2
SlateportCity_PokemartDecor:
	.2byte DECOR_RED_BRICK
	.2byte DECOR_BLUE_BRICK
	.2byte DECOR_YELLOW_BRICK
	.2byte DECOR_RED_BALLOON
	.2byte DECOR_BLUE_BALLOON
	.2byte DECOR_YELLOW_BALLOON
	.2byte DECOR_C_LOW_NOTE_MAT
	.2byte DECOR_D_NOTE_MAT
	.2byte DECOR_E_NOTE_MAT
	.2byte DECOR_F_NOTE_MAT
	.2byte DECOR_G_NOTE_MAT
	.2byte DECOR_A_NOTE_MAT
	.2byte DECOR_B_NOTE_MAT
	.2byte DECOR_C_HIGH_NOTE_MAT
	pokemartlistend

SlateportCity_EventScript_PowerTMClerk::
	lock
	faceplayer
	message gText_HowMayIServeYou
	waitmessage
	pokemart SlateportCity_Pokemart_PowerTMs
	msgbox gText_PleaseComeAgain, MSGBOX_DEFAULT
	release
	end

	.align 2
SlateportCity_Pokemart_PowerTMs:
	.2byte ITEM_TM_HIDDEN_POWER
	.2byte ITEM_TM_SECRET_POWER
	pokemartlistend

@ Scene with Capt Sterns interview and Team Aqua announcing plans to steal Submarine
SlateportCity_EventScript_CaptStern::
	lockall
	msgbox SlateportCity_Text_SternMoveAheadWithExploration, MSGBOX_DEFAULT
	msgbox SlateportCity_Text_GabbyWonderfulThanksForInterview, MSGBOX_DEFAULT
	closemessage
	applymovement LOCALID_SLATEPORT_GABBY, Common_Movement_WalkInPlaceFasterRight
	waitmovement 0
	delay 10
	applymovement LOCALID_SLATEPORT_TY, Common_Movement_WalkInPlaceFasterDown
	waitmovement 0
	delay 25
	applymovement LOCALID_SLATEPORT_CAPT_STERN, SlateportCity_Movement_SternWatchGabbyAndTyExit
	applymovement LOCALID_PLAYER, SlateportCity_Movement_PlayerFaceStern
	applymovement LOCALID_SLATEPORT_GABBY, SlateportCity_Movement_GabbyExit
	applymovement LOCALID_SLATEPORT_TY, SlateportCity_Movement_TyExit
	waitmovement 0
	removeobject LOCALID_SLATEPORT_GABBY
	removeobject LOCALID_SLATEPORT_TY
	msgbox SlateportCity_Text_SternWhewFirstInterview, MSGBOX_DEFAULT
	applymovement LOCALID_SLATEPORT_CAPT_STERN, Common_Movement_WalkInPlaceFasterUp
	waitmovement 0
	msgbox SlateportCity_Text_OhPlayerWeMadeDiscovery, MSGBOX_DEFAULT
	playbgm MUS_ENCOUNTER_AQUA, FALSE
	msgbox SlateportCity_Text_AquaWillAssumeControlOfSubmarine, MSGBOX_DEFAULT
	applymovement LOCALID_SLATEPORT_COOK, Common_Movement_WalkInPlaceFasterLeft
	applymovement LOCALID_SLATEPORT_FAT_MAN, Common_Movement_WalkInPlaceFasterLeft
	applymovement LOCALID_SLATEPORT_OLD_WOMAN, SlateportCity_Movement_OldWomanConcern
	applymovement LOCALID_SLATEPORT_RICH_BOY, Common_Movement_QuestionMark
	applymovement LOCALID_SLATEPORT_MAN_1, SlateportCity_Movement_ManConcern
	waitmovement 0
	applymovement LOCALID_SLATEPORT_CAPT_STERN, Common_Movement_WalkInPlaceFasterDown
	waitmovement 0
	msgbox SlateportCity_Text_SternWhatWasAllThat, MSGBOX_DEFAULT
	playse SE_PIN
	applymovement LOCALID_SLATEPORT_CAPT_STERN, Common_Movement_ExclamationMark
	waitmovement 0
	applymovement LOCALID_SLATEPORT_CAPT_STERN, Common_Movement_Delay48
	waitmovement 0
	applymovement LOCALID_SLATEPORT_CAPT_STERN, Common_Movement_WalkInPlaceFasterUp
	waitmovement 0
	msgbox SlateportCity_Text_FromHarborTryingToTakeSub, MSGBOX_DEFAULT
	msgbox SlateportCity_Text_PleaseComeWithMe, MSGBOX_DEFAULT
	closemessage
	applymovement LOCALID_SLATEPORT_CAPT_STERN, SlateportCity_Movement_SternEnterHarbor
	applymovement LOCALID_PLAYER, SlateportCity_Movement_PlayerEnterHarbor
	waitmovement 0
	removeobject LOCALID_SLATEPORT_CAPT_STERN
	clearflag FLAG_HIDE_SLATEPORT_CITY_HARBOR_CAPTAIN_STERN
	clearflag FLAG_HIDE_SLATEPORT_CITY_HARBOR_SUBMARINE_SHADOW
	clearflag FLAG_HIDE_SLATEPORT_CITY_HARBOR_AQUA_GRUNT
	clearflag FLAG_HIDE_SLATEPORT_CITY_HARBOR_ARCHIE
	setvar VAR_SLATEPORT_CITY_STATE, 2
	warp MAP_SLATEPORT_CITY_HARBOR, 11, 14
	waitstate
	releaseall
	end

SlateportCity_Movement_OldWomanConcern:
	delay_16
	delay_16
	emote_question_mark
	walk_in_place_faster_right
	delay_16
	delay_16
	walk_in_place_faster_left
	step_end

SlateportCity_Movement_ManConcern:
	emote_question_mark
	walk_in_place_faster_up
	delay_16
	walk_in_place_faster_down
	delay_16
	delay_16
	walk_in_place_faster_left
	step_end

SlateportCity_Movement_GabbyExit:
	delay_16
	walk_left
	walk_left
	walk_down
	walk_left
	walk_left
	walk_left
	walk_left
	walk_left
	walk_left
	walk_left
	walk_left
	step_end

SlateportCity_Movement_TyExit:
	walk_down
	walk_left
	walk_left
	walk_left
	walk_down
	walk_left
	walk_left
	walk_left
	walk_left
	walk_left
	walk_left
	walk_left
	walk_left
	step_end

SlateportCity_Movement_Unused:
	walk_down
	walk_in_place_faster_up
	step_end

SlateportCity_Movement_SternEnterHarbor:
	walk_right
	walk_up
	walk_up
	set_invisible
	step_end

SlateportCity_Movement_SternWatchGabbyAndTyExit:
	delay_16
	delay_16
	delay_16
	delay_16
	delay_16
	walk_down
	walk_left
	step_end

SlateportCity_Movement_PlayerEnterHarbor:
	walk_in_place_faster_right
	delay_16
	delay_16
	walk_right
	walk_up
	step_end

SlateportCity_Movement_PlayerFaceStern:
	delay_16
	delay_16
	delay_16
	delay_16
	delay_16
	delay_16
	delay_16
	walk_in_place_faster_down
	step_end

SlateportCity_EventScript_Ty::
	msgbox SlateportCity_Text_BigSmileForCamera, MSGBOX_SIGN
	end

SlateportCity_EventScript_Gabby::
	msgbox SlateportCity_Text_MostInvaluableExperience, MSGBOX_SIGN
	end

SlateportCity_EventScript_Man3::
	msgbox SlateportCity_Text_WonderIfLighthouseStartlesPokemon, MSGBOX_NPC
	end

SlateportCity_EventScript_BerryPowderClerk::
	lock
	faceplayer
	goto_if_set FLAG_RECEIVED_POWDER_JAR, SlateportCity_EventScript_ReceivedPowderJar
	msgbox SlateportCity_Text_ExplainBerries, MSGBOX_DEFAULT
	giveitem ITEM_POWDER_JAR
	setflag FLAG_RECEIVED_POWDER_JAR
	msgbox SlateportCity_Text_ExplainBerryPowder, MSGBOX_DEFAULT
	release
	end

SlateportCity_EventScript_ReceivedPowderJar::
	setvar VAR_0x8004, 1
	specialvar VAR_RESULT, HasEnoughBerryPowder
	goto_if_eq VAR_RESULT, FALSE, SlateportCity_EventScript_ExplainBerryPowder
	msgbox SlateportCity_Text_BroughtMeSomeBerryPowder, MSGBOX_DEFAULT
	special DisplayBerryPowderVendorMenu
	goto SlateportCity_EventScript_ChooseBerryPowderItem
	end

SlateportCity_EventScript_ExplainBerryPowder::
	msgbox SlateportCity_Text_ExplainBerryPowder, MSGBOX_DEFAULT
	release
	end

SlateportCity_EventScript_ChooseBerryPowderItem::
	message SlateportCity_Text_ExchangeWhatWithIt
	waitmessage
	setvar VAR_0x8004, SCROLL_MULTI_BERRY_POWDER_VENDOR
	special ShowScrollableMultichoice
	waitstate
	switch VAR_RESULT
	case 0, SlateportCity_EventScript_EnergyPowder
	case 1, SlateportCity_EventScript_EnergyRoot
	case 2, SlateportCity_EventScript_HealPowder
	case 3, SlateportCity_EventScript_RevivalHerb
	case 4, SlateportCity_EventScript_Protein
	case 5, SlateportCity_EventScript_Iron
	case 6, SlateportCity_EventScript_Carbos
	case 7, SlateportCity_EventScript_Calcium
	case 8, SlateportCity_EventScript_Zinc
	case 9, SlateportCity_EventScript_HPUp
	case 10, SlateportCity_EventScript_PPUp
	case 11, SlateportCity_EventScript_CancelPowderItemSelect
	case MULTI_B_PRESSED, SlateportCity_EventScript_CancelPowderItemSelect
	end

SlateportCity_EventScript_EnergyPowder::
	bufferitemname STR_VAR_1, ITEM_ENERGY_POWDER
	setvar VAR_0x8008, ITEM_ENERGY_POWDER
	setvar VAR_0x8009, 50
	goto SlateportCity_EventScript_TryBuyBerryPowderItem
	end

SlateportCity_EventScript_EnergyRoot::
	bufferitemname STR_VAR_1, ITEM_ENERGY_ROOT
	setvar VAR_0x8008, ITEM_ENERGY_ROOT
	setvar VAR_0x8009, 80
	goto SlateportCity_EventScript_TryBuyBerryPowderItem
	end

SlateportCity_EventScript_HealPowder::
	bufferitemname STR_VAR_1, ITEM_HEAL_POWDER
	setvar VAR_0x8008, ITEM_HEAL_POWDER
	setvar VAR_0x8009, 50
	goto SlateportCity_EventScript_TryBuyBerryPowderItem
	end

SlateportCity_EventScript_RevivalHerb::
	bufferitemname STR_VAR_1, ITEM_REVIVAL_HERB
	setvar VAR_0x8008, ITEM_REVIVAL_HERB
	setvar VAR_0x8009, 300
	goto SlateportCity_EventScript_TryBuyBerryPowderItem
	end

SlateportCity_EventScript_Protein::
	bufferitemname STR_VAR_1, ITEM_PROTEIN
	setvar VAR_0x8008, ITEM_PROTEIN
	setvar VAR_0x8009, 1000
	goto SlateportCity_EventScript_TryBuyBerryPowderItem
	end

SlateportCity_EventScript_Iron::
	bufferitemname STR_VAR_1, ITEM_IRON
	setvar VAR_0x8008, ITEM_IRON
	setvar VAR_0x8009, 1000
	goto SlateportCity_EventScript_TryBuyBerryPowderItem
	end

SlateportCity_EventScript_Carbos::
	bufferitemname STR_VAR_1, ITEM_CARBOS
	setvar VAR_0x8008, ITEM_CARBOS
	setvar VAR_0x8009, 1000
	goto SlateportCity_EventScript_TryBuyBerryPowderItem
	end

SlateportCity_EventScript_Calcium::
	bufferitemname STR_VAR_1, ITEM_CALCIUM
	setvar VAR_0x8008, ITEM_CALCIUM
	setvar VAR_0x8009, 1000
	goto SlateportCity_EventScript_TryBuyBerryPowderItem
	end

SlateportCity_EventScript_Zinc::
	bufferitemname STR_VAR_1, ITEM_ZINC
	setvar VAR_0x8008, ITEM_ZINC
	setvar VAR_0x8009, 1000
	goto SlateportCity_EventScript_TryBuyBerryPowderItem
	end

SlateportCity_EventScript_HPUp::
	bufferitemname STR_VAR_1, ITEM_HP_UP
	setvar VAR_0x8008, ITEM_HP_UP
	setvar VAR_0x8009, 1000
	goto SlateportCity_EventScript_TryBuyBerryPowderItem
	end

SlateportCity_EventScript_PPUp::
	bufferitemname STR_VAR_1, ITEM_PP_UP
	setvar VAR_0x8008, ITEM_PP_UP
	setvar VAR_0x8009, 3000
	goto SlateportCity_EventScript_TryBuyBerryPowderItem
	end

SlateportCity_EventScript_CancelPowderItemSelect::
	msgbox SlateportCity_Text_ComeBackToTradeBerryPowder, MSGBOX_DEFAULT
	special RemoveBerryPowderVendorMenu
	release
	end

SlateportCity_EventScript_TryBuyBerryPowderItem::
	msgbox SlateportCity_Text_ExchangeBerryPowderForItem, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, SlateportCity_EventScript_ChooseBerryPowderItem
	copyvar VAR_0x8004, VAR_0x8009
	specialvar VAR_RESULT, HasEnoughBerryPowder
	goto_if_eq VAR_RESULT, FALSE, SlateportCity_EventScript_NotEnoughBerryPowder
	giveitem VAR_0x8008
	goto_if_eq VAR_RESULT, FALSE, SlateportCity_EventScript_NoRoomForBerryPowderItem
	copyvar VAR_0x8004, VAR_0x8009
	special TakeBerryPowder
	special PrintPlayerBerryPowderAmount
	msgbox SlateportCity_Text_FineBerryPowderTradeSomethingElse, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, YES, SlateportCity_EventScript_ChooseBerryPowderItem
	msgbox SlateportCity_Text_WhenYouGetMoreBringItToMe, MSGBOX_DEFAULT
	special RemoveBerryPowderVendorMenu
	release
	end

SlateportCity_EventScript_NoRoomForBerryPowderItem::
	msgbox gText_TheBagIsFull, MSGBOX_DEFAULT
	special RemoveBerryPowderVendorMenu
	release
	end

SlateportCity_EventScript_NotEnoughBerryPowder::
	msgbox SlateportCity_Text_DontHaveEnoughBerryPowder, MSGBOX_DEFAULT
	goto SlateportCity_EventScript_ChooseBerryPowderItem
	end

SlateportCity_EventScript_ScottBattleTentScene::
	lockall
	applymovement LOCALID_PLAYER, Common_Movement_FaceUp
	waitmovement 0
	opendoor 10, 12
	waitdooranim
	addobject LOCALID_SLATEPORT_SCOTT
	applymovement LOCALID_PLAYER, SlateportCity_Movement_PushPlayerDown
	applymovement LOCALID_SLATEPORT_SCOTT, SlateportCity_Movement_ScottExitBattleTent
	waitmovement 0
	closedoor 10, 12
	waitdooranim
	msgbox SlateportCity_Text_TakingBattleTentChallenge, MSGBOX_DEFAULT
	closemessage
	applymovement LOCALID_PLAYER, SlateportCity_Movement_PlayerWatchScottExit
	applymovement LOCALID_SLATEPORT_SCOTT, SlateportCity_Movement_ScottExitAfterBattleTent
	waitmovement 0
	removeobject LOCALID_SLATEPORT_SCOTT
	addvar VAR_SCOTT_STATE, 1
	setvar VAR_SLATEPORT_OUTSIDE_MUSEUM_STATE, 3
	releaseall
	end

SlateportCity_Movement_PushPlayerDown:
	lock_facing_direction
	walk_down
	unlock_facing_direction
	step_end

SlateportCity_Movement_PlayerWatchScottExit:
	delay_16
	walk_in_place_faster_right
	step_end

SlateportCity_Movement_ScottExitBattleTent:
	delay_8
	walk_down
	step_end

SlateportCity_Movement_ScottExitAfterBattleTent:
	walk_right
	walk_right
	walk_right
	walk_right
	walk_right
	walk_right
	walk_right
	walk_right
	step_end

SlateportCity_EventScript_BerryCrushRankingsSign::
	lockall
	special ShowBerryCrushRankings
	waitstate
	releaseall
	end

SlateportCity_Text_EnergyGuruSellWhatYouNeed:
	.string "I'm the ENERGY GURU!\p"
	.string "I sell what you need!\p"
	.string "Vitamins, positive vibes and a 12-week\n"
	.string "course.$"

SlateportCity_Text_OhYourPokemon:
	.string "Oh? Your {STR_VAR_1}…$"

SlateportCity_Text_PleaseGiveItThisEffortRibbon:
	.string "It trained like an absolute animal!\p"
	.string "Here, give it this EFFORT RIBBON.\n"
	.string "Participation trophies are for losers.$"

SlateportCity_Text_ReceivedEffortRibbon:
	.string "{PLAYER} received the EFFORT RIBBON.$"

SlateportCity_Text_PutEffortRibbonOnMon:
	.string "{PLAYER} put the EFFORT RIBBON on\n"
	.string "{STR_VAR_1}.$"

SlateportCity_Text_GoForItLittleHarder:
	.string "Hmm. It's a bit soft. Go grind some more.\p"
	.string "Come back with a beast, and I'll give it\n"
	.string "something nice.$"

SlateportCity_Text_EffortRibbonLooksGoodOnIt:
	.string "Your {STR_VAR_1} still wears that EFFORT\n"
	.string "RIBBON! Gains, baby!$"

SlateportCity_Text_WonderIfLighthouseStartlesPokemon:
	.string "I'm building a personal brand around\n"
	.string "mindful productivity.\p"
	.string "I've been here eight months. The WiFi\n"
	.string "doesn't work. I haven't worked.$"

SlateportCity_Text_SeaweedFullOfLife:
	.string "Look at this seaweed!\p"
	.string "Fresh and full of life.\p"
	.string "It just bit me.$"

SlateportCity_Text_HowTownIsBornAndGrows:
	.string "Where water is clean, harvests gather.\p"
	.string "Where people gather, a market starts.\p"
	.string "Where a market starts, remote workers\n"
	.string "show up with laptops.$"

SlateportCity_Text_SlateportWonderfulPlace:
	.string "Shopping with the scent of the ocean…\p"
	.string "SLATEPORT is wonderful!\p"
	.string "The fish market next door helps with\n"
	.string "the scent.$"

SlateportCity_Text_BuyBricksSoDecorWontGetDirty:
	.string "If you put DOLLS or CUSHIONS on the\n"
	.string "floor, they get dirty.\p"
	.string "So I'm buying BRICKS to put them on.\p"
	.string "My mom says that's not how bricks work.\n"
	.string "My mom is not an interior designer.$"

SlateportCity_Text_GoingToCompeteInBattleTent:
	.string "Wroooar! I'm entering the BATTLE TENT!\p"
	.string "But first, I need to catch some\n"
	.string "POKéMON!\p"
	.string "And learn what a POKéMON is.$"

SlateportCity_Text_BushedHikingFromMauville:
	.string "Whew… I'm bushed…\p"
	.string "I walked from MAUVILLE. This city is\n"
	.string "huge.\p"
	.string "Should've brought my BIKE. Or my\n"
	.string "scooter. Or a car.$"

SlateportCity_Text_EveryoneCallsHimCaptStern:
	.string "STERN built the MUSEUM and leads an\n"
	.string "undersea team.\p"
	.string "So everyone calls him CAPT. STERN.\p"
	.string "He's never had a boat license.$"

SlateportCity_Text_WhatsLongLineOverThere:
	.string "What's that long line over there?\p"
	.string "Free sparkling water? I'm in.$"

SlateportCity_Text_VisitedMuseumOften:
	.string "As a kid, I went to the MUSEUM every\n"
	.string "week.\p"
	.string "I dreamt about the mysteries of the\n"
	.string "sea. Now I sell fish at the market. The\l"
	.string "sea won.$"

SlateportCity_Text_QuitPushing:
	.string "Hey! Quit pushing!\p"
	.string "This is the line for free PERRIER!$"

SlateportCity_Text_AquaHasPolicy:
	.string "TEAM AQUA assembles and disperses at\n"
	.string "the operation site.\p"
	.string "Bring your own bottle.$"

SlateportCity_Text_BossIsBrilliant:
	.string "Our BOSS is brilliant.\p"
	.string "Why would he want a MUSEUM? Unless it\n"
	.string "has a mineral spring.$"

SlateportCity_Text_WhatsNewSchemeIWonder:
	.string "What's the new scheme?\p"
	.string "Last time the BOSS got mad, somebody\n"
	.string "brought SPA BLAUW. Still water.\p"
	.string "He's still not over it.$"

SlateportCity_Text_ShouldTakeItAll:
	.string "If there's something we need in the\n"
	.string "MUSEUM, take it all!\p"
	.string "Especially the water cooler.$"

SlateportCity_Text_DontButtIn:
	.string "Hey! Don't butt in!\p"
	.string "I've been waiting for my CHAUDFONTAINE\n"
	.string "all day!$"

SlateportCity_Text_RemindsMeOfLongLineForGames:
	.string "A long line?\p"
	.string "Reminds me of queuing for\n"
	.string "limited-edition SAN PELLEGRINO\l"
	.string "flavors.$"

SlateportCity_Text_WhyAreWeLiningUp:
	.string "Why are we lining up and paying? We\n"
	.string "should just march in!\p"
	.string "And drink everything.$"

SlateportCity_Text_WhatDoYouWant:
	.string "What? What do you want?\p"
	.string "Still or sparkling?\p"
	.string "Wrong answer.$"

SlateportCity_Text_IllReadSignForYou:
	.string "You want to read this sign? I'll read it\n"
	.string "for you!\p"
	.string "It says: “BUY AQUA SPARKLING WATER.”\p"
	.string "…What? It totally says that.$"

SlateportCity_Text_SaysSomethingLikeSeaIsEndless:
	.string "Let's see…\p"
	.string "I think it says “the bubbles in the sea\n"
	.string "are endless.”\p"
	.string "Yup, pretty sure.$"

SlateportCity_Text_ShouldveBroughtMyGameBoy:
	.string "Grumble…\p"
	.string "Should've brought my Game Boy Advance.\n"
	.string "And a six-pack of SOURCY.$"

SlateportCity_Text_HotSpringsAfterOperation:
	.string "After this operation, the BOSS is\n"
	.string "taking us to a mineral spring spa!\p"
	.string "Natural bubbles!$"

SlateportCity_Text_SeaIsSoWet:
	.string "The sea is so vast…\p"
	.string "Could it be made of POKéMON tears?\p"
	.string "That would explain the salt.$"

SlateportCity_Text_SinkOldBoats:
	.string "Old ships get sunk so POKéMON can live\n"
	.string "in them.\p"
	.string "My ex-wife did that to my boat.$"

SlateportCity_Text_BuyTooMuch:
	.string "Every time I come here, I buy too much.\p"
	.string "I came for milk. I have a kayak now.$"

SlateportCity_Text_GetNameRaterToHelpYou:
	.string "Want to rename your POKéMON?\p"
	.string "The NAME RATER does it.\p"
	.string "He'll judge you, though. Hard.$"

SlateportCity_Text_CantChangeTradeMonName:
	.string "You can't rename a traded POKéMON.\p"
	.string "The original TRAINER's love is in the\n"
	.string "name.\p"
	.string "Even if the name is “POOPFACE.”$"

SlateportCity_Text_BattleTentBuiltRecently:
	.string "I'm a digital nomad. I help brands unlock\n"
	.string "their authentic synergy.\p"
	.string "What that means? I post pictures of my\n"
	.string "laptop on the beach.$"

SlateportCity_Text_CaptSternBeingInterviewed:
	.string "I hoped it was a famous star so I could\n"
	.string "get an autograph.\p"
	.string "But it's just CAPT. STERN. Boo. I want my\n"
	.string "money back.$"

SlateportCity_Text_InterviewerSoCool:
	.string "That lady interviewer is so cool.\p"
	.string "When I grow up, I'm going to be an\n"
	.string "international journalist! Or an\l"
	.string "influencer. Same thing.$"

SlateportCity_Text_SternSaysDiscoveredSomething:
	.string "CAPT. STERN says they found something\n"
	.string "at the bottom of the sea.\p"
	.string "A treasure? A monster? A really big\n"
	.string "shoe?$"

SlateportCity_Text_CaptainComeBackWithBigFish:
	.string "What's going on? Did the CAPTAIN catch\n"
	.string "a big fish?\p"
	.string "How much per kilo?$"

SlateportCity_Text_AmIOnTV:
	.string "Hey! Mom! Am I on TV?! Mom?!$"

SlateportCity_Text_CaptainsACelebrity:
	.string "A TV interview! Here! In SLATEPORT!\n"
	.string "Somebody hold my fish!$"

SlateportCity_Text_BigSmileForCamera:
	.string "TY: Okay, CAPT. STERN, big smile for the\n"
	.string "camera!$"

SlateportCity_Text_MostInvaluableExperience:
	.string "GABBY: I see, I see. What a most\n"
	.string "invaluable experience…$"

SlateportCity_Text_SternMoveAheadWithExploration:
	.string "CAPT. STERN: Yes, indeed. We'll keep\n"
	.string "exploring.$"

SlateportCity_Text_GabbyWonderfulThanksForInterview:
	.string "GABBY: Wonderful, CAPT. STERN! Thank\n"
	.string "you for your time.\p"
	.string "We hope to interview you again when you\n"
	.string "find more stuff!$"

SlateportCity_Text_SternWhewFirstInterview:
	.string "CAPT. STERN: Whew…\p"
	.string "My first time on TV. I sweated through\n"
	.string "three shirts.$"

SlateportCity_Text_OhPlayerWeMadeDiscovery:
	.string "Oh! {PLAYER}{KUN}! You're looking great!\p"
	.string "We made a huge discovery on our last\n"
	.string "dive.\p"
	.string "An underwater cavern on ROUTE 128!\p"
	.string "We think a POKéMON lives there that was\n"
	.string "believed to be extinct for ages.$"

SlateportCity_Text_AquaWillAssumeControlOfSubmarine:
	.string "Fufufu… CAPT. STERN, I presume.\p"
	.string "TEAM AQUA is hereby acquiring your\n"
	.string "submarine!\p"
	.string "Your objections are meaningless!\n"
	.string "Consider it a hostile takeover!\p"
	.string "Fufufu… Watch and learn what TEAM AQUA\n"
	.string "has planned!$"

SlateportCity_Text_SternWhatWasAllThat:
	.string "CAPT. STERN: What was that?\p"
	.string "Someone with a megaphone… Where did it\n"
	.string "come from?$"

SlateportCity_Text_FromHarborTryingToTakeSub:
	.string "It's from the HARBOR! They're stealing\n"
	.string "my submarine!$"

SlateportCity_Text_PleaseComeWithMe:
	.string "{PLAYER}{KUN}! Please, come with me!$"

SlateportCity_Text_BattleTentSign:
	.string "BATTLE TENT SLATEPORT SITE\n"
	.string "“Find it! The ultimate POKéMON!”$"

SlateportCity_Text_SternsShipyardWantedSign:
	.string "STERN'S SHIPYARD\p"
	.string "“Wanted: a sailor capable of sailing in\n"
	.string "all currents. Unpaid internship.”$"

SlateportCity_Text_SternsShipyardNearsCompletion:
	.string "STERN'S SHIPYARD\p"
	.string "“The ferry S.S. TIDAL is almost done.\n"
	.string "Slateport to Lilycove, no refunds.”$"

SlateportCity_Text_SternsShipyardFerryComplete:
	.string "STERN'S SHIPYARD\p"
	.string "“Boarding for the S.S. TIDAL is at the\n"
	.string "HARBOR. Seasickness bags not\l"
	.string "included.”$"

SlateportCity_Text_PokemonFanClubSign:
	.string "POKéMON FAN CLUB\n"
	.string "“Calling all fans of POKéMON! Lanyards\l"
	.string "mandatory.”$"

SlateportCity_Text_OceanicMuseumSign:
	.string "“The endless sea sustains all life.\n"
	.string "Bubbles sold separately.”\p"
	.string "OCEANIC MUSEUM$"

SlateportCity_Text_CitySign:
	.string "SLATEPORT CITY\p"
	.string "“The port where people, POKéMON and\n"
	.string "remote workers cross paths.”$"

SlateportCity_Text_MarketSign:
	.string "SLATEPORT MARKET\n"
	.string "“Unique items found nowhere else!\l"
	.string "Returns found nowhere either.”$"

SlateportCity_Text_HarborFerryUnderConstruction:
	.string "SLATEPORT HARBOR\p"
	.string "“The ferry S.S. TIDAL is still being\n"
	.string "built in the SHIPYARD.\p"
	.string "“Service starts soon. Probably. Ask\n"
	.string "DOCK.”$"

SlateportCity_Text_HarborSign:
	.string "SLATEPORT HARBOR\p"
	.string "“Enjoy a delightful cruise on the S.S.\n"
	.string "TIDAL. Now with 30% less vomit!”$"

SlateportCity_Text_NameRatersHouseSign:
	.string "NAME RATER'S HOUSE\n"
	.string "“POKéMON nicknames rated. Honestly.\l"
	.string "Brace yourself.”$"

SlateportCity_Text_ExplainBerries:
	.string "When wild POKéMON get hurt, they chew\n"
	.string "on BERRIES to heal.\p"
	.string "Did you know that?\p"
	.string "Someone saw that and thought:\n"
	.string "“Medicine!”\p"
	.string "Did you know that?\p"
	.string "To make medicine, you have to crush\n"
	.string "BERRIES into powder.\p"
	.string "Did you know that?\p"
	.string "You look like a BERRY fan! I've got\n"
	.string "something for you.\p"
	.string "Did you know that? You didn't. I just\n"
	.string "told you.$"

SlateportCity_Text_ExplainBerryPowder:
	.string "I had BERRY CRUSH machines installed at\n"
	.string "POKéMON CENTERS.\p"
	.string "They're at the DIRECT CORNER upstairs.\p"
	.string "Did you know?\p"
	.string "Could you make BERRY POWDER for me with\n"
	.string "those?\p"
	.string "Bring me lots, and I'll make you all kinds\n"
	.string "of medicine. Totally legal. Did you know?$"

SlateportCity_Text_BroughtMeSomeBerryPowder:
	.string "Did you bring me some BERRY POWDER? Did\n"
	.string "you know I was waiting?$"

SlateportCity_Text_ExchangeWhatWithIt:
	.string "What would you like in exchange?$"

SlateportCity_Text_ExchangeBerryPowderForItem:
	.string "So, your BERRY POWDER for one {STR_VAR_1}?$"

SlateportCity_Text_DontHaveEnoughBerryPowder:
	.string "Oh, dear. Not enough BERRY POWDER. Did\n"
	.string "you know that?$"

SlateportCity_Text_FineBerryPowderTradeSomethingElse:
	.string "Ooh, fine powder. This will make\n"
	.string "excellent medicine.\p"
	.string "Want to trade more BERRY POWDER for\n"
	.string "something else?$"

SlateportCity_Text_WhenYouGetMoreBringItToMe:
	.string "Okay! Bring me more BERRY POWDER when\n"
	.string "you have it!$"

SlateportCity_Text_ComeBackToTradeBerryPowder:
	.string "Come back to trade BERRY POWDER for\n"
	.string "medicine.\p"
	.string "I'm always running my bazaar here.\p"
	.string "Did you know? Now you do.$"

SlateportCity_Text_YouDroveTeamAquaAway:
	.string "SCOTT: It's me! Your rival! …No. It's\n"
	.string "SCOTT. I borrowed the clothes. They\l"
	.string "don't know yet.\p"
	.string "TEAM AQUA ran away from you. I saw\n"
	.string "everything. I always see everything.$"

SlateportCity_Text_MaybeThisTrainer:
	.string "SCOTT: Hmm… You smell like PETALBURG.$"

SlateportCity_Text_LetsRegisterEachOther:
	.string "SCOTT: Let's register each other in our\n"
	.string "POKéNAVS. I already had your number.\l"
	.string "This just makes it official.\p"
	.string "… … … … … …$"

SlateportCity_Text_RegisteredScott:
	.string "Registered this SCOTT person in the\n"
	.string "POKéNAV. He was already in there.$"

SlateportCity_Text_KeepEyeOnTrainersBeSeeingYou:
	.string "SCOTT: I'd love to follow you around.\p"
	.string "…I mean, I won't. Be seeing you, {PLAYER}{KUN}.$"

SlateportCity_Text_TakingBattleTentChallenge:
	.string "SCOTT: The BATTLE TENT! I'll be\n"
	.string "watching. You won't know from where.$"

@ Project Grounded: Scott is steeds vermomd. Hier als je rivaal.
SlateportCity_EventScript_SetScottDisguise::
	setvar VAR_OBJ_GFX_ID_0, OBJ_EVENT_GFX_RIVAL_MAY_NORMAL
	checkplayergender
	call_if_eq VAR_RESULT, FEMALE, SlateportCity_EventScript_SetScottDisguiseFemale
	return

SlateportCity_EventScript_SetScottDisguiseFemale::
	setvar VAR_OBJ_GFX_ID_0, OBJ_EVENT_GFX_RIVAL_BRENDAN_NORMAL
	return

@ Project Grounded: strandman die maar één vraag stelt.
SlateportCity_EventScript_SpitOrSwallow::
	lock
	faceplayer
	goto_if_set FLAG_RECEIVED_SPIT_SWALLOW_MON, SlateportCity_EventScript_SpitOrSwallowNice
	getpartysize
	goto_if_eq VAR_RESULT, PARTY_SIZE, SlateportCity_EventScript_SpitOrSwallowAsk
	message SlateportCity_Text_SpitOrSwallow
	waitmessage
	dynmultichoice 21, 6, TRUE, 2, 0, DYN_MULTICHOICE_CB_NONE, SlateportCity_Text_Spit, SlateportCity_Text_Swallow
	goto_if_eq VAR_RESULT, 1, SlateportCity_EventScript_Swallow
	givemon SPECIES_SILICOBRA, 10, item=ITEM_NONE, abilityNum=0, move1=MOVE_SPIT_UP, move2=MOVE_STOCKPILE, move3=MOVE_NONE, move4=MOVE_NONE
	bufferspeciesname STR_VAR_1, SPECIES_SILICOBRA
	goto SlateportCity_EventScript_SpitOrSwallowReceived

SlateportCity_EventScript_Swallow::
	givemon SPECIES_CRAMORANT, 10, item=ITEM_NONE, move1=MOVE_STOCKPILE, move2=MOVE_SWALLOW, move3=MOVE_NONE, move4=MOVE_NONE
	bufferspeciesname STR_VAR_1, SPECIES_CRAMORANT
SlateportCity_EventScript_SpitOrSwallowReceived::
	playfanfare MUS_OBTAIN_ITEM
	message SlateportCity_Text_ReceivedSpitOrSwallowMon
	waitmessage
	waitfanfare
	setflag FLAG_RECEIVED_SPIT_SWALLOW_MON
SlateportCity_EventScript_SpitOrSwallowNice::
	msgbox SlateportCity_Text_Nice, MSGBOX_DEFAULT
	release
	end

@ Volle party: hij stelt alleen de vraag, zonder keuzemenu.
SlateportCity_EventScript_SpitOrSwallowAsk::
	msgbox SlateportCity_Text_SpitOrSwallow, MSGBOX_DEFAULT
	release
	end

SlateportCity_Text_SpitOrSwallow:
	.string "Spit or swallow?$"

SlateportCity_Text_Spit:
	.string "SPIT$"

SlateportCity_Text_Swallow:
	.string "SWALLOW$"

SlateportCity_Text_ReceivedSpitOrSwallowMon:
	.string "{PLAYER} received a {STR_VAR_1}!$"

SlateportCity_Text_Nice:
	.string "Nice.$"

@ Project Grounded: Prof. Oak staat bij de vuurtoren naar zee te kijken. Gevecht, daarna een Kanto-starter naar keuze.
SlateportCity_EventScript_ProfOak::
	lock
	faceplayer
	goto_if_set FLAG_RECEIVED_OAK_STARTER, SlateportCity_EventScript_ProfOakDone
	goto_if_defeated TRAINER_PROF_OAK, SlateportCity_EventScript_ProfOakGiveStarter
	msgbox SlateportCity_Text_ProfOakIntro, MSGBOX_DEFAULT
	trainerbattle_no_intro TRAINER_PROF_OAK, SlateportCity_Text_ProfOakDefeat
	goto SlateportCity_EventScript_ProfOakGiveStarter
	end

SlateportCity_EventScript_ProfOakGiveStarter::
	msgbox SlateportCity_Text_ProfOakOfferStarter, MSGBOX_DEFAULT
	dynmultichoice 18, 4, TRUE, 3, 0, DYN_MULTICHOICE_CB_NONE, SlateportCity_Text_OakBulbasaur, SlateportCity_Text_OakCharmander, SlateportCity_Text_OakSquirtle
	switch VAR_RESULT
	case 0, SlateportCity_EventScript_ProfOakGiveBulbasaur
	case 1, SlateportCity_EventScript_ProfOakGiveCharmander
	case 2, SlateportCity_EventScript_ProfOakGiveSquirtle
	goto SlateportCity_EventScript_ProfOakGiveBulbasaur
	end

SlateportCity_EventScript_ProfOakGiveBulbasaur::
	setvar VAR_TEMP_1, SPECIES_BULBASAUR
	goto SlateportCity_EventScript_ProfOakGiveMon
	end

SlateportCity_EventScript_ProfOakGiveCharmander::
	setvar VAR_TEMP_1, SPECIES_CHARMANDER
	goto SlateportCity_EventScript_ProfOakGiveMon
	end

SlateportCity_EventScript_ProfOakGiveSquirtle::
	setvar VAR_TEMP_1, SPECIES_SQUIRTLE
	goto SlateportCity_EventScript_ProfOakGiveMon
	end

SlateportCity_EventScript_ProfOakGiveMon::
	bufferspeciesname STR_VAR_1, VAR_TEMP_1
	givemon VAR_TEMP_1, 15
	goto_if_eq VAR_RESULT, MON_CANT_GIVE, Common_EventScript_NoMoreRoomForPokemon
	playfanfare MUS_OBTAIN_ITEM
	message SlateportCity_Text_ProfOakReceivedStarter
	waitmessage
	waitfanfare
	goto_if_eq VAR_RESULT, MON_GIVEN_TO_PC, SlateportCity_EventScript_ProfOakStarterToPC
	goto SlateportCity_EventScript_ProfOakStarterGiven
	end

SlateportCity_EventScript_ProfOakStarterToPC::
	call Common_EventScript_TransferredToPC
	goto SlateportCity_EventScript_ProfOakStarterGiven
	end

SlateportCity_EventScript_ProfOakStarterGiven::
	setflag FLAG_RECEIVED_OAK_STARTER
	msgbox SlateportCity_Text_ProfOakAfterStarter, MSGBOX_DEFAULT
	applymovement LOCALID_SLATEPORT_PROF_OAK, Common_Movement_FaceRight
	waitmovement 0
	release
	end

SlateportCity_EventScript_ProfOakDone::
	msgbox SlateportCity_Text_ProfOakDone, MSGBOX_DEFAULT
	applymovement LOCALID_SLATEPORT_PROF_OAK, Common_Movement_FaceRight
	waitmovement 0
	release
	end

SlateportCity_Text_ProfOakIntro:
	.string "OAK: …The sea. Hoenn's sea.\n"
	.string "It's wetter than Kanto's.\p"
	.string "I'm on vacation. My grandson kept\n"
	.string "calling me, so I dropped my phone\l"
	.string "off the S.S. Anne. On purpose.\p"
	.string "Hm? Are you a boy or a girl?\p"
	.string "…Never mind. I stopped asking\n"
	.string "in 1996. It never helped.\p"
	.string "Let's see what Hoenn's kids are\n"
	.string "made of. Kanto style!$"

SlateportCity_Text_ProfOakDefeat:
	.string "Well! My Tauros hasn't lost\n"
	.string "since the Gold and Silver beta.$"

SlateportCity_Text_ProfOakOfferStarter:
	.string "OAK: Here. Take one of these.\p"
	.string "I've carried them around since\n"
	.string "the nineties. They keep asking when\l"
	.string "they get to evolve.\p"
	.string "I never know what to tell them.\n"
	.string "Pick one. Quickly, before I get\l"
	.string "sentimental.$"

SlateportCity_Text_OakBulbasaur:
	.string "BULBASAUR$"

SlateportCity_Text_OakCharmander:
	.string "CHARMANDER$"

SlateportCity_Text_OakSquirtle:
	.string "SQUIRTLE$"

SlateportCity_Text_ProfOakReceivedStarter:
	.string "{PLAYER} received {STR_VAR_1}!$"

SlateportCity_Text_ProfOakAfterStarter:
	.string "OAK: Raise it well.\n"
	.string "Or don't. I'm on vacation.$"

SlateportCity_Text_ProfOakDone:
	.string "OAK: The sea is calming.\n"
	.string "Unlike my grandson.\p"
	.string "Smell ya later, as he says.\n"
	.string "Every. Single. Time.$"

@ Project Grounded: Victory-gauntlet (post-game), uitdager Vernon. Zie LibertyGarden/scripts.inc.
SlateportCity_EventScript_VictoryChallengerVernon::
	goto_if_unset FLAG_SYS_GAME_CLEAR, SlateportCity_EventScript_VictoryChallengerVernonNotYet
	trainerbattle_single TRAINER_VICTORY_VERNON, SlateportCity_Text_VictoryVernonIntro, SlateportCity_Text_VictoryVernonDefeat, SlateportCity_EventScript_VictoryChallengerVernonStamp
	msgbox SlateportCity_Text_VictoryVernonPost, MSGBOX_AUTOCLOSE
	end

SlateportCity_EventScript_VictoryChallengerVernonNotYet::
	msgbox SlateportCity_Text_VictoryVernonNotYet, MSGBOX_NPC
	end

SlateportCity_EventScript_VictoryChallengerVernonStamp::
	call VictoryGauntlet_EventScript_GiveStamp
	release
	end

SlateportCity_Text_VictoryVernonNotYet:
	.string "CHAMPIONS only, peasant.\p"
	.string "I had my butler check your net worth.\n"
	.string "It's mostly POTIONS.$"

SlateportCity_Text_VictoryVernonIntro:
	.string "Victory? I bought mine. Three times,\n"
	.string "actually. Volume discount.\p"
	.string "Let's see if yours is on sale.$"

SlateportCity_Text_VictoryVernonDefeat:
	.string "Impossible! I paid for this outcome!$"

SlateportCity_Text_VictoryVernonPost:
	.string "You'll be hearing from my lawyer.\p"
	.string "He's a PERSIAN. He bills by the scratch.$"
