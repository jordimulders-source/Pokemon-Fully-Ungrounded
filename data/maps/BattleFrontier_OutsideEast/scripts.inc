BattleFrontier_OutsideEast_MapScripts::
	map_script MAP_SCRIPT_ON_RESUME, BattleFrontier_OutsideEast_OnResume
	map_script MAP_SCRIPT_ON_TRANSITION, BattleFrontier_OutsideEast_OnTransition
	.byte 0

BattleFrontier_OutsideEast_OnResume:
	call_if_set FLAG_SYS_CTRL_OBJ_DELETE, BattleFrontier_OutsideEast_EventScript_TryRemoveSudowoodo
	end

BattleFrontier_OutsideEast_EventScript_TryRemoveSudowoodo::
	specialvar VAR_RESULT, GetBattleOutcome
	goto_if_ne VAR_RESULT, B_OUTCOME_CAUGHT, Common_EventScript_NopReturn
	removeobject VAR_LAST_TALKED
	return

BattleFrontier_OutsideEast_OnTransition:
	setvar VAR_BRAVO_TRAINER_BATTLE_TOWER_ON, 0
	setflag FLAG_HIDE_BATTLE_TOWER_REPORTER
	setflag FLAG_TEMP_11 @ Project Grounded: Marshadow verschijnt pas in de Keccles-scene
	call BattleFrontier_OutsideEast_EventScript_SetupRival
	call_if_unset FLAG_DEFEATED_SUDOWOODO, BattleFrontier_OutsideEast_EventScript_ShowSudowoodo
	end

@ Project Grounded: rivaal voor de Battle Tower (gevecht 8), na Pacifidlog (FLAG_RIVAL_PG_PACIFIDLOG_DONE) tot hij
@ met pensioen naar het Paradiso Resort gaat (FLAG_RIVAL_PG_RETIRED). Object-flag FLAG_TEMP_12.
BattleFrontier_OutsideEast_EventScript_SetupRival::
	setflag FLAG_TEMP_12
	goto_if_unset FLAG_RIVAL_PG_PACIFIDLOG_DONE, Common_EventScript_NopReturn
	goto_if_set FLAG_RIVAL_PG_RETIRED, Common_EventScript_NopReturn
	clearflag FLAG_TEMP_12
	setvar VAR_OBJ_GFX_ID_0, OBJ_EVENT_GFX_RIVAL_BRENDAN_NORMAL
	checkplayergender
	goto_if_ne VAR_RESULT, MALE, Common_EventScript_NopReturn
	setvar VAR_OBJ_GFX_ID_0, OBJ_EVENT_GFX_RIVAL_MAY_NORMAL
	return

BattleFrontier_OutsideEast_EventScript_Rival::
	lock
	faceplayer
	checkplayergender
	call_if_eq VAR_RESULT, MALE, BattleFrontier_OutsideEast_EventScript_RivalMusicMay
	call_if_ne VAR_RESULT, MALE, BattleFrontier_OutsideEast_EventScript_RivalMusicBrendan
	msgbox BattleFrontier_OutsideEast_Text_RivalPGIntro, MSGBOX_DEFAULT
	switch VAR_STARTER_MON
	case 0, BattleFrontier_OutsideEast_EventScript_RivalTreecko
	case 1, BattleFrontier_OutsideEast_EventScript_RivalTorchic
	case 2, BattleFrontier_OutsideEast_EventScript_RivalMudkip
	end

BattleFrontier_OutsideEast_EventScript_RivalMusicMay::
	playbgm MUS_ENCOUNTER_MAY, TRUE
	return

BattleFrontier_OutsideEast_EventScript_RivalMusicBrendan::
	playbgm MUS_ENCOUNTER_BRENDAN, TRUE
	return

BattleFrontier_OutsideEast_EventScript_RivalTreecko::
	trainerbattle_no_intro TRAINER_RIVAL_POSTGAME_TREECKO, BattleFrontier_OutsideEast_Text_RivalPGDefeat
	goto BattleFrontier_OutsideEast_EventScript_RivalAfter
	end

BattleFrontier_OutsideEast_EventScript_RivalTorchic::
	trainerbattle_no_intro TRAINER_RIVAL_POSTGAME_TORCHIC, BattleFrontier_OutsideEast_Text_RivalPGDefeat
	goto BattleFrontier_OutsideEast_EventScript_RivalAfter
	end

BattleFrontier_OutsideEast_EventScript_RivalMudkip::
	trainerbattle_no_intro TRAINER_RIVAL_POSTGAME_MUDKIP, BattleFrontier_OutsideEast_Text_RivalPGDefeat
	goto BattleFrontier_OutsideEast_EventScript_RivalAfter
	end

