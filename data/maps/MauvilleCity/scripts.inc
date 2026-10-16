MauvilleCity_MapScripts::
	map_script MAP_SCRIPT_ON_TRANSITION, MauvilleCity_OnTransition
	.byte 0

MauvilleCity_OnTransition:
	setvar VAR_0x8004, 0
	call Common_EventScript_SickBlikDevSpawn  @ SickBlik als developer (post-game, dagrotatie)
	setflag FLAG_VISITED_MAUVILLE_CITY
	clearflag FLAG_FORCE_MIRAGE_TOWER_VISIBLE
	clearflag FLAG_HIDE_SLATEPORT_MUSEUM_POPULATION
	setflag FLAG_SYS_TV_START
	clearflag FLAG_MAUVILLE_GYM_BARRIERS_STATE
	setvar VAR_MAUVILLE_GYM_STATE, 0
	call_if_set FLAG_GOT_TM_THUNDERBOLT_FROM_WATTSON, MauvilleCity_EventScript_MoveWattsonBackToGym
	call MauvilleCity_EventScript_SetColressVisibility
	end

MauvilleCity_EventScript_MoveWattsonBackToGym::
	clearflag FLAG_HIDE_MAUVILLE_GYM_WATTSON
	setflag FLAG_HIDE_MAUVILLE_CITY_WATTSON
	setflag FLAG_WATTSON_REMATCH_AVAILABLE
	return

MauvilleCity_EventScript_Boy::
	msgbox MauvilleCity_Text_NurseHurtMonBackToHealth, MSGBOX_NPC
	end

MauvilleCity_EventScript_Maniac::
	msgbox MauvilleCity_Text_AllSortsOfPeopleComeThrough, MSGBOX_NPC
	end

MauvilleCity_EventScript_Woman::
	msgbox MauvilleCity_Text_RydelVeryGenerous, MSGBOX_NPC
	end

@ Project Grounded: eenmalige item-giveaway (testrun Jordi)
MauvilleCity_EventScript_RichBoy::
	lock
	faceplayer
	msgbox MauvilleCity_Text_PokemonCanJumpYouOnBike, MSGBOX_DEFAULT
	goto_if_set FLAG_RECEIVED_MAUVILLE_RICH_BOY_GIFT, MauvilleCity_EventScript_RichBoy_GiftDone
	msgbox MauvilleCity_Text_TakeExpertBelt, MSGBOX_DEFAULT
	giveitem ITEM_EXPERT_BELT
	goto_if_eq VAR_RESULT, FALSE, Common_EventScript_ShowBagIsFull
	setflag FLAG_RECEIVED_MAUVILLE_RICH_BOY_GIFT
MauvilleCity_EventScript_RichBoy_GiftDone::
	release
	end

MauvilleCity_EventScript_CitySign::
	msgbox MauvilleCity_Text_CitySign, MSGBOX_SIGN
	end

MauvilleCity_EventScript_GymSign::
	msgbox MauvilleCity_Text_GymSign, MSGBOX_SIGN
	end

MauvilleCity_EventScript_BikeShopSign::
	msgbox MauvilleCity_Text_BikeShopSign, MSGBOX_SIGN
	end

MauvilleCity_EventScript_GameCornerSign::
	msgbox MauvilleCity_Text_GameCornerSign, MSGBOX_SIGN
	end

MauvilleCity_EventScript_SchoolKidM::
	lock
	faceplayer
	goto_if_set FLAG_TV_EXPLAINED, MauvilleCity_EventScript_TVExplained
	msgbox MauvilleCity_Text_ExplainTV, MSGBOX_DEFAULT
	setflag FLAG_TV_EXPLAINED
	release
	end

MauvilleCity_EventScript_TVExplained::
	msgbox MauvilleCity_Text_BeenCheckingOutTV, MSGBOX_DEFAULT
	release
	end

MauvilleCity_EventScript_WallysUncle::
	lock
	faceplayer
	goto_if_set FLAG_DECLINED_WALLY_BATTLE_MAUVILLE, MauvilleCity_EventScript_UncleAskPlayerToBattleWally
	msgbox MauvilleCity_Text_UncleHesTooPeppy, MSGBOX_DEFAULT
	closemessage
	applymovement LOCALID_MAUVILLE_WALLYS_UNCLE, Common_Movement_FaceOriginalDirection
	waitmovement 0
	release
	end

MauvilleCity_EventScript_UncleAskPlayerToBattleWally::
	msgbox MauvilleCity_Text_UncleCanYouBattleWally, MSGBOX_DEFAULT
	closemessage
	applymovement LOCALID_MAUVILLE_WALLYS_UNCLE, Common_Movement_FaceOriginalDirection
	waitmovement 0
	release
	end

