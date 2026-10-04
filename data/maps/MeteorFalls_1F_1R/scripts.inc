MeteorFalls_1F_1R_MapScripts::
	map_script MAP_SCRIPT_ON_LOAD, MeteorFalls_1F_1R_OnLoad
	.byte 0

MeteorFalls_1F_1R_OnLoad:
	call_if_set FLAG_SYS_GAME_CLEAR, MeteorFalls_1F_1R_EventScript_OpenStevensCave
	call_if_set FLAG_SYS_GAME_CLEAR, MeteorFalls_1F_1R_EventScript_OpenUnknownCave
	end

@ Project Grounded: na de Hall of Fame een grotopening naar de verborgen grot met Mewtwo (Cerulean Cave-hommage)
MeteorFalls_1F_1R_EventScript_OpenUnknownCave::
	setmetatile 12, 25, METATILE_MeteorFalls_CaveEntrance_Top, TRUE
	setmetatile 11, 26, METATILE_MeteorFalls_CaveEntrance_Left, TRUE
	setmetatile 12, 26, METATILE_MeteorFalls_CaveEntrance_Bottom, FALSE
	setmetatile 13, 26, METATILE_MeteorFalls_CaveEntrance_Right, TRUE
	return

MeteorFalls_1F_1R_EventScript_OpenStevensCave::
	setmetatile 4, 1, METATILE_MeteorFalls_CaveEntrance_Top, TRUE
	setmetatile 3, 2, METATILE_MeteorFalls_CaveEntrance_Left, TRUE
	setmetatile 4, 2, METATILE_MeteorFalls_CaveEntrance_Bottom, FALSE
	setmetatile 5, 2, METATILE_MeteorFalls_CaveEntrance_Right, TRUE
	return