@ verhuizing: zwart, weg, en hij staat voortaan in het Paradiso Resort (ParadisoResort_OnTransition)
BattleFrontier_OutsideEast_EventScript_RivalAfter::
	msgbox BattleFrontier_OutsideEast_Text_RivalPGPostBattle, MSGBOX_DEFAULT
	closemessage
	fadescreen FADE_TO_BLACK
	removeobject LOCALID_FRONTIER_RIVAL
	setflag FLAG_TEMP_12
	setflag FLAG_RIVAL_PG_RETIRED
	savebgm MUS_DUMMY
	fadedefaultbgm
	delay 30
	fadescreen FADE_FROM_BLACK
	msgbox BattleFrontier_OutsideEast_Text_RivalPGMovedAway, MSGBOX_DEFAULT
	release
	end

BattleFrontier_OutsideEast_EventScript_ShowSudowoodo::
	clearflag FLAG_HIDE_BATTLE_FRONTIER_SUDOWOODO
	return

BattleFrontier_OutsideEast_EventScript_BattleTowerSign::
	msgbox BattleFrontier_OutsideEast_Text_BattleTowerSign, MSGBOX_SIGN
	end

BattleFrontier_OutsideEast_EventScript_BattlePalaceSign::
	msgbox BattleFrontier_OutsideEast_Text_BattlePalaceSign, MSGBOX_SIGN
	end

BattleFrontier_OutsideEast_EventScript_BattleArenaSign::
	msgbox BattleFrontier_OutsideEast_Text_BattleArenaSign, MSGBOX_SIGN
	end

BattleFrontier_OutsideEast_EventScript_BattlePyramidSign::
	msgbox BattleFrontier_OutsideEast_Text_BattlePyramidSign, MSGBOX_SIGN
	end

BattleFrontier_OutsideEast_EventScript_NinjaBoy::
	msgbox BattleFrontier_OutsideEast_Text_BattleTowerFeelsSpecial, MSGBOX_NPC
	end

BattleFrontier_OutsideEast_EventScript_Man1::
	msgbox BattleFrontier_OutsideEast_Text_ConquerLeagueAndFrontier, MSGBOX_NPC
	end

BattleFrontier_OutsideEast_EventScript_Hiker::
	msgbox BattleFrontier_OutsideEast_Text_PyramidTooHarsh, MSGBOX_NPC
	end

BattleFrontier_OutsideEast_EventScript_HexManiac::
	msgbox BattleFrontier_OutsideEast_Text_ThriveInDarkness, MSGBOX_NPC
	end

BattleFrontier_OutsideEast_EventScript_BlackBelt1::
	msgbox BattleFrontier_OutsideEast_Text_PutTogetherUltimateTeam, MSGBOX_NPC
	end

BattleFrontier_OutsideEast_EventScript_Cook::
	lock
	msgbox BattleFrontier_OutsideEast_Text_BelieveInYouBuddy, MSGBOX_DEFAULT
	release
	end

BattleFrontier_OutsideEast_EventScript_Zigzagoon::
	lock
	faceplayer
	waitse
	playmoncry SPECIES_ZIGZAGOON, CRY_MODE_NORMAL
	msgbox BattleFrontier_OutsideEast_Text_ZigzagoonLooksVacant, MSGBOX_DEFAULT
	waitmoncry
	release
	end

BattleFrontier_OutsideEast_EventScript_RichBoy::
	msgbox BattleFrontier_OutsideEast_Text_PeopleCallMeBusybody, MSGBOX_NPC
	end

BattleFrontier_OutsideEast_EventScript_ExpertF::
	msgbox BattleFrontier_OutsideEast_Text_OnceBeatGymLeader, MSGBOX_NPC
	end

BattleFrontier_OutsideEast_EventScript_TriathleteF::
	msgbox BattleFrontier_OutsideEast_Text_FastOnBikeAndBattles, MSGBOX_NPC
	end

BattleFrontier_OutsideEast_EventScript_Twin::
	msgbox BattleFrontier_OutsideEast_Text_BetterThanDaddyAtPokemon, MSGBOX_NPC
	end

BattleFrontier_OutsideEast_EventScript_Man2::
	lock
	msgbox BattleFrontier_OutsideEast_Text_GoRackUpSomeWinsForDaddy, MSGBOX_DEFAULT
	release
	end

BattleFrontier_OutsideEast_EventScript_TriathleteM::
	msgbox BattleFrontier_OutsideEast_Text_DidScottBringYouHere, MSGBOX_NPC
	end

