@ Project Grounded: LakeAcuity_Cavern (gegenereerd door tools/grounded/maptools/lakes.py)
LakeAcuity_Cavern_MapScripts::
	.byte 0

LakeAcuity_Cavern_EventScript_Uxie::
	lock
	faceplayer
	msgbox LakeAcuity_Cavern_Text_Legend, MSGBOX_DEFAULT
	playmoncry SPECIES_UXIE, CRY_MODE_ENCOUNTER
	waitmoncry
	setwildbattle SPECIES_UXIE, 94
	setflag FLAG_SYS_CTRL_OBJ_DELETE
	special BattleSetup_StartLegendaryBattle
	waitstate
	clearflag FLAG_SYS_CTRL_OBJ_DELETE
	specialvar VAR_RESULT, GetBattleOutcome
	goto_if_eq VAR_RESULT, B_OUTCOME_RAN, LakeAcuity_Cavern_EventScript_LegendStays
	goto_if_eq VAR_RESULT, B_OUTCOME_PLAYER_TELEPORTED, LakeAcuity_Cavern_EventScript_LegendStays
	removeobject LOCALID_LAKE_ACUITY_CAVERN_UXIE
	setflag FLAG_HIDE_LAKE_ACUITY_UXIE
	setflag FLAG_LAKE_ACUITY_DONE
	goto_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, LakeAcuity_Cavern_EventScript_LegendCaught
	msgbox LakeAcuity_Cavern_Text_LegendFled, MSGBOX_DEFAULT
	release
	end

LakeAcuity_Cavern_EventScript_LegendCaught::
	msgbox LakeAcuity_Cavern_Text_LegendCaught, MSGBOX_DEFAULT
	release
	end

LakeAcuity_Cavern_EventScript_LegendStays::
	release
	end

LakeAcuity_Cavern_EventScript_Wall::
	msgbox LakeAcuity_Cavern_Text_Wall, MSGBOX_SIGN
	end

@ ---------------------------------------------------------------- teksten (placeholders, Jordi herschrijft ze)
LakeAcuity_Cavern_Text_Legend:
	.string "A small yellow being floats above the\n"
	.string "water with its eyes shut.\p"
	.string "It is said that meeting its gaze wipes\n"
	.string "your memory. It already knows this\l"
	.string "about you. It knows a lot about you. It\l"
	.string "is being polite about the browser\l"
	.string "history.$"

LakeAcuity_Cavern_Text_LegendCaught:
	.string "You caught UXIE. You will remember this\n"
	.string "forever. Probably. Ask UXIE.$"

LakeAcuity_Cavern_Text_LegendFled:
	.string "UXIE fades away. You feel like you\n"
	.string "forgot something. You did. You forgot\l"
	.string "to catch it.$"

LakeAcuity_Cavern_Text_Wall:
	.string "The cave is flooded. Of course it is.\p"
	.string "Someone carved a message into the\n"
	.string "rock: “BACK IN 5 MINUTES.” The rock is\l"
	.string "several thousand years old.$"
