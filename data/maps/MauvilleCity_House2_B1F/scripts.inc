MauvilleCity_House2_B1F_MapScripts::
	map_script MAP_SCRIPT_ON_LOAD, MauvilleCity_House2_B1F_OnLoad
	.byte 0

MauvilleCity_House2_B1F_OnLoad:
	setmetatile 8, 2, METATILE_Building_TV_On, TRUE
	end

MauvilleCity_House2_B1F_EventScript_TV::
	lockall
	goto_if_set FLAG_CAUGHT_MAUVILLE_ROTOM, MauvilleCity_House2_B1F_EventScript_BoringNews
	goto_if_unset FLAG_BADGE03_GET, MauvilleCity_House2_B1F_EventScript_Static
	msgbox MauvilleCity_House2_B1F_Text_TrashTV, MSGBOX_DEFAULT
	closemessage
	setvar VAR_0x8004, 1
	setvar VAR_0x8005, 1
	setvar VAR_0x8006, 8
	setvar VAR_0x8007, 3
	special ShakeCamera
	playmoncry SPECIES_ROTOM, CRY_MODE_ENCOUNTER
	waitstate
	msgbox MauvilleCity_House2_B1F_Text_RotomBurstsOut, MSGBOX_DEFAULT
	waitmoncry
	closemessage
	setwildbattle SPECIES_ROTOM, 40
	dowildbattle
	specialvar VAR_RESULT, GetBattleOutcome
	goto_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, MauvilleCity_House2_B1F_EventScript_Caught
	msgbox MauvilleCity_House2_B1F_Text_RotomBackInTV, MSGBOX_DEFAULT
	releaseall
	end

MauvilleCity_House2_B1F_EventScript_Caught::
	setflag FLAG_CAUGHT_MAUVILLE_ROTOM
	releaseall
	end

MauvilleCity_House2_B1F_EventScript_Static::
	msgbox MauvilleCity_House2_B1F_Text_Static, MSGBOX_DEFAULT
	releaseall
	end

MauvilleCity_House2_B1F_EventScript_BoringNews::
	msgbox MauvilleCity_House2_B1F_Text_BoringNews, MSGBOX_DEFAULT
	releaseall
	end

MauvilleCity_House2_B1F_Text_Static:
	.string "Bzzzt… krrsh…\p"
	.string "Nothing but static.\n"
	.string "The TV seems to be waiting for\l"
	.string "someone with more badges.\p"
	.string "Rude, but fair.$"

MauvilleCity_House2_B1F_Text_TrashTV:
	.string "The TV flickers on by itself.\p"
	.string "“Welcome back to SHOCKING EXES,\n"
	.string "Hoenn's trashiest talk show!”\p"
	.string "“Today's guest says her ex never\n"
	.string "lifts a finger around the house.”\p"
	.string "“He just hangs around in the\n"
	.string "fridge. Then the microwave.\l"
	.string "Then the lawnmower!”\p"
	.string "“The audience wants to know…\n"
	.string "WHO is your new ex?!”\p"
	.string "“My new ex is…”\p"
	.string "“…ROTOM!”$"

MauvilleCity_House2_B1F_Text_RotomBurstsOut:
	.string "Something bursts out of the screen!$"

MauvilleCity_House2_B1F_Text_RotomBackInTV:
	.string "ROTOM zipped back into the TV.\n"
	.string "The talk show is on a commercial\l"
	.string "break. It will be back.$"

MauvilleCity_House2_B1F_Text_BoringNews:
	.string "“…and in other news, the price of\n"
	.string "POKé BALLS remains unchanged.\p"
	.string "Weather: cloudy, maybe.\n"
	.string "Back to you, nobody.”\p"
	.string "Ever since ROTOM moved out,\n"
	.string "this TV is painfully normal.$"
