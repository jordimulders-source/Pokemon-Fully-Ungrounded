MossdeepCity_SpaceCenter_1F_MapScripts::
	map_script MAP_SCRIPT_ON_LOAD, MossdeepCity_SpaceCenter_1F_OnLoad
	map_script MAP_SCRIPT_ON_TRANSITION, MossdeepCity_SpaceCenter_1F_OnTransition
	.byte 0

MossdeepCity_SpaceCenter_1F_OnTransition:
	goto_if_eq VAR_MOSSDEEP_CITY_STATE, 2, MossdeepCity_SpaceCenter_1F_EventScript_MoveObjectsForTeamMagma
	end

MossdeepCity_SpaceCenter_1F_EventScript_MoveObjectsForTeamMagma::
	setobjectxyperm LOCALID_SPACE_CENTER_1F_SAILOR, 1, 9
	setobjectmovementtype LOCALID_SPACE_CENTER_1F_SAILOR, MOVEMENT_TYPE_FACE_RIGHT
	setobjectxyperm LOCALID_SPACE_CENTER_1F_WOMAN, 0, 8
	setobjectmovementtype LOCALID_SPACE_CENTER_1F_WOMAN, MOVEMENT_TYPE_FACE_RIGHT
	setobjectxyperm LOCALID_SPACE_CENTER_1F_OLD_MAN, 1, 6
	setobjectmovementtype LOCALID_SPACE_CENTER_1F_OLD_MAN, MOVEMENT_TYPE_FACE_RIGHT
	setobjectxyperm LOCALID_SPACE_CENTER_1F_SCIENTIST_1, 3, 4
	setobjectmovementtype LOCALID_SPACE_CENTER_1F_SCIENTIST_1, MOVEMENT_TYPE_FACE_RIGHT
	setobjectmovementtype LOCALID_SPACE_CENTER_1F_SCIENTIST_2, MOVEMENT_TYPE_FACE_RIGHT
	goto_if_eq VAR_MOSSDEEP_SPACE_CENTER_STAIR_GUARD_STATE, 1, MossdeepCity_SpaceCenter_1F_EventScript_MoveStairGuardLeft
	goto_if_eq VAR_MOSSDEEP_SPACE_CENTER_STAIR_GUARD_STATE, 2, MossdeepCity_SpaceCenter_1F_EventScript_MoveStairGuardDown
	goto_if_eq VAR_MOSSDEEP_SPACE_CENTER_STAIR_GUARD_STATE, 3, MossdeepCity_SpaceCenter_1F_EventScript_MoveStairGuardRight
	end

MossdeepCity_SpaceCenter_1F_EventScript_MoveStairGuardLeft::
	setobjectxyperm LOCALID_SPACE_CENTER_1F_STAIR_GRUNT, 12, 2
	end

MossdeepCity_SpaceCenter_1F_EventScript_MoveStairGuardDown::
	setobjectxyperm LOCALID_SPACE_CENTER_1F_STAIR_GRUNT, 13, 3
	end

@ Functionally unused. See comment on MossdeepCity_SpaceCenter_1F_EventScript_MoveGruntFromStairsEast
MossdeepCity_SpaceCenter_1F_EventScript_MoveStairGuardRight::
	setobjectxyperm LOCALID_SPACE_CENTER_1F_STAIR_GRUNT, 14, 2
	end

MossdeepCity_SpaceCenter_1F_OnLoad:
	goto_if_le VAR_MOSSDEEP_CITY_STATE, 2, MossdeepCity_SpaceCenter_1F_EventScript_SetMagmaNote
	end

MossdeepCity_SpaceCenter_1F_EventScript_SetMagmaNote::
	setmetatile 2, 5, METATILE_Facility_DataPad, TRUE
	return

MossdeepCity_SpaceCenter_1F_EventScript_RocketLaunchCounter::
	lock
	faceplayer
	goto_if_eq VAR_MOSSDEEP_CITY_STATE, 2, MossdeepCity_SpaceCenter_1F_EventScript_RocketLaunchCounterMagma
	dotimebasedevents
	specialvar VAR_RESULT, GetWeekCount
	buffernumberstring STR_VAR_1, VAR_RESULT
	call_if_eq VAR_RESULT, 0, MossdeepCity_SpaceCenter_1F_EventScript_NoLaunchesYet
	call_if_ge VAR_RESULT, 1, MossdeepCity_SpaceCenter_1F_EventScript_ShowLaunchNumber
	closemessage
	applymovement VAR_LAST_TALKED, Common_Movement_FaceOriginalDirection
	waitmovement 0
	release
	end

