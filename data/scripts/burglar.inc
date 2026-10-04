@ Project Grounded: de Burglar (SIMON) die af en toe uit een huis in de steden komt. Gestart door
@ Burglar_TryTriggerOnStep (src/burglar.c) als de speler vlak voor het huis loopt. Teksten: data/text/burglar.inc.
@ VAR_0x8004 = stad (0 Mauville, 1 Slateport, 2 Lilycove, 3 Rustboro, 4 Verdanturf, 5 Fallarbor, 6 Petalburg),
@ VAR_0x8005/0x8006 = deur, VAR_0x8007 = sterkte (0-4), VAR_0x8008 = aantal keer al verslagen.

Burglar_EventScript_Scene::
	lockall
	special Burglar_SetupVars
	opendoor VAR_0x8005, VAR_0x8006
	waitdooranim
	special Burglar_SpawnThief
	applymovement LOCALID_BURGLAR_THIEF, Burglar_Movement_StepOut
	waitmovement LOCALID_BURGLAR_THIEF
	closedoor VAR_0x8005, VAR_0x8006
	waitdooranim
	playse SE_PIN
	applymovement LOCALID_BURGLAR_THIEF, Common_Movement_ExclamationMark
	waitmovement LOCALID_BURGLAR_THIEF
	playbgm MUS_ENCOUNTER_SUSPICIOUS, FALSE
	special Burglar_ThiefApproachPlayer
	waitmovement LOCALID_BURGLAR_THIEF
	call_if_ne VAR_0x8008, 0, Burglar_EventScript_Again
	call_if_eq VAR_0x8004, 0, Burglar_EventScript_Intro0
	call_if_eq VAR_0x8004, 1, Burglar_EventScript_Intro1
	call_if_eq VAR_0x8004, 2, Burglar_EventScript_Intro2
	call_if_eq VAR_0x8004, 3, Burglar_EventScript_Intro3
	call_if_eq VAR_0x8004, 4, Burglar_EventScript_Intro4
	call_if_eq VAR_0x8004, 5, Burglar_EventScript_Intro5
	call_if_eq VAR_0x8004, 6, Burglar_EventScript_Intro6
	switch VAR_0x8007
	case 0, Burglar_EventScript_Battle1
	case 1, Burglar_EventScript_Battle2
	case 2, Burglar_EventScript_Battle3
	case 3, Burglar_EventScript_Battle4
	goto Burglar_EventScript_Battle5
	end

Burglar_EventScript_Battle1::
	cleartrainerflag TRAINER_BURGLAR_1
	trainerbattle_no_intro TRAINER_BURGLAR_1, Burglar_Text_Defeat
	goto Burglar_EventScript_AfterBattle
	end

Burglar_EventScript_Battle2::
	cleartrainerflag TRAINER_BURGLAR_2
	trainerbattle_no_intro TRAINER_BURGLAR_2, Burglar_Text_Defeat
	goto Burglar_EventScript_AfterBattle
	end

Burglar_EventScript_Battle3::
	cleartrainerflag TRAINER_BURGLAR_3
	trainerbattle_no_intro TRAINER_BURGLAR_3, Burglar_Text_Defeat
	goto Burglar_EventScript_AfterBattle
	end

Burglar_EventScript_Battle4::
	cleartrainerflag TRAINER_BURGLAR_4
	trainerbattle_no_intro TRAINER_BURGLAR_4, Burglar_Text_Defeat
	goto Burglar_EventScript_AfterBattle
	end

Burglar_EventScript_Battle5::
	cleartrainerflag TRAINER_BURGLAR_5
	trainerbattle_no_intro TRAINER_BURGLAR_5, Burglar_Text_Defeat
	goto Burglar_EventScript_AfterBattle
	end

