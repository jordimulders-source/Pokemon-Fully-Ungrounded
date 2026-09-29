DewfordTown_Hall_MapScripts::
	.byte 0

DewfordTown_Hall_EventScript_Girl::
	lock
	faceplayer
	call Common_EventScript_BufferTrendyPhrase
	special IsTrendyPhraseBoring
	goto_if_eq VAR_RESULT, TRUE, DewfordTown_Hall_EventScript_GirlBoredOfTrend
	msgbox DewfordTown_Hall_Text_CantImagineLifeWithoutTrend, MSGBOX_DEFAULT
	release
	end

DewfordTown_Hall_EventScript_GirlBoredOfTrend::
	msgbox DewfordTown_Hall_Text_GettingBoredOfTrend, MSGBOX_DEFAULT
	release
	end

DewfordTown_Hall_EventScript_Woman::
	lock
	faceplayer
	call Common_EventScript_BufferTrendyPhrase
	msgbox DewfordTown_Hall_Text_TeachingMonAboutTrend, MSGBOX_DEFAULT
	release
	end

DewfordTown_Hall_EventScript_Man::
	lock
	faceplayer
	call Common_EventScript_BufferTrendyPhrase
	special BufferDeepLinkPhrase
	msgbox DewfordTown_Hall_Text_DeepLinkBetweenXAndY, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, YES, DewfordTown_Hall_EventScript_ConfirmTrendLink
	goto_if_eq VAR_RESULT, NO, DewfordTown_Hall_EventScript_RejectTrendLink
	end

DewfordTown_Hall_EventScript_ConfirmTrendLink::
	msgbox DewfordTown_Hall_Text_MyHunchWasRight, MSGBOX_DEFAULT
	release
	end

DewfordTown_Hall_EventScript_RejectTrendLink::
	msgbox DewfordTown_Hall_Text_NotEasyToKeepUp, MSGBOX_DEFAULT
	release
	end

DewfordTown_Hall_EventScript_ExpertM::
	lock
	faceplayer
	call Common_EventScript_BufferTrendyPhrase
	msgbox DewfordTown_Hall_Text_TVShowAboutTrend, MSGBOX_DEFAULT
	closemessage
	applymovement LOCALID_DEWFORD_HALL_EXPERT_M, Common_Movement_WalkInPlaceFasterUp
	waitmovement 0
	release
	end

DewfordTown_Hall_EventScript_Twin::
	lock
	faceplayer
	call Common_EventScript_BufferTrendyPhrase
	msgbox DewfordTown_Hall_Text_IsTrendMorePopularAcrossSea, MSGBOX_DEFAULT
	closemessage
	applymovement LOCALID_DEWFORD_HALL_TWIN, Common_Movement_WalkInPlaceFasterUp
	waitmovement 0
	release
	end

DewfordTown_Hall_EventScript_LittleBoy::
	lock
	faceplayer
	call Common_EventScript_BufferTrendyPhrase
	msgbox DewfordTown_Hall_Text_CollectTrendMerchandise, MSGBOX_DEFAULT
	release
	end

DewfordTown_Hall_EventScript_Bookshelf::
	lockall
	call Common_EventScript_BufferTrendyPhrase
	msgbox DewfordTown_Hall_Text_BooksAboutTrend, MSGBOX_DEFAULT
	releaseall
	end

DewfordTown_Hall_EventScript_Painting::
	lockall
	call Common_EventScript_BufferTrendyPhrase
	special GetDewfordHallPaintingNameIndex
	switch VAR_RESULT
	case 0, DewfordTown_Hall_EventScript_ScreamTitle
	case 4, DewfordTown_Hall_EventScript_ScreamTitle
	case 1, DewfordTown_Hall_EventScript_SmileTitle
	case 5, DewfordTown_Hall_EventScript_ScreamTitle
	case 2, DewfordTown_Hall_EventScript_LastTitle
	case 6, DewfordTown_Hall_EventScript_LastTitle
	case 3, DewfordTown_Hall_EventScript_BirthTitle
	case 7, DewfordTown_Hall_EventScript_LastTitle
	end

DewfordTown_Hall_EventScript_ScreamTitle::
	msgbox DewfordTown_Hall_Text_TrendsScream, MSGBOX_DEFAULT
	releaseall
	end

DewfordTown_Hall_EventScript_SmileTitle::
	msgbox DewfordTown_Hall_Text_TrendsSmile, MSGBOX_DEFAULT
	releaseall
	end

DewfordTown_Hall_EventScript_LastTitle::
	msgbox DewfordTown_Hall_Text_LastTrend, MSGBOX_DEFAULT
	releaseall
	end

