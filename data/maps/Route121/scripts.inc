Route121_MapScripts::
	map_script MAP_SCRIPT_ON_TRANSITION, Route121_OnTransition
	.byte 0

@ Project Grounded: Rocket-sidequest. De dief staat (verborgen) in de deur van de Safari Zone en komt pas tevoorschijn
@ als de coord-trigger voor de deur afgaat (VAR_ROCKET_QUEST 0 -> 1).
Route121_OnTransition:
	setflag FLAG_HIDE_ROUTE121_ROCKET_RUNNER
	end

Route121_EventScript_RocketRunner::
	lockall
	opendoor 37, 5
	waitdooranim
	clearflag FLAG_HIDE_ROUTE121_ROCKET_RUNNER
	addobject LOCALID_ROUTE121_ROCKET_RUNNER
	playse SE_M_DOUBLE_SLAP
	applymovement LOCALID_PLAYER, Route121_Movement_PlayerKnockedBack
	waitmovement 0
	applymovement LOCALID_ROUTE121_ROCKET_RUNNER, Route121_Movement_RunnerBumps
	waitmovement 0
	closedoor 37, 5
	waitdooranim
	playbgm MUS_RG_ENCOUNTER_ROCKET, FALSE
	applymovement LOCALID_ROUTE121_ROCKET_RUNNER, Common_Movement_ExclamationMark
	waitmovement 0
	msgbox Route121_Text_RocketRunner, MSGBOX_DEFAULT
	closemessage
	applymovement LOCALID_ROUTE121_ROCKET_RUNNER, Route121_Movement_RunnerFlees
	waitmovement 0
	removeobject LOCALID_ROUTE121_ROCKET_RUNNER
	setflag FLAG_HIDE_ROUTE121_ROCKET_RUNNER
	fadedefaultbgm
	setvar VAR_ROCKET_QUEST, 1
	releaseall
	end

Route121_Movement_PlayerKnockedBack:
	lock_facing_direction
	walk_faster_down
	unlock_facing_direction
	step_end

Route121_Movement_RunnerBumps:
	walk_faster_down
	step_end

Route121_Movement_RunnerFlees:
	walk_faster_left
	walk_faster_left
	walk_faster_left
	walk_faster_up
	walk_faster_left
	walk_faster_left
	walk_faster_left
	walk_faster_left
	walk_faster_left
	walk_faster_left
	walk_faster_left
	walk_faster_left
	step_end

Route121_Text_RocketRunner:
	.string "Outta my way, kid! I'm on a very\n"
	.string "important, very legal errand!\p"
	.string "These? These aren't the ZONE KEYS\n"
	.string "to the new Safari Zones. No sir.\p"
	.string "They're the keys to my condo.\n"
	.string "My secret jungle condo.\p"
	.string "Inside a tree. Like a normal guy.\n"
	.string "With a normal condo.\p"
	.string "...I've said too much. Bye!$"


Route121_EventScript_Woman::
	msgbox Route121_Text_AheadLoomsMtPyre, MSGBOX_NPC
	end

Route121_EventScript_MtPyrePierSign::
	msgbox Route121_Text_MtPyrePierSign, MSGBOX_SIGN
	end

Route121_EventScript_SafariZoneSign::
	msgbox Route121_Text_SafariZoneSign, MSGBOX_SIGN
	end

Route121_EventScript_AquaGruntsMoveOut::
	lockall
	playbgm MUS_ENCOUNTER_AQUA, FALSE
	applymovement LOCALID_ROUTE121_GRUNT_2, Common_Movement_WalkInPlaceRight
	waitmovement 0
	msgbox Route121_Text_OkayMoveOutToMtPyre, MSGBOX_DEFAULT
	closemessage
	applymovement LOCALID_ROUTE121_GRUNT_1, Route121_Movement_Grunt1Exit
	applymovement LOCALID_ROUTE121_GRUNT_2, Route121_Movement_Grunt2Exit
	applymovement LOCALID_ROUTE121_GRUNT_3, Route121_Movement_Grunt3Exit
	waitmovement 0
	fadedefaultbgm
	removeobject LOCALID_ROUTE121_GRUNT_1
	removeobject LOCALID_ROUTE121_GRUNT_2
	removeobject LOCALID_ROUTE121_GRUNT_3
	setvar VAR_ROUTE121_STATE, 1
	releaseall
	end

