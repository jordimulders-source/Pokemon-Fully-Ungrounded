SkyPillar_Outside_MapScripts::
	map_script MAP_SCRIPT_ON_TRANSITION, SkyPillar_Outside_OnTransition
	map_script MAP_SCRIPT_ON_LOAD, SkyPillar_Outside_OnLoad
	map_script MAP_SCRIPT_ON_FRAME_TABLE, SkyPillar_Outside_OnFrame
	.byte 0

SkyPillar_Outside_OnTransition:
	call SkyPillar_Outside_EventScript_SetZinniaVisibility
	call_if_eq VAR_SOOTOPOLIS_CITY_STATE, 3, SkyPillar_Outside_EventScript_HideMapNamePopup
	call_if_ge VAR_SOOTOPOLIS_CITY_STATE, 4, SkyPillar_Outside_EventScript_CheckSetAbnormalWeather
	end

SkyPillar_Outside_EventScript_HideMapNamePopup::
	setflag FLAG_HIDE_MAP_NAME_POPUP
	return

SkyPillar_Outside_EventScript_CheckSetAbnormalWeather::
	call_if_set FLAG_SYS_WEATHER_CTRL, Common_EventScript_SetAbnormalWeather
	return

SkyPillar_Outside_OnLoad:
	call_if_set FLAG_WALLACE_GOES_TO_SKY_PILLAR, SkyPillar_Outside_EventScript_OpenDoor
	end

SkyPillar_Outside_EventScript_OpenDoor::
	setmetatile 14, 4, METATILE_Pacifidlog_SkyPillar_DoorOpen_Top, FALSE
	setmetatile 14, 5, METATILE_Pacifidlog_SkyPillar_DoorOpen_Bottom, FALSE
	return

SkyPillar_Outside_OnFrame:
	map_script_2 VAR_SOOTOPOLIS_CITY_STATE, 3, SkyPillar_Outside_EventScript_WallaceScene
	.2byte 0

SkyPillar_Outside_EventScript_WallaceScene::
	lockall
	applymovement LOCALID_SKY_PILLAR_WALLACE, SkyPillar_Outside_Movement_WallaceApproachPlayer
	waitmovement 0
	applymovement LOCALID_PLAYER, Common_Movement_WalkInPlaceFasterLeft
	waitmovement 0
	msgbox SkyPillar_Outside_Text_OpenedDoorToSkyPillar, MSGBOX_DEFAULT
	closemessage
	delay 30
	setvar VAR_0x8004, 1  @ vertical pan
	setvar VAR_0x8005, 1  @ horizontal pan
	setvar VAR_0x8006, 8  @ num shakes
	setvar VAR_0x8007, 3  @ shake delay
	special ShakeCamera
	waitstate
	delay 40
	msgbox SkyPillar_Outside_Text_EarthquakeNotMomentToWaste, MSGBOX_DEFAULT
	closemessage
	applymovement LOCALID_PLAYER, SkyPillar_Outside_Movement_PlayerClimbSkyPillar
	applymovement LOCALID_SKY_PILLAR_WALLACE, SkyPillar_Outside_Movement_WallaceClimbSkyPillar
	waitmovement 0
	setvar VAR_0x8004, 1   @ vertical pan
	setvar VAR_0x8005, 3   @ horizontal pan
	setvar VAR_0x8006, 20  @ num shakes
	setvar VAR_0x8007, 5   @ shake delay
	special ShakeCamera
	waitstate
	delay 20
	applymovement LOCALID_SKY_PILLAR_WALLACE, Common_Movement_WalkInPlaceFasterLeft
	waitmovement 0
	delay 10
	applymovement LOCALID_SKY_PILLAR_WALLACE, Common_Movement_WalkInPlaceFasterRight
	waitmovement 0
	delay 20
	applymovement LOCALID_SKY_PILLAR_WALLACE, Common_Movement_WalkInPlaceFasterDown
	waitmovement 0
	delay 30
	msgbox SkyPillar_Outside_Text_SituationGettingWorse, MSGBOX_DEFAULT
	closemessage
	setflag FLAG_SYS_WEATHER_CTRL
	setweather WEATHER_ABNORMAL
	doweather
	special WaitWeather
	waitstate
	delay 30
	msgbox SkyPillar_Outside_Text_GotToGoBackForSootopolis, MSGBOX_DEFAULT
	closemessage
	playse SE_EXIT
	fadescreenswapbuffers FADE_TO_BLACK
	clearflag FLAG_HIDE_MAP_NAME_POPUP
	setvar VAR_SOOTOPOLIS_CITY_STATE, 4
	removeobject LOCALID_SKY_PILLAR_WALLACE
	clearflag FLAG_HIDE_SOOTOPOLIS_CITY_WALLACE
	clearflag FLAG_HIDE_SKY_PILLAR_ZINNIA
	addobject LOCALID_SKY_PILLAR_ZINNIA
	fadescreenswapbuffers FADE_FROM_BLACK
	@ Project Grounded: Zinnia staat ineens voor de deur
	applymovement LOCALID_PLAYER, Common_Movement_WalkInPlaceFasterUp
	waitmovement 0
	call SkyPillar_Outside_EventScript_ZinniaTest
	releaseall
	end

SkyPillar_Outside_Movement_WallaceApproachPlayer:
	walk_down
	walk_down
	walk_down
	walk_down
	walk_down
	walk_down
	walk_down
	walk_right
	walk_right
	walk_right
	step_end

SkyPillar_Outside_Movement_WallaceClimbSkyPillar:
	walk_left
	walk_left
	walk_left
	walk_up
	walk_up
	walk_up
	walk_up
	walk_right
	walk_up
	walk_up
	walk_up
	walk_up
	step_end

