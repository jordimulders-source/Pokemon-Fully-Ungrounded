DewfordTown_MapScripts::
	map_script MAP_SCRIPT_ON_TRANSITION, DewfordTown_OnTransition
	.byte 0

DewfordTown_OnTransition:
	setflag FLAG_VISITED_DEWFORD_TOWN
	end

DewfordTown_EventScript_Briney::
	lock
	faceplayer
	setvar VAR_0x8004, 1 @ Project Grounded: Keldeo-eiland (UnchartedIsle/scripts.inc)
	call EventScript_BrineyKeldeoTrip
	goto_if_unset FLAG_DELIVERED_STEVEN_LETTER, DewfordTown_EventScript_ReturnToPetalburgPrompt
	message DewfordTown_Text_WhereAreWeBound
	waitmessage
	multichoicedefault 21, 6, MULTI_BRINEY_ON_DEWFORD, 2, FALSE
	switch VAR_RESULT
	case 0, DewfordTown_EventScript_ChoosePetalburg
	case 1, DewfordTown_EventScript_ChooseSlateport
	case 2, DewfordTown_EventScript_CancelSailSelect
	case MULTI_B_PRESSED, DewfordTown_EventScript_CancelSailSelect
	end

DewfordTown_EventScript_ChoosePetalburg::
	msgbox DewfordTown_Text_PetalburgWereSettingSail, MSGBOX_DEFAULT
	closemessage
	goto DewfordTown_EventScript_SailToPetalburg
	release
	end

DewfordTown_EventScript_ChooseSlateport::
	msgbox DewfordTown_Text_SlateportWereSettingSail, MSGBOX_DEFAULT
	closemessage
	goto DewfordTown_EventScript_SailToSlateport
	release
	end

DewfordTown_EventScript_CancelSailSelect::
	msgbox DewfordTown_Text_JustTellMeWhenYouNeedToSetSail, MSGBOX_DEFAULT
	closemessage
	release
	end

DewfordTown_EventScript_ReturnToPetalburgPrompt::
	msgbox DewfordTown_Text_SetSailBackToPetalburg, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, YES, DewfordTown_EventScript_SailBackToPetalburg
	msgbox DewfordTown_Text_GoDeliverIllBeWaiting, MSGBOX_DEFAULT
	release
	end

DewfordTown_EventScript_SailBackToPetalburg::
	msgbox DewfordTown_Text_PetalburgWereSettingSail2, MSGBOX_DEFAULT
	closemessage
	goto DewfordTown_EventScript_SailToPetalburg
	end

DewfordTown_EventScript_Woman::
	msgbox DewfordTown_Text_TinyIslandCommunity, MSGBOX_NPC
	end

DewfordTown_EventScript_TownSign::
	msgbox DewfordTown_Text_TownSign, MSGBOX_SIGN
	end

DewfordTown_EventScript_GymSign::
	msgbox DewfordTown_Text_GymSign, MSGBOX_SIGN
	end

DewfordTown_EventScript_HallSign::
	msgbox DewfordTown_Text_HallSign, MSGBOX_SIGN
	end

DewfordTown_EventScript_OldRodFisherman::
	lock
	faceplayer
	goto_if_set FLAG_RECEIVED_OLD_ROD, DewfordTown_EventScript_HowsFishing
	msgbox DewfordTown_Text_GettingItchToFish, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, YES, DewfordTown_EventScript_GiveOldRod
	goto_if_eq VAR_RESULT, NO, DewfordTown_EventScript_NotGettingItchToFish
	end

DewfordTown_EventScript_GiveOldRod::
	msgbox DewfordTown_Text_GiveYouOneOfMyRods, MSGBOX_DEFAULT
	giveitem ITEM_OLD_ROD
	goto_if_eq VAR_RESULT, FALSE, Common_EventScript_ShowBagIsFull
	setflag FLAG_RECEIVED_OLD_ROD
	msgbox DewfordTown_Text_ThrowInFishingAdvice, MSGBOX_DEFAULT
	release
	end

DewfordTown_EventScript_NotGettingItchToFish::
	msgbox DewfordTown_Text_ThatsTooBadThen, MSGBOX_DEFAULT
	release
	end

DewfordTown_EventScript_HowsFishing::
	message DewfordTown_Text_HowsYourFishing
	waitmessage
	multichoice 20, 8, MULTI_HOWS_FISHING, TRUE
	goto_if_eq VAR_RESULT, 0, DewfordTown_EventScript_FishingExcellent
	goto_if_eq VAR_RESULT, 1, DewfordTown_EventScript_FishingNotSoGood
	end

DewfordTown_EventScript_FishingExcellent::
	msgbox DewfordTown_Text_GreatHaulInSomeBigOnes, MSGBOX_DEFAULT
	release
	end

