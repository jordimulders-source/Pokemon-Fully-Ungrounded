Underwater_Route105_MapScripts::
	map_script MAP_SCRIPT_ON_RESUME, Underwater_Route105_OnResume
	.byte 0

Underwater_Route105_OnResume:
	call AbnormalWeather_Underwater_SetupEscapeWarp
	end

@ --- zee_vulling_1 (gegenereerd door tools/grounded/maptools/zee_vulling_1.py) ---
Underwater_Route105_EventScript_ZVGrave::
	msgbox Underwater_Route105_Text_ZVGrave, MSGBOX_SIGN
	end

Underwater_Route105_Text_ZVGrave:
	.string "Words are carved into the rock:\p'HERE LIES CAPTAIN BARNABY.\nHE SAID HE COULD HOLD HIS BREATH\lFOR AN HOUR.'\p'HE COULD NOT.'$"
@ --- einde zee_vulling_1 ---

@ --- zee_vulling_4 (gegenereerd door tools/grounded/maptools/zee_vulling_4.py) ---
Underwater_Route105_EventScript_ZV4Nerissa::
	trainerbattle_single TRAINER_DIVER_NERISSA, Underwater_Route105_Text_ZV4Nerissa_Intro, Underwater_Route105_Text_ZV4Nerissa_Defeat
	msgbox Underwater_Route105_Text_ZV4Nerissa_Post, MSGBOX_AUTOCLOSE
	end

Underwater_Route105_Text_ZV4Nerissa_Intro:
	.string "Shh! I'm going for the record.\nEleven minutes on one breath.\pI'm at minute ten. Talking costs\nair. Battling costs air.\lLet's do it anyway.$"

Underwater_Route105_Text_ZV4Nerissa_Defeat:
	.string "...!\n(She gives a thumbs up. Or down.)$"

Underwater_Route105_Text_ZV4Nerissa_Post:
	.string "New plan: the record is for\nMOST BATTLES ON ONE BREATH.\lI'm currently the world champion.$"
@ --- einde zee_vulling_4 ---