Route121_Movement_Grunt1Exit:
	walk_down
	walk_down
	walk_down
	walk_down
	walk_down
	walk_down
	walk_down
	walk_down
	step_end

Route121_Movement_Grunt2Exit:
	walk_down
	walk_down
	walk_down
	walk_down
	walk_down
	walk_down
	walk_down
	walk_down
	step_end

Route121_Movement_Grunt3Exit:
	walk_down
	walk_down
	walk_down
	walk_down
	walk_down
	walk_down
	walk_down
	walk_down
	step_end

Route121_EventScript_Vanessa::
	trainerbattle_single TRAINER_VANESSA, Route121_Text_VanessaIntro, Route121_Text_VanessaDefeat
	msgbox Route121_Text_VanessaPostBattle, MSGBOX_AUTOCLOSE
	end

Route121_EventScript_Walter::
	trainerbattle_single TRAINER_WALTER_1, Route121_Text_WalterIntro, Route121_Text_WalterDefeat, Route121_EventScript_RegisterWalter
	specialvar VAR_RESULT, ShouldTryRematchBattle
	goto_if_eq VAR_RESULT, TRUE, Route121_EventScript_RematchWalter
	msgbox Route121_Text_WalterPostBattle, MSGBOX_DEFAULT
	release
	end

Route121_EventScript_RegisterWalter::
	special PlayerFaceTrainerAfterBattle
	waitmovement 0
	msgbox Route121_Text_WalterRegister, MSGBOX_DEFAULT
	register_matchcall TRAINER_WALTER_1
	release
	end

Route121_EventScript_RematchWalter::
	trainerbattle_rematch TRAINER_WALTER_1, Route121_Text_WalterRematchIntro, Route121_Text_WalterRematchDefeat
	msgbox Route121_Text_WalterPostRematch, MSGBOX_AUTOCLOSE
	end

Route121_EventScript_Tammy::
	trainerbattle_single TRAINER_TAMMY, Route121_Text_TammyIntro, Route121_Text_TammyDefeat
	msgbox Route121_Text_TammyPostBattle, MSGBOX_AUTOCLOSE
	end

Route121_EventScript_Kate::
	trainerbattle_double TRAINER_KATE_AND_JOY, Route121_Text_KateIntro, Route121_Text_KateDefeat, Route121_Text_KateNotEnoughMons
	msgbox Route121_Text_KatePostBattle, MSGBOX_AUTOCLOSE
	end

Route121_EventScript_Joy::
	trainerbattle_double TRAINER_KATE_AND_JOY, Route121_Text_JoyIntro, Route121_Text_JoyDefeat, Route121_Text_JoyNotEnoughMons
	msgbox Route121_Text_JoyPostBattle, MSGBOX_AUTOCLOSE
	end

Route121_EventScript_Jessica::
	trainerbattle_single TRAINER_JESSICA_1, Route121_Text_JessicaIntro, Route121_Text_JessicaDefeat, Route121_EventScript_RegisterJessica
	specialvar VAR_RESULT, ShouldTryRematchBattle
	goto_if_eq VAR_RESULT, TRUE, Route121_EventScript_RematchJessica
	msgbox Route121_Text_JessicaPostBattle, MSGBOX_DEFAULT
	release
	end

Route121_EventScript_RegisterJessica::
	special PlayerFaceTrainerAfterBattle
	waitmovement 0
	msgbox Route121_Text_JessicaRegister, MSGBOX_DEFAULT
	register_matchcall TRAINER_JESSICA_1
	release
	end

Route121_EventScript_RematchJessica::
	trainerbattle_rematch TRAINER_JESSICA_1, Route121_Text_JessicaRematchIntro, Route121_Text_JessicaRematchDefeat
	msgbox Route121_Text_JessicaPostRematch, MSGBOX_AUTOCLOSE
	end