MossdeepCity_SpaceCenter_1F_EventScript_NoLaunchesYet::
	msgbox MossdeepCity_SpaceCenter_1F_Text_RocketLaunchImminent, MSGBOX_DEFAULT
	return

MossdeepCity_SpaceCenter_1F_EventScript_ShowLaunchNumber::
	msgbox MossdeepCity_SpaceCenter_1F_Text_SuccessfulLaunchNumber, MSGBOX_DEFAULT
	return

MossdeepCity_SpaceCenter_1F_EventScript_RocketLaunchCounterMagma::
	dotimebasedevents
	specialvar VAR_RESULT, GetWeekCount
	buffernumberstring STR_VAR_1, VAR_RESULT
	call_if_eq VAR_RESULT, 0, MossdeepCity_SpaceCenter_1F_EventScript_NoLaunchesYetMagma
	call_if_ge VAR_RESULT, 1, MossdeepCity_SpaceCenter_1F_EventScript_ShowLaunchNumberMagma
	closemessage
	applymovement VAR_LAST_TALKED, Common_Movement_WalkInPlaceFasterRight
	waitmovement 0
	release
	end

MossdeepCity_SpaceCenter_1F_EventScript_NoLaunchesYetMagma::
	msgbox MossdeepCity_SpaceCenter_1F_Text_HaywireButRocketLaunchImminent, MSGBOX_DEFAULT
	return

MossdeepCity_SpaceCenter_1F_EventScript_ShowLaunchNumberMagma::
	msgbox MossdeepCity_SpaceCenter_1F_Text_HaywireButSuccessfulLaunchNumber, MSGBOX_DEFAULT
	return

MossdeepCity_SpaceCenter_1F_EventScript_Scientist::
	lock
	faceplayer
	goto_if_eq VAR_MOSSDEEP_CITY_STATE, 2, MossdeepCity_SpaceCenter_1F_EventScript_ScientistMagma
	goto_if_set FLAG_SYS_GAME_CLEAR, MossdeepCity_SpaceCenter_1F_EventScript_DeoxysMeteor
	msgbox MossdeepCity_SpaceCenter_1F_Text_RocketLaunchDemandsPerfection, MSGBOX_DEFAULT
	release
	end

MossdeepCity_SpaceCenter_1F_EventScript_ScientistMagma::
	msgbox MossdeepCity_SpaceCenter_1F_Text_MagmaHaveSightsOnSpaceCenter, MSGBOX_DEFAULT
	applymovement VAR_LAST_TALKED, Common_Movement_WalkInPlaceFasterRight
	waitmovement 0
	release
	end

@ Project Grounded: Deoxys-event. Na de Hall of Fame schiet deze wetenschapper je de ruimte in (MeteorSpace).
@ Niet meer zolang Deoxys gevangen is (FLAG_BATTLED_DEOXYS) of verslagen (FLAG_DEFEATED_DEOXYS, tot de volgende League).
MossdeepCity_SpaceCenter_1F_EventScript_DeoxysMeteor::
	goto_if_set FLAG_BATTLED_DEOXYS, MossdeepCity_SpaceCenter_1F_EventScript_DeoxysCaught
	goto_if_set FLAG_DEFEATED_DEOXYS, MossdeepCity_SpaceCenter_1F_EventScript_DeoxysGone
	goto_if_set FLAG_METEOR_SPACE_RETURNED, MossdeepCity_SpaceCenter_1F_EventScript_LaunchAgain
	msgbox MossdeepCity_SpaceCenter_1F_Text_MeteorIncoming, MSGBOX_YESNO
	goto MossdeepCity_SpaceCenter_1F_EventScript_LaunchAnswer
	end

MossdeepCity_SpaceCenter_1F_EventScript_LaunchAgain::
	msgbox MossdeepCity_SpaceCenter_1F_Text_LaunchAgain, MSGBOX_YESNO
	goto MossdeepCity_SpaceCenter_1F_EventScript_LaunchAnswer
	end

