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