MeteorFalls_1F_1R_EventScript_MagmaStealsMeteoriteScene::
	lockall
	playbgm MUS_ENCOUNTER_MAGMA, FALSE
	applymovement LOCALID_PLAYER, Common_Movement_FaceDown
	waitmovement 0
	delay 30
	applymovement LOCALID_METEOR_FALLS_MAGMA_GRUNT_1, Common_Movement_WalkInPlaceDown
	waitmovement 0
	msgbox MeteorFalls_1F_1R_Text_WithThisMeteorite, MSGBOX_DEFAULT
	closemessage
	applymovement LOCALID_METEOR_FALLS_MAGMA_GRUNT_1, Common_Movement_WalkInPlaceFasterUp
	applymovement LOCALID_METEOR_FALLS_MAGMA_GRUNT_2, Common_Movement_WalkInPlaceFasterUp
	waitmovement 0
	playse SE_PIN
	applymovement LOCALID_METEOR_FALLS_MAGMA_GRUNT_1, Common_Movement_ExclamationMark
	waitmovement 0
	applymovement LOCALID_METEOR_FALLS_MAGMA_GRUNT_1, Common_Movement_Delay48
	waitmovement 0
	msgbox MeteorFalls_1F_1R_Text_DontExpectMercyFromMagma, MSGBOX_DEFAULT
	closemessage
	applymovement LOCALID_METEOR_FALLS_MAGMA_GRUNT_1, MeteorFalls_1F_1R_Movement_MagmaGruntApproachPlayer
	waitmovement 0
	msgbox MeteorFalls_1F_1R_Text_HoldItRightThereMagma, MSGBOX_DEFAULT
	closemessage
	applymovement LOCALID_PLAYER, Common_Movement_WalkInPlaceFasterLeft
	applymovement LOCALID_METEOR_FALLS_MAGMA_GRUNT_1, Common_Movement_WalkInPlaceFasterLeft
	applymovement LOCALID_METEOR_FALLS_MAGMA_GRUNT_2, Common_Movement_WalkInPlaceFasterLeft
	waitmovement 0
	addobject LOCALID_METEOR_FALLS_ARCHIE
	addobject LOCALID_METEOR_FALLS_AQUA_GRUNT_1
	addobject LOCALID_METEOR_FALLS_AQUA_GRUNT_2
	playbgm MUS_ENCOUNTER_AQUA, FALSE
	applymovement LOCALID_METEOR_FALLS_ARCHIE, MeteorFalls_1F_1R_Movement_ArchieArrive
	applymovement LOCALID_METEOR_FALLS_AQUA_GRUNT_1, MeteorFalls_1F_1R_Movement_AquaGrunt1Arrive
	applymovement LOCALID_METEOR_FALLS_AQUA_GRUNT_2, MeteorFalls_1F_1R_Movement_AquaGrunt2Arrive
	waitmovement 0
	applymovement LOCALID_METEOR_FALLS_MAGMA_GRUNT_1, Common_Movement_WalkInPlaceFasterLeft
	applymovement LOCALID_METEOR_FALLS_MAGMA_GRUNT_2, Common_Movement_WalkInPlaceFasterLeft
	waitmovement 0
	msgbox MeteorFalls_1F_1R_Text_BeSeeingYouTeamAqua, MSGBOX_DEFAULT
	closemessage
	applymovement LOCALID_PLAYER, MeteorFalls_1F_1R_Movement_PushPlayerOutOfWay
	applymovement LOCALID_METEOR_FALLS_MAGMA_GRUNT_1, MeteorFalls_1F_1R_Movement_MagmaGrunt1Exit
	applymovement LOCALID_METEOR_FALLS_MAGMA_GRUNT_2, MeteorFalls_1F_1R_Movement_MagmaGrunt2Exit
	waitmovement 0
	removeobject LOCALID_METEOR_FALLS_MAGMA_GRUNT_1
	removeobject LOCALID_METEOR_FALLS_MAGMA_GRUNT_2
	applymovement LOCALID_METEOR_FALLS_ARCHIE, MeteorFalls_1F_1R_Movement_ArchieApproachPlayer
	waitmovement 0
	msgbox MeteorFalls_1F_1R_Text_ArchieSeenYouBefore, MSGBOX_DEFAULT
	closemessage
	applymovement LOCALID_METEOR_FALLS_AQUA_GRUNT_1, MeteorFalls_1F_1R_Movement_AquaGrunt1ApproachArchie
	applymovement LOCALID_METEOR_FALLS_AQUA_GRUNT_2, MeteorFalls_1F_1R_Movement_AquaGrunt2ApproachArchie
	waitmovement 0
	msgbox MeteorFalls_1F_1R_Text_BossWeShouldChaseMagma, MSGBOX_DEFAULT
	applymovement LOCALID_METEOR_FALLS_ARCHIE, Common_Movement_WalkInPlaceFasterDown
	waitmovement 0
	msgbox MeteorFalls_1F_1R_Text_ArchieYesNoTellingWhatMagmaWillDo, MSGBOX_DEFAULT
	applymovement LOCALID_METEOR_FALLS_ARCHIE, Common_Movement_WalkInPlaceFasterLeft
	waitmovement 0
	msgbox MeteorFalls_1F_1R_Text_ArchieFarewell, MSGBOX_DEFAULT
	closemessage
	applymovement LOCALID_METEOR_FALLS_ARCHIE, MeteorFalls_1F_1R_Movement_ArchieExit
	applymovement LOCALID_METEOR_FALLS_AQUA_GRUNT_1, MeteorFalls_1F_1R_Movement_AquaGrunt1Exit
	applymovement LOCALID_METEOR_FALLS_AQUA_GRUNT_2, MeteorFalls_1F_1R_Movement_AquaGrunt2Exit
	waitmovement 0
	fadedefaultbgm
	removeobject LOCALID_METEOR_FALLS_ARCHIE
	removeobject LOCALID_METEOR_FALLS_AQUA_GRUNT_1
	removeobject LOCALID_METEOR_FALLS_AQUA_GRUNT_2
	setflag FLAG_HIDE_ROUTE_112_TEAM_MAGMA
	setflag FLAG_MET_ARCHIE_METEOR_FALLS
	setflag FLAG_HIDE_FALLARBOR_TOWN_BATTLE_TENT_SCOTT
	setvar VAR_METEOR_FALLS_STATE, 1
	releaseall
	end

MeteorFalls_1F_1R_Movement_MagmaGruntApproachPlayer:
	walk_right
	walk_right
	walk_in_place_faster_up
	step_end

MeteorFalls_1F_1R_Movement_MagmaGrunt1Exit:
	walk_fast_up
	walk_fast_up
	walk_fast_right
	walk_fast_right
	walk_fast_right
	walk_fast_right
	walk_fast_right
	walk_fast_right
	walk_fast_right
	step_end

MeteorFalls_1F_1R_Movement_MagmaGrunt2Exit:
	walk_fast_up
	walk_fast_up
	walk_fast_up
	walk_fast_right
	walk_fast_right
	walk_fast_right
	walk_fast_right
	walk_fast_right
	walk_fast_right
	walk_fast_right
	step_end

MeteorFalls_1F_1R_Movement_ArchieArrive:
	walk_right
	walk_right
	walk_right
	walk_right
	walk_right
	walk_right
	step_end