DewfordTown_EventScript_FishingNotSoGood::
	msgbox DewfordTown_Text_FishingAdvice, MSGBOX_DEFAULT
	release
	end

DewfordTown_EventScript_SailToPetalburg::
	call EventScript_BackupMrBrineyLocation
	setobjectsubpriority LOCALID_DEWFORD_BRINEY, MAP_DEWFORD_TOWN, 0
	setobjectsubpriority LOCALID_PLAYER, MAP_DEWFORD_TOWN, 0
	applymovement LOCALID_DEWFORD_BRINEY, DewfordTown_Movement_BrineyBoardBoat
	waitmovement 0
	removeobject LOCALID_DEWFORD_BRINEY
	applymovement LOCALID_PLAYER, DewfordTown_Movement_PlayerBoardBoat
	waitmovement 0
	hideobjectat LOCALID_PLAYER, MAP_DEWFORD_TOWN
	call Common_EventScript_PlayBrineysBoatMusic
	applymovement LOCALID_DEWFORD_BOAT, DewfordTown_Movement_SailToPetalburg
	applymovement LOCALID_PLAYER, DewfordTown_Movement_SailToPetalburg
	waitmovement 0
	showobjectat LOCALID_PLAYER, MAP_ROUTE104
	call Common_EventScript_StopBrineysBoatMusic
	applymovement LOCALID_PLAYER, DewfordTown_Movement_ExitBoatPetalburg
	waitmovement 0
	showobjectat LOCALID_PLAYER, MAP_ROUTE104
	clearflag FLAG_HIDE_BRINEYS_HOUSE_MR_BRINEY
	clearflag FLAG_HIDE_BRINEYS_HOUSE_PEEKO
	clearflag FLAG_HIDE_ROUTE_104_MR_BRINEY_BOAT
	setflag FLAG_HIDE_MR_BRINEY_BOAT_DEWFORD_TOWN
	hideobjectat LOCALID_DEWFORD_BOAT, MAP_DEWFORD_TOWN
	setvar VAR_BOARD_BRINEY_BOAT_STATE, 2
	resetobjectsubpriority LOCALID_PLAYER, MAP_DEWFORD_TOWN
	warp MAP_ROUTE104_MR_BRINEYS_HOUSE, 5, 4
	copyvar VAR_BRINEY_LOCATION, VAR_0x8008
	waitstate
	release
	end

DewfordTown_EventScript_SailToSlateport::
	call EventScript_BackupMrBrineyLocation
	setobjectsubpriority LOCALID_DEWFORD_BRINEY, MAP_DEWFORD_TOWN, 0
	setobjectsubpriority LOCALID_PLAYER, MAP_DEWFORD_TOWN, 1
	applymovement LOCALID_DEWFORD_BRINEY, DewfordTown_Movement_BrineyBoardBoat
	waitmovement 0
	removeobject LOCALID_DEWFORD_BRINEY
	applymovement LOCALID_PLAYER, DewfordTown_Movement_PlayerBoardBoat
	waitmovement 0
	hideobjectat LOCALID_PLAYER, MAP_DEWFORD_TOWN
	call Common_EventScript_PlayBrineysBoatMusic
	applymovement LOCALID_DEWFORD_BOAT, DewfordTown_Movement_SailToSlateport
	applymovement LOCALID_PLAYER, DewfordTown_Movement_SailToSlateport
	waitmovement 0
	call Common_EventScript_StopBrineysBoatMusic
	showobjectat LOCALID_PLAYER, MAP_ROUTE109
	applymovement LOCALID_PLAYER, DewfordTown_Movement_ExitBoatSlateport
	waitmovement 0
	setobjectxyperm LOCALID_ROUTE109_BRINEY, 21, 26
	addobject LOCALID_ROUTE109_BRINEY
	setobjectsubpriority LOCALID_ROUTE109_BRINEY, MAP_ROUTE109, 0
	applymovement LOCALID_ROUTE109_BRINEY, DewfordTown_Movement_BrineyExitBoat
	waitmovement 0
	clearflag FLAG_HIDE_ROUTE_109_MR_BRINEY
	addobject LOCALID_ROUTE109_BOAT
	clearflag FLAG_HIDE_ROUTE_109_MR_BRINEY_BOAT
	setflag FLAG_HIDE_MR_BRINEY_BOAT_DEWFORD_TOWN
	hideobjectat LOCALID_DEWFORD_BOAT, MAP_DEWFORD_TOWN
	call_if_unset FLAG_DELIVERED_DEVON_GOODS, DewfordTown_EventScript_LandedSlateportDeliverGoods
	call_if_set FLAG_DELIVERED_DEVON_GOODS, DewfordTown_EventScript_LandedSlateport
	closemessage
	copyvar VAR_BRINEY_LOCATION, VAR_0x8008
	resetobjectsubpriority LOCALID_PLAYER, MAP_DEWFORD_TOWN
	resetobjectsubpriority LOCALID_ROUTE109_BRINEY, MAP_ROUTE109
	copyobjectxytoperm LOCALID_ROUTE109_BRINEY
	release
	end