DewfordTown_Hall_EventScript_BirthTitle::
	msgbox DewfordTown_Hall_Text_BirthOfTrend, MSGBOX_DEFAULT
	releaseall
	end

DewfordTown_Hall_EventScript_SchoolKidM::
	lockall
	setvar VAR_0x8008, 0
	goto DewfordTown_Hall_EventScript_DoTrendDebate
	end

DewfordTown_Hall_EventScript_PsychicM::
	lockall
	setvar VAR_0x8008, 1
	goto DewfordTown_Hall_EventScript_DoTrendDebate
	end

DewfordTown_Hall_EventScript_DoTrendDebate::
	call Common_EventScript_BufferTrendyPhrase
	special GetDewfordHallPaintingNameIndex
	switch VAR_RESULT
	case 0, DewfordTown_Hall_EventScript_TrendDebate1
	case 1, DewfordTown_Hall_EventScript_TrendDebate1
	case 2, DewfordTown_Hall_EventScript_TrendDebate2
	case 3, DewfordTown_Hall_EventScript_TrendDebate2
	case 4, DewfordTown_Hall_EventScript_TrendDebate3
	case 5, DewfordTown_Hall_EventScript_TrendDebate3
	case 6, DewfordTown_Hall_EventScript_TrendDebate4
	case 7, DewfordTown_Hall_EventScript_TrendDebate5
	end

DewfordTown_Hall_EventScript_TrendDebate1::
	call DewfordTown_Hall_EventScript_DebateReact1
	msgbox DewfordTown_Hall_Text_SawTrendCoolestThing, MSGBOX_DEFAULT
	call DewfordTown_Hall_EventScript_DebateReact2
	msgbox DewfordTown_Hall_Text_AllegedTrendNotAuthentic, MSGBOX_DEFAULT
	releaseall
	end

DewfordTown_Hall_EventScript_TrendDebate2::
	call DewfordTown_Hall_EventScript_DebateReact1
	msgbox DewfordTown_Hall_Text_ComposedTrendThemeSong, MSGBOX_DEFAULT
	call DewfordTown_Hall_EventScript_DebateReact2
	msgbox DewfordTown_Hall_Text_WorkOnYourSinging, MSGBOX_DEFAULT
	releaseall
	end

DewfordTown_Hall_EventScript_TrendDebate3::
	call DewfordTown_Hall_EventScript_DebateReact1
	msgbox DewfordTown_Hall_Text_OrganizeTrendParty, MSGBOX_DEFAULT
	call DewfordTown_Hall_EventScript_DebateReact2
	msgbox DewfordTown_Hall_Text_BrilliantIndeed, MSGBOX_DEFAULT
	releaseall
	end

DewfordTown_Hall_EventScript_TrendDebate4::
	call DewfordTown_Hall_EventScript_DebateReact1
	msgbox DewfordTown_Hall_Text_TrendHasBecomePartOfLife, MSGBOX_DEFAULT
	call DewfordTown_Hall_EventScript_DebateReact2
	msgbox DewfordTown_Hall_Text_TrendWeighsHeavilyOnMind, MSGBOX_DEFAULT
	releaseall
	end

DewfordTown_Hall_EventScript_TrendDebate5::
	call DewfordTown_Hall_EventScript_DebateReact1
	msgbox DewfordTown_Hall_Text_IfWeTeamUpWellBeInvincible, MSGBOX_DEFAULT
	call DewfordTown_Hall_EventScript_DebateReact2
	msgbox DewfordTown_Hall_Text_WellBeTrendDuo, MSGBOX_DEFAULT
	releaseall
	end

DewfordTown_Hall_EventScript_DontMovePlayer1::
	return

DewfordTown_Hall_EventScript_DebateReact1::
	applymovement LOCALID_DEWFORD_HALL_PSYCHIC_M, DewfordTown_Hall_Movement_PsychicWalkInPlaceLeft
	waitmovement 0
	goto_if_eq VAR_0x8008, 0, DewfordTown_Hall_EventScript_PlayerReactWest
	goto_if_eq VAR_0x8008, 1, DewfordTown_Hall_EventScript_DontMovePlayer2
	end

DewfordTown_Hall_EventScript_PlayerReactWest::
	goto_if_eq VAR_FACING, DIR_EAST, DewfordTown_Hall_EventScript_DontMovePlayer1
	applymovement LOCALID_PLAYER, Common_Movement_WalkInPlaceFasterRight
	waitmovement 0
	return

