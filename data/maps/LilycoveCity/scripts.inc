LilycoveCity_MapScripts::
	map_script MAP_SCRIPT_ON_TRANSITION, LilycoveCity_OnTransition
	map_script MAP_SCRIPT_ON_LOAD, LilycoveCity_OnLoad
	.byte 0

LilycoveCity_OnTransition:
	setflag FLAG_VISITED_LILYCOVE_CITY
	setvar VAR_CONTEST_HALL_STATE, 0
	setflag FLAG_HIDE_LILYCOVE_CONTEST_HALL_REPORTER
	call_if_set FLAG_SYS_WEATHER_CTRL, Common_EventScript_SetAbnormalWeather
	call Common_EventScript_SetupRivalGfxId
	end

LilycoveCity_OnLoad:
	call_if_unset FLAG_TEAM_AQUA_ESCAPED_IN_SUBMARINE, LilycoveCity_EventScript_SetWailmerMetatiles
	end

LilycoveCity_EventScript_SetWailmerMetatiles::
	setmetatile 76, 12, METATILE_Lilycove_Wailmer0, TRUE
	setmetatile 77, 12, METATILE_Lilycove_Wailmer1, TRUE
	setmetatile 76, 13, METATILE_Lilycove_Wailmer2, TRUE
	setmetatile 77, 13, METATILE_Lilycove_Wailmer3, TRUE
	setmetatile 76, 14, METATILE_Lilycove_Wailmer0_Alt, TRUE
	setmetatile 77, 14, METATILE_Lilycove_Wailmer1_Alt, TRUE
	setmetatile 76, 15, METATILE_Lilycove_Wailmer2, TRUE
	setmetatile 77, 15, METATILE_Lilycove_Wailmer3, TRUE
	setmetatile 77, 16, METATILE_Lilycove_Wailmer0_Alt, TRUE
	setmetatile 78, 16, METATILE_Lilycove_Wailmer1_Alt, TRUE
	setmetatile 77, 17, METATILE_Lilycove_Wailmer2, TRUE
	setmetatile 78, 17, METATILE_Lilycove_Wailmer3, TRUE
	return

LilycoveCity_EventScript_BerryGentleman::
	lock
	faceplayer
	dotimebasedevents
	goto_if_set FLAG_DAILY_LILYCOVE_RECEIVED_BERRY, LilycoveCity_EventScript_ReceivedBerry
	msgbox LilycoveCity_Text_BerrySuitsYou, MSGBOX_DEFAULT
	random 10
	addvar VAR_RESULT, FIRST_BERRY_INDEX
	giveitem VAR_RESULT
	goto_if_eq VAR_RESULT, FALSE, Common_EventScript_ShowBagIsFull
	setflag FLAG_DAILY_LILYCOVE_RECEIVED_BERRY
	msgbox LilycoveCity_Text_BecauseYoureTrainer, MSGBOX_DEFAULT
	release
	end

LilycoveCity_EventScript_ReceivedBerry::
	msgbox LilycoveCity_Text_PokeblocksSuitPokemon, MSGBOX_DEFAULT
	release
	end

LilycoveCity_EventScript_Man3::
	msgbox LilycoveCity_Text_ContestHallInTown, MSGBOX_NPC
	end

LilycoveCity_EventScript_Girl::
	lock
	faceplayer
	goto_if_set FLAG_BADGE07_GET, LilycoveCity_EventScript_GirlAquaGone
	msgbox LilycoveCity_Text_StrangeCaveInCove, MSGBOX_DEFAULT
	release
	end

LilycoveCity_EventScript_GirlAquaGone::
	msgbox LilycoveCity_Text_GoingToMoveDeleterForHMs, MSGBOX_DEFAULT
	release
	end

LilycoveCity_EventScript_RichBoy::
	msgbox LilycoveCity_Text_ImFromKanto, MSGBOX_NPC
	end

LilycoveCity_EventScript_Sailor2::
	lock
	faceplayer
	goto_if_set FLAG_TEAM_AQUA_ESCAPED_IN_SUBMARINE, LilycoveCity_EventScript_Sailor2AquaGone
	msgbox LilycoveCity_Text_TeamAquaBeenTrainingWailmer, MSGBOX_DEFAULT
	release
	end

LilycoveCity_EventScript_Sailor2AquaGone::
	msgbox LilycoveCity_Text_SomeonePuntedTeamAquaOut, MSGBOX_DEFAULT
	release
	end