DewfordTown_EventScript_LandedSlateportDeliverGoods::
	msgbox DewfordTown_Text_BrineyLandedInSlateportDeliverGoods, MSGBOX_DEFAULT
	return

DewfordTown_EventScript_LandedSlateport::
	msgbox DewfordTown_Text_BrineyLandedInSlateport, MSGBOX_DEFAULT
	return

DewfordTown_Movement_SailToPetalburg:
	walk_up
	walk_up
	walk_fast_up
	walk_fast_up
	walk_fast_up
	walk_fast_up
	walk_fast_up
	walk_fast_up
	walk_fast_up
	walk_fast_up
	walk_fast_up
	walk_fast_up
	walk_fast_up
	walk_fast_up
	walk_fast_up
	walk_fast_up
	walk_fast_up
	walk_up
	walk_up
	walk_left
	walk_left
	walk_fast_left
	walk_fast_left
	walk_fast_left
	walk_fast_left
	walk_faster_left
	walk_faster_left
	walk_faster_left
	walk_faster_left
	walk_faster_left
	walk_faster_left
	walk_faster_left
	walk_faster_left
	walk_faster_left
	walk_faster_left
	walk_faster_left
	walk_faster_left
	walk_faster_left
	walk_faster_left
	walk_faster_left
	walk_faster_left
	walk_faster_left
	walk_faster_left
	walk_faster_left
	walk_faster_left
	walk_faster_left
	walk_faster_left
	walk_faster_left
	walk_faster_left
	walk_faster_left
	walk_faster_left
	walk_faster_left
	walk_faster_left
	walk_faster_left
	walk_faster_left
	walk_faster_left
	walk_faster_left
	walk_faster_left
	walk_faster_left
	walk_faster_left
	walk_faster_left
	walk_faster_left
	walk_faster_left
	walk_faster_left
	walk_faster_left
	walk_fast_left
	walk_fast_left
	walk_fast_left
	walk_fast_left
	walk_fast_up
	walk_fast_up
	walk_fast_up
	walk_fast_up
	walk_faster_up
	walk_faster_up
	walk_faster_up
	walk_faster_up
	walk_faster_up
	walk_faster_up
	walk_faster_up
	walk_faster_up
	walk_faster_up
	walk_faster_up
	walk_faster_up
	walk_faster_up
	walk_faster_up
	walk_faster_up
	walk_faster_up
	walk_faster_up
	walk_faster_up
	walk_faster_up
	walk_faster_up
	walk_faster_up
	walk_faster_up
	walk_faster_up
	walk_faster_up
	walk_faster_up
	walk_faster_up
	walk_faster_up
	walk_faster_up
	walk_faster_up
	walk_faster_up
	walk_faster_up
	walk_faster_up
	walk_faster_up
	walk_faster_up
	walk_faster_up
	walk_faster_up
	walk_faster_up
	walk_faster_up
	walk_faster_up
	walk_faster_up
	walk_faster_up
	walk_faster_up
	walk_faster_up
	walk_faster_up
	walk_faster_up
	walk_faster_up
	walk_faster_up
	walk_faster_up
	walk_faster_up
	walk_faster_up
	walk_faster_up
	walk_faster_up
	walk_faster_up
	walk_faster_up
	walk_faster_up
	walk_faster_up
	walk_faster_up
	walk_faster_up
	walk_faster_up
	walk_faster_up
	walk_faster_up
	walk_faster_up
	walk_faster_up
	walk_faster_up
	walk_faster_up
	walk_faster_up
	walk_faster_up
	walk_faster_up
	walk_faster_up
	walk_faster_up
	walk_faster_up
	walk_faster_up
	walk_faster_up
	walk_faster_up
	walk_faster_up
	walk_faster_up
	walk_faster_up
	walk_faster_up
	walk_faster_up
	walk_faster_up
	walk_faster_up
	walk_faster_up
	walk_faster_up
	walk_faster_up
	walk_fast_up
	walk_fast_up
	walk_fast_up
	walk_fast_up
	walk_fast_left
	walk_fast_left
	walk_faster_left
	walk_faster_left
	walk_faster_left
	walk_faster_left
	walk_faster_left
	walk_faster_left
	walk_fast_left
	walk_fast_left
	walk_fast_up
	walk_fast_up
	walk_faster_up
	walk_faster_up
	walk_faster_up
	walk_faster_up
	walk_faster_up
	walk_faster_up
	walk_faster_up
	walk_faster_up
	walk_faster_up
	walk_faster_up
	walk_faster_up
	walk_faster_up
	walk_faster_up
	walk_faster_up
	walk_fast_up
	walk_fast_up
	walk_fast_up
	walk_fast_up
	walk_up
	walk_up
	walk_up
	walk_up
	step_end

