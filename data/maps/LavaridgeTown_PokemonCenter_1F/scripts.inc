LavaridgeTown_PokemonCenter_1F_MapScripts::
	map_script MAP_SCRIPT_ON_TRANSITION, LavaridgeTown_PokemonCenter_1F_OnTransition
	map_script MAP_SCRIPT_ON_RESUME, CableClub_OnResume
	.byte 0

LavaridgeTown_PokemonCenter_1F_OnTransition:
	setrespawn HEAL_LOCATION_LAVARIDGE_TOWN
	call Common_EventScript_UpdateBrineyLocation
	end

LavaridgeTown_PokemonCenter_1F_EventScript_Nurse::
	setvar VAR_0x800B, LOCALID_LAVARIDGE_NURSE
	call Common_EventScript_PkmnCenterNurse
	waitmessage
	waitbuttonpress
	release
	end

LavaridgeTown_PokemonCenter_1F_EventScript_Protipmaster::
	lock
	faceplayer
	msgbox LavaridgeTown_PokemonCenter_1F_Text_ProtipMaster, MSGBOX_NPC
	release
	end

LavaridgeTown_PokemonCenter_1F_EventScript_Youngster::
	msgbox LavaridgeTown_PokemonCenter_1F_Text_HotSpringCanInvigorate, MSGBOX_NPC
	end

LavaridgeTown_PokemonCenter_1F_EventScript_Woman::
	msgbox LavaridgeTown_PokemonCenter_1F_Text_TrainersPokemonSpendTimeTogether, MSGBOX_NPC
	end

LavaridgeTown_PokemonCenter_1F_EventScript_Gentleman::
	msgbox LavaridgeTown_PokemonCenter_1F_Text_TrainersShouldRestToo, MSGBOX_NPC
	end

LavaridgeTown_PokemonCenter_1F_Text_TrainersPokemonSpendTimeTogether:
	.string "I think POKéMON get closer to their\n"
	.string "TRAINERS if they spend time together.\p"
	.string "The longer the better.\n"
	.string "That's what I think.$"

LavaridgeTown_PokemonCenter_1F_Text_HotSpringCanInvigorate:
	.string "POKéMON UNITE. A MOBA.\p"
	.string "POKéMON CAFé. Serving lattes.\p"
	.string "Who asked for this?!\p"
	.string "I just want to throw balls at animals.\n"
	.string "Like a normal person.$"

LavaridgeTown_PokemonCenter_1F_Text_TrainersShouldRestToo:
	.string "Hohoho… You hear that jingle?\n"
	.string "Ding-ding-dididing. Three seconds and\l"
	.string "your POKéMON are good as new.\p"
	.string "And then you send them right back out.\n"
	.string "Burned, poisoned, frozen, thrown into\l"
	.string "walls.\p"
	.string "Heal, fight, faint. Heal, fight, faint.\p"
	.string "What a life…$"

LavaridgeTown_PokemonCenter_1F_Text_ProtipMaster:
	.string "Hello, I am the PROTIP ORACLE!\p"
	.string "I spread my knowledge around POKéMON\n"
	.string "CENTERS teaching the younger\l"
	.string "generation how to play.\p"
	.string "Did you know: You get money when\n"
	.string "you win fights. Get Rich or Die\l"
	.string "Trying, like my homeboy 50 used to say!$"
	