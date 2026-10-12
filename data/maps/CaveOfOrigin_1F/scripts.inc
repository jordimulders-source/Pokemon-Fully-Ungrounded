CaveOfOrigin_1F_MapScripts::
	map_script MAP_SCRIPT_ON_TRANSITION, CaveOfOrigin_1F_OnTransition
	.byte 0

CaveOfOrigin_1F_OnTransition:
	call_if_set FLAG_UNUSED_RS_LEGENDARY_BATTLE_DONE, CaveOfOrigin_EventScript_DisableTriggers
	end

@ --- kaart_vulling_4 (gegenereerd door tools/grounded/maptools/kaart_vulling_4.py) ---
CaveOfOrigin_1F_EventScript_KV4Grunt::
	trainerbattle_single TRAINER_KV4_MAGMA_GRUNT_ORIGIN, CaveOfOrigin_1F_Text_KV4Grunt_Intro, CaveOfOrigin_1F_Text_KV4Grunt_Defeat
	msgbox CaveOfOrigin_1F_Text_KV4Grunt_Post, MSGBOX_AUTOCLOSE
	end

CaveOfOrigin_1F_Text_KV4Grunt_Intro:
	.string "I quit TEAM MAGMA this morning.\nI'm still in the uniform. It's\lthe only clean thing I own.$"

CaveOfOrigin_1F_Text_KV4Grunt_Defeat:
	.string "Even unemployed, I lose.$"

CaveOfOrigin_1F_Text_KV4Grunt_Post:
	.string "I came to watch the apocalypse up\nclose. You know. For closure.\pIt's mostly just humid.$"
@ --- einde kaart_vulling_4 ---
