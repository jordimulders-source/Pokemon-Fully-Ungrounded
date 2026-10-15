Route104_MrBrineysHouse_MapScripts::
	map_script MAP_SCRIPT_ON_TRANSITION, Route104_MrBrineysHouse_OnTransition
	.byte 0

Route104_MrBrineysHouse_OnTransition:
	setflag FLAG_LANDMARK_MR_BRINEY_HOUSE
	call_if_eq VAR_BRINEY_HOUSE_STATE, 1, Route104_MrBrineysHouse_EventScript_SetBrineyPeekoPos
	call_if_set FLAG_RECEIVED_POKENAV, Route104_MrBrineysHouse_EventScript_HideRustboroRival
	end

Route104_MrBrineysHouse_EventScript_HideRustboroRival::
	setflag FLAG_HIDE_RUSTBORO_CITY_RIVAL
	return

Route104_MrBrineysHouse_EventScript_SetBrineyPeekoPos::
	setobjectxyperm LOCALID_BRINEYS_HOUSE_BRINEY, 9, 3
	setobjectmovementtype LOCALID_BRINEYS_HOUSE_BRINEY, MOVEMENT_TYPE_WALK_SEQUENCE_DOWN_LEFT_UP_RIGHT
	setobjectxyperm LOCALID_BRINEYS_HOUSE_PEEKO, 9, 6
	setobjectmovementtype LOCALID_BRINEYS_HOUSE_PEEKO, MOVEMENT_TYPE_WALK_SEQUENCE_LEFT_UP_RIGHT_DOWN
	return

Route104_MrBrineysHouse_EventScript_Briney::
	lock
	faceplayer
	setvar VAR_0x8004, 0 @ Project Grounded: Keldeo-eiland (UnchartedIsle/scripts.inc)
	call EventScript_BrineyKeldeoTrip
	call_if_unset FLAG_MR_BRINEY_SAILING_INTRO, Route104_MrBrineysHouse_EventScript_SailingIntro
	goto_if_unset FLAG_DELIVERED_STEVEN_LETTER, Route104_MrBrineysHouse_EventScript_SailBothDeliveries
	goto_if_unset FLAG_DELIVERED_DEVON_GOODS, Route104_MrBrineysHouse_EventScript_SailDeliverPackage
	goto Route104_MrBrineysHouse_EventScript_WhereAreWeBound
	end

Route104_MrBrineysHouse_EventScript_SailingIntro::
	setflag FLAG_MR_BRINEY_SAILING_INTRO
	msgbox Route104_MrBrineysHouse_Text_WaitUpPeeko, MSGBOX_DEFAULT
	msgbox Route104_MrBrineysHouse_Text_ItsYouLetsSailToDewford, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, Route104_MrBrineysHouse_EventScript_DeclineDeliverySailing
	goto Route104_MrBrineysHouse_EventScript_SailToDewford
	end

Route104_MrBrineysHouse_EventScript_WhereAreWeBound::
	message Route104_MrBrineysHouse_Text_WhereAreWeBound
	waitmessage
Route104_MrBrineysHouse_EventScript_ChooseDestination::
	multichoicedefault 20, 6, MULTI_BRINEY_HOUSE, 2, FALSE
	switch VAR_RESULT
	case 0, Route104_MrBrineysHouse_EventScript_SailToDewford
	case 1, Route104_MrBrineysHouse_EventScript_SailToSlateport
	case 2, Route104_MrBrineysHouse_EventScript_DeclineSailing
	case MULTI_B_PRESSED, Route104_MrBrineysHouse_EventScript_DeclineSailing
	end

@ Project Grounded: na de brief in Dewford vaart Briney ook direct naar Slateport (zonder animatie,
@ zie "bootreis zonder animatie" in CLAUDE.md). Eindtoestand = die van Dewford -> Slateport.
Route104_MrBrineysHouse_EventScript_SailToSlateport::
	goto_if_unset FLAG_DELIVERED_DEVON_GOODS, Route104_MrBrineysHouse_EventScript_SlateportGoodsText
	msgbox Route104_MrBrineysHouse_Text_SetSailForSlateport, MSGBOX_DEFAULT
	goto Route104_MrBrineysHouse_EventScript_DoSailToSlateport
	end

Route104_MrBrineysHouse_EventScript_SlateportGoodsText::
	msgbox Route104_MrBrineysHouse_Text_SetSailForSlateportGoods, MSGBOX_DEFAULT
Route104_MrBrineysHouse_EventScript_DoSailToSlateport::
	closemessage
	setflag FLAG_HIDE_ROUTE_104_MR_BRINEY
	setflag FLAG_HIDE_ROUTE_104_MR_BRINEY_BOAT
	setflag FLAG_HIDE_BRINEYS_HOUSE_MR_BRINEY
	setflag FLAG_HIDE_BRINEYS_HOUSE_PEEKO
	setflag FLAG_HIDE_MR_BRINEY_DEWFORD_TOWN
	setflag FLAG_HIDE_MR_BRINEY_BOAT_DEWFORD_TOWN
	clearflag FLAG_HIDE_ROUTE_109_MR_BRINEY
	clearflag FLAG_HIDE_ROUTE_109_MR_BRINEY_BOAT
	call_if_ne VAR_BRINEY_LOCATION, 0, Route104_MrBrineysHouse_EventScript_SetLocationRoute109
	fadescreen FADE_TO_BLACK
	applymovement LOCALID_PLAYER, Common_Movement_FaceDown
	waitmovement 0
	playse SE_M_SURF
	delay 40
	warpsilent MAP_ROUTE109, 21, 23
	waitstate
	releaseall
	end

