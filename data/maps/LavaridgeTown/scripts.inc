LavaridgeTown_MapScripts::
	map_script MAP_SCRIPT_ON_TRANSITION, LavaridgeTown_OnTransition
	map_script MAP_SCRIPT_ON_FRAME_TABLE, LavaridgeTown_OnFrame
	.byte 0

LavaridgeTown_OnTransition:
	setflag FLAG_VISITED_LAVARIDGE_TOWN
	call_if_set FLAG_WHITEOUT_TO_LAVARIDGE, LavaridgeTown_EventScript_ClearLavaridgeWhiteOut
	call_if_set FLAG_DEFEATED_EVIL_TEAM_MT_CHIMNEY, LavaridgeTown_EventScript_ShowMtChimneyTrainers
	call Common_EventScript_SetupRivalGfxId
	call Common_EventScript_SetupRivalOnBikeGfxId
	call_if_eq VAR_LAVARIDGE_TOWN_STATE, 1, LavaridgeTown_EventScript_CheckSetRivalPos
	call_if_eq VAR_LAVARIDGE_TOWN_STATE, 1, LavaridgeTown_EventScript_HideMapNamePopup
	end

LavaridgeTown_EventScript_ClearLavaridgeWhiteOut::
	clearflag FLAG_WHITEOUT_TO_LAVARIDGE
	return

LavaridgeTown_EventScript_CheckSetRivalPos::
	getplayerxy VAR_0x8004, VAR_0x8005
	goto_if_eq VAR_0x8004, 9, LavaridgeTown_EventScript_SetRivalPos
	return

LavaridgeTown_EventScript_SetRivalPos::
	setobjectxyperm LOCALID_LAVARIDGE_RIVAL, 11, 9
	setobjectxyperm LOCALID_LAVARIDGE_RIVAL_ON_BIKE, 9, 8
	setobjectmovementtype LOCALID_LAVARIDGE_RIVAL_ON_BIKE, MOVEMENT_TYPE_FACE_UP
	clearflag FLAG_HIDE_LAVARIDGE_TOWN_RIVAL
	return

LavaridgeTown_EventScript_ShowMtChimneyTrainers::
	clearflag FLAG_HIDE_MT_CHIMNEY_TRAINERS
	return

LavaridgeTown_EventScript_HideMapNamePopup::
	setflag FLAG_HIDE_MAP_NAME_POPUP
	return

LavaridgeTown_OnFrame:
	map_script_2 VAR_LAVARIDGE_TOWN_STATE, 1, LavaridgeTown_EventScript_RivalGiveGoGoggles
	.2byte 0

LavaridgeTown_EventScript_RivalGiveGoGoggles::
	lockall
	getplayerxy VAR_0x8008, VAR_0x8009
	call_if_eq VAR_0x8008, 9, LavaridgeTown_EventScript_RivalNoticePlayer
	call_if_ne VAR_0x8008, 9, LavaridgeTown_EventScript_RivalExitHerbShop
	delay 20
	checkplayergender
	call_if_eq VAR_RESULT, MALE, LavaridgeTown_EventScript_PlayMayMusic
	call_if_eq VAR_RESULT, FEMALE, LavaridgeTown_EventScript_PlayBrendanMusic
	call_if_eq VAR_0x8008, 9, LavaridgeTown_EventScript_RivalApproachPlayer1
	call_if_ne VAR_0x8008, 9, LavaridgeTown_EventScript_RivalApproachPlayer2
	checkplayergender
	goto_if_eq VAR_RESULT, MALE, LavaridgeTown_EventScript_MayGiveGoGoggles
	goto_if_eq VAR_RESULT, FEMALE, LavaridgeTown_EventScript_BrendanGiveGoGoggles
	end

