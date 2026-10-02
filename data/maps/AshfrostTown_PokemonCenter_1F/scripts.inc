AshfrostTown_PokemonCenter_1F_MapScripts::
	map_script MAP_SCRIPT_ON_TRANSITION, AshfrostTown_PokemonCenter_1F_OnTransition
	map_script MAP_SCRIPT_ON_RESUME, CableClub_OnResume
	.byte 0

AshfrostTown_PokemonCenter_1F_OnTransition:
	setrespawn HEAL_LOCATION_ASHFROST_TOWN
	end

AshfrostTown_PokemonCenter_1F_EventScript_Nurse::
	setvar VAR_0x800B, LOCALID_ASHFROST_NURSE
	call Common_EventScript_PkmnCenterNurse
	waitmessage
	waitbuttonpress
	release
	end

AshfrostTown_PokemonCenter_1F_EventScript_ExpertM::
	msgbox AshfrostTown_PokemonCenter_1F_EventScript_ExpertM_Text, MSGBOX_NPC
	end

AshfrostTown_PokemonCenter_1F_EventScript_ExpertM_Text:
	.string "(Placeholder: visitor in the\nPOKéMON CENTER.)$"

AshfrostTown_PokemonCenter_1F_EventScript_Protipmaster::
	lock
	faceplayer
	msgbox AshfrostTown_PokemonCenter_1F_Text_ProtipMaster, MSGBOX_NPC
	release
	end

AshfrostTown_PokemonCenter_1F_Text_ProtipMaster:
	.string "Hello, I am the PROTIP ORACLE!\p"
	.string "I spread my knowledge around POKéMON\n"
	.string "CENTERS teaching the younger\l"
	.string "generation how to play.\p"
	.string "Did you know: ICE-type POKéMON don't\n"
	.string "take damage in a SNOW STORM.\p"
	.string "Neither do you, if you never go\n"
	.string "outside. That's why I live in\l"
	.string "POKéMON CENTERS now. All of them.$"
