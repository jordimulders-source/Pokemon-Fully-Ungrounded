@ Project Grounded: SpacetimeCave (tools/grounded/maptools/spacetime_cave.py)
SpacetimeCave_MapScripts::
	map_script MAP_SCRIPT_ON_LOAD, SpacetimeCave_OnLoad
	map_script MAP_SCRIPT_ON_TRANSITION, SpacetimeCave_OnTransition
	map_script MAP_SCRIPT_ON_FRAME_TABLE, SpacetimeCave_OnFrame
	.byte 0

SpacetimeCave_EventScript_RiftPark::
	msgbox SpacetimeCave_Text_RiftPark, MSGBOX_SIGN
	end

SpacetimeCave_EventScript_RiftLakes::
	msgbox SpacetimeCave_Text_RiftLakes, MSGBOX_SIGN
	end

SpacetimeCave_EventScript_RiftChargestone::
	msgbox SpacetimeCave_Text_RiftChargestone, MSGBOX_SIGN
	end

SpacetimeCave_EventScript_RiftGlimwood::
	msgbox SpacetimeCave_Text_RiftGlimwood, MSGBOX_SIGN
	end

SpacetimeCave_EventScript_RiftAreaZero::
	msgbox SpacetimeCave_Text_RiftAreaZero, MSGBOX_SIGN
	end

SpacetimeCave_EventScript_RiftCoronet::
	msgbox SpacetimeCave_Text_RiftCoronet, MSGBOX_SIGN
	end

SpacetimeCave_EventScript_RiftUnknown::
	lockall
	call Spacetime_AllSidequestsDone
	goto_if_eq VAR_RESULT, TRUE, SpacetimeCave_EventScript_RiftUnknownOpen
	buffernumberstring STR_VAR_1, VAR_0x8005
	msgbox SpacetimeCave_Text_RiftUnknownSealed, MSGBOX_DEFAULT
	releaseall
	end

SpacetimeCave_EventScript_RiftUnknownOpen::
	msgbox SpacetimeCave_Text_RiftUnknownOpen, MSGBOX_DEFAULT
	releaseall
	end

@ Spacetime_AllSidequestsDone: VAR_RESULT = TRUE als alle Spacetime-sidequests klaar zijn, VAR_0x8005 = het
@ aantal dat nog openstaat. Uitbreiden: de klaar-flag van een nieuwe locatie in SIDEQUESTS (spacetime_cave.py)
@ zetten. Nog niet gebouwde locaties (National Park/Ilex, Chargestone Cave, Glimwood Tangle, Area Zero) tellen
@ pas mee als hun flag in de lijst staat; tot dan telt alleen wat bestaat.
Spacetime_AllSidequestsDone::
	setvar VAR_0x8005, 0
	call_if_unset FLAG_SPACETIME_LAVENDER_DONE, Spacetime_EventScript_CountOpen @ Lavender Town: de kwade geesten verdreven
	call_if_unset FLAG_SPACETIME_CERULEAN_DONE, Spacetime_EventScript_CountOpen @ Cerulean Cave: Mewtwo gevangen of verslagen
	setvar VAR_RESULT, FALSE
	call_if_eq VAR_0x8005, 0, Spacetime_EventScript_AllDone
	return

Spacetime_EventScript_CountOpen:
	addvar VAR_0x8005, 1
	return

Spacetime_EventScript_AllDone:
	setvar VAR_RESULT, TRUE
	return

SpacetimeCave_OnLoad:
	call_if_unset FLAG_SPACETIME_RIFTS_OPENED, SpacetimeCave_EventScript_HideRifts
	goto_if_unset FLAG_SPACETIME_RIFTS_OPENED, SpacetimeCave_EventScript_OnLoadEnd
	call Spacetime_AllSidequestsDone
	call_if_eq VAR_RESULT, TRUE, SpacetimeCave_EventScript_UnsealUnknown
SpacetimeCave_EventScript_OnLoadEnd:
	end

SpacetimeCave_OnTransition:
	call_if_unset FLAG_SPACETIME_RIFTS_OPENED, SpacetimeCave_EventScript_ArmScene
	end

SpacetimeCave_EventScript_ArmScene:
	setvar VAR_TEMP_1, 1
	return

