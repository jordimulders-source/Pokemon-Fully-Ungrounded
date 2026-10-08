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

@ --- zee_vulling_4 (gegenereerd door tools/grounded/maptools/zee_vulling_4.py) ---
Underwater_Route125_EventScript_ZV4Gill::
	trainerbattle_single TRAINER_DIVER_GILL, Underwater_Route125_Text_ZV4Gill_Intro, Underwater_Route125_Text_ZV4Gill_Defeat
	msgbox Underwater_Route125_Text_ZV4Gill_Post, MSGBOX_AUTOCLOSE
	end

Underwater_Route125_Text_ZV4Gill_Intro:
	.string "Have you seen my son? He's a\nCLAUNCHER. Small. One big claw.\pHe's 34. He said he needed space.\nThe ocean is mostly space.$"

Underwater_Route125_Text_ZV4Gill_Defeat:
	.string "You fight like his mother.\nAlso a CLAUNCHER.$"

Underwater_Route125_Text_ZV4Gill_Post:
	.string "If you see him, tell him his room\nis still a rock. Same rock.\lI didn't touch it.$"
@ --- einde zee_vulling_4 ---
