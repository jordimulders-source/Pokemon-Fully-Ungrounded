@ Project Grounded: CeruleanCave_B1F (tools/grounded/maptools/spacetime_cave.py)
CeruleanCave_B1F_MapScripts::
	.byte 0

CeruleanCave_B1F_EventScript_Mewtwo::
	lock
	faceplayer
	msgbox CeruleanCave_B1F_Text_Mewtwo, MSGBOX_DEFAULT
	closemessage
	playmoncry SPECIES_MEWTWO, CRY_MODE_ENCOUNTER
	waitmoncry
	setwildbattle SPECIES_MEWTWO, 70
	setflag FLAG_SYS_CTRL_OBJ_DELETE
	special BattleSetup_StartLegendaryBattle
	waitstate
	clearflag FLAG_SYS_CTRL_OBJ_DELETE
	specialvar VAR_RESULT, GetBattleOutcome
	goto_if_eq VAR_RESULT, B_OUTCOME_RAN, CeruleanCave_B1F_EventScript_MewtwoStays
	goto_if_eq VAR_RESULT, B_OUTCOME_PLAYER_TELEPORTED, CeruleanCave_B1F_EventScript_MewtwoStays
	removeobject LOCALID_CERULEAN_CAVE_MEWTWO
	setflag FLAG_HIDE_METEOR_FALLS_MEWTWO
CeruleanCave_B1F_EventScript_MewtwoStays::
	release
	end

@ ---------------------------------------------------------------- teksten (placeholders, Jordi herschrijft ze)
CeruleanCave_B1F_Text_Mewtwo:
	.string "A voice echoes inside your head.\p"
	.string "“So. You found the real cave. The one in\n"
	.string "Hoenn was a sublet.”\p"
	.string "“I was cloned in a lab, abandoned by my\n"
	.string "makers, and left in a cave for\l"
	.string "twenty-five years.”\p"
	.string "“You are the first visitor who didn't\n"
	.string "bring a camera crew. Let us begin.”$"
