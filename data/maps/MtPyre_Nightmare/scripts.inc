@ Project Grounded: Darkrai's nachtmerrie. Je komt hier in slaap vanaf de top van Mt. Pyre (post-game, 's nachts).
@ Darkrai (lv 70) zweeft voor het heiligdom. Na het gevecht (wat de uitkomst ook is) word je wakker op de top.
MtPyre_Nightmare_MapScripts::
	map_script MAP_SCRIPT_ON_FRAME_TABLE, MtPyre_Nightmare_OnFrame
	.byte 0

MtPyre_Nightmare_OnFrame:
	map_script_2 VAR_NIGHT_LEGEND_STATE, 2, MtPyre_Nightmare_EventScript_Arrive
	.2byte 0

MtPyre_Nightmare_EventScript_Arrive::
	lockall
	applymovement LOCALID_PLAYER, Common_Movement_FaceUp
	waitmovement 0
	msgbox MtPyre_Nightmare_Text_WhereIsThis, MSGBOX_DEFAULT
	setvar VAR_NIGHT_LEGEND_STATE, 4
	releaseall
	end

MtPyre_Nightmare_EventScript_Darkrai::
	lockall
	faceplayer
	msgbox MtPyre_Nightmare_Text_Darkrai, MSGBOX_DEFAULT
	closemessage
	playmoncry SPECIES_DARKRAI, CRY_MODE_ENCOUNTER
	waitmoncry
	setwildbattle SPECIES_DARKRAI, 93
	setflag FLAG_SYS_CTRL_OBJ_DELETE
	special BattleSetup_StartLegendaryBattle
	waitstate
	clearflag FLAG_SYS_CTRL_OBJ_DELETE
	specialvar VAR_RESULT, GetBattleOutcome
	goto_if_eq VAR_RESULT, B_OUTCOME_RAN, MtPyre_Nightmare_EventScript_DarkraiStays
	goto_if_eq VAR_RESULT, B_OUTCOME_PLAYER_TELEPORTED, MtPyre_Nightmare_EventScript_DarkraiStays
	setflag FLAG_DEFEATED_DARKRAI
	removeobject LOCALID_MT_PYRE_NIGHTMARE_DARKRAI
	msgbox MtPyre_Nightmare_Text_NightmareFades, MSGBOX_DEFAULT
	goto MtPyre_Nightmare_EventScript_WakeUp
	end

MtPyre_Nightmare_EventScript_DarkraiStays::
	msgbox MtPyre_Nightmare_Text_DarkraiLaughs, MSGBOX_DEFAULT
	goto MtPyre_Nightmare_EventScript_WakeUp
	end

MtPyre_Nightmare_EventScript_WakeUp::
	closemessage
	setvar VAR_NIGHT_LEGEND_STATE, 3
	fadescreenspeed FADE_TO_BLACK, 6
	warpsilent MAP_MT_PYRE_SUMMIT, 23, 7
	waitstate
	releaseall
	end

MtPyre_Nightmare_Text_WhereIsThis:
	.string "…Huh?\p"
	.string "This is the summit, but the colors are\n"
	.string "all wrong and the stairs are gone.\p"
	.string "There are more graves than before. One\n"
	.string "of them has your name on it. Spelled\l"
	.string "wrong.$"

MtPyre_Nightmare_Text_Darkrai:
	.string "A shadow with one cold blue eye is\n"
	.string "waiting in front of the shrine.\p"
	.string "One, two, DARKRAI's coming for you. It\n"
	.string "never learned the rest of the song.$"

MtPyre_Nightmare_Text_NightmareFades:
	.string "The shadow dissolves.\n"
	.string "The nightmare falls apart like a cheap\l"
	.string "sequel…$"

MtPyre_Nightmare_Text_DarkraiLaughs:
	.string "DARKRAI sinks back into the dark,\n"
	.string "laughing.\p"
	.string "It'll be waiting the next time you fall\n"
	.string "asleep. Sleep tight!$"