BattleFrontier_OutsideEast_EventScript_Sudowoodo::
	lock
	faceplayer
	waitse
	playse SE_SUDOWOODO_SHAKE
	applymovement LOCALID_FRONTIER_SUDOWOODO, BattleFrontier_OutsideEast_Movement_SudowoodoShake
	waitmovement 0
	release
	end

BattleFrontier_OutsideEast_EventScript_WaterSudowoodo::
	lock
	faceplayer
	special DoWateringBerryTreeAnim
	waitstate
	waitse
	playse SE_SUDOWOODO_SHAKE
	applymovement LOCALID_FRONTIER_SUDOWOODO, BattleFrontier_OutsideEast_Movement_SudowoodoShake
	waitmovement 0
	msgbox gText_Sudowoodo_Attacked, MSGBOX_DEFAULT
	closemessage
	waitse
	playmoncry SPECIES_SUDOWOODO, CRY_MODE_ENCOUNTER
	delay 40
	waitmoncry
	setvar VAR_LAST_TALKED, LOCALID_FRONTIER_SUDOWOODO
	setwildbattle SPECIES_SUDOWOODO, 83
	setflag FLAG_SYS_CTRL_OBJ_DELETE
	dowildbattle
	clearflag FLAG_SYS_CTRL_OBJ_DELETE
	specialvar VAR_RESULT, GetBattleOutcome
	goto_if_eq VAR_RESULT, B_OUTCOME_WON, BattleFrontier_OutsideEast_EventScript_DefeatedSudowoodo
	goto_if_eq VAR_RESULT, B_OUTCOME_RAN, BattleFrontier_OutsideEast_EventScript_DefeatedSudowoodo
	goto_if_eq VAR_RESULT, B_OUTCOME_PLAYER_TELEPORTED, BattleFrontier_OutsideEast_EventScript_DefeatedSudowoodo
	setflag FLAG_DEFEATED_SUDOWOODO
	release
	end

BattleFrontier_OutsideEast_EventScript_DefeatedSudowoodo::
	setflag FLAG_DEFEATED_SUDOWOODO
	goto Common_EventScript_RemoveStaticPokemon
	end

BattleFrontier_OutsideEast_Movement_SudowoodoShake:
	face_right
	delay_8
	face_down
	delay_8
	face_left
	delay_8
	face_down
	delay_8
	face_right
	delay_8
	face_down
	delay_8
	face_left
	delay_8
	face_down
	step_end

BattleFrontier_OutsideEast_EventScript_Maniac1::
	msgbox BattleFrontier_OutsideEast_Text_HeardPrettyGirlAtBattleArena, MSGBOX_NPC
	end

BattleFrontier_OutsideEast_EventScript_Girl::
	msgbox BattleFrontier_OutsideEast_Text_SometimesImportantOldManInThere, MSGBOX_NPC
	end

BattleFrontier_OutsideEast_EventScript_PsychicM::
	msgbox BattleFrontier_OutsideEast_Text_LegendOfBattlePyramid, MSGBOX_NPC
	end

BattleFrontier_OutsideEast_EventScript_Man3::
	msgbox BattleFrontier_OutsideEast_Text_GotWipedOut, MSGBOX_NPC
	end

BattleFrontier_OutsideEast_EventScript_Woman1::
	msgbox BattleFrontier_OutsideEast_Text_ToughTrainerInBattleTower, MSGBOX_NPC
	end

BattleFrontier_OutsideEast_EventScript_Woman2::
	msgbox BattleFrontier_OutsideEast_Text_EnoughBattlePointsForDoll, MSGBOX_NPC
	end

BattleFrontier_OutsideEast_EventScript_BlackBelt2::
	msgbox BattleFrontier_OutsideEast_Text_LikeToHaveNameRecordedHere, MSGBOX_NPC
	end

BattleFrontier_OutsideEast_EventScript_Maniac2::
	lock
	msgbox BattleFrontier_OutsideEast_Text_CanDoAnythingWithYou, MSGBOX_DEFAULT
	release
	end

BattleFrontier_OutsideEast_EventScript_Woman3::
	lock
	msgbox BattleFrontier_OutsideEast_Text_PowerOfOurLoveWillOvercome, MSGBOX_DEFAULT
	release
	end

BattleFrontier_OutsideEast_EventScript_RankingHallSign::
	msgbox BattleFrontier_OutsideEast_Text_RankingHallSign, MSGBOX_SIGN
	end

BattleFrontier_OutsideEast_EventScript_ExchangeCornerSign::
	msgbox BattleFrontier_OutsideEast_Text_ExchangeCornerSign, MSGBOX_SIGN
	end