MossdeepCity_SpaceCenter_1F_EventScript_LaunchAnswer::
	goto_if_eq VAR_RESULT, NO, MossdeepCity_SpaceCenter_1F_EventScript_NoLaunch
	msgbox MossdeepCity_SpaceCenter_1F_Text_StrapIn, MSGBOX_DEFAULT
	closemessage
	goto MossdeepCity_SpaceCenter_1F_EventScript_LaunchToSpace
	end

MossdeepCity_SpaceCenter_1F_EventScript_NoLaunch::
	msgbox MossdeepCity_SpaceCenter_1F_Text_NoLaunch, MSGBOX_DEFAULT
	release
	end

@ lancering: aftellen, het gebouw trilt, witte flits, dan zwart en je valt op de meteoriet (valwarp)
MossdeepCity_SpaceCenter_1F_EventScript_LaunchToSpace::
	applymovement VAR_LAST_TALKED, Common_Movement_FaceUp
	waitmovement 0
	msgbox MossdeepCity_SpaceCenter_1F_Text_Countdown, MSGBOX_DEFAULT
	closemessage
	playse SE_M_EXPLOSION
	setvar VAR_0x8004, 2
	setvar VAR_0x8005, 3
	setvar VAR_0x8006, 24
	setvar VAR_0x8007, 3
	special ShakeCamera
	waitstate
	playse SE_M_SKY_UPPERCUT
	fadescreenspeed FADE_TO_WHITE, 2
	setvar VAR_0x8004, 9
	setvar VAR_0x8005, 57
	special DoMeteorSpaceFallWarp
	waitstate
	end

MossdeepCity_SpaceCenter_1F_EventScript_DeoxysCaught::
	msgbox MossdeepCity_SpaceCenter_1F_Text_DeoxysCaught, MSGBOX_DEFAULT
	release
	end

MossdeepCity_SpaceCenter_1F_EventScript_DeoxysGone::
	msgbox MossdeepCity_SpaceCenter_1F_Text_DeoxysGone, MSGBOX_DEFAULT
	release
	end

MossdeepCity_SpaceCenter_1F_EventScript_SunStoneMan::
	lock
	faceplayer
	goto_if_eq VAR_MOSSDEEP_CITY_STATE, 2, MossdeepCity_SpaceCenter_1F_EventScript_SunStoneManMagma
	goto_if_set FLAG_RECEIVED_SUN_STONE_MOSSDEEP, MossdeepCity_SpaceCenter_1F_EventScript_GaveSunStone
	msgbox MossdeepCity_SpaceCenter_1F_Text_FoundThisYouCanHaveIt, MSGBOX_DEFAULT
	giveitem ITEM_SUN_STONE
	goto_if_eq VAR_RESULT, FALSE, Common_EventScript_ShowBagIsFull
	setflag FLAG_RECEIVED_SUN_STONE_MOSSDEEP
	msgbox MossdeepCity_SpaceCenter_1F_Text_HoennFamousForMeteorShowers, MSGBOX_DEFAULT
	release
	end

MossdeepCity_SpaceCenter_1F_EventScript_GaveSunStone::
	msgbox MossdeepCity_SpaceCenter_1F_Text_HoennFamousForMeteorShowers, MSGBOX_DEFAULT
	release
	end

MossdeepCity_SpaceCenter_1F_EventScript_SunStoneManMagma::
	goto_if_set FLAG_RECEIVED_SUN_STONE_MOSSDEEP, MossdeepCity_SpaceCenter_1F_EventScript_GaveSunStoneMagma
	msgbox MossdeepCity_SpaceCenter_1F_Text_MagmaCantStealFuelTakeThis, MSGBOX_DEFAULT
	giveitem ITEM_SUN_STONE
	goto_if_eq VAR_RESULT, FALSE, Common_EventScript_ShowBagIsFull
	setflag FLAG_RECEIVED_SUN_STONE_MOSSDEEP
	msgbox MossdeepCity_SpaceCenter_1F_Text_CantStrollOnBeachWithMagma, MSGBOX_DEFAULT
	applymovement VAR_LAST_TALKED, Common_Movement_WalkInPlaceFasterRight
	waitmovement 0
	release
	end

MossdeepCity_SpaceCenter_1F_EventScript_GaveSunStoneMagma::
	msgbox MossdeepCity_SpaceCenter_1F_Text_CantStrollOnBeachWithMagma, MSGBOX_DEFAULT
	applymovement VAR_LAST_TALKED, Common_Movement_WalkInPlaceFasterRight
	waitmovement 0
	release
	end

