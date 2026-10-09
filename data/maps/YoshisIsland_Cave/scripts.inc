@ Project Grounded: Yoshi's Island, kristalgrot (tools/grounded/maptools/yoshis_island.py)
YoshisIsland_Cave_MapScripts::
	.byte 0

YoshisIsland_Cave_EventScript_ShyGuy::
	trainerbattle_single TRAINER_YI_SHY_GUY_CAVE, YoshisIsland_Cave_Text_ShyGuyIntro, YoshisIsland_Cave_Text_ShyGuyDefeat
	msgbox YoshisIsland_Cave_Text_ShyGuyPost, MSGBOX_AUTOCLOSE
	end

YoshisIsland_Cave_EventScript_MsgBlock::
	msgbox YoshisIsland_Cave_Text_MsgBlock, MSGBOX_SIGN
	end

YoshisIsland_Cave_EventScript_EggBlock::
	msgbox YoshisIsland_Cave_Text_EggBlock, MSGBOX_SIGN
	end

YoshisIsland_Cave_EventScript_Bucket::
	msgbox YoshisIsland_Cave_Text_Bucket, MSGBOX_SIGN
	end

YoshisIsland_Cave_EventScript_Pow::
	msgbox YoshisIsland_Cave_Text_Pow, MSGBOX_SIGN
	end

@ ---------------------------------------------------------------- teksten (placeholders, Jordi herschrijft ze)
YoshisIsland_Cave_Text_ShyGuyIntro:
	.string "(The MINER GUY has a tiny lamp on his\n"
	.string "mask. He shines it in your eyes. On\l"
	.string "purpose.)$"

YoshisIsland_Cave_Text_ShyGuyDefeat:
	.string "(The MINER GUY's lamp flickers out. He\n"
	.string "keeps it on his mask out of principle.)$"

YoshisIsland_Cave_Text_ShyGuyPost:
	.string "(The MINER GUY is mining the same\n"
	.string "crystal he mined yesterday. It's a union\l"
	.string "thing.)$"

YoshisIsland_Cave_Text_MsgBlock:
	.string "MESSAGE BLOCK: This crystal cave\n"
	.string "belongs to the SHY GUY MINING UNION.\p"
	.string "MESSAGE BLOCK: Hard hats required.\n"
	.string "Masks required. Faces strictly\l"
	.string "optional, and frankly discouraged.$"

YoshisIsland_Cave_Text_EggBlock:
	.string "(Two EGG BLOCKS, a green one and a red\n"
	.string "one. They are not on speaking terms.)$"

YoshisIsland_Cave_Text_Bucket:
	.string "(A ? BUCKET. You look inside. It's empty.\n"
	.string "The ? was a lie.)$"

YoshisIsland_Cave_Text_Pow:
	.string "(A POW BLOCK. You think about it. You\n"
	.string "decide not to. The cave thanks you.)$"
