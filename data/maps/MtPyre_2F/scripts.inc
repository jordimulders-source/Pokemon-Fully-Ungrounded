MtPyre_2F_MapScripts::
	map_script MAP_SCRIPT_ON_FRAME_TABLE, CaveHole_CheckFallDownHole
	map_script MAP_SCRIPT_ON_TRANSITION, CaveHole_FixCrackedGround
	map_script MAP_SCRIPT_ON_RESUME, MtPyre_2F_SetHoleWarp
	.byte 0

MtPyre_2F_SetHoleWarp:
	setstepcallback STEP_CB_CRACKED_FLOOR
	setholewarp MAP_MT_PYRE_1F
	end

MtPyre_2F_EventScript_Woman::
	msgbox MtPyre_2F_Text_MemoriesOfSkitty, MSGBOX_NPC
	end

MtPyre_2F_EventScript_PokefanM::
	msgbox MtPyre_2F_Text_TumbledFromFloorAbove, MSGBOX_NPC
	end

MtPyre_2F_EventScript_Mark::
	trainerbattle_single TRAINER_MARK, MtPyre_2F_Text_MarkIntro, MtPyre_2F_Text_MarkDefeat
	msgbox MtPyre_2F_Text_MarkPostBattle, MSGBOX_AUTOCLOSE
	end

MtPyre_2F_EventScript_Luke::
	trainerbattle_double TRAINER_DEZ_AND_LUKE, MtPyre_2F_Text_LukeIntro, MtPyre_2F_Text_LukeDefeat, MtPyre_2F_Text_LukeNotEnoughMons
	msgbox MtPyre_2F_Text_LukePostBattle, MSGBOX_AUTOCLOSE
	end

MtPyre_2F_EventScript_Dez::
	trainerbattle_double TRAINER_DEZ_AND_LUKE, MtPyre_2F_Text_DezIntro, MtPyre_2F_Text_DezDefeat, MtPyre_2F_Text_DezNotEnoughMons
	msgbox MtPyre_2F_Text_DezPostBattle, MSGBOX_AUTOCLOSE
	end

MtPyre_2F_EventScript_Leah::
	trainerbattle_single TRAINER_LEAH, MtPyre_2F_Text_LeahIntro, MtPyre_2F_Text_LeahDefeat
	msgbox MtPyre_2F_Text_LeahPostBattle, MSGBOX_AUTOCLOSE
	end

MtPyre_2F_EventScript_Zander::
	trainerbattle_single TRAINER_ZANDER, MtPyre_2F_Text_ZanderIntro, MtPyre_2F_Text_ZanderDefeat
	msgbox MtPyre_2F_Text_ZanderPostBattle, MSGBOX_AUTOCLOSE
	end

MtPyre_2F_Text_MemoriesOfSkitty:
	.string "Memories of my darling SKITTY…\p"
	.string "My eyes overflow…\p"
	.string "She ran away. She's not dead. She just\n"
	.string "hated me.$"

MtPyre_2F_Text_TumbledFromFloorAbove:
	.string "Ouch… There are holes in the floor.\p"
	.string "I fell from the floor above.\p"
	.string "Three times. Same hole.$"

MtPyre_2F_Text_MarkIntro:
	.string "Hey! Are you looking for POKéMON? You\n"
	.string "came after me!\p"
	.string "This graveyard is MY hunting ground!\n"
	.string "Rude!$"

MtPyre_2F_Text_MarkDefeat:
	.string "Ayieeeeh! Sorry! Forgive me!$"

MtPyre_2F_Text_MarkPostBattle:
	.string "Nobody comes here, so I thought there'd\n"
	.string "be rare POKéMON.\p"
	.string "There are. They're dead.$"

MtPyre_2F_Text_LukeIntro:
	.string "LUKE: We're here on a dare.\p"
	.string "If I show her how cool I am, she'll fall\n"
	.string "for me!\p"
	.string "I'll cream you!$"

MtPyre_2F_Text_LukeDefeat:
	.string "LUKE: Whoopsie! …She's not falling for\n"
	.string "me, is she?$"

MtPyre_2F_Text_LukePostBattle:
	.string "LUKE: We lost, but I'm right here by your\n"
	.string "side, babe!\p"
	.string "…Babe? Where did she go?$"

MtPyre_2F_Text_LukeNotEnoughMons:
	.string "LUKE: Bring more POKéMON!\p"
	.string "I need to look cool for my girl!$"

MtPyre_2F_Text_DezIntro:
	.string "DEZ: I'm here on a dare with my\n"
	.string "boyfriend.\p"
	.string "It's scary, but I'll make him look cool by\n"
	.string "beating you!$"

MtPyre_2F_Text_DezDefeat:
	.string "DEZ: Waaaah! I'm scared! Take me home,\n"
	.string "LUKE!$"

MtPyre_2F_Text_DezPostBattle:
	.string "DEZ: We're lovey-dovey, so losing\n"
	.string "doesn't matter!\p"
	.string "…He screamed louder than me, though.$"

MtPyre_2F_Text_DezNotEnoughMons:
	.string "DEZ: Bring at least two POKéMON.\p"
	.string "My boyfriend's strong. Emotionally, not\n"
	.string "really.$"

MtPyre_2F_Text_LeahIntro:
	.string "Be gone…\p"
	.string "Intruders…$"

MtPyre_2F_Text_LeahDefeat:
	.string "…Sorry. Old habit.\p"
	.string "I used to work in LAVENDER TOWN.$"

MtPyre_2F_Text_LeahPostBattle:
	.string "Give… me… your…\p"
	.string "…Actually, never mind.$"

MtPyre_2F_Text_ZanderIntro:
	.string "KIYAAAAAH! I'm terrified!$"

MtPyre_2F_Text_ZanderDefeat:
	.string "NOOOOO! I lost my wits!$"

MtPyre_2F_Text_ZanderPostBattle:
	.string "Everything that moves freaks me out…\p"
	.string "I came here to train my courage.\p"
	.string "Wrong place. Very wrong place.$"

