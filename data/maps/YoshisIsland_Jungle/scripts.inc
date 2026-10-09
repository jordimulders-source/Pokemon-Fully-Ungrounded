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
	goto_if_set FLAG_YI_NEP_ENUT_DONE, YoshisIsland_Jungle_EventScript_NepChill
	msgbox YoshisIsland_Jungle_Text_Nep1, MSGBOX_DEFAULT
	closemessage
	@ hij is 8 tegels hoog: de camera kijkt even omhoog, anders valt zijn kop buiten beeld
	special SpawnCameraObject
	applymovement OBJ_EVENT_ID_CAMERA, YoshisIsland_Jungle_EventScript_Movement_CamUp
	waitmovement 0
	playse SE_M_DIVE
	applymovement LOCALID_YI_NEP_ENUT, YoshisIsland_Jungle_EventScript_Movement_NepRise
	delay 24
	playmoncry SPECIES_DONDOZO, CRY_MODE_ENCOUNTER
	msgbox YoshisIsland_Jungle_Text_Nep2, MSGBOX_DEFAULT
	waitmoncry
	closemessage
	applymovement OBJ_EVENT_ID_CAMERA, YoshisIsland_Jungle_EventScript_Movement_CamDown
	waitmovement 0
	special RemoveCameraObject
	setwildbattle SPECIES_DONDOZO, 90
	dowildbattle
	specialvar VAR_RESULT, GetBattleOutcome
	goto_if_eq VAR_RESULT, B_OUTCOME_WON, YoshisIsland_Jungle_EventScript_NepGone
	goto_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, YoshisIsland_Jungle_EventScript_NepGone
	msgbox YoshisIsland_Jungle_Text_NepStill, MSGBOX_DEFAULT
	release
	end

YoshisIsland_Jungle_EventScript_NepGone::
	setflag FLAG_YI_NEP_ENUT_DONE
	msgbox YoshisIsland_Jungle_Text_NepGone, MSGBOX_DEFAULT
	release
	end

YoshisIsland_Jungle_EventScript_NepChill::
	special SpawnCameraObject
	applymovement OBJ_EVENT_ID_CAMERA, YoshisIsland_Jungle_EventScript_Movement_CamUp
	waitmovement 0
	playse SE_M_DIVE
	applymovement LOCALID_YI_NEP_ENUT, Common_Movement_FaceUp
	waitmovement 0
	msgbox YoshisIsland_Jungle_Text_NepChill, MSGBOX_DEFAULT
	closemessage
	playse SE_M_DIVE
	applymovement LOCALID_YI_NEP_ENUT, Common_Movement_FaceDown
	waitmovement 0
	applymovement OBJ_EVENT_ID_CAMERA, YoshisIsland_Jungle_EventScript_Movement_CamDown
	waitmovement 0
	special RemoveCameraObject
	release
	end

