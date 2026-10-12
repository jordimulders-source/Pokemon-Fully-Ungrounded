@ Project Grounded: Koraalkathedraal onder Route 126 (kopie van ShoalCave_HighTideEntranceRoom + koraal).
@ Ingang: zwemgat in Underwater_Route126 (64,18); terug = duiken. Kaart en scripts: tools/grounded/maptools/coral_cathedral.py.
Route126_CoralCathedral_MapScripts::
	map_script MAP_SCRIPT_ON_RESUME, Route126_CoralCathedral_OnResume
	.byte 0

Route126_CoralCathedral_OnResume:
	setdivewarp MAP_UNDERWATER_ROUTE126, 64, 19
	setescapewarp MAP_UNDERWATER_ROUTE126, 64, 19
	end

Route126_CoralCathedral_EventScript_Plaque::
	msgbox Route126_CoralCathedral_Text_Plaque, MSGBOX_SIGN
	end

Route126_CoralCathedral_EventScript_Corinne::
	trainerbattle_single TRAINER_SWIMMER_CORINNE, Route126_CoralCathedral_Text_CorinneIntro, Route126_CoralCathedral_Text_CorinneDefeat
	msgbox Route126_CoralCathedral_Text_CorinnePost, MSGBOX_AUTOCLOSE
	end

Route126_CoralCathedral_EventScript_Dorian::
	trainerbattle_single TRAINER_FISHERMAN_DORIAN, Route126_CoralCathedral_Text_DorianIntro, Route126_CoralCathedral_Text_DorianDefeat
	msgbox Route126_CoralCathedral_Text_DorianPost, MSGBOX_AUTOCLOSE
	end

@ ---------------------------------------------------------------- teksten (placeholders, Jordi herschrijft ze)
Route126_CoralCathedral_Text_Plaque:
	.string "THE CORAL CATHEDRAL\p"
	.string "Services every Sunday. Current\n"
	.string "congregation: forty CORSOLA and one\l"
	.string "very confused LUVDISC.\p"
	.string "Please do not touch the pews. The pews\n"
	.string "are alive.$"

Route126_CoralCathedral_Text_CorinneIntro:
	.string "I've been swimming laps around this\n"
	.string "coral since I was six.\p"
	.string "It has not grown. I have. Neither of us\n"
	.string "is happy about it.$"

Route126_CoralCathedral_Text_CorinneDefeat:
	.string "Fine. I'll go back to my laps.$"

Route126_CoralCathedral_Text_CorinnePost:
	.string "Coral grows one centimeter a year.\p"
	.string "I did the math. I will be dead before it\n"
	.string "reaches the ceiling. So will you. Sleep\l"
	.string "well.$"

Route126_CoralCathedral_Text_DorianIntro:
	.string "Fishing in a cathedral? The sign didn't\n"
	.string "say I couldn't.\p"
	.string "The sign also didn't say I could. That's\n"
	.string "what lawyers call a gray area.$"

Route126_CoralCathedral_Text_DorianDefeat:
	.string "My line snapped. A sign from above.$"

Route126_CoralCathedral_Text_DorianPost:
	.string "I caught a LUVDISC here once. It looked\n"
	.string "at me like I'd ruined its wedding.\p"
	.string "I let it go. I still think about it.$"