MossdeepCity_SpaceCenter_1F_EventScript_Woman::
	lock
	faceplayer
	goto_if_set FLAG_SYS_GAME_CLEAR, MossdeepCity_SpaceCenter_1F_EventScript_WomanNormal
	goto_if_eq VAR_MOSSDEEP_CITY_STATE, 2, MossdeepCity_SpaceCenter_1F_EventScript_WomanMagma
	goto_if_lt VAR_MOSSDEEP_CITY_STATE, 2, MossdeepCity_SpaceCenter_1F_EventScript_WomanNormal
	goto MossdeepCity_SpaceCenter_1F_EventScript_WomanMagma
	end

MossdeepCity_SpaceCenter_1F_EventScript_WomanNormal::
	msgbox MossdeepCity_SpaceCenter_1F_Text_DidPokemonComeFromSpace, MSGBOX_DEFAULT
	release
	end

MossdeepCity_SpaceCenter_1F_EventScript_WomanMagma::
	msgbox MossdeepCity_SpaceCenter_1F_Text_AquaShouldBeatMagma, MSGBOX_DEFAULT
	release
	end

MossdeepCity_SpaceCenter_1F_EventScript_OldMan::
	lock
	faceplayer
	goto_if_set FLAG_SYS_GAME_CLEAR, MossdeepCity_SpaceCenter_1F_EventScript_OldManNormal
	goto_if_eq VAR_MOSSDEEP_CITY_STATE, 2, MossdeepCity_SpaceCenter_1F_EventScript_OldManMagma
	goto_if_lt VAR_MOSSDEEP_CITY_STATE, 2, MossdeepCity_SpaceCenter_1F_EventScript_OldManNormal
	goto MossdeepCity_SpaceCenter_1F_EventScript_OldManMagma
	end

MossdeepCity_SpaceCenter_1F_EventScript_OldManNormal::
	msgbox MossdeepCity_SpaceCenter_1F_Text_RocketsBoggleMyMind, MSGBOX_DEFAULT
	closemessage
	applymovement VAR_LAST_TALKED, Common_Movement_FaceOriginalDirection
	waitmovement 0
	release
	end

MossdeepCity_SpaceCenter_1F_EventScript_OldManMagma::
	msgbox MossdeepCity_SpaceCenter_1F_Text_MagmaWantsToSpoilMyDream, MSGBOX_DEFAULT
	closemessage
	applymovement VAR_LAST_TALKED, Common_Movement_FaceOriginalDirection
	waitmovement 0
	release
	end

MossdeepCity_SpaceCenter_1F_EventScript_Steven::
	lock
	faceplayer
	msgbox MossdeepCity_SpaceCenter_1F_Text_StevenMagmaCantBeAllowedToTakeFuel, MSGBOX_DEFAULT
	applymovement VAR_LAST_TALKED, Common_Movement_FaceOriginalDirection
	waitmovement 0
	release
	end

MossdeepCity_SpaceCenter_1F_EventScript_MagmaNote::
	lockall
	msgbox MossdeepCity_SpaceCenter_1F_Text_MagmaIntentToStealNotice, MSGBOX_DEFAULT
	releaseall
	end

MossdeepCity_SpaceCenter_1F_EventScript_Grunt3::
	trainerbattle_single TRAINER_GRUNT_SPACE_CENTER_3, MossdeepCity_SpaceCenter_1F_Text_Grunt3Intro, MossdeepCity_SpaceCenter_1F_Text_Grunt3Defeat
	msgbox MossdeepCity_SpaceCenter_1F_Text_Grunt3PostBattle, MSGBOX_AUTOCLOSE
	end

MossdeepCity_SpaceCenter_1F_EventScript_Grunt1::
	trainerbattle_single TRAINER_GRUNT_SPACE_CENTER_1, MossdeepCity_SpaceCenter_1F_Text_Grunt1Intro, MossdeepCity_SpaceCenter_1F_Text_Grunt1Defeat
	msgbox MossdeepCity_SpaceCenter_1F_Text_Grunt1PostBattle, MSGBOX_AUTOCLOSE
	end

MossdeepCity_SpaceCenter_1F_EventScript_Grunt4::
	trainerbattle_single TRAINER_GRUNT_SPACE_CENTER_4, MossdeepCity_SpaceCenter_1F_Text_Grunt4Intro, MossdeepCity_SpaceCenter_1F_Text_Grunt4Defeat
	msgbox MossdeepCity_SpaceCenter_1F_Text_Grunt4PostBattle, MSGBOX_AUTOCLOSE
	end

