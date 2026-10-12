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
	goto_if_set FLAG_RECEIVED_SILPH_SCOPE, LavenderTown_PokemonCenter_1F_EventScript_ScopeAfter
	msgbox LavenderTown_PokemonCenter_1F_Text_ProtipMaster, MSGBOX_DEFAULT
	giveitem ITEM_SILPH_SCOPE
	setflag FLAG_RECEIVED_SILPH_SCOPE
	msgbox LavenderTown_PokemonCenter_1F_Text_ScopeGiven, MSGBOX_DEFAULT
	release
	end

LavenderTown_PokemonCenter_1F_EventScript_ScopeAfter::
	msgbox LavenderTown_PokemonCenter_1F_Text_ScopeAfter, MSGBOX_DEFAULT
	release
	end

LavenderTown_PokemonCenter_1F_Text_ProtipMaster:
	.string "I used to sell SILPH SCOPES. Lovely\n"
	.string "things. You look through one and the\l"
	.string "ghosts stop pretending.\p"
	.string "Then the fog came and nobody bought\n"
	.string "anything ever again. Here. Last one.\l"
	.string "Take it before it starts haunting me\l"
	.string "too.$"

LavenderTown_PokemonCenter_1F_Text_ScopeGiven:
	.string "Look at a GHOST through it and you'll\n"
	.string "see what it really is.\p"
	.string "Usually something with too many teeth.\n"
	.string "No refunds. There's no shop left to\l"
	.string "refund it at.$"


LavenderTown_PokemonCenter_1F_Text_ScopeAfter:
	.string "How's the SCOPE? Seen anything you\n"
	.string "can't unsee?\p"
	.string "Good. That means it works.$"
