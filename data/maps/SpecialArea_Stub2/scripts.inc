@ Project Grounded: lege plek van Birth Island (geschrapt). De kaart blijft bestaan zodat de kaartnummers erna
@ (Trainer Hill, Navel Rock, Stadium, Spire, ...) in bestaande saves gelijk blijven. Geen toegang.
SpecialArea_Stub2_MapScripts::
	map_script MAP_SCRIPT_ON_FRAME_TABLE, SpecialArea_Stub2_OnFrame
	.byte 0

SpecialArea_Stub2_OnFrame:
	map_script_2 VAR_TEMP_0, 0, SpecialArea_Stub2_EventScript_Leave
	.2byte 0

SpecialArea_Stub2_EventScript_Leave::
	setvar VAR_TEMP_0, 1
	warp MAP_LILYCOVE_CITY_HARBOR, 8, 11
	waitstate
	end
