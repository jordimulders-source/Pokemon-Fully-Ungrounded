@ Project Grounded: LakeVerity_Cavern (gegenereerd door tools/grounded/maptools/lakes.py)
LakeVerity_Cavern_MapScripts::
	.byte 0

LakeVerity_Cavern_EventScript_Mesprit::
	lock
	faceplayer
	msgbox LakeVerity_Cavern_Text_Legend, MSGBOX_DEFAULT
	playmoncry SPECIES_MESPRIT, CRY_MODE_ENCOUNTER
	waitmoncry
	setwildbattle SPECIES_MESPRIT, 94
	setflag FLAG_SYS_CTRL_OBJ_DELETE
	special BattleSetup_StartLegendaryBattle
	waitstate
	clearflag FLAG_SYS_CTRL_OBJ_DELETE
	specialvar VAR_RESULT, GetBattleOutcome
	goto_if_eq VAR_RESULT, B_OUTCOME_RAN, LakeVerity_Cavern_EventScript_LegendStays
	goto_if_eq VAR_RESULT, B_OUTCOME_PLAYER_TELEPORTED, LakeVerity_Cavern_EventScript_LegendStays
	removeobject LOCALID_LAKE_VERITY_CAVERN_MESPRIT
	setflag FLAG_HIDE_LAKE_VERITY_MESPRIT
	setflag FLAG_LAKE_VERITY_DONE
	goto_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, LakeVerity_Cavern_EventScript_LegendCaught
	msgbox LakeVerity_Cavern_Text_LegendFled, MSGBOX_DEFAULT
	release
	end

LakeVerity_Cavern_EventScript_LegendCaught::
	msgbox LakeVerity_Cavern_Text_LegendCaught, MSGBOX_DEFAULT
	release
	end

LakeVerity_Cavern_EventScript_LegendStays::
	release
	end

LakeVerity_Cavern_EventScript_Wall::
	msgbox LakeVerity_Cavern_Text_Wall, MSGBOX_SIGN
	end

@ ---------------------------------------------------------------- teksten (placeholders, Jordi herschrijft ze)
LakeVerity_Cavern_Text_Legend:
	.string "A small pink being drifts over the\n"
	.string "water, humming.\p"
	.string "It is the embodiment of emotion. It\n"
	.string "looks at you and starts crying, then\l"
	.string "laughing, then crying again. It is\l"
	.string "having your feelings for you. You're\l"
	.string "welcome.$"

LakeVerity_Cavern_Text_LegendCaught:
	.string "You caught MESPRIT. It is already\n"
	.string "crying about how happy it is.$"

LakeVerity_Cavern_Text_LegendFled:
	.string "MESPRIT vanishes in a puff of mixed\n"
	.string "feelings. Mostly yours.$"

LakeVerity_Cavern_Text_Wall:
	.string "The cave is flooded. With water. And,\n"
	.string "faintly, with feelings.\p"
	.string "Someone carved a message into the\n"
	.string "rock: “BACK IN 5 MINUTES.” The rock is\l"
	.string "several thousand years old.$"
