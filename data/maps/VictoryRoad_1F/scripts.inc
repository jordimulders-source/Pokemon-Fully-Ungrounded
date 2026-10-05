VictoryRoad_1F_MapScripts::
	map_script MAP_SCRIPT_ON_TRANSITION, VictoryRoad_1F_OnTransition
	.byte 0

VictoryRoad_1F_OnTransition:
	call_if_eq VAR_VICTORY_ROAD_1F_STATE, 1, VictoryRoad_1F_EventScript_SetEntranceWallyPos1
	call_if_eq VAR_VICTORY_ROAD_1F_STATE, 2, VictoryRoad_1F_EventScript_SetEntranceWallyPos2
	end

VictoryRoad_1F_EventScript_SetEntranceWallyPos1::
	setobjectxyperm LOCALID_VICTORY_ROAD_ENTRANCE_WALLY, 2, 24
	setobjectmovementtype LOCALID_VICTORY_ROAD_ENTRANCE_WALLY, MOVEMENT_TYPE_FACE_DOWN
	return

VictoryRoad_1F_EventScript_SetEntranceWallyPos2::
	setobjectxyperm LOCALID_VICTORY_ROAD_ENTRANCE_WALLY, 3, 24
	setobjectmovementtype LOCALID_VICTORY_ROAD_ENTRANCE_WALLY, MOVEMENT_TYPE_FACE_DOWN
	return

VictoryRoad_1F_EventScript_WallyBattleTrigger1::
	lockall
	setvar VAR_0x8008, 1
	addobject LOCALID_VICTORY_ROAD_ENTRANCE_WALLY
	applymovement LOCALID_VICTORY_ROAD_ENTRANCE_WALLY, VictoryRoad_1F_Movement_WallyApproachPlayer1
	waitmovement 0
	goto VictoryRoad_1F_EventScript_WallyEntranceBattle
	end

VictoryRoad_1F_EventScript_WallyBattleTrigger2::
	lockall
	setvar VAR_0x8008, 2
	addobject LOCALID_VICTORY_ROAD_ENTRANCE_WALLY
	applymovement LOCALID_VICTORY_ROAD_ENTRANCE_WALLY, VictoryRoad_1F_Movement_WallyApproachPlayer2
	waitmovement 0
	goto VictoryRoad_1F_EventScript_WallyEntranceBattle
	end

VictoryRoad_1F_EventScript_WallyEntranceBattle::
	applymovement LOCALID_PLAYER, Common_Movement_WalkInPlaceFasterDown
	waitmovement 0
	msgbox VictoryRoad_1F_Text_WallyNotGoingToLoseAnymore, MSGBOX_DEFAULT
	trainerbattle_no_intro TRAINER_WALLY_VR_1, VictoryRoad_1F_Text_WallyEntranceDefeat
	msgbox VictoryRoad_1F_Text_WallyPostEntranceBattle, MSGBOX_DEFAULT
	clearflag FLAG_HIDE_VICTORY_ROAD_ENTRANCE_WALLY
	copyobjectxytoperm LOCALID_VICTORY_ROAD_ENTRANCE_WALLY
	setflag FLAG_DEFEATED_WALLY_VICTORY_ROAD
	copyvar VAR_VICTORY_ROAD_1F_STATE, VAR_0x8008
	releaseall
	end

VictoryRoad_1F_Movement_WallyApproachPlayer1:
	walk_left
	walk_left
	walk_left
	walk_left
	walk_left
	walk_left
	walk_left
	walk_left
	walk_left
	walk_left
	walk_up
	step_end

VictoryRoad_1F_Movement_WallyApproachPlayer2:
	walk_left
	walk_left
	walk_left
	walk_left
	walk_left
	walk_left
	walk_left
	walk_left
	walk_left
	walk_up
	step_end

@ This Wally appears near the entrance once his battle is triggered and remains there until the Hall of Fame is entered
VictoryRoad_1F_EventScript_EntranceWally::
	msgbox VictoryRoad_1F_Text_WallyPostEntranceBattle, MSGBOX_NPC
	end

@ This Wally appears and remains at the exit after the Hall of Fame is entered
VictoryRoad_1F_EventScript_ExitWally::
	trainerbattle_single TRAINER_WALLY_VR_2, VictoryRoad_1F_Text_WallyIntro, VictoryRoad_1F_Text_WallyDefeat
	specialvar VAR_RESULT, ShouldTryRematchBattle
	goto_if_eq VAR_RESULT, TRUE, VictoryRoad_1F_EventScript_RematchWally
	msgbox VictoryRoad_1F_Text_WallyPostBattle, MSGBOX_AUTOCLOSE
	end

VictoryRoad_1F_EventScript_RematchWally::
	trainerbattle_rematch TRAINER_WALLY_VR_2, VictoryRoad_1F_Text_WallyIntro, VictoryRoad_1F_Text_WallyDefeat
	msgbox VictoryRoad_1F_Text_WallyPostBattle, MSGBOX_AUTOCLOSE
	end

