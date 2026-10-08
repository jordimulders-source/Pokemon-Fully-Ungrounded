@ Project Grounded: de diepzeetrog onder Route 127 (zwemgat in de kop van de centrale trog van onderwater 127,
@ 24,13). Kopie van Underwater_SealedChamber, 14 rijen dieper. Bovenkomen = terug naar het diepe water van Route 127.
@ Kaart: tools/grounded/maptools/zee_vulling_4.py
Underwater_Route127_Trench_MapScripts::
	map_script MAP_SCRIPT_ON_DIVE_WARP, Underwater_Route127_Trench_OnDive
	.byte 0

Underwater_Route127_Trench_OnDive:
	setdivewarp MAP_ROUTE127, 24, 14
	end

@ --- zee_vulling_4 (gegenereerd door tools/grounded/maptools/zee_vulling_4.py) ---
Underwater_Route127_Trench_EventScript_ZV4Abyssa::
	trainerbattle_single TRAINER_DIVER_ABYSSA, Underwater_Route127_Trench_Text_ZV4Abyssa_Intro, Underwater_Route127_Trench_Text_ZV4Abyssa_Defeat
	msgbox Underwater_Route127_Trench_Text_ZV4Abyssa_Post, MSGBOX_AUTOCLOSE
	end

Underwater_Route127_Trench_Text_ZV4Abyssa_Intro:
	.string "I'm going to touch the bottom of\nthe deepest trench in HOENN.\pThen I'm going to come back up and\ntell people. That's the hard part.$"

Underwater_Route127_Trench_Text_ZV4Abyssa_Defeat:
	.string "Fine. You can touch it first.\nIt's just sand. I knew it.$"

Underwater_Route127_Trench_Text_ZV4Abyssa_Post:
	.string "Down there, the pressure is like\nforty WAILORD sitting on you.\pI've had worse family reunions.$"

Underwater_Route127_Trench_EventScript_ZV4Bottom::
	msgbox Underwater_Route127_Trench_Text_ZV4Bottom, MSGBOX_SIGN
	end

Underwater_Route127_Trench_Text_ZV4Bottom:
	.string "A plaque, bolted to the rock:\p'DEEPEST POINT IN HOENN.\pDEPTH: MORE THAN OUR TECHNOLOGY\nCOULD RELIABLY MEASURE.'\pUnderneath, smaller:\n'The research team turned back\lhere. The LANTURN did not.'$"
@ --- einde zee_vulling_4 ---
