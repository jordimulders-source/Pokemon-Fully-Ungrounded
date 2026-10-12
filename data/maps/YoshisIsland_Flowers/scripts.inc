@ Project Grounded: Yoshi's Island, het bloemenveld (tools/grounded/maptools/yoshis_island.py)
YoshisIsland_Flowers_MapScripts::
	map_script MAP_SCRIPT_ON_LOAD, YoshisIsland_Flowers_OnLoad
	.byte 0

YoshisIsland_Flowers_OnLoad:
	call_if_set FLAG_YI_BRIDGE_CLOUD, YoshisIsland_Flowers_EventScript_SetBridge
	end

YoshisIsland_Flowers_EventScript_SetBridge::
	setmetatile 17, 11, 0x2E3, FALSE
	setmetatile 17, 12, 0x2E4, FALSE
	setmetatile 17, 13, 0x2E5, FALSE
	setmetatile 17, 14, 0x2E6, FALSE
	setmetatile 18, 11, 0x2E7, FALSE
	setmetatile 18, 12, 0x2E8, FALSE
	setmetatile 18, 13, 0x2E9, FALSE
	setmetatile 18, 14, 0x2EA, FALSE
	return

YoshisIsland_Flowers_EventScript_BridgeCloud::
	lock
	playse SE_BALLOON_RED
	applymovement LOCALID_YI_BRIDGE_CLOUD, YoshisIsland_Flowers_EventScript_Movement_CloudPop
	waitmovement 0
	removeobject LOCALID_YI_BRIDGE_CLOUD
	setflag FLAG_YI_BRIDGE_CLOUD
	playse SE_DING_DONG
	call YoshisIsland_Flowers_EventScript_SetBridge
	special DrawWholeMapView
	msgbox YoshisIsland_Flowers_Text_BridgeCloud, MSGBOX_DEFAULT
	release
	end

YoshisIsland_Flowers_EventScript_Movement_CloudPop:
	jump_in_place_down
	jump_in_place_down
	step_end

YoshisIsland_Flowers_EventScript_Cloud::
	lock
	playse SE_BALLOON_RED
	applymovement LOCALID_YI_FLOWERS_CLOUD, YoshisIsland_Flowers_EventScript_Movement_CloudPop
	waitmovement 0
	removeobject LOCALID_YI_FLOWERS_CLOUD
	setflag FLAG_ITEM_YOSHIS_ISLAND_FLOWERS_LUMIOSE_GALETTE
	playse SE_BALLOON_BLUE
	msgbox YoshisIsland_Flowers_Text_Cloud, MSGBOX_DEFAULT
	giveitem ITEM_LUMIOSE_GALETTE, 2
	release
	end

YoshisIsland_Flowers_EventScript_ShyGuy::
	trainerbattle_single TRAINER_YI_SHY_GUY_FLOWERS, YoshisIsland_Flowers_Text_ShyGuyIntro, YoshisIsland_Flowers_Text_ShyGuyDefeat
	msgbox YoshisIsland_Flowers_Text_ShyGuyPost, MSGBOX_AUTOCLOSE
	end

YoshisIsland_Flowers_EventScript_MsgEntrance::
	msgbox YoshisIsland_Flowers_Text_MsgEntrance, MSGBOX_SIGN
	end

YoshisIsland_Flowers_EventScript_MsgGoal::
	msgbox YoshisIsland_Flowers_Text_MsgGoal, MSGBOX_SIGN
	end

YoshisIsland_Flowers_EventScript_MsgBridge::
	msgbox YoshisIsland_Flowers_Text_MsgBridge, MSGBOX_SIGN
	end

YoshisIsland_Flowers_EventScript_Switch::
	msgbox YoshisIsland_Flowers_Text_Switch, MSGBOX_SIGN
	end

YoshisIsland_Flowers_EventScript_EggBlock::
	msgbox YoshisIsland_Flowers_Text_EggBlock, MSGBOX_SIGN
	end

@ ---------------------------------------------------------------- teksten (placeholders, Jordi herschrijft ze)
YoshisIsland_Flowers_Text_BridgeCloud:
	.string "POP! The ? CLOUD bursts and a row of\n"
	.string "little rafts unrolls across the gap, like\l"
	.string "a carpet that has been waiting its\l"
	.string "whole life for this.\p"
	.string "It's a bridge now. Don't look down. Down\n"
	.string "is also clouds.$"

YoshisIsland_Flowers_Text_Cloud:
	.string "POP! The ? CLOUD bursts and two\n"
	.string "galettes float down, still warm.\p"
	.string "The sky bakes. Nobody told you the sky\n"
	.string "bakes.$"

YoshisIsland_Flowers_Text_ShyGuyIntro:
	.string "(The GROOVY GUY has a flower stuck in\n"
	.string "his mask. It's the 70s up here. It's\l"
	.string "always the 70s up here.)$"

YoshisIsland_Flowers_Text_ShyGuyDefeat:
	.string "(The GROOVY GUY gives you the flower.\n"
	.string "It wilts immediately. Bad vibes.)$"

YoshisIsland_Flowers_Text_ShyGuyPost:
	.string "(The GROOVY GUY is lying in the grass,\n"
	.string "watching the clouds. The clouds are\l"
	.string "below him. He has not noticed.)$"

YoshisIsland_Flowers_Text_MsgEntrance:
	.string "MESSAGE BLOCK: FLOWER FIELD, ABOVE THE\n"
	.string "CLOUDS.\p"
	.string "MESSAGE BLOCK: Safety notice: the\n"
	.string "edges are clouds. Clouds are not floors.\l"
	.string "We have had complaints. Well. We had\l"
	.string "complaints.$"

YoshisIsland_Flowers_Text_MsgGoal:
	.string "MESSAGE BLOCK: Congratulations, you\n"
	.string "reached the GOAL!\p"
	.string "MESSAGE BLOCK: There is no bonus\n"
	.string "roulette. There is no score screen.\l"
	.string "There is a CHERISH BALL and a deep\l"
	.string "sense of closure.$"

YoshisIsland_Flowers_Text_MsgBridge:
	.string "MESSAGE BLOCK: No bridge? Pop the ?\n"
	.string "CLOUD!\p"
	.string "MESSAGE BLOCK: ? CLOUDS contain items,\n"
	.string "bridges or disappointment. The odds are\l"
	.string "not published.$"

YoshisIsland_Flowers_Text_Switch:
	.string "(A red ! SWITCH. In another game it\n"
	.string "would make things solid. You press it\l"
	.string "anyway.\p"
	.string "Somewhere, something becomes slightly\n"
	.string "more solid. You will never find out\l"
	.string "what.)$"

YoshisIsland_Flowers_Text_EggBlock:
	.string "(An EGG BLOCK. It's out of eggs. There's\n"
	.string "a little sign: BACK IN 5 MINUTES. The\l"
	.string "sign is dated three games ago.)$"
