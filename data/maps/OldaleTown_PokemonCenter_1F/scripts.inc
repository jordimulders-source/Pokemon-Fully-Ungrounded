OldaleTown_PokemonCenter_1F_MapScripts::
	map_script MAP_SCRIPT_ON_TRANSITION, OldaleTown_PokemonCenter_1F_OnTransition
	map_script MAP_SCRIPT_ON_RESUME, CableClub_OnResume
	.byte 0

OldaleTown_PokemonCenter_1F_OnTransition:
	setrespawn HEAL_LOCATION_OLDALE_TOWN
	call Common_EventScript_UpdateBrineyLocation
	end

OldaleTown_PokemonCenter_1F_EventScript_Nurse::
	setvar VAR_0x800B, 1
	call Common_EventScript_PkmnCenterNurse
	waitmessage
	waitbuttonpress
	release
	end

OldaleTown_PokemonCenter_1F_EventScript_Gentleman::
	msgbox OldaleTown_PokemonCenter_1F_Text_TrainersCanUsePC, MSGBOX_NPC
	end

OldaleTown_PokemonCenter_1F_EventScript_Boy::
	msgbox OldaleTown_PokemonCenter_1F_Text_PokemonCentersAreGreat, MSGBOX_NPC
	end

OldaleTown_PokemonCenter_1F_EventScript_Girl::
	lock
	faceplayer
	goto_if_set FLAG_SYS_POKEDEX_GET, OldaleTown_PokemonCenter_1F_EventScript_WirelessClubAvailable
	msgbox OldaleTown_PokemonCenter_1F_Text_WirelessClubNotAvailable, MSGBOX_DEFAULT
	release
	end

OldaleTown_PokemonCenter_1F_EventScript_WirelessClubAvailable::
	msgbox OldaleTown_PokemonCenter_1F_Text_TradedInWirelessClub, MSGBOX_DEFAULT
	release
	end

OldaleTown_PokemonCenter_1F_EventScript_Protipmaster::
	lock
	faceplayer
	msgbox OldaleTown_PokemonCenter_1F_Text_ProtipMaster, MSGBOX_NPC
	release
	end

OldaleTown_PokemonCenter_1F_EventScript_GameboyLG::
	lock
	faceplayer
	msgbox OldaleTown_PokemonCenter_1F_Text_GameboyLG, MSGBOX_NPC
	release
	end

OldaleTown_PokemonCenter_1F_EventScript_GameboyFR::
	lock
	faceplayer
	msgbox OldaleTown_PokemonCenter_1F_Text_GameboyFR, MSGBOX_NPC
	release
	end

OldaleTown_PokemonCenter_1F_Text_TrainersCanUsePC:
	.string "That PC in the corner there uses\n"
	.string "Windows 98. So it takes a solid\l"
	.string "minute to stuff your POKéMON there.\p"
	.string "But at least it's good nostalgia bait!$"

OldaleTown_PokemonCenter_1F_Text_PokemonCentersAreGreat:
	.string "POKéMON CENTERS are strange!\p"
	.string "There's always a whole bunch of\n"
	.string "freeloaders inside, are they homeless?\p"
	.string "What do they do in life? What do I do\n"
	.string "in life? Never talk to strangers.$"

OldaleTown_PokemonCenter_1F_Text_WirelessClubNotAvailable:
	.string "The POKéMON WIRELESS CLUB on\n"
	.string "the second floor is fucking useless.\p"
	.string "Because it is 2026 and we do not use\n"
	.string "this outdated technology anymore.$"

OldaleTown_PokemonCenter_1F_Text_TradedInWirelessClub:
	.string "The POKéMON WIRELESS CLUB on\n"
	.string "the second floor is fucking useless.\p"
	.string "Just do something else with your life.$"

OldaleTown_PokemonCenter_1F_Text_ProtipMaster:
	.string "Hello, I am the PROTIP ORACLE!\p"
	.string "I spread my knowledge around POKéMON\n"
	.string "CENTERS teaching the younger\l"
	.string "generation how to play.\p"
	.string "Did you know: You can run from wild\n"
	.string "POKéMON battles by pressing 'RUN'.\p"
	.string "No need to use WHIRLWIND anymore!$"

OldaleTown_PokemonCenter_1F_Text_GameboyLG:
	.string "Check my new SWITCH 2!\n"
	.string "I'm playing POKéMON LEAFGREEN.\p"
	.string "20 euros for a rom dump that I have\n"
	.string "played many times before.\p"
	.string "What a deal! I especially love the\n"
	.string "lush expansive SEVII ISLANDS.$"

OldaleTown_PokemonCenter_1F_Text_GameboyFR:
	.string "Yo! I bought FIRERED for 20 euros\n"
	.string "for my SWITCH 2.\p"
	.string "I mean I could've bought indie games,\n"
	.string "but who cares.\p"
	.string "I just want to solo everything with\n"
	.string "CHARIZARD. You can't do that in\l"
	.string "HOLLOW KNIGHT or SLAY THE SPIRE.$"

