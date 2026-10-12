Underwater_Route126_MapScripts::
	.byte 0

@ --- zee_vulling_4 (gegenereerd door tools/grounded/maptools/zee_vulling_4.py) ---
Underwater_Route126_EventScript_ZV4Odessa::
	trainerbattle_single TRAINER_DIVER_ODESSA, Underwater_Route126_Text_ZV4Odessa_Intro, Underwater_Route126_Text_ZV4Odessa_Defeat
	msgbox Underwater_Route126_Text_ZV4Odessa_Post, MSGBOX_AUTOCLOSE
	end

Underwater_Route126_Text_ZV4Odessa_Intro:
	.string "Welcome to the SOOTOPOLIS DIVE\nTOUR! On your left: rock.\pOn your right: also rock.\nTips are appreciated. Battles too.$"

Underwater_Route126_Text_ZV4Odessa_Defeat:
	.string "Tour's over. Please exit through\nthe gift shop. There is no gift\nshop.$"

Underwater_Route126_Text_ZV4Odessa_Post:
	.string "The rocks here are older than the\ncity. The city is older than me.\pI'm older than the rocks feel.\nIt's the job.$"

Underwater_Route126_EventScript_ZV4Stone::
	msgbox Underwater_Route126_Text_ZV4Stone, MSGBOX_SIGN
	end

Underwater_Route126_Text_ZV4Stone:
	.string "A carved stone, half buried:\p'HERE LIES THE FIRST SOOTOPOLIS\nSUBMARINE. IT WORKED PERFECTLY.\pIT JUST NEVER CAME BACK UP.'$"
@ --- einde zee_vulling_4 ---