DewfordTown_Movement_SailToSlateport:
	walk_right
	walk_fast_right
	walk_fast_right
	walk_faster_right
	walk_faster_right
	walk_faster_right
	walk_faster_right
	walk_faster_right
	walk_faster_right
	walk_faster_right
	walk_faster_right
	walk_faster_right
	walk_faster_right
	walk_faster_right
	walk_faster_right
	walk_faster_right
	walk_faster_right
	walk_faster_right
	walk_faster_right
	walk_faster_right
	walk_faster_right
	walk_faster_right
	walk_faster_right
	walk_faster_right
	walk_faster_right
	walk_faster_right
	walk_faster_right
	walk_faster_right
	walk_faster_right
	walk_faster_right
	walk_faster_right
	walk_faster_right
	walk_faster_right
	walk_faster_right
	walk_faster_right
	walk_faster_right
	walk_faster_right
	walk_faster_right
	walk_faster_right
	walk_faster_right
	walk_faster_right
	walk_faster_right
	walk_faster_right
	walk_faster_right
	walk_faster_right
	walk_faster_right
	walk_faster_right
	walk_faster_right
	walk_faster_right
	walk_faster_right
	walk_faster_right
	walk_faster_right
	walk_faster_right
	walk_faster_right
	walk_faster_right
	walk_faster_right
	walk_faster_right
	walk_faster_right
	walk_faster_right
	walk_faster_right
	walk_faster_right
	walk_faster_right
	walk_faster_right
	walk_faster_right
	walk_faster_right
	walk_faster_right
	walk_faster_right
	walk_faster_right
	walk_faster_right
	walk_faster_right
	walk_faster_right
	walk_faster_right
	walk_faster_right
	walk_faster_right
	walk_faster_right
	walk_faster_right
	walk_faster_right
	walk_faster_right
	walk_faster_right
	walk_faster_right
	walk_faster_right
	walk_faster_right
	walk_faster_right
	walk_faster_right
	walk_faster_right
	walk_faster_right
	walk_faster_right
	walk_faster_right
	walk_faster_right
	walk_faster_right
	walk_faster_right
	walk_faster_right
	walk_faster_right
	walk_faster_right
	walk_faster_right
	walk_faster_right
	walk_faster_right
	walk_faster_right
	walk_faster_right
	walk_faster_right
	walk_faster_right
	walk_faster_right
	walk_faster_right
	walk_faster_right
	walk_faster_right
	walk_faster_right
	walk_faster_right
	walk_faster_right
	walk_faster_right
	walk_faster_right
	walk_faster_right
	walk_faster_right
	walk_faster_right
	walk_faster_right
	walk_faster_right
	walk_faster_right
	walk_faster_right
	walk_faster_right
	walk_faster_right
	walk_faster_right
	walk_faster_right
	walk_faster_right
	walk_faster_right
	walk_faster_right
	walk_faster_right
	walk_faster_right
	walk_faster_right
	walk_faster_right
	walk_faster_right
	walk_faster_right
	walk_faster_right
	walk_faster_right
	walk_faster_right
	walk_faster_right
	walk_faster_right
	walk_faster_right
	walk_faster_right
	walk_faster_right
	walk_faster_right
	walk_faster_right
	walk_faster_right
	walk_faster_right
	walk_faster_right
	walk_faster_right
	walk_faster_right
	walk_faster_right
	walk_faster_right
	walk_fast_right
	walk_fast_right
	walk_fast_up
	walk_fast_up
	walk_faster_up
	walk_faster_up
	walk_faster_up
	walk_faster_up
	walk_faster_up
	walk_faster_up
	walk_faster_up
	walk_faster_up
	walk_faster_up
	walk_faster_up
	walk_fast_up
	walk_fast_up
	walk_fast_up
	walk_fast_up
	walk_fast_up
	walk_fast_up
	walk_fast_up
	walk_fast_up
	walk_fast_up
	walk_fast_up
	step_end

DewfordTown_Movement_PlayerBoardBoat:
	walk_right
	walk_up
	step_end

DewfordTown_Movement_ExitBoatPetalburg:
	walk_up
	walk_up
	walk_up
	step_end

DewfordTown_Movement_ExitBoatSlateport:
	walk_up
	walk_up
	walk_up
	walk_in_place_faster_down
	step_end

DewfordTown_Movement_BrineyBoardBoat:
	walk_up
	step_end