MossdeepCity_SpaceCenter_1F_EventScript_Grunt2::
	lock
	faceplayer
	goto_if_set FLAG_DEFEATED_GRUNT_SPACE_CENTER_1F, MossdeepCity_SpaceCenter_1F_EventScript_Grunt2Defeated
	msgbox MossdeepCity_SpaceCenter_1F_Text_Grunt2Intro, MSGBOX_DEFAULT
	trainerbattle_no_intro TRAINER_GRUNT_SPACE_CENTER_2, MossdeepCity_SpaceCenter_1F_Text_Grunt2Defeat
	setflag FLAG_DEFEATED_GRUNT_SPACE_CENTER_1F
	copyobjectxytoperm LOCALID_SPACE_CENTER_1F_STAIR_GRUNT
	switch VAR_FACING
	case DIR_WEST, MossdeepCity_SpaceCenter_1F_EventScript_MoveGruntFromStairsWest
#ifdef BUGFIX
	case DIR_EAST, MossdeepCity_SpaceCenter_1F_EventScript_MoveGruntFromStairsEast
#else
	case DIR_WEST, MossdeepCity_SpaceCenter_1F_EventScript_MoveGruntFromStairsEast
#endif
	applymovement LOCALID_SPACE_CENTER_1F_STAIR_GRUNT, MossdeepCity_SpaceCenter_1F_Movement_MoveGruntFromStairs
	waitmovement 0
	setvar VAR_MOSSDEEP_SPACE_CENTER_STAIR_GUARD_STATE, 2
	release
	end

MossdeepCity_SpaceCenter_1F_EventScript_Grunt2Defeated::
	msgbox MossdeepCity_SpaceCenter_1F_Text_Grunt2PostBattle, MSGBOX_DEFAULT
	release
	end

MossdeepCity_SpaceCenter_1F_EventScript_MoveGruntFromStairsWest::
	applymovement LOCALID_SPACE_CENTER_1F_STAIR_GRUNT, MossdeepCity_SpaceCenter_1F_Movement_MoveGruntFromStairsWest
	waitmovement 0
	setvar VAR_MOSSDEEP_SPACE_CENTER_STAIR_GUARD_STATE, 1
	release
	end

@ Functionally unused by mistake. The movement is handled anyway after the switch (see above)
@ This also means VAR_MOSSDEEP_SPACE_CENTER_STAIR_GUARD_STATE can never be 3
MossdeepCity_SpaceCenter_1F_EventScript_MoveGruntFromStairsEast::
	applymovement LOCALID_SPACE_CENTER_1F_STAIR_GRUNT, MossdeepCity_SpaceCenter_1F_Movement_MoveGruntFromStairsEast
	waitmovement 0
	setvar VAR_MOSSDEEP_SPACE_CENTER_STAIR_GUARD_STATE, 3
	release
	end

MossdeepCity_SpaceCenter_1F_Movement_MoveGruntFromStairsWest:
	lock_facing_direction
	walk_left
	unlock_facing_direction
	step_end

@ Functionally unused. See above
MossdeepCity_SpaceCenter_1F_Movement_MoveGruntFromStairsEast:
	lock_facing_direction
	walk_right
	unlock_facing_direction
	step_end

@ This was meant to only handle the player facing North, but by mistake(?) it also handles the player facing East
MossdeepCity_SpaceCenter_1F_Movement_MoveGruntFromStairs:
	face_left
	lock_facing_direction
	walk_right
	unlock_facing_direction
	step_end

MossdeepCity_SpaceCenter_1F_Text_RocketLaunchImminent:
	.string "The rocket launch is imminent!\p"
	.string "No, you can't come.$"

MossdeepCity_SpaceCenter_1F_Text_SuccessfulLaunchNumber:
	.string "The rocket launched safely!\p"
	.string "Successful launch no. {STR_VAR_1}!\p"
	.string "We don't count the other ones.$"

MossdeepCity_SpaceCenter_1F_Text_HaywireButRocketLaunchImminent:
	.string "Things are a bit haywire right now, but…\p"
	.string "The launch is imminent!\p"
	.string "The show must go on. Into space.$"

