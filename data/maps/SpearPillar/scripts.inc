@ Project Grounded: SpearPillar (tools/grounded/maptools/coronet.py)
SpearPillar_MapScripts::
	map_script MAP_SCRIPT_ON_LOAD, SpearPillar_OnLoad
	map_script MAP_SCRIPT_ON_TRANSITION, SpearPillar_OnTransition
	map_script MAP_SCRIPT_ON_FRAME_TABLE, SpearPillar_OnFrame
	.byte 0

SpearPillar_OnLoad:
	call_if_set FLAG_HALL_OF_ORIGIN_OPEN, SpearPillar_EventScript_ShowLightStair
	end

SpearPillar_OnTransition:
	setflag FLAG_HIDE_CORONET_DIALGA
	setflag FLAG_HIDE_CORONET_PALKIA
	call SpearPillar_EventScript_ArmLightStair
	end

SpearPillar_OnFrame:
	map_script_2 VAR_TEMP_4, 1, SpearPillar_EventScript_LightStairScene
	.2byte 0

@ de trap van licht naar de Hall of Origin (Arceus, data/scripts/azure_flute.inc): verschijnt op Spear Pillar en op
@ Sky Pillar zodra de Azure Flute zwijgt (FLAG_ARCEUS_SKY_PILLAR); FLAG_HALL_OF_ORIGIN_OPEN houdt hem open
SpearPillar_EventScript_ArmLightStair:
	goto_if_unset FLAG_ARCEUS_SKY_PILLAR, Common_EventScript_NopReturn
	goto_if_set FLAG_HALL_OF_ORIGIN_OPEN, Common_EventScript_NopReturn
	setvar VAR_TEMP_4, 1
	return

SpearPillar_EventScript_ShowLightStair:
	setmetatile 16, 5, 0x300, FALSE
	setmetatile 16, 6, 0x2FE, FALSE
	setmetatile 16, 7, 0x2FE, FALSE
	setmetatile 16, 8, 0x2FE, FALSE
	setmetatile 16, 9, 0x2FE, FALSE
	setmetatile 16, 10, 0x2FE, FALSE
	setmetatile 16, 11, 0x2FE, FALSE
	setmetatile 16, 12, 0x2FE, FALSE
	setmetatile 16, 13, 0x2FE, FALSE
	setmetatile 16, 14, 0x2FE, FALSE
	setmetatile 16, 15, 0x2FE, FALSE
	setmetatile 17, 5, 0x301, FALSE
	setmetatile 17, 6, 0x2FF, FALSE
	setmetatile 17, 7, 0x2FF, FALSE
	setmetatile 17, 8, 0x2FF, FALSE
	setmetatile 17, 9, 0x2FF, FALSE
	setmetatile 17, 10, 0x2FF, FALSE
	setmetatile 17, 11, 0x2FF, FALSE
	setmetatile 17, 12, 0x2FF, FALSE
	setmetatile 17, 13, 0x2FF, FALSE
	setmetatile 17, 14, 0x2FF, FALSE
	setmetatile 17, 15, 0x2FF, FALSE
	return

SpearPillar_EventScript_LightStairScene:
	lockall
	setvar VAR_TEMP_4, 0
	delay 20
	msgbox SpearPillar_Text_ArceusCalls, MSGBOX_DEFAULT
	closemessage
	call AzureFlute_EventScript_Flash
	playmoncry SPECIES_ARCEUS, CRY_MODE_ENCOUNTER
	waitmoncry
	setflag FLAG_HALL_OF_ORIGIN_OPEN
	call SpearPillar_EventScript_ShowLightStair
	special DrawWholeMapView
	msgbox SpearPillar_Text_StairDescends, MSGBOX_DEFAULT
	releaseall
	end

SpearPillar_EventScript_DialgaAltar::
	lock
	goto_if_set FLAG_CORONET_DIALGA_DONE, SpearPillar_EventScript_DialgaEmpty
	msgbox SpearPillar_Text_DialgaAltar, MSGBOX_DEFAULT
	closemessage
	setvar VAR_0x8004, 2
	setvar VAR_0x8005, 3
	setvar VAR_0x8006, 12
	setvar VAR_0x8007, 3
	special ShakeCamera
	waitstate
	clearflag FLAG_HIDE_CORONET_DIALGA
	addobject LOCALID_CORONET_DIALGA
	playmoncry SPECIES_DIALGA, CRY_MODE_ENCOUNTER
	waitmoncry
	msgbox SpearPillar_Text_DialgaAppears, MSGBOX_DEFAULT
	closemessage
	setwildbattle SPECIES_DIALGA, 100
	setflag FLAG_SYS_CTRL_OBJ_DELETE
	special BattleSetup_StartLegendaryBattle
	waitstate
	clearflag FLAG_SYS_CTRL_OBJ_DELETE
	removeobject LOCALID_CORONET_DIALGA
	setflag FLAG_HIDE_CORONET_DIALGA
	specialvar VAR_RESULT, GetBattleOutcome
	goto_if_eq VAR_RESULT, B_OUTCOME_RAN, SpearPillar_EventScript_DialgaFled
	goto_if_eq VAR_RESULT, B_OUTCOME_PLAYER_TELEPORTED, SpearPillar_EventScript_DialgaFled
	setflag FLAG_CORONET_DIALGA_DONE
	goto_if_set FLAG_CORONET_PALKIA_DONE, SpearPillar_EventScript_BothDone
	msgbox SpearPillar_Text_DialgaDone, MSGBOX_DEFAULT
	release
	end

SpearPillar_EventScript_DialgaFled::
	msgbox SpearPillar_Text_DialgaFled, MSGBOX_DEFAULT
	release
	end