DewfordTown_Movement_BrineyExitBoat:
	walk_up
	walk_up
	step_end

DewfordTown_EventScript_TrendyPhraseBoy::
	lock
	faceplayer
	call Common_EventScript_BufferTrendyPhrase
	msgbox DewfordTown_Text_XIsTheBiggestHappeningThingRight, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, YES, DewfordTown_EventScript_ConfirmTrendyPhrase
	goto_if_eq VAR_RESULT, NO, DewfordTown_EventScript_RejectTrendyPhrase
	end

DewfordTown_EventScript_ConfirmTrendyPhrase::
	msgbox DewfordTown_Text_YeahDefinitionOfInRightNow, MSGBOX_DEFAULT
	release
	end

DewfordTown_EventScript_RejectTrendyPhrase::
	msgbox DewfordTown_Text_TellMeWhatsNewAndIn, MSGBOX_DEFAULT
	setvar VAR_0x8004, EASY_CHAT_TYPE_TRENDY_PHRASE
	call Common_ShowEasyChatScreen
	lock
	faceplayer
	goto_if_eq VAR_RESULT, TRUE, DewfordTown_EventScript_GiveNewTrendyPhrase
	goto_if_eq VAR_RESULT, FALSE, DewfordTown_EventScript_CancelNewTrendyPhrase
	end

DewfordTown_EventScript_GiveNewTrendyPhrase::
	incrementgamestat GAME_STAT_STARTED_TRENDS
	goto_if_eq VAR_0x8004, FALSE, DewfordTown_EventScript_PhraseNotTrendyEnough
	msgbox DewfordTown_Text_OfCourseIKnowAboutThat, MSGBOX_DEFAULT
	release
	end

DewfordTown_EventScript_CancelNewTrendyPhrase::
	msgbox DewfordTown_Text_HearOfAnyTrendsComeShareWithMe, MSGBOX_DEFAULT
	release
	end

DewfordTown_EventScript_PhraseNotTrendyEnough::
	msgbox DewfordTown_Text_XHuhIThinkYIsCool, MSGBOX_DEFAULT
	release
	end

DewfordTown_Text_TinyIslandCommunity:
	.string "DEWFORD is a tiny island community. If\n"
	.string "someone cheats on their wife, everyone\l"
	.string "knows within days.$"

DewfordTown_Text_TownSign:
	.string "DEWFORD TOWN “Where the island is nicer\n"
	.string "than its people”$"

DewfordTown_Text_GymSign:
	.string "DEWFORD TOWN POKéMON GYM LEADER:\n"
	.string "BRAWLY “DO YOU WANT TO BE A FUCKING\l"
	.string "FIGHTER?”$"

DewfordTown_Text_HallSign:
	.string "DEWFORD HALL “Everyone's gossip\n"
	.string "center!”$"

Route104_Text_LandedInDewfordDeliverLetter:
	.string "MR. BRINEY: Ahoy! We've hit land in\n"
	.string "DEWFORD.\p"
	.string "The people here are toxic. I will stay on\n"
	.string "the boat while you will search for that\l"
	.string "metalhead. What was his name, Stevie?$"

DewfordTown_Text_SetSailBackToPetalburg:
	.string "MR. BRINEY: Have you found Stewie?\p"
	.string "Or do you want to get back to a normal\n"
	.string "place, like PETALBURG?$"

DewfordTown_Text_PetalburgWereSettingSail2:
	.string "MR. BRINEY: PETALBURG it is, then!\n"
	.string "Finally!\p"
	.string "Take your seasick pills, we are going\n"
	.string "faster than lightning!$"

DewfordTown_Text_GoDeliverIllBeWaiting:
	.string "MR. BRINEY: Ugh, well take your time\n"
	.string "then. It's not like I'm very bored\l"
	.string "staying next to my boat all day.$"

DewfordTown_Text_BrineyLandedInDewford:
	.string "MR. BRINEY: Ahoy! We've hit land in\n"
	.string "DEWFORD!\p"
	.string "Was it really necessary to throw up\n"
	.string "inside of the boat?$"

DewfordTown_Text_WhereAreWeBound:
	.string "MR. BRINEY: Ahoy! I will sail eternally!\n"
	.string "What shithole will we touch down on\l"
	.string "next?$"

DewfordTown_Text_PetalburgWereSettingSail:
	.string "MR. BRINEY: PETALBURG, is it? Finally!\p"
	.string "Vamonos!$"

DewfordTown_Text_SlateportWereSettingSail:
	.string "MR. BRINEY: SLATEPORT, is it? That's a\n"
	.string "surprise. Are you sure, you are ready\l"
	.string "yet?$"

DewfordTown_Text_JustTellMeWhenYouNeedToSetSail:
	.string "MR. BRINEY: Get your shit together and\n"
	.string "then we get outta here!$"