MauvilleCity_EventScript_Wally::
	lockall
	goto_if_set FLAG_DECLINED_WALLY_BATTLE_MAUVILLE, MauvilleCity_EventScript_WallyRequestBattleAgain
	applymovement LOCALID_MAUVILLE_WALLY, Common_Movement_WalkInPlaceFasterRight
	waitmovement 0
	msgbox MauvilleCity_Text_WallyWantToChallengeGym, MSGBOX_DEFAULT
	msgbox MauvilleCity_Text_UncleYourePushingIt, MSGBOX_DEFAULT
	msgbox MauvilleCity_Text_WallyWeCanBeatAnyone, MSGBOX_DEFAULT
	applymovement LOCALID_MAUVILLE_WALLY, Common_Movement_FacePlayer
	waitmovement 0
	playse SE_PIN
	applymovement LOCALID_MAUVILLE_WALLY, Common_Movement_ExclamationMark
	waitmovement 0
	applymovement LOCALID_MAUVILLE_WALLY, Common_Movement_Delay48
	waitmovement 0
	msgbox MauvilleCity_Text_WallyWillYouBattleMe, MSGBOX_YESNO
	goto MauvilleCity_EventScript_BattleWallyPrompt
	end

MauvilleCity_EventScript_BattleWallyPrompt::
	call_if_eq VAR_RESULT, YES, MauvilleCity_EventScript_BattleWally
	goto_if_eq VAR_RESULT, NO, MauvilleCity_EventScript_DeclineWallyBattle
	closemessage
	switch VAR_FACING
	case DIR_NORTH, MauvilleCity_EventScript_WallyAndUncleExitNorth
	case DIR_EAST, MauvilleCity_EventScript_WallyAndUncleExitEast
	end

MauvilleCity_EventScript_WallyAndUncleExitNorth::
	applymovement LOCALID_PLAYER, MauvilleCity_Movement_PlayerWatchWallyExitNorth1
	applymovement LOCALID_MAUVILLE_WALLY, MauvilleCity_Movement_WallyExitNorth1
	applymovement LOCALID_MAUVILLE_WALLYS_UNCLE, MauvilleCity_Movement_WallysUncleExitNorth1
	waitmovement 0
	applymovement LOCALID_MAUVILLE_WALLY, Common_Movement_WalkInPlaceFasterRight
	waitmovement 0
	delay 30
	applymovement LOCALID_PLAYER, MauvilleCity_Movement_PlayerFaceUncleNorth
	applymovement LOCALID_MAUVILLE_WALLYS_UNCLE, MauvilleCity_Movement_WallysUncleApproachPlayerNorth
	waitmovement 0
	msgbox MauvilleCity_Text_UncleVisitUsSometime, MSGBOX_DEFAULT
	closemessage
	applymovement LOCALID_PLAYER, MauvilleCity_Movement_PlayerWatchWallyExitNorth2
	applymovement LOCALID_MAUVILLE_WALLYS_UNCLE, MauvilleCity_Movement_WallysUncleExitNorth2
	applymovement LOCALID_MAUVILLE_WALLY, MauvilleCity_Movement_WallyExitNorth2
	waitmovement 0
	goto MauvilleCity_EventScript_DefeatedWally
	end

MauvilleCity_EventScript_WallyAndUncleExitEast::
	applymovement LOCALID_PLAYER, MauvilleCity_Movement_PlayerWatchWallyExitEast1
	applymovement LOCALID_MAUVILLE_WALLY, MauvilleCity_Movement_WallyExitEast1
	applymovement LOCALID_MAUVILLE_WALLYS_UNCLE, MauvilleCity_Movement_WallysUncleExitEast1
	waitmovement 0
	applymovement LOCALID_MAUVILLE_WALLY, Common_Movement_WalkInPlaceFasterRight
	waitmovement 0
	delay 30
	applymovement LOCALID_MAUVILLE_WALLYS_UNCLE, MauvilleCity_Movement_WallysUncleApproachPlayerEast
	waitmovement 0
	msgbox MauvilleCity_Text_UncleVisitUsSometime, MSGBOX_DEFAULT
	closemessage
	applymovement LOCALID_PLAYER, MauvilleCity_Movement_PlayerWatchWallyExitEast2
	applymovement LOCALID_MAUVILLE_WALLYS_UNCLE, MauvilleCity_Movement_WallysUncleExitEast2
	applymovement LOCALID_MAUVILLE_WALLY, MauvilleCity_Movement_WallyExitEast2
	waitmovement 0
	goto MauvilleCity_EventScript_DefeatedWally
	end

MauvilleCity_EventScript_DefeatedWally::
	removeobject LOCALID_MAUVILLE_WALLY
	removeobject LOCALID_MAUVILLE_WALLYS_UNCLE
	clearflag FLAG_HIDE_VERDANTURF_TOWN_WANDAS_HOUSE_WALLY
	clearflag FLAG_HIDE_VERDANTURF_TOWN_WANDAS_HOUSE_WALLYS_UNCLE
	setflag FLAG_DEFEATED_WALLY_MAUVILLE
	setvar VAR_WALLY_CALL_STEP_COUNTER, 0
	setflag FLAG_ENABLE_FIRST_WALLY_POKENAV_CALL
	call_if_eq VAR_FACING, DIR_NORTH, MauvilleCity_EventScript_ScottApproachPlayerNorth
	call_if_eq VAR_FACING, DIR_EAST, MauvilleCity_EventScript_ScottApproachPlayerEast
	applymovement LOCALID_PLAYER, Common_Movement_WalkInPlaceFasterDown
	waitmovement 0
	msgbox MauvilleCity_Text_ScottYouDidntHoldBack, MSGBOX_DEFAULT
	closemessage
	addvar VAR_SCOTT_STATE, 1
	call_if_eq VAR_FACING, DIR_NORTH, MauvilleCity_EventScript_ScottExitNorth
	call_if_eq VAR_FACING, DIR_EAST, MauvilleCity_EventScript_ScottExitEast
	removeobject LOCALID_MAUVILLE_SCOTT
	releaseall
	end