LilycoveCity_EventScript_Woman2::
	lock
	faceplayer
	goto_if_set FLAG_TEAM_AQUA_ESCAPED_IN_SUBMARINE, LilycoveCity_EventScript_Woman2AquaGone
	msgbox LilycoveCity_Text_SomeoneStoleMyPokemon, MSGBOX_DEFAULT
	release
	end

LilycoveCity_EventScript_Woman2AquaGone::
	msgbox LilycoveCity_Text_MissingPokemonCameBack, MSGBOX_DEFAULT
	release
	end

LilycoveCity_EventScript_Man2::
	msgbox LilycoveCity_Text_ImArtDealer, MSGBOX_NPC
	end

LilycoveCity_EventScript_ExpertM1::
	msgbox LilycoveCity_Text_SeaRemainsForeverYoung, MSGBOX_SIGN
	end

LilycoveCity_EventScript_ExpertF::
	msgbox LilycoveCity_Text_SixtyYearsAgoHusbandProposed, MSGBOX_SIGN
	end

LilycoveCity_EventScript_ExpertM2::
	lock
	faceplayer
	goto_if_set FLAG_BADGE07_GET, LilycoveCity_EventScript_ExpertM2AquaGone
	msgbox LilycoveCity_Text_TeamAquaRenovatedCavern, MSGBOX_DEFAULT
	release
	end

LilycoveCity_EventScript_ExpertM2AquaGone::
	msgbox LilycoveCity_Text_TeamAquaLotGoneForGood, MSGBOX_DEFAULT
	release
	end

LilycoveCity_EventScript_Sailor1::
	msgbox LilycoveCity_Text_HeardTowerCalledSkyPillar, MSGBOX_NPC
	end

LilycoveCity_EventScript_FatMan::
	msgbox LilycoveCity_Text_SawTallTowerOnRoute131, MSGBOX_NPC
	end

LilycoveCity_EventScript_Man1::
	lockall
	msgbox LilycoveCity_Text_JustArrivedAndSawRarePokemon, MSGBOX_NPC
	applymovement LOCALID_LILYCOVE_MAN_1, Common_Movement_FaceOriginalDirection
	end

LilycoveCity_EventScript_Woman1::
	lockall
	msgbox LilycoveCity_Text_HoneymoonVowToSeeRarePokemon, MSGBOX_NPC
	applymovement LOCALID_LILYCOVE_WOMAN_1, Common_Movement_FaceOriginalDirection
	end

LilycoveCity_EventScript_CitySign::
	msgbox LilycoveCity_Text_CitySign, MSGBOX_SIGN
	end

LilycoveCity_EventScript_ContestHallSign::
	msgbox LilycoveCity_Text_ContestHallSign, MSGBOX_SIGN
	end

LilycoveCity_EventScript_MotelSign::
	msgbox LilycoveCity_Text_MotelSign, MSGBOX_SIGN
	end

LilycoveCity_EventScript_MuseumSign::
	lockall
	specialvar VAR_0x8004, CountPlayerMuseumPaintings
	switch VAR_0x8004
	case 0, LilycoveCity_EventScript_MuseumSignNoPaintings
	msgbox LilycoveCity_Text_MuseumSignPlayersExhibit, MSGBOX_DEFAULT
	releaseall
	end

LilycoveCity_EventScript_MuseumSignNoPaintings::
	msgbox LilycoveCity_Text_MuseumSign, MSGBOX_DEFAULT
	releaseall
	end

LilycoveCity_EventScript_HarborSign::
	lockall
	goto_if_set FLAG_SYS_GAME_CLEAR, LilycoveCity_EventScript_HarborSignFerryReady
	msgbox LilycoveCity_Text_HarborSignUnderConstruction, MSGBOX_DEFAULT
	releaseall
	end

LilycoveCity_EventScript_HarborSignFerryReady::
	msgbox LilycoveCity_Text_HarborSign, MSGBOX_DEFAULT
	releaseall
	end

LilycoveCity_EventScript_TrainerFanClubSign::
	msgbox LilycoveCity_Text_TrainerFanClubSign, MSGBOX_SIGN
	end

LilycoveCity_EventScript_DepartmentStoreSign::
	msgbox LilycoveCity_Text_DepartmentStoreSign, MSGBOX_SIGN
	end

LilycoveCity_EventScript_MoveDeletersHouseSign::
	msgbox LilycoveCity_Text_MoveDeletersHouseSign, MSGBOX_SIGN
	end

