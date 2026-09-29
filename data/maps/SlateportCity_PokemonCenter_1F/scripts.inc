SlateportCity_PokemonCenter_1F_MapScripts::
	map_script MAP_SCRIPT_ON_TRANSITION, SlateportCity_PokemonCenter_1F_OnTransition
	map_script MAP_SCRIPT_ON_RESUME, CableClub_OnResume
	.byte 0

SlateportCity_PokemonCenter_1F_OnTransition:
	setrespawn HEAL_LOCATION_SLATEPORT_CITY
	call Common_EventScript_UpdateBrineyLocation
	end

SlateportCity_PokemonCenter_1F_EventScript_Protipmaster::
	lock
	faceplayer
	msgbox SlateportCity_PokemonCenter_1F_Text_ProtipMaster, MSGBOX_NPC
	release
	end

SlateportCity_PokemonCenter_1F_EventScript_Nurse::
	setvar VAR_0x800B, LOCALID_SLATEPORT_NURSE
	call Common_EventScript_PkmnCenterNurse
	waitmessage
	waitbuttonpress
	release
	end

SlateportCity_PokemonCenter_1F_EventScript_Sailor::
	msgbox SlateportCity_PokemonCenter_1F_Text_RaiseDifferentTypesOfPokemon, MSGBOX_NPC
	end

SlateportCity_PokemonCenter_1F_EventScript_Woman::
	msgbox SlateportCity_PokemonCenter_1F_Text_TradedMonWithFriend, MSGBOX_NPC
	end

SlateportCity_PokemonCenter_1F_Text_RaiseDifferentTypesOfPokemon:
	.string "I pay ¥999 a month for a POKéMON\n"
	.string "subscription.\p"
	.string "Six POKéMON at a time. New ones every\n"
	.string "month.\p"
	.string "Are they mine? No.\p"
	.string "Do I care? Also no.$"

SlateportCity_PokemonCenter_1F_Text_TradedMonWithFriend:
	.string "Since POKOPIA, I don't battle anymore.\p"
	.string "I just want to be friends with my\n"
	.string "POKéMON and build a little house\l"
	.string "together. Please don't make me battle.$"

SlateportCity_PokemonCenter_1F_Text_ProtipMaster:
	.string "Hello, I am the PROTIP ORACLE!\p"
	.string "I spread my knowledge around POKéMON\n"
	.string "CENTERS teaching the younger\l"
	.string "generation how to play.\p"
	.string "Did you know: POKéMON can learn new\n"
	.string "moves! Either by levelling up,\l"
	.string "evolving, relearning moves or\l"
	.string "learning TMs.\p"
	.string "No need to keep using TACKLE until\n"
	.string "the end game. What a relief!$"
	