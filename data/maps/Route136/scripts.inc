Route136_MapScripts::
	map_script MAP_SCRIPT_ON_TRANSITION, Route136_OnTransition
	.byte 0

Route136_OnTransition:
	checkplayergender
	goto_if_eq VAR_RESULT, MALE, Route136_EventScript_SetMayGfx
	setvar VAR_OBJ_GFX_ID_0, OBJ_EVENT_GFX_RIVAL_BRENDAN_NORMAL
	end

Route136_EventScript_SetMayGfx::
	setvar VAR_OBJ_GFX_ID_0, OBJ_EVENT_GFX_RIVAL_MAY_NORMAL
	end

@ ---------------------------------------------------------------- rivaal bij de bergpas
Route136_EventScript_RivalTrigger::
	goto_if_set FLAG_HIDE_ROUTE136_RIVAL, Route136_EventScript_RivalTriggerEnd
	lockall
	applymovement OBJ_EVENT_ID_PLAYER, Common_Movement_FaceUp
	waitmovement 0
	goto Route136_EventScript_RivalTalk
Route136_EventScript_RivalTriggerEnd::
	end

Route136_EventScript_Rival::
	lock
	faceplayer
Route136_EventScript_RivalTalk::
	checkplayergender
	goto_if_eq VAR_RESULT, MALE, Route136_EventScript_May
	goto Route136_EventScript_Brendan
	end

Route136_EventScript_May::
	playbgm MUS_ENCOUNTER_MAY, TRUE
	msgbox Route136_Text_MayIntro, MSGBOX_DEFAULT
	switch VAR_STARTER_MON
	case 0, Route136_EventScript_MayTreecko
	case 1, Route136_EventScript_MayTorchic
	case 2, Route136_EventScript_MayMudkip
	end

Route136_EventScript_MayTreecko::
	trainerbattle_no_intro TRAINER_MAY_ROUTE_136_TREECKO, Route136_Text_MayDefeat
	goto Route136_EventScript_MayAfter
	end

Route136_EventScript_MayTorchic::
	trainerbattle_no_intro TRAINER_MAY_ROUTE_136_TORCHIC, Route136_Text_MayDefeat
	goto Route136_EventScript_MayAfter
	end

Route136_EventScript_MayMudkip::
	trainerbattle_no_intro TRAINER_MAY_ROUTE_136_MUDKIP, Route136_Text_MayDefeat
	goto Route136_EventScript_MayAfter
	end

Route136_EventScript_MayAfter::
	msgbox Route136_Text_MayPostBattle, MSGBOX_DEFAULT
	goto Route136_EventScript_RivalLeaves
	end

Route136_EventScript_Brendan::
	playbgm MUS_ENCOUNTER_BRENDAN, TRUE
	msgbox Route136_Text_BrendanIntro, MSGBOX_DEFAULT
	switch VAR_STARTER_MON
	case 0, Route136_EventScript_BrendanTreecko
	case 1, Route136_EventScript_BrendanTorchic
	case 2, Route136_EventScript_BrendanMudkip
	end

Route136_EventScript_BrendanTreecko::
	trainerbattle_no_intro TRAINER_BRENDAN_ROUTE_136_TREECKO, Route136_Text_BrendanDefeat
	goto Route136_EventScript_BrendanAfter
	end

Route136_EventScript_BrendanTorchic::
	trainerbattle_no_intro TRAINER_BRENDAN_ROUTE_136_TORCHIC, Route136_Text_BrendanDefeat
	goto Route136_EventScript_BrendanAfter
	end

Route136_EventScript_BrendanMudkip::
	trainerbattle_no_intro TRAINER_BRENDAN_ROUTE_136_MUDKIP, Route136_Text_BrendanDefeat
	goto Route136_EventScript_BrendanAfter
	end

Route136_EventScript_BrendanAfter::
	msgbox Route136_Text_BrendanPostBattle, MSGBOX_DEFAULT
	goto Route136_EventScript_RivalLeaves
	end

