@ Project Grounded: LakeValor_Cavern (gegenereerd door tools/grounded/maptools/lakes.py)
LakeValor_Cavern_MapScripts::
	.byte 0

LakeValor_Cavern_EventScript_Azelf::
	lock
	faceplayer
	msgbox LakeValor_Cavern_Text_Legend, MSGBOX_DEFAULT
	playmoncry SPECIES_AZELF, CRY_MODE_ENCOUNTER
	waitmoncry
	setwildbattle SPECIES_AZELF, 94
	setflag FLAG_SYS_CTRL_OBJ_DELETE
	special BattleSetup_StartLegendaryBattle
	waitstate
	clearflag FLAG_SYS_CTRL_OBJ_DELETE
	specialvar VAR_RESULT, GetBattleOutcome
	goto_if_eq VAR_RESULT, B_OUTCOME_RAN, LakeValor_Cavern_EventScript_LegendStays
	goto_if_eq VAR_RESULT, B_OUTCOME_PLAYER_TELEPORTED, LakeValor_Cavern_EventScript_LegendStays
	removeobject LOCALID_LAKE_VALOR_CAVERN_AZELF
	setflag FLAG_HIDE_LAKE_VALOR_AZELF
	setflag FLAG_LAKE_VALOR_DONE
	goto_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, LakeValor_Cavern_EventScript_LegendCaught
	msgbox LakeValor_Cavern_Text_LegendFled, MSGBOX_DEFAULT
	release
	end

LakeValor_Cavern_EventScript_LegendCaught::
	msgbox LakeValor_Cavern_Text_LegendCaught, MSGBOX_DEFAULT
	release
	end

LakeValor_Cavern_EventScript_LegendStays::
	release
	end

LakeValor_Cavern_EventScript_Wall::
	msgbox LakeValor_Cavern_Text_Wall, MSGBOX_SIGN
	end

@ ---------------------------------------------------------------- teksten (placeholders, Jordi herschrijft ze)
LakeValor_Cavern_Text_Legend:
	.string "A small blue being hovers in the dark,\n"
	.string "perfectly still.\p"
	.string "It is the embodiment of willpower. It\n"
	.string "has been waiting here for a challenger\l"
	.string "for about four thousand years, out of\l"
	.string "sheer stubbornness.$"

LakeValor_Cavern_Text_LegendCaught:
	.string "You caught AZELF. It looks very brave\n"
	.string "inside the ball. From a safe distance.$"

LakeValor_Cavern_Text_LegendFled:
	.string "AZELF vanishes. It wasn't scared. It\n"
	.string "just had a thing. A brave thing.\l"
	.string "Elsewhere.$"

LakeValor_Cavern_Text_Wall:
	.string "The cave is flooded. AZELF could have\n"
	.string "picked dry land. It picked drama.\p"
	.string "Someone carved a message into the\n"
	.string "rock: “BACK IN 5 MINUTES.” The rock is\l"
	.string "several thousand years old.$"
