@ Project Grounded: SpacetimeCave (tools/grounded/maptools/spacetime_cave.py)
SpacetimeCave_MapScripts::
	map_script MAP_SCRIPT_ON_LOAD, SpacetimeCave_OnLoad
	map_script MAP_SCRIPT_ON_TRANSITION, SpacetimeCave_OnTransition
	map_script MAP_SCRIPT_ON_FRAME_TABLE, SpacetimeCave_OnFrame
	.byte 0

SpacetimeCave_EventScript_RiftGlimwood::
	msgbox SpacetimeCave_Text_RiftGlimwood, MSGBOX_SIGN
	end

SpacetimeCave_EventScript_RiftAreaZero::
	msgbox SpacetimeCave_Text_RiftAreaZero, MSGBOX_SIGN
	end

@ Spacetime_AllSidequestsDone: VAR_RESULT = TRUE als alle Spacetime-sidequests klaar zijn, VAR_0x8005 = het
@ aantal dat nog openstaat. Uitbreiden: de klaar-flag van een nieuwe locatie in SIDEQUESTS (spacetime_cave.py)
@ zetten. Nog niet gebouwde locaties (National Park/Ilex, Chargestone Cave, Glimwood Tangle, Area Zero) tellen
@ pas mee als hun flag in de lijst staat; tot dan telt alleen wat bestaat.
Spacetime_AllSidequestsDone::
	setvar VAR_0x8005, 0
	call_if_unset FLAG_SPACETIME_LAVENDER_DONE, Spacetime_EventScript_CountOpen @ Lavender Town: de kwade geesten verdreven
	call_if_unset FLAG_SPACETIME_CERULEAN_DONE, Spacetime_EventScript_CountOpen @ Cerulean Cave: Mewtwo gevangen of verslagen
	call_if_unset FLAG_SPACETIME_CHARGESTONE_DONE, Spacetime_EventScript_CountOpen @ Chargestone Cave: Zeraora gevangen of verslagen
	call_if_unset FLAG_NATIONAL_PARK_DONE, Spacetime_EventScript_CountOpen @ National Park: Eternatus gevangen of verslagen
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
	call_if_unset FLAG_SPACETIME_LAKES_SCENE, SpacetimeCave_EventScript_HideLakes
	call Spacetime_AllSidequestsDone
	call_if_eq VAR_RESULT, TRUE, SpacetimeCave_EventScript_OpenGateUnknown
	call_if_set FLAG_SPACETIME_YOSHI_DONE, SpacetimeCave_EventScript_OpenGateYoshi
	getcaughtmon SPECIES_GIRATINA
	call_if_ne VAR_RESULT, 0, SpacetimeCave_EventScript_OpenGateGiratina
	end

SpacetimeCave_OnTransition:
	call_if_unset FLAG_SPACETIME_RIFTS_OPENED, SpacetimeCave_EventScript_ArmScene
	call_if_set FLAG_SPACETIME_LAKES_SCENE, SpacetimeCave_EventScript_DisarmLakes
	end

SpacetimeCave_EventScript_ArmScene:
	setvar VAR_TEMP_1, 1
	return

SpacetimeCave_EventScript_DisarmLakes:
	setvar VAR_TEMP_2, 1
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
	return

SpacetimeCave_EventScript_OpenRifts:
	setmetatile 4, 5, 0x3CE, FALSE
	setmetatile 5, 5, 0x3CF, FALSE
	setmetatile 4, 6, 0x3D0, TRUE
	setmetatile 5, 6, 0x3D1, TRUE
	setmetatile 4, 10, 0x3CE, FALSE
	setmetatile 5, 10, 0x3CF, FALSE
	setmetatile 4, 11, 0x3D0, TRUE
	setmetatile 5, 11, 0x3D1, TRUE
	setmetatile 4, 14, 0x3CE, FALSE
	setmetatile 5, 14, 0x3CF, FALSE
	setmetatile 4, 15, 0x3D0, TRUE
	setmetatile 5, 15, 0x3D1, TRUE
	setmetatile 21, 5, 0x3CE, FALSE
	setmetatile 22, 5, 0x3CF, FALSE
	setmetatile 21, 6, 0x3D0, TRUE
	setmetatile 22, 6, 0x3D1, TRUE
	setmetatile 21, 10, 0x3CE, TRUE
	setmetatile 22, 10, 0x3CF, TRUE
	setmetatile 21, 11, 0x3D0, TRUE
	setmetatile 22, 11, 0x3D1, TRUE
	setmetatile 21, 14, 0x3CE, TRUE
	setmetatile 22, 14, 0x3CF, TRUE
	setmetatile 21, 15, 0x3D0, TRUE
	setmetatile 22, 15, 0x3D1, TRUE
	return

