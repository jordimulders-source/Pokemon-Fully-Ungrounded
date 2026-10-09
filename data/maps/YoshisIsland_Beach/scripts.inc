@ Project Grounded: Yoshi's Island, het strand (tools/grounded/maptools/yoshis_island.py)
YoshisIsland_Beach_MapScripts::
	map_script MAP_SCRIPT_ON_TRANSITION, YoshisIsland_Beach_OnTransition
	map_script MAP_SCRIPT_ON_FRAME_TABLE, YoshisIsland_Beach_OnFrame
	.byte 0

YoshisIsland_Beach_OnTransition:
	call_if_set FLAG_YI_ARRIVED, YoshisIsland_Beach_EventScript_SetArrived
	end

YoshisIsland_Beach_EventScript_SetArrived::
	setvar VAR_TEMP_1, 1
	return

YoshisIsland_Beach_OnFrame:
	map_script_2 VAR_TEMP_1, 0, YoshisIsland_Beach_EventScript_Arrival
	.2byte 0

YoshisIsland_Beach_EventScript_Arrival::
	lockall
	setvar VAR_TEMP_1, 1
	setflag FLAG_YI_ARRIVED
	setvar VAR_0x8004, 2
	setvar VAR_0x8005, 2
	setvar VAR_0x8006, 10
	setvar VAR_0x8007, 4
	special ShakeCamera
	waitstate
	playse SE_FALL
	msgbox YoshisIsland_Beach_Text_Arrival1, MSGBOX_DEFAULT
	closemessage
	playse SE_PIN
	applymovement LOCALID_YI_BEACH_YOSHI, YoshisIsland_Beach_EventScript_Movement_YoshiIn
	waitmovement 0
	applymovement OBJ_EVENT_ID_PLAYER, Common_Movement_FaceLeft
	waitmovement 0
	msgbox YoshisIsland_Beach_Text_Arrival2, MSGBOX_DEFAULT
	closemessage
	applymovement LOCALID_YI_BEACH_YOSHI, YoshisIsland_Beach_EventScript_Movement_YoshiBack
	waitmovement 0
	msgbox YoshisIsland_Beach_Text_Arrival3, MSGBOX_DEFAULT
	releaseall
	end

YoshisIsland_Beach_EventScript_Movement_YoshiIn:
	walk_fast_down
	walk_fast_down
	walk_fast_down
	walk_fast_right
	face_right
	jump_in_place_right
	step_end

YoshisIsland_Beach_EventScript_Movement_YoshiBack:
	walk_left
	walk_up
	walk_up
	walk_up
	face_down
	step_end

YoshisIsland_Beach_EventScript_Yoshi::
	lock
	faceplayer
	goto_if_set FLAG_YI_WARIO_DONE, YoshisIsland_Beach_EventScript_YoshiDone
	msgbox YoshisIsland_Beach_Text_YoshiPipe, MSGBOX_DEFAULT
	release
	end

YoshisIsland_Beach_EventScript_YoshiDone::
	msgbox YoshisIsland_Beach_Text_YoshiDone, MSGBOX_DEFAULT
	release
	end

YoshisIsland_Beach_EventScript_Guards::
	lock
	faceplayer
	goto YoshisIsland_Beach_EventScript_GuardsBattle

YoshisIsland_Beach_EventScript_GuardsWon::
	msgbox YoshisIsland_Beach_Text_GuardsWon, MSGBOX_DEFAULT
	closemessage
	fadescreenswapbuffers FADE_TO_BLACK
	removeobject LOCALID_YI_BEACH_GUARD_A
	removeobject LOCALID_YI_BEACH_GUARD_B
	removeobject LOCALID_YI_BEACH_YOSHI
	setflag FLAG_YI_BEACH_GUARDS
	setflag FLAG_YI_YOSHI_AHEAD
	fadescreenswapbuffers FADE_FROM_BLACK
	msgbox YoshisIsland_Beach_Text_YoshiAhead, MSGBOX_DEFAULT
	release
	end

YoshisIsland_Beach_EventScript_GuardsBattle::
	msgbox YoshisIsland_Beach_Text_GuardsIntro, MSGBOX_DEFAULT
	closemessage
YoshisIsland_Beach_EventScript_GuardsChoose::
	special SavePlayerParty
	fadescreen FADE_TO_BLACK
	special ChooseHalfPartyForBattle
	waitstate
	goto_if_ne VAR_RESULT, 0, YoshisIsland_Beach_EventScript_GuardsFight
	special LoadPlayerParty
	goto YoshisIsland_Beach_EventScript_GuardsChoose

YoshisIsland_Beach_EventScript_GuardsFight::
	multi_2_vs_2 TRAINER_YI_SHY_GUY_BEACH_A, YoshisIsland_Beach_Text_GuardsDefeatA, TRAINER_YI_SHY_GUY_BEACH_B, YoshisIsland_Beach_Text_GuardsDefeatB, PARTNER_YOSHI
	switch VAR_RESULT
	case 1, YoshisIsland_Beach_EventScript_GuardsWon
	fadescreen FADE_TO_BLACK
	special SetCB2WhiteOut
	waitstate

YoshisIsland_Beach_EventScript_Sign::
	msgbox YoshisIsland_Beach_Text_Sign, MSGBOX_SIGN
	end