LavaridgeTown_EventScript_MayGiveGoGoggles::
	msgbox LavaridgeTown_Text_MayNiceBadgesTakeThis, MSGBOX_DEFAULT
	giveitem ITEM_GO_GOGGLES
	setflag FLAG_RECEIVED_GO_GOGGLES
	msgbox LavaridgeTown_Text_MayExplainGoGogglesChallengeDad, MSGBOX_DEFAULT
	goto LavaridgeTown_EventScript_RivalExit
	end

LavaridgeTown_EventScript_BrendanGiveGoGoggles::
	msgbox LavaridgeTown_Text_BrendanNiceBadgesTakeThis, MSGBOX_DEFAULT
	giveitem ITEM_GO_GOGGLES
	setflag FLAG_RECEIVED_GO_GOGGLES
	msgbox LavaridgeTown_Text_BrendanExplainGoGogglesChallengeDad, MSGBOX_DEFAULT
	goto LavaridgeTown_EventScript_RivalExit
	end

LavaridgeTown_EventScript_RivalExit::
	closemessage
	removeobject LOCALID_LAVARIDGE_RIVAL
	addobject LOCALID_LAVARIDGE_RIVAL_ON_BIKE
	delay 30
	call_if_eq VAR_0x8008, 9, LavaridgeTown_EventScript_RivalExit1
	call_if_ne VAR_0x8008, 9, LavaridgeTown_EventScript_RivalExit2
	removeobject LOCALID_LAVARIDGE_RIVAL_ON_BIKE
	setvar VAR_LAVARIDGE_TOWN_STATE, 2
	clearflag FLAG_HIDE_MAP_NAME_POPUP
	savebgm MUS_DUMMY
	fadedefaultbgm
	releaseall
	end

LavaridgeTown_EventScript_PlayMayMusic::
	playbgm MUS_ENCOUNTER_MAY, TRUE
	return

LavaridgeTown_EventScript_PlayBrendanMusic::
	playbgm MUS_ENCOUNTER_BRENDAN, TRUE
	return

LavaridgeTown_EventScript_RivalNoticePlayer::
	applymovement LOCALID_LAVARIDGE_RIVAL, Common_Movement_WalkInPlaceFasterUp
	waitmovement 0
	playse SE_PIN
	applymovement LOCALID_LAVARIDGE_RIVAL, Common_Movement_ExclamationMark
	waitmovement 0
	applymovement LOCALID_LAVARIDGE_RIVAL, Common_Movement_Delay48
	waitmovement 0
	return

LavaridgeTown_EventScript_RivalExitHerbShop::
	opendoor 12, 15
	waitdooranim
	addobject LOCALID_LAVARIDGE_RIVAL
	applymovement LOCALID_LAVARIDGE_RIVAL, LavaridgeTown_Movement_RivalExitHerbShop
	waitmovement 0
	closedoor 12, 15
	waitdooranim
	applymovement LOCALID_LAVARIDGE_RIVAL, Common_Movement_WalkInPlaceFasterLeft
	waitmovement 0
	playse SE_PIN
	applymovement LOCALID_LAVARIDGE_RIVAL, Common_Movement_ExclamationMark
	waitmovement 0
	applymovement LOCALID_LAVARIDGE_RIVAL, Common_Movement_Delay48
	waitmovement 0
	applymovement LOCALID_PLAYER, Common_Movement_WalkInPlaceFasterRight
	waitmovement 0
	return

LavaridgeTown_EventScript_RivalApproachPlayer1::
	applymovement LOCALID_LAVARIDGE_RIVAL, LavaridgeTown_Movement_RivalApproachPlayer1
	waitmovement 0
	return

LavaridgeTown_EventScript_RivalApproachPlayer2::
	applymovement LOCALID_LAVARIDGE_RIVAL, LavaridgeTown_Movement_RivalApproachPlayer2
	waitmovement 0
	return