DewfordTown_Text_GettingItchToFish:
	.string "This is a renowned catfishing spot. I\n"
	.string "was a victim once.$"

DewfordTown_Text_GiveYouOneOfMyRods:
	.string "Oh you too? I'll hand you over an OLD\n"
	.string "ROD. It won't help you against fake\l"
	.string "pictures, but at least you can calm\l"
	.string "down and catch some MAGIKARP.$"

DewfordTown_Text_ThrowInFishingAdvice:
	.string "Fantastic! Well, go on then! Start\n"
	.string "fishing! If you catch a Water Pokémon\l"
	.string "now, it'll be well evolved before you will\l"
	.string "enter the Fire gym.$"

DewfordTown_Text_ThatsTooBadThen:
	.string "You don't like fishing? Kids these days,\n"
	.string "continue doomscrolling then!$"

DewfordTown_Text_HowsYourFishing:
	.string "Did you catch anything? Except a cold?$"

DewfordTown_Text_GreatHaulInSomeBigOnes:
	.string "Well, watch out for nature\n"
	.string "organizations. I don't think MAGIKARP\l"
	.string "will become extinct anytime soon, but\l"
	.string "still!$"

DewfordTown_Text_FishingAdvice:
	.string "Ahh, that's a pity. Patience is key,\n"
	.string "young fisherman! I've heard through\l"
	.string "the grapevine that spitting in the\l"
	.string "water lures fish out.$"

DewfordTown_Text_XIsTheBiggestHappeningThingRight:
	.string "Sup, you bottom feeder. I am super\n"
	.string "trendy and I really think I am too good\l"
	.string "for you.\p"
	.string "Listen, have you heard about this new\n"
	.string "“{STR_VAR_1}”?\p"
	.string "You haven't, BOOMER! BOOMER!\p"
	.string "I mean, sheesh, “{STR_VAR_1}”… It's\n"
	.string "trending on TikTok.\p"
	.string "I mean are you from another planet?\n"
	.string "Geez...$"

DewfordTown_Text_TellMeWhatsNewAndIn:
	.string "Hahaha loser!\p"
	.string "(Does a Fortnite dance and turns\n"
	.string "around.)$"

DewfordTown_Text_OfCourseIKnowAboutThat:
	.string "Whut? “{STR_VAR_2}”?\p"
	.string "Are you gaslighting me? Well. “{STR_VAR_2}”\n"
	.string "I guess..$"

DewfordTown_Text_XHuhIThinkYIsCool:
	.string "Hmm… “{STR_VAR_2},” huh?\p"
	.string "I mean you are gaslighting me.\n"
	.string "“{STR_VAR_1}” is so much better. You won't\l"
	.string "tell me what to do.$"

DewfordTown_Text_HearOfAnyTrendsComeShareWithMe:
	.string "Please go away and hang out with your\n"
	.string "boomer friends or something.$"

DewfordTown_Text_YeahDefinitionOfInRightNow:
	.string "Yeah, haha of course.\p"
	.string "“{STR_VAR_1}” is the definition of\n"
	.string "trending. You surprise me in a positive\l"
	.string "way.$"

@ ===== Project Grounded: wekelijks visserstoernooi op de steiger (fishing_tournament.c) =====

DewfordTown_EventScript_FishJudge::
	lock
	faceplayer
	special FishTourney_Weigh
	goto_if_eq VAR_RESULT, 0, DewfordTown_EventScript_FishJudgeFull
	goto_if_eq VAR_0x8004, TRUE, DewfordTown_EventScript_FishJudgeRepeat
DewfordTown_EventScript_FishJudgeFull::
	special FishTourney_GetBoardInfo
	msgbox DewfordTown_Text_FishJudgeIntro, MSGBOX_DEFAULT
	special FishTourney_Weigh
	goto_if_eq VAR_RESULT, 0, DewfordTown_EventScript_FishJudgeNoFish
	playse SE_BALL_TRAY_BALL
	msgbox DewfordTown_Text_FishJudgeWeigh, MSGBOX_DEFAULT
	switch VAR_RESULT
	case 1, DewfordTown_EventScript_FishJudgeFirst
	case 2, DewfordTown_EventScript_FishJudgeSecond
	msgbox DewfordTown_Text_FishJudgeThird, MSGBOX_DEFAULT
	goto DewfordTown_EventScript_FishJudgeConsolation

DewfordTown_EventScript_FishJudgeSecond::
	msgbox DewfordTown_Text_FishJudgeSecond, MSGBOX_DEFAULT
	goto DewfordTown_EventScript_FishJudgeConsolation