BattleFrontier_OutsideEast_EventScript_Gentleman::
	msgbox BattleFrontier_OutsideEast_Text_FrontierNotExclusivelyForToughTrainers, MSGBOX_NPC
	end

BattleFrontier_OutsideEast_EventScript_OldWoman::
	lock
	faceplayer
	goto_if_set FLAG_DEFEATED_SUDOWOODO, BattleFrontier_OutsideEast_EventScript_OldWomanSudowoodoGone
	msgbox BattleFrontier_OutsideEast_Text_OddTreeHereSeemsToWiggle, MSGBOX_DEFAULT
	release
	end

BattleFrontier_OutsideEast_EventScript_OldWomanSudowoodoGone::
	msgbox BattleFrontier_OutsideEast_Text_OnceAnOddTreePastHere, MSGBOX_DEFAULT
	release
	end

BattleFrontier_OutsideEast_EventScript_Camper::
	msgbox BattleFrontier_OutsideEast_Text_StickyMonWithLongTail, MSGBOX_NPC
	end

BattleFrontier_OutsideEast_Text_BattleTowerSign:
	.string "This is the BATTLE TOWER!\n"
	.string "Keep the win streak as the toughest\l"
	.string "TRAINER!$"

BattleFrontier_OutsideEast_Text_BattlePalaceSign:
	.string "This is the BATTLE PALACE!\n"
	.string "Keep your eyes on POKéMON battles!$"

BattleFrontier_OutsideEast_Text_BattleArenaSign:
	.string "This is the BATTLE ARENA!\n"
	.string "Let the toughest teams gather!$"

BattleFrontier_OutsideEast_Text_BattlePyramidSign:
	.string "This is the BATTLE PYRAMID!\n"
	.string "Advance through the Battle Quest!$"

BattleFrontier_OutsideEast_Text_RankingHallSign:
	.string "BATTLE FRONTIER RANKING HALL\n"
	.string "Set your sights on new records!$"

BattleFrontier_OutsideEast_Text_ExchangeCornerSign:
	.string "BATTLE POINT EXCHANGE SERVICE CORNER\n"
	.string "Exchange your Battle Points!$"

BattleFrontier_OutsideEast_Text_BattleTowerFeelsSpecial:
	.string "Wow!\n"
	.string "It's huge!\p"
	.string "The BATTLE TOWER feels special.\n"
	.string "It's different from the others.$"

BattleFrontier_OutsideEast_Text_ConquerLeagueAndFrontier:
	.string "My grand ambition is to conquer both\n"
	.string "the BATTLE FRONTIER and the POKéMON\l"
	.string "LEAGUE.\p"
	.string "And if my dream comes true…\p"
	.string "I… I'm going to ask MIMI next door\n"
	.string "if she will be friends with me!$"

BattleFrontier_OutsideEast_Text_PyramidTooHarsh:
	.string "The BATTLE PYRAMID's too harsh!\n"
	.string "I just can't make it to the top!\p"
	.string "Since I'm out of options, maybe I can\n"
	.string "climb the outside…$"

BattleFrontier_OutsideEast_Text_ThriveInDarkness:
	.string "I thrive in darkness…\n"
	.string "Yes… What is worthy of me?\l"
	.string "None other than the BATTLE PYRAMID…\p"
	.string "What say you to wandering in darkness\n"
	.string "and in utter and total desperation?$"

BattleFrontier_OutsideEast_Text_PutTogetherUltimateTeam:
	.string "I didn't sleep for a week, but then\n"
	.string "I put together the ultimate team!\p"
	.string "I can't see myself losing, no joke.\n"
	.string "We're storming the BATTLE ARENA!$"

BattleFrontier_OutsideEast_Text_DidScottBringYouHere:
	.string "Did SCOTT bring you here, too?\n"
	.string "What is it with that guy?\p"
	.string "It sounds like he really does know\n"
	.string "how to spot talented TRAINERS, but…\p"
	.string "I've never seen him battling in person\n"
	.string "ever.$"

BattleFrontier_OutsideEast_Text_BelieveInYouBuddy:
	.string "ZIGG!\n"
	.string "I believe in you, little buddy!\p"
	.string "I'll make my little ZIGG any favorite\n"
	.string "tasty treats you like if you win!$"

BattleFrontier_OutsideEast_Text_ZigzagoonLooksVacant:
	.string "ZIGZAGOON looks vacant…$"