SpacetimeCave_OnFrame:
	map_script_2 VAR_TEMP_1, 1, SpacetimeCave_EventScript_FirstVisit
	.2byte 0

SpacetimeCave_EventScript_HideRifts:
	setmetatile 4, 5, 0x201, FALSE
	setmetatile 5, 5, 0x201, FALSE
	setmetatile 4, 6, 0x201, FALSE
	setmetatile 5, 6, 0x201, FALSE
	setmetatile 4, 10, 0x201, FALSE
	setmetatile 5, 10, 0x201, FALSE
	setmetatile 4, 11, 0x201, FALSE
	setmetatile 5, 11, 0x201, FALSE
	setmetatile 4, 14, 0x201, FALSE
	setmetatile 5, 14, 0x201, FALSE
	setmetatile 4, 15, 0x201, FALSE
	setmetatile 5, 15, 0x201, FALSE
	setmetatile 21, 5, 0x201, FALSE
	setmetatile 22, 5, 0x201, FALSE
	setmetatile 21, 6, 0x201, FALSE
	setmetatile 22, 6, 0x201, FALSE
	setmetatile 21, 10, 0x201, FALSE
	setmetatile 22, 10, 0x201, FALSE
	setmetatile 21, 11, 0x201, FALSE
	setmetatile 22, 11, 0x201, FALSE
	setmetatile 21, 14, 0x201, FALSE
	setmetatile 22, 14, 0x201, FALSE
	setmetatile 21, 15, 0x201, FALSE
	setmetatile 22, 15, 0x201, FALSE
	setmetatile 8, 15, 0x201, FALSE
	setmetatile 9, 15, 0x201, FALSE
	setmetatile 8, 16, 0x201, FALSE
	setmetatile 9, 16, 0x201, FALSE
	setmetatile 17, 15, 0x201, FALSE
	setmetatile 18, 15, 0x201, FALSE
	setmetatile 17, 16, 0x201, FALSE
	setmetatile 18, 16, 0x201, FALSE
	setmetatile 12, 15, 0x201, FALSE
	setmetatile 13, 15, 0x201, FALSE
	setmetatile 12, 16, 0x201, FALSE
	setmetatile 13, 16, 0x201, FALSE
	return

SpacetimeCave_EventScript_OpenRifts:
	setmetatile 4, 5, 0x3AA, FALSE
	setmetatile 5, 5, 0x3AB, FALSE
	setmetatile 4, 6, 0x3AC, TRUE
	setmetatile 5, 6, 0x3AD, TRUE
	setmetatile 4, 10, 0x3AA, FALSE
	setmetatile 5, 10, 0x3AB, FALSE
	setmetatile 4, 11, 0x3AC, TRUE
	setmetatile 5, 11, 0x3AD, TRUE
	setmetatile 4, 14, 0x3AA, TRUE
	setmetatile 5, 14, 0x3AB, TRUE
	setmetatile 4, 15, 0x3AC, TRUE
	setmetatile 5, 15, 0x3AD, TRUE
	setmetatile 21, 5, 0x3AA, TRUE
	setmetatile 22, 5, 0x3AB, TRUE
	setmetatile 21, 6, 0x3AC, TRUE
	setmetatile 22, 6, 0x3AD, TRUE
	setmetatile 21, 10, 0x3AA, TRUE
	setmetatile 22, 10, 0x3AB, TRUE
	setmetatile 21, 11, 0x3AC, TRUE
	setmetatile 22, 11, 0x3AD, TRUE
	setmetatile 21, 14, 0x3AA, TRUE
	setmetatile 22, 14, 0x3AB, TRUE
	setmetatile 21, 15, 0x3AC, TRUE
	setmetatile 22, 15, 0x3AD, TRUE
	setmetatile 8, 15, 0x3AA, TRUE
	setmetatile 9, 15, 0x3AB, TRUE
	setmetatile 8, 16, 0x3AC, TRUE
	setmetatile 9, 16, 0x3AD, TRUE
	setmetatile 17, 15, 0x3AE, TRUE
	setmetatile 18, 15, 0x3AF, TRUE
	setmetatile 17, 16, 0x3B0, TRUE
	setmetatile 18, 16, 0x3B1, TRUE
	setmetatile 12, 15, 0x3AE, TRUE
	setmetatile 13, 15, 0x3AF, TRUE
	setmetatile 12, 16, 0x3B0, TRUE
	setmetatile 13, 16, 0x3B1, TRUE
	return

