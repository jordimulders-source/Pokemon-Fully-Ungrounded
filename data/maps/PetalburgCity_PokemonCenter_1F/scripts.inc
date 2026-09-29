PetalburgCity_PokemonCenter_1F_MapScripts::
	map_script MAP_SCRIPT_ON_TRANSITION, PetalburgCity_PokemonCenter_1F_OnTransition
	map_script MAP_SCRIPT_ON_RESUME, CableClub_OnResume
	.byte 0

PetalburgCity_PokemonCenter_1F_OnTransition:
	setrespawn HEAL_LOCATION_PETALBURG_CITY
	call Common_EventScript_UpdateBrineyLocation
	end

PetalburgCity_PokemonCenter_1F_EventScript_Nurse::
	setvar VAR_0x800B, LOCALID_PETALBURG_NURSE
	call Common_EventScript_PkmnCenterNurse
	waitmessage
	waitbuttonpress
	release
	end

PetalburgCity_PokemonCenter_1F_EventScript_FatMan::
	msgbox PetalburgCity_PokemonCenter_1F_Text_PCStorageSystem, MSGBOX_NPC
	end

PetalburgCity_PokemonCenter_1F_EventScript_Youngster::
	msgbox PetalburgCity_PokemonCenter_1F_Text_OranBerryRegainedHP, MSGBOX_NPC
	end

PetalburgCity_PokemonCenter_1F_EventScript_Woman::
	lock
	faceplayer
	msgbox PetalburgCity_PokemonCenter_1F_Text_ManyTypesOfPokemon, MSGBOX_DEFAULT
	specialvar VAR_RESULT, IsStarterInParty
	goto_if_eq VAR_RESULT, TRUE, PetalburgCity_PokemonCenter_1F_EventScript_SayStarterTypeInfo
	release
	end

PetalburgCity_PokemonCenter_1F_EventScript_SayStarterTypeInfo::
	call_if_eq VAR_STARTER_MON, 0, PetalburgCity_PokemonCenter_1F_EventScript_SayTreeckoType
	call_if_eq VAR_STARTER_MON, 1, PetalburgCity_PokemonCenter_1F_EventScript_SayTorchicType
	call_if_eq VAR_STARTER_MON, 2, PetalburgCity_PokemonCenter_1F_EventScript_SayMudkipType
	release
	end

PetalburgCity_PokemonCenter_1F_EventScript_Protipmaster::
	lock
	faceplayer
	msgbox PetalburgCity_PokemonCenter_1F_Text_ProtipMaster, MSGBOX_NPC
	release
	end

PetalburgCity_PokemonCenter_1F_EventScript_SayTreeckoType::
	msgbox PetalburgCity_PokemonCenter_1F_Text_TreeckoIsGrassType, MSGBOX_DEFAULT
	return

PetalburgCity_PokemonCenter_1F_EventScript_SayTorchicType::
	msgbox PetalburgCity_PokemonCenter_1F_Text_TorchicIsFireType, MSGBOX_DEFAULT
	return

PetalburgCity_PokemonCenter_1F_EventScript_SayMudkipType::
	msgbox PetalburgCity_PokemonCenter_1F_Text_MudkipIsWaterType, MSGBOX_DEFAULT
	return

PetalburgCity_PokemonCenter_1F_Text_PCStorageSystem:
	.string "The PC Storage System got hacked.\p"
	.string "My POKéMON, my moves, my EVs. All leaked.\p"
	.string "Now every kid on the route counters my\n"
	.string "team.\p"
	.string "I haven't won in six weeks.$"

PetalburgCity_PokemonCenter_1F_Text_OranBerryRegainedHP:
	.string "I walked 10 km to hatch an EGG.\p"
	.string "It was a MAGIKARP.\p"
	.string "Again.$"

PetalburgCity_PokemonCenter_1F_Text_ManyTypesOfPokemon:
	.string "GRASS beats WATER, WATER beats FIRE,\n"
	.string "FIRE beats GRASS.\p"
	.string "So where are the monkeys?!\p"
	.string "PANSAGE, PANSEAR, PANPOUR!\p"
	.string "The whole triangle, in monkey form!\p"
	.string "Somebody left them out on purpose. I\n"
	.string "KNOW it.$"

PetalburgCity_PokemonCenter_1F_Text_TreeckoIsGrassType:
	.string "Your TREECKO is a GRASS type.\p"
	.string "Strong against WATER and GROUND.\p"
	.string "Weak against FIRE. And bugs. And birds.\n"
	.string "And poison. And ice. Poor thing.$"

PetalburgCity_PokemonCenter_1F_Text_TorchicIsFireType:
	.string "Your TORCHIC is a FIRE type.\p"
	.string "Strong against GRASS and BUG.\p"
	.string "Weak against WATER. And it's a chicken.\n"
	.string "Just saying.$"

PetalburgCity_PokemonCenter_1F_Text_MudkipIsWaterType:
	.string "Your MUDKIP is a WATER type.\p"
	.string "Strong against FIRE.\p"
	.string "It evolves into GROUND too. Then only\n"
	.string "GRASS hurts it. Smart pick.$"

PetalburgCity_PokemonCenter_1F_Text_ProtipMaster:
	.string "Hello, I am the PROTIP ORACLE!\p"
	.string "I spread my knowledge around POKéMON\n"
	.string "CENTERS teaching the younger\l"
	.string "generation how to play.\p"
	.string "Did you know: You can talk to NPCs,\n"
	.string "by pressing “A”, when you are\l"
	.string "facing them.\p"
	.string "People might give you very useful\n"
	.string "tips. You should try it on me!$"
	