LilycoveCity_EventScript_WailmerTrainerGrunt::
	lockall
	goto_if_set FLAG_MET_WAILMER_TRAINER, LilycoveCity_EventScript_MetWailmerTrainer
	msgbox LilycoveCity_Text_WailmerLeapOutOfWater, MSGBOX_DEFAULT
	applymovement VAR_LAST_TALKED, Common_Movement_FacePlayer
	waitmovement 0
	msgbox LilycoveCity_Text_GetLostMessingUpTraining, MSGBOX_DEFAULT
	applymovement VAR_LAST_TALKED, Common_Movement_FaceOriginalDirection
	waitmovement 0
	setflag FLAG_MET_WAILMER_TRAINER
	releaseall
	end

LilycoveCity_EventScript_MetWailmerTrainer::
	msgbox LilycoveCity_Text_WailmerLeapOutOfWater, MSGBOX_DEFAULT
	releaseall
	end

LilycoveCity_EventScript_AquaGrunt1::
	msgbox LilycoveCity_Text_MovedLootIntoHideoutToday, MSGBOX_NPC
	end

LilycoveCity_EventScript_AquaGrunt2::
	msgbox LilycoveCity_Text_ChanceToDoBigThings, MSGBOX_NPC
	end

LilycoveCity_EventScript_AquaGrunt3::
	msgbox LilycoveCity_Text_DontGoNearCaveInCove, MSGBOX_NPC
	end

LilycoveCity_EventScript_AquaGrunt4::
	msgbox LilycoveCity_Text_IfWorldBecomesOurs, MSGBOX_NPC
	end

LilycoveCity_EventScript_Rival::
	lock
	faceplayer
	checkplayergender
	goto_if_eq VAR_RESULT, MALE, LilycoveCity_EventScript_May
	goto_if_eq VAR_RESULT, FEMALE, LilycoveCity_EventScript_Brendan
	end

LilycoveCity_EventScript_May::
	playbgm MUS_ENCOUNTER_MAY, TRUE
	call_if_set FLAG_DECLINED_RIVAL_BATTLE_LILYCOVE, LilycoveCity_EventScript_MayAskToBattleAgain
	call_if_unset FLAG_DECLINED_RIVAL_BATTLE_LILYCOVE, LilycoveCity_EventScript_MayAskToBattle
	goto_if_eq VAR_RESULT, NO, LilycoveCity_EventScript_DeclineMayBattle
	msgbox LilycoveCity_Text_MayWontBeBeaten, MSGBOX_DEFAULT
	switch VAR_STARTER_MON
	case 0, LilycoveCity_EventScript_BattleMayTreecko
	case 1, LilycoveCity_EventScript_BattleMayTorchic
	case 2, LilycoveCity_EventScript_BattleMayMudkip
	end

LilycoveCity_EventScript_MayAskToBattleAgain::
	msgbox LilycoveCity_Text_MayBattleMe, MSGBOX_YESNO
	return

LilycoveCity_EventScript_MayAskToBattle::
	msgbox LilycoveCity_Text_MayShoppingLetsBattle, MSGBOX_YESNO
	return

LilycoveCity_EventScript_DeclineMayBattle::
	setflag FLAG_DECLINED_RIVAL_BATTLE_LILYCOVE
	msgbox LilycoveCity_Text_MayNotRaisingPokemon, MSGBOX_DEFAULT
	savebgm MUS_DUMMY
	fadedefaultbgm
	release
	end

LilycoveCity_EventScript_Brendan::
	playbgm MUS_ENCOUNTER_BRENDAN, TRUE
	call_if_set FLAG_DECLINED_RIVAL_BATTLE_LILYCOVE, LilycoveCity_EventScript_BrendanAskToBattleAgain
	call_if_unset FLAG_DECLINED_RIVAL_BATTLE_LILYCOVE, LilycoveCity_EventScript_BrendanAskToBattle
	goto_if_eq VAR_RESULT, NO, LilycoveCity_EventScript_DeclineBrendanBattle
	msgbox LilycoveCity_Text_BrendanWontBeBeaten, MSGBOX_DEFAULT
	switch VAR_STARTER_MON
	case 0, LilycoveCity_EventScript_BattleBrendanTreecko
	case 1, LilycoveCity_EventScript_BattleBrendanTorchic
	case 2, LilycoveCity_EventScript_BattleBrendanMudkip
	end

LilycoveCity_EventScript_BrendanAskToBattleAgain::
	msgbox LilycoveCity_Text_BrendanBattleMe, MSGBOX_YESNO
	return

