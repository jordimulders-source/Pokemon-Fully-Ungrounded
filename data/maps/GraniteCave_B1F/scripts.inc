GraniteCave_B1F_MapScripts::
	map_script MAP_SCRIPT_ON_FRAME_TABLE, CaveHole_CheckFallDownHole
	map_script MAP_SCRIPT_ON_TRANSITION, CaveHole_FixCrackedGround
	map_script MAP_SCRIPT_ON_RESUME, GraniteCave_B1F_SetHoleWarp
	.byte 0

GraniteCave_B1F_SetHoleWarp:
	setstepcallback STEP_CB_CRACKED_FLOOR
	setholewarp MAP_GRANITE_CAVE_B2F
	end

@ --- kaart_vulling_4 (gegenereerd door tools/grounded/maptools/kaart_vulling_4.py) ---
GraniteCave_B1F_EventScript_KV4Spelunker::
	lock
	faceplayer
	goto_if_set FLAG_KV4_GRANITECAVE_B1F_GIFT_SPELUNKER, GraniteCave_B1F_EventScript_KV4Spelunker_After
	msgbox GraniteCave_B1F_Text_KV4Spelunker, MSGBOX_DEFAULT
	giveitem ITEM_HARD_STONE
	goto_if_eq VAR_RESULT, FALSE, Common_EventScript_ShowBagIsFull
	setflag FLAG_KV4_GRANITECAVE_B1F_GIFT_SPELUNKER
	release
	end
GraniteCave_B1F_EventScript_KV4Spelunker_After:
	msgbox GraniteCave_B1F_Text_KV4Spelunker_After, MSGBOX_DEFAULT
	release
	end

GraniteCave_B1F_Text_KV4Spelunker:
	.string "I've been mapping this cave for\ntwelve years. Look. My map.\p…Yes, it's a drawing of a man in\na suit. He walked past in year two.\lI got distracted.\pHe was looking for stones. Here.\nHave one. I have a lot of stones.$"

GraniteCave_B1F_Text_KV4Spelunker_After:
	.string "Year thirteen. I'm adding a hat.\nHe didn't have a hat. Artistic\lfreedom.$"

GraniteCave_B1F_EventScript_KV4Doug::
	trainerbattle_single TRAINER_KV4_HIKER_DOUG, GraniteCave_B1F_Text_KV4Doug_Intro, GraniteCave_B1F_Text_KV4Doug_Defeat
	msgbox GraniteCave_B1F_Text_KV4Doug_Post, MSGBOX_AUTOCLOSE
	end

GraniteCave_B1F_Text_KV4Doug_Intro:
	.string "Oi! You're standing in my\nfavourite dark spot!$"

GraniteCave_B1F_Text_KV4Doug_Defeat:
	.string "Fine. I'll find a darker one.$"

GraniteCave_B1F_Text_KV4Doug_Post:
	.string "There's a guy down the hall drawing\na map. Twelve years. He still asks\lme where the exit is.$"

GraniteCave_B1F_EventScript_KV4Graffiti::
	msgbox GraniteCave_B1F_Text_KV4Graffiti, MSGBOX_SIGN
	end

GraniteCave_B1F_Text_KV4Graffiti:
	.string "Scratched into the rock:\p“STEVEN WAS HERE.”\n“NO HE WASN'T. -STEVEN”$"
@ --- einde kaart_vulling_4 ---