MauvilleCity_EventScript_ScottApproachPlayerNorth::
	addobject LOCALID_MAUVILLE_SCOTT
	applymovement LOCALID_MAUVILLE_SCOTT, MauvilleCity_Movement_ScottApproachPlayerNorth
	waitmovement 0
	return

MauvilleCity_EventScript_ScottApproachPlayerEast::
	setobjectxyperm LOCALID_MAUVILLE_SCOTT, 12, 13
	addobject LOCALID_MAUVILLE_SCOTT
	applymovement LOCALID_MAUVILLE_SCOTT, MauvilleCity_Movement_ScottApproachPlayerEast
	waitmovement 0
	return

MauvilleCity_EventScript_ScottExitNorth::
	applymovement LOCALID_PLAYER, MauvilleCity_Movement_PlayerWatchScottExitNorth
	applymovement LOCALID_MAUVILLE_SCOTT, MauvilleCity_Movement_ScottExitNorth
	waitmovement 0
	return

MauvilleCity_EventScript_ScottExitEast::
	applymovement LOCALID_PLAYER, MauvilleCity_Movement_PlayerWatchScottExitEast
	applymovement LOCALID_MAUVILLE_SCOTT, MauvilleCity_Movement_ScottExitEast
	waitmovement 0
	return

MauvilleCity_EventScript_BattleWally::
	msgbox MauvilleCity_Text_WallyHereICome, MSGBOX_DEFAULT
	trainerbattle_no_intro TRAINER_WALLY_MAUVILLE, MauvilleCity_Text_WallyDefeat
	applymovement LOCALID_MAUVILLE_WALLY, Common_Movement_WalkInPlaceFasterRight
	waitmovement 0
	msgbox MauvilleCity_Text_WallyIllGoBackToVerdanturf, MSGBOX_DEFAULT
	applymovement LOCALID_MAUVILLE_WALLY, Common_Movement_FacePlayer
	waitmovement 0
	msgbox MauvilleCity_Text_ThankYouNotEnoughToBattle, MSGBOX_DEFAULT
	applymovement LOCALID_MAUVILLE_WALLY, Common_Movement_WalkInPlaceFasterRight
	waitmovement 0
	msgbox MauvilleCity_Text_UncleNoNeedToBeDown, MSGBOX_DEFAULT
	return

MauvilleCity_EventScript_DeclineWallyBattle::
	setflag FLAG_DECLINED_WALLY_BATTLE_MAUVILLE
	msgbox MauvilleCity_Text_WallyMyUncleWontKnowImStrong, MSGBOX_DEFAULT
	release
	end

MauvilleCity_EventScript_WallyRequestBattleAgain::
	applymovement LOCALID_MAUVILLE_WALLY, Common_Movement_FacePlayer
	waitmovement 0
	msgbox MauvilleCity_Text_WallyPleaseBattleMe, MSGBOX_YESNO
	goto MauvilleCity_EventScript_BattleWallyPrompt
	end

MauvilleCity_Movement_WallyExitNorth1:
	walk_left
	walk_left
	walk_down
	walk_down
	walk_left
	step_end

MauvilleCity_Movement_WallyExitEast1:
	walk_down
	walk_down
	walk_left
	walk_left
	walk_left
	step_end

MauvilleCity_Movement_WallyExitNorth2:
	delay_16
	delay_16
	walk_left
	walk_left
	walk_left
	walk_left
	walk_left
	walk_left
	walk_left
	walk_left
	delay_8
	step_end

MauvilleCity_Movement_WallyExitEast2:
	delay_16
	delay_16
	walk_left
	walk_left
	walk_left
	walk_left
	walk_left
	walk_left
	walk_left
	walk_left
	delay_8
	step_end

MauvilleCity_Movement_PlayerWatchWallyExitNorth2:
	delay_16
	delay_8
	walk_in_place_faster_left
	step_end

MauvilleCity_Movement_PlayerWatchWallyExitEast2:
	delay_16
	delay_16
	delay_16
	walk_in_place_faster_left
	step_end

MauvilleCity_Movement_PlayerWatchScottExitNorth:
	delay_16
	walk_in_place_faster_left
	step_end

MauvilleCity_Movement_PlayerWatchScottExitEast:
	delay_16
	delay_16
	walk_in_place_faster_left
	step_end

MauvilleCity_Movement_PlayerWatchWallyExitEast1:
	delay_16
	walk_in_place_faster_down
	step_end

MauvilleCity_Movement_PlayerWatchWallyExitNorth1:
	delay_16
	walk_in_place_faster_left
	step_end

