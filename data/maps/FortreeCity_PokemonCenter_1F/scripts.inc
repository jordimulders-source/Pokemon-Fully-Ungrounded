FortreeCity_PokemonCenter_1F_MapScripts::
	map_script MAP_SCRIPT_ON_TRANSITION, FortreeCity_PokemonCenter_1F_OnTransition
	map_script MAP_SCRIPT_ON_RESUME, CableClub_OnResume
	.byte 0

FortreeCity_PokemonCenter_1F_OnTransition:
	setrespawn HEAL_LOCATION_FORTREE_CITY
	end

FortreeCity_PokemonCenter_1F_EventScript_Nurse::
	setvar VAR_0x800B, LOCALID_FORTREE_NURSE
	call Common_EventScript_PkmnCenterNurse
	waitmessage
	waitbuttonpress
	release
	end

@ Project Grounded: telt hoeveel Pokémon je gevangen hebt (National Dex) en lacht je uit onder de 20.
FortreeCity_PokemonCenter_1F_EventScript_Gentleman::
	lock
	faceplayer
	setvar VAR_0x8004, 1
	specialvar VAR_RESULT, ScriptGetPokedexInfo
	buffernumberstring STR_VAR_1, VAR_0x8006
	goto_if_lt VAR_0x8006, 20, FortreeCity_PokemonCenter_1F_EventScript_GentlemanLaugh
	msgbox FortreeCity_PokemonCenter_1F_Text_GoToSafariZone, MSGBOX_DEFAULT
	release
	end

FortreeCity_PokemonCenter_1F_EventScript_GentlemanLaugh::
	msgbox FortreeCity_PokemonCenter_1F_Text_PlayVanillaEmerald, MSGBOX_DEFAULT
	release
	end

FortreeCity_PokemonCenter_1F_EventScript_Man::
	msgbox FortreeCity_PokemonCenter_1F_Text_RecordCornerIsNeat, MSGBOX_NPC
	end

FortreeCity_PokemonCenter_1F_EventScript_Protipmaster::
	lock
	faceplayer
	msgbox FortreeCity_PokemonCenter_1F_Text_ProtipMaster, MSGBOX_NPC
	release
	end

FortreeCity_PokemonCenter_1F_EventScript_Boy::
	msgbox FortreeCity_PokemonCenter_1F_Text_DoYouKnowAboutPokenav, MSGBOX_NPC
	end

FortreeCity_PokemonCenter_1F_Text_GoToSafariZone:
	.string "Listen, kid. {STR_VAR_1} POKéMON caught?\n"
	.string "Not bad. Go to the SAFARI ZONE for more.$"

FortreeCity_PokemonCenter_1F_Text_RecordCornerIsNeat:
	.string "Have you seen the tournament results?\n"
	.string "INCINEROAR. INCINEROAR. INCINEROAR.\p"
	.string "Fake Out, Intimidate, Parting Shot,\n"
	.string "repeat. That cat has been in every top\l"
	.string "cut since before I had a job.$"

FortreeCity_PokemonCenter_1F_Text_DoYouKnowAboutPokenav:
	.string "Did you see that?!\p"
	.string "A talking KECLEON just walked in here\n"
	.string "and healed its POKéMON at the counter!\p"
	.string "It even said good morning to everyone\n"
	.string "inside.\p"
	.string "Very creepy.$"

FortreeCity_PokemonCenter_1F_Text_ProtipMaster:
	.string "Hello, I am the PROTIP ORACLE!\p"
	.string "I spread my knowledge around POKéMON\n"
	.string "CENTERS teaching the younger\l"
	.string "generation how to play.\p"
	.string "Did you know: When your POKéMON falls\n"
	.string "asleep, it will not do anything but\l"
	.string "sleep. What a lazy bastard!\p"
	.string "Wake 'em up! Before you Gogo!$"
	
FortreeCity_PokemonCenter_1F_Text_PlayVanillaEmerald:
	.string "Listen, kid. How many POKéMON have you\n"
	.string "caught? {STR_VAR_1}? HAHAHAHA!\p"
	.string "Why are you even playing a romhack like\n"
	.string "this if you don't catch POKéMON?\p"
	.string "Go play vanilla EMERALD!$"