LilycoveCity_EventScript_BrendanAskToBattle::
	msgbox LilycoveCity_Text_BrendanShoppingLetsBattle, MSGBOX_YESNO
	return

LilycoveCity_EventScript_DeclineBrendanBattle::
	setflag FLAG_DECLINED_RIVAL_BATTLE_LILYCOVE
	msgbox LilycoveCity_Text_BrendanNoConfidence, MSGBOX_DEFAULT
	savebgm MUS_DUMMY
	fadedefaultbgm
	release
	end

LilycoveCity_EventScript_BattleMayTreecko::
	trainerbattle_no_intro TRAINER_MAY_LILYCOVE_TREECKO, LilycoveCity_Text_MayDefeat
	goto LilycoveCity_EventScript_DefeatedMay
	end

LilycoveCity_EventScript_BattleMayTorchic::
	trainerbattle_no_intro TRAINER_MAY_LILYCOVE_TORCHIC, LilycoveCity_Text_MayDefeat
	goto LilycoveCity_EventScript_DefeatedMay
	end

LilycoveCity_EventScript_BattleMayMudkip::
	trainerbattle_no_intro TRAINER_MAY_LILYCOVE_MUDKIP, LilycoveCity_Text_MayDefeat
	goto LilycoveCity_EventScript_DefeatedMay
	end

LilycoveCity_EventScript_BattleBrendanTreecko::
	trainerbattle_no_intro TRAINER_BRENDAN_LILYCOVE_TREECKO, LilycoveCity_Text_BrendanDefeat
	goto LilycoveCity_EventScript_DefeatedBrendan
	end

LilycoveCity_EventScript_BattleBrendanTorchic::
	trainerbattle_no_intro TRAINER_BRENDAN_LILYCOVE_TORCHIC, LilycoveCity_Text_BrendanDefeat
	goto LilycoveCity_EventScript_DefeatedBrendan
	end

LilycoveCity_EventScript_BattleBrendanMudkip::
	trainerbattle_no_intro TRAINER_BRENDAN_LILYCOVE_MUDKIP, LilycoveCity_Text_BrendanDefeat
	goto LilycoveCity_EventScript_DefeatedBrendan
	end

LilycoveCity_EventScript_DefeatedMay::
	msgbox LilycoveCity_Text_MayGoingBackToLittleroot, MSGBOX_DEFAULT
	setvar VAR_RESULT, FALSE
	call_if_set FLAG_BADGE06_GET, LilycoveCity_EventScript_CheckFinalBadge
	call_if_eq VAR_RESULT, FALSE, LilycoveCity_EventScript_MayCollectBadges
	call_if_eq VAR_RESULT, TRUE, LilycoveCity_EventScript_MayPokemonLeague
	clearflag FLAG_HIDE_LITTLEROOT_TOWN_MAYS_HOUSE_RIVAL_BEDROOM
	clearflag FLAG_HIDE_LITTLEROOT_TOWN_MAYS_HOUSE_2F_PICHU_DOLL
	goto LilycoveCity_EventScript_RivalFlyAway
	end

LilycoveCity_EventScript_CheckFinalBadge::
	goto_if_set FLAG_BADGE08_GET, LilycoveCity_EventScript_HasFinalBadge
	return

LilycoveCity_EventScript_HasFinalBadge::
	setvar VAR_RESULT, TRUE
	return

LilycoveCity_EventScript_MayCollectBadges::
	msgbox LilycoveCity_Text_MayYouGoingToCollectBadges, MSGBOX_DEFAULT
	return

LilycoveCity_EventScript_MayPokemonLeague::
	goto_if_set FLAG_SYS_GAME_CLEAR, LilycoveCity_EventScript_MayBattleFrontier
	msgbox LilycoveCity_Text_MayYouGoingToPokemonLeague, MSGBOX_DEFAULT
	return

LilycoveCity_EventScript_MayBattleFrontier::
	msgbox LilycoveCity_Text_MayYouGoingToBattleFrontier, MSGBOX_DEFAULT
	return

LilycoveCity_EventScript_DefeatedBrendan::
	msgbox LilycoveCity_Text_BrendanGoingBackToLittleroot, MSGBOX_DEFAULT
	setvar VAR_RESULT, FALSE
	call_if_set FLAG_BADGE06_GET, LilycoveCity_EventScript_CheckFinalBadge
	call_if_eq VAR_RESULT, FALSE, LilycoveCity_EventScript_BrendanCollectBadges
	call_if_eq VAR_RESULT, TRUE, LilycoveCity_EventScript_BrendanPokemonLeague
	clearflag FLAG_HIDE_LITTLEROOT_TOWN_BRENDANS_HOUSE_RIVAL_BEDROOM
	clearflag FLAG_HIDE_LITTLEROOT_TOWN_BRENDANS_HOUSE_2F_SWABLU_DOLL
	goto LilycoveCity_EventScript_RivalFlyAway
	end