DewfordTown_EventScript_FishJudgeRepeat::
	msgbox DewfordTown_Text_FishJudgeRepeat, MSGBOX_DEFAULT
	release
	end

DewfordTown_EventScript_FishJudgeNoFish::
	goto_if_eq VAR_0x8007, TRUE, DewfordTown_EventScript_FishJudgeNotAFish
	msgbox DewfordTown_Text_FishJudgeNoFish, MSGBOX_DEFAULT
	goto DewfordTown_EventScript_FishJudgeRules

DewfordTown_EventScript_FishJudgeNotAFish::
	msgbox DewfordTown_Text_FishJudgeNotAFish, MSGBOX_DEFAULT
DewfordTown_EventScript_FishJudgeRules::
	msgbox DewfordTown_Text_FishJudgeRules, MSGBOX_DEFAULT
	release
	end

DewfordTown_EventScript_FishJudgeAlreadyClaimed::
	msgbox DewfordTown_Text_FishJudgeAlreadyClaimed, MSGBOX_DEFAULT
	release
	end

DewfordTown_EventScript_FishJudgeConsolation::
	goto_if_eq VAR_0x8004, TRUE, DewfordTown_EventScript_FishJudgeAlreadyClaimed
	msgbox DewfordTown_Text_FishJudgeConsolation, MSGBOX_DEFAULT
	giveitem VAR_0x8005
	goto_if_eq VAR_RESULT, FALSE, Common_EventScript_ShowBagIsFull
	special FishTourney_ClaimPrize
	goto_if_eq VAR_0x8005, ITEM_LUCKY_EGG, DewfordTown_EventScript_FishJudgeLuckyEgg
	msgbox DewfordTown_Text_FishJudgeSeeYouNextWeek, MSGBOX_DEFAULT
	release
	end

DewfordTown_EventScript_FishJudgeLuckyEgg::
	msgbox DewfordTown_Text_FishJudgeLuckyEgg, MSGBOX_DEFAULT
	release
	end

DewfordTown_EventScript_FishJudgeFirst::
	msgbox DewfordTown_Text_FishJudgeFirst, MSGBOX_DEFAULT
	goto_if_eq VAR_0x8004, TRUE, DewfordTown_EventScript_FishJudgeAlreadyClaimed
	msgbox DewfordTown_Text_FishJudgeWinnerPrize, MSGBOX_DEFAULT
	giveitem VAR_0x8005
	goto_if_eq VAR_RESULT, FALSE, Common_EventScript_ShowBagIsFull
	special FishTourney_ClaimPrize
	goto_if_set FLAG_FISH_TOURNEY_TROPHY, DewfordTown_EventScript_FishJudgeNoConsolation
	msgbox DewfordTown_Text_FishJudgeTrophy, MSGBOX_DEFAULT
	givedecoration DECOR_SILVER_SHIELD
	goto_if_eq VAR_RESULT, FALSE, DewfordTown_EventScript_FishJudgeNoConsolation
	setflag FLAG_FISH_TOURNEY_TROPHY
DewfordTown_EventScript_FishJudgeNoConsolation::
	msgbox DewfordTown_Text_FishJudgeNoConsolation, MSGBOX_DEFAULT
	release
	end

DewfordTown_EventScript_FishBoaster::
	lock
	faceplayer
	special FishTourney_GetBoardInfo
	msgbox DewfordTown_Text_FishBoaster, MSGBOX_DEFAULT
	release
	end

DewfordTown_EventScript_FeebasMan::
	msgbox DewfordTown_Text_FeebasMan, MSGBOX_NPC
	end

DewfordTown_Text_FishJudgeIntro:
	.string "Welcome to the DEWFORD WEEKLY\n"
	.string "BIG CATCH. No rods, no reels, no\l"
	.string "skill. Only weight.\p"
	.string "This week's leader is a MAGIKARP\n"
	.string "weighing {STR_VAR_2}.\p"
	.string "Its owner:\n"
	.string "{STR_VAR_1}.\p"
	.string "Nobody knows how.\n"
	.string "We stopped asking.$"

DewfordTown_Text_FishJudgeRepeat:
	.string "Back again? {STR_VAR_1} still weighs\n"
	.string "{STR_VAR_2}. Still not a MAGIKARP.\p"
	.string "You got your prize this week.\n"
	.string "New contest next week.$"

DewfordTown_Text_FishJudgeNoFish:
	.string "I'd weigh your fish, but you don't have\n"
	.string "one.\p"
	.string "Bring a FISH. An actual fish. We had an\n"
	.string "incident.$"

DewfordTown_Text_FishJudgeNotAFish:
	.string "{STR_VAR_3}? …That is not a fish.\p"
	.string "The old rulebook said “anything wet”. I\n"
	.string "wrote it. I was drunk.\p"
	.string "Then someone brought a KYOGRE. The\n"
	.string "pier is still in Slateport.\p"
	.string "New rulebook. Sober edition.$"

