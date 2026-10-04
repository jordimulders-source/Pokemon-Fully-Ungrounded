LilycoveCity_House3_MapScripts::
	map_script MAP_SCRIPT_ON_TRANSITION, LilycoveCity_House3_OnTransition
	.byte 0

LilycoveCity_House3_OnTransition:
	random 4
	copyvar VAR_TEMP_1, VAR_RESULT
	end

LilycoveCity_House3_EventScript_PokefanF::
	lock
	faceplayer
	msgbox LilycoveCity_House3_Text_LearnFromMasterOfPokeblocks, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, LilycoveCity_House3_EventScript_DeclinePokeblockLearn
	msgbox LilycoveCity_House3_Text_ExplainPokeblocks, MSGBOX_DEFAULT
	closemessage
	applymovement VAR_LAST_TALKED, Common_Movement_FaceOriginalDirection
	waitmovement 0
	release
	end

LilycoveCity_House3_EventScript_DeclinePokeblockLearn::
	msgbox LilycoveCity_House3_Text_OhAreYouSure, MSGBOX_DEFAULT
	closemessage
	applymovement VAR_LAST_TALKED, Common_Movement_FaceOriginalDirection
	waitmovement 0
	release
	end

LilycoveCity_House3_EventScript_Man::
	lock
	faceplayer
	msgbox LilycoveCity_House3_Text_HappyToHaveQuadruplets, MSGBOX_DEFAULT
	closemessage
	applymovement VAR_LAST_TALKED, Common_Movement_FaceOriginalDirection
	waitmovement 0
	release
	end

LilycoveCity_House3_EventScript_GameBoyKid1::
	lock
	faceplayer
	switch VAR_TEMP_1
	case 0, LilycoveCity_House3_EventScript_WereDoingMultiBattle
	case 1, LilycoveCity_House3_EventScript_WereMixingRecords
	case 2, LilycoveCity_House3_EventScript_WereBlendingBerries
	case 3, LilycoveCity_House3_EventScript_WereDoingContest
	end

LilycoveCity_House3_EventScript_GameBoyKid2::
	lock
	faceplayer
	switch VAR_TEMP_1
	case 0, LilycoveCity_House3_EventScript_WereDoingMultiBattle
	case 1, LilycoveCity_House3_EventScript_WereMixingRecords
	case 2, LilycoveCity_House3_EventScript_WereBlendingBerries
	case 3, LilycoveCity_House3_EventScript_WereDoingContest
	end

LilycoveCity_House3_EventScript_GameBoyKid3::
	lock
	faceplayer
	switch VAR_TEMP_1
	case 0, LilycoveCity_House3_EventScript_WereDoingMultiBattle
	case 1, LilycoveCity_House3_EventScript_WereMixingRecords
	case 2, LilycoveCity_House3_EventScript_WereBlendingBerries
	case 3, LilycoveCity_House3_EventScript_WereDoingContest
	end

LilycoveCity_House3_EventScript_GameBoyKid4::
	lock
	faceplayer
	switch VAR_TEMP_1
	case 0, LilycoveCity_House3_EventScript_WereDoingMultiBattle
	case 1, LilycoveCity_House3_EventScript_WereMixingRecords
	case 2, LilycoveCity_House3_EventScript_WereBlendingBerries
	case 3, LilycoveCity_House3_EventScript_WereDoingContest
	end

LilycoveCity_House3_EventScript_WereDoingMultiBattle::
	msgbox LilycoveCity_House3_Text_GoingToWinMultiBattles, MSGBOX_DEFAULT
	release
	end

LilycoveCity_House3_EventScript_WereMixingRecords::
	msgbox LilycoveCity_House3_Text_LikeMixingAtRecordCorner, MSGBOX_DEFAULT
	release
	end

LilycoveCity_House3_EventScript_WereBlendingBerries::
	msgbox LilycoveCity_House3_Text_MakePokeblocksWithBerryBlender, MSGBOX_DEFAULT
	release
	end

LilycoveCity_House3_EventScript_WereDoingContest::
	msgbox LilycoveCity_House3_Text_GoingToEnterContest, MSGBOX_DEFAULT
	release
	end

LilycoveCity_House3_Text_LearnFromMasterOfPokeblocks:
	.string "Oh, my! Traveling alone? So young!\p"
	.string "My kids could learn from you. Four of\n"
	.string "them. All at once.\p"
	.string "Me? I'm a master of {POKEBLOCK}S.\p"
	.string "Want to learn from me?$"

LilycoveCity_House3_Text_OhAreYouSure:
	.string "Oh? Are you sure?\p"
	.string "You can't do everything alone, dear!\n"
	.string "Trust me. Quadruplets.$"

LilycoveCity_House3_Text_ExplainPokeblocks:
	.string "Good! This is long, so listen!\p"
	.string "{POKEBLOCK}S are rated on how they feel.\p"
	.string "Lower feel rating = better. Remember\n"
	.string "that!\p"
	.string "A good {POKEBLOCK} has a low feel and a high\n"
	.string "level.\p"
	.string "Use different kinds of BERRIES for\n"
	.string "smooth {POKEBLOCK}S.\p"
	.string "More people blending = smoother\n"
	.string "{POKEBLOCK}S.\p"
	.string "So make friends and blend together.\p"
	.string "That's it! Good luck, dear!\p"
	.string "Now, if you'll excuse me, someone is\n"
	.string "crying. Someone is always crying.$"

LilycoveCity_House3_Text_HappyToHaveQuadruplets:
	.string "My wife had quadruplets.\p"
	.string "I was shocked.\p"
	.string "Now I just want to sleep. For one night.$"

LilycoveCity_House3_Text_GoingToWinMultiBattles:
	.string "We're doing MULTI BATTLES.\p"
	.string "I'm going to win. I always win. I'm the\n"
	.string "oldest by four minutes.$"

LilycoveCity_House3_Text_LikeMixingAtRecordCorner:
	.string "We like mixing stuff at the RECORD\n"
	.string "CORNER.\p"
	.string "What gets mixed? Nobody knows.$"

LilycoveCity_House3_Text_MakePokeblocksWithBerryBlender:
	.string "We're making super {POKEBLOCK}S with the\n"
	.string "BERRY BLENDER!\p"
	.string "Four of us! Perfect!$"

LilycoveCity_House3_Text_GoingToEnterContest:
	.string "I'm entering a CONTEST to brag about my\n"
	.string "POKéMON.\p"
	.string "My brothers are entering too. It'll be a\n"
	.string "war.$"

