Underwater_Route129_MapScripts::
	map_script MAP_SCRIPT_ON_RESUME, Underwater_Route129_OnResume
	.byte 0

Underwater_Route129_OnResume:
	call AbnormalWeather_Underwater_SetupEscapeWarp
	end

@ --- zee_vulling_1 (gegenereerd door tools/grounded/maptools/zee_vulling_1.py) ---

@ --- einde zee_vulling_1 ---

@ --- zee_vulling_3 (gegenereerd door tools/grounded/maptools/zee_vulling_3.py) ---
Underwater_Route129_EventScript_ZV3Chest::
	msgbox Underwater_Route129_Text_ZV3Chest, MSGBOX_SIGN
	end

Underwater_Route129_Text_ZV3Chest:
	.string "A rotten chest with an X on the lid.\nInside, a note:\p'THE REAL TREASURE WAS THE FRIENDS\nWE DROWNED ALONG THE WAY.\l-CAPT. REDBEARD'\pP.S. 'Three steps east. Don't tell\nthe friends.'$"
@ --- einde zee_vulling_3 ---

@ --- zee_vulling_4 (gegenereerd door tools/grounded/maptools/zee_vulling_4.py) ---
Underwater_Route129_EventScript_ZV4Diver::
	msgbox Underwater_Route129_Text_ZV4Diver, MSGBOX_NPC
	end

Underwater_Route129_Text_ZV4Diver:
	.string "I followed the captain's map. X\nmarks the spot. I dug for a week.\pFound a note. The note said: 'THREE\nSTEPS EAST'. I took three steps.\pSomebody had already been there.\nStory of my life. Also of my wife.$"
@ --- einde zee_vulling_4 ---
