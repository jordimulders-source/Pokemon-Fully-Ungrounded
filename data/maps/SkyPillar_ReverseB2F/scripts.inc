@ Project Grounded: omgekeerde Sky Pillar B2F (2F op zijn kop). Hier zijn boven en onder omgedraaid
@ (DoCB1_Overworld in src/overworld.c wisselt UP en DOWN op deze kaart).
SkyPillar_ReverseB2F_MapScripts::
	map_script MAP_SCRIPT_ON_FRAME_TABLE, SkyPillar_ReverseB2F_OnFrame
	.byte 0

SkyPillar_ReverseB2F_OnFrame:
	map_script_2 VAR_SKY_PILLAR_REVERSE_STATE, 3, SkyPillar_ReverseB2F_EventScript_Arrived
	.2byte 0

SkyPillar_ReverseB2F_EventScript_Arrived::
	lockall
	delay 30
	msgbox SkyPillar_ReverseB2F_Text_Arrived, MSGBOX_DEFAULT
	setvar VAR_SKY_PILLAR_REVERSE_STATE, 4
	releaseall
	end

SkyPillar_ReverseB2F_Text_Arrived:
	.string "Your inner ear files a complaint.\n"
	.string "Gravity here misread the instructions.\p"
	.string "Up is down. Down is up. Left is still left.\n"
	.string "Don't get used to it.$"
