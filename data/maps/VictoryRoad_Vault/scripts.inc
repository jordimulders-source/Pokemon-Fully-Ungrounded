@ Project Grounded: kluis van Hiker Gordon (Victory Road B1F). Strength-blokpuzzel, opgelost en
@ gecontroleerd door tools/grounded/maptools/victory_road_ext.py; de blokken staan bij elk bezoek terug.
VictoryRoad_Vault_MapScripts::
	.byte 0

VictoryRoad_Vault_EventScript_Sign::
	msgbox VictoryRoad_Vault_Text_Sign, MSGBOX_SIGN
	end

VictoryRoad_Vault_Text_Sign:
	.string "Something is scratched into the wall.\p"
	.string "PRIVATE VAULT OF HIKER GORDON.\n"
	.string "Protected by an unsolvable boulder\l"
	.string "puzzle.\p"
	.string "If you can read this, you are\n"
	.string "already inside. Please leave.\p"
	.string "PS: Pushing things down from above\n"
	.string "never solved anything. Ask my ex.$"
