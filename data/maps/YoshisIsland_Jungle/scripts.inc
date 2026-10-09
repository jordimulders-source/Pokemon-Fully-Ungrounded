@ Project Grounded: Yoshi's Island, de jungle (tools/grounded/maptools/yoshis_island.py)
YoshisIsland_Jungle_MapScripts::
	.byte 0

YoshisIsland_Jungle_EventScript_Poochy::
	lock
	faceplayer
	goto_if_set FLAG_YI_POOCHY_MET, YoshisIsland_Jungle_EventScript_PoochyRide
	setflag FLAG_YI_POOCHY_MET
	msgbox YoshisIsland_Jungle_Text_PoochyMeet, MSGBOX_DEFAULT
YoshisIsland_Jungle_EventScript_PoochyRide::
	msgbox YoshisIsland_Jungle_Text_PoochyRide, MSGBOX_DEFAULT
	closemessage
	getplayerxy VAR_TEMP_0, VAR_TEMP_1
	goto_if_gt VAR_TEMP_0, 10, YoshisIsland_Jungle_EventScript_PoochyWest
	applymovement LOCALID_YI_POOCHY, YoshisIsland_Jungle_EventScript_Movement_PoochyEast
	applymovement OBJ_EVENT_ID_PLAYER, YoshisIsland_Jungle_EventScript_Movement_PlayerEast
	waitmovement 0
	fadescreenswapbuffers FADE_TO_BLACK
	setobjectxyperm LOCALID_YI_POOCHY, 10, 8
	setobjectxy LOCALID_YI_POOCHY, 10, 8
	turnobject LOCALID_YI_POOCHY, DIR_EAST
	fadescreenswapbuffers FADE_FROM_BLACK
	release
	end

YoshisIsland_Jungle_EventScript_PoochyWest::
	applymovement LOCALID_YI_POOCHY, YoshisIsland_Jungle_EventScript_Movement_PoochyWest
	applymovement OBJ_EVENT_ID_PLAYER, YoshisIsland_Jungle_EventScript_Movement_PlayerWest
	waitmovement 0
	call_if_unset FLAG_YI_POOCHY_DUG, YoshisIsland_Jungle_EventScript_PoochyDig
	fadescreenswapbuffers FADE_TO_BLACK
	setobjectxyperm LOCALID_YI_POOCHY, 8, 8
	setobjectxy LOCALID_YI_POOCHY, 8, 8
	turnobject LOCALID_YI_POOCHY, DIR_WEST
	fadescreenswapbuffers FADE_FROM_BLACK
	release
	end

YoshisIsland_Jungle_EventScript_PoochyDig::
	applymovement LOCALID_YI_POOCHY, YoshisIsland_Jungle_EventScript_Movement_PoochySniff
	waitmovement 0
	playse SE_M_DIG
	msgbox YoshisIsland_Jungle_Text_PoochyDig, MSGBOX_DEFAULT
	giveitem ITEM_STRANGE_SOUVENIR, 1
	setflag FLAG_YI_POOCHY_DUG
	setflag FLAG_ITEM_YOSHIS_ISLAND_JUNGLE_STRANGE_SOUVENIR
	closemessage
	return

YoshisIsland_Jungle_EventScript_Movement_PoochyEast:
	walk_fast_right
	walk_fast_right
	walk_fast_right
	walk_fast_right
	step_end

YoshisIsland_Jungle_EventScript_Movement_PlayerEast:
	walk_fast_right
	walk_fast_right
	walk_fast_right
	walk_fast_right
	step_end

YoshisIsland_Jungle_EventScript_Movement_PoochyWest:
	walk_fast_left
	walk_fast_left
	walk_fast_left
	walk_fast_left
	step_end

YoshisIsland_Jungle_EventScript_Movement_PlayerWest:
	walk_fast_left
	walk_fast_left
	walk_fast_left
	walk_fast_left
	step_end

