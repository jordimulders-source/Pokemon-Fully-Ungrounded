SootopolisCity_House4_MapScripts::
	.byte 0

SootopolisCity_House4_EventScript_Man::
	msgbox SootopolisCity_House4_Text_AncientTreasuresWaitingInSea, MSGBOX_NPC
	end

SootopolisCity_House4_EventScript_Woman::
	msgbox SootopolisCity_House4_Text_StrollUnderwaterWithPokemon, MSGBOX_NPC
	end

SootopolisCity_House4_EventScript_Azumarill::
	lock
	faceplayer
	waitse
	playmoncry SPECIES_AZUMARILL, CRY_MODE_NORMAL
	msgbox SootopolisCity_House4_Text_Azumarill, MSGBOX_DEFAULT
	waitmoncry
	release
	end

SootopolisCity_House4_Text_AncientTreasuresWaitingInSea:
	.string "Listen up.\p"
	.string "There's an ancient ruin in the sea\n"
	.string "around here.\p"
	.string "Like ATLANTIS. With POKéMON. And\n"
	.string "treasure.$"

SootopolisCity_House4_Text_StrollUnderwaterWithPokemon:
	.string "Ancient treasures… Maybe they exist,\n"
	.string "maybe not.\p"
	.string "An underwater stroll with my POKéMON\n"
	.string "would be lovely anyway.\p"
	.string "If I could hold my breath longer than 8\n"
	.string "seconds.$"

SootopolisCity_House4_Text_Azumarill:
	.string "AZUMARILL: Marurii.$"