BattleFrontier_OutsideEast_Text_PeopleCallMeBusybody:
	.string "People call me a busybody,\n"
	.string "but I can't help it.\p"
	.string "Your hat's on crooked!\n"
	.string "Oh, no, trash on the ground!\l"
	.string "Oops, it's almost dinnertime!\p"
	.string "I don't know if I can stand to just\n"
	.string "watch at the BATTLE PALACE…$"

BattleFrontier_OutsideEast_Text_OnceBeatGymLeader:
	.string "I may not look that impressive now,\n"
	.string "but I once beat a GYM LEADER.\p"
	.string "Who knows, maybe I should give it\n"
	.string "another shot at glory.$"

BattleFrontier_OutsideEast_Text_FastOnBikeAndBattles:
	.string "I'm fast on my BIKE, and that goes for\n"
	.string "the way I battle, too.\p"
	.string "I win matches in the blink of\n"
	.string "an eye!$"

BattleFrontier_OutsideEast_Text_BetterThanDaddyAtPokemon:
	.string "I'm better than my daddy\n"
	.string "at POKéMON.$"

BattleFrontier_OutsideEast_Text_GoRackUpSomeWinsForDaddy:
	.string "Go on, my baby sweetie!\n"
	.string "Go rack up some wins for Daddy!\p"
	.string "You're just like your mother,\n"
	.string "so you'll be dominating!$"

BattleFrontier_OutsideEast_Text_HeardPrettyGirlAtBattleArena:
	.string "It wasn't easy getting here,\n"
	.string "but I'd heard about this knockout\l"
	.string "pretty girl at the BATTLE ARENA.\p"
	.string "Instead of her, do you know what\n"
	.string "I found?\p"
	.string "A whole teeming mob of sweaty,\n"
	.string "stinky, and primitive martial artists!$"

BattleFrontier_OutsideEast_Text_SometimesImportantOldManInThere:
	.string "I sometimes see this really important-\n"
	.string "looking old man going in there.\p"
	.string "He has these really awesome POKéMON.\n"
	.string "He seems really nice, though.$"

BattleFrontier_OutsideEast_Text_LegendOfBattlePyramid:
	.string "Do you know it?\n"
	.string "The legend of the BATTLE PYRAMID?\p"
	.string "When there comes a confident TRAINER\n"
	.string "reaching for the golden pinnacle,\l"
	.string "there shall appear a man among men.\p"
	.string "Don't know that legend?\n"
	.string "Well, of course not!\l"
	.string "I just made it up!\p"
	.string "What's it supposed to mean?\n"
	.string "That, my friend, I can't say!$"

BattleFrontier_OutsideEast_Text_GotWipedOut:
	.string "Man! Oh man!\n"
	.string "I've never lost once before!\p"
	.string "But I got wiped out with no saving\n"
	.string "grace at all!\p"
	.string "And then I'm told I don't have any\n"
	.string "talent?! Man!$"

BattleFrontier_OutsideEast_Text_ToughTrainerInBattleTower:
	.string "This guy ran into a horribly tough\n"
	.string "TRAINER while he was on the BATTLE\l"
	.string "TOWER challenge.\p"
	.string "Now look at him…\p"
	.string "You need to be cautious if you ever\n"
	.string "decide to go to the BATTLE TOWER.$"

BattleFrontier_OutsideEast_Text_EnoughBattlePointsForDoll:
	.string "Yes!\n"
	.string "I've finally got enough Battle Points!\p"
	.string "I guess I'll trade for another giant\n"
	.string "plush DOLL!$"

BattleFrontier_OutsideEast_Text_LikeToHaveNameRecordedHere:
	.string "Oh, yeah, okay!\n"
	.string "So this is the RANKING HALL!\p"
	.string "I'd like to go down in history as\n"
	.string "a super champ and have my name\l"
	.string "recorded here for posterity.$"

BattleFrontier_OutsideEast_Text_CanDoAnythingWithYou:
	.string "With you by my side, I can do anything.$"

BattleFrontier_OutsideEast_Text_PowerOfOurLoveWillOvercome:
	.string "Ooh, darling, you are so wonderful!\p"
	.string "Ooh, I just can't wait anymore!\p"
	.string "Let's go to a MULTI BATTLE ROOM\n"
	.string "right this instant!\p"
	.string "If we get together in the BATTLE SALON,\n"
	.string "the power of our love will overcome\l"
	.string "everyone we meet.\p"
	.string "Why, before us, darling, everything\n"
	.string "will topple like dominoes!$"

BattleFrontier_OutsideEast_Text_FrontierNotExclusivelyForToughTrainers:
	.string "The BATTLE FRONTIER isn't exclusively\n"
	.string "for tough TRAINERS.\p"
	.string "Many people with special abilities\n"
	.string "have been invited, it seems.\p"
	.string "That man SCOTT…\p"
	.string "He may have built this place to serve\n"
	.string "a bigger objective…$"

