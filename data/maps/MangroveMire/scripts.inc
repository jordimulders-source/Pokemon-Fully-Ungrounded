@ Project Grounded: Mangrove Mire (kaart: tools/grounded/maptools/mangrove_swamp.py)
@ Mangrovemoeras tussen Fortree Jungle (west) en Route 120 (oost). Andere tileset, dus warps via coord-triggers.
@ Placeholderteksten; Jordi herschrijft ze via de Dialoogstudio.

MangroveMire_MapScripts::
	map_script MAP_SCRIPT_ON_TRANSITION, MangroveMire_OnTransition
	.byte 0

@ Project Grounded: Virizion (swords_keldeo.py) staat pas na de Hall of Fame op de open plek aan het oostelijke
@ zijpad (49,14); weg na vangen/verslaan.
MangroveMire_OnTransition:
	call_if_unset FLAG_SYS_GAME_CLEAR, SwordsOfJustice_EventScript_HideSword
	call_if_set FLAG_DEFEATED_VIRIZION, SwordsOfJustice_EventScript_HideSword
	end

MangroveMire_EventScript_Virizion::
	lock
	msgbox MangroveMire_Text_Virizion, MSGBOX_DEFAULT
	closemessage
	playmoncry SPECIES_VIRIZION, CRY_MODE_ENCOUNTER
	waitmoncry
	setwildbattle SPECIES_VIRIZION, 70
	setflag FLAG_SYS_CTRL_OBJ_DELETE
	special BattleSetup_StartLegendaryBattle
	waitstate
	clearflag FLAG_SYS_CTRL_OBJ_DELETE
	specialvar VAR_RESULT, GetBattleOutcome
	goto_if_eq VAR_RESULT, B_OUTCOME_RAN, SwordsOfJustice_EventScript_SwordStays
	goto_if_eq VAR_RESULT, B_OUTCOME_PLAYER_TELEPORTED, SwordsOfJustice_EventScript_SwordStays
	removeobject LOCALID_MANGROVE_MIRE_VIRIZION
	setflag FLAG_DEFEATED_VIRIZION
	goto SwordsOfJustice_EventScript_AfterSword
	end

MangroveMire_EventScript_CutTree::
	msgbox MangroveMire_Text_CutTree, MSGBOX_SIGN
	end

MangroveMire_Text_Virizion:
	.string "A slender green deer stands where\n"
	.string "the path gives up.\p"
	.string "It is the only thing in this swamp\n"
	.string "that is not damp. Somehow.\p"
	.string "It lowers its horns. Politely.\n"
	.string "Like a fencer. A wet fencer.$"

MangroveMire_Text_CutTree:
	.string "A mangrove trunk with one clean,\n"
	.string "diagonal cut. No axe does that.\p"
	.string "The tree seems fine with it. It has\n"
	.string "seen worse. It lives in a swamp.$"

MangroveMire_EventScript_ToJungle::
	warpsilent MAP_FORTREE_JUNGLE, 38, 39
	waitstate
	end

MangroveMire_EventScript_ToRoute120::
	warpsilent MAP_ROUTE120, 1, 60
	waitstate
	end

MangroveMire_EventScript_SignWest::
	msgbox MangroveMire_Text_SignWest, MSGBOX_SIGN
	end

MangroveMire_EventScript_SignEast::
	msgbox MangroveMire_Text_SignEast, MSGBOX_SIGN
	end

@ ---------------------------------------------------------------- trainers
MangroveMire_EventScript_Otto::
	trainerbattle_single TRAINER_MIRE_OTTO, MangroveMire_Text_OttoIntro, MangroveMire_Text_OttoDefeat
	msgbox MangroveMire_Text_OttoPostBattle, MSGBOX_AUTOCLOSE
	end

MangroveMire_EventScript_Griselda::
	trainerbattle_single TRAINER_MIRE_GRISELDA, MangroveMire_Text_GriseldaIntro, MangroveMire_Text_GriseldaDefeat
	msgbox MangroveMire_Text_GriseldaPostBattle, MSGBOX_AUTOCLOSE
	end

MangroveMire_EventScript_Fern::
	trainerbattle_single TRAINER_MIRE_FERN, MangroveMire_Text_FernIntro, MangroveMire_Text_FernDefeat
	msgbox MangroveMire_Text_FernPostBattle, MSGBOX_AUTOCLOSE
	end

MangroveMire_EventScript_Kappa::
	trainerbattle_single TRAINER_MIRE_KAPPA, MangroveMire_Text_KappaIntro, MangroveMire_Text_KappaDefeat
	msgbox MangroveMire_Text_KappaPostBattle, MSGBOX_AUTOCLOSE
	end

@ ---------------------------------------------------------------- teksten
MangroveMire_Text_SignWest:
	.string "MANGROVE MIRE\n"
	.string "{LEFT_ARROW} FORTREE JUNGLE  ROUTE 120 {RIGHT_ARROW}\p"
	.string "Stay on the boardwalk. The mud has\n"
	.string "a lost-and-found. Nobody has ever\l"
	.string "found anything in it.$"

MangroveMire_Text_SignEast:
	.string "MANGROVE MIRE\n"
	.string "{LEFT_ARROW} FORTREE JUNGLE  ROUTE 120 {RIGHT_ARROW}\p"
	.string "Leaving the mire? Check your shoes.\n"
	.string "Then check them for passengers.$"

MangroveMire_Text_OttoIntro:
	.string "Shh! I've been waiting nine hours\n"
	.string "for a bite.\p"
	.string "You'll do.$"

MangroveMire_Text_OttoDefeat:
	.string "Even the swamp is laughing at me.\n"
	.string "It sounds like a drain.$"

MangroveMire_Text_OttoPostBattle:
	.string "Fish here taste like old boots.\n"
	.string "I know, because I've caught both.$"

MangroveMire_Text_GriseldaIntro:
	.string "Hehehe… Welcome to my kitchen.\p"
	.string "The cauldron is the whole swamp.\n"
	.string "You're the seasoning.$"

MangroveMire_Text_GriseldaDefeat:
	.string "My curses only work on people\n"
	.string "who read the terms and conditions.$"

MangroveMire_Text_GriseldaPostBattle:
	.string "Swamp gas isn't a ghost.\n"
	.string "Usually. Don't breathe it in, just\l"
	.string "in case it's Gary.$"

MangroveMire_Text_FernIntro:
	.string "I'm a POKéMON RANGER. My job is\n"
	.string "protecting this ecosystem.\p"
	.string "You are an invasive species.$"

MangroveMire_Text_FernDefeat:
	.string "Fine. You can stay.\n"
	.string "Like the mosquitoes.$"

MangroveMire_Text_FernPostBattle:
	.string "Mangroves store more carbon than\n"
	.string "rainforests.\p"
	.string "They also store a lot of my\n"
	.string "flip-flops.$"

MangroveMire_Text_KappaIntro:
	.string "You bowed to the tree! Nobody ever\n"
	.string "bows to the tree!\p"
	.string "…Wait, you didn't bow. Battle!$"

MangroveMire_Text_KappaDefeat:
	.string "A true ninja knows when to retreat.\n"
	.string "My legs are stuck in the mud though.$"

MangroveMire_Text_KappaPostBattle:
	.string "Three days I've been a tree.\n"
	.string "A woodpecker proposed to me.$"