YoshisIsland_Jungle_EventScript_Movement_PoochySniff:
	face_down
	jump_in_place_down
	face_left
	jump_in_place_left
	step_end

YoshisIsland_Jungle_EventScript_NepEnut::
	lock
	faceplayer
	msgbox YoshisIsland_Jungle_Text_Nep1, MSGBOX_DEFAULT
	closemessage
	applymovement LOCALID_YI_NEP_ENUT, YoshisIsland_Jungle_EventScript_Movement_NepJump
	waitmovement 0
	playmoncry SPECIES_DONDOZO, CRY_MODE_ENCOUNTER
	msgbox YoshisIsland_Jungle_Text_Nep2, MSGBOX_DEFAULT
	waitmoncry
	closemessage
	setwildbattle SPECIES_DONDOZO, 90
	dowildbattle
	specialvar VAR_RESULT, GetBattleOutcome
	goto_if_eq VAR_RESULT, B_OUTCOME_WON, YoshisIsland_Jungle_EventScript_NepGone
	goto_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, YoshisIsland_Jungle_EventScript_NepGone
	msgbox YoshisIsland_Jungle_Text_NepStill, MSGBOX_DEFAULT
	release
	end

YoshisIsland_Jungle_EventScript_NepGone::
	fadescreenswapbuffers FADE_TO_BLACK
	removeobject LOCALID_YI_NEP_ENUT
	setflag FLAG_YI_NEP_ENUT_DONE
	fadescreenswapbuffers FADE_FROM_BLACK
	msgbox YoshisIsland_Jungle_Text_NepGone, MSGBOX_DEFAULT
	release
	end

YoshisIsland_Jungle_EventScript_Movement_NepJump:
	jump_in_place_down
	jump_in_place_down
	jump_in_place_down
	step_end

YoshisIsland_Jungle_EventScript_Movement_CloudPop:
	jump_in_place_down
	jump_in_place_down
	step_end

YoshisIsland_Jungle_EventScript_Cloud::
	lock
	playse SE_BALLOON_RED
	applymovement LOCALID_YI_JUNGLE_CLOUD, YoshisIsland_Jungle_EventScript_Movement_CloudPop
	waitmovement 0
	removeobject LOCALID_YI_JUNGLE_CLOUD
	setflag FLAG_ITEM_YOSHIS_ISLAND_JUNGLE_MOOMOO_MILK
	playse SE_BALLOON_BLUE
	msgbox YoshisIsland_Jungle_Text_Cloud, MSGBOX_DEFAULT
	giveitem ITEM_MOOMOO_MILK, 3
	release
	end

YoshisIsland_Jungle_EventScript_ShyGuy::
	trainerbattle_single TRAINER_YI_SHY_GUY_JUNGLE, YoshisIsland_Jungle_Text_ShyGuyIntro, YoshisIsland_Jungle_Text_ShyGuyDefeat
	msgbox YoshisIsland_Jungle_Text_ShyGuyPost, MSGBOX_AUTOCLOSE
	end

YoshisIsland_Jungle_EventScript_MsgEntrance::
	msgbox YoshisIsland_Jungle_Text_MsgEntrance, MSGBOX_SIGN
	end

YoshisIsland_Jungle_EventScript_MsgThorns::
	msgbox YoshisIsland_Jungle_Text_MsgThorns, MSGBOX_SIGN
	end

YoshisIsland_Jungle_EventScript_MsgLake::
	msgbox YoshisIsland_Jungle_Text_MsgLake, MSGBOX_SIGN
	end

YoshisIsland_Jungle_EventScript_EggBlock::
	msgbox YoshisIsland_Jungle_Text_EggBlock, MSGBOX_SIGN
	end

@ ---------------------------------------------------------------- teksten (placeholders, Jordi herschrijft ze)
YoshisIsland_Jungle_Text_PoochyMeet:
	.string "POOCHY: Ruff!\p"
	.string "(This dog's name is POOCHY. He's pretty\n"
	.string "cute, huh? He does not care about\l"
	.string "thorns. He has never cared about\l"
	.string "anything except running in the\l"
	.string "direction you are facing.)$"

