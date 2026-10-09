@ Project Grounded: ChargestoneCave_B2F (tools/grounded/maptools/chargestone.py)
ChargestoneCave_B2F_MapScripts::
	map_script MAP_SCRIPT_ON_TRANSITION, ChargestoneCave_B2F_OnTransition
	.byte 0

ChargestoneCave_B2F_EventScript_Grunt::
	trainerbattle_single TRAINER_CHARGESTONE_GRUNT_B2F, ChargestoneCave_B2F_Text_GruntIntro, ChargestoneCave_B2F_Text_GruntDefeat
	msgbox ChargestoneCave_B2F_Text_GruntPost, MSGBOX_AUTOCLOSE
	end

ChargestoneCave_B2F_EventScript_Machine::
	msgbox ChargestoneCave_B2F_Text_Machine, MSGBOX_SIGN
	end

ChargestoneCave_B2F_OnTransition:
	setflag FLAG_HIDE_CHARGESTONE_ZERAORA
	goto_if_set FLAG_SPACETIME_CHARGESTONE_DONE, ChargestoneCave_B2F_EventScript_OnTransitionEnd
	goto_if_not_defeated TRAINER_CHARGESTONE_COLRESS, ChargestoneCave_B2F_EventScript_OnTransitionEnd
	clearflag FLAG_HIDE_CHARGESTONE_ZERAORA
ChargestoneCave_B2F_EventScript_OnTransitionEnd:
	end

ChargestoneCave_B2F_EventScript_Colress::
	lock
	faceplayer
	goto_if_defeated TRAINER_CHARGESTONE_COLRESS, ChargestoneCave_B2F_EventScript_ColressAfter
	msgbox ChargestoneCave_B2F_Text_ColressIntro, MSGBOX_DEFAULT
	trainerbattle_no_intro TRAINER_CHARGESTONE_COLRESS, ChargestoneCave_B2F_Text_ColressDefeat
	msgbox ChargestoneCave_B2F_Text_ColressShutdown, MSGBOX_DEFAULT
	closemessage
	playse SE_THUNDER
	setvar VAR_0x8004, 2
	setvar VAR_0x8005, 2
	setvar VAR_0x8006, 10
	setvar VAR_0x8007, 3
	special ShakeCamera
	waitstate
	special SpawnCameraObject
	applymovement OBJ_EVENT_ID_CAMERA, ChargestoneCave_B2F_EventScript_Movement_CameraUp
	waitmovement 0
	clearflag FLAG_HIDE_CHARGESTONE_ZERAORA
	addobject LOCALID_CHARGESTONE_ZERAORA
	playse SE_M_THUNDERBOLT
	playmoncry SPECIES_ZERAORA, CRY_MODE_ENCOUNTER
	waitmoncry
	msgbox ChargestoneCave_B2F_Text_ZeraoraFree, MSGBOX_DEFAULT
	closemessage
	applymovement OBJ_EVENT_ID_CAMERA, ChargestoneCave_B2F_EventScript_Movement_CameraDown
	waitmovement 0
	special RemoveCameraObject
	release
	end

ChargestoneCave_B2F_EventScript_Movement_CameraUp:
	walk_slow_up
	walk_slow_up
	walk_slow_up
	step_end

ChargestoneCave_B2F_EventScript_Movement_CameraDown:
	walk_down
	walk_down
	walk_down
	step_end

ChargestoneCave_B2F_EventScript_ColressAfter::
	goto_if_set FLAG_SPACETIME_CHARGESTONE_DONE, ChargestoneCave_B2F_EventScript_ColressDone
	msgbox ChargestoneCave_B2F_Text_ColressAfter, MSGBOX_DEFAULT
	release
	end

ChargestoneCave_B2F_EventScript_ColressDone::
	msgbox ChargestoneCave_B2F_Text_ColressDone, MSGBOX_DEFAULT
	release
	end