MauvilleCity_Movement_WallysUncleExitNorth1:
	walk_left
	walk_left
	walk_left
	walk_down
	walk_down
	step_end

MauvilleCity_Movement_WallysUncleExitEast1:
	walk_left
	walk_down
	walk_down
	walk_left
	walk_left
	step_end

MauvilleCity_Movement_PlayerFaceUncleNorth:
	delay_16
	delay_8
	delay_4
	walk_in_place_faster_down
	step_end

MauvilleCity_Movement_WallysUncleApproachPlayerNorth:
	walk_right
	walk_right
	walk_in_place_faster_up
	step_end

MauvilleCity_Movement_WallysUncleApproachPlayerEast:
	walk_right
	walk_up
	step_end

MauvilleCity_Movement_WallysUncleExitNorth2:
	walk_left
	walk_left
	walk_left
	walk_left
	walk_left
	walk_left
	walk_left
	walk_left
	step_end

MauvilleCity_Movement_WallysUncleExitEast2:
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

MauvilleCity_Movement_ScottApproachPlayerNorth:
	walk_up
	walk_up
	walk_up
	walk_up
	walk_up
	walk_up
	walk_left
	walk_left
	walk_left
	walk_left
	walk_in_place_faster_up
	step_end

MauvilleCity_Movement_ScottApproachPlayerEast:
	walk_up
	walk_up
	walk_up
	walk_up
	walk_up
	walk_left
	walk_left
	walk_left
	walk_left
	walk_left
	walk_up
	step_end

MauvilleCity_Movement_ScottExitNorth:
	walk_left
	walk_left
	walk_left
	walk_left
	walk_left
	walk_left
	walk_left
	walk_left
	walk_left
	step_end

MauvilleCity_Movement_ScottExitEast:
	walk_down
	walk_left
	walk_left
	walk_left
	walk_left
	walk_left
	walk_left
	walk_left
	walk_left
	walk_left
	step_end

MauvilleCity_EventScript_Wattson::
	lock
	faceplayer
	goto_if_set FLAG_GOT_TM_THUNDERBOLT_FROM_WATTSON, MauvilleCity_EventScript_ReceivedThunderbolt
	goto_if_eq VAR_NEW_MAUVILLE_STATE, 2, MauvilleCity_EventScript_CompletedNewMauville
	goto_if_set FLAG_GOT_BASEMENT_KEY_FROM_WATTSON, MauvilleCity_EventScript_BegunNewMauville
	msgbox MauvilleCity_Text_WattsonNeedFavorTakeKey, MSGBOX_DEFAULT
	giveitem ITEM_BASEMENT_KEY
	goto_if_eq VAR_RESULT, FALSE, Common_EventScript_ShowBagIsFull
	setflag FLAG_GOT_BASEMENT_KEY_FROM_WATTSON
	msgbox MauvilleCity_Text_WattsonWontBeChallenge, MSGBOX_DEFAULT
	release
	end

MauvilleCity_EventScript_BegunNewMauville::
	msgbox MauvilleCity_Text_WattsonWontBeChallenge, MSGBOX_DEFAULT
	release
	end

MauvilleCity_EventScript_CompletedNewMauville::
	msgbox MauvilleCity_Text_WattsonThanksTakeTM, MSGBOX_DEFAULT
	giveitem ITEM_TM_THUNDERBOLT
	goto_if_eq VAR_RESULT, FALSE, Common_EventScript_ShowBagIsFull
	setflag FLAG_GOT_TM_THUNDERBOLT_FROM_WATTSON
	msgbox MauvilleCity_Text_WattsonYoungTakeCharge, MSGBOX_DEFAULT
	release
	end

MauvilleCity_EventScript_ReceivedThunderbolt::
	msgbox MauvilleCity_Text_WattsonYoungTakeCharge, MSGBOX_DEFAULT
	release
	end

MauvilleCity_EventScript_RegisterWallyCall::
	lockall
	pokenavcall MauvilleCity_Text_WallyPokenavCall
	waitmessage
	delay 30
	playfanfare MUS_REGISTER_MATCH_CALL
	msgbox MauvilleCity_Text_RegisteredWally, MSGBOX_DEFAULT
	waitfanfare
	closemessage
	delay 30
	setflag FLAG_ENABLE_WALLY_MATCH_CALL
	clearflag FLAG_ENABLE_FIRST_WALLY_POKENAV_CALL
	releaseall
	end

MauvilleCity_Text_UncleHesTooPeppy:
	.string "UNCLE: This kid catches a RALTS with\n"
	.string "only a few moves, and suddenly he\l"
	.string "thinks he can take on the world.$"

MauvilleCity_Text_WallyWantToChallengeGym:
	.string "WALLY: UNC, power clear have. RALTS\n"
	.string "use moving like CONFUSIC or\l"
	.string "TELEPORTATIONS, effective hits super.\l"
	.string "Before beatable ZIGZAGOON three.$"

MauvilleCity_Text_UncleYourePushingIt:
	.string "UNCLE: Now hold on, WALLY, you bigmouth.\p"
	.string "You've beaten two ZIGZAGOON that were\n"
	.string "already close to fainting, because some\l"
	.string "kid with overpowered POKéMON walked\l"
	.string "past.\p"
	.string "And now you think you're the bomb\n"
	.string "diggity?$"