YoshisIsland_Jungle_Text_PoochyRide:
	.string "POOCHY: RUFF RUFF! (Hitch a ride!)$"

YoshisIsland_Jungle_Text_PoochyDig:
	.string "(POOCHY sniffs the ground, digs like his\n"
	.string "life depends on it, and proudly drops\l"
	.string "something at your feet. It is a\l"
	.string "souvenir. Of what, nobody knows. POOCHY\l"
	.string "knows. POOCHY isn't telling.)$"

YoshisIsland_Jungle_Text_Nep1:
	.string "???: Yoshi!\p"
	.string "(A blue YOSHI waves at you from the\n"
	.string "shore. He has very big teeth. He has\l"
	.string "more teeth than YOSHI. He has more\l"
	.string "teeth than most sharks.)$"

YoshisIsland_Jungle_Text_Nep2:
	.string "NEP-ENUT: YOSHIIIIIIII!!\p"
	.string "(That is not a YOSHI. That was never a\n"
	.string "YOSHI. It's NEP-ENUT, a DONDOZO in a\l"
	.string "blue YOSHI costume that has been\l"
	.string "waiting at this lake for someone\l"
	.string "gullible to walk past.)$"

YoshisIsland_Jungle_Text_NepStill:
	.string "(NEP-ENUT climbs back into his costume\n"
	.string "and waves again, slightly less\l"
	.string "convincingly.)$"

YoshisIsland_Jungle_Text_NepGone:
	.string "(The blue YOSHI costume is lying empty\n"
	.string "on the shore. It is soaking wet. It\l"
	.string "smells like a whole lake.)$"

YoshisIsland_Jungle_Text_Cloud:
	.string "POP! The ? CLOUD bursts and it rains\n"
	.string "milk. Only on you.\p"
	.string "You caught some of it in bottles. You\n"
	.string "had bottles. You have always had\l"
	.string "bottles.$"

YoshisIsland_Jungle_Text_ShyGuyIntro:
	.string "(The JUNGLE GUY has painted his mask\n"
	.string "green for camouflage. He is standing on\l"
	.string "a yellow path.)$"

YoshisIsland_Jungle_Text_ShyGuyDefeat:
	.string "(The JUNGLE GUY quietly unpaints his\n"
	.string "mask.)$"

YoshisIsland_Jungle_Text_ShyGuyPost:
	.string "(The JUNGLE GUY is pretending to be a\n"
	.string "bush. You are being polite about it.)$"

YoshisIsland_Jungle_Text_MsgEntrance:
	.string "MESSAGE BLOCK: Welcome to the jungle!\n"
	.string "We've got fun and games! Mostly games.\l"
	.string "Mostly SHY GUYS.\p"
	.string "MESSAGE BLOCK: Tip: the tall grass is\n"
	.string "level 91. It does not care about your\l"
	.string "feelings.$"

YoshisIsland_Jungle_Text_MsgThorns:
	.string "MESSAGE BLOCK: THORNS! YOSHIS can't\n"
	.string "walk on thorns. Trainers can't walk on\l"
	.string "thorns.\p"
	.string "MESSAGE BLOCK: POOCHY can walk on\n"
	.string "thorns. POOCHY can walk on anything.\l"
	.string "Science stopped asking.$"

YoshisIsland_Jungle_Text_MsgLake:
	.string "MESSAGE BLOCK: Please do not feed the\n"
	.string "blue YOSHI.\p"
	.string "MESSAGE BLOCK: There is no blue YOSHI.\n"
	.string "If you see a blue YOSHI, please re-read\l"
	.string "this sign.$"

YoshisIsland_Jungle_Text_EggBlock:
	.string "(An EGG BLOCK. You bonk it. An egg pops\n"
	.string "out, rolls into the jungle and is never\l"
	.string "seen again. EGG BLOCKS are like that.)$"
