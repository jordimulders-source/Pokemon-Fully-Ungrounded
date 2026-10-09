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
	.string "I am the emissary of the sky. ARCEUS\n"
	.string "made the sky on the second day.\p"
	.string "I was made on the third. I'm still bitter\n"
	.string "about it.$"

HallOfOrigin_Stairway_Text_StratosDefeat:
	.string "Grounded. By you. The irony is not lost\n"
	.string "on me.$"

HallOfOrigin_Stairway_Text_StratosPost:
	.string "Above us there's only more of ARCEUS.\n"
	.string "Mind your head.$"

HallOfOrigin_Stairway_Text_ThalassaIntro:
	.string "Emissary of the sea. Yes, I'm in a\n"
	.string "swimsuit at the top of the sky.\p"
	.string "ARCEUS said 'dress for the job you\n"
	.string "want'.$"

HallOfOrigin_Stairway_Text_ThalassaDefeat:
	.string "Washed up. On a mountain. Somehow.$"

HallOfOrigin_Stairway_Text_ThalassaPost:
	.string "Every ocean in every dimension says hi.\n"
	.string "They're mostly salty about it.$"

HallOfOrigin_Stairway_Text_BedrockIntro:
	.string "Emissary of the land. Before there was\n"
	.string "ground, there was me, waiting to be\l"
	.string "stood on.\p"
	.string "Go on. Everyone does.$"

HallOfOrigin_Stairway_Text_BedrockDefeat:
	.string "Eroded. It happens to the best of us.\n"
	.string "Slowly, usually.$"

HallOfOrigin_Stairway_Text_BedrockPost:
	.string "The atrium is up the stairs. The stairs\n"
	.string "are me, technically. You're welcome.$"

HallOfOrigin_Stairway_Text_Fountain:
	.string "A pool of light, humming to itself. Your\n"
	.string "POKéMON drink from it and look\l"
	.string "healthier.\p"
	.string "You feel judged, but in a supportive\n"
	.string "way.$"
