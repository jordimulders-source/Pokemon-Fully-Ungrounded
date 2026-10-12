EverGrandeCity_MapScripts::
	map_script MAP_SCRIPT_ON_TRANSITION, EverGrandeCity_OnTransition
	.byte 0

EverGrandeCity_OnTransition:
	call_if_set FLAG_SYS_WEATHER_CTRL, Common_EventScript_SetAbnormalWeather
	end

EverGrandeCity_EventScript_VictoryRoadSign::
	msgbox EverGrandeCity_Text_EnteringVictoryRoad, MSGBOX_SIGN
	end

EverGrandeCity_EventScript_CitySign::
	msgbox EverGrandeCity_Text_CitySign, MSGBOX_SIGN
	end

EverGrandeCity_EventScript_PokemonLeagueSign::
	msgbox EverGrandeCity_Text_EnteringPokemonLeague, MSGBOX_SIGN
	end

EverGrandeCity_EventScript_SetVisitedEverGrande::
	setflag FLAG_VISITED_EVER_GRANDE_CITY
	setvar VAR_TEMP_1, 1
	end

EverGrandeCity_Text_EnteringVictoryRoad:
	.string "ENTERING VICTORY ROAD\p"
	.string "Last chance to turn back.$"

EverGrandeCity_Text_EnteringPokemonLeague:
	.string "ENTERING POKéMON LEAGUE\p"
	.string "No refunds.$"

EverGrandeCity_Text_CitySign:
	.string "EVER GRANDE CITY\p"
	.string "“The paradise of flowers, the sea, and\n"
	.string "very tired TRAINERS.”$"

@ --- land_vulling (gegenereerd door tools/grounded/maptools/land_vulling.py) ---
EverGrandeCity_EventScript_LVHotDog::
	lock
	faceplayer
	goto_if_set FLAG_DAILY_EVER_GRANDE_HOTDOG, EverGrandeCity_EventScript_LVHotDog_SoldOut
	msgbox EverGrandeCity_Text_LVHotDog, MSGBOX_DEFAULT
	giveitem ITEM_BIG_MALASADA
	goto_if_eq VAR_RESULT, FALSE, Common_EventScript_ShowBagIsFull
	setflag FLAG_DAILY_EVER_GRANDE_HOTDOG
	msgbox EverGrandeCity_Text_LVHotDog_Given, MSGBOX_DEFAULT
	release
	end
EverGrandeCity_EventScript_LVHotDog_SoldOut:
	msgbox EverGrandeCity_Text_LVHotDog_SoldOut, MSGBOX_DEFAULT
	release
	end

EverGrandeCity_Text_LVHotDog:
	.string "VICTORY DOGS! Get your VICTORY DOGS\pFirst one's free. For courage.\nMost challengers only need one.\pWe ran out of sausages in 2003.\nIt's a MALASADA now. Same spirit.$"

EverGrandeCity_Text_LVHotDog_Given:
	.string "Eat it before the ELITE FOUR.\nNobody wants to lose on an empty\lstomach. Full stomach is fine.$"

EverGrandeCity_Text_LVHotDog_SoldOut:
	.string "One VICTORY DOG per person per day.\pLeague rules. The ELITE FOUR\ncomplained about sticky hands.$"

EverGrandeCity_EventScript_LVHotDogCart::
	msgbox EverGrandeCity_Text_LVHotDogCart, MSGBOX_SIGN
	end

EverGrandeCity_Text_LVHotDogCart:
	.string "A cart. The menu says:\n'VICTORY DOG - free'\l'DEFEAT DOG - also free, but sad'$"

EverGrandeCity_EventScript_LVPhotographer::
	lock
	faceplayer
	goto_if_set FLAG_SYS_GAME_CLEAR, EverGrandeCity_EventScript_LVPhotographer_Post
	msgbox EverGrandeCity_Text_LVPhotographer, MSGBOX_DEFAULT
	fadescreen FADE_TO_WHITE
	fadescreen FADE_FROM_WHITE
	msgbox EverGrandeCity_Text_LVPhotographer_Done, MSGBOX_DEFAULT
	release
	end
EverGrandeCity_EventScript_LVPhotographer_Post:
	msgbox EverGrandeCity_Text_LVPhotographer_Post, MSGBOX_DEFAULT
	release
	end

EverGrandeCity_Text_LVPhotographer:
	.string "Hold it! I take a picture of every\nchallenger before they go in.\pThe 'before' picture.\nSay 'ELITE'!$"

EverGrandeCity_Text_LVPhotographer_Done:
	.string "Lovely. I'll take the 'after'\npicture when you come out.\pThose are usually sadder.\nBetter lighting, though.$"

EverGrandeCity_Text_LVPhotographer_Post:
	.string "The new CHAMPION! Your 'before'\npicture is on the wall now.\pNext to 'challenger, crying'\nand 'challenger, crying, wet'.$"

EverGrandeCity_EventScript_LVFanM::
	lock
	faceplayer
	goto_if_set FLAG_SYS_GAME_CLEAR, EverGrandeCity_EventScript_LVFanM_Post
	msgbox EverGrandeCity_Text_LVFanM, MSGBOX_DEFAULT
	release
	end
EverGrandeCity_EventScript_LVFanM_Post:
	msgbox EverGrandeCity_Text_LVFanM_Post, MSGBOX_DEFAULT
	release
	end

