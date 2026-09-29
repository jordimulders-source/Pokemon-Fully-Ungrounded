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
	.string "You're not a real TRAINER if you don't\n"
	.string "believe in your POKéMON.\p"
	.string "Only those who trust their POKéMON win\n"
	.string "in the end. And those who overlevel.$"

VerdanturfTown_PokemonCenter_1F_Text_VisitForBattleTent:
	.string "Summer 2016, the whole town was outside\n"
	.string "catching POKéMON.\p"
	.string "Now it's just me.\p"
	.string "And a guy with six phones on a bike.$"

VerdanturfTown_PokemonCenter_1F_Text_ProtipMaster:
	.string "Hello, I am the PROTIP ORACLE!\p"
	.string "I spread my knowledge around POKéMON\n"
	.string "CENTERS teaching the younger\l"
	.string "generation how to play.\p"
	.string "Did you know: Attacks have different\n"
	.string "types! Try attacking a FIRE-type\l"
	.string "POKéMON with a WATER-move.\p"
	.string "Something interesting will happen!$"
	
