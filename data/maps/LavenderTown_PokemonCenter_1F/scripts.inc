@ Project Grounded: LavenderTown_PokemonCenter_1F (kopie van AshfrostTown_PokemonCenter_1F, tools/grounded/maptools/spacetime_cave.py)
LavenderTown_PokemonCenter_1F_MapScripts::
	map_script MAP_SCRIPT_ON_TRANSITION, LavenderTown_PokemonCenter_1F_OnTransition
	map_script MAP_SCRIPT_ON_RESUME, CableClub_OnResume
	.byte 0

LavenderTown_PokemonCenter_1F_OnTransition:
	setrespawn HEAL_LOCATION_LAVENDER_TOWN
	end

LavenderTown_PokemonCenter_1F_EventScript_Nurse::
	setvar VAR_0x800B, LOCALID_LAVENDER_NURSE
	call Common_EventScript_PkmnCenterNurse
	waitmessage
	waitbuttonpress
	release
	end

LavenderTown_PokemonCenter_1F_EventScript_ExpertM::
	msgbox LavenderTown_PokemonCenter_1F_EventScript_ExpertM_Text, MSGBOX_NPC
	end

LavenderTown_PokemonCenter_1F_EventScript_ExpertM_Text:
	.string "I come here to talk to the NURSE. She's\n"
	.string "the only one in town who answers when\l"
	.string "you speak to her.\p"
	.string "Well. The only one who's alive.$"

LavenderTown_PokemonCenter_1F_EventScript_Protipmaster::
	lock
	faceplayer
	msgbox LavenderTown_PokemonCenter_1F_Text_ProtipMaster, MSGBOX_NPC
	release
	end

LavenderTown_PokemonCenter_1F_Text_ProtipMaster:
	.string "Hello, I am the PROTIP ORACLE!\p"
	.string "I spread my knowledge around POKéMON\n"
	.string "CENTERS teaching the younger\l"
	.string "generation how to play.\p"
	.string "Did you know: ICE-type POKéMON don't\n"
	.string "take damage in a SNOW STORM.\p"
	.string "Neither do you, if you never go\n"
	.string "outside. That's why I live in\l"
	.string "POKéMON CENTERS now. All of them.$"
