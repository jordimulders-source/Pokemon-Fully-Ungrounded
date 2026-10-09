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
	.string "I used to sell SILPH SCOPES. Lovely\n"
	.string "things. You look through one and the\l"
	.string "ghosts stop pretending.\p"
	.string "Then the fog came and the ghosts\n"
	.string "stopped pretending all on their own.\l"
	.string "Terrible for business.$"