MeteorFalls_1F_1R_Movement_AquaGrunt1Arrive:
	delay_16
	delay_16
	walk_right
	walk_right
	walk_right
	walk_right
	walk_right
	step_end

MeteorFalls_1F_1R_Movement_AquaGrunt2Arrive:
	delay_16
	delay_16
	walk_right
	walk_right
	walk_right
	walk_right
	walk_right
	step_end

MeteorFalls_1F_1R_Movement_ArchieExit:
	walk_right
	walk_right
	walk_right
	walk_right
	walk_right
	walk_right
	walk_right
	step_end

MeteorFalls_1F_1R_Movement_ArchieApproachPlayer:
	walk_right
	walk_right
	walk_up
	walk_up
	walk_in_place_faster_left
	step_end

MeteorFalls_1F_1R_Movement_AquaGrunt1Exit:
	walk_up
	walk_up
	walk_right
	walk_right
	walk_right
	walk_right
	walk_right
	walk_right
	walk_right
	step_end

MeteorFalls_1F_1R_Movement_AquaGrunt1ApproachArchie:
	walk_right
	walk_right
	walk_right
	walk_in_place_faster_up
	step_end

MeteorFalls_1F_1R_Movement_AquaGrunt2Exit:
	walk_up
	walk_up
	walk_up
	walk_right
	walk_right
	walk_right
	walk_right
	walk_right
	walk_right
	walk_right
	step_end

MeteorFalls_1F_1R_Movement_AquaGrunt2ApproachArchie:
	walk_right
	walk_right
	walk_right
	walk_in_place_faster_up
	step_end

MeteorFalls_1F_1R_Movement_PushPlayerOutOfWay:
	walk_in_place_faster_down
	delay_4
	walk_in_place_faster_right
	lock_facing_direction
	walk_left
	unlock_facing_direction
	face_right
	step_end

MeteorFalls_1F_1R_EventScript_ProfCozmo::
	lock
	faceplayer
	goto_if_set FLAG_MET_PROF_COZMO, MeteorFalls_1F_1R_EventScript_MetCozmo
	setflag FLAG_MET_PROF_COZMO
	msgbox MeteorFalls_1F_1R_Text_MeetProfCozmo, MSGBOX_DEFAULT
	release
	end

MeteorFalls_1F_1R_EventScript_MetCozmo::
	msgbox MeteorFalls_1F_1R_Text_WhatsTeamMagmaDoingAtMtChimney, MSGBOX_DEFAULT
	release
	end

MeteorFalls_1F_1R_Text_WithThisMeteorite:
	.string "Hehehe! With this METEORITE, the\n"
	.string "peppers of MT. CHIMNEY will…$"

MeteorFalls_1F_1R_Text_DontExpectMercyFromMagma:
	.string "Heh?\p"
	.string "Get in MAGMA's way and you'll taste the\n"
	.string "heat!$"

MeteorFalls_1F_1R_Text_HoldItRightThereMagma:
	.string "Hold it right there, MAGMA!\p"
	.string "Keep your chili off the world!$"

MeteorFalls_1F_1R_Text_BeSeeingYouTeamAqua:
	.string "Hehehe! Even AQUA shows up!\p"
	.string "Too much trouble. We've got the\n"
	.string "METEORITE!\p"
	.string "Off to MT. CHIMNEY! See you, you\n"
	.string "bubble-heads!$"

MeteorFalls_1F_1R_Text_ArchieSeenYouBefore:
	.string "ARCHIE: Didn't I see you at the MUSEUM?\p"
	.string "{PLAYER}, is it? Odd kid.\p"
	.string "TEAM MAGMA are fanatics. They sell hot\n"
	.string "sauce.\p"
	.string "MAXIE wants GROUDON to grow the\n"
	.string "ultimate pepper.\p"
	.string "Disgusting. We sell sparkling water.\n"
	.string "Classy.$"

MeteorFalls_1F_1R_Text_BossWeShouldChaseMagma:
	.string "BOSS, we should chase MAGMA…\p"
	.string "After this SPA.$"

MeteorFalls_1F_1R_Text_ArchieYesNoTellingWhatMagmaWillDo:
	.string "ARCHIE: Yes, yes! To MT. CHIMNEY!\p"
	.string "Before MAGMA sets the market on fire!$"

MeteorFalls_1F_1R_Text_ArchieFarewell:
	.string "ARCHIE: Keep an eye on MAGMA, {PLAYER}.\p"
	.string "And stay hydrated. Farewell!$"

