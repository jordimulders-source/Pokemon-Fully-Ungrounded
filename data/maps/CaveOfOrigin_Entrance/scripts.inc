CaveOfOrigin_Entrance_MapScripts::
	map_script MAP_SCRIPT_ON_RESUME, CaveOfOrigin_Entrance_OnResume
	.byte 0

CaveOfOrigin_Entrance_OnResume:
	setescapewarp MAP_SOOTOPOLIS_CITY, 31, 17
	end

@ --- kaart_vulling_4 (gegenereerd door tools/grounded/maptools/kaart_vulling_4.py) ---
CaveOfOrigin_Entrance_EventScript_KV4Reporter::
	msgbox CaveOfOrigin_Entrance_Text_KV4Reporter, MSGBOX_NPC
	end

CaveOfOrigin_Entrance_Text_KV4Reporter:
	.string "This is GABBY's backup, live from\nthe end of the world!\pOur sources say the sky and the sea\nare fighting. Our other sources say\lthat's every Tuesday in HOENN.\pBack to you in the studio. Hello?\nIs there still a studio?$"
@ --- einde kaart_vulling_4 ---