VictoryRoad_1F_EventScript_Edgar::
	trainerbattle_single TRAINER_EDGAR, VictoryRoad_1F_Text_EdgarIntro, VictoryRoad_1F_Text_EdgarDefeat
	msgbox VictoryRoad_1F_Text_EdgarPostBattle, MSGBOX_AUTOCLOSE
	end

VictoryRoad_1F_EventScript_Dave::
	trainerbattle_single TRAINER_DAVE, VictoryRoad_1F_Text_AlbertIntro, VictoryRoad_1F_Text_AlbertDefeat
	msgbox VictoryRoad_1F_Text_AlbertPostBattle, MSGBOX_AUTOCLOSE
	end

VictoryRoad_1F_EventScript_Hope::
	trainerbattle_single TRAINER_HOPE, VictoryRoad_1F_Text_HopeIntro, VictoryRoad_1F_Text_HopeDefeat
	msgbox VictoryRoad_1F_Text_HopePostBattle, MSGBOX_AUTOCLOSE
	end

VictoryRoad_1F_EventScript_Quincy::
	trainerbattle_single TRAINER_QUINCY, VictoryRoad_1F_Text_QuincyIntro, VictoryRoad_1F_Text_QuincyDefeat
	msgbox VictoryRoad_1F_Text_QuincyPostBattle, MSGBOX_AUTOCLOSE
	end

VictoryRoad_1F_EventScript_Katelynn::
	trainerbattle_single TRAINER_KATELYNN, VictoryRoad_1F_Text_KatelynnIntro, VictoryRoad_1F_Text_KatelynnDefeat
	msgbox VictoryRoad_1F_Text_KatelynnPostBattle, MSGBOX_AUTOCLOSE
	end

VictoryRoad_1F_Text_WallyNotGoingToLoseAnymore:
	.string "WALLY: {PLAYER}! Journey much! Winnings\n"
	.string "over again.\p"
	.string "Strongness improve, my back, neck\n"
	.string "strong!\p"
	.string "Gyms me, but also RALTS. RALTS not\n"
	.string "RALTS more. WALLY not WALLY more.\p"
	.string "You lose!$"

VictoryRoad_1F_Text_WallyEntranceDefeat:
	.string "AGES FOR THE FIGHT! Pumping!$"

VictoryRoad_1F_Text_WallyPostEntranceBattle:
	.string "WALLY: {PLAYER}! Thank! Improving my\n"
	.string "life muches, happy man.\p"
	.string "Now, I find wife and kid! Bye!$"

VictoryRoad_1F_Text_WallyIntro:
	.string "WALLY: Finding wife and kid not easy.\n"
	.string "Now fight easy!$"

VictoryRoad_1F_Text_WallyDefeat:
	.string "MORE AGES, PUMP IT UP!$"

VictoryRoad_1F_Text_WallyPostBattle:
	.string "WALLY: Yay fights muches fun. Losing\n"
	.string "never old, strong come, strong stay,\l"
	.string "strong continue!$"

VictoryRoad_1F_Text_EdgarIntro:
	.string "I've made it this far a couple of times.\p"
	.string "The last stretch is so long…\p"
	.string "I'm not even sure where the exit is\n"
	.string "anymore.$"

VictoryRoad_1F_Text_EdgarDefeat:
	.string "My dream ends here. Again. For the ninth\n"
	.string "time.$"

VictoryRoad_1F_Text_EdgarPostBattle:
	.string "You made it this far. Keep going!\p"
	.string "If anyone becomes CHAMPION, it's you.\p"
	.string "I'll just live here.$"

VictoryRoad_1F_Text_AlbertIntro:
	.string "WAKE UP! Grab a brush and put a little\n"
	.string "make-up!$"

VictoryRoad_1F_Text_AlbertDefeat:
	.string "…I cry when angels deserve to die…$"

VictoryRoad_1F_Text_AlbertPostBattle:
	.string "I lost here…\p"
	.string "Trust in my self-righteous suicide…$"

VictoryRoad_1F_Text_HopeIntro:
	.string "This endless road lives up to its name.\p"
	.string "VICTORY. Or at least very long.$"

VictoryRoad_1F_Text_HopeDefeat:
	.string "Your battle style is fantastic… Mine is\n"
	.string "apparently “losing”.$"

VictoryRoad_1F_Text_HopePostBattle:
	.string "You could become CHAMPION.\p"
	.string "If you find the way out. Good luck.$"

VictoryRoad_1F_Text_QuincyIntro:
	.string "WHY DO THEY ALWAYS SEND THE POOR?!$"

VictoryRoad_1F_Text_QuincyDefeat:
	.string "…Barbarisms by Barbaras.$"

VictoryRoad_1F_Text_QuincyPostBattle:
	.string "Getting through here is the final test.\p"
	.string "Everybody's going to the party. Have a\n"
	.string "real good time.$"

VictoryRoad_1F_Text_KatelynnIntro:
	.string "FUCK YOU, I WON'T DO WHAT YOU TELL ME!$"

VictoryRoad_1F_Text_KatelynnDefeat:
	.string "…Okay. I'll do what you tell me.$"

VictoryRoad_1F_Text_KatelynnPostBattle:
	.string "Killing in the name of… Never mind.$"