EverGrandeCity_Text_LVFanM:
	.string "I come here every day to cheer for\nwhoever walks past.\pGO, STRANGER! YOU CAN DO IT!\n...Probably! Statistically, no!$"

EverGrandeCity_Text_LVFanM_Post:
	.string "IT'S THE CHAMPION! I cheered for\nyou! I cheer for everyone, but\ltoday it worked!$"

EverGrandeCity_EventScript_LVFanGirl::
	lock
	faceplayer
	goto_if_set FLAG_SYS_GAME_CLEAR, EverGrandeCity_EventScript_LVFanGirl_Post
	msgbox EverGrandeCity_Text_LVFanGirl, MSGBOX_DEFAULT
	release
	end
EverGrandeCity_EventScript_LVFanGirl_Post:
	msgbox EverGrandeCity_Text_LVFanGirl_Post, MSGBOX_DEFAULT
	release
	end

EverGrandeCity_Text_LVFanGirl:
	.string "I made a sign for the CHAMPION.\pIt says 'MARRY ME, STEVEN'.\nI'm nine. It's a long-term plan.$"

EverGrandeCity_Text_LVFanGirl_Post:
	.string "Oh, YOU'RE the CHAMPION now?\p...Hold on, I need a new sign.\nDo you spell {PLAYER} with a 'Q'?$"

EverGrandeCity_EventScript_LVBramwell::
	trainerbattle_single TRAINER_EVER_GRANDE_BRAMWELL, EverGrandeCity_Text_LVBramwell_Intro, EverGrandeCity_Text_LVBramwell_Defeat
	msgbox EverGrandeCity_Text_LVBramwell_Post, MSGBOX_AUTOCLOSE
	end

EverGrandeCity_Text_LVBramwell_Intro:
	.string "Forty-seven times I've challenged\nthe ELITE FOUR. Forty-seven!\pThis is my warm-up. You are\nmy warm-up. Nothing personal.$"

EverGrandeCity_Text_LVBramwell_Defeat:
	.string "Forty-eight.\nThat one counts. Somehow it counts.$"

EverGrandeCity_Text_LVBramwell_Post:
	.string "SIDNEY knows my name. Not because\nI'm good. Because I'm always there.$"

EverGrandeCity_EventScript_LVGloria::
	trainerbattle_single TRAINER_EVER_GRANDE_GLORIA, EverGrandeCity_Text_LVGloria_Intro, EverGrandeCity_Text_LVGloria_Defeat
	msgbox EverGrandeCity_Text_LVGloria_Post, MSGBOX_AUTOCLOSE
	end

EverGrandeCity_Text_LVGloria_Intro:
	.string "Wait! Are you famous? You walk like\nsomeone who could be famous.\pBattle me, and if you win, I'll put\nyou in my scrapbook!$"

EverGrandeCity_Text_LVGloria_Defeat:
	.string "Into the scrapbook you go!\nPage 412. Between two strangers.$"

EverGrandeCity_Text_LVGloria_Post:
	.string "My scrapbook is mostly people who\nlost in there. Very thick book.\lVery sad book.$"

EverGrandeCity_EventScript_LVRocky::
	trainerbattle_single TRAINER_EVER_GRANDE_ROCKY, EverGrandeCity_Text_LVRocky_Intro, EverGrandeCity_Text_LVRocky_Defeat
	msgbox EverGrandeCity_Text_LVRocky_Post, MSGBOX_AUTOCLOSE
	end

EverGrandeCity_Text_LVRocky_Intro:
	.string "I'm busking for the League entry\nfee. One song, one battle.\pThe song is about how expensive\nthe League entry fee is.$"

EverGrandeCity_Text_LVRocky_Defeat:
	.string "Sold out! Of everything!\nMostly hope.$"

EverGrandeCity_Text_LVRocky_Post:
	.string "Fun fact: there IS no entry fee.\nI just never asked.$"

EverGrandeCity_EventScript_LVOldWoman::
	lock
	faceplayer
	goto_if_set FLAG_SYS_GAME_CLEAR, EverGrandeCity_EventScript_LVOldWoman_Post
	msgbox EverGrandeCity_Text_LVOldWoman, MSGBOX_DEFAULT
	release
	end
EverGrandeCity_EventScript_LVOldWoman_Post:
	msgbox EverGrandeCity_Text_LVOldWoman_Post, MSGBOX_DEFAULT
	release
	end

EverGrandeCity_Text_LVOldWoman:
	.string "Sixty years I've lived at the foot\nof the POKeMON LEAGUE.\pNever been inside. Have you seen\nthe stairs? Have you seen my knees?$"

EverGrandeCity_Text_LVOldWoman_Post:
	.string "A new CHAMPION, they say.\pLovely. Could you install a lift?\nThat's what a CHAMPION is for.$"

EverGrandeCity_EventScript_LVFisherman::
	msgbox EverGrandeCity_Text_LVFisherman, MSGBOX_NPC
	end

EverGrandeCity_Text_LVFisherman:
	.string "Best fishing spot in HOENN, right\nunder the waterfall.\pEvery trainer who loses in there\nthrows a POKe BALL off the cliff.\lI catch about four a day.$"
@ --- einde land_vulling ---