SpacetimeCave_EventScript_HideLakes:
	setmetatile 13, 42, 0x201, FALSE
	setmetatile 14, 42, 0x201, FALSE
	setmetatile 13, 43, 0x201, FALSE
	setmetatile 14, 43, 0x201, FALSE
	setmetatile 7, 45, 0x201, FALSE
	setmetatile 8, 45, 0x201, FALSE
	setmetatile 7, 46, 0x201, FALSE
	setmetatile 8, 46, 0x201, FALSE
	setmetatile 18, 45, 0x201, FALSE
	setmetatile 19, 45, 0x201, FALSE
	setmetatile 18, 46, 0x201, FALSE
	setmetatile 19, 46, 0x201, FALSE
	return

SpacetimeCave_EventScript_OpenLakes:
	setmetatile 13, 42, 0x3CE, TRUE
	setmetatile 14, 42, 0x3CF, TRUE
	setmetatile 13, 43, 0x3D0, TRUE
	setmetatile 14, 43, 0x3D1, TRUE
	setmetatile 7, 45, 0x3CE, TRUE
	setmetatile 8, 45, 0x3CF, TRUE
	setmetatile 7, 46, 0x3D0, TRUE
	setmetatile 8, 46, 0x3D1, TRUE
	setmetatile 18, 45, 0x3CE, TRUE
	setmetatile 19, 45, 0x3CF, TRUE
	setmetatile 18, 46, 0x3D0, TRUE
	setmetatile 19, 46, 0x3D1, TRUE
	return

SpacetimeCave_EventScript_OpenGateUnknown:
	setmetatile 13, 19, 0x201, FALSE
	setmetatile 14, 19, 0x201, FALSE
	setmetatile 13, 20, 0x201, FALSE
	setmetatile 14, 20, 0x201, FALSE
	return

SpacetimeCave_EventScript_OpenGateYoshi:
	setmetatile 13, 34, 0x201, FALSE
	setmetatile 14, 34, 0x201, FALSE
	setmetatile 13, 35, 0x201, FALSE
	setmetatile 14, 35, 0x201, FALSE
	return

SpacetimeCave_EventScript_OpenGateGiratina:
	setmetatile 12, 54, 0x212, TRUE
	setmetatile 13, 54, 0x201, FALSE
	setmetatile 14, 54, 0x201, FALSE
	setmetatile 15, 54, 0x210, TRUE
	setmetatile 12, 55, 0x212, TRUE
	setmetatile 13, 55, 0x201, FALSE
	setmetatile 14, 55, 0x201, FALSE
	setmetatile 15, 55, 0x210, TRUE
	setmetatile 12, 56, 0x212, TRUE
	setmetatile 13, 56, 0x201, FALSE
	setmetatile 14, 56, 0x201, FALSE
	setmetatile 15, 56, 0x210, TRUE
	setmetatile 12, 57, 0x212, TRUE
	setmetatile 13, 57, 0x201, FALSE
	setmetatile 14, 57, 0x201, FALSE
	setmetatile 15, 57, 0x210, TRUE
	setmetatile 12, 58, 0x21A, TRUE
	setmetatile 13, 58, 0x201, FALSE
	setmetatile 14, 58, 0x201, FALSE
	setmetatile 15, 58, 0x218, TRUE
	setmetatile 12, 59, 0x219, TRUE
	setmetatile 13, 59, 0x201, FALSE
	setmetatile 14, 59, 0x201, FALSE
	setmetatile 15, 59, 0x219, TRUE
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

