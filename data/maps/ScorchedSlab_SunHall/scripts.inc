@ Project Grounded: Scorched Slab, Zonnezaal (tools/grounded/maptools/scorched_slab_ext.py).
@ Drie zonnestenen (Strength) moeten tegelijk in de drie lichtschachten staan; dan gaat de zonnedeur open.
@ PushBoulder_End (src/field_player_avatar.c) start StoneInLight zodra een steen op een lichtschacht belandt.
ScorchedSlab_SunHall_MapScripts::
	map_script MAP_SCRIPT_ON_LOAD, ScorchedSlab_SunHall_OnLoad
	.byte 0

ScorchedSlab_SunHall_OnLoad:
	call_if_unset FLAG_SCORCHED_SLAB_SUN_DOOR_OPEN, ScorchedSlab_SunHall_EventScript_CloseSunDoor
	end

ScorchedSlab_SunHall_EventScript_CloseSunDoor::
	setmetatile 12, 1, METATILE_Cave_EntranceCover, TRUE
	setmetatile 13, 1, METATILE_Cave_EntranceCover, TRUE
	setmetatile 14, 1, METATILE_Cave_EntranceCover, TRUE
	setmetatile 12, 2, METATILE_Cave_SealedChamberBraille_Mid, TRUE
	setmetatile 13, 2, METATILE_Cave_SealedChamberBraille_Mid, TRUE
	setmetatile 14, 2, METATILE_Cave_SealedChamberBraille_Mid, TRUE
	return

ScorchedSlab_SunHall_EventScript_StoneInLight::
	lockall
	playse SE_M_MORNING_SUN
	goto_if_set FLAG_SCORCHED_SLAB_SUN_DOOR_OPEN, ScorchedSlab_SunHall_EventScript_StoneGlowsAgain
	specialvar VAR_RESULT, ScorchedSlab_CountLitStones
	goto_if_eq VAR_RESULT, 3, ScorchedSlab_SunHall_EventScript_OpenSunDoor
	goto_if_eq VAR_RESULT, 2, ScorchedSlab_SunHall_EventScript_TwoStones
	msgbox ScorchedSlab_SunHall_Text_OneStone, MSGBOX_DEFAULT
	releaseall
	end

ScorchedSlab_SunHall_EventScript_TwoStones::
	msgbox ScorchedSlab_SunHall_Text_TwoStones, MSGBOX_DEFAULT
	releaseall
	end

ScorchedSlab_SunHall_EventScript_StoneGlowsAgain::
	msgbox ScorchedSlab_SunHall_Text_StoneGlowsAgain, MSGBOX_DEFAULT
	releaseall
	end

ScorchedSlab_SunHall_EventScript_OpenSunDoor::
	msgbox ScorchedSlab_SunHall_Text_ThreeStones, MSGBOX_DEFAULT
	closemessage
	setvar VAR_0x8004, 2
	setvar VAR_0x8005, 2
	setvar VAR_0x8006, 8
	setvar VAR_0x8007, 3
	special ShakeCamera
	waitstate
	setmetatile 12, 1, METATILE_Cave_SealedChamberEntrance_TopLeft, TRUE
	setmetatile 13, 1, METATILE_Cave_SealedChamberEntrance_TopMid, TRUE
	setmetatile 14, 1, METATILE_Cave_SealedChamberEntrance_TopRight, TRUE
	setmetatile 12, 2, METATILE_Cave_SealedChamberEntrance_BottomLeft, TRUE
	setmetatile 13, 2, METATILE_Cave_SealedChamberEntrance_BottomMid, FALSE
	setmetatile 14, 2, METATILE_Cave_SealedChamberEntrance_BottomRight, TRUE
	special DrawWholeMapView
	playse SE_BANG
	waitse
	setflag FLAG_SCORCHED_SLAB_SUN_DOOR_OPEN
	msgbox ScorchedSlab_SunHall_Text_DoorOpen, MSGBOX_DEFAULT
	releaseall
	end

