@ All the LOCALID constants used in this file are essentially redundant.
@ They're all used to have the NPC the player talked to turn back so they're facing
@ their original direction (because they're watching/participating in the contests).
@ They could all be substituted for VAR_LAST_TALKED.
LilycoveCity_ContestHall_MapScripts::
	.byte 0

LilycoveCity_ContestHall_EventScript_Boy1::
	msgbox LilycoveCity_ContestHall_Text_TodayWonSmartnessContest, MSGBOX_NPC
	end

LilycoveCity_ContestHall_EventScript_Boy2::
	msgbox LilycoveCity_ContestHall_Text_EnteredBunchOfContests, MSGBOX_NPC
	end

LilycoveCity_ContestHall_EventScript_Girl::
	msgbox LilycoveCity_ContestHall_Text_ManWhoWonEarlierHadPokeblocks, MSGBOX_NPC
	end

LilycoveCity_ContestHall_EventScript_Sailor::
	msgbox LilycoveCity_ContestHall_Text_IsntThisPlaceHumongous, MSGBOX_NPC
	end

LilycoveCity_ContestHall_EventScript_SmartContestMC::
	lock
	faceplayer
	msgbox LilycoveCity_ContestHall_Text_GiveItBestSmartAppeal, MSGBOX_DEFAULT
	closemessage
	applymovement LOCALID_SMART_MC, Common_Movement_FaceOriginalDirection
	waitmovement 0
	release
	end

LilycoveCity_ContestHall_EventScript_SmartContestJudge::
	lock
	faceplayer
	msgbox LilycoveCity_ContestHall_Text_AreYouEnjoyingThisContest, MSGBOX_DEFAULT
	closemessage
	applymovement LOCALID_SMART_JUDGE, Common_Movement_FaceOriginalDirection
	waitmovement 0
	release
	end

LilycoveCity_ContestHall_EventScript_SmartContestant1::
	lock
	faceplayer
	msgbox LilycoveCity_ContestHall_Text_EnteredWrongContest, MSGBOX_DEFAULT
	closemessage
	applymovement LOCALID_SMART_CONTESTANT_1, Common_Movement_FaceOriginalDirection
	waitmovement 0
	release
	end

LilycoveCity_ContestHall_EventScript_SmartContestant2::
	lock
	faceplayer
	msgbox LilycoveCity_ContestHall_Text_RaisedMonToBeSmart, MSGBOX_DEFAULT
	closemessage
	applymovement LOCALID_SMART_CONTESTANT_2, Common_Movement_FaceOriginalDirection
	waitmovement 0
	release
	end

LilycoveCity_ContestHall_EventScript_SmartContestant3::
	lock
	faceplayer
	msgbox LilycoveCity_ContestHall_Text_IfMonPullsSmartMoveNext, MSGBOX_DEFAULT
	closemessage
	applymovement LOCALID_SMART_CONTESTANT_3, Common_Movement_FaceOriginalDirection
	waitmovement 0
	release
	end

LilycoveCity_ContestHall_EventScript_SmartContestant4::
	lock
	faceplayer
	msgbox LilycoveCity_ContestHall_Text_DontAppreciateCuteLeechLife, MSGBOX_DEFAULT
	closemessage
	applymovement LOCALID_SMART_CONTESTANT_4, Common_Movement_FaceOriginalDirection
	waitmovement 0
	release
	end

LilycoveCity_ContestHall_EventScript_SmartContestAudience1::
	msgbox LilycoveCity_ContestHall_Text_YoureBeautifulGrandpa, MSGBOX_SIGN
	end

LilycoveCity_ContestHall_EventScript_SmartContestAudience2::
	lock
	faceplayer
	msgbox LilycoveCity_ContestHall_Text_AllSeemToUseDifferentMoves, MSGBOX_DEFAULT
	closemessage
	applymovement LOCALID_SMART_AUDIENCE_2, Common_Movement_FaceOriginalDirection
	waitmovement 0
	release
	end

LilycoveCity_ContestHall_EventScript_SmartContestAudience3::
	lock
	faceplayer
	msgbox LilycoveCity_ContestHall_Text_PokemonSmarterThanTrainers, MSGBOX_DEFAULT
	closemessage
	applymovement LOCALID_SMART_AUDIENCE_3, Common_Movement_FaceOriginalDirection
	waitmovement 0
	release
	end

LilycoveCity_ContestHall_EventScript_SmartContestAudience4::
	lock
	faceplayer
	msgbox LilycoveCity_ContestHall_Text_StillLoveSmartnessContests, MSGBOX_DEFAULT
	closemessage
	applymovement LOCALID_SMART_AUDIENCE_4, Common_Movement_FaceOriginalDirection
	waitmovement 0
	release
	end

LilycoveCity_ContestHall_EventScript_BeautyContestMC::
	lock
	faceplayer
	msgbox LilycoveCity_ContestHall_Text_AreYouEnteringBeautyContest, MSGBOX_DEFAULT
	closemessage
	applymovement LOCALID_BEAUTY_MC, Common_Movement_FaceOriginalDirection
	waitmovement 0
	release
	end

LilycoveCity_ContestHall_EventScript_BeautyContestJudge::
	lock
	faceplayer
	msgbox LilycoveCity_ContestHall_Text_EveryPokemonPristineBeauty, MSGBOX_DEFAULT
	closemessage
	applymovement LOCALID_BEAUTY_JUDGE, Common_Movement_FaceOriginalDirection
	waitmovement 0
	release
	end

LilycoveCity_ContestHall_EventScript_BeautyContestant1::
	lock
	faceplayer
	msgbox LilycoveCity_ContestHall_Text_EyesWillBeGluedToMyBeauty, MSGBOX_DEFAULT
	closemessage
	applymovement LOCALID_BEAUTY_CONTESTANT_1, Common_Movement_FaceOriginalDirection
	waitmovement 0
	release
	end

LilycoveCity_ContestHall_EventScript_BeautyContestant2::
	lock
	faceplayer
	msgbox LilycoveCity_ContestHall_Text_OverdidGrooming, MSGBOX_DEFAULT
	closemessage
	applymovement LOCALID_BEAUTY_CONTESTANT_2, Common_Movement_FaceOriginalDirection
	waitmovement 0
	release
	end

LilycoveCity_ContestHall_EventScript_BeautyContestant3::
	lock
	faceplayer
	msgbox LilycoveCity_ContestHall_Text_JudgeWontSeeAuroraBeam, MSGBOX_DEFAULT
	closemessage
	applymovement LOCALID_BEAUTY_CONTESTANT_3, Common_Movement_FaceOriginalDirection
	waitmovement 0
	release
	end

LilycoveCity_ContestHall_EventScript_BeautyContestant4::
	lock
	faceplayer
	msgbox LilycoveCity_ContestHall_Text_PokemonLooksLikeYoungerMe, MSGBOX_DEFAULT
	closemessage
	applymovement LOCALID_BEAUTY_CONTESTANT_4, Common_Movement_FaceOriginalDirection
	waitmovement 0
	release
	end

LilycoveCity_ContestHall_EventScript_BeautyContestAudience1::
	lock
	faceplayer
	msgbox LilycoveCity_ContestHall_Text_WinBeautyContestMakesMeHappy, MSGBOX_DEFAULT
	closemessage
	applymovement LOCALID_BEAUTY_AUDIENCE_1, Common_Movement_FaceOriginalDirection
	waitmovement 0
	release
	end

LilycoveCity_ContestHall_EventScript_BeautyContestAudience2::
	lock
	faceplayer
	msgbox LilycoveCity_ContestHall_Text_GanderAtAllThosePrettyPokemon, MSGBOX_DEFAULT
	closemessage
	applymovement LOCALID_BEAUTY_AUDIENCE_2, Common_Movement_FaceOriginalDirection
	waitmovement 0
	release
	end

LilycoveCity_ContestHall_EventScript_BeautyContestAudience3::
	lock
	faceplayer
	msgbox LilycoveCity_ContestHall_Text_CantWinOnBeautyAlone, MSGBOX_DEFAULT
	closemessage
	applymovement LOCALID_BEAUTY_AUDIENCE_3, Common_Movement_FaceOriginalDirection
	waitmovement 0
	release
	end

LilycoveCity_ContestHall_EventScript_CuteContestMC::
	lock
	faceplayer
	msgbox LilycoveCity_ContestHall_Text_InTheMiddleOfContest, MSGBOX_DEFAULT
	closemessage
	applymovement LOCALID_CUTE_MC, Common_Movement_FaceOriginalDirection
	waitmovement 0
	release
	end

LilycoveCity_ContestHall_EventScript_CuteContestJudge::
	lock
	faceplayer
	msgbox LilycoveCity_ContestHall_Text_SuchCharmingCuteAppeals, MSGBOX_DEFAULT
	closemessage
	applymovement LOCALID_CUTE_JUDGE, Common_Movement_FaceOriginalDirection
	waitmovement 0
	release
	end

LilycoveCity_ContestHall_EventScript_CuteContestant1::
	lock
	faceplayer
	msgbox LilycoveCity_ContestHall_Text_MyAzurillWasDistracted, MSGBOX_DEFAULT
	closemessage
	applymovement LOCALID_CUTE_CONTESTANT_1, Common_Movement_FaceOriginalDirection
	waitmovement 0
	release
	end

LilycoveCity_ContestHall_EventScript_CuteContestant2::
	lock
	faceplayer
	msgbox LilycoveCity_ContestHall_Text_NeverWonBattleButContest, MSGBOX_DEFAULT
	closemessage
	applymovement LOCALID_CUTE_CONTESTANT_2, Common_Movement_FaceOriginalDirection
	waitmovement 0
	release
	end

LilycoveCity_ContestHall_EventScript_CuteContestant3::
	lock
	faceplayer
	msgbox LilycoveCity_ContestHall_Text_PetalDanceIsMarvel, MSGBOX_DEFAULT
	closemessage
	applymovement LOCALID_CUTE_CONTESTANT_3, Common_Movement_FaceOriginalDirection
	waitmovement 0
	release
	end

LilycoveCity_ContestHall_EventScript_CuteContestant4::
	lock
	faceplayer
	msgbox LilycoveCity_ContestHall_Text_MyMonAppealSoMuchCuter, MSGBOX_DEFAULT
	closemessage
	applymovement LOCALID_CUTE_CONTESTANT_4, Common_Movement_FaceOriginalDirection
	waitmovement 0
	release
	end

LilycoveCity_ContestHall_EventScript_CuteContestAudience1::
	lockall
	applymovement LOCALID_CUTE_AUDIENCE_1, Common_Movement_FacePlayer
	waitmovement 0
	msgbox LilycoveCity_ContestHall_Text_MyChildIsInContest, MSGBOX_DEFAULT
	closemessage
	applymovement LOCALID_CUTE_AUDIENCE_1, Common_Movement_FaceOriginalDirection
	waitmovement 0
	delay 25
	msgbox LilycoveCity_ContestHall_Text_ComeOnDear, MSGBOX_DEFAULT
	releaseall
	end

LilycoveCity_ContestHall_EventScript_CuteContestAudience2::
	lock
	faceplayer
	msgbox LilycoveCity_ContestHall_Text_WantCuteMonOfMyOwn, MSGBOX_DEFAULT
	closemessage
	applymovement LOCALID_CUTE_AUDIENCE_2, Common_Movement_FaceOriginalDirection
	waitmovement 0
	release
	end

LilycoveCity_ContestHall_EventScript_CuteContestAudience3::
	lock
	faceplayer
	msgbox LilycoveCity_ContestHall_Text_ThatGirlThereIsCutest, MSGBOX_DEFAULT
	closemessage
	applymovement LOCALID_CUTE_AUDIENCE_3, Common_Movement_FaceOriginalDirection
	waitmovement 0
	release
	end

LilycoveCity_ContestHall_EventScript_BeautyStageSign::
	msgbox LilycoveCity_ContestHall_Text_BeautyContestStage, MSGBOX_SIGN
	end

LilycoveCity_ContestHall_EventScript_CuteStageSign::
	msgbox LilycoveCity_ContestHall_Text_CuteContestStage, MSGBOX_SIGN
	end

LilycoveCity_ContestHall_EventScript_SmartStageSign::
	msgbox LilycoveCity_ContestHall_Text_SmartContestStage, MSGBOX_SIGN
	end

LilycoveCity_ContestHall_Text_TodayWonSmartnessContest:
	.string "This POKéMON won BEAUTY before. Today\n"
	.string "it won SMART.\p"
	.string "Pretty AND smart. Unlike me.$"

LilycoveCity_ContestHall_Text_EnteredBunchOfContests:
	.string "I've entered a bunch of CONTESTS.\p"
	.string "I don't know how they work. Nobody\n"
	.string "does.$"

LilycoveCity_ContestHall_Text_ManWhoWonEarlierHadPokeblocks:
	.string "The winner had a whole bunch of {POKEBLOCK}S.\p"
	.string "Pay to win.$"

LilycoveCity_ContestHall_Text_IsntThisPlaceHumongous:
	.string "Whoa, this place is huge!\p"
	.string "The tension… The hairspray… I can't\n"
	.string "breathe.$"

LilycoveCity_ContestHall_Text_GiveItBestSmartAppeal:
	.string "MC: SMART POKéMON and TRAINERS, are\n"
	.string "you ready?!\p"
	.string "Show us what you've got!\p"
	.string "Please be quick. I'm paid by the hour.$"

LilycoveCity_ContestHall_Text_AreYouEnjoyingThisContest:
	.string "JUDGE: Enjoying the CONTEST?\p"
	.string "Come back with three friends.\p"
	.string "If you have three friends.$"

LilycoveCity_ContestHall_Text_EnteredWrongContest:
	.string "Ayayay… I entered my tough POKéMON in\n"
	.string "the SMARTNESS CONTEST.\p"
	.string "It tried to eat the judge.$"

LilycoveCity_ContestHall_Text_RaisedMonToBeSmart:
	.string "I spent years raising this POKéMON to\n"
	.string "be smart.\p"
	.string "It's smarter than me now. It knows it.$"

LilycoveCity_ContestHall_Text_IfMonPullsSmartMoveNext:
	.string "There it is!\p"
	.string "One more smart move and the crowd will\n"
	.string "go wild!\p"
	.string "(Nobody is watching.)$"

LilycoveCity_ContestHall_Text_DontAppreciateCuteLeechLife:
	.string "Oh, dear!\p"
	.string "My ZUBAT's LEECH LIFE is so cute I used\n"
	.string "it every turn!\p"
	.string "The judges called security.$"

LilycoveCity_ContestHall_Text_YoureBeautifulGrandpa:
	.string "Kiyaaah! You're beautiful, Grandpa!\p"
	.string "Grandpa is a MACHAMP.$"

LilycoveCity_ContestHall_Text_AllSeemToUseDifferentMoves:
	.string "Same POKéMON, different moves.\p"
	.string "Everyone thinks they're special.$"

LilycoveCity_ContestHall_Text_PokemonSmarterThanTrainers:
	.string "I think the POKéMON look smarter\n"
	.string "than their TRAINERS. By a lot.$"

LilycoveCity_ContestHall_Text_StillLoveSmartnessContests:
	.string "I still love SMARTNESS CONTESTS.\p"
	.string "That intellectual green color…\p"
	.string "I don't know what it means, but I love\n"
	.string "it.$"

LilycoveCity_ContestHall_Text_AreYouEnteringBeautyContest:
	.string "MC: Entering the BEAUTY CONTEST?\p"
	.string "Filters are not allowed. Good luck!$"

LilycoveCity_ContestHall_Text_EveryPokemonPristineBeauty:
	.string "JUDGE: Every POKéMON here is pristine\n"
	.string "beauty!\p"
	.string "I forgot to score. Everyone gets a 10.$"

LilycoveCity_ContestHall_Text_EyesWillBeGluedToMyBeauty:
	.string "A POKéMON this beautiful…\p"
	.string "Everyone will stare.\p"
	.string "At it. Then at me. Mostly me.$"

LilycoveCity_ContestHall_Text_OverdidGrooming:
	.string "Waaaah!\p"
	.string "I groomed my POKéMON too much…\p"
	.string "Now it's bald.$"

LilycoveCity_ContestHall_Text_JudgeWontSeeAuroraBeam:
	.string "This AURORA BEAM is so dazzling, the\n"
	.string "JUDGE will be astrally projected out of\l"
	.string "the building.$"

LilycoveCity_ContestHall_Text_PokemonLooksLikeYoungerMe:
	.string "This POKéMON looks just like me when I\n"
	.string "was younger.\p"
	.string "My husband laughed.\p"
	.string "He's sleeping on the couch.$"

LilycoveCity_ContestHall_Text_WinBeautyContestMakesMeHappy:
	.string "If I win BEAUTY, I'm happy.\p"
	.string "If I lose, I'm suing.$"

LilycoveCity_ContestHall_Text_GanderAtAllThosePrettyPokemon:
	.string "Wahahaha!\p"
	.string "Look at all these pretty POKéMON! I\n"
	.string "love the glitz!\p"
	.string "And the free champagne.$"

LilycoveCity_ContestHall_Text_CantWinOnBeautyAlone:
	.string "You can't win on beauty alone.\p"
	.string "You need connections.$"

LilycoveCity_ContestHall_Text_InTheMiddleOfContest:
	.string "MC: Hello! We're in the middle of a\n"
	.string "CONTEST!\p"
	.string "Get out.$"

LilycoveCity_ContestHall_Text_SuchCharmingCuteAppeals:
	.string "JUDGE: Such cute appeals!\p"
	.string "Adorable! I'm crying! I'm always crying!$"

LilycoveCity_ContestHall_Text_MyAzurillWasDistracted:
	.string "My AZURILL got distracted by another\n"
	.string "POKéMON.\p"
	.string "Love is a distraction.$"

LilycoveCity_ContestHall_Text_NeverWonBattleButContest:
	.string "My POKéMON never won a battle.\p"
	.string "But in a CONTEST? A legend.\p"
	.string "A legend of nothing.$"

LilycoveCity_ContestHall_Text_PetalDanceIsMarvel:
	.string "My POKéMON's PETAL DANCE is elegance\n"
	.string "itself.\p"
	.string "Disturb it and I'll call my lawyer.$"

LilycoveCity_ContestHall_Text_MyMonAppealSoMuchCuter:
	.string "Everyone's POKéMON are cute.\p"
	.string "But mine? Cuter.\p"
	.string "I will not be taking questions.$"

LilycoveCity_ContestHall_Text_MyChildIsInContest:
	.string "My child is in this CONTEST.\p"
	.string "I'm living my dreams through her.$"

LilycoveCity_ContestHall_Text_ComeOnDear:
	.string "Come on, dear! Smile! SMILE!\p"
	.string "Mommy didn't pay for this for nothing!$"

LilycoveCity_ContestHall_Text_ThatGirlThereIsCutest:
	.string "That girl is the cutest.\p"
	.string "What? They judge POKéMON?\p"
	.string "…Oh. Then I'll go.$"

LilycoveCity_ContestHall_Text_WantCuteMonOfMyOwn:
	.string "All these cute POKéMON!\p"
	.string "I'm going to catch one!\p"
	.string "And put it in a dress!$"

LilycoveCity_ContestHall_Text_BeautyContestStage:
	.string "BEAUTY CONTEST STAGE\p"
	.string "FILTERS NOT ALLOWED!$"

LilycoveCity_ContestHall_Text_CuteContestStage:
	.string "CUTENESS CONTEST STAGE\p"
	.string "PARENTS, CALM DOWN!$"

LilycoveCity_ContestHall_Text_SmartContestStage:
	.string "SMARTNESS CONTEST STAGE\p"
	.string "POKéMON ONLY. TRAINERS NEED NOT APPLY.$"

