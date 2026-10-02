VerdanturfTown_MapScripts::
	map_script MAP_SCRIPT_ON_TRANSITION, VerdanturfTown_OnTransition
	.byte 0

VerdanturfTown_OnTransition:
	setflag FLAG_VISITED_VERDANTURF_TOWN
	setvar VAR_CONTEST_HALL_STATE, 0
	@ Project Grounded: Birch staat hier pas na zijn gevecht op Route 109
	setflag FLAG_HIDE_VERDANTURF_BIRCH
	goto_if_defeated TRAINER_BIRCH, VerdanturfTown_EventScript_ShowBirch
	end

VerdanturfTown_EventScript_ShowBirch::
	clearflag FLAG_HIDE_VERDANTURF_BIRCH
	end

VerdanturfTown_EventScript_Twin::
	lock
	faceplayer
	goto_if_set FLAG_RUSTURF_TUNNEL_OPENED, VerdanturfTown_EventScript_TwinTunnelOpen
	msgbox VerdanturfTown_Text_ManTryingToDigTunnel, MSGBOX_DEFAULT
	applymovement LOCALID_VERDANTURF_TWIN, Common_Movement_FaceOriginalDirection
	waitmovement 0
	release
	end

VerdanturfTown_EventScript_TwinTunnelOpen::
	msgbox VerdanturfTown_Text_ManDugTunnelForLove, MSGBOX_DEFAULT
	applymovement LOCALID_VERDANTURF_TWIN, Common_Movement_FaceOriginalDirection
	waitmovement 0
	release
	end

VerdanturfTown_EventScript_Man::
	msgbox VerdanturfTown_Text_AirCleanHere, MSGBOX_NPC
	end

VerdanturfTown_EventScript_Camper::
	msgbox VerdanturfTown_Text_MakeBattleTentDebut, MSGBOX_NPC
	end

VerdanturfTown_EventScript_Boy::
	lock
	faceplayer
	goto_if_set FLAG_RUSTURF_TUNNEL_OPENED, VerdanturfTown_EventScript_BoyTunnelOpen
	msgbox VerdanturfTown_Text_GuyTryingToBustThroughCave, MSGBOX_DEFAULT
	release
	end

VerdanturfTown_EventScript_BoyTunnelOpen::
	msgbox VerdanturfTown_Text_EasyToGetToRustboroNow, MSGBOX_DEFAULT
	release
	end

VerdanturfTown_EventScript_TownSign::
	msgbox VerdanturfTown_Text_TownSign, MSGBOX_SIGN
	end

VerdanturfTown_EventScript_WandasHouseSign::
	msgbox VerdanturfTown_Text_WandasHouse, MSGBOX_SIGN
	end

VerdanturfTown_EventScript_BattleTentSign::
	msgbox VerdanturfTown_Text_BattleTentSign, MSGBOX_SIGN
	end

VerdanturfTown_EventScript_RusturfTunnelSign::
	msgbox VerdanturfTown_Text_RusturfTunnelSign, MSGBOX_SIGN
	end

VerdanturfTown_Text_ManTryingToDigTunnel:
	.string "My papa told me.\p"
	.string "This tunnel is full of timid POKéMON.\p"
	.string "They freak out from loud noises.\p"
	.string "So they stopped the big tunnel project.\p"
	.string "But one man is digging it all by himself!\n"
	.string "With a spoon, probably!$"

VerdanturfTown_Text_ManDugTunnelForLove:
	.string "There was a man who dug a whole tunnel\n"
	.string "for a lady he loved.\p"
	.string "I just text my girlfriend.$"

VerdanturfTown_Text_AirCleanHere:
	.string "The air is clean here.\p"
	.string "That's it. That's the whole town.\p"
	.string "VERDANTURF is lamer than TEAM FLARE.\p"
	.string "At least they had a plan.$"

VerdanturfTown_Text_MakeBattleTentDebut:
	.string "My POKéMON and I are on a hot winning\n"
	.string "streak.\p"
	.string "So I'm making my BATTLE TENT debut\n"
	.string "here. Pray for me.$"

VerdanturfTown_Text_GuyTryingToBustThroughCave:
	.string "Did you see the cave next to the\n"
	.string "POKéMON MART?\p"
	.string "There's a guy in there smashing\n"
	.string "boulders to get to the other side.\p"
	.string "It'd be great if it went through… Then\n"
	.string "we could go to RUSTBORO without a\l"
	.string "three-day detour.$"

VerdanturfTown_Text_EasyToGetToRustboroNow:
	.string "The cave next to the MART is a tunnel\n"
	.string "now!\p"
	.string "Now I can go buy new DEVON stuff in\n"
	.string "RUSTBORO every day. My wallet hates it.$"

VerdanturfTown_Text_TownSign:
	.string "VERDANTURF TOWN\p"
	.string "“The windswept highlands with the\n"
	.string "sweet fragrance of grass. Hay fever\l"
	.string "capital of HOENN.”$"

VerdanturfTown_Text_WandasHouse:
	.string "WANDA'S HOUSE\p"
	.string "(Her boyfriend lives in the tunnel.)$"

VerdanturfTown_Text_BattleTentSign:
	.string "BATTLE TENT VERDANTURF SITE\n"
	.string "“Feast Your Eyes on Battles!”$"

VerdanturfTown_Text_RusturfTunnelSign:
	.string "RUSTURF TUNNEL\n"
	.string "“Linking RUSTBORO and VERDANTURF.\p"
	.string "”The tunnel project has been canceled.\n"
	.string "Walk.“$"

@ ---------------------------------------------------------------- Project Grounded: Birch en de Hoenn-Grimer
VerdanturfTown_EventScript_Birch::
	lock
	faceplayer
	goto_if_defeated TRAINER_BIRCH_VERDANTURF, VerdanturfTown_EventScript_BirchPostBattle
	msgbox VerdanturfTown_Text_BirchIntro, MSGBOX_DEFAULT
	trainerbattle_no_intro TRAINER_BIRCH_VERDANTURF, VerdanturfTown_Text_BirchDefeat
	msgbox VerdanturfTown_Text_BirchPostBattle, MSGBOX_DEFAULT
	applymovement LOCALID_VERDANTURF_BIRCH, Common_Movement_FaceDown
	waitmovement 0
	release
	end

VerdanturfTown_EventScript_BirchPostBattle::
	msgbox VerdanturfTown_Text_BirchPostBattle, MSGBOX_DEFAULT
	applymovement LOCALID_VERDANTURF_BIRCH, Common_Movement_FaceDown
	waitmovement 0
	release
	end

VerdanturfTown_Text_BirchIntro:
	.string "BIRCH: Shh! {PLAYER}, look at\n"
	.string "this soil. LOOK at it.\p"
	.string "Dark. Crumbly. Fragrant.\n"
	.string "The richest earth in all of HOENN.\p"
	.string "And do you know why? Natural\n"
	.string "fertilizer! A whole new form of\l"
	.string "GRIMER lives in these fields!\p"
	.string "Brown, earthy, and made of… well.\n"
	.string "Of exactly what you think.\p"
	.string "I am its biggest fan. I have\n"
	.string "a poster. I have TWO posters.\p"
	.string "Here, let me show you. Up close.$"

VerdanturfTown_Text_BirchDefeat:
	.string "BIRCH: Even in defeat, it smells\n"
	.string "like progress!$"

VerdanturfTown_Text_BirchPostBattle:
	.string "BIRCH: The farmers here say their\n"
	.string "carrots have never been bigger.\p"
	.string "They also say they would like me\n"
	.string "to stop kneeling in their fields.$"
