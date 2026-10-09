@ Project Grounded: HallOfOrigin_Stairway (tools/grounded/maptools/hall_of_origin.py)
HallOfOrigin_Stairway_MapScripts::
	.byte 0

HallOfOrigin_Stairway_EventScript_Stratos::
	trainerbattle_single TRAINER_HOO_STRATOS, HallOfOrigin_Stairway_Text_StratosIntro, HallOfOrigin_Stairway_Text_StratosDefeat
	msgbox HallOfOrigin_Stairway_Text_StratosPost, MSGBOX_AUTOCLOSE
	end

HallOfOrigin_Stairway_EventScript_Thalassa::
	trainerbattle_single TRAINER_HOO_THALASSA, HallOfOrigin_Stairway_Text_ThalassaIntro, HallOfOrigin_Stairway_Text_ThalassaDefeat
	msgbox HallOfOrigin_Stairway_Text_ThalassaPost, MSGBOX_AUTOCLOSE
	end

HallOfOrigin_Stairway_EventScript_Bedrock::
	trainerbattle_single TRAINER_HOO_BEDROCK, HallOfOrigin_Stairway_Text_BedrockIntro, HallOfOrigin_Stairway_Text_BedrockDefeat
	msgbox HallOfOrigin_Stairway_Text_BedrockPost, MSGBOX_AUTOCLOSE
	end

HallOfOrigin_Stairway_EventScript_Fountain::
	lockall
	fadescreen FADE_TO_WHITE
	special HealPlayerParty
	fadescreen FADE_FROM_WHITE
	msgbox HallOfOrigin_Stairway_Text_Fountain, MSGBOX_DEFAULT
	releaseall
	end

@ ---------------------------------------------------------------- teksten (placeholders, Jordi herschrijft ze)
HallOfOrigin_Stairway_Text_StratosIntro:
	.string "CONSTRUCT ONLINE. DESIGNATION: SKY.\p"
	.string "ARCEUS carved me out of a cloud. It\n"
	.string "took six tries. The other five drifted\l"
	.string "off.$"

HallOfOrigin_Stairway_Text_StratosDefeat:
	.string "Altitude... lost. Filing a complaint with\n"
	.string "gravity.$"

HallOfOrigin_Stairway_Text_StratosPost:
	.string "My maker watches through my eyes. Wave.\n"
	.string "No, the other eye.$"

HallOfOrigin_Stairway_Text_ThalassaIntro:
	.string "CONSTRUCT ONLINE. DESIGNATION: SEA.\p"
	.string "I am made of stone and I guard the\n"
	.string "ocean. Nobody at the planning meeting\l"
	.string "saw the problem.$"

HallOfOrigin_Stairway_Text_ThalassaDefeat:
	.string "Sinking. As predicted. By everyone.$"

HallOfOrigin_Stairway_Text_ThalassaPost:
	.string "Every ocean in every dimension says hi.\n"
	.string "They're mostly salty about it.$"

HallOfOrigin_Stairway_Text_BedrockIntro:
	.string "CONSTRUCT ONLINE. DESIGNATION: LAND.\p"
	.string "I was the first thing ARCEUS made after\n"
	.string "the floor. Technically, I am also the\l"
	.string "floor.$"

HallOfOrigin_Stairway_Text_BedrockDefeat:
	.string "Eroded. It happens to the best of us.\n"
	.string "Slowly, usually.$"

HallOfOrigin_Stairway_Text_BedrockPost:
	.string "Mind the steps. They're my cousins. They\n"
	.string "bite.$"

HallOfOrigin_Stairway_Text_Fountain:
	.string "A pool of light, humming to itself. Your\n"
	.string "POKéMON drink from it and look\l"
	.string "healthier.\p"
	.string "You feel judged, but in a supportive\n"
	.string "way.$"
