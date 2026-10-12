MeteorFalls_CraterRoom_MapScripts::
	map_script MAP_SCRIPT_ON_TRANSITION, MeteorFalls_CraterRoom_OnTransition
	.byte 0

@ Project Grounded: 25% kans op een willekeurige static encounter midden in de kamer.
@ VAR_TEMP_1 = gekozen soort (0-5), FLAG_TEMP_11 verbergt de Pokémon.
MeteorFalls_CraterRoom_OnTransition:
	setflag FLAG_TEMP_11
	random 4
	goto_if_ne VAR_RESULT, 0, MeteorFalls_CraterRoom_OnTransition_End
	random 6
	copyvar VAR_TEMP_1, VAR_RESULT
	call_if_eq VAR_TEMP_1, 0, MeteorFalls_CraterRoom_EventScript_SetGfx_BAGON
	call_if_eq VAR_TEMP_1, 1, MeteorFalls_CraterRoom_EventScript_SetGfx_DEINO
	call_if_eq VAR_TEMP_1, 2, MeteorFalls_CraterRoom_EventScript_SetGfx_LAPRAS
	call_if_eq VAR_TEMP_1, 3, MeteorFalls_CraterRoom_EventScript_SetGfx_MIENFOO
	call_if_eq VAR_TEMP_1, 4, MeteorFalls_CraterRoom_EventScript_SetGfx_MINIOR_METEOR
	call_if_eq VAR_TEMP_1, 5, MeteorFalls_CraterRoom_EventScript_SetGfx_CARBINK
	clearflag FLAG_TEMP_11
MeteorFalls_CraterRoom_OnTransition_End:
	end

MeteorFalls_CraterRoom_EventScript_SetGfx_BAGON:
	setvar VAR_OBJ_GFX_ID_0, OBJ_EVENT_GFX_SPECIES(BAGON)
	return

MeteorFalls_CraterRoom_EventScript_SetGfx_DEINO:
	setvar VAR_OBJ_GFX_ID_0, OBJ_EVENT_GFX_SPECIES(DEINO)
	return

MeteorFalls_CraterRoom_EventScript_SetGfx_LAPRAS:
	setvar VAR_OBJ_GFX_ID_0, OBJ_EVENT_GFX_SPECIES(LAPRAS)
	return

MeteorFalls_CraterRoom_EventScript_SetGfx_MIENFOO:
	setvar VAR_OBJ_GFX_ID_0, OBJ_EVENT_GFX_SPECIES(MIENFOO)
	return

MeteorFalls_CraterRoom_EventScript_SetGfx_MINIOR_METEOR:
	setvar VAR_OBJ_GFX_ID_0, OBJ_EVENT_GFX_SPECIES(MINIOR_METEOR)
	return

MeteorFalls_CraterRoom_EventScript_SetGfx_CARBINK:
	setvar VAR_OBJ_GFX_ID_0, OBJ_EVENT_GFX_SPECIES(CARBINK)
	return

MeteorFalls_CraterRoom_EventScript_StaticMon::
	lock
	faceplayer
	goto_if_eq VAR_TEMP_1, 0, MeteorFalls_CraterRoom_EventScript_Battle_BAGON
	goto_if_eq VAR_TEMP_1, 1, MeteorFalls_CraterRoom_EventScript_Battle_DEINO
	goto_if_eq VAR_TEMP_1, 2, MeteorFalls_CraterRoom_EventScript_Battle_LAPRAS
	goto_if_eq VAR_TEMP_1, 3, MeteorFalls_CraterRoom_EventScript_Battle_MIENFOO
	goto_if_eq VAR_TEMP_1, 4, MeteorFalls_CraterRoom_EventScript_Battle_MINIOR_METEOR
	goto_if_eq VAR_TEMP_1, 5, MeteorFalls_CraterRoom_EventScript_Battle_CARBINK
	release
	end

MeteorFalls_CraterRoom_EventScript_Battle_BAGON:
	playmoncry SPECIES_BAGON, CRY_MODE_ENCOUNTER
	waitmoncry
	setwildbattle SPECIES_BAGON, 30
	goto MeteorFalls_CraterRoom_EventScript_DoBattle

MeteorFalls_CraterRoom_EventScript_Battle_DEINO:
	playmoncry SPECIES_DEINO, CRY_MODE_ENCOUNTER
	waitmoncry
	setwildbattle SPECIES_DEINO, 30
	goto MeteorFalls_CraterRoom_EventScript_DoBattle

MeteorFalls_CraterRoom_EventScript_Battle_LAPRAS:
	playmoncry SPECIES_LAPRAS, CRY_MODE_ENCOUNTER
	waitmoncry
	setwildbattle SPECIES_LAPRAS, 33
	goto MeteorFalls_CraterRoom_EventScript_DoBattle

MeteorFalls_CraterRoom_EventScript_Battle_MIENFOO:
	playmoncry SPECIES_MIENFOO, CRY_MODE_ENCOUNTER
	waitmoncry
	setwildbattle SPECIES_MIENFOO, 30
	goto MeteorFalls_CraterRoom_EventScript_DoBattle

MeteorFalls_CraterRoom_EventScript_Battle_MINIOR_METEOR:
	playmoncry SPECIES_MINIOR_METEOR, CRY_MODE_ENCOUNTER
	waitmoncry
	setwildbattle SPECIES_MINIOR_METEOR, 30
	goto MeteorFalls_CraterRoom_EventScript_DoBattle

MeteorFalls_CraterRoom_EventScript_Battle_CARBINK:
	playmoncry SPECIES_CARBINK, CRY_MODE_ENCOUNTER
	waitmoncry
	setwildbattle SPECIES_CARBINK, 30
	goto MeteorFalls_CraterRoom_EventScript_DoBattle

MeteorFalls_CraterRoom_EventScript_DoBattle:
	dowildbattle
	removeobject LOCALID_CRATER_ROOM_STATIC
	setflag FLAG_TEMP_11
	release
	end
