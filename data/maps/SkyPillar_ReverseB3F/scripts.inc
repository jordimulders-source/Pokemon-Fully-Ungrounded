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
	@ Spacetime S2: verslagen = hij blijft (de Spacetime-gang opent pas als Giratina gevangen is)
	goto_if_eq VAR_RESULT, B_OUTCOME_WON, SkyPillar_ReverseB3F_EventScript_GiratinaStays
	fadescreenswapbuffers FADE_TO_BLACK
	removeobject LOCALID_SKY_PILLAR_REVERSE_GIRATINA
	setflag FLAG_HIDE_SKY_PILLAR_GIRATINA
	fadescreenswapbuffers FADE_FROM_BLACK
SkyPillar_ReverseB3F_EventScript_GiratinaStays::
	releaseall
	end

SkyPillar_ReverseB3F_Text_Giratina:
	.string "ARCEUS banished this one down here for\n"
	.string "being rude. That was a few thousand\l"
	.string "years ago.\p"
	.string "It has had a lot of time to get ruder.$"
