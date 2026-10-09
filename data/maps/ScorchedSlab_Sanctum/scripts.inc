@ Project Grounded: Scorched Slab, Zonnesanctum achter de zonnedeur. Hogepriesteres Helia, Volcarona lv 42
@ in de grote lichtvlek, Heat Rock en TM59 Weather Ball.
ScorchedSlab_Sanctum_MapScripts::
	.byte 0

ScorchedSlab_Sanctum_EventScript_Volcarona::
	lock
	faceplayer
	msgbox ScorchedSlab_Sanctum_Text_Volcarona, MSGBOX_DEFAULT
	playmoncry SPECIES_VOLCARONA, CRY_MODE_ENCOUNTER
	waitmoncry
	setwildbattle SPECIES_VOLCARONA, 54
	setflag FLAG_SYS_CTRL_OBJ_DELETE
	dowildbattle
	clearflag FLAG_SYS_CTRL_OBJ_DELETE
	specialvar VAR_RESULT, GetBattleOutcome
	goto_if_eq VAR_RESULT, B_OUTCOME_RAN, ScorchedSlab_Sanctum_EventScript_VolcaronaStays
	goto_if_eq VAR_RESULT, B_OUTCOME_PLAYER_TELEPORTED, ScorchedSlab_Sanctum_EventScript_VolcaronaStays
	removeobject LOCALID_SCORCHED_SLAB_VOLCARONA
	setflag FLAG_HIDE_SCORCHED_SLAB_VOLCARONA
ScorchedSlab_Sanctum_EventScript_VolcaronaStays::
	release
	end

ScorchedSlab_Sanctum_EventScript_Helia::
	trainerbattle_single TRAINER_SLAB_HELIA, ScorchedSlab_Sanctum_Text_HeliaIntro, ScorchedSlab_Sanctum_Text_HeliaDefeat
	msgbox ScorchedSlab_Sanctum_Text_HeliaPostBattle, MSGBOX_AUTOCLOSE
	end

ScorchedSlab_Sanctum_EventScript_Mural::
	msgbox ScorchedSlab_Sanctum_Text_Mural, MSGBOX_SIGN
	end

ScorchedSlab_Sanctum_Text_Volcarona:
	.string "A VOLCARONA basks in the light from\n"
	.string "the ceiling. It is very warm.\p"
	.string "The cult thinks it is the sun.\n"
	.string "It has never corrected them.\p"
	.string "It flares its wings. Somebody's\n"
	.string "about to get a tan.$"

ScorchedSlab_Sanctum_Text_HeliaIntro:
	.string "You opened the sun door?\n"
	.string "With STRENGTH? And ROCKS?\p"
	.string "We tried prayer for 400 years.\n"
	.string "Nobody told us about rocks.\p"
	.string "The sun forgives. I don't.$"

ScorchedSlab_Sanctum_Text_HeliaDefeat:
	.string "Eclipsed. By a child with a\n"
	.string "backpack.$"

ScorchedSlab_Sanctum_Text_HeliaPostBattle:
	.string "Go on, meet our god. Bring burn\n"
	.string "heals. Bring several.\p"
	.string "Last pilgrim brought a WATER-type.\n"
	.string "We still use him as a humidifier.$"

ScorchedSlab_Sanctum_Text_Mural:
	.string "A mural of a giant moth wearing\n"
	.string "the sun as a hat.\p"
	.string "Tiny worshippers bow beneath it.\n"
	.string "One of them is clearly asleep.$"
