@ Project Grounded: omgekeerde Sky Pillar B1F (1F op zijn kop). Je valt hier binnen door het gat in 1F;
@ de ingangsmat bovenin leidt terug naar buiten. Bouwscript: tools/grounded/maptools/reverse_pillar.py
SkyPillar_ReverseB1F_MapScripts::
	map_script MAP_SCRIPT_ON_FRAME_TABLE, SkyPillar_ReverseB1F_OnFrame
	.byte 0

SkyPillar_ReverseB1F_OnFrame:
	map_script_2 VAR_SKY_PILLAR_REVERSE_STATE, 2, SkyPillar_ReverseB1F_EventScript_Landed
	.2byte 0

SkyPillar_ReverseB1F_EventScript_Landed::
	lockall
	delay 30
	msgbox SkyPillar_ReverseB1F_Text_Landed, MSGBOX_DEFAULT
	setvar VAR_SKY_PILLAR_REVERSE_STATE, 3
	releaseall
	end

SkyPillar_ReverseB1F_Text_Landed:
	.string "You landed on the ceiling. Which is now\n"
	.string "the floor.\p"
	.string "Welcome to the Upside Down. No kids on\n"
	.string "bikes, no waffles. Just you.\p"
	.string "The stairs only go down from here. Like\n"
	.string "your sense of direction.$"
