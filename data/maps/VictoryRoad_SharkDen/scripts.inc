@ Project Grounded: Garchomp-hol onder Victory Road (gat in de vloer van B1F (35,22)).
@ Vaste Garchomp lv 58 op een stapel rugzakken; de buit ligt eromheen. Ladder terug naar B1F (36,22).
VictoryRoad_SharkDen_MapScripts::
	.byte 0

VictoryRoad_SharkDen_EventScript_Garchomp::
	lock
	faceplayer
	msgbox VictoryRoad_SharkDen_Text_Garchomp, MSGBOX_DEFAULT
	playmoncry SPECIES_GARCHOMP, CRY_MODE_ENCOUNTER
	waitmoncry
	setwildbattle SPECIES_GARCHOMP, 81
	setflag FLAG_SYS_CTRL_OBJ_DELETE
	dowildbattle
	clearflag FLAG_SYS_CTRL_OBJ_DELETE
	specialvar VAR_RESULT, GetBattleOutcome
	goto_if_eq VAR_RESULT, B_OUTCOME_RAN, VictoryRoad_SharkDen_EventScript_GarchompStays
	goto_if_eq VAR_RESULT, B_OUTCOME_PLAYER_TELEPORTED, VictoryRoad_SharkDen_EventScript_GarchompStays
	removeobject LOCALID_VR_SHARK_DEN_GARCHOMP
	setflag FLAG_HIDE_VICTORY_ROAD_GARCHOMP
VictoryRoad_SharkDen_EventScript_GarchompStays::
	release
	end

VictoryRoad_SharkDen_EventScript_Backpacks::
	msgbox VictoryRoad_SharkDen_Text_Backpacks, MSGBOX_SIGN
	end

VictoryRoad_SharkDen_Text_Garchomp:
	.string "A GARCHOMP is asleep on a pile of\n"
	.string "backpacks. Some still have name tags.\p"
	.string "It smells faintly of the last three\n"
	.string "people who wanted to be CHAMPION.\p"
	.string "…It's awake now.$"

VictoryRoad_SharkDen_Text_Backpacks:
	.string "A heap of chewed-up backpacks.\p"
	.string "One name tag reads: “If found,\n"
	.string "I was almost CHAMPION.”$"