MauvilleCity_Text_WallyWeCanBeatAnyone:
	.string "WALLY: Uncle no understanding have,\n"
	.string "knowledge little. Rule of POKéMON\l"
	.string "faint is faint.$"

MauvilleCity_Text_WallyWillYouBattleMe:
	.string "WALLY: Oh! Greet {PLAYER}!\p"
	.string "Power increasings. Now gym challenge\n"
	.string "want. Engagement? Test power.$"

MauvilleCity_Text_WallyMyUncleWontKnowImStrong:
	.string "WALLY: Unfortunatings. Time of later.\n"
	.string "Understand heal understand well.$"

MauvilleCity_Text_UncleCanYouBattleWally:
	.string "UNCLE: {PLAYER}{KUN}, there's my savior!\p"
	.string "Beat this little brat and knock some\n"
	.string "sense into his little brain!$"

MauvilleCity_Text_WallyPleaseBattleMe:
	.string "WALLY: {PLAYER}, gratitude when\n"
	.string "will have engagement.$"

MauvilleCity_Text_WallyHereICome:
	.string "WALLY: {PLAYER}, thank. DESTINATION!$"

MauvilleCity_Text_WallyDefeat:
	.string "WALLY: … … … … … … …\p"
	.string "… … … … … … … …\p"
	.string "Failure have$"

MauvilleCity_Text_WallyIllGoBackToVerdanturf:
	.string "WALLY: UNCLE…\n"
	.string "VERDANTURF walk$"

MauvilleCity_Text_ThankYouNotEnoughToBattle:
	.string "{PLAYER}, thanks a lot. Being a TRAINER\n"
	.string "is tough, isn't it?\p"
	.string "But not as tough as a 9-to-5 of manual\n"
	.string "labor in our garden.\p"
	.string "And to be fair, I really need this kid\n"
	.string "for that this summer.\p"
	.string "So man up!$"

MauvilleCity_Text_UncleNoNeedToBeDown:
	.string "UNCLE: WALLY, get yo ass to the garden.\p"
	.string "And don't forget the apple knife on\n"
	.string "your way there.$"

MauvilleCity_Text_UncleVisitUsSometime:
	.string "UNCLE: {PLAYER}{KUN}, it just dawned on me:\n"
	.string "you're the one who told WALLY to get a\l"
	.string "RALTS.\p"
	.string "At least a RALTS grows up useful\n"
	.string "eventually.\p"
	.string "Thanks for not being an asshole!$"

MauvilleCity_Text_WallyPokenavCall:
	.string "… … … … … …\n"
	.string "… … … … … Beep!\p"
	.string "WALLY: Greet, {PLAYER}!\p"
	.string "UNC have POKéNAV purchase. Fast\n"
	.string "speed fast, call often? {PLAYER}!\p"
	.string "… … … … … …\n"
	.string "… … … … … Click!$"

MauvilleCity_Text_RegisteredWally:
	.string "Registered WALLY in the POKéNAV.$"

MauvilleCity_Text_ScottYouDidntHoldBack:
	.string "SCOTT: Hehe…\n"
	.string "I was watching that match like the\l"
	.string "creep that I am!\p"
	.string "You're friends with that boy WALLY,\n"
	.string "aren't you?\p"
	.string "But you didn't hold anything back\n"
	.string "and beat him impressively.\p"
	.string "Yeah! That's what a real bully\n"
	.string "tends to do!\l"
	.string "I idolize TRAINERS like that!\p"
	.string "… … … … … …\n"
	.string "I'll be cheering for you!$"

MauvilleCity_Text_WattsonNeedFavorTakeKey:
	.string "WATTSON: {PLAYER}{KUN}! Just the kid I need!\p"
	.string "Under the city is NEW MAUVILLE, my DATA\n"
	.string "CENTER. AI, crypto, everyone's browser\l"
	.string "history. All of it.\p"
	.string "It uses more power than the whole\n"
	.string "region. The cooling is one fan I bought\l"
	.string "in 1998.\p"
	.string "It's overheating. Go switch off the\n"
	.string "GENERATOR. Here's the KEY to NEW\l"
	.string "MAUVILLE.$"

MauvilleCity_Text_WattsonWontBeChallenge:
	.string "WATTSON: The entrance is a short SURF\n"
	.string "from ROUTE 110.\p"
	.string "Don't mind the smell. That's the AI\n"
	.string "thinking. Wahahahaha!$"

MauvilleCity_Text_WattsonThanksTakeTM:
	.string "WATTSON: Wahahahaha! My servers are\n"
	.string "safe! Your data too. Mostly.\p"
	.string "Here, a TM with THUNDERBOLT. The\n"
	.string "electricity bill goes to the city.$"

MauvilleCity_Text_WattsonYoungTakeCharge:
	.string "WATTSON: Wahahahaha! Nothing beats\n"
	.string "cheap labor. I mean, young people\l"
	.string "stepping up!$"