YoshisIsland_Jungle_EventScript_Movement_NepRise:
	walk_in_place_slow_down
	walk_in_place_slow_down
	walk_in_place_slow_down
	walk_in_place_slow_down
	walk_in_place_slow_down
	walk_in_place_slow_down
	walk_in_place_slow_down
	walk_in_place_slow_down
	walk_in_place_slow_down
	walk_in_place_slow_down
	walk_in_place_slow_down
	walk_in_place_slow_down
	walk_in_place_slow_down
	walk_in_place_slow_down
	walk_in_place_slow_down
	walk_in_place_slow_down
	walk_in_place_slow_down
	walk_in_place_slow_down
	walk_in_place_slow_down
	walk_in_place_slow_down
	walk_in_place_slow_down
	walk_in_place_slow_down
	walk_in_place_slow_down
	walk_in_place_slow_down
	walk_in_place_slow_down
	walk_in_place_slow_down
	walk_in_place_slow_down
	walk_in_place_slow_down
	walk_in_place_slow_down
	walk_in_place_slow_down
	walk_in_place_slow_down
	walk_in_place_slow_down
	walk_in_place_slow_down
	walk_in_place_slow_down
	walk_in_place_slow_down
	walk_in_place_slow_down
	walk_in_place_slow_down
	walk_in_place_slow_down
	walk_in_place_slow_down
	walk_in_place_slow_down
	walk_in_place_slow_down
	walk_in_place_slow_down
	walk_in_place_slow_down
	walk_in_place_slow_down
	walk_in_place_slow_down
	walk_in_place_slow_down
	walk_in_place_slow_down
	walk_in_place_slow_down
	walk_in_place_slow_down
	walk_in_place_slow_down
	walk_in_place_slow_down
	walk_in_place_slow_down
	walk_in_place_slow_down
	walk_in_place_slow_down
	walk_in_place_slow_down
	walk_in_place_slow_down
	walk_in_place_slow_down
	walk_in_place_slow_down
	walk_in_place_slow_down
	walk_in_place_slow_down
	walk_in_place_slow_down
	walk_in_place_slow_down
	walk_in_place_slow_down
	walk_in_place_slow_down
	step_end

YoshisIsland_Jungle_EventScript_Movement_CamUp:
	walk_fast_up
	walk_fast_up
	walk_fast_up
	walk_fast_up
	step_end

YoshisIsland_Jungle_EventScript_Movement_CamDown:
	walk_fast_down
	walk_fast_down
	walk_fast_down
	walk_fast_down
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
	.string "(Two very angry eyebrows are floating\n"
	.string "on the lake. Under the eyebrows: eyes.\l"
	.string "Under the eyes: a lot more lake than you\l"
	.string "would like.)$"

YoshisIsland_Jungle_Text_Nep2:
	.string "NEP-ENUT: GLOOOORP!!\p"
	.string "(NEP-ENUT rises out of the lake. All of\n"
	.string "him. He used to chase YOSHI through\l"
	.string "entire levels. Then he found out you\l"
	.string "can just wait in a lake for people to\l"
	.string "come and look.)\p"
	.string "(Up close he's a DONDOZO. Most lake\n"
	.string "monsters are a fish if you get close\l"
	.string "enough. Nobody gets close enough.)$"

YoshisIsland_Jungle_Text_NepStill:
	.string "(NEP-ENUT sinks back down until only\n"
	.string "the eyebrows are left. The eyebrows\l"
	.string "keep watching. Judging, mostly.)$"

YoshisIsland_Jungle_Text_NepGone:
	.string "(NEP-ENUT sinks back down until only\n"
	.string "the eyebrows are left. He seems...\l"
	.string "relieved? Being a final boss for one\l"
	.string "lake is a lot of pressure.)$"

YoshisIsland_Jungle_Text_NepChill:
	.string "(NEP-ENUT rises out of the lake again.\n"
	.string "Slowly. Like a man getting off a couch.)\p"
	.string "NEP-ENUT: Oh. It's you. Listen. In my own\n"
	.string "game I was one gag in one level. Then\l"
	.string "the credits rolled and nobody called.\p"
	.string "NEP-ENUT: Here I got a lake, a DONDOZO,\n"
	.string "and 128 by 128 pixels. Some guy making a\l"
	.string "romhack in his spare time gave me more\l"
	.string "screen time than Nintendo ever did.\p"
	.string "NEP-ENUT: ...Don't tell Nintendo. GLORP.$"

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
	.string "eyebrows.\p"
	.string "MESSAGE BLOCK: The eyebrows are\n"
	.string "attached to something. The something\l"
	.string "is attached to the lake. Swimming is at\l"
	.string "your own risk. The risk is large. Very\l"
	.string "large. Larger than it looks.$"

YoshisIsland_Jungle_Text_EggBlock:
	.string "(An EGG BLOCK. You bonk it. An egg pops\n"
	.string "out, rolls into the jungle and is never\l"
	.string "seen again. EGG BLOCKS are like that.)$"
