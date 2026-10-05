MeteorFalls_B1F_2R_MapScripts::
	.byte 0

@ Project Grounded: het vergrote Bagon-bekken (kaart: tools/grounded/maptools/meteor_falls_ext.py).
@ Placeholderteksten; Jordi herschrijft ze via de Dialoogstudio.

MeteorFalls_B1F_2R_EventScript_Meteorite::
	msgbox MeteorFalls_B1F_2R_Text_Meteorite, MSGBOX_SIGN
	end

MeteorFalls_B1F_2R_EventScript_Drake::
	trainerbattle_single TRAINER_METEOR_DRAKE, MeteorFalls_B1F_2R_Text_DrakeIntro, MeteorFalls_B1F_2R_Text_DrakeDefeat
	msgbox MeteorFalls_B1F_2R_Text_DrakePostBattle, MSGBOX_AUTOCLOSE
	end

MeteorFalls_B1F_2R_Text_Meteorite:
	.string "A chunk of meteorite, still faintly\n"
	.string "warm after a few thousand years.\p"
	.string "Something has clearly been headbutting\n"
	.string "it. Repeatedly. With hope.$"

MeteorFalls_B1F_2R_Text_DrakeIntro:
	.string "Every Bagon down here dreams of\n"
	.string "flying. So do I.\p"
	.string "Neither of us has wings. One of us\n"
	.string "has a tax return. Battle!$"

MeteorFalls_B1F_2R_Text_DrakeDefeat:
	.string "Grounded. Again. Story of my life.$"

MeteorFalls_B1F_2R_Text_DrakePostBattle:
	.string "That crack in the north wall? I hit it\n"
	.string "with my head for a week.\p"
	.string "The Bagon said I was doing it wrong.$"
