FortreeCity_MapScripts::
	map_script MAP_SCRIPT_ON_TRANSITION, FortreeCity_OnTransition
	map_script MAP_SCRIPT_ON_RESUME, FortreeCity_OnResume
	.byte 0

FortreeCity_OnTransition:
	setvar VAR_0x8004, 1
	call Common_EventScript_SickBlikDevSpawn  @ SickBlik als developer (post-game, dagrotatie)
	setflag FLAG_VISITED_FORTREE_CITY
	end

FortreeCity_OnResume:
	setstepcallback STEP_CB_FORTREE_BRIDGE
	end

FortreeCity_EventScript_Man::
	msgbox FortreeCity_Text_SawGiganticPokemonInSky, MSGBOX_NPC
	end

FortreeCity_EventScript_Woman::
	lock
	faceplayer
	goto_if_set FLAG_KECLEON_FLED_FORTREE, FortreeCity_EventScript_WomanGymAccessible
	msgbox FortreeCity_Text_SomethingBlockingGym, MSGBOX_DEFAULT
	release
	end

FortreeCity_EventScript_WomanGymAccessible::
	msgbox FortreeCity_Text_ThisTimeIllBeatWinona, MSGBOX_DEFAULT
	release
	end

FortreeCity_EventScript_Girl::
	msgbox FortreeCity_Text_TreesGrowByDrinkingRainwater, MSGBOX_NPC
	end

FortreeCity_EventScript_OldMan::
	msgbox FortreeCity_Text_EveryoneHealthyAndLively, MSGBOX_NPC
	end

FortreeCity_EventScript_Boy::
	msgbox FortreeCity_Text_BugPokemonComeThroughWindow, MSGBOX_NPC
	end

FortreeCity_EventScript_GameboyKid::
	msgbox FortreeCity_Text_PokemonThatEvolveWhenTraded, MSGBOX_NPC
	end

FortreeCity_EventScript_CitySign::
	msgbox FortreeCity_Text_CitySign, MSGBOX_SIGN
	end

FortreeCity_EventScript_GymSign::
	msgbox FortreeCity_Text_GymSign, MSGBOX_SIGN
	end

FortreeCity_EventScript_Kecleon::
	lock
	faceplayer
	checkitem ITEM_DEVON_SCOPE
	goto_if_eq VAR_RESULT, TRUE, FortreeCity_EventScript_AskUseDevonScope
	msgbox FortreeCity_Text_SomethingUnseeable, MSGBOX_DEFAULT
	release
	end

FortreeCity_EventScript_AskUseDevonScope::
	msgbox FortreeCity_Text_UnseeableUseDevonScope, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, YES, FortreeCity_EventScript_UseDevonScope
	release
	end

@ Project Grounded: de onzichtbare Kecleon is Keccles (tweede gevecht)
FortreeCity_EventScript_UseDevonScope::
	msgbox FortreeCity_Text_UsedDevonScopeKeccles, MSGBOX_DEFAULT
	closemessage
	applymovement VAR_LAST_TALKED, Movement_KecleonAppears
	waitmovement 0
	waitse
	playmoncry SPECIES_KECLEON, CRY_MODE_ENCOUNTER
	delay 40
	waitmoncry
	call FortreeCity_EventScript_KecclesSpyingText
	trainerbattle_no_intro TRAINER_KECCLES_2, FortreeCity_Text_KecclesDefeat
	applymovement VAR_LAST_TALKED, FortreeCity_Movement_KecleonFlee
	waitmovement 0
	removeobject VAR_LAST_TALKED
	setflag FLAG_KECLEON_FLED_FORTREE
	release
	end

@ Project Grounded: eerste echte kennismaking als de speler Keccles nog nergens had ontmoet (strand van Route 115 of Route 136)
FortreeCity_EventScript_KecclesSpyingText::
	goto_if_defeated TRAINER_KECCLES_1, FortreeCity_EventScript_KecclesSpyingMet
	goto_if_defeated TRAINER_KECCLES_3, FortreeCity_EventScript_KecclesSpyingMet
	msgbox FortreeCity_Text_KecclesSpyingFirstMeet, MSGBOX_DEFAULT
	return

FortreeCity_EventScript_KecclesSpyingMet::
	msgbox FortreeCity_Text_KecclesSpying, MSGBOX_DEFAULT
	return

FortreeCity_Movement_KecleonFlee:
	walk_right
	step_end

FortreeCity_Text_SawGiganticPokemonInSky:
	.string "No one believes me, but I saw a gigantic\n"
	.string "green POKéMON in the sky.\p"
	.string "It flew toward ROUTE 131. Like a huge\n"
	.string "SERPERIOR.\p"
	.string "By the way… Sniff… You smell like\n"
	.string "spices. Did you go to an Indian place?$"

