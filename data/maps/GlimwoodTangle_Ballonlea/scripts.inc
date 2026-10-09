@ Project Grounded: GlimwoodTangle_Ballonlea (tools/grounded/maptools/glimwood.py)
GlimwoodTangle_Ballonlea_MapScripts::
	map_script MAP_SCRIPT_ON_TRANSITION, GlimwoodTangle_Ballonlea_OnTransition
	map_script MAP_SCRIPT_ON_FRAME_TABLE, GlimwoodTangle_Ballonlea_OnFrame
	.byte 0

GlimwoodTangle_Ballonlea_OnTransition:
	call_if_set FLAG_GLIMWOOD_SCENE_PENDING, GlimwoodTangle_Ballonlea_EventScript_SetScene
	goto_if_set FLAG_GLIMWOOD_XERNEAS_DONE, GlimwoodTangle_Ballonlea_EventScript_StateEnd
	setmaplayoutindex LAYOUT_GLIMWOOD_TANGLE_BALLONLEA_DYING
	setweather WEATHER_SHADE
	savebgm MUS_RG_POKE_TOWER
GlimwoodTangle_Ballonlea_EventScript_StateEnd:
	end

GlimwoodTangle_Ballonlea_EventScript_SetScene:
	setvar VAR_TEMP_1, 1
	return

GlimwoodTangle_Ballonlea_OnFrame:
	map_script_2 VAR_TEMP_1, 1, GlimwoodTangle_Ballonlea_EventScript_Scene
	.2byte 0

GlimwoodTangle_Ballonlea_EventScript_Scene:
	lockall
	setvar VAR_TEMP_1, 0
	clearflag FLAG_GLIMWOOD_SCENE_PENDING
	delay 30
	playse SE_M_HEAL_BELL
	msgbox GlimwoodTangle_Ballonlea_Text_Relit, MSGBOX_DEFAULT
	releaseall
	end

GlimwoodTangle_Ballonlea_EventScript_Witch::
	lock
	faceplayer
	goto_if_set FLAG_SPACETIME_GLIMWOOD_DONE, GlimwoodTangle_Ballonlea_EventScript_WitchDone
	goto_if_set FLAG_GLIMWOOD_XERNEAS_DONE, GlimwoodTangle_Ballonlea_EventScript_WitchLight
	goto_if_set FLAG_GLIMWOOD_GANG_BOSS, GlimwoodTangle_Ballonlea_EventScript_WitchGo
	msgbox GlimwoodTangle_Ballonlea_Text_Witch, MSGBOX_DEFAULT
	release
	end

GlimwoodTangle_Ballonlea_EventScript_WitchGo:
	msgbox GlimwoodTangle_Ballonlea_Text_WitchGo, MSGBOX_DEFAULT
	release
	end

GlimwoodTangle_Ballonlea_EventScript_WitchLight:
	msgbox GlimwoodTangle_Ballonlea_Text_WitchLight, MSGBOX_DEFAULT
	release
	end

GlimwoodTangle_Ballonlea_EventScript_WitchDone:
	msgbox GlimwoodTangle_Ballonlea_Text_WitchDone, MSGBOX_DEFAULT
	release
	end

GlimwoodTangle_Ballonlea_EventScript_Boss::
	lock
	faceplayer
	playmoncry SPECIES_GRIMMSNARL, CRY_MODE_ENCOUNTER
	msgbox GlimwoodTangle_Ballonlea_Text_Boss, MSGBOX_DEFAULT
	waitmoncry
	closemessage
	setwildbattle SPECIES_GRIMMSNARL, 67, ITEM_NONE, SPECIES_MORGREM, 66, ITEM_NONE
	dowildbattle
	specialvar VAR_RESULT, GetBattleOutcome
	goto_if_eq VAR_RESULT, B_OUTCOME_WON, GlimwoodTangle_Ballonlea_EventScript_BossGone
	goto_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, GlimwoodTangle_Ballonlea_EventScript_BossGone
	release
	end

GlimwoodTangle_Ballonlea_EventScript_BossGone::
	fadescreen FADE_TO_BLACK
	removeobject LOCALID_BALLONLEA_BOSS_A
	removeobject LOCALID_BALLONLEA_BOSS_B
	setflag FLAG_GLIMWOOD_GANG_BOSS
	fadescreen FADE_FROM_BLACK
	msgbox GlimwoodTangle_Ballonlea_Text_BossGone, MSGBOX_DEFAULT
	release
	end

GlimwoodTangle_Ballonlea_EventScript_Xerneas::
	lock
	playmoncry SPECIES_XERNEAS, CRY_MODE_ENCOUNTER
	msgbox GlimwoodTangle_Ballonlea_Text_Xerneas, MSGBOX_DEFAULT
	waitmoncry
	closemessage
	setwildbattle SPECIES_XERNEAS, 70
	special BattleSetup_StartLegendaryBattle
	waitstate
	specialvar VAR_RESULT, GetBattleOutcome
	goto_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, GlimwoodTangle_Ballonlea_EventScript_XerneasCaught
	goto_if_eq VAR_RESULT, B_OUTCOME_WON, GlimwoodTangle_Ballonlea_EventScript_XerneasTree
	release
	end

