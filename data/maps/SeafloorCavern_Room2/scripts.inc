SeafloorCavern_Room2_MapScripts::
	.byte 0

@ --- kaart_vulling_4 (gegenereerd door tools/grounded/maptools/kaart_vulling_4.py) ---
SeafloorCavern_Room2_EventScript_KV4Grunt::
	trainerbattle_single TRAINER_KV4_AQUA_GRUNT_SEAFLOOR, SeafloorCavern_Room2_Text_KV4Grunt_Intro, SeafloorCavern_Room2_Text_KV4Grunt_Defeat
	msgbox SeafloorCavern_Room2_Text_KV4Grunt_Post, MSGBOX_AUTOCLOSE
	end

SeafloorCavern_Room2_Text_KV4Grunt_Intro:
	.string "Is it over? Did we win? Nobody\ntold me anything. I'm guarding a\lrock. It's a very important rock.$"

SeafloorCavern_Room2_Text_KV4Grunt_Defeat:
	.string "Ow. So that's a yes to\n“did we lose”,\lwasn't it?$"

SeafloorCavern_Room2_Text_KV4Grunt_Post:
	.string "The BOSS said “stay here until I\ncome back”. That was three weeks\lago. I named the rock. It's Gary.$"
@ --- einde kaart_vulling_4 ---