MossdeepCity_SpaceCenter_1F_Text_HaywireButSuccessfulLaunchNumber:
	.string "Things are a bit haywire, but…\p"
	.string "The rocket launched safely! Launch no.\n"
	.string "{STR_VAR_1}!$"

MossdeepCity_SpaceCenter_1F_Text_RocketLaunchDemandsPerfection:
	.string "Soon AI will fly the rockets. No humans\n"
	.string "needed at all.\p"
	.string "…Open the pod bay doors, HAL. I'm sure\n"
	.string "that'll be fine.$"

MossdeepCity_SpaceCenter_1F_Text_MagmaHaveSightsOnSpaceCenter:
	.string "TEAM MAGMA wants our SPACE CENTER.\p"
	.string "But nothing stops our launch!\p"
	.string "Not even hot sauce.$"

MossdeepCity_SpaceCenter_1F_Text_FoundThisYouCanHaveIt:
	.string "I found this on the beach.\p"
	.string "It's a rock. From space? Maybe.\p"
	.string "You can have it. I have 400.$"

MossdeepCity_SpaceCenter_1F_Text_HoennFamousForMeteorShowers:
	.string "Meteor showers are nice. But have you\n"
	.string "ever met the machine elves?\p"
	.string "One cup of ayahuasca and you don't\n"
	.string "need a rocket.$"

MossdeepCity_SpaceCenter_1F_Text_MagmaCantStealFuelTakeThis:
	.string "TEAM MAGMA can't steal the rocket fuel.\p"
	.string "Oh, here, have this stone I found on the\n"
	.string "beach.\p"
	.string "Maybe it's from space. Maybe from a\n"
	.string "beach.$"

MossdeepCity_SpaceCenter_1F_Text_CantStrollOnBeachWithMagma:
	.string "With TEAM MAGMA around, beach walks\n"
	.string "aren't safe.\p"
	.string "They keep offering me samples.$"

MossdeepCity_SpaceCenter_1F_Text_DidPokemonComeFromSpace:
	.string "Some say POKéMON came from space.\p"
	.string "Could it be true?\p"
	.string "CLEFAIRY did. I'm sure of it. Look at it.$"

MossdeepCity_SpaceCenter_1F_Text_AquaShouldBeatMagma:
	.string "TEAM AQUA should deal with TEAM MAGMA!\p"
	.string "But then AQUA gets cocky.\p"
	.string "Sparkling water AND smug. Unbearable.$"

MossdeepCity_SpaceCenter_1F_Text_RocketsBoggleMyMind:
	.string "A giant chunk of metal flies into\n"
	.string "space…\p"
	.string "It boggles my mind!\p"
	.string "I still don't trust elevators.$"

MossdeepCity_SpaceCenter_1F_Text_MagmaWantsToSpoilMyDream:
	.string "A giant chunk of metal flies into\n"
	.string "space…\p"
	.string "And TEAM MAGMA wants to ruin my dream!\p"
	.string "With SAUCE! Not having it!$"

MossdeepCity_SpaceCenter_1F_Text_StevenMagmaCantBeAllowedToTakeFuel:
	.string "STEVEN: You read that proclamation?\n"
	.string "TEAM MAGMA wants the rocket fuel.\p"
	.string "Not on my watch! This island is METAL!\p"
	.string "I'll keep an eye on things. Go check out\n"
	.string "the town!$"

MossdeepCity_SpaceCenter_1F_Text_Grunt3Intro:
	.string "As promised, we're here for the rocket\n"
	.string "fuel!\p"
	.string "For the spiciest volcano in history!$"

MossdeepCity_SpaceCenter_1F_Text_Grunt3Defeat:
	.string "Ran out of fuel…\p"
	.string "And sauce.$"

MossdeepCity_SpaceCenter_1F_Text_Grunt3PostBattle:
	.string "Don't think you're on a roll!\p"
	.string "The BOSS is upstairs. He's very spicy.$"

MossdeepCity_SpaceCenter_1F_Text_Grunt1Intro:
	.string "ALL YOUR BASE ARE BELONG TO US.$"

MossdeepCity_SpaceCenter_1F_Text_Grunt1Defeat:
	.string "Grrr… We should've brought the ghost\n"
	.string "peppers…$"

MossdeepCity_SpaceCenter_1F_Text_Grunt1PostBattle:
	.string "Fine! Next time, we'll come unannounced.\p"
	.string "And extra spicy.$"