GlimwoodTangle_Ballonlea_EventScript_XerneasTree::
	msgbox GlimwoodTangle_Ballonlea_Text_XerneasTree, MSGBOX_DEFAULT
	release
	end

GlimwoodTangle_Ballonlea_EventScript_XerneasCaught::
	removeobject LOCALID_BALLONLEA_XERNEAS
	setflag FLAG_GLIMWOOD_XERNEAS_DONE
	setflag FLAG_GLIMWOOD_SCENE_PENDING
	playse SE_M_HEAL_BELL
	fadescreenspeed FADE_TO_WHITE, 8
	warpsilent MAP_GLIMWOOD_TANGLE_BALLONLEA, 17, 6
	waitstate
	release
	end

GlimwoodTangle_Ballonlea_EventScript_HouseDoor::
	msgbox GlimwoodTangle_Ballonlea_Text_HouseDoor, MSGBOX_SIGN
	end

GlimwoodTangle_Ballonlea_EventScript_WitchDoor::
	msgbox GlimwoodTangle_Ballonlea_Text_WitchDoor, MSGBOX_SIGN
	end

GlimwoodTangle_Ballonlea_EventScript_Arthur::
	trainerbattle_single TRAINER_BALLONLEA_GENTLEMAN_ARTHUR, GlimwoodTangle_Ballonlea_Text_ArthurIntro, GlimwoodTangle_Ballonlea_Text_ArthurDefeat
	msgbox GlimwoodTangle_Ballonlea_Text_ArthurPost, MSGBOX_AUTOCLOSE
	end

@ ---------------------------------------------------------------- teksten (placeholders, Jordi herschrijft ze)
GlimwoodTangle_Ballonlea_Text_Relit:
	.string "Light floods back into BALLONLEA.\n"
	.string "Every mushroom glows at once, like a\l"
	.string "village that just remembered it left\l"
	.string "the oven on.$"

GlimwoodTangle_Ballonlea_Text_Witch:
	.string "You again! Pop quiz: who's blocking the\n"
	.string "stairs to XERNEAS? ...A GRIMMSNARL with\l"
	.string "a fringe. Correct. Go and be rude to it.$"

GlimwoodTangle_Ballonlea_Text_WitchGo:
	.string "Stairs are free. XERNEAS sleeps in the\n"
	.string "fairy ring up top. Be gentle. And bring a\l"
	.string "ball. Gentleness alone has never caught\l"
	.string "anything.$"

GlimwoodTangle_Ballonlea_Text_WitchLight:
	.string "Look at it glow! Pop quiz: what comes\n"
	.string "after life? ...Yes. Exactly. Something\l"
	.string "just landed in the forest. Don't keep it\l"
	.string "waiting.$"

GlimwoodTangle_Ballonlea_Text_WitchDone:
	.string "XERNEAS and YVELTAL. You've got the\n"
	.string "whole circle of life in your bag, dearie.\l"
	.string "Final quiz: who's cleaning up all these\l"
	.string "spores? ...Wrong. It's still you.$"

GlimwoodTangle_Ballonlea_Text_Boss:
	.string "GRIMMSNARL, the boss of the gang, sits\n"
	.string "on the stairs with its hair crossed.\l"
	.string "MORGREM holds its coat. Nobody gets\l"
	.string "past without a fight. Or a very good\l"
	.string "bribe.$"

GlimwoodTangle_Ballonlea_Text_BossGone:
	.string "GRIMMSNARL storms off into the dark,\n"
	.string "taking its hair with it. The stairs to\l"
	.string "XERNEAS are free.$"

GlimwoodTangle_Ballonlea_Text_Xerneas:
	.string "XERNEAS slumbers in the fairy ring, its\n"
	.string "antlers flickering like a lamp on its\l"
	.string "last bulb. It opens one eye. Then the\l"
	.string "other. Then the antlers.$"

GlimwoodTangle_Ballonlea_Text_XerneasTree:
	.string "XERNEAS turns into a tree to rest. Give\n"
	.string "it a minute. ...It's back. Trees are\l"
	.string "surprisingly fast at this.$"

GlimwoodTangle_Ballonlea_Text_HouseDoor:
	.string "The door is locked. A note: OUT. DO NOT\n"
	.string "LICK THE WALLS. THEY ARE LOAD-BEARING\l"
	.string "MUSHROOM.$"

GlimwoodTangle_Ballonlea_Text_WitchDoor:
	.string "THE WITCH'S HOUSE. Visitors by\n"
	.string "appointment. Appointments by prophecy.$"

GlimwoodTangle_Ballonlea_Text_ArthurIntro:
	.string "I review the BALLONLEA STADIUM shows.\n"
	.string "One star. Every one. Let's see what\l"
	.string "you're worth.$"

GlimwoodTangle_Ballonlea_Text_ArthurDefeat:
	.string "Two stars. Don't let it go to your head.$"

GlimwoodTangle_Ballonlea_Text_ArthurPost:
	.string "The play tonight is about a mushroom\n"
	.string "who becomes a stage. I've seen it.\l"
	.string "Twice. Unwillingly.$"
