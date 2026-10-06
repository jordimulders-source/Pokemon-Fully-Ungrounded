@ Project Grounded: Whirl Island (Lugia). Alleen bereikbaar door te duiken (Dive = badge 7): onder Route 124 een
@ zwemgat naar Underwater_WhirlIsland, bovenkomen in de lagune binnen een ring van draaikolken. Het diepe water
@ in de lagune (20,33) is ook de weg terug. De grot (15,27) leidt naar Lugia (WhirlIsland_Cave).
@ Kaart: tools/grounded/maptools/sea_temple_lugia.py
WhirlIsland_MapScripts::
	map_script MAP_SCRIPT_ON_RESUME, WhirlIsland_OnResume
	.byte 0

WhirlIsland_OnResume:
	setdivewarp MAP_UNDERWATER_WHIRL_ISLAND, 9, 6
	end

WhirlIsland_EventScript_Bottle::
	msgbox WhirlIsland_Text_Bottle, MSGBOX_SIGN
	end

WhirlIsland_Text_Bottle:
	.string "There's a message in a bottle stuck\n"
	.string "in the shallows.\p"
	.string "“Day 40. Still circling. The\n"
	.string "whirlpools let you in, but they never\l"
	.string "let you out.\p"
	.string "Day 41. Just remembered I can DIVE.\n"
	.string "Bye.”$"

@ --- zee_vulling_2 (gegenereerd door tools/grounded/maptools/zee_vulling_2.py) ---
WhirlIsland_EventScript_ZV2Keeper::
	lock
	faceplayer
	goto_if_set FLAG_RECEIVED_WHIRL_ISLAND_KINGS_ROCK, WhirlIsland_EventScript_ZV2Keeper_After
	msgbox WhirlIsland_Text_ZV2Keeper, MSGBOX_DEFAULT
	giveitem ITEM_KINGS_ROCK
	goto_if_eq VAR_RESULT, FALSE, Common_EventScript_ShowBagIsFull
	setflag FLAG_RECEIVED_WHIRL_ISLAND_KINGS_ROCK
	release
	end
WhirlIsland_EventScript_ZV2Keeper_After:
	msgbox WhirlIsland_Text_ZV2KeeperAfter, MSGBOX_DEFAULT
	release
	end

WhirlIsland_Text_ZV2Keeper:
	.string "...\p(The old man hasn't spoken in a\nyear. He points at his SLOWPOKE.)\pSLOWPOKE: ...Yawn.\p(Apparently that means 'take this'.\nHe hands you a crown-shaped rock.)$"

WhirlIsland_Text_ZV2KeeperAfter:
	.string "...\p(He points at the sea. Then at the\nsky. Then at his SLOWPOKE. Then he\lgoes back to staring.)$"

WhirlIsland_EventScript_ZV2Slowpoke::
	lock
	faceplayer
	playmoncry SPECIES_SLOWPOKE, CRY_MODE_NORMAL
	msgbox WhirlIsland_Text_ZV2Slowpoke, MSGBOX_DEFAULT
	waitmoncry
	release
	end

WhirlIsland_Text_ZV2Slowpoke:
	.string "SLOWPOKE: ......................\p...Pokaaa?\pIt answered a question you asked\nfour minutes ago.$"

WhirlIsland_EventScript_ZV2Skye::
	trainerbattle_single TRAINER_BIRD_KEEPER_SKYE, WhirlIsland_Text_ZV2Skye_Intro, WhirlIsland_Text_ZV2Skye_Defeat
	msgbox WhirlIsland_Text_ZV2Skye_Post, MSGBOX_AUTOCLOSE
	end

WhirlIsland_Text_ZV2Skye_Intro:
	.string "Something huge sleeps below this\nisland. A bird! A BIG bird!\pI've waited three summers. My\nbirds are bored. Entertain them!$"

WhirlIsland_Text_ZV2Skye_Defeat:
	.string "My birds are entertained.\nI am not.$"

WhirlIsland_Text_ZV2Skye_Post:
	.string "The old man knows something.\nHe won't say. His SLOWPOKE says\l'yawn'. I've decoded nothing.$"
@ --- einde zee_vulling_2 ---