SpacetimeCave_EventScript_GateUnknown::
	lockall
	call Spacetime_AllSidequestsDone
	goto_if_eq VAR_RESULT, TRUE, SpacetimeCave_EventScript_GateEnd
	buffernumberstring STR_VAR_1, VAR_0x8005
	msgbox SpacetimeCave_Text_GateUnknown, MSGBOX_DEFAULT
	releaseall
	end

SpacetimeCave_EventScript_GateYoshi::
	lockall
	goto_if_set FLAG_SPACETIME_YOSHI_DONE, SpacetimeCave_EventScript_GateEnd
	msgbox SpacetimeCave_Text_GateYoshi, MSGBOX_DEFAULT
	releaseall
	end

SpacetimeCave_EventScript_GateEnd::
	releaseall
	end

SpacetimeCave_EventScript_Inscription::
	lockall
	getcaughtmon SPECIES_GIRATINA
	goto_if_ne VAR_RESULT, 0, SpacetimeCave_EventScript_GateEnd
	msgbox SpacetimeCave_Text_Inscription, MSGBOX_DEFAULT
	releaseall
	end

SpacetimeCave_EventScript_PortalUnknown::
	lockall
	playse SE_M_TELEPORT
	setvar VAR_0x8004, 1
	setvar VAR_0x8005, 1
	setvar VAR_0x8006, 8
	setvar VAR_0x8007, 3
	special ShakeCamera
	waitstate
	msgbox SpacetimeCave_Text_PortalUnknown, MSGBOX_DEFAULT
	releaseall
	end

SpacetimeCave_EventScript_PortalAcuity::
	msgbox SpacetimeCave_Text_PortalAcuity, MSGBOX_SIGN
	end

SpacetimeCave_EventScript_PortalValor::
	msgbox SpacetimeCave_Text_PortalValor, MSGBOX_SIGN
	end

SpacetimeCave_EventScript_PortalVerity::
	msgbox SpacetimeCave_Text_PortalVerity, MSGBOX_SIGN
	end

SpacetimeCave_EventScript_PortalCoronet::
	msgbox SpacetimeCave_Text_PortalCoronet, MSGBOX_SIGN
	end

SpacetimeCave_EventScript_LakesScene::
	lockall
	applymovement OBJ_EVENT_ID_PLAYER, SpacetimeCave_EventScript_Movement_LakesIn
	waitmovement 0
	playmoncry SPECIES_PALKIA, CRY_MODE_ENCOUNTER
	waitmoncry
	msgbox SpacetimeCave_Text_LakesPalkia1, MSGBOX_DEFAULT
	playmoncry SPECIES_DIALGA, CRY_MODE_ENCOUNTER
	waitmoncry
	msgbox SpacetimeCave_Text_LakesDialga1, MSGBOX_DEFAULT
	msgbox SpacetimeCave_Text_LakesPalkia2, MSGBOX_DEFAULT
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
	call SpacetimeCave_EventScript_OpenLakes
	special DrawWholeMapView
	removeobject LOCALID_SPACETIME_LAKES_DIALGA
	removeobject LOCALID_SPACETIME_LAKES_PALKIA
	setflag FLAG_SPACETIME_LAKES_SCENE
	setvar VAR_TEMP_2, 1
	delay 20
	fadescreenspeed FADE_FROM_WHITE, 4
	playse SE_M_TELEPORT
	msgbox SpacetimeCave_Text_LakesOpen, MSGBOX_DEFAULT
	releaseall
	end

SpacetimeCave_EventScript_Movement_LakesIn:
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
	.string "PALKIA: The passage to the south stays\n"
	.string "shut until every one of these is fixed.\p"
	.string "What's down there? Ask again later.\n"
	.string "Ideally much later. Ideally never.$"

SpacetimeCave_Text_RiftsOpen:
	.string "The cave tore open in six places at\n"
	.string "once!\p"
	.string "DIALGA and PALKIA are gone. The\n"
	.string "passage to the south is still a wall of\l"
	.string "folded spacetime.$"

SpacetimeCave_Text_GateUnknown:
	.string "The passage is blocked by a wall of\n"
	.string "folded spacetime. It flickers between\l"
	.string "'rock', 'not rock' and 'error'.\p"
	.string "It won't settle until the rifts upstairs\n"
	.string "are fixed. {STR_VAR_1} to go.$"