MeteorFalls_1F_1R_Text_MeetProfCozmo:
	.string "I… I'm COZMO… A PROFESSOR…\p"
	.string "TEAM MAGMA asked me to guide them to\n"
	.string "METEOR FALLS…\p"
	.string "They promised hot sauce. They tricked\n"
	.string "me. They took my METEORITE…\p"
	.string "Then TEAM AQUA showed up with\n"
	.string "sparkling water.\p"
	.string "I don't understand any of this.\p"
	.string "What will MAGMA do with the METEORITE\n"
	.string "at MT. CHIMNEY?$"

MeteorFalls_1F_1R_Text_WhatsTeamMagmaDoingAtMtChimney:
	.string "PROF. COZMO: That TEAM MAGMA…\p"
	.string "What will they do with the METEORITE at\n"
	.string "MT. CHIMNEY?\p"
	.string "Grow peppers? On a volcano?$"

@ Project Grounded: Wally wacht bij de ingang en daagt je uit.
MeteorFalls_1F_1R_EventScript_WallyApproachUpper::
	lockall
	call MeteorFalls_1F_1R_EventScript_WallyNotices
	applymovement LOCALID_METEOR_FALLS_WALLY, MeteorFalls_1F_1R_Movement_WallyApproachUpper
	waitmovement 0
	goto MeteorFalls_1F_1R_EventScript_WallyBattle
	end

MeteorFalls_1F_1R_EventScript_WallyApproachLower::
	lockall
	call MeteorFalls_1F_1R_EventScript_WallyNotices
	applymovement LOCALID_METEOR_FALLS_WALLY, MeteorFalls_1F_1R_Movement_WallyApproachLower
	waitmovement 0
	goto MeteorFalls_1F_1R_EventScript_WallyBattle
	end

MeteorFalls_1F_1R_EventScript_WallyNotices::
	applymovement LOCALID_PLAYER, Common_Movement_WalkInPlaceFasterLeft
	waitmovement 0
	playse SE_PIN
	applymovement LOCALID_METEOR_FALLS_WALLY, Common_Movement_ExclamationMark
	waitmovement 0
	return

MeteorFalls_1F_1R_EventScript_WallyBattle::
	msgbox MeteorFalls_1F_1R_Text_WallyFallOfMeteor, MSGBOX_DEFAULT
	closemessage
	applymovement LOCALID_METEOR_FALLS_WALLY, MeteorFalls_1F_1R_Movement_WallySpin
	waitmovement 0
	msgbox MeteorFalls_1F_1R_Text_WallyVeryBeaut, MSGBOX_DEFAULT
	trainerbattle_no_intro TRAINER_WALLY_METEOR_FALLS, MeteorFalls_1F_1R_Text_WallyDefeat
	msgbox MeteorFalls_1F_1R_Text_WallyPostBattle, MSGBOX_DEFAULT
	closemessage
	applymovement LOCALID_METEOR_FALLS_WALLY, MeteorFalls_1F_1R_Movement_WallyExit
	waitmovement 0
	removeobject LOCALID_METEOR_FALLS_WALLY
	setflag FLAG_HIDE_METEOR_FALLS_WALLY
	setvar VAR_WALLY_METEOR_FALLS_STATE, 1
	releaseall
	end

MeteorFalls_1F_1R_Movement_WallyApproachUpper:
	walk_right
	walk_up
	walk_right
	face_right
	step_end

MeteorFalls_1F_1R_Movement_WallyApproachLower:
	walk_right
	walk_right
	face_right
	step_end

MeteorFalls_1F_1R_Movement_WallySpin:
	face_down
	delay_8
	face_left
	delay_8
	face_up
	delay_8
	face_right
	delay_8
	face_down
	delay_8
	face_left
	delay_8
	face_up
	delay_8
	face_right
	step_end

MeteorFalls_1F_1R_Movement_WallyExit:
	walk_fast_left
	walk_fast_left
	walk_fast_left
	walk_fast_left
	step_end

MeteorFalls_1F_1R_Text_WallyFallOfMeteor:
	.string "WALLY: {PLAYER}!\n"
	.string "Fall of Meteor.$"

MeteorFalls_1F_1R_Text_WallyVeryBeaut:
	.string "Wow! Very beaut!\n"
	.string "Train much team.\p"
	.string "Timing of battle appear now!$"

MeteorFalls_1F_1R_Text_WallyDefeat:
	.string "Wow… {PLAYER} strong!$"

MeteorFalls_1F_1R_Text_WallyPostBattle:
	.string "WALLY: Oh thank! Realizations moves,\n"
	.string "hmmmm planning more and more.\p"
	.string "Think become good!$"
