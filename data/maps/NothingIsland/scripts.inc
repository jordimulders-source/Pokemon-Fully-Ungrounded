@ Project Grounded: Nothing Island (mistbank ten westen van Route 105). Kaart: tools/grounded/maptools/plasma_frigate.py
@ Post-game Genesect-sidequest: de vrachtbrief in de serverkluis onder New Mauville (VAR_PLASMA_FRIGATE 1) zet de
@ Neo Plasma-bemanning op het eiland. Nigel blokkeert de steiger; aan het eind van de steiger ga je aan boord.
@ Placeholderteksten; Jordi herschrijft ze via de Dialoogstudio.
NothingIsland_MapScripts::
	map_script MAP_SCRIPT_ON_TRANSITION, NothingIsland_OnTransition
	.byte 0

NothingIsland_OnTransition:
	setflag FLAG_HIDE_PLASMA_ISLAND_CREW
	goto_if_eq VAR_PLASMA_FRIGATE, 0, NothingIsland_EventScript_TransitionEnd
	clearflag FLAG_HIDE_PLASMA_ISLAND_CREW
	call_if_defeated TRAINER_PLASMA_NIGEL, NothingIsland_EventScript_NigelAside
NothingIsland_EventScript_TransitionEnd:
	end

NothingIsland_EventScript_NigelAside::
	setobjectxyperm LOCALID_PLASMA_NIGEL, 21, 14
	setobjectmovementtype LOCALID_PLASMA_NIGEL, MOVEMENT_TYPE_FACE_DOWN
	return

NothingIsland_EventScript_Lookout::
	trainerbattle_single TRAINER_PLASMA_ISLE_LOOKOUT, NothingIsland_Text_LookoutIntro, NothingIsland_Text_LookoutDefeat
	msgbox NothingIsland_Text_LookoutPostBattle, MSGBOX_AUTOCLOSE
	end

NothingIsland_EventScript_Guard::
	trainerbattle_single TRAINER_PLASMA_ISLE_GUARD, NothingIsland_Text_GuardIntro, NothingIsland_Text_GuardDefeat
	msgbox NothingIsland_Text_GuardPostBattle, MSGBOX_AUTOCLOSE
	end

NothingIsland_EventScript_Nigel::
	trainerbattle_single TRAINER_PLASMA_NIGEL, NothingIsland_Text_NigelIntro, NothingIsland_Text_NigelDefeat, NothingIsland_EventScript_NigelDefeated
	msgbox NothingIsland_Text_NigelPostBattle, MSGBOX_AUTOCLOSE
	end

NothingIsland_EventScript_NigelDefeated::
	msgbox NothingIsland_Text_NigelStepsAside, MSGBOX_DEFAULT
	closemessage
	getplayerxy VAR_0x8004, VAR_0x8005
	goto_if_eq VAR_0x8005, 14, NothingIsland_EventScript_NigelDown
	applymovement LOCALID_PLASMA_NIGEL, NothingIsland_Movement_NigelAside
	goto NothingIsland_EventScript_NigelMoved
NothingIsland_EventScript_NigelDown::
	applymovement LOCALID_PLASMA_NIGEL, NothingIsland_Movement_NigelAsideDown
NothingIsland_EventScript_NigelMoved::
	waitmovement 0
	setobjectxyperm LOCALID_PLASMA_NIGEL, 21, 14
	setobjectmovementtype LOCALID_PLASMA_NIGEL, MOVEMENT_TYPE_FACE_DOWN
	release
	end

NothingIsland_Movement_NigelAside:
	walk_up
	face_down
	step_end

NothingIsland_Movement_NigelAsideDown:
	walk_down
	face_up
	step_end

@ coord-trigger aan het eind van de steiger
NothingIsland_EventScript_Gangway::
	lockall
	goto_if_eq VAR_PLASMA_FRIGATE, 0, NothingIsland_EventScript_GangwayLocked
	msgbox NothingIsland_Text_Board, MSGBOX_DEFAULT
	closemessage
	playse SE_EXIT
	warp MAP_PLASMA_FRIGATE_CORRIDOR, 2, 11
	waitstate
	releaseall
	end

NothingIsland_EventScript_GangwayLocked::
	msgbox NothingIsland_Text_GangwayLocked, MSGBOX_DEFAULT
	closemessage
	applymovement OBJ_EVENT_ID_PLAYER, NothingIsland_Movement_StepBack
	waitmovement 0
	releaseall
	end

NothingIsland_Movement_StepBack:
	walk_left
	step_end

NothingIsland_Text_GangwayLocked:
	.string "A sign on the gangway:\p"
	.string "“THIS IS NOT A SHIP.\n"
	.string "THERE IS NOTHING HERE.\l"
	.string "ESPECIALLY NOT A SHIP.”\p"
	.string "The not-ship is locked.$"

NothingIsland_Text_Board:
	.string "You walk up the gangway of the\n"
	.string "ship that isn't there.$"

NothingIsland_Text_LookoutIntro:
	.string "LOOKOUT REPORT, HOUR 400:\n"
	.string "fog. Fog. More fog.\p"
	.string "Oh! A kid! Finally, something\n"
	.string "to write down!$"

NothingIsland_Text_LookoutDefeat:
	.string "LOOKOUT REPORT, HOUR 400:\n"
	.string "got destroyed. Saw it coming.$"

NothingIsland_Text_LookoutPostBattle:
	.string "They gave me binoculars.\n"
	.string "In a fog bank.\p"
	.string "I think this is a punishment.$"

NothingIsland_Text_GuardIntro:
	.string "Welcome to NOTHING ISLAND!\n"
	.string "There's nothing here.\p"
	.string "Except me. And my POKéMON.\n"
	.string "And a frigate. Forget the frigate.$"

NothingIsland_Text_GuardDefeat:
	.string "That's nothing.\n"
	.string "Nothing happened.$"

NothingIsland_Text_GuardPostBattle:
	.string "Even the TENTACOOL left this island.\n"
	.string "They said the vibes were off.$"

NothingIsland_Text_NigelIntro:
	.string "NIGEL. Head of Logistics.\n"
	.string "I signed for the bug.\p"
	.string "Do you know how hard it is to fit\n"
	.string "an angry Paleozoic tank in a\l"
	.string "standard shipping crate?\p"
	.string "You don't. Nobody asks Logistics.\n"
	.string "Nobody ever asks Logistics.$"

NothingIsland_Text_NigelDefeat:
	.string "Package… delivered.\n"
	.string "To my face.$"

NothingIsland_Text_NigelStepsAside:
	.string "Fine. Go aboard.\p"
	.string "Sign the guest book. It's a crate.\n"
	.string "Everything here is a crate.$"

NothingIsland_Text_NigelPostBattle:
	.string "Fun fact: SHIPMENT 0451 also had\n"
	.string "a return label.\p"
	.string "We were going to send it back if\n"
	.string "it didn't fit. It didn't fit.$"
