MossdeepCity_PokemonCenter_1F_MapScripts::
	map_script MAP_SCRIPT_ON_TRANSITION, MossdeepCity_PokemonCenter_1F_OnTransition
	map_script MAP_SCRIPT_ON_RESUME, CableClub_OnResume
	.byte 0

MossdeepCity_PokemonCenter_1F_OnTransition:
	setrespawn HEAL_LOCATION_MOSSDEEP_CITY
	end

MossdeepCity_PokemonCenter_1F_EventScript_Nurse::
	setvar VAR_0x800B, LOCALID_MOSSDEEP_NURSE
	call Common_EventScript_PkmnCenterNurse
	waitmessage
	waitbuttonpress
	release
	end

MossdeepCity_PokemonCenter_1F_EventScript_Protipmaster::
	lock
	faceplayer
	msgbox MossdeepCity_PokemonCenter_1F_Text_ProtipMaster, MSGBOX_NPC
	release
	end

MossdeepCity_PokemonCenter_1F_EventScript_Woman::
	msgbox MossdeepCity_PokemonCenter_1F_Text_GymLeaderDuoFormidable, MSGBOX_NPC
	end

MossdeepCity_PokemonCenter_1F_EventScript_Girl::
	msgbox MossdeepCity_PokemonCenter_1F_Text_AbilitiesMightChangeMoves, MSGBOX_NPC
	end

MossdeepCity_PokemonCenter_1F_Text_GymLeaderDuoFormidable:
	.string "Did you see a girl in a white hat?\p"
	.string "She keeps yelling at her bag.\p"
	.string "“Get back in the bag, NEBBY!”$"

MossdeepCity_PokemonCenter_1F_Text_AbilitiesMightChangeMoves:
	.string "The POKéSTOP here gave me three POKé\n"
	.string "BALLS and a sprained ankle.\p"
	.string "I walked into the sea.$"

MossdeepCity_PokemonCenter_1F_Text_ProtipMaster:
	.string "Hello, I am the PROTIP ORACLE!\p"
	.string "I spread my knowledge around POKéMON\n"
	.string "CENTERS teaching the younger\l"
	.string "generation how to play.\p"
	.string "Did you know: Like this loser girl over\n"
	.string "here has been saying, ABILITIES might\l"
	.string "change battles.\p"
	.string "My favorite ABILITY is “RUN AWAY”.\n"
	.string "You can run from wild POKéMON, but\l"
	.string "not from TRAINERS.\p"
	.string "I use it in all my VGC teams!$"
	