SpacetimeCave_EventScript_UnsealUnknown:
	setmetatile 17, 15, 0x3AA, TRUE
	setmetatile 18, 15, 0x3AB, TRUE
	setmetatile 17, 16, 0x3AC, TRUE
	setmetatile 18, 16, 0x3AD, TRUE
	return

SpacetimeCave_EventScript_FirstVisit::
	lockall
	setvar VAR_TEMP_1, 0
	applymovement OBJ_EVENT_ID_PLAYER, SpacetimeCave_EventScript_Movement_PlayerIn
	waitmovement 0
	playmoncry SPECIES_DIALGA, CRY_MODE_ENCOUNTER
	waitmoncry
	msgbox SpacetimeCave_Text_Dialga1, MSGBOX_DEFAULT
	playmoncry SPECIES_PALKIA, CRY_MODE_ENCOUNTER
	waitmoncry
	msgbox SpacetimeCave_Text_Palkia1, MSGBOX_DEFAULT
	msgbox SpacetimeCave_Text_Dialga2, MSGBOX_DEFAULT
	msgbox SpacetimeCave_Text_Palkia2, MSGBOX_DEFAULT
	closemessage
	playmoncry SPECIES_DIALGA, CRY_MODE_ENCOUNTER
	waitmoncry
	playmoncry SPECIES_PALKIA, CRY_MODE_ENCOUNTER
	setvar VAR_0x8004, 2
	setvar VAR_0x8005, 2
	setvar VAR_0x8006, 12
	setvar VAR_0x8007, 4
	special ShakeCamera
	waitstate
	waitmoncry
	playse SE_M_DETECT
	fadescreenspeed FADE_TO_WHITE, 2
	call SpacetimeCave_EventScript_OpenRifts
	special DrawWholeMapView
	removeobject LOCALID_SPACETIME_DIALGA
	removeobject LOCALID_SPACETIME_PALKIA
	setflag FLAG_SPACETIME_RIFTS_OPENED
	delay 20
	fadescreenspeed FADE_FROM_WHITE, 4
	playse SE_M_TELEPORT
	msgbox SpacetimeCave_Text_RiftsOpen, MSGBOX_DEFAULT
	releaseall
	end

SpacetimeCave_EventScript_Movement_PlayerIn:
	walk_down
	walk_down
	walk_down
	step_end

SpacetimeCave_EventScript_Plaque::
	msgbox SpacetimeCave_Text_Plaque, MSGBOX_SIGN
	end

SpacetimeCave_EventScript_Researcher::
	lock
	faceplayer
	call Spacetime_AllSidequestsDone
	goto_if_eq VAR_RESULT, TRUE, SpacetimeCave_EventScript_ResearcherDone
	buffernumberstring STR_VAR_1, VAR_0x8005
	msgbox SpacetimeCave_Text_Researcher, MSGBOX_DEFAULT
	release
	end

SpacetimeCave_EventScript_ResearcherDone::
	msgbox SpacetimeCave_Text_ResearcherDone, MSGBOX_DEFAULT
	release
	end

@ ---------------------------------------------------------------- teksten (placeholders, Jordi herschrijft ze)
SpacetimeCave_Text_RiftPark:
	.string "The rift is wide open. Through it you\n"
	.string "can just make out a park shaped like a\l"
	.string "POKé BALL, and a forest behind it that\l"
	.string "hums.\p"
	.string "The other side hasn't finished existing\n"
	.string "yet, though. Spacetime is still loading.$"

SpacetimeCave_Text_RiftLakes:
	.string "The rift is wide open. Through it you\n"
	.string "can just make out three lakes, and\l"
	.string "three pairs of eyes that are definitely\l"
	.string "watching.\p"
	.string "The other side hasn't finished existing\n"
	.string "yet, though. Spacetime is still loading.$"

