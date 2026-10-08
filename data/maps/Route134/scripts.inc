Route134_MapScripts::
	map_script MAP_SCRIPT_ON_RESUME, Route134_OnResume
	.byte 0

Route134_OnResume:
	setdivewarp MAP_UNDERWATER_ROUTE134, 8, 6
	end

Route134_EventScript_Jack::
	trainerbattle_single TRAINER_JACK, Route134_Text_JackIntro, Route134_Text_JackDefeat
	msgbox Route134_Text_JackPostBattle, MSGBOX_AUTOCLOSE
	end

Route134_EventScript_Laurel::
	trainerbattle_single TRAINER_LAUREL, Route134_Text_LaurelIntro, Route134_Text_LaurelDefeat
	msgbox Route134_Text_LaurelPostBattle, MSGBOX_AUTOCLOSE
	end

Route134_EventScript_Alex::
	trainerbattle_single TRAINER_ALEX, Route134_Text_AlexIntro, Route134_Text_AlexDefeat
	msgbox Route134_Text_AlexPostBattle, MSGBOX_AUTOCLOSE
	end

Route134_EventScript_Aaron::
	trainerbattle_single TRAINER_AARON, Route134_Text_AaronIntro, Route134_Text_AaronDefeat
	msgbox Route134_Text_AaronPostBattle, MSGBOX_AUTOCLOSE
	end

Route134_EventScript_Hitoshi::
	trainerbattle_single TRAINER_HITOSHI, Route134_Text_HitoshiIntro, Route134_Text_HitoshiDefeat
	msgbox Route134_Text_HitoshiPostBattle, MSGBOX_AUTOCLOSE
	end

Route134_EventScript_Hudson::
	trainerbattle_single TRAINER_HUDSON, Route134_Text_HudsonIntro, Route134_Text_HudsonDefeat
	msgbox Route134_Text_HudsonPostBattle, MSGBOX_AUTOCLOSE
	end

Route134_EventScript_Reyna::
	trainerbattle_single TRAINER_REYNA, Route134_Text_ReynaIntro, Route134_Text_ReynaDefeat
	msgbox Route134_Text_ReynaPostBattle, MSGBOX_AUTOCLOSE
	end

Route134_EventScript_Marley::
	trainerbattle_single TRAINER_MARLEY, Route134_Text_MarleyIntro, Route134_Text_MarleyDefeat
	msgbox Route134_Text_MarleyPostBattle, MSGBOX_AUTOCLOSE
	end

Route134_EventScript_Kelvin::
	trainerbattle_single TRAINER_KELVIN, Route134_Text_KelvinIntro, Route134_Text_KelvinDefeat
	msgbox Route134_Text_KelvinPostBattle, MSGBOX_AUTOCLOSE
	end

@ --- zee_vulling_2 (gegenereerd door tools/grounded/maptools/zee_vulling_2.py) ---
Route134_EventScript_ZV2Architect::
	msgbox Route134_Text_ZV2Architect, MSGBOX_NPC
	end

Route134_Text_ZV2Architect:
	.string "This is where the lighthouse goes.\nBig. White. Stripes. A light.\pProblem: nobody in HOENN knows what\na lighthouse looks like.\pI asked around. Someone drew me a\nvery tall PEEKO. I'm considering it.\p...Wait. There's one south of ROUTE 133\nalready? And the lamp is a LANTURN?\pCheater.$"

Route134_EventScript_ZV2Kage::
	trainerbattle_single TRAINER_NINJA_BOY_KAGE, Route134_Text_ZV2Kage_Intro, Route134_Text_ZV2Kage_Defeat
	msgbox Route134_Text_ZV2Kage_Post, MSGBOX_AUTOCLOSE
	end

Route134_Text_ZV2Kage_Intro:
	.string "...!\pYou saw me?! I was hiding! In the\nsand! In full black clothing!$"

Route134_Text_ZV2Kage_Defeat:
	.string "My disguise needs work.\nMaybe a beige ninja.$"

Route134_Text_ZV2Kage_Post:
	.string "The architect thinks I'm a\nlighthouse. I'm not correcting him.$"
@ --- einde zee_vulling_2 ---

@ --- zee_vulling_4 (gegenereerd door tools/grounded/maptools/zee_vulling_4.py) ---
Route134_EventScript_ZV4Dorian::
	trainerbattle_single TRAINER_RUIN_MANIAC_DORIAN, Route134_Text_ZV4Dorian_Intro, Route134_Text_ZV4Dorian_Defeat
	msgbox Route134_Text_ZV4Dorian_Post, MSGBOX_AUTOCLOSE
	end

Route134_Text_ZV4Dorian_Intro:
	.string "Somewhere under this sea is a\nSEALED CHAMBER. With BRAILLE.\pI can't read braille.\nI brought a shovel. Same thing.$"

Route134_Text_ZV4Dorian_Defeat:
	.string "My shovel isn't waterproof.\nNeither am I.$"

Route134_Text_ZV4Dorian_Post:
	.string "The chamber is south of here,\ndeep down. They say you need a\lWAILORD and a RELICANTH to open it.\pI have a RELICANTH. My WAILORD\nis in a different chamber.\lIt's called 'the PC'.$"
@ --- einde zee_vulling_4 ---