Route121_EventScript_Cale::
	trainerbattle_single TRAINER_CALE, Route121_Text_CaleIntro, Route121_Text_CaleDefeat
	msgbox Route121_Text_CalePostBattle, MSGBOX_AUTOCLOSE
	end

Route121_EventScript_Myles::
	trainerbattle_single TRAINER_MYLES, Route121_Text_MylesIntro, Route121_Text_MylesDefeat
	msgbox Route121_Text_MylesPostBattle, MSGBOX_AUTOCLOSE
	end

Route121_EventScript_Pat::
	trainerbattle_single TRAINER_PAT, Route121_Text_PatIntro, Route121_Text_PatDefeat
	msgbox Route121_Text_PatPostBattle, MSGBOX_AUTOCLOSE
	end

Route121_EventScript_Marcel::
	trainerbattle_single TRAINER_MARCEL, Route121_Text_MarcelIntro, Route121_Text_MarcelDefeat
	msgbox Route121_Text_MarcelPostBattle, MSGBOX_AUTOCLOSE
	end

Route121_EventScript_Cristin::
	trainerbattle_single TRAINER_CRISTIN_1, Route121_Text_CristinIntro, Route121_Text_CristinDefeat, Route121_EventScript_RegisterCristin
	specialvar VAR_RESULT, ShouldTryRematchBattle
	goto_if_eq VAR_RESULT, TRUE, Route121_EventScript_RematchCristin
	msgbox Route121_Text_CristinPostBattle, MSGBOX_DEFAULT
	release
	end

Route121_EventScript_RegisterCristin::
	special PlayerFaceTrainerAfterBattle
	waitmovement 0
	msgbox Route121_Text_CristinRegister, MSGBOX_DEFAULT
	register_matchcall TRAINER_CRISTIN_1
	release
	end

Route121_EventScript_RematchCristin::
	trainerbattle_rematch TRAINER_CRISTIN_1, Route121_Text_CristinRematchIntro, Route121_Text_CristinRematchDefeat
	msgbox Route121_Text_CristinPostRematch, MSGBOX_AUTOCLOSE
	end

Route121_Text_OkayMoveOutToMtPyre:
	.string "Okay! We move out to MT. PYRE!\p"
	.string "Bring the chili!$"

Route121_Text_AheadLoomsMtPyre:
	.string "Ahead looms MT. PYRE…\p"
	.string "A monument to the spirits of departed\n"
	.string "POKéMON…\p"
	.string "And a great view. Bring a snack.$"

Route121_Text_MtPyrePierSign:
	.string "MT. PYRE PIER\p"
	.string "…The sign is old and worn out. Someone\n"
	.string "scratched into it:\p"
	.string "“There came a spooky bunch… BOO!”$"

Route121_Text_SafariZoneSign:
	.string "“Filled with rare POKéMON!”\n"
	.string "SAFARI ZONE\p"
	.string "Enter at your own risk. The POKéMON are\n"
	.string "dangerous.$"

@ extra_fights { (tools/grounded/maptools/extra_fights.py)
Route121_EventScript_EF_MitchRoute121::
	trainerbattle_single TRAINER_MITCH_ROUTE_121, Route121_Text_EF_MitchRoute121Intro, Route121_Text_EF_MitchRoute121Defeat
	msgbox Route121_Text_EF_MitchRoute121PostBattle, MSGBOX_AUTOCLOSE
	end

Route121_Text_EF_MitchRoute121Intro:
	.string "MITCH: You again. Okay. Breathe.\p"
	.string "Last week I played for 12 people.\n"
	.string "Eleven were Zigzagoon.\p"
	.string "The twelfth asked for a refund.\n"
	.string "Let's battle before I overthink it.$"

Route121_Text_EF_MitchRoute121Defeat:
	.string "Drop. Silence. Story of my life.$"

Route121_Text_EF_MitchRoute121PostBattle:
	.string "MITCH: Next gig: VICTORY ROAD.\n"
	.string "Terrible acoustics. Perfect.\p"
	.string "Nobody will hear me fail.$"

@ }