LilycoveCity_EventScript_BrendanCollectBadges::
	msgbox LilycoveCity_Text_BrendanYouGoingToCollectBadges, MSGBOX_DEFAULT
	return

LilycoveCity_EventScript_BrendanPokemonLeague::
	goto_if_set FLAG_SYS_GAME_CLEAR, LilycoveCity_EventScript_BrendanBattleFrontier
	msgbox LilycoveCity_Text_BrendanYouGoingToPokemonLeague, MSGBOX_DEFAULT
	return

LilycoveCity_EventScript_BrendanBattleFrontier::
	msgbox LilycoveCity_Text_BrendanYouGoingToBattleFrontier, MSGBOX_DEFAULT
	return

LilycoveCity_EventScript_RivalFlyAway::
	call LilycoveCity_EventScript_RivalEonTicket
	closemessage
	applymovement VAR_LAST_TALKED, Common_Movement_WalkInPlaceFasterDown
	waitmovement 0
	delay 50
	setfieldeffectargument 0, 1
	dofieldeffect FLDEFF_NPCFLY_OUT
	delay 15
	removeobject VAR_LAST_TALKED
	waitfieldeffect FLDEFF_NPCFLY_OUT
	savebgm MUS_DUMMY
	fadedefaultbgm
	setflag FLAG_MET_RIVAL_LILYCOVE
	release
	end

LilycoveCity_EventScript_SchoolKidM::
	lock
	faceplayer
	msgbox LilycoveCity_Text_DoYouKnowAboutBerryBlender, MSGBOX_YESNO
	call_if_eq VAR_RESULT, YES, LilycoveCity_EventScript_KnowAboutBerryBlender
	call_if_eq VAR_RESULT, NO, LilycoveCity_EventScript_DontKnowAboutBerryBlender
	release
	end

LilycoveCity_EventScript_KnowAboutBerryBlender::
	msgbox LilycoveCity_Text_FasterSpinBetterPokeblocks, MSGBOX_DEFAULT
	return

LilycoveCity_EventScript_DontKnowAboutBerryBlender::
	msgbox LilycoveCity_Text_ExplainBerryBlender, MSGBOX_DEFAULT
	return

LilycoveCity_Text_MayShoppingLetsBattle:
	.string "MAY: Oh, {PLAYER}{KUN}! Shopping too?\p"
	.string "I bought a ton of DOLLS and POSTERS.\p"
	.string "And I raised my POKéMON properly, of\n"
	.string "course.\p"
	.string "I'm more worried about yours. Show me!$"

LilycoveCity_Text_MayNotRaisingPokemon:
	.string "MAY: Why not? Haven't you been raising\n"
	.string "your POKéMON?\p"
	.string "That's a bad look, {PLAYER}{KUN}.$"

LilycoveCity_Text_MayBattleMe:
	.string "MAY: Come on, battle me so I can check\n"
	.string "out your POKéMON!$"

LilycoveCity_Text_MayWontBeBeaten:
	.string "MAY: My POKéMON won't lose to yours,\n"
	.string "{PLAYER}{KUN}!$"

LilycoveCity_Text_MayDefeat:
	.string "… … … … … …\p"
	.string "I remember our battle on ROUTE 103.\p"
	.string "That's what made you this strong,\n"
	.string "right?\p"
	.string "So technically, I made you. You're\n"
	.string "welcome.$"

LilycoveCity_Text_MayGoingBackToLittleroot:
	.string "MAY: I'm going back to LITTLEROOT soon.\p"
	.string "My POKéDEX is coming along. Dad will be\n"
	.string "proud.\p"
	.string "He's always proud. Of the POKéDEX.$"

LilycoveCity_Text_MayYouGoingToCollectBadges:
	.string "{PLAYER}{KUN}, what's your plan?\p"
	.string "All the BADGES and the LEAGUE?\p"
	.string "While you do that, I'll finish my\n"
	.string "POKéDEX. Before you! See ya!$"

LilycoveCity_Text_MayYouGoingToPokemonLeague:
	.string "{PLAYER}{KUN}, what's your plan?\p"
	.string "The LEAGUE? Or the POKéDEX?\p"
	.string "You beat me at battling, but I'll beat\n"
	.string "you at the POKéDEX! See ya!$"

