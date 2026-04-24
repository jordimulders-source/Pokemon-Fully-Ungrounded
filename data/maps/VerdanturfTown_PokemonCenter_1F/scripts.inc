VerdanturfTown_PokemonCenter_1F_MapScripts::
	map_script MAP_SCRIPT_ON_TRANSITION, VerdanturfTown_PokemonCenter_1F_OnTransition
	map_script MAP_SCRIPT_ON_RESUME, CableClub_OnResume
	.byte 0

VerdanturfTown_PokemonCenter_1F_OnTransition:
	setrespawn HEAL_LOCATION_VERDANTURF_TOWN
	call Common_EventScript_UpdateBrineyLocation
	end

VerdanturfTown_PokemonCenter_1F_EventScript_Nurse::
	setvar VAR_0x800B, LOCALID_VERDANTURF_NURSE
	call Common_EventScript_PkmnCenterNurse
	waitmessage
	waitbuttonpress
	release
	end

VerdanturfTown_PokemonCenter_1F_EventScript_Gentleman::
	msgbox VerdanturfTown_PokemonCenter_1F_Text_FaithInYourPokemon, MSGBOX_NPC
	end

VerdanturfTown_PokemonCenter_1F_EventScript_Protipmaster::
	lock
	faceplayer
	msgbox VerdanturfTown_PokemonCenter_1F_Text_ProtipMaster, MSGBOX_NPC
	release
	end

VerdanturfTown_PokemonCenter_1F_EventScript_ExpertM::
	msgbox VerdanturfTown_PokemonCenter_1F_Text_VisitForBattleTent, MSGBOX_NPC
	end

VerdanturfTown_PokemonCenter_1F_Text_FaithInYourPokemon:
	.string "You can't consider yourself a real\n"
	.string "TRAINER if you don't have faith\l"
	.string "in your POKéMON.\p"
	.string "Only those people who can believe\n"
	.string "in their battling POKéMON can win\l"
	.string "through to the very end.$"

VerdanturfTown_PokemonCenter_1F_Text_VisitForBattleTent:
	.string "The reason why anyone would visit\n"
	.string "VERDANTURF…\p"
	.string "It's the BATTLE TENT. It goes without\n"
	.string "saying.\p"
	.string "Or is there somebody here that you\n"
	.string "came to see?$"

VerdanturfTown_PokemonCenter_1F_Text_ProtipMaster:
	.string "Hello, I am the PROTIP ORACLE!\p"
	.string "I spread my knowledge around POKéMON\n"
	.string "CENTERS teaching the younger\l"
	.string "generation how to play.\p"
	.string "Did you know: Attacks have different\n"
	.string "types! Try attacking a FIRE-type\l"
	.string "POKéMON with a WATER-move.\p"
	.string "Something interesting will happen!$"
	