FortreeCity_Text_SomethingBlockingGym:
	.string "I want to go to the GYM, but something\n"
	.string "invisible is in the way.\p"
	.string "I trained on ROUTE 120 for this!\p"
	.string "I'll just stand here. Forever.$"

FortreeCity_Text_ThisTimeIllBeatWinona:
	.string "I brought my pride-and-joy POKéMON.\p"
	.string "This time I'll beat WINONA!\p"
	.string "If she's awake. She's always jetlagged.$"

FortreeCity_Text_TreesGrowByDrinkingRainwater:
	.string "I headbutt every tree I see.\p"
	.string "In JOHTO, POKéMON fall out.\p"
	.string "In HOENN? Nothing.\p"
	.string "Just bark and a headache.\p"
	.string "Tree 417. Here I go.$"

FortreeCity_Text_EveryoneHealthyAndLively:
	.string "We live in trees here.\p"
	.string "Climbing ladders all day keeps you\n"
	.string "young.\p"
	.string "I'm 94. I have calves of steel.$"

FortreeCity_Text_BugPokemonComeThroughWindow:
	.string "Living in trees is okay.\p"
	.string "But BUG POKéMON crawl in through the\n"
	.string "window.\p"
	.string "And into my cereal. Goddamn MOTHIM.$"

FortreeCity_Text_PokemonThatEvolveWhenTraded:
	.string "Some POKéMON only evolve when you\n"
	.string "trade them!\p"
	.string "Nobody has a link cable anymore,\n"
	.string "though.\p"
	.string "So this godlike figure changed the\n"
	.string "rules. Way better!$"

FortreeCity_Text_SomethingUnseeable:
	.string "Something unseeable is in the way.$"

FortreeCity_Text_UnseeableUseDevonScope:
	.string "Something invisible is in the way.\p"
	.string "Use the DEVON SCOPE?$"

FortreeCity_Text_UsedDevonScopeKeccles:
	.string "{PLAYER} used the DEVON SCOPE.\p"
	.string "An invisible POKéMON became visible!$"

FortreeCity_Text_KecclesSpying:
	.string "KECCLES: Wow, was that necessary?\p"
	.string "Oh, I was camouflaged? My apologies.\p"
	.string "I was spying the GYM, not in a creepy\n"
	.string "way, in a tactical way. Planning my\l"
	.string "attack.\p"
	.string "Let me tell you, most POKéMON have no\n"
	.string "clue about tactics.\p"
	.string "They can be smart, but they are too\n"
	.string "obedient.\p"
	.string "Once they get confined to a POKé BALL,\n"
	.string "their free will wanes.\p"
	.string "Sometimes I wonder, what real free will\n"
	.string "is…\p"
	.string "Anyways, let's check if we are both\n"
	.string "ready for WINONA!$"

FortreeCity_Text_KecclesSpyingFirstMeet:
	.string "KECCLES: Wow, was that necessary?\p"
	.string "Oh, I was camouflaged? My apologies.\p"
	.string "I'm KECCLES. A KECLEON with an\n"
	.string "academic career. Yes, I talk.\p"
	.string "We were supposed to meet on the\n"
	.string "beach of ROUTE 115. I had a speech.\p"
	.string "You never showed up. Rude.\p"
	.string "Anyway. I was spying on the GYM. Not\n"
	.string "in a creepy way, in a tactical way.\p"
	.string "Most POKéMON have no clue about\n"
	.string "tactics. They're too obedient.\p"
	.string "Once they get confined to a POKé BALL,\n"
	.string "their free will wanes.\p"
	.string "Sometimes I wonder, what real free will\n"
	.string "is…\p"
	.string "Anyways, let's check if we are both\n"
	.string "ready for WINONA!$"

FortreeCity_Text_KecclesDefeat:
	.string "Hmmm…$"

FortreeCity_Text_UsedDevonScopePokemonFled:
	.string "{PLAYER} used the DEVON SCOPE.\p"
	.string "An invisible POKéMON became visible!\p"
	.string "It was very embarrassed and ran away!$"

FortreeCity_Text_CitySign:
	.string "FORTREE CITY\n"
	.string "“The treetop city that frolics with\l"
	.string "nature. Mind the ladders.”$"

FortreeCity_Text_GymSign:
	.string "FORTREE CITY POKéMON GYM\n"
	.string "LEADER: WINONA\p"
	.string "“The soaring superstar! Currently\n"
	.string "jetlagged. Do not disturb.”$"
