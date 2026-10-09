@ Project Grounded: de grot van Whirl Island (kopie van MarineCave_End). Lugia (lv 60) ligt aan de rand van het meer,
@ maar alleen als de Silver Wing (zeetempel, Route 128) in de tas zit. Verslagen = komt bij een volgend bezoek
@ terug; gevangen = weg (FLAG_CAUGHT_WHIRL_ISLAND_LUGIA). Objectflag FLAG_TEMP_1 (gezet = verborgen).
WhirlIsland_Cave_MapScripts::
	map_script MAP_SCRIPT_ON_TRANSITION, WhirlIsland_Cave_OnTransition
	.byte 0

WhirlIsland_Cave_OnTransition:
	setflag FLAG_TEMP_1
	goto_if_set FLAG_CAUGHT_WHIRL_ISLAND_LUGIA, WhirlIsland_Cave_EventScript_TransitionEnd
	checkitem ITEM_SILVER_WING
	goto_if_eq VAR_RESULT, FALSE, WhirlIsland_Cave_EventScript_TransitionEnd
	clearflag FLAG_TEMP_1
WhirlIsland_Cave_EventScript_TransitionEnd::
	end

WhirlIsland_Cave_EventScript_Lugia::
	lock
	faceplayer
	playmoncry SPECIES_LUGIA, CRY_MODE_ENCOUNTER
	msgbox WhirlIsland_Cave_Text_Lugia, MSGBOX_DEFAULT
	waitmoncry
	closemessage
	setwildbattle SPECIES_LUGIA, 90
	setflag FLAG_SYS_CTRL_OBJ_DELETE
	special BattleSetup_StartLegendaryBattle
	waitstate
	clearflag FLAG_SYS_CTRL_OBJ_DELETE
	specialvar VAR_RESULT, GetBattleOutcome
	goto_if_eq VAR_RESULT, B_OUTCOME_RAN, WhirlIsland_Cave_EventScript_LugiaStays
	goto_if_eq VAR_RESULT, B_OUTCOME_PLAYER_TELEPORTED, WhirlIsland_Cave_EventScript_LugiaStays
	removeobject LOCALID_WHIRL_ISLAND_LUGIA
	setflag FLAG_TEMP_1
	goto_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, WhirlIsland_Cave_EventScript_LugiaCaught
	msgbox WhirlIsland_Cave_Text_LugiaDived, MSGBOX_DEFAULT
	release
	end

WhirlIsland_Cave_EventScript_LugiaCaught::
	setflag FLAG_CAUGHT_WHIRL_ISLAND_LUGIA
WhirlIsland_Cave_EventScript_LugiaStays::
	release
	end

WhirlIsland_Cave_EventScript_Lake::
	goto_if_set FLAG_CAUGHT_WHIRL_ISLAND_LUGIA, WhirlIsland_Cave_EventScript_LakeEmpty
	msgbox WhirlIsland_Cave_Text_Lake, MSGBOX_SIGN
	end

WhirlIsland_Cave_EventScript_LakeEmpty::
	msgbox WhirlIsland_Cave_Text_LakeEmpty, MSGBOX_SIGN
	end

WhirlIsland_Cave_Text_Lugia:
	.string "The water folds open.\p"
	.string "Something silver and very old looks at\n"
	.string "you. Then at the feather in your bag.\l"
	.string "Then back at you.\p"
	.string "It clearly means: “That's mine.”$"

WhirlIsland_Cave_Text_LugiaDived:
	.string "LUGIA sinks back into the lake without\n"
	.string "a sound.\p"
	.string "It will come up again. It is a very\n"
	.string "patient bird. Unlike your rival.$"

WhirlIsland_Cave_Text_Lake:
	.string "The water is perfectly still.\p"
	.string "Something enormous is down there,\n"
	.string "ignoring you. Professionally.\p"
	.string "Maybe it would care if you carried\n"
	.string "something that belongs to it.$"

WhirlIsland_Cave_Text_LakeEmpty:
	.string "Just water now. Wet, slightly\n"
	.string "disappointed water.$"
