Underwater_Route128_MapScripts::
	.byte 0

@ --- zee_vulling_1 (gegenereerd door tools/grounded/maptools/zee_vulling_1.py) ---

@ --- einde zee_vulling_1 ---

@ --- zee_vulling_3 (gegenereerd door tools/grounded/maptools/zee_vulling_3.py) ---
Underwater_Route128_EventScript_ZV3Mailbag::
	msgbox Underwater_Route128_Text_ZV3Mailbag, MSGBOX_SIGN
	end

Underwater_Route128_Text_ZV3Mailbag:
	.string "A mailbag, sealed tight. One letter\nhas floated out:\p'Dear Mom, the cruise is lovely.\nThe captain says KYOGRE is a myth.\lMore soon!'\pThere was no more soon.$"
@ --- einde zee_vulling_3 ---

@ --- zee_vulling_4 (gegenereerd door tools/grounded/maptools/zee_vulling_4.py) ---
Underwater_Route128_EventScript_ZV4Brine::
	trainerbattle_single TRAINER_DIVER_BRINE, Underwater_Route128_Text_ZV4Brine_Intro, Underwater_Route128_Text_ZV4Brine_Defeat
	msgbox Underwater_Route128_Text_ZV4Brine_Post, MSGBOX_AUTOCLOSE
	end

Underwater_Route128_Text_ZV4Brine_Intro:
	.string "A submarine came through here once.\nTeam AQUA. Very loud. No manners.\pEver since, I check everyone.\nArms up. Fins out.$"

Underwater_Route128_Text_ZV4Brine_Defeat:
	.string "You're clean. Suspiciously clean.\nNobody's that clean underwater.$"

Underwater_Route128_Text_ZV4Brine_Post:
	.string "The sub left a smell down there.\nThe smell is still here.\lIt has a name now. Gary.$"
@ --- einde zee_vulling_4 ---