DewfordTown_Hall_EventScript_DontMovePlayer2::
	return

DewfordTown_Hall_EventScript_DebateReact2::
	applymovement LOCALID_DEWFORD_HALL_SCHOOL_KID_M, DewfordTown_Hall_Movement_SchoolKidWalkInPlaceRight
	waitmovement 0
	goto_if_eq VAR_0x8008, 0, DewfordTown_Hall_EventScript_PlayerReactNorthSouth
	goto_if_eq VAR_0x8008, 1, DewfordTown_Hall_EventScript_PlayerReactEast
	end

DewfordTown_Hall_EventScript_PlayerReactNorthSouth::
	call_if_eq VAR_FACING, DIR_NORTH, DewfordTown_Hall_EventScript_PlayerWalkInPlaceUp
	call_if_eq VAR_FACING, DIR_SOUTH, DewfordTown_Hall_EventScript_PlayerWalkInPlaceDown
	return

DewfordTown_Hall_EventScript_PlayerWalkInPlaceUp::
	applymovement LOCALID_PLAYER, Common_Movement_WalkInPlaceFasterUp
	waitmovement 0
	return

DewfordTown_Hall_EventScript_PlayerWalkInPlaceDown::
	applymovement LOCALID_PLAYER, Common_Movement_WalkInPlaceFasterDown
	waitmovement 0
	return

DewfordTown_Hall_EventScript_PlayerReactEast::
	goto_if_eq VAR_FACING, DIR_WEST, DewfordTown_Hall_EventScript_DontMovePlayer1
	applymovement LOCALID_PLAYER, Common_Movement_WalkInPlaceFasterLeft
	waitmovement 0
	return

DewfordTown_Hall_Movement_PsychicWalkInPlaceLeft:
	walk_in_place_left
	step_end

DewfordTown_Hall_Movement_SchoolKidWalkInPlaceRight:
	walk_in_place_right
	step_end

DewfordTown_Hall_EventScript_SludgeBombMan::
	lock
	faceplayer
	call Common_EventScript_BufferTrendyPhrase
	goto_if_set FLAG_RECEIVED_TM_SLUDGE_BOMB, DewfordTown_Hall_EventScript_ReceivedSludgeBomb
	msgbox DewfordTown_Hall_Text_GiveYouSludgeBomb, MSGBOX_DEFAULT
	giveitem ITEM_TM_SLUDGE_BOMB
	goto_if_eq VAR_RESULT, FALSE, Common_EventScript_ShowBagIsFull
	setflag FLAG_RECEIVED_TM_SLUDGE_BOMB
	release
	end

DewfordTown_Hall_EventScript_ReceivedSludgeBomb::
	msgbox DewfordTown_Hall_Text_LoveSludgeBombButTrendInToo, MSGBOX_DEFAULT
	release
	end

DewfordTown_Hall_Text_CantImagineLifeWithoutTrend:
	.string "What's in vogue? “{STR_VAR_1}”! Obviously!\p"
	.string "I can't imagine life without “{STR_VAR_1}”!\p"
	.string "I've said that about 40 trends this\n"
	.string "year.$"

DewfordTown_Hall_Text_GettingBoredOfTrend:
	.string "What's in vogue? “{STR_VAR_1}”!\p"
	.string "But I'm kind of over it already.\p"
	.string "On to the next thing.$"

DewfordTown_Hall_Text_TeachingMonAboutTrend:
	.string "I'm teaching my POKéMON about\n"
	.string "“{STR_VAR_1}.”\p"
	.string "It bit me.$"

DewfordTown_Hall_Text_DeepLinkBetweenXAndY:
	.string "I'm researching “{STR_VAR_1}.”\p"
	.string "Is there a deep link between “{STR_VAR_1}”\n"
	.string "and “{STR_VAR_2}”?\p"
	.string "I heard it on a podcast. Six hours long.$"

DewfordTown_Hall_Text_MyHunchWasRight:
	.string "Oh! My hunch was right!\p"
	.string "I'm one step closer to being hip, yowza!$"

DewfordTown_Hall_Text_NotEasyToKeepUp:
	.string "What?! Really?!\p"
	.string "It's hard for an old guy like me to keep\n"
	.string "up!\p"
	.string "I just learned what a meme is.$"

DewfordTown_Hall_Text_TVShowAboutTrend:
	.string "“{STR_VAR_1}”…\p"
	.string "Isn't there a TV show on it? Season 7\n"
	.string "was bad.$"

DewfordTown_Hall_Text_IsTrendMorePopularAcrossSea:
	.string "Across the sea…\p"
	.string "Is “{STR_VAR_1}” even more popular?\p"
	.string "They always get everything first.$"

