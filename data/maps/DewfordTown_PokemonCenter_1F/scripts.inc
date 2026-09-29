DewfordTown_PokemonCenter_1F_MapScripts::
	map_script MAP_SCRIPT_ON_TRANSITION, DewfordTown_PokemonCenter_1F_OnTransition
	map_script MAP_SCRIPT_ON_RESUME, CableClub_OnResume
	.byte 0

DewfordTown_PokemonCenter_1F_OnTransition:
	setrespawn HEAL_LOCATION_DEWFORD_TOWN
	call Common_EventScript_UpdateBrineyLocation
	end

DewfordTown_PokemonCenter_1F_EventScript_Protipmaster::
	lock
	faceplayer
	msgbox DewfordTown_PokemonCenter_1F_Text_ProtipMaster, MSGBOX_NPC
	release
	end

DewfordTown_PokemonCenter_1F_EventScript_Nurse::
	setvar VAR_0x800B, LOCALID_DEWFORD_NURSE
	call Common_EventScript_PkmnCenterNurse
	waitmessage
	waitbuttonpress
	release
	end

DewfordTown_PokemonCenter_1F_EventScript_PokefanF::
	msgbox DewfordTown_PokemonCenter_1F_Text_StoneCavern, MSGBOX_NPC
	end

DewfordTown_PokemonCenter_1F_EventScript_Man::
	msgbox DewfordTown_PokemonCenter_1F_Text_FaintedMonCanUseHM, MSGBOX_NPC
	end

DewfordTown_PokemonCenter_1F_Text_StoneCavern:
	.string "There's a stone cavern at the edge of\n"
	.string "town. Rare stones, dark corners, no\l"
	.string "neighbors.\p"
	.string "Last Friday I saw MADAME SILK go in\n"
	.string "with a boombox and a bag of feathers.\l"
	.string "Ten minutes later, RANDY followed with a\l"
	.string "fishing ROD.\p"
	.string "There are no fish in that cave.$"

DewfordTown_PokemonCenter_1F_Text_FaintedMonCanUseHM:
	.string "Even if a POKéMON faints, it can still\n"
	.string "use a move from a HIDDEN MACHINE.\p"
	.string "An unconscious PELIPPER carrying you\n"
	.string "across the ocean. A knocked-out\l"
	.string "LAPRAS as your ferry.\p"
	.string "Anywhere else they'd call that POKéMON\n"
	.string "abuse. But somehow it's still perfectly\l"
	.string "legal these days.$"

DewfordTown_PokemonCenter_1F_Text_ProtipMaster:
	.string "Hello, I am the PROTIP ORACLE!\p"
	.string "I spread my knowledge around POKéMON\n"
	.string "CENTERS teaching the younger\l"
	.string "generation how to play.\p"
	.string "Did you know: You can do damage by\n"
	.string "using attacks. If you do enough\l"
	.string "damage, you will win fights!$"
