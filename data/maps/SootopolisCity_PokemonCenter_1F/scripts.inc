SootopolisCity_PokemonCenter_1F_MapScripts::
	map_script MAP_SCRIPT_ON_TRANSITION, SootopolisCity_PokemonCenter_1F_OnTransition
	map_script MAP_SCRIPT_ON_RESUME, CableClub_OnResume
	.byte 0

SootopolisCity_PokemonCenter_1F_OnTransition:
	setrespawn HEAL_LOCATION_SOOTOPOLIS_CITY
	end

SootopolisCity_PokemonCenter_1F_EventScript_Nurse::
	setvar VAR_0x800B, LOCALID_SOOTOPOLIS_NURSE
	call Common_EventScript_PkmnCenterNurse
	waitmessage
	waitbuttonpress
	release
	end

SootopolisCity_PokemonCenter_1F_EventScript_Gentleman::
	lock
	faceplayer
	goto_if_ge VAR_SKY_PILLAR_STATE, 2, SootopolisCity_PokemonCenter_1F_EventScript_GentlemanNoLegendaries
	goto_if_unset FLAG_KYOGRE_ESCAPED_SEAFLOOR_CAVERN, SootopolisCity_PokemonCenter_1F_EventScript_GentlemanNoLegendaries
	msgbox SootopolisCity_PokemonCenter_1F_Text_EveryoneTakenRefuge, MSGBOX_DEFAULT
	release
	end

SootopolisCity_PokemonCenter_1F_EventScript_Protipmaster::
	lock
	faceplayer
	msgbox SootopolisCity_PokemonCenter_1F_Text_ProtipMaster, MSGBOX_NPC
	release
	end

SootopolisCity_PokemonCenter_1F_EventScript_GentlemanNoLegendaries::
	msgbox SootopolisCity_PokemonCenter_1F_Text_WallaceToughestInHoenn, MSGBOX_DEFAULT
	release
	end

SootopolisCity_PokemonCenter_1F_EventScript_Woman::
	lock
	faceplayer
	goto_if_ge VAR_SKY_PILLAR_STATE, 2, SootopolisCity_PokemonCenter_1F_EventScript_WomanNoLegendaries
	goto_if_unset FLAG_KYOGRE_ESCAPED_SEAFLOOR_CAVERN, SootopolisCity_PokemonCenter_1F_EventScript_WomanNoLegendaries
	msgbox SootopolisCity_PokemonCenter_1F_Text_ArentPokemonOurFriends, MSGBOX_DEFAULT
	release
	end

SootopolisCity_PokemonCenter_1F_EventScript_WomanNoLegendaries::
	msgbox SootopolisCity_PokemonCenter_1F_Text_AlwaysBeFriendsWithPokemon, MSGBOX_DEFAULT
	release
	end

SootopolisCity_PokemonCenter_1F_Text_WallaceToughestInHoenn:
	.string "Our GYM LEADER WALLACE is one of the\n"
	.string "toughest TRAINERS in HOENN.\p"
	.string "Some say it's the wine. Others say it's\n"
	.string "talent.\p"
	.string "But the ELITE FOUR are said to be even\n"
	.string "stronger.\p"
	.string "And the CHAMPION? Nobody knows. He's\n"
	.string "always in a cave somewhere.$"

SootopolisCity_PokemonCenter_1F_Text_EveryoneTakenRefuge:
	.string "Everyone is hiding in their homes.\p"
	.string "I'm hiding in the POKéMON CENTER.\p"
	.string "Free healing. Free chairs. Good choice.$"

SootopolisCity_PokemonCenter_1F_Text_AlwaysBeFriendsWithPokemon:
	.string "Whenever, wherever, whatever happens,\n"
	.string "I'll always be friends with POKéMON.\p"
	.string "Humans are the problem.$"

SootopolisCity_PokemonCenter_1F_Text_ArentPokemonOurFriends:
	.string "Aren't POKéMON our friends?\p"
	.string "Why are they going wild?\p"
	.string "Maybe we deserve it.$"

SootopolisCity_PokemonCenter_1F_Text_ProtipMaster:
	.string "Hello, I am the PROTIP ORACLE!\p"
	.string "I spread my knowledge around POKéMON\n"
	.string "CENTERS teaching the younger\l"
	.string "generation how to play.\p"
	.string "Did you know: You can use items in\n"
	.string "battle. Like POTIONS!\p"
	.string "They heal your POKéMON. I recommend\n"
	.string "using X-ITEMS, like X ACCURACY.\p"
	.string "It makes your FURY SWIPES easier\n"
	.string "to hit!$"
	