YoshisIsland_Beach_EventScript_Movement_CloudPop:
	jump_in_place_down
	jump_in_place_down
	step_end

YoshisIsland_Beach_EventScript_Cloud::
	lock
	playse SE_BALLOON_RED
	applymovement LOCALID_YI_BEACH_CLOUD, YoshisIsland_Beach_EventScript_Movement_CloudPop
	waitmovement 0
	removeobject LOCALID_YI_BEACH_CLOUD
	setflag FLAG_ITEM_YOSHIS_ISLAND_BEACH_SHALOUR_SABLE
	playse SE_BALLOON_BLUE
	msgbox YoshisIsland_Beach_Text_Cloud, MSGBOX_DEFAULT
	giveitem ITEM_SHALOUR_SABLE, 2
	release
	end

YoshisIsland_Beach_EventScript_MsgBlock::
	msgbox YoshisIsland_Beach_Text_MsgBlock, MSGBOX_SIGN
	end

@ ---------------------------------------------------------------- teksten (placeholders, Jordi herschrijft ze)
YoshisIsland_Beach_Text_Arrival1:
	.string "Something went wrong.\p"
	.string "The ????? rift spits you out of a hole\n"
	.string "in the sky, high above an island that\l"
	.string "looks like it was drawn with crayons.\l"
	.string "You fall for a very long time. You land\l"
	.string "face-first in warm sand.\p"
	.string "Nothing is broken. The art style would\n"
	.string "never allow it.$"

YoshisIsland_Beach_Text_Arrival2:
	.string "YOSHI: Yoshi?\p"
	.string "(A green dinosaur in red shoes pokes\n"
	.string "you with his nose, decides you are not a\l"
	.string "melon, and looks relieved for both of\l"
	.string "you.)\p"
	.string "YOSHI: Yoshi! Yoshi yoshi!\p"
	.string "(Roughly: the SHY GUYS took over the\n"
	.string "island. They stole the eggs, the flags\l"
	.string "and the fun. He could use a trainer. You\l"
	.string "will do.)$"

YoshisIsland_Beach_Text_Arrival3:
	.string "(YOSHI points at the green pipe up the\n"
	.string "path. Two SHY GUYS are standing in\l"
	.string "front of it, trying very hard to look\l"
	.string "like a wall.)$"

YoshisIsland_Beach_Text_YoshiPipe:
	.string "YOSHI: Yoshi!\p"
	.string "(He points at the SHY GUYS by the pipe,\n"
	.string "then at you, then at himself. Two\l"
	.string "against two. He has done the maths. It\l"
	.string "is the only maths he knows.)$"

YoshisIsland_Beach_Text_YoshiDone:
	.string "YOSHI: Yoshi... yoshi!\p"
	.string "(He waves at the rift with his whole\n"
	.string "body. The island is safe, the eggs are\l"
	.string "home, and he will keep your spot on the\l"
	.string "beach warm. Literally. He is lying on it.)$"

YoshisIsland_Beach_Text_GuardsWon:
	.string "(The SHY GUYS shuffle aside. One of\n"
	.string "them writes something in a tiny\l"
	.string "notebook. It is probably your name. It\l"
	.string "is probably misspelled.)$"

YoshisIsland_Beach_Text_YoshiAhead:
	.string "YOSHI: Yoshi!\p"
	.string "(YOSHI dives headfirst into the pipe.\n"
	.string "There is a loud BWOING. Then, faintly,\l"
	.string "from very far away: 'yoshi'.)$"

YoshisIsland_Beach_Text_GuardsIntro:
	.string "(Two SHY GUYS block the pipe. They do\n"
	.string "not speak. The red one adjusts his\l"
	.string "mask. The green one adjusts his mask in\l"
	.string "solidarity.)\p"
	.string "YOSHI: Yoshi!\p"
	.string "(YOSHI hops next to you. Pick three\n"
	.string "POKéMON; he brings his own.)$"

YoshisIsland_Beach_Text_GuardsDefeatA:
	.string "(The SHY GUY stares at you. It's unclear\n"
	.string "whether it's judging you. It is.)$"

YoshisIsland_Beach_Text_GuardsDefeatB:
	.string "(The SHYER GUY hides behind the SHY\n"
	.string "GUY. Nobody was ready for this level of\l"
	.string "shyness.)$"

YoshisIsland_Beach_Text_Sign:
	.string "WELCOME TO YOSHI'S ISLAND\n"
	.string "Population: Yoshis. Also SHY GUYS,\l"
	.string "temporarily.\l"
	.string "Please do not eat the scenery. (Yoshis\l"
	.string "excepted.)$"

YoshisIsland_Beach_Text_Cloud:
	.string "POP! The ? CLOUD bursts. It was full of\n"
	.string "biscuits.\p"
	.string "Nobody knows how biscuits get into\n"
	.string "clouds. Nobody on this island has ever\l"
	.string "asked.$"

YoshisIsland_Beach_Text_MsgBlock:
	.string "MESSAGE BLOCK: Hi! I'm a MESSAGE BLOCK!\n"
	.string "Hit me from below for a helpful hint!\p"
	.string "MESSAGE BLOCK: ...you can't. This game is\n"
	.string "top-down. Fine. The hint is free: the\l"
	.string "pipe on the right goes to the jungle.\l"
	.string "The jungle has a lake. The lake has a\l"
	.string "YOSHI in it that is not a YOSHI.$"