Burglar_EventScript_AfterBattle::
	special Burglar_SetupVars
	special Burglar_RestoreThief
	applymovement LOCALID_BURGLAR_THIEF, Burglar_Movement_Stunned
	waitmovement LOCALID_BURGLAR_THIEF
	msgbox Burglar_Text_Stunned, MSGBOX_DEFAULT
	opendoor VAR_0x8005, VAR_0x8006
	waitdooranim
	special Burglar_SpawnResident
	applymovement LOCALID_BURGLAR_RESIDENT, Burglar_Movement_StepOut
	waitmovement LOCALID_BURGLAR_RESIDENT
	closedoor VAR_0x8005, VAR_0x8006
	waitdooranim
	playse SE_PIN
	applymovement LOCALID_BURGLAR_RESIDENT, Common_Movement_ExclamationMark
	waitmovement LOCALID_BURGLAR_RESIDENT
	special Burglar_ResidentApproachThief
	waitmovement LOCALID_BURGLAR_RESIDENT
	call_if_eq VAR_0x8004, 0, Burglar_EventScript_Resident0
	call_if_eq VAR_0x8004, 1, Burglar_EventScript_Resident1
	call_if_eq VAR_0x8004, 2, Burglar_EventScript_Resident2
	call_if_eq VAR_0x8004, 3, Burglar_EventScript_Resident3
	call_if_eq VAR_0x8004, 4, Burglar_EventScript_Resident4
	call_if_eq VAR_0x8004, 5, Burglar_EventScript_Resident5
	call_if_eq VAR_0x8004, 6, Burglar_EventScript_Resident6
	msgbox Burglar_Text_Flee, MSGBOX_DEFAULT
	special Burglar_ThiefFlee
	waitmovement LOCALID_BURGLAR_THIEF
	setvar VAR_0x8004, LOCALID_BURGLAR_THIEF
	special Burglar_RemoveActor
	special Burglar_SetupVars
	fadedefaultbgm
	msgbox Burglar_Text_Dropped, MSGBOX_DEFAULT
	goto_if_eq VAR_0x8007, 4, Burglar_EventScript_BigNugget
	giveitem ITEM_NUGGET
	goto Burglar_EventScript_Thanks
	end

Burglar_EventScript_BigNugget::
	giveitem ITEM_BIG_NUGGET
	goto Burglar_EventScript_Thanks
	end

Burglar_EventScript_Thanks::
	applymovement LOCALID_BURGLAR_RESIDENT, Burglar_Movement_FaceAround
	waitmovement LOCALID_BURGLAR_RESIDENT
	msgbox Burglar_Text_Thanks, MSGBOX_DEFAULT
	special Burglar_ResidentGoHome
	waitmovement LOCALID_BURGLAR_RESIDENT
	opendoor VAR_0x8005, VAR_0x8006
	waitdooranim
	applymovement LOCALID_BURGLAR_RESIDENT, Burglar_Movement_StepIn
	waitmovement LOCALID_BURGLAR_RESIDENT
	setvar VAR_0x8004, LOCALID_BURGLAR_RESIDENT
	special Burglar_RemoveActor
	special Burglar_SetupVars
	closedoor VAR_0x8005, VAR_0x8006
	waitdooranim
	special Burglar_Finish
	releaseall
	end

Burglar_EventScript_Again::
	msgbox Burglar_Text_Again, MSGBOX_DEFAULT
	return

Burglar_EventScript_Intro0::
	msgbox Burglar_Text_Intro0, MSGBOX_DEFAULT
	return
Burglar_EventScript_Intro1::
	msgbox Burglar_Text_Intro1, MSGBOX_DEFAULT
	return
Burglar_EventScript_Intro2::
	msgbox Burglar_Text_Intro2, MSGBOX_DEFAULT
	return
Burglar_EventScript_Intro3::
	msgbox Burglar_Text_Intro3, MSGBOX_DEFAULT
	return
Burglar_EventScript_Intro4::
	msgbox Burglar_Text_Intro4, MSGBOX_DEFAULT
	return
Burglar_EventScript_Intro5::
	msgbox Burglar_Text_Intro5, MSGBOX_DEFAULT
	return
Burglar_EventScript_Intro6::
	msgbox Burglar_Text_Intro6, MSGBOX_DEFAULT
	return

Burglar_EventScript_Resident0::
	msgbox Burglar_Text_Resident0, MSGBOX_DEFAULT
	return
Burglar_EventScript_Resident1::
	msgbox Burglar_Text_Resident1, MSGBOX_DEFAULT
	return
Burglar_EventScript_Resident2::
	msgbox Burglar_Text_Resident2, MSGBOX_DEFAULT
	return
Burglar_EventScript_Resident3::
	msgbox Burglar_Text_Resident3, MSGBOX_DEFAULT
	return
Burglar_EventScript_Resident4::
	msgbox Burglar_Text_Resident4, MSGBOX_DEFAULT
	return
Burglar_EventScript_Resident5::
	msgbox Burglar_Text_Resident5, MSGBOX_DEFAULT
	return
Burglar_EventScript_Resident6::
	msgbox Burglar_Text_Resident6, MSGBOX_DEFAULT
	return

Burglar_Movement_StepOut:
	walk_down
	step_end

Burglar_Movement_StepIn:
	walk_up
	step_end

Burglar_Movement_Stunned:
	emote_question_mark
	delay_16
	walk_in_place_faster_left
	walk_in_place_faster_right
	walk_in_place_faster_left
	walk_in_place_faster_right
	face_player
	step_end

Burglar_Movement_FaceAround:
	face_player
	step_end
