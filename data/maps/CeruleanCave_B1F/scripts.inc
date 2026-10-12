@ Project Grounded: CeruleanCave_B1F (tools/grounded/maptools/spacetime_cave.py)
CeruleanCave_B1F_MapScripts::
	.byte 0

CeruleanCave_B1F_EventScript_Maxine::
	trainerbattle_single TRAINER_CC_GRUNT_MAXINE, CeruleanCave_B1F_Text_MaxineIntro, CeruleanCave_B1F_Text_MaxineDefeat
	msgbox CeruleanCave_B1F_Text_MaxinePost, MSGBOX_AUTOCLOSE
	end

CeruleanCave_B1F_EventScript_Giovanni::
	trainerbattle_single TRAINER_CC_GIOVANNI, CeruleanCave_B1F_Text_GiovanniIntro, CeruleanCave_B1F_Text_GiovanniDefeat, CeruleanCave_B1F_EventScript_GiovanniDefeated
	end

CeruleanCave_B1F_EventScript_GiovanniDefeated::
	msgbox CeruleanCave_B1F_Text_GiovanniLeaves, MSGBOX_DEFAULT
	closemessage
	fadescreen FADE_TO_BLACK
	removeobject LOCALID_CERULEAN_CAVE_GIOVANNI
	fadescreen FADE_FROM_BLACK
	goto CeruleanCave_B1F_EventScript_MewtwoHeal

CeruleanCave_B1F_EventScript_Mewtwo::
	lock
	faceplayer
	goto CeruleanCave_B1F_EventScript_MewtwoHeal

CeruleanCave_B1F_EventScript_MewtwoHeal::
	playmoncry SPECIES_MEWTWO, CRY_MODE_ENCOUNTER
	msgbox CeruleanCave_B1F_Text_Mewtwo, MSGBOX_DEFAULT
	waitmoncry
	closemessage
	playse SE_M_PSYBEAM
	fadescreenspeed FADE_TO_WHITE, 4
	special HealPlayerParty
	fadescreenspeed FADE_FROM_WHITE, 4
	playfanfare MUS_HEAL
	waitfanfare
	msgbox CeruleanCave_B1F_Text_MewtwoHealed, MSGBOX_DEFAULT
	closemessage
	playmoncry SPECIES_MEWTWO, CRY_MODE_ENCOUNTER
	waitmoncry
	setwildbattle SPECIES_MEWTWO, 95
	setflag FLAG_SYS_CTRL_OBJ_DELETE
	special BattleSetup_StartLegendaryBattle
	waitstate
	clearflag FLAG_SYS_CTRL_OBJ_DELETE
	specialvar VAR_RESULT, GetBattleOutcome
	goto_if_eq VAR_RESULT, B_OUTCOME_RAN, CeruleanCave_B1F_EventScript_MewtwoStays
	goto_if_eq VAR_RESULT, B_OUTCOME_PLAYER_TELEPORTED, CeruleanCave_B1F_EventScript_MewtwoStays
	removeobject LOCALID_CERULEAN_CAVE_MEWTWO
	setflag FLAG_HIDE_METEOR_FALLS_MEWTWO
	setflag FLAG_SPACETIME_CERULEAN_DONE
CeruleanCave_B1F_EventScript_MewtwoStays::
	release
	end

@ ---------------------------------------------------------------- teksten (placeholders, Jordi herschrijft ze)
CeruleanCave_B1F_Text_MaxineIntro:
	.string "I'm TEAM ROCKET's head of research. Our\n"
	.string "research says: you shouldn't be here.$"

CeruleanCave_B1F_Text_MaxineDefeat:
	.string "Peer review is brutal.$"

CeruleanCave_B1F_Text_MaxinePost:
	.string "We cloned it once. We can't even find it\n"
	.string "twice. Science is humbling.$"

CeruleanCave_B1F_Text_GiovanniIntro:
	.string "GIOVANNI: So. The child from the hole in\n"
	.string "the sky.\p"
	.string "In this world, TEAM ROCKET never fell.\n"
	.string "We simply ran out of things to steal.\l"
	.string "Then the cave started whispering a\l"
	.string "name.\p"
	.string "MEWTWO was made by my people. I'm only\n"
	.string "collecting what's mine.$"

CeruleanCave_B1F_Text_GiovanniDefeat:
	.string "...Impressive. Annoyingly so.$"

CeruleanCave_B1F_Text_GiovanniLeaves:
	.string "GIOVANNI: Keep it, then. Every\n"
	.string "dimension has a GIOVANNI, and every\l"
	.string "GIOVANNI learns to lose with dignity.\p"
	.string "Most of them. I'm one of the good ones.\p"
	.string "TEAM ROCKET! We're leaving. Somebody\n"
	.string "fetch the van.$"

CeruleanCave_B1F_Text_Mewtwo:
	.string "A voice echoes inside your head.\p"
	.string "“He was right about one thing. I was\n"
	.string "made. I was not made to be owned.”\p"
	.string "“You fought him for me, and your team is\n"
	.string "exhausted. I will not fight an\l"
	.string "exhausted opponent. Where is the honor\l"
	.string "in that? Where is the CHALLENGE?”$"

CeruleanCave_B1F_Text_MewtwoHealed:
	.string "MEWTWO restored your POKéMON to full\n"
	.string "health!\p"
	.string "“Now. Show me what you are worth.”$"
