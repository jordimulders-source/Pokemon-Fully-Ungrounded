@ Project Grounded: omgekeerde Sky Pillar B3F (5F op zijn kop): Giratina zweeft voor de put (lv 70, Origin Forme
@ met Griseous Core, eigen transitie B_TRANSITION_GIRATINA en de Giratina-muziek uit Platinum)
SkyPillar_ReverseB3F_MapScripts::
	.byte 0

SkyPillar_ReverseB3F_EventScript_Giratina::
	lockall
	faceplayer
	playmoncry SPECIES_GIRATINA_ORIGIN, CRY_MODE_ENCOUNTER
	waitmoncry
	msgbox SkyPillar_ReverseB3F_Text_Giratina, MSGBOX_DEFAULT
	setwildbattle SPECIES_GIRATINA_ORIGIN, 70, ITEM_GRISEOUS_CORE
	setflag FLAG_SYS_CTRL_OBJ_DELETE
	special BattleSetup_StartLegendaryBattle
	waitstate
	clearflag FLAG_SYS_CTRL_OBJ_DELETE
	specialvar VAR_RESULT, GetBattleOutcome
	goto_if_eq VAR_RESULT, B_OUTCOME_RAN, SkyPillar_ReverseB3F_EventScript_GiratinaStays
	goto_if_eq VAR_RESULT, B_OUTCOME_PLAYER_TELEPORTED, SkyPillar_ReverseB3F_EventScript_GiratinaStays
	fadescreenswapbuffers FADE_TO_BLACK
	removeobject LOCALID_SKY_PILLAR_REVERSE_GIRATINA
	setflag FLAG_HIDE_SKY_PILLAR_GIRATINA
	fadescreenswapbuffers FADE_FROM_BLACK
SkyPillar_ReverseB3F_EventScript_GiratinaStays::
	releaseall
	end

SkyPillar_ReverseB3F_Text_Giratina:
	.string "Rayquaza guards the sky.\n"
	.string "This one guards the bit underneath\l"
	.string "that nobody ever cleans.\p"
	.string "It has been banished down here for\n"
	.string "being rude. It looks ready to be\l"
	.string "rude again.$"