MauvilleCity_Text_NurseHurtMonBackToHealth:
	.string "Battles are cool and stuff…\p"
	.string "But if your POKéMON gets hurt, you have\n"
	.string "to heal it.\p"
	.string "Or just put it in the PC and forget\n"
	.string "about it. Like my dad.$"

MauvilleCity_Text_AllSortsOfPeopleComeThrough:
	.string "MAUVILLE's roads go north, south, east\n"
	.string "and west.\p"
	.string "So all sorts of people come through.\p"
	.string "And all their data goes through the\n"
	.string "datacenter.$"

MauvilleCity_Text_RydelVeryGenerous:
	.string "Have you been to RYDEL'S CYCLES?\p"
	.string "RYDEL gives away bikes. Free.\p"
	.string "Nobody knows how he pays rent.$"

MauvilleCity_Text_PokemonCanJumpYouOnBike:
	.string "Even on a BIKE, wild POKéMON can jump\n"
	.string "you.\p"
	.string "That's why I take a limo.$"

MauvilleCity_Text_CitySign:
	.string "MAUVILLE CITY\n"
	.string "“The bright and shiny city of fun!\l"
	.string "Powered by the datacenter.”$"

MauvilleCity_Text_GymSign:
	.string "MAUVILLE CITY POKéMON GYM\n"
	.string "LEADER: WATTSON\p"
	.string "“Our Electric Wizard! Commercializes\n"
	.string "everything electric or electronic!\l"
	.string "Wahahaha!”$"

MauvilleCity_Text_BikeShopSign:
	.string "“Ride in gravel and shake up your soul!\n"
	.string "And your spine.”\l"
	.string "RYDEL'S CYCLES$"

MauvilleCity_Text_GameCornerSign:
	.string "“The play spot for all! Until it isn't.”\n"
	.string "MAUVILLE GAME CORNER$"

MauvilleCity_Text_ExplainTV:
	.string "Do you watch TV?\p"
	.string "They've added tons of new shows. All of\n"
	.string "them are about us.\p"
	.string "Sometimes they put you on TV without\n"
	.string "asking.\p"
	.string "The datacenter knows everything.\n"
	.string "Everything.\p"
	.string "That's why I watch. Just to see what\n"
	.string "they know.$"

MauvilleCity_Text_BeenCheckingOutTV:
	.string "Have you been watching TV?\p"
	.string "The datacenter is watching you back.$"

@ ---------------------------------------------------------------- Project Grounded: Colress in Mauville
@ Bij de eerste keer binnenkomen vanaf Route 110 loopt Colress op je af. Weiger je het gevecht, dan wacht hij
@ bij het Pokémon Center (VAR_COLRESS_MAUVILLE_STATE 1) tot je het wel aangaat.
MauvilleCity_EventScript_SetColressVisibility::
	setflag FLAG_HIDE_MAUVILLE_COLRESS
	call_if_eq VAR_COLRESS_MAUVILLE_STATE, 2, MauvilleCity_EventScript_ColressMagearnaVisibility
	goto_if_ne VAR_COLRESS_MAUVILLE_STATE, 1, Common_EventScript_NopReturn
	clearflag FLAG_HIDE_MAUVILLE_COLRESS
	return

@ Na de Plasma Frigate (VAR_PLASMA_FRIGATE 8) staat Colress bij het Pokémon Center met Magearna, tot je hem hebt.
MauvilleCity_EventScript_ColressMagearnaVisibility::
	goto_if_set FLAG_RECEIVED_MAGEARNA, Common_EventScript_NopReturn
	goto_if_lt VAR_PLASMA_FRIGATE, 8, Common_EventScript_NopReturn
	setobjectxyperm LOCALID_MAUVILLE_COLRESS, 21, 9
	setobjectmovementtype LOCALID_MAUVILLE_COLRESS, MOVEMENT_TYPE_FACE_DOWN
	clearflag FLAG_HIDE_MAUVILLE_COLRESS
	return

MauvilleCity_EventScript_ColressMagearna::
	msgbox MauvilleCity_Text_ColressMagearna, MSGBOX_DEFAULT
	setvar VAR_0x8004, SPECIES_MAGEARNA
	setvar VAR_0x8005, 60
	setvar VAR_0x8006, ITEM_NONE
	call Grounded_EventScript_GiveGiftMon
	goto_if_eq VAR_RESULT, FALSE, MauvilleCity_EventScript_ColressMagearnaNoRoom
	setflag FLAG_RECEIVED_MAGEARNA
	msgbox MauvilleCity_Text_ColressMagearnaAfter, MSGBOX_DEFAULT
	closemessage
	fadescreen FADE_TO_BLACK
	removeobject LOCALID_MAUVILLE_COLRESS
	setflag FLAG_HIDE_MAUVILLE_COLRESS
	fadescreen FADE_FROM_BLACK
	release
	end

MauvilleCity_EventScript_ColressMagearnaNoRoom::
	msgbox MauvilleCity_Text_ColressMagearnaNoRoom, MSGBOX_DEFAULT
	release
	end