DewfordTown_Hall_Text_CollectTrendMerchandise:
	.string "I collect official “{STR_VAR_1}”\n"
	.string "merchandise.\p"
	.string "DOLLS… Clothing… Picture books…\p"
	.string "My parents are broke. I'm not sharing!$"

DewfordTown_Hall_Text_BooksAboutTrend:
	.string "GOOD “{STR_VAR_1}” & BAD “{STR_VAR_1}”…\p"
	.string "“{STR_VAR_1}” FOR DUMMIES…\p"
	.string "The shelf is full of books about\n"
	.string "“{STR_VAR_1}.” None were read.$"

DewfordTown_Hall_Text_TrendsScream:
	.string "“{STR_VAR_1}'S SCREAM” is the title.\p"
	.string "It's a horror novel.$"

DewfordTown_Hall_Text_TrendsSmile:
	.string "“{STR_VAR_1}'S SMILE” is the title.\p"
	.string "It's a self-help book.$"

DewfordTown_Hall_Text_LastTrend:
	.string "It's titled “THE LAST {STR_VAR_1}.”\p"
	.string "There's a sequel.$"

DewfordTown_Hall_Text_BirthOfTrend:
	.string "It's titled “THE BIRTH OF {STR_VAR_1}.”\p"
	.string "It's a prequel.$"

DewfordTown_Hall_Text_SawTrendCoolestThing:
	.string "I saw “{STR_VAR_1}”! Cool, huh?\p"
	.string "The coolest thing ever! The real thing!\p"
	.string "I posted it everywhere.$"

DewfordTown_Hall_Text_AllegedTrendNotAuthentic:
	.string "Oh, no, no, no.\p"
	.string "That “{STR_VAR_1}” you saw? Fake.\p"
	.string "The real one is sharper, yet more mellow.\p"
	.string "I've never seen it either. But I know.$"

DewfordTown_Hall_Text_ComposedTrendThemeSong:
	.string "Listen, I wrote a theme song for\n"
	.string "“{STR_VAR_1}.”\p"
	.string "Okay, here it goes! … …\p"
	.string "Oh! {STR_VAR_1}!\p"
	.string "Wonderful {STR_VAR_1}!\p"
	.string "That's the whole song.$"

DewfordTown_Hall_Text_WorkOnYourSinging:
	.string "… …\p"
	.string "Chap, work on your singing before you\n"
	.string "trifle with “{STR_VAR_1}.”\p"
	.string "My ears are bleeding.$"

DewfordTown_Hall_Text_OrganizeTrendParty:
	.string "As I was saying, we should throw a\n"
	.string "“{STR_VAR_1}” party on the island.\p"
	.string "With burlesque. You know who'll come.$"

DewfordTown_Hall_Text_BrilliantIndeed:
	.string "A smashing idea!\p"
	.string "It'll settle who's the best at\n"
	.string "“{STR_VAR_1}”!\p"
	.string "From today, our lives revolve around\n"
	.string "“{STR_VAR_1}”! Until next week.$"

DewfordTown_Hall_Text_TrendHasBecomePartOfLife:
	.string "I was thinking…\p"
	.string "“{STR_VAR_1}” isn't just a trend anymore.\p"
	.string "It's part of our lives. Like taxes.$"

DewfordTown_Hall_Text_TrendWeighsHeavilyOnMind:
	.string "Beg pardon? That much, what?\p"
	.string "“{STR_VAR_1}” weighs on your mind day and\n"
	.string "night.\p"
	.string "You're the “{STR_VAR_1}” PROFESSOR, old\n"
	.string "sport! Seek help.$"

DewfordTown_Hall_Text_IfWeTeamUpWellBeInvincible:
	.string "If we team up, we'll be invincible at\n"
	.string "“{STR_VAR_1}”!$"

DewfordTown_Hall_Text_WellBeTrendDuo:
	.string "Spot on!\p"
	.string "We'll be the “{STR_VAR_1}” DUO!\p"
	.string "Matching outfits! Hahahah!$"

DewfordTown_Hall_Text_GiveYouSludgeBomb:
	.string "SLUDGE BOMB. It's a bomb. Of sludge.\p"
	.string "It may poison the target. Here's one.$"

DewfordTown_Hall_Text_LoveSludgeBombButTrendInToo:
	.string "I love SLUDGE BOMB.\p"
	.string "But POKéMON with “{STR_VAR_1}” are in too.\p"
	.string "I can't choose. I'm not a strong man.$"