Route136_EventScript_RivalLeaves::
	closemessage
	applymovement LOCALID_ROUTE136_RIVAL, Route136_Movement_RivalLeaves
	waitmovement 0
	removeobject LOCALID_ROUTE136_RIVAL
	setflag FLAG_HIDE_ROUTE136_RIVAL
	savebgm MUS_DUMMY
	fadedefaultbgm
	release
	end

Route136_Movement_RivalLeaves:
	walk_up
	walk_up
	walk_up
	step_end

@ ---------------------------------------------------------------- Keccles (onzichtbaar, Devon Scope)
Route136_EventScript_Keccles::
	lock
	faceplayer
	checkitem ITEM_DEVON_SCOPE
	goto_if_eq VAR_RESULT, TRUE, Route136_EventScript_KecclesAskScope
	msgbox Route136_Text_SomethingUnseeable, MSGBOX_DEFAULT
	release
	end

Route136_EventScript_KecclesAskScope::
	msgbox Route136_Text_UseDevonScope, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, YES, Route136_EventScript_KecclesReveal
	release
	end

Route136_EventScript_KecclesReveal::
	msgbox Route136_Text_UsedDevonScope, MSGBOX_DEFAULT
	closemessage
	applymovement VAR_LAST_TALKED, Movement_KecleonAppears
	waitmovement 0
	waitse
	playmoncry SPECIES_KECLEON, CRY_MODE_ENCOUNTER
	delay 40
	waitmoncry
	msgbox Route136_Text_KecclesIntro, MSGBOX_DEFAULT
	trainerbattle_no_intro TRAINER_KECCLES_3, Route136_Text_KecclesDefeat
	msgbox Route136_Text_KecclesPostBattle, MSGBOX_DEFAULT
	closemessage
	applymovement VAR_LAST_TALKED, Route136_Movement_KecclesFlee
	waitmovement 0
	removeobject VAR_LAST_TALKED
	setflag FLAG_HIDE_ROUTE136_KECCLES
	release
	end

Route136_Movement_KecclesFlee:
	walk_down
	walk_down
	step_end

@ ---------------------------------------------------------------- trainers
Route136_EventScript_Otto::
	trainerbattle_single TRAINER_OTTO, Route136_Text_OttoIntro, Route136_Text_OttoDefeat
	msgbox Route136_Text_OttoPostBattle, MSGBOX_AUTOCLOSE
	end

Route136_EventScript_Helmut::
	trainerbattle_single TRAINER_HELMUT, Route136_Text_HelmutIntro, Route136_Text_HelmutDefeat
	msgbox Route136_Text_HelmutPostBattle, MSGBOX_AUTOCLOSE
	end

Route136_EventScript_Connor::
	trainerbattle_single TRAINER_CONNOR, Route136_Text_ConnorIntro, Route136_Text_ConnorDefeat
	msgbox Route136_Text_ConnorPostBattle, MSGBOX_AUTOCLOSE
	end

Route136_EventScript_Sigrid::
	trainerbattle_single TRAINER_SIGRID, Route136_Text_SigridIntro, Route136_Text_SigridDefeat
	msgbox Route136_Text_SigridPostBattle, MSGBOX_AUTOCLOSE
	end

Route136_EventScript_Rafael::
	trainerbattle_single TRAINER_RAFAEL, Route136_Text_RafaelIntro, Route136_Text_RafaelDefeat
	msgbox Route136_Text_RafaelPostBattle, MSGBOX_AUTOCLOSE
	end

Route136_EventScript_Hakon::
	trainerbattle_single TRAINER_HAKON, Route136_Text_HakonIntro, Route136_Text_HakonDefeat
	msgbox Route136_Text_HakonPostBattle, MSGBOX_AUTOCLOSE
	end