MossdeepCity_SpaceCenter_1F_Text_Grunt4Intro:
	.string "We want all the rocket fuel.\p"
	.string "Every. Last. Drop.\p"
	.string "For the pepper greenhouse.$"

MossdeepCity_SpaceCenter_1F_Text_Grunt4Defeat:
	.string "Please, spare some fuel? Even a tiny\n"
	.string "cup!\p"
	.string "I'll trade you a hot sauce.$"

MossdeepCity_SpaceCenter_1F_Text_Grunt4PostBattle:
	.string "What do we do with rocket fuel?\p"
	.string "No idea! Ask the BOSS upstairs!\p"
	.string "Something with peppers. Always peppers.$"

MossdeepCity_SpaceCenter_1F_Text_Grunt2Intro:
	.string "The BOSS said nobody gets past me!\p"
	.string "Nobody!$"

MossdeepCity_SpaceCenter_1F_Text_Grunt2Defeat:
	.string "Ack! Ack! Aaack! The BOSS is going to\n"
	.string "put hot sauce in my eyes!$"

MossdeepCity_SpaceCenter_1F_Text_Grunt2PostBattle:
	.string "Tell the BOSS I never left my post.\p"
	.string "I stayed until the bitter end.\p"
	.string "Like a good chili.$"

MossdeepCity_SpaceCenter_1F_Text_MagmaIntentToStealNotice:
	.string "This is… An intent-to-steal notice?\p"
	.string "“To the staff of the SPACE CENTER: How\n"
	.string "are you? We are doing fine.\p"
	.string "“We will soon visit you to take your\n"
	.string "rocket fuel.\p"
	.string "“Please don't try to stop us. We will\n"
	.string "take the fuel no matter what.\p"
	.string "“Let there be more land! TEAM MAGMA”\p"
	.string "…I'm going to be an astronaut. I'll eat\n"
	.string "space ice cream every day.$"

@ Project Grounded: Deoxys-event (placeholders; Jordi herschrijft)
MossdeepCity_SpaceCenter_1F_Text_MeteorIncoming:
	.string "Ah. You. The CHAMPION. Perfect timing.\p"
	.string "Our telescope found a meteorite\n"
	.string "heading straight for Hoenn. It hits in…\l"
	.string "soon. “Soon” is a scientific term.\p"
	.string "Something on it is sending signals.\n"
	.string "Shaped like DNA. We don't know what\l"
	.string "that means, but it sounds terrible.\p"
	.string "We need to shoot someone with very\n"
	.string "strong POKéMON into space. You're the\l"
	.string "strongest person we know. Also the only\l"
	.string "one who didn't run.\p"
	.string "So. Can we launch you into space? Your\n"
	.string "POKéMON come too. Legally they have to.$"

MossdeepCity_SpaceCenter_1F_Text_LaunchAgain:
	.string "The meteorite is still up there, still\n"
	.string "sending DNA-shaped signals.\p"
	.string "Another trip into space?$"

MossdeepCity_SpaceCenter_1F_Text_StrapIn:
	.string "Wonderful! Sign here. And here. And\n"
	.string "here, which says “no refunds”.\p"
	.string "The rocket is in the back. Well. The\n"
	.string "rocket was in the back. Budget cuts.\p"
	.string "You'll be going up in a cardboard box\n"
	.string "that says FRAGILE. It's very\l"
	.string "aerodynamic if you don't think about it.$"

MossdeepCity_SpaceCenter_1F_Text_NoLaunch:
	.string "Understood. We'll send the intern.\p"
	.string "He has a SLAKOTH. We're all going to die.$"

MossdeepCity_SpaceCenter_1F_Text_Countdown:
	.string "Launching in three…\n"
	.string "two…\p"
	.string "One is a scary number. We skip that.\p"
	.string "LIFTOFF!$"

MossdeepCity_SpaceCenter_1F_Text_DeoxysCaught:
	.string "The meteorite stopped sending signals.\n"
	.string "So did our coffee machine. Unrelated,\l"
	.string "probably.\p"
	.string "Thanks for saving the planet. We can't\n"
	.string "pay you, but you can keep the box.$"

MossdeepCity_SpaceCenter_1F_Text_DeoxysGone:
	.string "The meteorite has gone quiet. For now.\p"
	.string "Our instruments say the signal comes\n"
	.string "back after your next visit to the\l"
	.string "POKéMON LEAGUE. Don't ask how\l"
	.string "instruments know that.$"