LilycoveCity_Text_MayYouGoingToBattleFrontier:
	.string "{PLAYER}{KUN}, what's your plan?\p"
	.string "The BATTLE FRONTIER? Or the POKéDEX?\p"
	.string "You beat me at battling, but not at the\n"
	.string "POKéDEX! See ya!$"

LilycoveCity_Text_BrendanShoppingLetsBattle:
	.string "BRENDAN: Oh, it's {PLAYER}.\p"
	.string "I'm running an errand for my dad. I'm NOT\n"
	.string "buying DOLLS.\p"
	.string "…Anyway. Battle? See who raised their\n"
	.string "POKéMON better?$"

LilycoveCity_Text_BrendanNoConfidence:
	.string "BRENDAN: What, scared?$"

LilycoveCity_Text_BrendanBattleMe:
	.string "BRENDAN: Battle? Let's see whose\n"
	.string "POKéMON are better.$"

LilycoveCity_Text_BrendanWontBeBeaten:
	.string "BRENDAN: I'm not losing to {PLAYER}. No\n"
	.string "way.$"

LilycoveCity_Text_BrendanDefeat:
	.string "Humph… You've been raising them.\p"
	.string "That stings. I had a head start.$"

LilycoveCity_Text_BrendanGoingBackToLittleroot:
	.string "BRENDAN: I'm going back to LITTLEROOT.\p"
	.string "The POKéDEX for my dad is coming along.\n"
	.string "I'll show him.\p"
	.string "Maybe he'll look up from his research\n"
	.string "for once.$"

LilycoveCity_Text_BrendanYouGoingToCollectBadges:
	.string "{PLAYER}, what's your plan?\p"
	.string "All the BADGES and the LEAGUE?\p"
	.string "Maybe I'll do that too… Anyway, hang in\n"
	.string "there.$"

LilycoveCity_Text_BrendanYouGoingToPokemonLeague:
	.string "{PLAYER}, what's your plan?\p"
	.string "The LEAGUE, right?\p"
	.string "If I trained a bit more, I'd be stronger\n"
	.string "than you. Probably.\p"
	.string "Anyway, hang in there.$"

LilycoveCity_Text_BrendanYouGoingToBattleFrontier:
	.string "{PLAYER}, what's your plan?\p"
	.string "The BATTLE FRONTIER? The POKéDEX?\p"
	.string "You're strong enough for the FRONTIER.\n"
	.string "Don't tell anyone I said that.$"

LilycoveCity_Text_MovedLootIntoHideoutToday:
	.string "Fufufu… We moved more loot into our\n"
	.string "HIDEOUT today.\p"
	.string "Mostly crates of SAN PELLEGRINO.\p"
	.string "Wh-who are you?! I was talking to\n"
	.string "myself!$"

LilycoveCity_Text_ChanceToDoBigThings:
	.string "I'm just a GRUNT.\p"
	.string "But on TEAM AQUA I get to do big things.\p"
	.string "Like carry water.$"

LilycoveCity_Text_DontGoNearCaveInCove:
	.string "Hey! Don't go near the cave in the cove!\p"
	.string "Why? Because I'm an adult!\p"
	.string "And it's where we keep the bubbles!$"

LilycoveCity_Text_IfWorldBecomesOurs:
	.string "If the world becomes TEAM AQUA's, every\n"
	.string "tap will pour sparkling water.\p"
	.string "Even the toilets.$"

LilycoveCity_Text_WailmerLeapOutOfWater:
	.string "There! WAILMER! Blow bubbles!$"

LilycoveCity_Text_GetLostMessingUpTraining:
	.string "What do you want?\p"
	.string "You're messing up our training. Go drink\n"
	.string "still water somewhere.$"

LilycoveCity_Text_ContestHallInTown:
	.string "There's a CONTEST HALL in this town.\p"
	.string "POKéMON come from all over to get their\n"
	.string "hair done.\p"
	.string "My heart swells! My wallet shrinks!$"

LilycoveCity_Text_StrangeCaveInCove:
	.string "Have you seen that strange cave in the\n"
	.string "cove?\p"
	.string "I heard bubbling. Fizzy bubbling.$"

LilycoveCity_Text_GoingToMoveDeleterForHMs:
	.string "I'm teaching my POKéMON CONTEST moves.\p"
	.string "So I'm deleting their HM moves.\p"
	.string "Nobody needs CUT on a stage.$"