SpacetimeCave_Text_GateYoshi:
	.string "Another fold in spacetime. This one\n"
	.string "smells faintly of fruit and is humming a\l"
	.string "jaunty tune.\p"
	.string "Whatever went wrong behind the ?????\n"
	.string "rift has to be put right first.$"

SpacetimeCave_Text_Inscription:
	.string "Words are carved into the dead end,\n"
	.string "upside down and back to front:\p"
	.string "'WHERE THE SKY PILLAR STANDS ON ITS\n"
	.string "HEAD, THE ONE WHO WAS BANISHED HOLDS\l"
	.string "THE DOOR. BRING IT ALONG, AND THE WALL\l"
	.string "WILL REMEMBER IT WAS NEVER A WALL.'$"

SpacetimeCave_Text_PortalUnknown:
	.string "You reach into the ????? rift...\p"
	.string "Something grabs your sleeve. A small\n"
	.string "hand. In a mask. It pulls, the rift\l"
	.string "hiccups, and spits you straight back\l"
	.string "out.\p"
	.string "Something went wrong. Spacetime says:\n"
	.string "island not found. Try again in a later\l"
	.string "version of reality.$"

SpacetimeCave_Text_PortalAcuity:
	.string "Snow blows out of this portal, and the\n"
	.string "cold has a voice. It is thinking about\l"
	.string "you. It knows things.\p"
	.string "LAKE ACUITY. The ice on the other side\n"
	.string "is still being installed.$"

SpacetimeCave_Text_PortalValor:
	.string "Behind this portal: a calm lake, and a\n"
	.string "cave in the middle of it, and something\l"
	.string "in the cave that is very brave from a\l"
	.string "safe distance.\p"
	.string "LAKE VALOR. Not open yet.$"

SpacetimeCave_Text_PortalVerity:
	.string "A lake, warm and still. Someone over\n"
	.string "there is feeling a lot of feelings, on\l"
	.string "your behalf.\p"
	.string "LAKE VERITY. Under construction. The\n"
	.string "feelings are not.$"

SpacetimeCave_Text_PortalCoronet:
	.string "The last portal. Behind it, a mountain\n"
	.string "climbs out of the top of the world.\p"
	.string "MT. CORONET. You can hear it breathing.\n"
	.string "It isn't ready for you. Possibly the\l"
	.string "other way round.$"

SpacetimeCave_Text_LakesPalkia1:
	.string "PALKIA: You again. Good. We were\n"
	.string "starting to think the island ate you.\p"
	.string "It does that. It's very round and very\n"
	.string "hungry.$"

SpacetimeCave_Text_LakesDialga1:
	.string "DIALGA: Listen. Something is coming. Not\n"
	.string "today. Not in any time I'd call 'soon'.\l"
	.string "But it is coming, in every dimension at\l"
	.string "once.\p"
	.string "We cannot stop it. We are space and\n"
	.string "time. It is the kind of problem that\l"
	.string "needs a brain, a heart and a spine.$"

SpacetimeCave_Text_LakesPalkia2:
	.string "PALKIA: Three of them. KNOWLEDGE,\n"
	.string "EMOTION, WILLPOWER. They sleep in three\l"
	.string "lakes.\p"
	.string "Go wake them up. Be polite. The last\n"
	.string "person who wasn't lost their memory,\l"
	.string "their feelings, and their car keys.$"

SpacetimeCave_Text_LakesOpen:
	.string "Three portals tore open: LAKE ACUITY,\n"
	.string "LAKE VALOR and LAKE VERITY!\p"
	.string "DIALGA and PALKIA are gone again. They\n"
	.string "really do love an exit.$"

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
	.string "passage to the south unfolds.$"

SpacetimeCave_Text_ResearcherDone:
	.string "Every working rift is quiet. You did\n"
	.string "that.\p"
	.string "The passage to the south has unfolded.\n"
	.string "Something down there is humming. I liked\l"
	.string "the screaming better. You knew where\l"
	.string "you stood.$"