SkyPillar_Outside_Movement_PlayerClimbSkyPillar:
	walk_left
	walk_left
	walk_left
	walk_left
	walk_up
	walk_up
	walk_up
	walk_up
	walk_right
	walk_up
	walk_up
	walk_up
	step_end

SkyPillar_Outside_EventScript_Wallace::
	end

SkyPillar_Outside_EventScript_ClosedDoor::
	msgbox SkyPillar_Outside_Text_DoorIsClosed, MSGBOX_SIGN
	end

SkyPillar_Outside_Text_DoorIsClosed:
	.string "The door is closed. It looks older than\n"
	.string "the concept of doors.$"

SkyPillar_Outside_Text_OpenedDoorToSkyPillar:
	.string "WALLACE: Oh my, how terribly rude of me!\p"
	.string "I was in such a hurry, I left you behind\n"
	.string "with the bottles!\p"
	.string "I've opened the door of the SKY PILLAR.\p"
	.string "{PLAYER}{KUN}, let's go! The vintage waits for\n"
	.string "no one!$"

SkyPillar_Outside_Text_EarthquakeNotMomentToWaste:
	.string "WALLACE: An earthquake! My cellar!\p"
	.string "There's not a moment to waste! Hurry!$"

SkyPillar_Outside_Text_SituationGettingWorse:
	.string "WALLACE: Hmm… This is getting worse.\n"
	.string "And I'm getting sober.$"

SkyPillar_Outside_Text_GotToGoBackForSootopolis:
	.string "WALLACE: This isn't good…\p"
	.string "The weather chaos has even reached\n"
	.string "this place…\p"
	.string "{PLAYER}{KUN}.\p"
	.string "RAYQUAZA should be up at the top.\p"
	.string "I'm worried about SOOTOPOLIS. And my\n"
	.string "wine cellar. Mostly SOOTOPOLIS. I have\l"
	.string "to go back.\p"
	.string "It's all up to you now. Don't fail us!$"

@ ---------------------------------------------------------------- Project Grounded: Zinnia test of je klaar bent voor Rayquaza
@ Alleen tijdens de klim naar Rayquaza (VAR_SOOTOPOLIS_CITY_STATE 4); ze blokkeert de deur tot je haar verslaat.
SkyPillar_Outside_EventScript_SetZinniaVisibility::
	setflag FLAG_HIDE_SKY_PILLAR_ZINNIA
	goto_if_ne VAR_SOOTOPOLIS_CITY_STATE, 4, Common_EventScript_NopReturn
	goto_if_defeated TRAINER_ZINNIA, Common_EventScript_NopReturn
	clearflag FLAG_HIDE_SKY_PILLAR_ZINNIA
	return

SkyPillar_Outside_EventScript_Zinnia::
	lock
	faceplayer
	call SkyPillar_Outside_EventScript_ZinniaTest
	release
	end

SkyPillar_Outside_EventScript_ZinniaTest::
	playse SE_PIN
	applymovement LOCALID_SKY_PILLAR_ZINNIA, Common_Movement_ExclamationMark
	waitmovement 0
	msgbox SkyPillar_Outside_Text_ZinniaIntro, MSGBOX_DEFAULT
	trainerbattle_no_intro TRAINER_ZINNIA, SkyPillar_Outside_Text_ZinniaDefeat
	msgbox SkyPillar_Outside_Text_ZinniaPostBattle, MSGBOX_DEFAULT
	closemessage
	fadescreen FADE_TO_BLACK
	removeobject LOCALID_SKY_PILLAR_ZINNIA
	setflag FLAG_HIDE_SKY_PILLAR_ZINNIA
	fadescreen FADE_FROM_BLACK
	return

SkyPillar_Outside_Text_ZinniaIntro:
	.string "???: Hold it right there, kid.\p"
	.string "Name's ZINNIA. I'm a LOREKEEPER. I keep\n"
	.string "the lore. All of it. Which is a problem,\l"
	.string "because nobody can follow it anymore.\l"
	.string "Including me.\p"
	.string "So. RAYQUAZA. Let me explain. The\n"
	.string "ancient Draconids worshipped RAYQUAZA.\l"
	.string "Then a splinter group worshipped the\l"
	.string "meteor RAYQUAZA ate.\p"
	.string "Then a splinter of that splinter\n"
	.string "worshipped the crater the meteor left.\l"
	.string "Then they had a schism about whether\l"
	.string "the crater counted as a hole or as an\l"
	.string "absence of ground.\p"
	.string "My great-grandmother's songs say\n"
	.string "RAYQUAZA ate the meteor. My\l"
	.string "great-aunt's songs say the meteor ate\l"
	.string "RAYQUAZA. The sacred tapestry says\l"
	.string "both, but somebody spilled soup on the\l"
	.string "important bit.\p"
	.string "There is also a prophecy. It's written in\n"
	.string "a language that only three people ever\l"
	.string "spoke, and two of them were the same\l"
	.string "person.\p"
	.string "And then there's the alternate timeline\n"
	.string "where all of this happened differently.\l"
	.string "Don't ask. I've been asked. I cried.\p"
	.string "Long story short: there's a very large,\n"
	.string "very cranky green noodle up there, and\l"
	.string "you're about to wake it.\p"
	.string "Show me you won't get eaten. That part\n"
	.string "of the lore, at least, is extremely\l"
	.string "consistent.$"

SkyPillar_Outside_Text_ZinniaDefeat:
	.string "Ha! Okay, okay. You might actually\n"
	.string "survive the noodle.$"

SkyPillar_Outside_Text_ZinniaPostBattle:
	.string "ZINNIA: Fine, the door's yours. Go up\n"
	.string "and wake RAYQUAZA.\p"
	.string "If it asks about the soup on the\n"
	.string "tapestry, it wasn't me.$"
