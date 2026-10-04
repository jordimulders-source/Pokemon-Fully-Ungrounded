SkyPillar_1F_MapScripts::
	map_script MAP_SCRIPT_ON_TRANSITION, SkyPillar_1F_OnTransition
	map_script MAP_SCRIPT_ON_LOAD, SkyPillar_1F_OnLoad
	map_script MAP_SCRIPT_ON_RESUME, SkyPillar_1F_OnResume
	map_script MAP_SCRIPT_ON_FRAME_TABLE, SkyPillar_1F_OnFrame
	.byte 0

SkyPillar_1F_OnTransition:
	call_if_lt VAR_SKY_PILLAR_STATE, 2, SkyPillar_1F_EventScript_CleanFloor
	call_if_set FLAG_DEFEATED_RAYQUAZA, SkyPillar_1F_EventScript_TryOpenRift
	end

SkyPillar_1F_EventScript_CleanFloor::
	setmaplayoutindex LAYOUT_SKY_PILLAR_1F_CLEAN
	return

@ Project Grounded: na Rayquaza scheurt de vloer open naar de omgekeerde Sky Pillar (Giratina)
SkyPillar_1F_EventScript_TryOpenRift::
	call_if_eq VAR_SKY_PILLAR_REVERSE_STATE, 0, SkyPillar_1F_EventScript_OpenRift
	return

SkyPillar_1F_EventScript_OpenRift::
	setvar VAR_SKY_PILLAR_REVERSE_STATE, 1
	return

SkyPillar_1F_OnLoad:
	call_if_set FLAG_DEFEATED_RAYQUAZA, SkyPillar_1F_EventScript_SetRift
	end

SkyPillar_1F_EventScript_SetRift::
	setmetatile 11, 11, METATILE_Pacifidlog_SkyPillar_CrackedFloor_Hole, FALSE
	return

SkyPillar_1F_OnResume:
	setholewarp MAP_SKY_PILLAR_REVERSE_B1F
	end

SkyPillar_1F_OnFrame:
	map_script_2 VAR_SKY_PILLAR_REVERSE_STATE, 1, SkyPillar_1F_EventScript_RiftScene
	.2byte 0

SkyPillar_1F_EventScript_RiftScene::
	lockall
	delay 20
	playse SE_M_EARTHQUAKE
	setvar VAR_0x8004, 1  @ vertical pan
	setvar VAR_0x8005, 0  @ horizontal pan
	setvar VAR_0x8006, 10 @ num shakes
	setvar VAR_0x8007, 4  @ shake delay
	special ShakeCamera
	waitstate
	playmoncry SPECIES_GIRATINA_ORIGIN, CRY_MODE_ENCOUNTER
	waitmoncry
	msgbox SkyPillar_1F_Text_Rift, MSGBOX_DEFAULT
	setvar VAR_SKY_PILLAR_REVERSE_STATE, 2
	releaseall
	end

SkyPillar_1F_Text_Rift:
	.string "The floor cracked open with a sound\n"
	.string "like a door being slammed backwards.\p"
	.string "Something down there just screamed.\n"
	.string "Or yawned. Hard to tell upside down.\p"
	.string "The tower apparently has a basement.\n"
	.string "Nobody mentioned a basement.$"