BattleFrontier_OutsideEast_Text_OddTreeHereSeemsToWiggle:
	.string "Excuse me, young one.\n"
	.string "Have you good eyesight?\p"
	.string "There is an odd tree past here, and to\n"
	.string "my tired eyes it seems to wiggle.$"

BattleFrontier_OutsideEast_Text_OnceAnOddTreePastHere:
	.string "Excuse me, young one.\n"
	.string "Have you a good memory?\p"
	.string "I have this feeling there once was\n"
	.string "an odd tree past here.$"

BattleFrontier_OutsideEast_Text_StickyMonWithLongTail:
	.string "I…\n"
	.string "I saw it!\p"
	.string "There was a sticky sort of a POKéMON\n"
	.string "with a long tail up ahead!\p"
	.string "It was hiding under a boulder, and\n"
	.string "it kept staring at me!$"

@ Project Grounded: Keccles (onzichtbaar, Devon Scope), post-game. Marshadow springt uit de schaduw van de speler,
@ komt in je team en vecht mee. Eenmalig gevecht (FLAG_HIDE_FRONTIER_KECCLES), Marshadow eenmalig (FLAG_RECEIVED_MARSHADOW).
BattleFrontier_OutsideEast_EventScript_Keccles::
	lock
	faceplayer
	checkitem ITEM_DEVON_SCOPE
	goto_if_eq VAR_RESULT, TRUE, BattleFrontier_OutsideEast_EventScript_KecclesAskScope
	msgbox BattleFrontier_OutsideEast_Text_KecclesUnseeable, MSGBOX_DEFAULT
	release
	end

BattleFrontier_OutsideEast_EventScript_KecclesAskScope::
	msgbox BattleFrontier_OutsideEast_Text_KecclesUseScope, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, YES, BattleFrontier_OutsideEast_EventScript_KecclesReveal
	release
	end

BattleFrontier_OutsideEast_EventScript_KecclesReveal::
	msgbox BattleFrontier_OutsideEast_Text_KecclesUsedScope, MSGBOX_DEFAULT
	closemessage
	applymovement LOCALID_FRONTIER_KECCLES, Movement_KecleonAppears
	waitmovement 0
	waitse
	playmoncry SPECIES_KECLEON, CRY_MODE_ENCOUNTER
	delay 40
	waitmoncry
	goto_if_set FLAG_RECEIVED_MARSHADOW, BattleFrontier_OutsideEast_EventScript_KecclesRetry
	msgbox BattleFrontier_OutsideEast_Text_KecclesIntro, MSGBOX_DEFAULT
	call_if_not_defeated TRAINER_KECCLES_1, BattleFrontier_OutsideEast_EventScript_KecclesSkippedBeach
	call_if_not_defeated TRAINER_KECCLES_3, BattleFrontier_OutsideEast_EventScript_KecclesSkippedSnow
	closemessage
	call BattleFrontier_OutsideEast_EventScript_MarshadowAppears
	goto_if_eq VAR_RESULT, FALSE, BattleFrontier_OutsideEast_EventScript_MarshadowNoRoom
	msgbox BattleFrontier_OutsideEast_Text_KecclesTwoAgainstSix, MSGBOX_DEFAULT
	goto BattleFrontier_OutsideEast_EventScript_KecclesBattle

@ Project Grounded: Keccles merkt het op als je een eerdere ontmoeting oversloeg
BattleFrontier_OutsideEast_EventScript_KecclesSkippedBeach::
	msgbox BattleFrontier_OutsideEast_Text_KecclesSkippedBeach, MSGBOX_DEFAULT
	return

BattleFrontier_OutsideEast_EventScript_KecclesSkippedSnow::
	msgbox BattleFrontier_OutsideEast_Text_KecclesSkippedSnow, MSGBOX_DEFAULT
	return

BattleFrontier_OutsideEast_EventScript_KecclesRetry::
	msgbox BattleFrontier_OutsideEast_Text_KecclesRetry, MSGBOX_DEFAULT
BattleFrontier_OutsideEast_EventScript_KecclesBattle::
	trainerbattle_no_intro TRAINER_KECCLES_FRONTIER, BattleFrontier_OutsideEast_Text_KecclesDefeat
	msgbox BattleFrontier_OutsideEast_Text_KecclesPostBattle, MSGBOX_DEFAULT
	closemessage
	applymovement LOCALID_FRONTIER_KECCLES, BattleFrontier_OutsideEast_Movement_KecclesLeave
	waitmovement 0
	removeobject LOCALID_FRONTIER_KECCLES
	setflag FLAG_HIDE_FRONTIER_KECCLES
	release
	end