LavaridgeTown_EventScript_RivalExit1::
	applymovement LOCALID_PLAYER, LavaridgeTown_Movement_PlayerWatchRivalExit
	applymovement LOCALID_LAVARIDGE_RIVAL_ON_BIKE, LavaridgeTown_Movement_RivalExit1
	waitmovement 0
	return

LavaridgeTown_EventScript_RivalExit2::
	applymovement LOCALID_LAVARIDGE_RIVAL_ON_BIKE, LavaridgeTown_Movement_RivalExit2
	waitmovement 0
	return

LavaridgeTown_Movement_RivalExit2:
	walk_fast_right
	walk_fast_right
	walk_fast_right
	walk_fast_up
	walk_fast_up
	walk_fast_up
	walk_fast_up
	walk_fast_up
	walk_fast_up
	walk_fast_up
	step_end

LavaridgeTown_Movement_PlayerWatchRivalExit:
	delay_16
	delay_8
	walk_in_place_faster_right
	step_end

LavaridgeTown_Movement_RivalExit1:
	walk_fast_down
	walk_fast_right
	walk_fast_right
	walk_fast_right
	walk_fast_right
	walk_fast_right
	walk_fast_right
	walk_fast_right
	walk_fast_right
	step_end

LavaridgeTown_Movement_RivalApproachPlayer2:
	walk_left
	walk_left
	walk_left
	walk_left
	walk_left
	walk_left
	step_end

LavaridgeTown_Movement_RivalApproachPlayer1:
	walk_left
	walk_left
	walk_up
	step_end

LavaridgeTown_Movement_RivalExitHerbShop:
	walk_down
	step_end

LavaridgeTown_EventScript_HotSpringsTrigger::
	specialvar VAR_RESULT, GetPlayerFacingDirection
	goto_if_eq VAR_RESULT, DIR_SOUTH, LavaridgeTown_EventScript_EnteredHotSprings
	end

LavaridgeTown_EventScript_EnteredHotSprings::
	incrementgamestat GAME_STAT_ENTERED_HOT_SPRINGS
	end

LavaridgeTown_EventScript_ExpertM::
	msgbox LavaridgeTown_Text_HotSpringsNeverRunDry, MSGBOX_NPC
	end

LavaridgeTown_EventScript_OldMan::
	msgbox LavaridgeTown_Text_PokemonNippedBackside, MSGBOX_SIGN
	end

LavaridgeTown_EventScript_Twin::
	msgbox LavaridgeTown_Text_BatheInHotSpringsEveryDay, MSGBOX_NPC
	end

LavaridgeTown_EventScript_HotSpringsOldWoman1::
	msgbox LavaridgeTown_Text_IfPokemonInHotSprings, MSGBOX_NPC
	end

LavaridgeTown_EventScript_HotSpringsOldWoman2::
	msgbox LavaridgeTown_Text_HotSpringsClaims, MSGBOX_NPC
	end

LavaridgeTown_EventScript_ExpertF::
	msgbox LavaridgeTown_Text_OhYouLikeHotSprings, MSGBOX_NPC
	end

LavaridgeTown_EventScript_EggWoman::
	lock
	faceplayer
	goto_if_set FLAG_RECEIVED_LAVARIDGE_EGG, LavaridgeTown_EventScript_ReceivedEgg
	msgbox LavaridgeTown_Text_HaveEggWillYouTakeIt, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, LavaridgeTown_EventScript_DeclineEgg
	getpartysize
	goto_if_eq VAR_RESULT, PARTY_SIZE, LavaridgeTown_EventScript_NoRoomForEgg
	msgbox LavaridgeTown_Text_HopeYoullWalkPlentyWithEgg, MSGBOX_DEFAULT
	setflag FLAG_RECEIVED_LAVARIDGE_EGG
	playfanfare MUS_OBTAIN_ITEM
	message LavaridgeTown_Text_ReceivedTheEgg
	waitfanfare
	call LavaridgeTown_EventScript_GiveOddEgg
	release
	end