MauvilleCity_EventScript_ColressArrives::
	lockall
	getplayerxy VAR_0x8004, VAR_0x8005
	copyvar VAR_0x8006, VAR_0x8004
	setvar VAR_0x8007, 0
	goto_if_ge VAR_0x8004, 30, MauvilleCity_EventScript_ColressFromLeft
	addvar VAR_0x8006, 7
	call MauvilleCity_EventScript_SpawnColress
	applymovement LOCALID_MAUVILLE_COLRESS, MauvilleCity_Movement_ColressWalkLeft
	goto MauvilleCity_EventScript_ColressTalk

MauvilleCity_EventScript_ColressFromLeft::
	setvar VAR_0x8007, 1
	subvar VAR_0x8006, 7
	call MauvilleCity_EventScript_SpawnColress
	applymovement LOCALID_MAUVILLE_COLRESS, MauvilleCity_Movement_ColressWalkRight
	goto MauvilleCity_EventScript_ColressTalk

MauvilleCity_EventScript_SpawnColress::
	setobjectxyperm LOCALID_MAUVILLE_COLRESS, VAR_0x8006, 17
	clearflag FLAG_HIDE_MAUVILLE_COLRESS
	addobject LOCALID_MAUVILLE_COLRESS
	return

MauvilleCity_EventScript_ColressTalk::
	waitmovement 0
	applymovement LOCALID_PLAYER, Common_Movement_WalkInPlaceFasterUp
	applymovement LOCALID_MAUVILLE_COLRESS, Common_Movement_WalkInPlaceFasterDown
	waitmovement 0
	playse SE_PIN
	applymovement LOCALID_MAUVILLE_COLRESS, Common_Movement_ExclamationMark
	waitmovement 0
	msgbox MauvilleCity_Text_ColressIntro, MSGBOX_DEFAULT
	msgbox MauvilleCity_Text_ColressAsk, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, MauvilleCity_EventScript_ColressDeclined
	call MauvilleCity_EventScript_ColressBattle
	closemessage
	fadescreen FADE_TO_BLACK
	removeobject LOCALID_MAUVILLE_COLRESS
	setflag FLAG_HIDE_MAUVILLE_COLRESS
	fadescreen FADE_FROM_BLACK
	releaseall
	end

MauvilleCity_EventScript_ColressDeclined::
	setvar VAR_COLRESS_MAUVILLE_STATE, 1
	msgbox MauvilleCity_Text_ColressDeclined, MSGBOX_DEFAULT
	call MauvilleCity_EventScript_ColressLeave
	removeobject LOCALID_MAUVILLE_COLRESS
	setobjectxyperm LOCALID_MAUVILLE_COLRESS, 21, 9
	addobject LOCALID_MAUVILLE_COLRESS
	releaseall
	end

MauvilleCity_EventScript_ColressBattle::
	msgbox MauvilleCity_Text_ColressAccept, MSGBOX_DEFAULT
	trainerbattle_no_intro TRAINER_COLRESS_MAUVILLE, MauvilleCity_Text_ColressDefeat
	setvar VAR_COLRESS_MAUVILLE_STATE, 2
	msgbox MauvilleCity_Text_ColressPostBattle, MSGBOX_DEFAULT
	return

@ aangesproken bij het Pokémon Center (na weigeren)
MauvilleCity_EventScript_Colress::
	lock
	faceplayer
	goto_if_eq VAR_COLRESS_MAUVILLE_STATE, 2, MauvilleCity_EventScript_ColressMagearna
	msgbox MauvilleCity_Text_ColressWaiting, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, MauvilleCity_EventScript_ColressStillWaiting
	call MauvilleCity_EventScript_ColressBattle
	closemessage
	fadescreen FADE_TO_BLACK
	removeobject LOCALID_MAUVILLE_COLRESS
	setflag FLAG_HIDE_MAUVILLE_COLRESS
	fadescreen FADE_FROM_BLACK
	release
	end

MauvilleCity_EventScript_ColressStillWaiting::
	msgbox MauvilleCity_Text_ColressStillWaiting, MSGBOX_DEFAULT
	release
	end

@ terug zoals hij kwam (VAR_0x8007: 0 = kwam van rechts)
MauvilleCity_EventScript_ColressLeave::
	call_if_eq VAR_0x8007, 0, MauvilleCity_EventScript_ColressLeaveRight
	call_if_eq VAR_0x8007, 1, MauvilleCity_EventScript_ColressLeaveLeft
	waitmovement 0
	return

MauvilleCity_EventScript_ColressLeaveRight::
	applymovement LOCALID_MAUVILLE_COLRESS, MauvilleCity_Movement_ColressLeaveRight
	return

MauvilleCity_EventScript_ColressLeaveLeft::
	applymovement LOCALID_MAUVILLE_COLRESS, MauvilleCity_Movement_ColressLeaveLeft
	return

MauvilleCity_Movement_ColressWalkLeft:
	walk_left
	walk_left
	walk_left
	walk_left
	walk_left
	walk_left
	walk_left
	step_end

MauvilleCity_Movement_ColressWalkRight:
	walk_right
	walk_right
	walk_right
	walk_right
	walk_right
	walk_right
	walk_right
	step_end