DewfordTown_Text_FishJudgeRules:
	.string "OFFICIAL LIST OF FISH, page 1 of 1:\p"
	.string "MAGIKARP. GYARADOS (legally still a\n"
	.string "MAGIKARP). GOLDEEN, SEAKING, HORSEA,\l"
	.string "SEADRA, KINGDRA.\p"
	.string "Yes, seahorses are fish. I checked.\n"
	.string "Twice.\p"
	.string "CHINCHOU, LANTURN, QWILFISH, OVERQWIL,\n"
	.string "REMORAID, MANTYKE, MANTINE, CARVANHA,\l"
	.string "SHARPEDO.\p"
	.string "BARBOACH, WHISCASH, FEEBAS, MILOTIC (a\n"
	.string "fish with a skincare routine), HUNTAIL,\l"
	.string "GOREBYSS.\p"
	.string "RELICANTH, LUVDISC, FINNEON, LUMINEON,\n"
	.string "BASCULIN, BASCULEGION, ALOMOMOLA,\l"
	.string "WISHIWASHI, BRUXISH.\p"
	.string "ARROKUDA, BARRASKEWDA, VELUZA,\n"
	.string "DONDOZO, ARCTOVISH, DRACOVISH. And\l"
	.string "STUNFISK. It's a flatfish. Look it up.\p"
	.string "NOT fish: whales, clams, crabs, turtles,\n"
	.string "ducks, dolphins, octopi and sea gods.\l"
	.string "Jellyfish are not fish. It's in the name.\l"
	.string "The name lies.\p"
	.string "OCTILLERY evolves from REMORAID. I\n"
	.string "don't want to talk about it.$"

DewfordTown_Text_FishJudgeWeigh:
	.string "Let's put {STR_VAR_1} on the scale…\p"
	.string "{STR_VAR_1}: {STR_VAR_2}!$"

DewfordTown_Text_FishJudgeSecond:
	.string "Second place! Beaten by a\n"
	.string "MAGIKARP. Like everyone. Always.$"

DewfordTown_Text_FishJudgeThird:
	.string "Third place. Behind a MAGIKARP\n"
	.string "and behind THAT guy.\p"
	.string "He's going to talk about this\n"
	.string "for weeks.$"

DewfordTown_Text_FishJudgeFirst:
	.string "…It's heavier than the MAGIKARP.\p"
	.string "That's not possible. The scale\n"
	.string "must be broken. Or reality.\p"
	.string "Fine. First place.\n"
	.string "The MAGIKARP stays on the board,\l"
	.string "though. Out of respect.$"

DewfordTown_Text_FishJudgeWinnerPrize:
	.string "The grand prize: one (1) POKé BALL.\n"
	.string "Try not to spend it all at once.$"

DewfordTown_Text_FishJudgeTrophy:
	.string "And a trophy. It's not real silver.\n"
	.string "Nothing here is real.$"

DewfordTown_Text_FishJudgeNoConsolation:
	.string "Winners don't get a consolation\n"
	.string "prize. Rules are rules.\p"
	.string "The losers got better stuff.\n"
	.string "Don't think about it.$"

DewfordTown_Text_FishJudgeConsolation:
	.string "Everyone who loses to a MAGIKARP\n"
	.string "gets a consolation prize.\p"
	.string "Don't tell the winners.$"

DewfordTown_Text_FishJudgeLuckyEgg:
	.string "That egg is worth more than first\n"
	.string "place ever was.\p"
	.string "Next week the consolation prizes\n"
	.string "get smaller. Budget cuts.$"

DewfordTown_Text_FishJudgeSeeYouNextWeek:
	.string "New contest next week.\n"
	.string "Same MAGIKARP energy.$"

DewfordTown_Text_FishJudgeAlreadyClaimed:
	.string "You already got your prize this\n"
	.string "week. Come back next week.\p"
	.string "There will be a new MAGIKARP.\n"
	.string "There's always a new MAGIKARP.$"

DewfordTown_Text_FishBoaster:
	.string "My {STR_VAR_3}.\n"
	.string "Second place, baby!\p"
	.string "First place? A MAGIKARP.\n"
	.string "Doesn't count. MAGIKARP is\l"
	.string "basically water with eyes.\p"
	.string "I've been second place 312 weeks\n"
	.string "in a row. That's a record too.$"

DewfordTown_Text_FeebasMan:
	.string "Forty years I've been fishing under\n"
	.string "this pier for a FEEBAS.\p"
	.string "My wife left. My kids left.\n"
	.string "My rod left, somehow.\p"
	.string "But I can feel it. Today's the day.\n"
	.string "It's been the day for forty years.$"