@ Project Grounded: een "Odd Egg" zoals in Crystal. Eén van 8 soorten (elk 1/8), 50% kans op shiny.
LavaridgeTown_EventScript_GiveOddEgg::
	random 8
	switch VAR_RESULT
	case 0, LavaridgeTown_EventScript_OddEggLarvesta
	case 1, LavaridgeTown_EventScript_OddEggDeino
	case 2, LavaridgeTown_EventScript_OddEggLitwick
	case 3, LavaridgeTown_EventScript_OddEggFuecoco
	case 4, LavaridgeTown_EventScript_OddEggManaphy
	case 5, LavaridgeTown_EventScript_OddEggTogepi
	case 6, LavaridgeTown_EventScript_OddEggFerroseed
	giveegg SPECIES_TOXEL
	goto LavaridgeTown_EventScript_OddEggShiny
LavaridgeTown_EventScript_OddEggLarvesta::
	giveegg SPECIES_LARVESTA
	goto LavaridgeTown_EventScript_OddEggShiny
LavaridgeTown_EventScript_OddEggDeino::
	giveegg SPECIES_DEINO
	goto LavaridgeTown_EventScript_OddEggShiny
LavaridgeTown_EventScript_OddEggLitwick::
	giveegg SPECIES_LITWICK
	goto LavaridgeTown_EventScript_OddEggShiny
LavaridgeTown_EventScript_OddEggFuecoco::
	giveegg SPECIES_FUECOCO
	goto LavaridgeTown_EventScript_OddEggShiny
LavaridgeTown_EventScript_OddEggManaphy::
	giveegg SPECIES_MANAPHY
	goto LavaridgeTown_EventScript_OddEggShiny
LavaridgeTown_EventScript_OddEggTogepi::
	giveegg SPECIES_TOGEPI
	goto LavaridgeTown_EventScript_OddEggShiny
LavaridgeTown_EventScript_OddEggFerroseed::
	giveegg SPECIES_FERROSEED
LavaridgeTown_EventScript_OddEggShiny::
	random 2
	goto_if_eq VAR_RESULT, 0, Common_EventScript_NopReturn
	special SetLastPartyMonShiny
	return

LavaridgeTown_EventScript_ReceivedEgg::
	msgbox LavaridgeTown_Text_EverySoOftenEggFoundAtDayCare, MSGBOX_DEFAULT
	release
	end

LavaridgeTown_EventScript_NoRoomForEgg::
	msgbox LavaridgeTown_Text_NoRoomForThisEgg, MSGBOX_DEFAULT
	release
	end

LavaridgeTown_EventScript_DeclineEgg::
	msgbox LavaridgeTown_Text_AsYouWishThen, MSGBOX_DEFAULT
	release
	end

LavaridgeTown_EventScript_TownSign::
	msgbox LavaridgeTown_Text_TownSign, MSGBOX_SIGN
	end

LavaridgeTown_EventScript_GymSign::
	msgbox LavaridgeTown_Text_GymSign, MSGBOX_SIGN
	end

LavaridgeTown_EventScript_HerbShopSign::
	msgbox LavaridgeTown_Text_HerbShopSign, MSGBOX_SIGN
	end

LavaridgeTown_Text_MayNiceBadgesTakeThis:
	.string "MAY: {PLAYER}{KUN}! Long time!\p"
	.string "You got the LAVARIDGE BADGE while I\n"
	.string "was in the hot springs?\p"
	.string "You didn't just catch strong POKéMON.\n"
	.string "You raised them. Ugh.\p"
	.string "Fine. You can have this.$"

LavaridgeTown_Text_MayExplainGoGogglesChallengeDad:
	.string "MAY: With those GO-GOGGLES, the desert\n"
	.string "near ROUTE 111 is no problem.\p"
	.string "But wow, {PLAYER}{KUN}… GYMS…\p"
	.string "You're only doing this so you don't lose\n"
	.string "to me.\p"
	.string "I'm going to challenge your dad in\n"
	.string "PETALBURG. See ya!$"