SpearPillar_EventScript_DialgaEmpty::
	msgbox SpearPillar_Text_DialgaEmpty, MSGBOX_DEFAULT
	release
	end

SpearPillar_EventScript_PalkiaAltar::
	lock
	goto_if_set FLAG_CORONET_PALKIA_DONE, SpearPillar_EventScript_PalkiaEmpty
	msgbox SpearPillar_Text_PalkiaAltar, MSGBOX_DEFAULT
	closemessage
	setvar VAR_0x8004, 2
	setvar VAR_0x8005, 3
	setvar VAR_0x8006, 12
	setvar VAR_0x8007, 3
	special ShakeCamera
	waitstate
	clearflag FLAG_HIDE_CORONET_PALKIA
	addobject LOCALID_CORONET_PALKIA
	playmoncry SPECIES_PALKIA, CRY_MODE_ENCOUNTER
	waitmoncry
	msgbox SpearPillar_Text_PalkiaAppears, MSGBOX_DEFAULT
	closemessage
	setwildbattle SPECIES_PALKIA, 100
	setflag FLAG_SYS_CTRL_OBJ_DELETE
	special BattleSetup_StartLegendaryBattle
	waitstate
	clearflag FLAG_SYS_CTRL_OBJ_DELETE
	removeobject LOCALID_CORONET_PALKIA
	setflag FLAG_HIDE_CORONET_PALKIA
	specialvar VAR_RESULT, GetBattleOutcome
	goto_if_eq VAR_RESULT, B_OUTCOME_RAN, SpearPillar_EventScript_PalkiaFled
	goto_if_eq VAR_RESULT, B_OUTCOME_PLAYER_TELEPORTED, SpearPillar_EventScript_PalkiaFled
	setflag FLAG_CORONET_PALKIA_DONE
	goto_if_set FLAG_CORONET_DIALGA_DONE, SpearPillar_EventScript_BothDone
	msgbox SpearPillar_Text_PalkiaDone, MSGBOX_DEFAULT
	release
	end

SpearPillar_EventScript_PalkiaFled::
	msgbox SpearPillar_Text_PalkiaFled, MSGBOX_DEFAULT
	release
	end

SpearPillar_EventScript_PalkiaEmpty::
	msgbox SpearPillar_Text_PalkiaEmpty, MSGBOX_DEFAULT
	release
	end

SpearPillar_EventScript_BothDone::
	msgbox SpearPillar_Text_BothDone, MSGBOX_DEFAULT
	closemessage
	setflag FLAG_SPACETIME_CORONET_DONE
	setvar VAR_0x8004, 3
	setvar VAR_0x8005, 3
	setvar VAR_0x8006, 16
	setvar VAR_0x8007, 2
	special ShakeCamera
	waitstate
	playse SE_M_TELEPORT
	waitse
	warp MAP_SPACETIME_CAVE, 20
	waitstate
	release
	end

@ ---------------------------------------------------------------- teksten (placeholders, Jordi herschrijft ze)
SpearPillar_Text_DialgaAltar:
	.string "A diamond floats above the altar,\n"
	.string "ticking.\p"
	.string "Not like a clock. Like a clock that's\n"
	.string "annoyed with you specifically.$"

SpearPillar_Text_DialgaAppears:
	.string "DIALGA: Gyaaahn!\p"
	.string "The seconds stop counting. One of them\n"
	.string "looks at you.$"

SpearPillar_Text_DialgaDone:
	.string "The diamond goes quiet. Somewhere a\n"
	.string "clock gets the time right for the first\l"
	.string "time in centuries.\p"
	.string "On the other altar, the pearl starts to\n"
	.string "glow.$"

SpearPillar_Text_DialgaFled:
	.string "DIALGA rewinds itself to before you\n"
	.string "showed up.\p"
	.string "The diamond ticks again. It's very smug\n"
	.string "about it.$"

SpearPillar_Text_DialgaEmpty:
	.string "The diamond is still. It's just a very\n"
	.string "expensive rock now.$"

SpearPillar_Text_PalkiaAltar:
	.string "A pearl hangs over the altar. The air\n"
	.string "around it bends, as if the pearl takes\l"
	.string "up more room than it should.$"

SpearPillar_Text_PalkiaAppears:
	.string "PALKIA: Graaaah!\p"
	.string "The mountain folds in on itself. You are\n"
	.string "now standing much closer to PALKIA\l"
	.string "than you agreed to.$"

SpearPillar_Text_PalkiaDone:
	.string "The pearl settles. Space unfolds and\n"
	.string "puts itself back roughly where it was.\p"
	.string "On the other altar, the diamond starts\n"
	.string "ticking.$"

SpearPillar_Text_PalkiaFled:
	.string "PALKIA steps sideways into a dimension\n"
	.string "you weren't invited to.\p"
	.string "The pearl is still glowing. Second date?$"

SpearPillar_Text_PalkiaEmpty:
	.string "The pearl is still. Space here is\n"
	.string "perfectly normal. It's unsettling.$"

SpearPillar_Text_ArceusCalls:
	.string "The AZURE FLUTE starts playing on its\n"
	.string "own, from inside your bag.\p"
	.string "ARCEUS: Up here. Above the spear. You've\n"
	.string "been standing on my doorstep this\l"
	.string "whole time.$"

SpearPillar_Text_StairDescends:
	.string "A stair of light unfolds from the emblem\n"
	.string "up into the sky.\p"
	.string "DIALGA and PALKIA would like it noted\n"
	.string "that they were never given a staircase.$"

SpearPillar_Text_BothDone:
	.string "Time and space both stop to look at\n"
	.string "you.\p"
	.string "That's never a good sign.\p"
	.string "SPEAR PILLAR folds up like a pop-up\n"
	.string "book, and you are the part that doesn't\l"
	.string "fit.$"
