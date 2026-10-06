Underwater_Route125_MapScripts::
	map_script MAP_SCRIPT_ON_RESUME, Underwater_Route125_OnResume
	.byte 0

Underwater_Route125_OnResume:
	call AbnormalWeather_Underwater_SetupEscapeWarp
	end

@ --- zee_vulling_1 (gegenereerd door tools/grounded/maptools/zee_vulling_1.py) ---
Underwater_Route125_EventScript_ZVDiver::
	msgbox Underwater_Route125_Text_ZVDiver, MSGBOX_NPC
	end

Underwater_Route125_Text_ZVDiver:
	.string "...!\p(He is holding his breath for\ncharity. He points at a sign:)\p'DAY 3. DON'T MAKE ME LAUGH.'\p(His face is very blue. It could\nbe the water. It is not the water.)$"
@ --- einde zee_vulling_1 ---