ChargestoneCave_B2F_EventScript_Zeraora::
	lock
	faceplayer
	playmoncry SPECIES_ZERAORA, CRY_MODE_ENCOUNTER
	msgbox ChargestoneCave_B2F_Text_Zeraora, MSGBOX_DEFAULT
	waitmoncry
	closemessage
	setwildbattle SPECIES_ZERAORA, 93
	setflag FLAG_SYS_CTRL_OBJ_DELETE
	special BattleSetup_StartLegendaryBattle
	waitstate
	clearflag FLAG_SYS_CTRL_OBJ_DELETE
	specialvar VAR_RESULT, GetBattleOutcome
	goto_if_eq VAR_RESULT, B_OUTCOME_RAN, ChargestoneCave_B2F_EventScript_ZeraoraStays
	goto_if_eq VAR_RESULT, B_OUTCOME_PLAYER_TELEPORTED, ChargestoneCave_B2F_EventScript_ZeraoraStays
	removeobject LOCALID_CHARGESTONE_ZERAORA
	setflag FLAG_HIDE_CHARGESTONE_ZERAORA
	setflag FLAG_SPACETIME_CHARGESTONE_DONE
	msgbox ChargestoneCave_B2F_Text_CaveCalm, MSGBOX_DEFAULT
ChargestoneCave_B2F_EventScript_ZeraoraStays::
	release
	end

@ ---------------------------------------------------------------- teksten (placeholders, Jordi herschrijft ze)
ChargestoneCave_B2F_Text_GruntIntro:
	.string "The lab is through here. Please wipe\n"
	.string "your feet. The floor is load-bearing AND\l"
	.string "current-bearing.$"

ChargestoneCave_B2F_Text_GruntDefeat:
	.string "My shoes are smoking. That's new.$"

ChargestoneCave_B2F_Text_GruntPost:
	.string "When the machine is on, ZERAORA screams\n"
	.string "at a frequency only POKéMON can hear.\p"
	.string "We wear earplugs anyway. Solidarity.$"

ChargestoneCave_B2F_Text_Machine:
	.string "A floating stone wired to a laptop. The\n"
	.string "screen reads:\p"
	.string "ZERAORA OUTPUT: 98%.\n"
	.string "ZERAORA MOOD: no.\l"
	.string "ETHICS MODULE: not found.$"

ChargestoneCave_B2F_Text_ColressIntro:
	.string "COLRESS: ...Why are you looking at me\n"
	.string "like that? Do I know you?\p"
	.string "...I'm not evil? Where on earth did you\n"
	.string "hear that?\p"
	.string "Parallel dimensions. While I do not\n"
	.string "dispute the possibility, it doesn't\l"
	.string "change my current standing.\p"
	.string "Here, I am evil, and I am very good at it.\n"
	.string "My machine drains ZERAORA's current\l"
	.string "into the cave. The rocks float. The\l"
	.string "lights stay on. ZERAORA has some notes.\p"
	.string "You came all this way to switch it off?\n"
	.string "Wonderful. A control group!$"

ChargestoneCave_B2F_Text_ColressDefeat:
	.string "Fascinating. You reduced my output by\n"
	.string "exactly one hundred percent.$"

ChargestoneCave_B2F_Text_ColressShutdown:
	.string "COLRESS: The machine is overloading. It\n"
	.string "appears it relied on my POKéMON not\l"
	.string "losing.\p"
	.string "A design flaw. I'll fix it in the next\n"
	.string "dimension.\p"
	.string "Ah. And there goes the battery.$"

ChargestoneCave_B2F_Text_ZeraoraFree:
	.string "The floating stones drop a few inches\n"
	.string "all at once.\p"
	.string "Something at the back of the lab\n"
	.string "stretches, crackles, and turns to look\l"
	.string "at you.$"

ChargestoneCave_B2F_Text_ColressAfter:
	.string "COLRESS: Go on, then. It's free, it's\n"
	.string "furious, and it is standing right behind\l"
	.string "my machine.\p"
	.string "I'd love the data. Try not to become\n"
	.string "part of it.$"

ChargestoneCave_B2F_Text_ColressDone:
	.string "COLRESS: The cave runs on plain old\n"
	.string "magnetism again. Dreadfully natural.\p"
	.string "In your dimension I'm the nice one? Tell\n"
	.string "him he's wasting his potential.$"

ChargestoneCave_B2F_Text_Zeraora:
	.string "ZERAORA: Grrrah!\p"
	.string "Its fur is standing on end. So is yours.$"

ChargestoneCave_B2F_Text_CaveCalm:
	.string "The hum in the walls fades to a gentle\n"
	.string "buzz.\p"
	.string "CHARGESTONE CAVE runs on its own again.$"