LilycoveCity_Text_ImFromKanto:
	.string "Back in KANTO, they said MEW was under\n"
	.string "the truck by the S.S. ANNE.\p"
	.string "Since then, I've pushed every truck\n"
	.string "I've seen in my life.\p"
	.string "I only found BUG POKéMON and RATTATA.$"

LilycoveCity_Text_TeamAquaBeenTrainingWailmer:
	.string "TEAM AQUA's WAILMER are blocking the\n"
	.string "cove.\p"
	.string "We SAILORS can't get out to sea.\p"
	.string "And they keep offering us sparkling\n"
	.string "water. We drink rum.$"

LilycoveCity_Text_SomeonePuntedTeamAquaOut:
	.string "Ahoy, did you hear?\p"
	.string "Someone kicked TEAM AQUA out!\p"
	.string "The WAILMER are gone. We can sail again.\n"
	.string "And drink rum in peace.$"

LilycoveCity_Text_SomeoneStoleMyPokemon:
	.string "I took a nap at the seaside inn…\p"
	.string "And someone stole my POKéMON!\p"
	.string "The inn gave me a coupon. For the mall.$"

LilycoveCity_Text_MissingPokemonCameBack:
	.string "My missing POKéMON came back!\p"
	.string "It smells like sparkling water.$"

LilycoveCity_Text_ImArtDealer:
	.string "I'm an ART DEALER.\p"
	.string "I buy paintings for too much and sell\n"
	.string "them for more.\p"
	.string "Art.$"

LilycoveCity_Text_SeaRemainsForeverYoung:
	.string "We grow old and wrinkled, but the sea\n"
	.string "stays forever young.\p"
	.string "Fwohoho…\p"
	.string "The sea never had a mall membership.$"

LilycoveCity_Text_SixtyYearsAgoHusbandProposed:
	.string "Sixty years ago, my husband proposed\n"
	.string "to me right here.\p"
	.string "The sea is as beautiful as ever.\p"
	.string "He's in the mall. He's been in the mall\n"
	.string "since 1987.$"

LilycoveCity_Text_TeamAquaRenovatedCavern:
	.string "That cave in the cove was natural.\p"
	.string "Then TEAM AQUA renovated it.\p"
	.string "Now it has a soda fountain.$"

LilycoveCity_Text_TeamAquaLotGoneForGood:
	.string "That cave in the cove…\p"
	.string "It's completely empty now.\p"
	.string "TEAM AQUA left for good. They left the\n"
	.string "empty bottles, though.$"

LilycoveCity_Text_CitySign:
	.string "LILYCOVE CITY\p"
	.string "“Where the land ends and the shopping\n"
	.string "begins.”$"

LilycoveCity_Text_ContestHallSign:
	.string "POKéMON CONTEST HALL\n"
	.string "“The gathering place for TRAINERS who\l"
	.string "don't like fighting.”$"

LilycoveCity_Text_MotelSign:
	.string "COVE LILY MOTEL\p"
	.string "“Remember us as COVE LILY of LILYCOVE.\n"
	.string "Please. Anyone.”$"

LilycoveCity_Text_MuseumSign:
	.string "LILYCOVE MUSEUM\p"
	.string "“POKéMON Masterpiece Collection on\n"
	.string "exhibit! Gift shop open.”$"

LilycoveCity_Text_MuseumSignPlayersExhibit:
	.string "LILYCOVE MUSEUM\p"
	.string "“{PLAYER}'s POKéMON Collection on\n"
	.string "exhibit! Gift shop open.”$"

LilycoveCity_Text_HarborSignUnderConstruction:
	.string "LILYCOVE CITY HARBOR\p"
	.string "“The ferry S.S. TIDAL is under\n"
	.string "construction in SLATEPORT.\p"
	.string "”Service starts soon. Probably.“$"

LilycoveCity_Text_HarborSign:
	.string "LILYCOVE CITY HARBOR\p"
	.string "“Enjoy a delightful cruise on the S.S.\n"
	.string "TIDAL. Buffet included.”$"

LilycoveCity_Text_TrainerFanClubSign:
	.string "POKéMON TRAINER FAN CLUB\p"
	.string "The names of TRAINERS are scribbled all\n"
	.string "over the sign…\p"
	.string "Yours isn't there yet.$"

LilycoveCity_Text_DepartmentStoreSign:
	.string "LILYCOVE DEPARTMENT STORE\p"
	.string "“You don't need it.\p"
	.string "”You want it.“$"