MauvilleCity_Movement_ColressLeaveRight:
	walk_fast_right
	walk_fast_right
	walk_fast_right
	walk_fast_right
	walk_fast_right
	walk_fast_right
	walk_fast_right
	walk_fast_right
	step_end

MauvilleCity_Movement_ColressLeaveLeft:
	walk_fast_left
	walk_fast_left
	walk_fast_left
	walk_fast_left
	walk_fast_left
	walk_fast_left
	walk_fast_left
	walk_fast_left
	step_end

MauvilleCity_Text_ColressIntro:
	.string "???: Ah! A fresh data point walking into\n"
	.string "MAUVILLE!\p"
	.string "I am COLRESS. I came here because\n"
	.string "MAUVILLE calls itself the city of the\l"
	.string "future.\p"
	.string "Then I looked at the future. Allow me to\n"
	.string "present my findings.\p"
	.string "Exhibit A: the GAME CORNER. Every slot\n"
	.string "machine is a random number generator\l"
	.string "wired to one man named Gerald. When you\l"
	.string "win, Gerald cries.\p"
	.string "Exhibit B: the entire city runs on a\n"
	.string "single PAWMI in a hamster wheel.\l"
	.string "WATTSON calls this “the grid.”\p"
	.string "Exhibit C: the bike shop sells two bikes,\n"
	.string "but you may only own one. That is not a\l"
	.string "business model. That is a hostage\l"
	.string "situation.\p"
	.string "Exhibit D: the power plant under the\n"
	.string "city is sealed with a key. The key is in\l"
	.string "WATTSON's pocket. Next to a peppermint.\l"
	.string "The peppermint is also from 1987.\p"
	.string "Exhibit E: the internet here is a ROTOM\n"
	.string "in somebody's basement. It has opinions\l"
	.string "about your browser history.\p"
	.string "Conclusion: MAUVILLE is held together\n"
	.string "by tape, optimism and one very tired\l"
	.string "electric rodent.\p"
	.string "But the most interesting thing in this\n"
	.string "city... is your team.\p"
	.string "I sense structure. Synergy. Somebody\n"
	.string "actually thought about type coverage.\l"
	.string "Or got lucky in a statistically\l"
	.string "fascinating way.$"

MauvilleCity_Text_ColressAsk:
	.string "Would you let me test it in battle?\n"
	.string "Strictly for science.\p"
	.string "You may refuse. Science also studies\n"
	.string "rejection.$"

MauvilleCity_Text_ColressAccept:
	.string "Excellent! Let us collect some data!$"

MauvilleCity_Text_ColressDeclined:
	.string "A refusal! Noted, logged and\n"
	.string "timestamped.\p"
	.string "I will be near the POKéMON CENTER,\n"
	.string "recalibrating. Come find me when your\l"
	.string "curiosity wins.$"

MauvilleCity_Text_ColressDefeat:
	.string "Fascinating! My hypothesis was wrong.\n"
	.string "That is the best possible outcome!$"

MauvilleCity_Text_ColressPostBattle:
	.string "Your Pokémon brought out every last\n"
	.string "bit of their potential.\p"
	.string "Unlike MAUVILLE's power grid. I'm going\n"
	.string "to give that PAWMI a day off and see\l"
	.string "what happens.$"

MauvilleCity_Text_ColressWaiting:
	.string "COLRESS: Ah, my favorite data point!\n"
	.string "Has your curiosity finally won? Shall we\l"
	.string "battle?$"

MauvilleCity_Text_ColressStillWaiting:
	.string "Still no? Fine. I will keep observing the\n"
	.string "bike shop. I believe it's about to sell a\l"
	.string "third bike to nobody.$"

MauvilleCity_Text_ColressMagearna:
	.string "COLRESS: {PLAYER}. I heard you sank NEO\n"
	.string "PLASMA's frigate. Well. Inconvenienced\l"
	.string "it.\p"
	.string "GENESECT was their idea of science.\n"
	.string "Bolt a cannon to a fossil and call it\l"
	.string "progress. Crude.\p"
	.string "This is MAGEARNA. Built five hundred\n"
	.string "years ago by someone who actually knew\l"
	.string "what they were doing.\p"
	.string "I have studied it for ten years. The\n"
	.string "main thing I learned is that I am not\l"
	.string "that person.\p"
	.string "Take it. It deserves a trainer who\n"
	.string "brings out its true strength. I'll\l"
	.string "settle for one who reads the manual.$"

MauvilleCity_Text_ColressMagearnaAfter:
	.string "COLRESS: Its SOUL-HEART is a\n"
	.string "mechanical heart. Unlike mine, it works.\p"
	.string "If it starts ticking louder, that's\n"
	.string "normal. If it stops, run.$"

MauvilleCity_Text_ColressMagearnaNoRoom:
	.string "COLRESS: No room? Not even in a box?\n"
	.string "You have nineteen boxes. Fascinating.\l"
	.string "Come back when you've freed some up.$"

MauvilleCity_Text_TakeExpertBelt:
	.string "Here, peasant. An EXPERT BELT.\p"
	.string "It powers up super effective moves.\n"
	.string "My personal trainer left it behind.\p"
	.string "He's my personal ex-trainer now.$"