@ Marshadow komt achter de speler uit zijn schaduw (vak tegenover de kijkrichting), krijgt een uitroepteken van
@ Keccles en gaat via de gift-route je team in (vol: pc). VAR_RESULT = FALSE als er nergens plek is.
BattleFrontier_OutsideEast_EventScript_MarshadowAppears::
	msgbox BattleFrontier_OutsideEast_Text_ShadowMoves, MSGBOX_DEFAULT
	closemessage
	getplayerxy VAR_0x8004, VAR_0x8005
	specialvar VAR_RESULT, GetPlayerFacingDirection
	call_if_eq VAR_RESULT, DIR_NORTH, BattleFrontier_OutsideEast_EventScript_BehindNorth
	call_if_eq VAR_RESULT, DIR_SOUTH, BattleFrontier_OutsideEast_EventScript_BehindSouth
	call_if_eq VAR_RESULT, DIR_WEST, BattleFrontier_OutsideEast_EventScript_BehindWest
	call_if_eq VAR_RESULT, DIR_EAST, BattleFrontier_OutsideEast_EventScript_BehindEast
	setobjectxyperm LOCALID_FRONTIER_MARSHADOW, VAR_0x8004, VAR_0x8005
	playse SE_M_FAINT_ATTACK
	fadescreenspeed FADE_TO_BLACK, 1
	clearflag FLAG_TEMP_11
	addobject LOCALID_FRONTIER_MARSHADOW
	fadescreenspeed FADE_FROM_BLACK, 1
	waitse
	playmoncry SPECIES_MARSHADOW, CRY_MODE_ENCOUNTER
	applymovement LOCALID_FRONTIER_MARSHADOW, BattleFrontier_OutsideEast_Movement_MarshadowJump
	applymovement LOCALID_FRONTIER_KECCLES, Common_Movement_ExclamationMark
	waitmovement 0
	waitmoncry
	msgbox BattleFrontier_OutsideEast_Text_MarshadowAppeared, MSGBOX_DEFAULT
	closemessage
	setvar VAR_0x8004, SPECIES_MARSHADOW
	setvar VAR_0x8005, 85
	setvar VAR_0x8006, ITEM_NONE
	call Grounded_EventScript_GiveGiftMon
	goto_if_eq VAR_RESULT, FALSE, Common_EventScript_NopReturn
	setflag FLAG_RECEIVED_MARSHADOW
	applymovement LOCALID_FRONTIER_MARSHADOW, BattleFrontier_OutsideEast_Movement_Vanish
	waitmovement 0
	removeobject LOCALID_FRONTIER_MARSHADOW
	setflag FLAG_TEMP_11
	setvar VAR_RESULT, TRUE
	return

BattleFrontier_OutsideEast_EventScript_BehindNorth::
	addvar VAR_0x8005, 1
	return

BattleFrontier_OutsideEast_EventScript_BehindSouth::
	subvar VAR_0x8005, 1
	return

BattleFrontier_OutsideEast_EventScript_BehindWest::
	addvar VAR_0x8004, 1
	return

BattleFrontier_OutsideEast_EventScript_BehindEast::
	subvar VAR_0x8004, 1
	return

BattleFrontier_OutsideEast_EventScript_MarshadowNoRoom::
	msgbox BattleFrontier_OutsideEast_Text_MarshadowNoRoom, MSGBOX_DEFAULT
	closemessage
	applymovement LOCALID_FRONTIER_MARSHADOW, BattleFrontier_OutsideEast_Movement_Vanish
	waitmovement 0
	removeobject LOCALID_FRONTIER_MARSHADOW
	setflag FLAG_TEMP_11
	release
	end

BattleFrontier_OutsideEast_Movement_MarshadowJump:
	face_player
	jump_in_place_down
	step_end

BattleFrontier_OutsideEast_Movement_KecclesLeave:
BattleFrontier_OutsideEast_Movement_Vanish:
	set_invisible
	delay_4
	set_visible
	delay_4
	set_invisible
	delay_4
	set_visible
	delay_4
	set_invisible
	step_end

BattleFrontier_OutsideEast_Text_KecclesUnseeable:
	.string "Something invisible is standing here.\p"
	.string "It smells faintly of library.$"

BattleFrontier_OutsideEast_Text_KecclesUseScope:
	.string "Something invisible is standing here.\p"
	.string "Use the DEVON SCOPE?$"