LilycoveCity_Text_MoveDeletersHouseSign:
	.string "MOVE DELETER'S HOUSE\p"
	.string "“Unwanted moves deleted. Also\n"
	.string "memories, on request.”$"

LilycoveCity_Text_DoYouKnowAboutBerryBlender:
	.string "Do you know about the BERRY BLENDER?\p"
	.string "You put BERRIES in. You spin. You get\n"
	.string "candy for POKéMON.\p"
	.string "It's a smoothie with extra steps.$"

LilycoveCity_Text_FasterSpinBetterPokeblocks:
	.string "Everyone has to work together to spin\n"
	.string "it faster.\p"
	.string "The faster it spins, the better the {POKEBLOCK}S.\p"
	.string "It's teamwork. I hate teamwork.$"

LilycoveCity_Text_ExplainBerryBlender:
	.string "It makes candy called {POKEBLOCK}S.\p"
	.string "Good {POKEBLOCK}S improve a POKéMON's condition a\n"
	.string "lot.\p"
	.string "They're just smoothies. Don't tell\n"
	.string "anyone.$"

LilycoveCity_Text_HeardTowerCalledSkyPillar:
	.string "There's a tower out on the sea routes.\p"
	.string "The SKY PILLAR.\p"
	.string "Sounds like a great place for a mall.$"

LilycoveCity_Text_SawTallTowerOnRoute131:
	.string "I saw a tall tower near ROUTE 131.\p"
	.string "Could that be…?\p"
	.string "…a new department store?!$"

LilycoveCity_Text_JustArrivedAndSawRarePokemon:
	.string "LEGENDS: Z-A? One city. ONE city.\p"
	.string "I spent the whole game on rooftops.\p"
	.string "I wanted KALOS. I got a parking garage.$"

LilycoveCity_Text_HoneymoonVowToSeeRarePokemon:
	.string "Well, I loved LEGENDS: ARCEUS.\p"
	.string "Sneaking through the grass, throwing\n"
	.string "balls from the bushes…\p"
	.string "That's how I caught my husband.$"

@ Project Grounded: de rivaal heeft twee tickets voor Southern Island gekocht; jij kiest er een.
@ Rood = Latias, blauw = Latios (de ander zwerft na de Hall of Fame rond, via VAR_ROAMER_POKEMON).
LilycoveCity_EventScript_RivalEonTicket::
	goto_if_set FLAG_ENABLE_SHIP_SOUTHERN_ISLAND, Common_EventScript_NopReturn
	msgbox LilycoveCity_Text_RivalTwoTickets, MSGBOX_DEFAULT
	message LilycoveCity_Text_RivalPickTicket
	waitmessage
	dynmultichoice 19, 6, TRUE, 2, 0, DYN_MULTICHOICE_CB_NONE, LilycoveCity_Text_RedTicket, LilycoveCity_Text_BlueTicket
	call_if_eq VAR_RESULT, 0, LilycoveCity_EventScript_PickedRedTicket
	call_if_ne VAR_RESULT, 0, LilycoveCity_EventScript_PickedBlueTicket
	giveitem ITEM_EON_TICKET
	setflag FLAG_ENABLE_SHIP_SOUTHERN_ISLAND
	msgbox LilycoveCity_Text_RivalTicketAfter, MSGBOX_DEFAULT
	return

LilycoveCity_EventScript_PickedRedTicket::
	setvar VAR_ROAMER_POKEMON, 1  @ Southern Island: Latias
	return

LilycoveCity_EventScript_PickedBlueTicket::
	setvar VAR_ROAMER_POKEMON, 0  @ Southern Island: Latios
	return

LilycoveCity_Text_RedTicket:
	.string "RED TICKET$"

LilycoveCity_Text_BlueTicket:
	.string "BLUE TICKET$"

LilycoveCity_Text_RivalTwoTickets:
	.string "Oh, wait. I bought two ferry tickets to\n"
	.string "SOUTHERN ISLAND. Rumor says a really\l"
	.string "rare POKéMON lives there.\p"
	.string "Then I remembered I get seasick on a\n"
	.string "pedal boat. So... you can have one.$"

LilycoveCity_Text_RivalPickTicket:
	.string "Red one or blue one? Pick fast, before I\n"
	.string "get sentimental.$"

LilycoveCity_Text_RivalTicketAfter:
	.string "The ferry leaves from the harbor here\n"
	.string "in LILYCOVE.\p"
	.string "If you meet that POKéMON, say hi from\n"
	.string "me. From a safe distance. On dry land.$"