SpacetimeCave_Text_RiftChargestone:
	.string "The rift is wide open. Through it you\n"
	.string "can just make out floating rocks and\l"
	.string "enough static to restyle your hair.\p"
	.string "The other side hasn't finished existing\n"
	.string "yet, though. Spacetime is still loading.$"

SpacetimeCave_Text_RiftGlimwood:
	.string "The rift is wide open. Through it you\n"
	.string "can just make out glowing mushrooms\l"
	.string "and a forest that is far too pleased\l"
	.string "with itself.\p"
	.string "The other side hasn't finished existing\n"
	.string "yet, though. Spacetime is still loading.$"

SpacetimeCave_Text_RiftAreaZero:
	.string "The rift is wide open. Through it you\n"
	.string "can just make out a crater that keeps\l"
	.string "going down long after it should have\l"
	.string "stopped.\p"
	.string "The other side hasn't finished existing\n"
	.string "yet, though. Spacetime is still loading.$"

SpacetimeCave_Text_RiftCoronet:
	.string "This rift is sealed shut. Through the\n"
	.string "cracks: a mountain at the top of the\l"
	.string "world, and something enormous\l"
	.string "breathing behind it.\p"
	.string "DIALGA and PALKIA sealed this one\n"
	.string "themselves. It's the kind of seal that\l"
	.string "means 'later'.$"

SpacetimeCave_Text_RiftUnknownSealed:
	.string "The rift shows... nothing. A silhouette\n"
	.string "of a green dinosaur. Then static.\p"
	.string "It's sealed. Something on the other\n"
	.string "side is waiting until you've cleaned up\l"
	.string "the other rifts. {STR_VAR_1} to go.$"

SpacetimeCave_Text_RiftUnknownOpen:
	.string "The seal is gone. Something in there is\n"
	.string "very, very round, and it is humming a\l"
	.string "jaunty tune.\p"
	.string "The path isn't solid yet. Come back when\n"
	.string "spacetime has finished loading.$"

SpacetimeCave_Text_Dialga1:
	.string "DIALGA: ...Finally.\p"
	.string "Do you know how long we have been\n"
	.string "waiting for you? I do. Exactly. Down to\l"
	.string "the nanosecond. I am time. It's a whole\l"
	.string "thing.$"

SpacetimeCave_Text_Palkia1:
	.string "PALKIA: Don't mind him. He counts.\p"
	.string "Welcome to the space between spaces.\n"
	.string "Mind the edges. They're sharp, and some\l"
	.string "of them are Tuesdays.$"

SpacetimeCave_Text_Dialga2:
	.string "DIALGA: Every tear in this cave leads to\n"
	.string "a place that went wrong. Another\l"
	.string "dimension. Another time. Usually both.\p"
	.string "Go and fix them. We would do it\n"
	.string "ourselves, but we are very large and\l"
	.string "very busy.$"

SpacetimeCave_Text_Palkia2:
	.string "PALKIA: Two of them stay shut.\p"
	.string "One because you're not ready. The other\n"
	.string "because WE aren't. Don't ask which is\l"
	.string "which.$"

SpacetimeCave_Text_RiftsOpen:
	.string "The cave tore open in seven places at\n"
	.string "once!\p"
	.string "DIALGA and PALKIA are gone. Two rifts\n"
	.string "remain sealed: ????? and MT. CORONET.$"

SpacetimeCave_Text_Plaque:
	.string "SPACETIME CAVE\p"
	.string "Where places that no longer exist,\n"
	.string "never existed, or are in another\l"
	.string "cartridge go to wait.\p"
	.string "Please do not feed the timelines.$"

SpacetimeCave_Text_Researcher:
	.string "Did you SEE that? Two gods, one cave,\n"
	.string "zero safety briefings.\p"
	.string "I study the rifts. The far left one\n"
	.string "leads to a haunted town. The one below\l"
	.string "it smells like a very angry clone.\p"
	.string "My instruments say {STR_VAR_1} of the\n"
	.string "working rifts still need you before the\l"
	.string "sealed one in the corner calms down.$"

SpacetimeCave_Text_ResearcherDone:
	.string "Every working rift is quiet. You did\n"
	.string "that.\p"
	.string "The ????? rift has stopped screaming.\n"
	.string "Now it just hums. I liked the screaming\l"
	.string "better. You knew where you stood.$"