BattleFrontier_OutsideEast_Text_KecclesUsedScope:
	.string "{PLAYER} used the DEVON SCOPE.\p"
	.string "An invisible POKéMON became visible!\n"
	.string "Again.$"

BattleFrontier_OutsideEast_Text_KecclesIntro:
	.string "KECCLES: Oh. Hello, CHAMPION.\p"
	.string "I've been studying the SUDOWOODO here.\n"
	.string "It pretends to be a tree, and everyone\l"
	.string "simply believes it.\p"
	.string "I pretend to be nothing, and everyone\n"
	.string "walks straight into me. Where's the\l"
	.string "justice?\p"
	.string "Anyway. One last battle, rival.\n"
	.string "No camouflage. Just lizards.$"

BattleFrontier_OutsideEast_Text_ShadowMoves:
	.string "…Huh?\p"
	.string "{PLAYER}'s shadow is moving.\n"
	.string "{PLAYER} is not.$"

BattleFrontier_OutsideEast_Text_MarshadowAppeared:
	.string "MARSHADOW leapt out of {PLAYER}'s\n"
	.string "shadow!\p"
	.string "KECCLES: …How long has that been\n"
	.string "in there?\p"
	.string "MARSHADOW is shadowboxing at KECCLES.\p"
	.string "It seems to want to fight alongside\n"
	.string "a strong trainer. It picked you.\l"
	.string "Apparently a while ago.$"

BattleFrontier_OutsideEast_Text_MarshadowNoRoom:
	.string "MARSHADOW looked at your full boxes\n"
	.string "and sank back into your shadow.\p"
	.string "KECCLES: Make some room. I'll wait.\n"
	.string "Invisibly, obviously.$"

BattleFrontier_OutsideEast_Text_KecclesTwoAgainstSix:
	.string "KECCLES: Fine. I'm a scientist.\n"
	.string "I respect a larger sample size.$"

BattleFrontier_OutsideEast_Text_KecclesRetry:
	.string "KECCLES: Back for the rematch? Good.\p"
	.string "Is your shadow coming too?\n"
	.string "I'll assume yes. I always do now.$"

BattleFrontier_OutsideEast_Text_KecclesSkippedBeach:
	.string "KECCLES: Also. You never battled me\n"
	.string "on the beach of ROUTE 115.\p"
	.string "That was our origin story.\n"
	.string "You skipped the origin story. Rude.$"

BattleFrontier_OutsideEast_Text_KecclesSkippedSnow:
	.string "KECCLES: And on ROUTE 136, you walked\n"
	.string "right past me in the snow.\p"
	.string "I was invisible, yes.\n"
	.string "Still rude.$"

BattleFrontier_OutsideEast_Text_KecclesDefeat:
	.string "KECCLES: Hmmm…$"

BattleFrontier_OutsideEast_Text_KecclesPostBattle:
	.string "KECCLES: Wow, I can still learn\n"
	.string "something from that.\p"
	.string "It hid in your shadow through eight\n"
	.string "GYMS and a LEAGUE, and nobody noticed.\l"
	.string "Not even you.\p"
	.string "THAT is camouflage.\p"
	.string "I'm going home to stare at my own\n"
	.string "shadow for a while. Suspiciously.$"

BattleFrontier_OutsideEast_Text_RivalPGIntro:
	.string "{RIVAL}: {PLAYER}. You came.\p"
	.string "I've been standing in front of the\n"
	.string "BATTLE TOWER for three days.\l"
	.string "I haven't gone in. It's very tall.\p"
	.string "Here's the deal. I win, I keep going.\n"
	.string "I lose, I retire. For good.\p"
	.string "I already printed business cards.\n"
	.string "They just say “FORMER”.\l"
	.string "Nothing after it. Just FORMER.\p"
	.string "Make it count.$"

BattleFrontier_OutsideEast_Text_RivalPGDefeat:
	.string "…Huh. So that's what the end\n"
	.string "feels like. Weirdly sunny.$"

BattleFrontier_OutsideEast_Text_RivalPGPostBattle:
	.string "{RIVAL}: That's it. I'm done.\p"
	.string "I'm moving to the PARADISO RESORT.\n"
	.string "All-inclusive. Unlimited buffet.\p"
	.string "Unlimited sadness too, but they\n"
	.string "serve it in a coconut.\p"
	.string "Come visit. Bring nothing.\n"
	.string "Especially not ambition.$"

BattleFrontier_OutsideEast_Text_RivalPGMovedAway:
	.string "{RIVAL} packed one suitcase and\n"
	.string "a lifetime of regret, and left for\l"
	.string "the PARADISO RESORT.$"