LavaridgeTown_Text_BrendanNiceBadgesTakeThis:
	.string "BRENDAN: {PLAYER}, hey. Been a while.\p"
	.string "Hmm… Decent BADGE collection.\p"
	.string "Fine. You can have this.$"

LavaridgeTown_Text_BrendanExplainGoGogglesChallengeDad:
	.string "BRENDAN: Take these into the desert\n"
	.string "near ROUTE 111.\p"
	.string "Some POKéMON only live there. Look\n"
	.string "around.\p"
	.string "Me? I'm going to challenge NORMAN in\n"
	.string "PETALBURG.\p"
	.string "Your dad actually looks tough. Unlike\n"
	.string "you.\p"
	.string "See ya!$"

LavaridgeTown_Text_HaveEggWillYouTakeIt:
	.string "I have an EGG. Tried hatching it in hot\n"
	.string "sand. It's too odd for me.\p"
	.string "Could be anything. I'm scared of it. Will\n"
	.string "you take it?$"

LavaridgeTown_Text_HopeYoullWalkPlentyWithEgg:
	.string "Good! Walk plenty with it. And don't\n"
	.string "blame me for what comes out.$"

LavaridgeTown_Text_ReceivedTheEgg:
	.string "{PLAYER} received the EGG.$"

LavaridgeTown_Text_NoRoomForThisEgg:
	.string "You have too many POKéMON.\p"
	.string "No room for the EGG. Make room. It's\n"
	.string "worth it.$"

LavaridgeTown_Text_AsYouWishThen:
	.string "As you wish… It'll hatch into something\n"
	.string "weird anyway.$"

LavaridgeTown_Text_EverySoOftenEggFoundAtDayCare:
	.string "Every so often an EGG turns up at the\n"
	.string "DAY CARE. Nobody knows how. We don't\l"
	.string "ask.$"

LavaridgeTown_Text_HotSpringsNeverRunDry:
	.string "We take all the hot water we want, and\n"
	.string "the springs never run dry.\p"
	.string "It's magma. Heating water. Under our\n"
	.string "feet.\p"
	.string "Don't think about it too much.$"

LavaridgeTown_Text_PokemonNippedBackside:
	.string "Being buried in hot sand… So warm…\p"
	.string "Eh? Gyaah! Ouch!\p"
	.string "A POKéMON bit my behind! Again!$"

LavaridgeTown_Text_OhYouLikeHotSprings:
	.string "You like hot springs? At your age?\p"
	.string "Wait until your back starts talking to\n"
	.string "you.$"

LavaridgeTown_Text_BatheInHotSpringsEveryDay:
	.string "I bathe in the hot springs every day.\p"
	.string "I want to be a GYM LEADER like\n"
	.string "FLANNERY.\p"
	.string "Mom says I also need to shower\n"
	.string "sometimes. Like FLANNERY doesn't.$"

LavaridgeTown_Text_IfPokemonInHotSprings:
	.string "Life hasn't been the same since\n"
	.string "MICHAEL JACKSON died.$"

LavaridgeTown_Text_HotSpringsClaims:
	.string "Come on, it's been 17 years.$"

LavaridgeTown_Text_TownSign:
	.string "LAVARIDGE TOWN\p"
	.string "“HEAL. FIGHT. FAINT. WHAT A LIFE.”$"

LavaridgeTown_Text_GymSign:
	.string "LAVARIDGE TOWN POKéMON GYM\n"
	.string "LEADER: FLANNERY\p"
	.string "“Off the grid. No WiFi. Just raw,\n"
	.string "unwashed heat!”$"

LavaridgeTown_Text_HerbShopSign:
	.string "POKéMON HERB SHOP\n"
	.string "“Bitter taste--better cure! Your\l"
	.string "POKéMON will hate you.”$"

