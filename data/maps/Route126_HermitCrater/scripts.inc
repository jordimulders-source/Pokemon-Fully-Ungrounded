@ Project Grounded: bewoond kratertje bij Sootopolis (Route 126). Ingang: zwemgat in Underwater_Route126 24,14; terug = duiken in het donkere water.
@ Kaart en scripts: tools/grounded/maptools/sootopolis_craters.py (niet met de hand bewerken).
Route126_HermitCrater_MapScripts::
	map_script MAP_SCRIPT_ON_RESUME, Route126_HermitCrater_OnResume
	.byte 0

Route126_HermitCrater_OnResume:
	setdivewarp MAP_UNDERWATER_ROUTE126, 24, 15
	setescapewarp MAP_UNDERWATER_ROUTE126, 24, 15
	end

Route126_HermitCrater_EventScript_Lavis::
	trainerbattle_single TRAINER_LAVIS, Route126_HermitCrater_Text_LavisIntro, Route126_HermitCrater_Text_LavisDefeat
	msgbox Route126_HermitCrater_Text_LavisPost, MSGBOX_AUTOCLOSE
	end

Route126_HermitCrater_EventScript_Margot::
	trainerbattle_single TRAINER_SWIMMER_MARGOT, Route126_HermitCrater_Text_MargotIntro, Route126_HermitCrater_Text_MargotDefeat
	msgbox Route126_HermitCrater_Text_MargotPost, MSGBOX_AUTOCLOSE
	end

Route126_HermitCrater_EventScript_Fenna::
	trainerbattle_single TRAINER_AROMA_LADY_FENNA, Route126_HermitCrater_Text_FennaIntro, Route126_HermitCrater_Text_FennaDefeat
	msgbox Route126_HermitCrater_Text_FennaPost, MSGBOX_AUTOCLOSE
	end

Route126_HermitCrater_EventScript_Canvas::
	msgbox Route126_HermitCrater_Text_Canvas, MSGBOX_SIGN
	end

@ ---------------------------------------------------------------- teksten (placeholders, Jordi herschrijft ze)
Route126_HermitCrater_Text_LavisIntro:
	.string "Don't. Move.\p"
	.string "I have been painting this lake for\n"
	.string "thirty-one years. You are now IN it. Do\l"
	.string "you know what that does to a\l"
	.string "composition?$"

Route126_HermitCrater_Text_LavisDefeat:
	.string "Fine. You're in the painting. Small. In\n"
	.string "the corner. Drowning, but tastefully.$"

Route126_HermitCrater_Text_LavisPost:
	.string "My family guarded the SOOTOPOLIS\n"
	.string "crater for generations. I guard this\l"
	.string "one. It's smaller. Like my pension.\p"
	.string "WALLACE got the GYM. I got 'creative\n"
	.string "freedom'. It is mostly freedom to be\l"
	.string "alone with a lake that refuses to hold\l"
	.string "still.$"

Route126_HermitCrater_Text_MargotIntro:
	.string "Lap four thousand and twelve! The\n"
	.string "crater has no lanes, so I AM the lane.$"

Route126_HermitCrater_Text_MargotDefeat:
	.string "You broke my rhythm. And my team.\n"
	.string "Mostly the rhythm.$"

Route126_HermitCrater_Text_MargotPost:
	.string "Every lap I touch the wall and whisper\n"
	.string "'nearly'.\p"
	.string "Nearly what? Unclear. 'Nearly' is the\n"
	.string "whole point.$"

Route126_HermitCrater_Text_FennaIntro:
	.string "I came here for absolute silence. Then I\n"
	.string "brought a speaker. For the silence. So\l"
	.string "it's louder.$"

Route126_HermitCrater_Text_FennaDefeat:
	.string "Okay. That was loud.$"

Route126_HermitCrater_Text_FennaPost:
	.string "The painter says my COMFEY ruins his\n"
	.string "composition.\p"
	.string "My COMFEY says nothing. My COMFEY IS\n"
	.string "the composition.$"

Route126_HermitCrater_Text_Canvas:
	.string "A canvas is nailed to the tree. It shows\n"
	.string "this lake, very accurately.\p"
	.string "In the corner, a tiny figure is drowning.\n"
	.string "The paint is still wet.$"