Route104_MrBrineysHouse_EventScript_SetLocationRoute109::
	setvar VAR_BRINEY_LOCATION, 3
	return

Route104_MrBrineysHouse_EventScript_SailBothDeliveries::
	msgbox Route104_MrBrineysHouse_Text_NeedToMakeDeliveriesSailToDewford, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, Route104_MrBrineysHouse_EventScript_DeclineDeliverySailing
	goto Route104_MrBrineysHouse_EventScript_SailToDewford
	end

Route104_MrBrineysHouse_EventScript_SailDeliverPackage::
	message Route104_MrBrineysHouse_Text_NeedToDeliverPackageSailToDewford
	waitmessage
	goto Route104_MrBrineysHouse_EventScript_ChooseDestination
	end

Route104_MrBrineysHouse_EventScript_DeclineDeliverySailing::
	msgbox Route104_MrBrineysHouse_Text_DeclineDeliverySail, MSGBOX_DEFAULT
	release
	end

Route104_MrBrineysHouse_EventScript_DeclineSailing::
	msgbox Route104_MrBrineysHouse_Text_TellMeWheneverYouWantToSail, MSGBOX_DEFAULT
	release
	end

Route104_MrBrineysHouse_EventScript_SailToDewford::
	msgbox Route104_MrBrineysHouse_Text_SetSailForDewford, MSGBOX_DEFAULT
	call EventScript_BackupMrBrineyLocation
	setvar VAR_BOARD_BRINEY_BOAT_STATE, 1
	clearflag FLAG_HIDE_ROUTE_104_MR_BRINEY
	setflag FLAG_HIDE_BRINEYS_HOUSE_MR_BRINEY
	setflag FLAG_HIDE_BRINEYS_HOUSE_PEEKO
	setvar VAR_RUSTBORO_CITY_STATE, 8
	setvar VAR_ROUTE104_STATE, 2
	setflag FLAG_HIDE_RUSTBORO_CITY_RIVAL
	setflag FLAG_HIDE_ROUTE_104_RIVAL
	warp MAP_ROUTE104, 13, 51
	waitstate
	releaseall
	end

Route104_MrBrineysHouse_EventScript_Peeko::
	lock
	faceplayer
	waitse
	playmoncry SPECIES_WINGULL, CRY_MODE_NORMAL
	msgbox Route104_MrBrineysHouse_Text_Peeko, MSGBOX_DEFAULT
	waitmoncry
	release
	end

Route104_MrBrineysHouse_Text_WaitUpPeeko:
	.string "MR. BRINEY: Hold on, lass! Wait up,\n"
	.string "PEEKO!$"

Route104_MrBrineysHouse_Text_ItsYouLetsSailToDewford:
	.string "Hm? {PLAYER}{KUN}! You saved my darling\n"
	.string "PEEKO!\p"
	.string "You want to sail with me?\p"
	.string "A LETTER for DEWFORD and a package for\n"
	.string "SLATEPORT?\p"
	.string "Busy life for a kid!\p"
	.string "No problem. I'm your man! We sail for\n"
	.string "DEWFORD.$"

Route104_MrBrineysHouse_Text_SetSailForDewford:
	.string "MR. BRINEY: DEWFORD it is!\p"
	.string "Anchors aweigh! PEEKO, my darling, we're\n"
	.string "off!$"

Route104_MrBrineysHouse_Text_DeclineDeliverySail:
	.string "MR. BRINEY: Your deliveries can wait?\p"
	.string "Just tell me whenever you want to sail!$"

Route104_MrBrineysHouse_Text_NeedToMakeDeliveriesSailToDewford:
	.string "MR. BRINEY: Ahoy! I know what you want!\p"
	.string "A LETTER to DEWFORD and a package to\n"
	.string "SLATEPORT.\p"
	.string "No problem! I'm the man for the job!\p"
	.string "First, DEWFORD.$"

Route104_MrBrineysHouse_Text_NeedToDeliverPackageSailToDewford:
	.string "MR. BRINEY: Ahoy! I know what you want!\p"
	.string "A package for CAPT. STERN in SLATEPORT.\p"
	.string "No problem! I'm the man for the job!\p"
	.string "Straight there, or via DEWFORD?$"

Route104_MrBrineysHouse_Text_SetSailForSlateport:
	.string "MR. BRINEY: SLATEPORT, nonstop!\p"
	.string "PEEKO, hold on to your feathers.\n"
	.string "We're skipping the scenic route.$"

Route104_MrBrineysHouse_Text_SetSailForSlateportGoods:
	.string "MR. BRINEY: SLATEPORT, nonstop!\p"
	.string "Hand CAPT. STERN his package before it\n"
	.string "starts ticking. Or smelling.$"

Route104_MrBrineysHouse_Text_WhereAreWeBound:
	.string "MR. BRINEY: Ahoy! For you, I'll sail\n"
	.string "anytime!\p"
	.string "Where are we bound?$"

Route104_MrBrineysHouse_Text_TellMeWheneverYouWantToSail:
	.string "MR. BRINEY: PEEKO owes you her life.\p"
	.string "Just tell me when you want to sail!$"

Route104_MrBrineysHouse_Text_Peeko:
	.string "PEEKO: Pii piihyoro!$"