@ ---------------------------------------------------------------- teksten (placeholders voor Jordi)
Route136_Text_MayIntro:
	.string "MAY: {PLAYER}! You climbed all the\n"
	.string "way up here too?\p"
	.string "They say there's a town on the other\n"
	.string "side of this pass that's not even on\l"
	.string "the map yet.\p"
	.string "Let's see who deserves to see it first!$"

Route136_Text_MayDefeat:
	.string "MAY: You really are strong.$"

Route136_Text_MayPostBattle:
	.string "MAY: Go on, you found it first.\n"
	.string "I'll catch up with you!$"

Route136_Text_BrendanIntro:
	.string "BRENDAN: {PLAYER}! You climbed all\n"
	.string "the way up here too?\p"
	.string "They say there's a town on the other\n"
	.string "side of this pass that's not even on\l"
	.string "the map yet.\p"
	.string "Let's see who deserves to see it first!$"

Route136_Text_BrendanDefeat:
	.string "BRENDAN: You really are strong.$"

Route136_Text_BrendanPostBattle:
	.string "BRENDAN: Go on, you found it first.\n"
	.string "I'll catch up with you!$"

Route136_Text_SomethingUnseeable:
	.string "Something unseeable is in the way.$"

Route136_Text_UseDevonScope:
	.string "Something unseeable is in the way.\p"
	.string "Want to use the DEVON SCOPE?$"

Route136_Text_UsedDevonScope:
	.string "{PLAYER} used the DEVON SCOPE.\p"
	.string "An invisible POKéMON became completely\n"
	.string "visible!$"

Route136_Text_KecclesIntro:
	.string "KECCLES: You again!\p"
	.string "This is my spot. Nobody gets past\n"
	.string "without a battle!$"

Route136_Text_KecclesDefeat:
	.string "KECCLES: Hmmm…$"

Route136_Text_KecclesPostBattle:
	.string "KECCLES: See you in FORTREE.$"

Route136_Text_OttoIntro:
	.string "The higher you climb, the thinner\n"
	.string "the air. Can you handle it?$"

Route136_Text_OttoDefeat:
	.string "I need to catch my breath…$"

Route136_Text_OttoPostBattle:
	.string "Take it slow on the stairs up ahead.$"

Route136_Text_HelmutIntro:
	.string "These mountains have never been\n"
	.string "properly mapped. Let's battle!$"

Route136_Text_HelmutDefeat:
	.string "You climb like a pro.$"

Route136_Text_HelmutPostBattle:
	.string "I heard there's a hidden cave\n"
	.string "somewhere around here.$"

Route136_Text_ConnorIntro:
	.string "Only the strongest trainers make\n"
	.string "it up this mountain!$"

Route136_Text_ConnorDefeat:
	.string "You're one of them, apparently.$"

Route136_Text_ConnorPostBattle:
	.string "The stairs up that wall are brutal.$"

Route136_Text_SigridIntro:
	.string "Careful on this ledge.\n"
	.string "One wrong step…$"

Route136_Text_SigridDefeat:
	.string "You didn't even look down!$"

Route136_Text_SigridPostBattle:
	.string "The view from here is amazing,\n"
	.string "isn't it?$"

Route136_Text_RafaelIntro:
	.string "You found my training spot!$"

Route136_Text_RafaelDefeat:
	.string "Not bad at all.$"

Route136_Text_RafaelPostBattle:
	.string "Nobody ever comes up here.$"

Route136_Text_HakonIntro:
	.string "My dragons live on the highest peaks.\n"
	.string "Face them if you dare!$"

Route136_Text_HakonDefeat:
	.string "My dragons… defeated.$"

Route136_Text_HakonPostBattle:
	.string "Beyond the pass lies a valley no one\n"
	.string "has seen in a hundred years.$"

@ De bergpas naar Ashfrost: Ashfrost heeft een eigen tileset, dus geen naadloze connectie maar een warp
Route136_EventScript_ToAshfrost::
	warpsilent MAP_ASHFROST_TOWN, 7, 32
	waitstate
	end