ScorchedSlab_SunHall_EventScript_SunDoor::
	lockall
	goto_if_set FLAG_SCORCHED_SLAB_SUN_DOOR_OPEN, ScorchedSlab_SunHall_EventScript_SunDoorOpen
	msgbox ScorchedSlab_SunHall_Text_SunDoor, MSGBOX_DEFAULT
	specialvar VAR_RESULT, IsNightTime
	call_if_eq VAR_RESULT, TRUE, ScorchedSlab_SunHall_EventScript_SunDoorNight
	releaseall
	end

ScorchedSlab_SunHall_EventScript_SunDoorNight::
	msgbox ScorchedSlab_SunHall_Text_SunDoorNight, MSGBOX_DEFAULT
	return

ScorchedSlab_SunHall_EventScript_SunDoorOpen::
	msgbox ScorchedSlab_SunHall_Text_SunDoorOpen, MSGBOX_DEFAULT
	releaseall
	end

ScorchedSlab_SunHall_EventScript_Ray::
	trainerbattle_single TRAINER_SLAB_RAY, ScorchedSlab_SunHall_Text_RayIntro, ScorchedSlab_SunHall_Text_RayDefeat
	msgbox ScorchedSlab_SunHall_Text_RayPostBattle, MSGBOX_AUTOCLOSE
	end

ScorchedSlab_SunHall_Text_OneStone:
	.string "The stone drinks the sunlight and\n"
	.string "starts to glow.\p"
	.string "One sun. The other two holes in the\n"
	.string "ceiling look jealous.$"

ScorchedSlab_SunHall_Text_TwoStones:
	.string "Two stones glow. The floor is getting\n"
	.string "uncomfortably warm.\p"
	.string "Somewhere, a third beam of light is\n"
	.string "hitting nothing. What a waste.$"

ScorchedSlab_SunHall_Text_StoneGlowsAgain:
	.string "The stone glows. The door is already\n"
	.string "open. You're just pushing rocks for\l"
	.string "fun now. That's fine. No judgment.$"

ScorchedSlab_SunHall_Text_ThreeStones:
	.string "Three stones. Three suns.\n"
	.string "The whole hall hums like an oven\l"
	.string "that just finished preheating…$"

ScorchedSlab_SunHall_Text_DoorOpen:
	.string "The sun door grinds open.\p"
	.string "A smell of incense, sunscreen and\n"
	.string "regret drifts out.$"

ScorchedSlab_SunHall_Text_SunDoor:
	.string "Words are carved into the sealed door.\p"
	.string "“GIVE EACH SUN ITS STONE,\n"
	.string "AND THE DOOR SHALL KNOW DAY.”\p"
	.string "Underneath, in smaller letters:\n"
	.string "“Strength recommended. Lifting with\l"
	.string "the knees also recommended.”$"

ScorchedSlab_SunHall_Text_SunDoorNight:
	.string "It's night outside. The light from\n"
	.string "the ceiling is moonlight.\p"
	.string "The temple doesn't seem to care.\n"
	.string "Light is light. Very progressive.$"

ScorchedSlab_SunHall_Text_SunDoorOpen:
	.string "The sun door stands open.\n"
	.string "It looks smug about it.$"

ScorchedSlab_SunHall_Text_RayIntro:
	.string "Shh! I'm worshipping!\p"
	.string "Thirty years I've stared directly\n"
	.string "into the holy light. I can't see you\l"
	.string "at all. That's how devoted I am.$"

ScorchedSlab_SunHall_Text_RayDefeat:
	.string "A sunburn on my soul…\n"
	.string "SPF can't fix that.$"

ScorchedSlab_SunHall_Text_RayPostBattle:
	.string "The stones go in the light. Everybody\n"
	.string "knows that. I just never had Strength.\p"
	.string "Or a POKéMON that can push.\n"
	.string "Or friends. The sun is my friend.$"
